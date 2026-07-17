import pytest

from cmf_builder.workflow.node_validation import (
    CheckStatus,
    NodeOutputSnapshot,
    NodeValidationAction,
    NodeValidationAuthority,
    NodeValidationCommand,
    NodeValidationError,
    NodeValidationPolicy,
    ValidationCheck,
    compute_node_validation_payload_sha256,
    compute_node_validation_transition_payload_sha256,
    invalidate_node_validation_receipt,
    rollback_node_validation_receipt,
    validate_node_output,
    validate_repeat_node_validation,
)


def digest(label: str) -> str:
    return (label.encode().hex() * 64)[:64]


def parts(output_hash=None):
    snapshot = NodeOutputSnapshot(
        digest("workflow"),
        "1.0",
        "node:1",
        "1.0",
        digest("input"),
        output_hash or digest("output"),
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
    authority = NodeValidationAuthority(
        "authority",
        "1.0",
        digest("authority"),
        (NodeValidationAction.VALIDATE, NodeValidationAction.INVALIDATE, NodeValidationAction.ROLLBACK),
        ("*",),
    )
    command = NodeValidationCommand(
        "cmd",
        NodeValidationAction.VALIDATE,
        snapshot.snapshot_identity,
        compute_node_validation_payload_sha256(snapshot, policy, checks, ("ST-09.02",)),
        authority.authority_identity,
    )
    return snapshot, policy, checks, authority, command


def receipt(output_hash=None):
    snapshot, policy, checks, authority, command = parts(output_hash)
    return validate_node_output(
        snapshot=snapshot,
        policy=policy,
        checks=checks,
        authority=authority,
        command=command,
        predecessor_receipts=("ST-09.02",),
    )


def test_identical_inputs_produce_identical_receipts_and_repeat_is_idempotent():
    first = receipt()
    second = receipt()

    assert first.receipt_identity == second.receipt_identity
    assert validate_repeat_node_validation(first, second) is first


def test_changed_input_produces_conflicting_repeat_rejection():
    first = receipt()
    changed = receipt(digest("changed-output"))

    with pytest.raises(NodeValidationError) as caught:
        validate_repeat_node_validation(first, changed)
    assert caught.value.code == "CONFLICTING_REPEAT_COMMAND"


def test_invalidation_and_rollback_preserve_historical_receipt():
    issued = receipt()
    _, _, _, authority, _ = parts()
    invalidate_command = NodeValidationCommand(
        "invalidate",
        NodeValidationAction.INVALIDATE,
        issued.receipt_identity,
        compute_node_validation_transition_payload_sha256(issued.receipt_identity, NodeValidationAction.INVALIDATE),
        authority.authority_identity,
    )
    invalidated = invalidate_node_validation_receipt(issued, invalidate_command, authority)
    assert invalidated.active_after is False
    assert invalidated.historical_receipt_preserved is True

    rollback_command = NodeValidationCommand(
        "rollback",
        NodeValidationAction.ROLLBACK,
        issued.receipt_identity,
        compute_node_validation_transition_payload_sha256(issued.receipt_identity, NodeValidationAction.ROLLBACK),
        authority.authority_identity,
    )
    rollback = rollback_node_validation_receipt(issued, rollback_command, authority)
    assert rollback.active_after is False
    assert rollback.historical_receipt_preserved is True


def test_transition_rejects_payload_drift_atomically():
    issued = receipt()
    _, _, _, authority, _ = parts()
    bad_command = NodeValidationCommand(
        "invalidate",
        NodeValidationAction.INVALIDATE,
        issued.receipt_identity,
        digest("wrong-payload"),
        authority.authority_identity,
    )
    with pytest.raises(NodeValidationError) as caught:
        invalidate_node_validation_receipt(issued, bad_command, authority)
    assert caught.value.code == "COMMAND_PAYLOAD_MISMATCH"
