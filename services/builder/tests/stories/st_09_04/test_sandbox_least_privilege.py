import pytest

from cmf_builder.workflow.checkpoint_isolation import (
    CheckpointIsolationError,
    SandboxClass,
    SandboxPolicyDeclaration,
)


def sandbox(**overrides):
    values = {
        "policy_id": "sandbox:deterministic",
        "sandbox_class": SandboxClass.DETERMINISTIC_PROCESS,
        "immutable_environment_ref": "image@sha256:abc",
        "read_only_evidence_mounts": ("evidence://admitted",),
        "writable_staging_paths": ("staging://node",),
        "allowed_tools": ("python",),
        "network_allowlist": (),
        "secret_reference_names": ("OPENAI_API_KEY",),
        "cpu_limit": "2",
        "memory_limit": "4GiB",
        "time_limit_seconds": 60,
        "output_contract": "contract:output:v1",
        "logging_redaction_policy": "redact-secrets-and-prompts",
        "disposal_policy": "delete-staging-after-receipt",
        "isolation_mechanism_class": "local-policy-declaration",
    }
    values.update(overrides)
    return SandboxPolicyDeclaration(**values)


def test_sandbox_policy_is_deny_by_default_and_declaration_only():
    policy = sandbox()

    assert policy.deny_by_default is True
    assert policy.execution_performed is False
    assert policy.policy_identity


def test_sandbox_rejects_execution_or_non_deny_by_default():
    with pytest.raises(CheckpointIsolationError) as deny:
        sandbox(deny_by_default=False)
    assert deny.value.code == "SANDBOX_NOT_DENY_BY_DEFAULT"

    with pytest.raises(CheckpointIsolationError) as execution:
        sandbox(execution_performed=True)
    assert execution.value.code == "SANDBOX_EXECUTION_PROHIBITED"


def test_sandbox_rejects_secret_values_and_wildcard_provider_network():
    with pytest.raises(CheckpointIsolationError) as secret:
        sandbox(secret_reference_names=("OPENAI_API_KEY=not-allowed",))
    assert secret.value.code == "SECRET_VALUE_PROHIBITED"

    with pytest.raises(CheckpointIsolationError) as network:
        sandbox(sandbox_class=SandboxClass.PROVIDER_CALL, network_allowlist=("*",))
    assert network.value.code == "UNDECLARED_NETWORK_ACCESS"
