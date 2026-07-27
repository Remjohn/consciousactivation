from __future__ import annotations

from dataclasses import replace
import os
from pathlib import Path
import subprocess
import sys

import pytest

from cmf_builder.evaluation.selective_repair import (
    RepairAction,
    RepairCommand,
    SelectiveRepairError,
    canonical_json_bytes,
    compute_transition_payload_sha256,
    invalidate_repair_receipt,
    rollback_repair_receipt,
    validate_repeat_repair_receipt,
)
from tests.stories.st_08_05.test_accepted_diagnosis_and_repair_scope import (
    command,
    digest,
)
from tests.stories.st_08_05.test_escalation_and_failure_boundaries import (
    commit_inputs,
    commit_receipt,
    lifecycle_authority,
)


def transition_command(
    receipt,
    auth,
    *,
    action=RepairAction.INVALIDATE,
    command_id="invalidate-selective-repair-v1",
    resource_id=None,
    payload_sha256=None,
    restored_parent_identity=None,
    expected_authority_identity=None,
):
    return RepairCommand(
        command_id=command_id,
        action=action,
        resource_id=resource_id or receipt.receipt_identity,
        payload_sha256=payload_sha256
        or compute_transition_payload_sha256(
            prior_receipt_identity=receipt.receipt_identity,
            action=action,
            affected_descendants=receipt.candidate.affected_descendants,
            restored_parent_identity=restored_parent_identity,
        ),
        expected_authority_identity=(
            expected_authority_identity or auth.authority_identity
        ),
    )


def test_identical_repeat_commit_is_payload_safe_and_returns_original_receipt() -> None:
    existing = commit_receipt()
    repeated = commit_receipt()

    assert existing.receipt_identity == repeated.receipt_identity
    assert validate_repeat_repair_receipt(existing, repeated) is existing


def test_conflicting_repeat_commit_fails_closed() -> None:
    existing = commit_receipt()
    inputs = commit_inputs()
    auth = lifecycle_authority(RepairAction.COMMIT_CANDIDATE)
    changed_command = command(
        action=RepairAction.COMMIT_CANDIDATE,
        resource_id=inputs["candidate"].candidate_identity,
        payload_sha256=existing.commit_payload_sha256,
        governed_authority=auth,
        command_id="different-command-id",
    )
    changed = commit_receipt(
        inputs=inputs,
        governed_authority=auth,
        governed_command=changed_command,
    )

    with pytest.raises(SelectiveRepairError) as caught:
        validate_repeat_repair_receipt(existing, changed)

    assert caught.value.code == "CONFLICTING_REPEAT_COMMAND"


def test_commit_is_byte_identical_in_a_fresh_python_process() -> None:
    repository = Path(__file__).resolve().parents[3]
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join(
        (str(repository / "src"), str(repository), environment.get("PYTHONPATH", ""))
    )
    script = (
        "from tests.stories.st_08_05.test_escalation_and_failure_boundaries "
        "import commit_receipt; "
        "from cmf_builder.evaluation.selective_repair import canonical_json_bytes; "
        "import sys; sys.stdout.buffer.write(canonical_json_bytes(commit_receipt().as_dict()))"
    )

    fresh_bytes = subprocess.check_output(
        [sys.executable, "-c", script],
        cwd=repository,
        env=environment,
    )

    assert fresh_bytes == canonical_json_bytes(commit_receipt().as_dict())


def test_changed_governed_result_hash_changes_commit_identity() -> None:
    original = commit_receipt()
    inputs = commit_inputs()
    changed_result = replace(
        inputs["results"][0],
        result_sha256=digest("changed-governed-result"),
    )
    changed_inputs = {
        **inputs,
        "results": (changed_result,) + inputs["results"][1:],
    }
    changed = commit_receipt(inputs=changed_inputs)

    assert changed.receipt_identity != original.receipt_identity
    assert canonical_json_bytes(changed.as_dict()) != canonical_json_bytes(
        original.as_dict()
    )


def test_nested_candidate_tampering_is_detected_at_commit_serialization_boundary() -> None:
    receipt = commit_receipt()
    object.__setattr__(receipt.candidate, "candidate_version", "forged-version")

    with pytest.raises(SelectiveRepairError) as caught:
        receipt.as_dict()

    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"


def test_nested_local_result_tampering_is_detected_at_commit_serialization_boundary() -> None:
    receipt = commit_receipt()
    object.__setattr__(receipt.local_results[0], "result_sha256", digest("forged-result"))

    with pytest.raises(SelectiveRepairError) as caught:
        receipt.as_dict()

    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"


def test_invalidation_is_exactly_descendant_scoped_and_preserves_history() -> None:
    receipt = commit_receipt()
    historical_bytes = canonical_json_bytes(receipt.as_dict())
    auth = lifecycle_authority(RepairAction.INVALIDATE)
    cmd = transition_command(receipt, auth)

    transition = invalidate_repair_receipt(receipt, cmd, auth)

    assert transition.action is RepairAction.INVALIDATE
    assert transition.prior_receipt_identity == receipt.receipt_identity
    assert transition.invalidated_descendants == receipt.candidate.affected_descendants
    assert transition.active_after is False
    assert transition.historical_candidate_preserved is True
    assert transition.command_identity == cmd.command_identity
    assert transition.authority_identity == auth.authority_identity
    assert canonical_json_bytes(receipt.as_dict()) == historical_bytes


