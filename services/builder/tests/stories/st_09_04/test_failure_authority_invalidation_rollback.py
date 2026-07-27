import pytest

from cmf_builder.workflow.checkpoint_isolation import (
    AuthorityStatus,
    CheckpointAction,
    CheckpointAuthority,
    CheckpointCommand,
    CheckpointIsolationError,
    SideEffectRecord,
    commit_checkpoint,
    compute_checkpoint_payload_sha256,
    compute_checkpoint_transition_payload_sha256,
    invalidate_checkpoint,
    rollback_checkpoint,
)


def digest(label: str) -> str:
    return (label.encode().hex() * 64)[:64]


def authority(status=AuthorityStatus.ACTIVE):
    return CheckpointAuthority("authority", "1.0", digest("auth"), tuple(CheckpointAction), ("*",), status)


def values(**overrides):
    payload = {
        "checkpoint_id": "checkpoint:1",
        "checkpoint_version": "1.0",
        "run_id": "run:1",
        "workflow_hash": digest("workflow"),
        "profile_hash": digest("profile"),
        "completed_node_identities": ("node:a",),
        "committed_input_hashes": (digest("input"),),
        "committed_output_hashes": (digest("output"),),
        "node_validation_receipt_refs": ("receipt:validation",),
        "side_effect_records": (SideEffectRecord("effect:1", "idem:1", digest("effect"), True, human_action=True),),
        "event_stream_position": 1,
        "next_eligible_nodes": ("node:b",),
        "parent_checkpoint_ref": "checkpoint:0",
        "invalidation_refs": (),
    }
    payload.update(overrides)
    return payload


def checkpoint():
    auth = authority()
    payload = values()
    command = CheckpointCommand("commit", CheckpointAction.COMMIT, payload["run_id"], compute_checkpoint_payload_sha256(**payload), auth.authority_identity)
    return commit_checkpoint(command, auth, **payload), auth


def test_duplicate_side_effect_idempotency_key_fails_closed():
    auth = authority()
    payload = values(
        side_effect_records=(
            SideEffectRecord("effect:1", "same", digest("a"), True),
            SideEffectRecord("effect:2", "same", digest("b"), True),
        )
    )
    command = CheckpointCommand("commit", CheckpointAction.COMMIT, payload["run_id"], compute_checkpoint_payload_sha256(**payload), auth.authority_identity)
    with pytest.raises(CheckpointIsolationError) as caught:
        commit_checkpoint(command, auth, **payload)
    assert caught.value.code == "DUPLICATE_SIDE_EFFECT_IDEMPOTENCY_KEY"


def test_inactive_authority_and_payload_drift_fail_closed():
    auth = authority(AuthorityStatus.INVALIDATED)
    payload = values()
    command = CheckpointCommand("commit", CheckpointAction.COMMIT, payload["run_id"], compute_checkpoint_payload_sha256(**payload), auth.authority_identity)
    with pytest.raises(CheckpointIsolationError) as inactive:
        commit_checkpoint(command, auth, **payload)
    assert inactive.value.code == "INACTIVE_AUTHORITY"

    active = authority()
    bad_command = CheckpointCommand("commit", CheckpointAction.COMMIT, payload["run_id"], digest("wrong"), active.authority_identity)
    with pytest.raises(CheckpointIsolationError) as drift:
        commit_checkpoint(bad_command, active, **payload)
    assert drift.value.code == "COMMAND_PAYLOAD_MISMATCH"


def test_invalidation_and_rollback_preserve_historical_checkpoint():
    cp, auth = checkpoint()
    invalidate_command = CheckpointCommand(
        "invalidate",
        CheckpointAction.INVALIDATE,
        cp.checkpoint_identity,
        compute_checkpoint_transition_payload_sha256(cp.checkpoint_identity, CheckpointAction.INVALIDATE),
        auth.authority_identity,
    )
    invalidated = invalidate_checkpoint(cp, invalidate_command, auth)
    assert invalidated.active_after is False
    assert invalidated.historical_checkpoint_preserved is True

    rollback_command = CheckpointCommand(
        "rollback",
        CheckpointAction.ROLLBACK,
        cp.checkpoint_identity,
        compute_checkpoint_transition_payload_sha256(cp.checkpoint_identity, CheckpointAction.ROLLBACK),
        auth.authority_identity,
    )
    rollback = rollback_checkpoint(cp, rollback_command, auth)
    assert rollback.active_after is False
    assert rollback.historical_checkpoint_preserved is True
