import pytest

from cmf_builder.workflow.checkpoint_isolation import (
    CheckpointAction,
    CheckpointAuthority,
    CheckpointCommand,
    CheckpointIsolationError,
    ResumeRequest,
    SideEffectRecord,
    commit_checkpoint,
    compute_checkpoint_payload_sha256,
    compute_resume_payload_sha256,
    resume_checkpoint,
    validate_repeat_checkpoint,
)


def digest(label: str) -> str:
    return (label.encode().hex() * 64)[:64]


def authority(*actions):
    return CheckpointAuthority("checkpoint-authority", "1.0", digest("auth"), actions or tuple(CheckpointAction), ("*",))


def checkpoint_values(**overrides):
    values = {
        "checkpoint_id": "checkpoint:1",
        "checkpoint_version": "1.0.0-development",
        "run_id": "run:workflow:1",
        "workflow_hash": digest("workflow"),
        "profile_hash": digest("profile"),
        "completed_node_identities": ("node:a",),
        "committed_input_hashes": (digest("input"),),
        "committed_output_hashes": (digest("output"),),
        "node_validation_receipt_refs": ("receipt:node-validation",),
        "side_effect_records": (SideEffectRecord("effect:1", "idem:1", digest("effect"), True),),
        "event_stream_position": 7,
        "next_eligible_nodes": ("node:b",),
        "parent_checkpoint_ref": "checkpoint:0",
        "invalidation_refs": (),
    }
    values.update(overrides)
    return values


def committed_checkpoint(**overrides):
    values = checkpoint_values(**overrides)
    auth = authority()
    command = CheckpointCommand(
        "commit",
        CheckpointAction.COMMIT,
        values["run_id"],
        compute_checkpoint_payload_sha256(**values),
        auth.authority_identity,
    )
    return commit_checkpoint(command, auth, **values)


def test_checkpoint_commit_is_immutable_and_idempotent():
    first = committed_checkpoint()
    second = committed_checkpoint()

    assert first.checkpoint_identity == second.checkpoint_identity
    assert validate_repeat_checkpoint(first, second) is first
    assert first.as_dict()["production_ready"] is False


def test_changed_checkpoint_payload_conflicts_with_repeat():
    first = committed_checkpoint()
    changed = committed_checkpoint(event_stream_position=8)

    with pytest.raises(CheckpointIsolationError) as caught:
        validate_repeat_checkpoint(first, changed)
    assert caught.value.code == "CONFLICTING_REPEAT_COMMAND"


def test_resume_reuses_committed_outputs_without_repeating_side_effects():
    checkpoint = committed_checkpoint()
    request = ResumeRequest("run:workflow:1", digest("workflow"), digest("profile"), "node:b", digest("attempt-policy"), digest("input-b"))
    auth = authority()
    command = CheckpointCommand(
        "resume",
        CheckpointAction.RESUME,
        checkpoint.checkpoint_identity,
        compute_resume_payload_sha256(checkpoint, request),
        auth.authority_identity,
    )

    receipt = resume_checkpoint(checkpoint, request, command, auth)

    assert receipt.reused_node_outputs == (digest("output"),)
    assert receipt.duplicate_side_effects_prevented == ("idem:1",)
    assert receipt.ratified_human_actions_replayed is False


def test_resume_rejects_silent_profile_change_or_ineligible_node():
    checkpoint = committed_checkpoint()
    auth = authority()

    changed_profile = ResumeRequest("run:workflow:1", digest("workflow"), digest("other-profile"), "node:b", digest("attempt-policy"), digest("input-b"))
    command = CheckpointCommand("resume", CheckpointAction.RESUME, checkpoint.checkpoint_identity, compute_resume_payload_sha256(checkpoint, changed_profile), auth.authority_identity)
    with pytest.raises(CheckpointIsolationError) as profile_error:
        resume_checkpoint(checkpoint, changed_profile, command, auth)
    assert profile_error.value.code == "SILENT_PROFILE_CHANGE_PROHIBITED"

    ineligible = ResumeRequest("run:workflow:1", digest("workflow"), digest("profile"), "node:c", digest("attempt-policy"), digest("input-b"))
    command = CheckpointCommand("resume", CheckpointAction.RESUME, checkpoint.checkpoint_identity, compute_resume_payload_sha256(checkpoint, ineligible), auth.authority_identity)
    with pytest.raises(CheckpointIsolationError) as node_error:
        resume_checkpoint(checkpoint, ineligible, command, auth)
    assert node_error.value.code == "NODE_NOT_ELIGIBLE_FOR_RESUME"
