from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
from pathlib import Path
import sys
from threading import Thread
from time import sleep

import pytest

from cmf_builder.category_evidence.provider_contracts import (
    FailureCode,
    OutputFormat,
    ProviderRunAuthority,
    RetryPolicy,
)
from cmf_builder.category_evidence.provider_runner import (
    CancellationToken,
    GovernedProviderRunner,
    ProviderExecutionRejected,
)
from tests.category_native_evidence.provider_runner.test_provider_contracts import (
    configuration,
    request,
)


HERE = Path(__file__).parent
EXECUTABLE = Path(sys.executable)


def run(config=None, requested=None, authority=None, cancellation=None):
    config = config or configuration()
    requested = requested or request(config)
    return GovernedProviderRunner().run(
        configuration=config,
        request=requested,
        executable_path=EXECUTABLE,
        package_path=HERE / "provider_fixture.py",
        working_directory=HERE,
        working_directory_boundary=HERE.parent,
        authority=authority,
        cancellation=cancellation,
        inherited_environment={},
    )


def test_local_nonsemantic_fixture_proves_capture_hashing_and_repeatability() -> None:
    first = run()
    second = run()
    assert first.passed and second.passed
    assert first.stdout_bytes == b'{"meaning":"unchanged"}'
    assert first.stdout_sha256 == second.stdout_sha256
    assert first.manifest_id == second.manifest_id
    assert first.authority_receipt_id is None


@pytest.mark.parametrize(
    ("request_change", "expected"),
    [
        ({"configuration_hash": "0" * 64}, FailureCode.CONFIGURATION_DRIFT),
        ({"model_identity": "drifted-model"}, FailureCode.CONFIGURATION_DRIFT),
        ({"requested_tools": ("shell",)}, FailureCode.CONFIGURATION_DRIFT),
        ({"requested_network_hosts": ("example.com",)}, FailureCode.CONFIGURATION_DRIFT),
    ],
)
def test_configuration_and_policy_drift_fail_closed(request_change, expected) -> None:
    config = configuration()
    with pytest.raises(ProviderExecutionRejected) as caught:
        run(config, replace(request(config), **request_change))
    assert caught.value.failure.code is expected


def test_executable_hash_drift_fails_closed() -> None:
    config = configuration(executable_sha256="0" * 64)
    with pytest.raises(ProviderExecutionRejected) as caught:
        run(config, request(config))
    assert caught.value.failure.code is FailureCode.EXECUTABLE_DRIFT


def test_package_hash_drift_fails_closed() -> None:
    config = configuration(package_sha256="0" * 64)
    with pytest.raises(ProviderExecutionRejected) as caught:
        run(config, request(config))
    assert caught.value.failure.code is FailureCode.CONFIGURATION_DRIFT


def test_runtime_version_drift_fails_closed() -> None:
    config = configuration(runtime_version="Python 0.0.0")
    with pytest.raises(ProviderExecutionRejected) as caught:
        run(config, request(config))
    assert caught.value.failure.code is FailureCode.RUNTIME_VERSION_DRIFT


def test_runtime_version_probe_timeout_is_typed() -> None:
    config = configuration(
        runtime_version="unreachable",
        version_probe_argv=("provider_fixture.py", "sleep"),
        timeout_seconds=1,
    )
    with pytest.raises(ProviderExecutionRejected) as caught:
        run(config, request(config))
    assert caught.value.failure.code is FailureCode.TIMEOUT


def test_billable_or_credentialed_configuration_requires_governed_authority() -> None:
    config = configuration(
        may_incur_cost=True,
        requires_credentials=True,
        credential_environment_names=("OPENAI_API_KEY",),
    )
    with pytest.raises(ProviderExecutionRejected) as caught:
        run(config, request(config))
    assert caught.value.failure.code is FailureCode.AUTHORITY_MISSING


