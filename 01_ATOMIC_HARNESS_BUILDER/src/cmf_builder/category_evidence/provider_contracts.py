from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from hashlib import sha256
import json
import re
from typing import Any, Mapping


SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
ENVIRONMENT_NAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class ProviderContractError(ValueError):
    """Raised when provider evidence would violate its governed contract."""


class NetworkPolicy(StrEnum):
    DENY = "DENY"
    ALLOWLIST = "ALLOWLIST"


class OutputFormat(StrEnum):
    JSON = "JSON"
    TEXT = "TEXT"


class StreamPolicy(StrEnum):
    CAPTURE_UTF8 = "CAPTURE_UTF8"
    DISCARD = "DISCARD"


class FailureCode(StrEnum):
    AUTHORITY_MISSING = "AUTHORITY_MISSING"
    AUTHORITY_SCOPE_MISMATCH = "AUTHORITY_SCOPE_MISMATCH"
    CANCELLED = "CANCELLED"
    CONFIGURATION_DRIFT = "CONFIGURATION_DRIFT"
    CONFIGURATION_INVALID = "CONFIGURATION_INVALID"
    EXECUTABLE_DRIFT = "EXECUTABLE_DRIFT"
    INVOCATION_FAILED = "INVOCATION_FAILED"
    OUTPUT_INVALID = "OUTPUT_INVALID"
    RUNTIME_VERSION_DRIFT = "RUNTIME_VERSION_DRIFT"
    TIMEOUT = "TIMEOUT"


def canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha256_hex(value: bytes) -> str:
    return sha256(value).hexdigest()


def _require_sha256(value: str, field_name: str) -> None:
    if not SHA256_PATTERN.fullmatch(value):
        raise ProviderContractError(f"{field_name} must be a lowercase SHA-256")


def _require_unique(values: tuple[str, ...], field_name: str) -> None:
    if len(values) != len(set(values)):
        raise ProviderContractError(f"{field_name} contains duplicate values")


@dataclass(frozen=True, slots=True)
class DeterministicControls:
    seed: int | None
    seed_support: str
    temperature: str
    repeat_count: int
    additional_controls: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if self.seed_support not in {"SUPPORTED", "UNSUPPORTED", "UNKNOWN"}:
            raise ProviderContractError("seed_support is not governed")
        if self.seed_support == "SUPPORTED" and self.seed is None:
            raise ProviderContractError("a supported seed must be pinned")
        if self.seed_support == "UNSUPPORTED" and self.seed is not None:
            raise ProviderContractError("an unsupported seed cannot be supplied")
        if not self.temperature:
            raise ProviderContractError("temperature or equivalent must be explicit")
        if self.repeat_count < 1:
            raise ProviderContractError("repeat_count must be positive")
        names = tuple(name for name, _ in self.additional_controls)
        _require_unique(names, "additional_controls")
        if tuple(sorted(self.additional_controls)) != self.additional_controls:
            raise ProviderContractError("additional_controls must be canonically ordered")

    def payload(self) -> dict[str, Any]:
        return {
            "additional_controls": [list(item) for item in self.additional_controls],
            "repeat_count": self.repeat_count,
            "seed": self.seed,
            "seed_support": self.seed_support,
            "temperature": self.temperature,
        }


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    maximum_attempts: int
    retryable_exit_codes: tuple[int, ...] = ()
    retry_timeouts: bool = False

    def __post_init__(self) -> None:
        if self.maximum_attempts < 1:
            raise ProviderContractError("maximum_attempts must be positive")
        if len(self.retryable_exit_codes) != len(set(self.retryable_exit_codes)):
            raise ProviderContractError("retryable_exit_codes contains duplicates")
        if tuple(sorted(self.retryable_exit_codes)) != self.retryable_exit_codes:
            raise ProviderContractError("retryable_exit_codes must be canonically ordered")