def test_rollback_restores_parent_reference_without_deleting_failed_candidate_history() -> None:
    receipt = commit_receipt()
    historical_bytes = canonical_json_bytes(receipt.as_dict())
    auth = lifecycle_authority(RepairAction.ROLLBACK)
    cmd = transition_command(
        receipt,
        auth,
        action=RepairAction.ROLLBACK,
        command_id="rollback-selective-repair-v1",
        restored_parent_identity=receipt.candidate.parent_subject_identity,
    )

    transition = rollback_repair_receipt(receipt, cmd, auth)

    assert transition.action is RepairAction.ROLLBACK
    assert transition.active_after is False
    assert transition.restored_parent_identity == receipt.candidate.parent_subject_identity
    assert transition.historical_candidate_preserved is True
    assert transition.historical_receipt_preserved is True
    assert canonical_json_bytes(receipt.as_dict()) == historical_bytes


def test_identical_transition_commands_are_byte_deterministic() -> None:
    first_receipt = commit_receipt()
    second_receipt = commit_receipt()
    first_auth = lifecycle_authority(RepairAction.INVALIDATE)
    second_auth = lifecycle_authority(RepairAction.INVALIDATE)

    first = invalidate_repair_receipt(
        first_receipt,
        transition_command(first_receipt, first_auth),
        first_auth,
    )
    second = invalidate_repair_receipt(
        second_receipt,
        transition_command(second_receipt, second_auth),
        second_auth,
    )

    assert first.transition_identity == second.transition_identity
    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())


@pytest.mark.parametrize(
    ("change", "expected_code"),
    (
        ({"resource_id": digest("wrong-receipt")}, "COMMAND_RESOURCE_MISMATCH"),
        ({"payload_sha256": digest("wrong-payload")}, "COMMAND_PAYLOAD_MISMATCH"),
        (
            {"expected_authority_identity": digest("wrong-authority")},
            "AUTHORITY_IDENTITY_MISMATCH",
        ),
    ),
)
@pytest.mark.parametrize("action", (RepairAction.INVALIDATE, RepairAction.ROLLBACK))
def test_invalidation_and_rollback_require_exact_command_binding(
    action, change, expected_code
) -> None:
    receipt = commit_receipt()
    auth = lifecycle_authority(action)
    restored_parent = (
        receipt.candidate.parent_subject_identity
        if action is RepairAction.ROLLBACK
        else None
    )
    cmd = transition_command(
        receipt,
        auth,
        action=action,
        command_id=f"{action.value.lower()}-binding-test",
        restored_parent_identity=restored_parent,
    )
    cmd = replace(cmd, **change)

    function = (
        invalidate_repair_receipt
        if action is RepairAction.INVALIDATE
        else rollback_repair_receipt
    )
    with pytest.raises(SelectiveRepairError) as caught:
        function(receipt, cmd, auth)

    assert caught.value.code == expected_code


def test_invalidation_cannot_expand_beyond_the_graph_proven_descendant_set() -> None:
    receipt = commit_receipt()
    auth = lifecycle_authority(RepairAction.INVALIDATE)
    overbroad = receipt.candidate.affected_descendants + (digest("unaffected-sibling"),)
    cmd = RepairCommand(
        command_id="overbroad-invalidation",
        action=RepairAction.INVALIDATE,
        resource_id=receipt.receipt_identity,
        payload_sha256=compute_transition_payload_sha256(
            prior_receipt_identity=receipt.receipt_identity,
            action=RepairAction.INVALIDATE,
            affected_descendants=overbroad,
            restored_parent_identity=None,
        ),
        expected_authority_identity=auth.authority_identity,
    )

    with pytest.raises(SelectiveRepairError) as caught:
        invalidate_repair_receipt(
            receipt,
            cmd,
            auth,
            affected_descendants=overbroad,
        )

    assert caught.value.code == "INVALIDATION_SCOPE_BROADER_THAN_DIAGNOSIS"


def test_transition_failure_leaves_zero_partial_state_and_preserves_prior_history() -> None:
    receipt = commit_receipt()
    historical_bytes = canonical_json_bytes(receipt.as_dict())
    auth = lifecycle_authority(RepairAction.INVALIDATE)
    transition = None

    with pytest.raises(SelectiveRepairError) as caught:
        transition = invalidate_repair_receipt(
            receipt,
            transition_command(
                receipt,
                auth,
                payload_sha256=digest("conflicting-transition-payload"),
            ),
            auth,
        )

    assert caught.value.code == "COMMAND_PAYLOAD_MISMATCH"
    assert transition is None
    assert canonical_json_bytes(receipt.as_dict()) == historical_bytes