def test_any_semantic_provider_requires_governed_authority_even_when_local() -> None:
    config = configuration(semantic_provider=True)
    with pytest.raises(ProviderExecutionRejected) as caught:
        run(config, request(config))
    assert caught.value.failure.code is FailureCode.AUTHORITY_MISSING


def test_authority_is_bound_to_exact_configuration() -> None:
    config = configuration(may_incur_cost=True)
    authority = ProviderRunAuthority(
        authority_receipt_id="authority-test-only",
        configuration_hash="0" * 64,
        maximum_calls=1,
        maximum_repeats=1,
        maximum_expected_cost="0.00 TEST ONLY",
        data_classes=("synthetic",),
        credential_environment_names=(),
        retention_policy="discard_after_test",
    )
    with pytest.raises(ProviderExecutionRejected) as caught:
        run(config, request(config), authority=authority)
    assert caught.value.failure.code is FailureCode.AUTHORITY_SCOPE_MISMATCH


def test_authority_call_bound_is_enforced_statelessly_by_call_ordinal() -> None:
    config = configuration(may_incur_cost=True)
    authority = ProviderRunAuthority(
        authority_receipt_id="authority-test-only",
        configuration_hash=config.configuration_hash,
        maximum_calls=1,
        maximum_repeats=1,
        maximum_expected_cost="0.00 TEST ONLY",
        data_classes=("synthetic",),
        credential_environment_names=(),
        retention_policy="discard_after_test",
    )
    over_bound = replace(request(config), call_ordinal=2)
    with pytest.raises(ProviderExecutionRejected) as caught:
        run(config, over_bound, authority=authority)
    assert caught.value.failure.code is FailureCode.AUTHORITY_SCOPE_MISMATCH


def test_timeout_is_typed_and_never_passes() -> None:
    config = configuration(
        invocation_argv=("provider_fixture.py", "sleep"),
        timeout_seconds=1,
        retry_policy=RetryPolicy(maximum_attempts=1, retry_timeouts=False),
        output_format=OutputFormat.TEXT,
    )
    manifest = run(config, request(config))
    assert not manifest.passed
    assert manifest.failures[-1].code is FailureCode.TIMEOUT


def test_cancellation_kills_process_and_returns_typed_failure() -> None:
    config = configuration(
        invocation_argv=("provider_fixture.py", "sleep"),
        timeout_seconds=3,
        output_format=OutputFormat.TEXT,
    )
    token = CancellationToken.create()
    result = []

    thread = Thread(target=lambda: result.append(run(config, request(config), cancellation=token)))
    thread.start()
    sleep(0.1)
    token.cancel()
    thread.join(timeout=5)
    assert not thread.is_alive()
    assert result[0].failures[-1].code is FailureCode.CANCELLED


def test_nonzero_exit_is_captured_without_partial_success() -> None:
    config = configuration(
        invocation_argv=("provider_fixture.py", "fail"),
        accepted_exit_codes=(0,),
        output_format=OutputFormat.TEXT,
    )
    manifest = run(config, request(config))
    assert not manifest.passed
    assert manifest.exit_code == 17
    assert manifest.failures[-1].code is FailureCode.INVOCATION_FAILED
    assert sha256(manifest.stderr_bytes).hexdigest() == manifest.stderr_sha256


def test_invalid_declared_output_format_fails_closed() -> None:
    config = configuration(invocation_argv=("provider_fixture.py", "invalid-json"))
    with pytest.raises(ProviderExecutionRejected) as caught:
        run(config, request(config))
    assert caught.value.failure.code is FailureCode.OUTPUT_INVALID


def test_retry_policy_is_bounded_and_preserves_each_typed_failure() -> None:
    config = configuration(
        invocation_argv=("provider_fixture.py", "fail"),
        accepted_exit_codes=(0,),
        retry_policy=RetryPolicy(maximum_attempts=2, retryable_exit_codes=(17,)),
        output_format=OutputFormat.TEXT,
    )
    manifest = run(config, request(config))
    assert manifest.attempt_count == 2
    assert [failure.attempt for failure in manifest.failures] == [1, 2]