@dataclass(frozen=True, slots=True)
class ProviderConfiguration:
    configuration_id: str
    provider_identity: str
    provider_version: str
    runtime_identity: str
    runtime_version: str
    executable_name: str
    executable_sha256: str
    package_identity: str
    package_version: str
    package_sha256: str
    model_identity: str
    invocation_method: str
    invocation_argv: tuple[str, ...]
    version_probe_argv: tuple[str, ...]
    deterministic_controls: DeterministicControls
    timeout_seconds: int
    working_directory_boundary: str
    allowed_tools: tuple[str, ...]
    prohibited_tools: tuple[str, ...]
    network_policy: NetworkPolicy
    network_allowlist: tuple[str, ...]
    credential_environment_names: tuple[str, ...]
    retry_policy: RetryPolicy
    output_format: OutputFormat
    stdout_policy: StreamPolicy
    stderr_policy: StreamPolicy
    accepted_exit_codes: tuple[int, ...]
    may_incur_cost: bool
    requires_credentials: bool
    semantic_provider: bool
    policy_enforcement: str

    def __post_init__(self) -> None:
        for name in (
            "configuration_id",
            "provider_identity",
            "provider_version",
            "runtime_identity",
            "runtime_version",
            "executable_name",
            "package_identity",
            "package_version",
            "model_identity",
            "invocation_method",
            "working_directory_boundary",
            "policy_enforcement",
        ):
            if not getattr(self, name):
                raise ProviderContractError(f"{name} is required")
        _require_sha256(self.executable_sha256, "executable_sha256")
        _require_sha256(self.package_sha256, "package_sha256")
        if self.timeout_seconds < 1:
            raise ProviderContractError("timeout_seconds must be positive")
        if not self.invocation_argv:
            raise ProviderContractError("invocation_argv must be explicit")
        if not self.version_probe_argv:
            raise ProviderContractError("version_probe_argv must be explicit")
        for field_name, values in (
            ("allowed_tools", self.allowed_tools),
            ("prohibited_tools", self.prohibited_tools),
            ("network_allowlist", self.network_allowlist),
            ("credential_environment_names", self.credential_environment_names),
            ("accepted_exit_codes", self.accepted_exit_codes),
        ):
            _require_unique(values, field_name)
            if tuple(sorted(values)) != values:
                raise ProviderContractError(f"{field_name} must be canonically ordered")
        if set(self.allowed_tools).intersection(self.prohibited_tools):
            raise ProviderContractError("a tool cannot be both allowed and prohibited")
        if self.network_policy is NetworkPolicy.DENY and self.network_allowlist:
            raise ProviderContractError("DENY network policy cannot have an allowlist")
        if self.network_policy is NetworkPolicy.ALLOWLIST and not self.network_allowlist:
            raise ProviderContractError("ALLOWLIST network policy requires hosts")
        for name in self.credential_environment_names:
            if not ENVIRONMENT_NAME_PATTERN.fullmatch(name):
                raise ProviderContractError(
                    "credential environment fields contain names only, never values"
                )
        if self.requires_credentials and not self.credential_environment_names:
            raise ProviderContractError("credential names are required but absent")
        if not self.accepted_exit_codes:
            raise ProviderContractError("accepted_exit_codes must be explicit")

    def payload(self) -> dict[str, Any]:
        value = asdict(self)
        value["deterministic_controls"] = self.deterministic_controls.payload()
        value["network_policy"] = self.network_policy.value
        value["output_format"] = self.output_format.value
        value["stdout_policy"] = self.stdout_policy.value
        value["stderr_policy"] = self.stderr_policy.value
        value["retry_policy"] = asdict(self.retry_policy)
        for name in (
            "invocation_argv",
            "version_probe_argv",
            "allowed_tools",
            "prohibited_tools",
            "network_allowlist",
            "credential_environment_names",
            "accepted_exit_codes",
        ):
            value[name] = list(value[name])
        value["retry_policy"]["retryable_exit_codes"] = list(
            value["retry_policy"]["retryable_exit_codes"]
        )
        return value

    @property
    def configuration_hash(self) -> str:
        return sha256_hex(canonical_json_bytes(self.payload()))


@dataclass(frozen=True, slots=True)
class ProviderRunRequest:
    request_id: str
    configuration_id: str
    configuration_hash: str
    model_identity: str
    input_bytes: bytes
    deterministic_controls: DeterministicControls
    call_ordinal: int
    repeat_index: int
    requested_tools: tuple[str, ...] = ()
    requested_network_hosts: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ProviderContractError("request_id is required")
        _require_sha256(self.configuration_hash, "configuration_hash")
        if self.call_ordinal < 1:
            raise ProviderContractError("call_ordinal is one-based and must be positive")
        if self.repeat_index < 0:
            raise ProviderContractError("repeat_index cannot be negative")
        if tuple(sorted(self.requested_tools)) != self.requested_tools:
            raise ProviderContractError("requested_tools must be canonically ordered")
        if tuple(sorted(self.requested_network_hosts)) != self.requested_network_hosts:
            raise ProviderContractError(
                "requested_network_hosts must be canonically ordered"
            )

    def payload(self) -> dict[str, Any]:
        return {
            "call_ordinal": self.call_ordinal,
            "configuration_hash": self.configuration_hash,
            "configuration_id": self.configuration_id,
            "deterministic_controls": self.deterministic_controls.payload(),
            "input_sha256": sha256_hex(self.input_bytes),
            "model_identity": self.model_identity,
            "repeat_index": self.repeat_index,
            "request_id": self.request_id,
            "requested_network_hosts": list(self.requested_network_hosts),
            "requested_tools": list(self.requested_tools),
        }

    @property
    def request_hash(self) -> str:
        return sha256_hex(canonical_json_bytes(self.payload()))


@dataclass(frozen=True, slots=True)
class ProviderRunAuthority:
    authority_receipt_id: str
    configuration_hash: str
    maximum_calls: int
    maximum_repeats: int
    maximum_expected_cost: str
    data_classes: tuple[str, ...]
    credential_environment_names: tuple[str, ...]
    retention_policy: str

    def __post_init__(self) -> None:
        if not self.authority_receipt_id:
            raise ProviderContractError("authority_receipt_id is required")
        _require_sha256(self.configuration_hash, "configuration_hash")
        if self.maximum_calls < 1 or self.maximum_repeats < 1:
            raise ProviderContractError("authority call and repeat bounds must be positive")
        if not self.maximum_expected_cost or not self.retention_policy:
            raise ProviderContractError("cost and retention bounds must be explicit")
        for field_name, values in (
            ("data_classes", self.data_classes),
            ("credential_environment_names", self.credential_environment_names),
        ):
            _require_unique(values, field_name)
            if tuple(sorted(values)) != values:
                raise ProviderContractError(f"{field_name} must be canonically ordered")
        for name in self.credential_environment_names:
            if not ENVIRONMENT_NAME_PATTERN.fullmatch(name):
                raise ProviderContractError("authority records credential names only")


@dataclass(frozen=True, slots=True)
class ProviderFailure:
    code: FailureCode
    message: str
    attempt: int
    retryable: bool


@dataclass(frozen=True, slots=True)
class OutputCaptureManifest:
    manifest_id: str
    configuration_hash: str
    request_hash: str
    attempt_count: int
    exit_code: int | None
    exit_status: str
    stdout_sha256: str
    stderr_sha256: str
    stdout_bytes: bytes
    stderr_bytes: bytes
    output_format: OutputFormat
    runtime_duration_ms: int
    authority_receipt_id: str | None
    failures: tuple[ProviderFailure, ...]

    @property
    def passed(self) -> bool:
        return self.exit_status == "PASS"
