import pytest

from cmf_builder.workflow.node_validation import (
    AuthorityStatus,
    BoundedControlFlowPolicy,
    NodeOutputSnapshot,
    NodeValidationAction,
    NodeValidationAuthority,
    NodeValidationCommand,
    NodeValidationError,
    NodeValidationPolicy,
    ValidationCheck,
    CheckStatus,
    compute_node_validation_payload_sha256,
    validate_control_flow_state,
    validate_node_output,
)


def digest(label: str) -> str:
    return (label.encode().hex() * 64)[:64]


def bounded_policy(**overrides):
    values = {
        "policy_id": "bounded-control-flow",
        "maximum_attempts": 3,
        "timeout_seconds": 30,
        "retryable_failure_classes": ("TRANSIENT_LOCAL_FAILURE",),
        "non_retryable_failure_classes": ("AUTHORITY_FAILURE",),
        "circuit_breaker_condition": "three_consecutive_validation_failures",
        "terminal_states": ("READY", "ATTEMPTS_EXHAUSTED", "CIRCUIT_OPEN"),
        "escalation_destination": "owner:workflow-operator",
        "loop_limit": 3,
        "fan_out_limit": 2,
        "arbitration_limit": 1,
        "fallback_limit": 1,
    }
    values.update(overrides)
    return BoundedControlFlowPolicy(**values)


def test_bounded_policy_rejects_unbounded_retry_and_feedback_constructs():
    for field in ("maximum_attempts", "timeout_seconds", "loop_limit", "fan_out_limit", "arbitration_limit", "fallback_limit"):
        with pytest.raises(NodeValidationError) as caught:
            bounded_policy(**{field: 0})
        assert caught.value.code == "UNBOUNDED_CONTROL_FLOW"


def test_control_flow_state_blocks_after_exhaustion_or_open_circuit():
    ready = validate_control_flow_state(bounded_policy(), attempt_count=1)
    assert ready.output_release_allowed is True
    assert ready.further_attempts_allowed is True

    exhausted = validate_control_flow_state(bounded_policy(), attempt_count=3)
    assert exhausted.terminal_state == "ATTEMPTS_EXHAUSTED"
    assert exhausted.output_release_allowed is False

    circuit = validate_control_flow_state(bounded_policy(), attempt_count=1, circuit_open=True)
    assert circuit.terminal_state == "CIRCUIT_OPEN"
    assert circuit.further_attempts_allowed is False


def test_inactive_or_scope_mismatched_authority_fails_closed():
    snapshot = NodeOutputSnapshot(
        digest("workflow"),
        "1.0",
        "node:1",
        "1.0",
        digest("input"),
        digest("output"),
        "contract:v1",
    )
    policy = NodeValidationPolicy(
        "policy",
        "1.0",
        ("deterministic_validator",),
        False,
        True,
        ("HG-013",),
        ("complete",),
    )
    checks = (
        ValidationCheck("check", "deterministic_validator", CheckStatus.PASS, digest("check"), digest("authority")),
    )
    inactive_authority = NodeValidationAuthority(
        "authority",
        "1.0",
        digest("authority"),
        (NodeValidationAction.VALIDATE,),
        ("*",),
        AuthorityStatus.INVALIDATED,
    )
    command = NodeValidationCommand(
        "cmd",
        NodeValidationAction.VALIDATE,
        snapshot.snapshot_identity,
        compute_node_validation_payload_sha256(snapshot, policy, checks, ()),
        inactive_authority.authority_identity,
    )
    with pytest.raises(NodeValidationError) as inactive:
        validate_node_output(snapshot=snapshot, policy=policy, checks=checks, authority=inactive_authority, command=command, predecessor_receipts=())
    assert inactive.value.code == "INACTIVE_AUTHORITY"

    scoped_authority = NodeValidationAuthority(
        "authority",
        "1.0",
        digest("authority"),
        (NodeValidationAction.VALIDATE,),
        ("different-node",),
    )
    scoped_command = NodeValidationCommand(
        "cmd",
        NodeValidationAction.VALIDATE,
        snapshot.snapshot_identity,
        compute_node_validation_payload_sha256(snapshot, policy, checks, ()),
        scoped_authority.authority_identity,
    )
    with pytest.raises(NodeValidationError) as scoped:
        validate_node_output(snapshot=snapshot, policy=policy, checks=checks, authority=scoped_authority, command=scoped_command, predecessor_receipts=())
    assert scoped.value.code == "AUTHORITY_SCOPE_MISMATCH"
