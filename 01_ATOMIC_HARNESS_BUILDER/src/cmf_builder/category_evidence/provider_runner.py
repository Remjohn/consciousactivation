from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
from threading import Event
from time import monotonic, sleep

from cmf_builder.category_evidence.provider_contracts import (
    FailureCode,
    OutputCaptureManifest,
    OutputFormat,
    ProviderConfiguration,
    ProviderContractError,
    ProviderFailure,
    ProviderRunAuthority,
    ProviderRunRequest,
    StreamPolicy,
    canonical_json_bytes,
    sha256_hex,
)


class ProviderExecutionRejected(RuntimeError):
    def __init__(self, failure: ProviderFailure) -> None:
        super().__init__(failure.message)
        self.failure = failure


@dataclass(slots=True)
class CancellationToken:
    _event: Event

    @classmethod
    def create(cls) -> "CancellationToken":
        return cls(Event())

    def cancel(self) -> None:
        self._event.set()

    @property
    def cancelled(self) -> bool:
        return self._event.is_set()


class GovernedProviderRunner:
    """Development evidence runner; it does not grant provider eligibility."""

    def verify_configuration(
        self,
        *,
        configuration: ProviderConfiguration,
        request: ProviderRunRequest,
        executable_path: Path,
        package_path: Path,
        working_directory: Path,
        working_directory_boundary: Path,
        authority: ProviderRunAuthority | None,
    ) -> None:
        if request.configuration_id != configuration.configuration_id:
            self._reject(FailureCode.CONFIGURATION_DRIFT, "configuration id drift")
        if request.configuration_hash != configuration.configuration_hash:
            self._reject(FailureCode.CONFIGURATION_DRIFT, "configuration hash drift")
        if request.model_identity != configuration.model_identity:
            self._reject(FailureCode.CONFIGURATION_DRIFT, "model identity drift")
        if request.deterministic_controls != configuration.deterministic_controls:
            self._reject(FailureCode.CONFIGURATION_DRIFT, "deterministic-control drift")
        if request.repeat_index >= configuration.deterministic_controls.repeat_count:
            self._reject(FailureCode.CONFIGURATION_DRIFT, "repeat index exceeds policy")
        if not set(request.requested_tools).issubset(configuration.allowed_tools):
            self._reject(FailureCode.CONFIGURATION_DRIFT, "requested tool is not allowed")
        if set(request.requested_tools).intersection(configuration.prohibited_tools):
            self._reject(FailureCode.CONFIGURATION_DRIFT, "prohibited tool requested")
        if configuration.network_policy.value == "DENY" and request.requested_network_hosts:
            self._reject(FailureCode.CONFIGURATION_DRIFT, "network denied by configuration")
        if not set(request.requested_network_hosts).issubset(
            configuration.network_allowlist
        ):
            self._reject(FailureCode.CONFIGURATION_DRIFT, "network allowlist drift")

        executable = executable_path.resolve(strict=True)
        if executable.name.casefold() != configuration.executable_name.casefold():
            self._reject(FailureCode.EXECUTABLE_DRIFT, "executable name drift")
        if sha256(executable.read_bytes()).hexdigest() != configuration.executable_sha256:
            self._reject(FailureCode.EXECUTABLE_DRIFT, "executable byte hash drift")
        package = package_path.resolve(strict=True)
        if sha256(package.read_bytes()).hexdigest() != configuration.package_sha256:
            self._reject(FailureCode.CONFIGURATION_DRIFT, "package byte hash drift")

        boundary = working_directory_boundary.resolve(strict=True)
        directory = working_directory.resolve(strict=True)
        if not directory.is_relative_to(boundary):
            self._reject(
                FailureCode.CONFIGURATION_DRIFT,
                "working directory escapes the governed boundary",
            )
        if configuration.working_directory_boundary != "CALLER_PINNED_BOUNDARY":
            self._reject(
                FailureCode.CONFIGURATION_INVALID,
                "runner supports only caller-pinned working-directory boundaries",
            )

        if (
            configuration.semantic_provider
            or configuration.may_incur_cost
            or configuration.requires_credentials
        ):
            if authority is None:
                self._reject(
                    FailureCode.AUTHORITY_MISSING,
                    "credentialed or billable calls require a governed authority receipt",
                )
            self._verify_authority(configuration, request, authority)

    def run(
        self,
        *,
        configuration: ProviderConfiguration,
        request: ProviderRunRequest,
        executable_path: Path,
        package_path: Path,
        working_directory: Path,
        working_directory_boundary: Path,
        authority: ProviderRunAuthority | None = None,
        cancellation: CancellationToken | None = None,
        inherited_environment: dict[str, str] | None = None,
    ) -> OutputCaptureManifest:
        self.verify_configuration(
            configuration=configuration,
            request=request,
            executable_path=executable_path,
            package_path=package_path,
            working_directory=working_directory,
            working_directory_boundary=working_directory_boundary,
            authority=authority,
        )
        self._verify_runtime_version(configuration, executable_path, working_directory)

        environment_source = os.environ if inherited_environment is None else inherited_environment
        child_environment = {
            name: environment_source[name]
            for name in configuration.credential_environment_names
            if name in environment_source
        }
        missing_names = set(configuration.credential_environment_names).difference(
            child_environment
        )
        if configuration.requires_credentials and missing_names:
            self._reject(
                FailureCode.AUTHORITY_MISSING,
                "authorized credential environment name is unavailable",
            )

        failures: list[ProviderFailure] = []
        started = monotonic()
        stdout = b""
        stderr = b""
        exit_code: int | None = None
        exit_status = "FAIL"
        attempts = 0
        for attempt in range(1, configuration.retry_policy.maximum_attempts + 1):
            attempts = attempt
            result = self._invoke_once(
                configuration=configuration,
                request=request,
                executable_path=executable_path,
                working_directory=working_directory,
                environment=child_environment,
                cancellation=cancellation,
                attempt=attempt,
            )
            stdout, stderr, exit_code, failure = result
            if failure is None:
                exit_status = "PASS"
                break
            failures.append(failure)
            if not failure.retryable or attempt == configuration.retry_policy.maximum_attempts:
                break

        if exit_status == "PASS":
            self._verify_output(configuration.output_format, stdout)
        duration_ms = max(0, round((monotonic() - started) * 1000))
        identity_payload = {
            "authority_receipt_id": (
                authority.authority_receipt_id if authority is not None else None
            ),
            "configuration_hash": configuration.configuration_hash,
            "exit_code": exit_code,
            "exit_status": exit_status,
            "request_hash": request.request_hash,
            "stderr_sha256": sha256_hex(stderr),
            "stdout_sha256": sha256_hex(stdout),
        }
        manifest_id = f"provider-output:{sha256_hex(canonical_json_bytes(identity_payload))}"
        return OutputCaptureManifest(
            manifest_id=manifest_id,
            configuration_hash=configuration.configuration_hash,
            request_hash=request.request_hash,
            attempt_count=attempts,
            exit_code=exit_code,
            exit_status=exit_status,
            stdout_sha256=sha256_hex(stdout),
            stderr_sha256=sha256_hex(stderr),
            stdout_bytes=(
                stdout if configuration.stdout_policy is StreamPolicy.CAPTURE_UTF8 else b""
            ),
            stderr_bytes=(
                stderr if configuration.stderr_policy is StreamPolicy.CAPTURE_UTF8 else b""
            ),
            output_format=configuration.output_format,
            runtime_duration_ms=duration_ms,
            authority_receipt_id=(
                authority.authority_receipt_id if authority is not None else None
            ),
            failures=tuple(failures),
        )

    def _invoke_once(
        self,
        *,
        configuration: ProviderConfiguration,
        request: ProviderRunRequest,
        executable_path: Path,
        working_directory: Path,
        environment: dict[str, str],
        cancellation: CancellationToken | None,
        attempt: int,
    ) -> tuple[bytes, bytes, int | None, ProviderFailure | None]:
        process = subprocess.Popen(
            [str(executable_path), *configuration.invocation_argv],
            cwd=working_directory,
            env=environment,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        input_value: bytes | None = request.input_bytes
        started = monotonic()
        while True:
            if cancellation is not None and cancellation.cancelled:
                process.kill()
                stdout, stderr = process.communicate()
                return stdout, stderr, process.returncode, ProviderFailure(
                    FailureCode.CANCELLED,
                    "provider evidence call cancelled",
                    attempt,
                    False,
                )
            elapsed = monotonic() - started
            if elapsed >= configuration.timeout_seconds:
                process.kill()
                stdout, stderr = process.communicate()
                return stdout, stderr, process.returncode, ProviderFailure(
                    FailureCode.TIMEOUT,
                    "provider evidence call timed out",
                    attempt,
                    configuration.retry_policy.retry_timeouts,
                )
            try:
                stdout, stderr = process.communicate(input=input_value, timeout=0.05)
                input_value = None
                break
            except subprocess.TimeoutExpired:
                input_value = None
                sleep(0.001)
        exit_code = process.returncode
        if exit_code not in configuration.accepted_exit_codes:
            return stdout, stderr, exit_code, ProviderFailure(
                FailureCode.INVOCATION_FAILED,
                f"provider process exited with {exit_code}",
                attempt,
                exit_code in configuration.retry_policy.retryable_exit_codes,
            )
        return stdout, stderr, exit_code, None

    def _verify_runtime_version(
        self,
        configuration: ProviderConfiguration,
        executable_path: Path,
        working_directory: Path,
    ) -> None:
        try:
            probe = subprocess.run(
                [str(executable_path), *configuration.version_probe_argv],
                cwd=working_directory,
                env={},
                capture_output=True,
                timeout=configuration.timeout_seconds,
                check=False,
            )
            observed = (probe.stdout + probe.stderr).decode(
                "utf-8", errors="strict"
            ).strip()
        except subprocess.TimeoutExpired:
            self._reject(FailureCode.TIMEOUT, "runtime version probe timed out")
        except UnicodeDecodeError:
            self._reject(
                FailureCode.RUNTIME_VERSION_DRIFT,
                "runtime version probe was not strict UTF-8",
            )
        if probe.returncode != 0 or observed != configuration.runtime_version:
            self._reject(
                FailureCode.RUNTIME_VERSION_DRIFT,
                f"runtime version drift: observed {observed!r}",
            )

    @staticmethod
    def _verify_authority(
        configuration: ProviderConfiguration,
        request: ProviderRunRequest,
        authority: ProviderRunAuthority,
    ) -> None:
        if authority.configuration_hash != configuration.configuration_hash:
            GovernedProviderRunner._reject(
                FailureCode.AUTHORITY_SCOPE_MISMATCH,
                "authority is bound to another configuration",
            )
        if request.repeat_index >= authority.maximum_repeats:
            GovernedProviderRunner._reject(
                FailureCode.AUTHORITY_SCOPE_MISMATCH,
                "repeat exceeds authority",
            )
        if request.call_ordinal > authority.maximum_calls:
            GovernedProviderRunner._reject(
                FailureCode.AUTHORITY_SCOPE_MISMATCH,
                "call ordinal exceeds authority",
            )
        if tuple(configuration.credential_environment_names) != tuple(
            authority.credential_environment_names
        ):
            GovernedProviderRunner._reject(
                FailureCode.AUTHORITY_SCOPE_MISMATCH,
                "credential-name scope differs from authority",
            )

    @staticmethod
    def _verify_output(output_format: OutputFormat, stdout: bytes) -> None:
        try:
            decoded = stdout.decode("utf-8", errors="strict")
            if output_format is OutputFormat.JSON:
                json.loads(decoded)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            GovernedProviderRunner._reject(
                FailureCode.OUTPUT_INVALID,
                f"output does not satisfy {output_format.value}: {exc}",
            )

    @staticmethod
    def _reject(code: FailureCode, message: str) -> None:
        raise ProviderExecutionRejected(
            ProviderFailure(code=code, message=message, attempt=0, retryable=False)
        )
