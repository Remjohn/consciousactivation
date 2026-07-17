from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest

from cmf_builder.category_evidence.provider_contracts import (
    DeterministicControls,
    NetworkPolicy,
    OutputFormat,
    ProviderConfiguration,
    ProviderContractError,
    ProviderRunRequest,
    RetryPolicy,
    StreamPolicy,
    sha256_hex,
)


CONTROLS = DeterministicControls(
    seed=7,
    seed_support="SUPPORTED",
    temperature="0",
    repeat_count=3,
)


def python_sha256() -> str:
    return sha256_hex(Path(sys.executable).read_bytes())


def configuration(**changes) -> ProviderConfiguration:
    value = ProviderConfiguration(
        configuration_id="BD007-LOCAL-NONSEMANTIC-FIXTURE-v1",
        provider_identity="repository_local_test_fixture",
        provider_version="1.0.0",
        runtime_identity="CPython",
        runtime_version=f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        executable_name=Path(sys.executable).name,
        executable_sha256=python_sha256(),
        package_identity="tests/category_native_evidence/provider_runner/provider_fixture.py",
        package_version="1.0.0",
        package_sha256=sha256_hex((Path(__file__).parent / "provider_fixture.py").read_bytes()),
        model_identity="NON_SEMANTIC_ECHO_FIXTURE",
        invocation_method="SUBPROCESS_STDIN_STDOUT",
        invocation_argv=("provider_fixture.py", "echo-json"),
        version_probe_argv=("--version",),
        deterministic_controls=CONTROLS,
        timeout_seconds=2,
        working_directory_boundary="CALLER_PINNED_BOUNDARY",
        allowed_tools=(),
        prohibited_tools=("network", "shell"),
        network_policy=NetworkPolicy.DENY,
        network_allowlist=(),
        credential_environment_names=(),
        retry_policy=RetryPolicy(maximum_attempts=1),
        output_format=OutputFormat.JSON,
        stdout_policy=StreamPolicy.CAPTURE_UTF8,
        stderr_policy=StreamPolicy.CAPTURE_UTF8,
        accepted_exit_codes=(0,),
        may_incur_cost=False,
        requires_credentials=False,
        semantic_provider=False,
        policy_enforcement="TEST_FIXTURE_PROCESS_BOUNDARY",
    )
    return replace(value, **changes)


def request(config: ProviderConfiguration, **changes) -> ProviderRunRequest:
    value = ProviderRunRequest(
        request_id="request-001",
        configuration_id=config.configuration_id,
        configuration_hash=config.configuration_hash,
        model_identity=config.model_identity,
        input_bytes=b'{"meaning":"unchanged"}',
        deterministic_controls=CONTROLS,
        call_ordinal=1,
        repeat_index=0,
    )
    return replace(value, **changes)


def test_configuration_hash_is_canonical_and_changes_on_policy_drift() -> None:
    first = configuration()
    second = configuration()
    assert first.configuration_hash == second.configuration_hash
    assert len(first.configuration_hash) == 64
    assert replace(first, timeout_seconds=3).configuration_hash != first.configuration_hash


def test_request_hash_binds_exact_input_and_configuration() -> None:
    config = configuration()
    original = request(config)
    changed = replace(original, input_bytes=b'{"meaning":"changed"}')
    assert original.request_hash != changed.request_hash
    assert replace(original, call_ordinal=2).request_hash != original.request_hash


@pytest.mark.parametrize(
    "changes",
    [
        {"credential_environment_names": ("API_KEY=secret",)},
        {"network_policy": NetworkPolicy.DENY, "network_allowlist": ("example.com",)},
        {"allowed_tools": ("shell",), "prohibited_tools": ("shell",)},
        {"accepted_exit_codes": ()},
    ],
)
def test_invalid_or_secret_bearing_configuration_fails_closed(changes) -> None:
    with pytest.raises(ProviderContractError):
        configuration(**changes)


def test_configuration_records_environment_names_not_values() -> None:
    config = configuration(
        credential_environment_names=("OPENAI_API_KEY",),
        requires_credentials=True,
        may_incur_cost=True,
    )
    payload = config.payload()
    assert payload["credential_environment_names"] == ["OPENAI_API_KEY"]
    assert "secret" not in str(payload).lower()
