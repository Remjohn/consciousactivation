from __future__ import annotations

from dataclasses import replace
import os
from pathlib import Path
import subprocess
import sys

import pytest

from cmf_builder.evaluation.root_cause_diagnosis import (
    AuthorityStatus,
    DiagnosisAction,
    DiagnosisCommand,
    RootCauseDiagnosisError,
    build_rejection_receipt,
    canonical_json_bytes,
    canonical_sha256,
    invalidate_diagnosis_receipt,
    rollback_diagnosis_receipt,
    validate_repeat_receipt,
)
from tests.stories.st_08_04.test_failure_authority_boundaries import (
    authority,
    command,
    digest,
    issue_inputs,
    valid_receipt,
)


def transition_command(
    receipt,
    auth,
    *,
    action=DiagnosisAction.INVALIDATE,
    command_id="invalidate-root-cause-diagnosis-v1",
    resource_id=None,
    payload_sha256=None,
    expected_authority_identity=None,
):
    return DiagnosisCommand(
        command_id=command_id,
        action=action,
        resource_id=resource_id or receipt.receipt_identity,
        payload_sha256=payload_sha256
        or canonical_sha256(
            {
                "prior_receipt_identity": receipt.receipt_identity,
                "action": action.value,
            }
        ),
        expected_authority_identity=expected_authority_identity or auth.authority_identity,
    )


def test_identical_repeat_is_payload_safe_and_returns_original_receipt() -> None:
    existing = valid_receipt()
    candidate = valid_receipt()

    assert existing.receipt_identity == candidate.receipt_identity
    assert validate_repeat_receipt(existing, candidate) is existing


def test_conflicting_repeat_command_fails_closed() -> None:
    existing = valid_receipt()
    inputs = issue_inputs()
    auth = authority()
    candidate = valid_receipt(
        inputs=inputs,
        auth=auth,
        issue_command=command(inputs, auth, command_id="different-command-id"),
    )

    with pytest.raises(RootCauseDiagnosisError) as caught:
        validate_repeat_receipt(existing, candidate)

    assert caught.value.code == "CONFLICTING_REPEAT_COMMAND"


def test_identical_inputs_are_byte_equal_in_a_fresh_python_process() -> None:
    repository = Path(__file__).resolve().parents[3]
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join(
        (str(repository / "src"), str(repository), environment.get("PYTHONPATH", ""))
    )
    script = (
        "from tests.stories.st_08_04.test_failure_authority_boundaries "
        "import valid_receipt; "
        "from cmf_builder.evaluation.root_cause_diagnosis import canonical_json_bytes; "
        "import sys; sys.stdout.buffer.write(canonical_json_bytes(valid_receipt().as_dict()))"
    )

    fresh_bytes = subprocess.check_output(
        [sys.executable, "-c", script],
        cwd=repository,
        env=environment,
    )

    assert fresh_bytes == canonical_json_bytes(valid_receipt().as_dict())


@pytest.mark.parametrize(
    ("field", "changed_value"),
    (
        ("dependency_graph_sha256", digest("changed-dependency-graph")),
        ("run_id", "st-08.04-development-run-v2"),
        ("provenance_sha256", digest("changed-provenance")),
    ),
)
def test_changed_governed_lineage_changes_the_immutable_receipt_identity(field, changed_value) -> None:
    original = valid_receipt()
    inputs = issue_inputs(**{field: changed_value})
    auth = authority()
    changed = valid_receipt(
        inputs=inputs,
        auth=auth,
        issue_command=command(inputs, auth, command_id=f"issue-changed-{field}"),
    )

    assert changed.receipt_identity != original.receipt_identity
    assert getattr(changed, field) == changed_value


def test_nested_diagnosis_tampering_is_detected_at_receipt_serialization_boundary() -> None:
    receipt = valid_receipt()
    nested = receipt.diagnosis.hypothesis_tests_and_results[0]
    object.__setattr__(nested, "evidence_refs", (digest("forged-hypothesis-evidence"),))

    with pytest.raises(RootCauseDiagnosisError) as caught:
        receipt.as_dict()

    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"


def test_nested_dependency_edge_tampering_is_detected_at_receipt_serialization_boundary() -> None:
    receipt = valid_receipt()
    nested = receipt.graph.dependency_edges[0]
    object.__setattr__(nested, "child_identity", digest("forged-descendant"))

    with pytest.raises(RootCauseDiagnosisError) as caught:
        receipt.as_dict()

    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"


def test_exact_invalidation_scope_is_deterministic_and_non_destructive() -> None:
    receipt = valid_receipt()
    original_bytes = canonical_json_bytes(receipt.as_dict())
    auth = authority(DiagnosisAction.INVALIDATE)
    cmd = transition_command(receipt, auth)

    transition = invalidate_diagnosis_receipt(
        receipt,
        cmd,
        auth,
    )

    assert transition.prior_receipt_identity == receipt.receipt_identity
    assert transition.action is DiagnosisAction.INVALIDATE
    assert transition.active_after is False
    assert transition.historical_receipt_preserved is True
    assert receipt.graph is not None
    assert receipt.graph.invalidated_descendant_set
    assert transition.command_identity == cmd.command_identity
    assert transition.authority_identity == auth.authority_identity
    assert canonical_json_bytes(receipt.as_dict()) == original_bytes


def test_identical_invalidation_commands_produce_byte_identical_scope_receipts() -> None:
    first_receipt = valid_receipt()
    second_receipt = valid_receipt()
    first_auth = authority(DiagnosisAction.INVALIDATE)
    second_auth = authority(DiagnosisAction.INVALIDATE)

    first = invalidate_diagnosis_receipt(
        first_receipt,
        transition_command(first_receipt, first_auth),
        first_auth,
    )
    second = invalidate_diagnosis_receipt(
        second_receipt,
        transition_command(second_receipt, second_auth),
        second_auth,
    )

    assert first.transition_identity == second.transition_identity
    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())


def test_rollback_receipt_is_deterministic_and_never_mutates_diagnosis_or_graph() -> None:
    receipt = valid_receipt()
    original_bytes = canonical_json_bytes(receipt.as_dict())
    auth = authority(DiagnosisAction.ROLLBACK)
    cmd = transition_command(
        receipt,
        auth,
        action=DiagnosisAction.ROLLBACK,
        command_id="rollback-root-cause-diagnosis-v1",
    )

    transition = rollback_diagnosis_receipt(
        receipt,
        cmd,
        auth,
    )

    assert transition.prior_receipt_identity == receipt.receipt_identity
    assert transition.action is DiagnosisAction.ROLLBACK
    assert transition.active_after is False
    assert transition.historical_receipt_preserved is True
    assert canonical_json_bytes(receipt.as_dict()) == original_bytes


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
def test_rollback_requires_exact_authority_resource_and_payload(change, expected_code) -> None:
    receipt = valid_receipt()
    auth = authority(DiagnosisAction.ROLLBACK)
    cmd = transition_command(
        receipt,
        auth,
        action=DiagnosisAction.ROLLBACK,
        command_id="rollback-boundary-test",
    )
    cmd = replace(cmd, **change)

    with pytest.raises(RootCauseDiagnosisError) as caught:
        rollback_diagnosis_receipt(
            receipt,
            cmd,
            auth,
        )

    assert caught.value.code == expected_code


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
def test_invalidation_requires_exact_command_authority_resource_and_payload(change, expected_code) -> None:
    receipt = valid_receipt()
    auth = authority(DiagnosisAction.INVALIDATE)
    cmd = replace(transition_command(receipt, auth), **change)

    with pytest.raises(RootCauseDiagnosisError) as caught:
        invalidate_diagnosis_receipt(receipt, cmd, auth)

    assert caught.value.code == expected_code


def test_stale_authority_cannot_invalidate_active_diagnosis_scope() -> None:
    receipt = valid_receipt()
    auth = authority(DiagnosisAction.INVALIDATE, status=AuthorityStatus.SUPERSEDED)

    with pytest.raises(RootCauseDiagnosisError) as caught:
        invalidate_diagnosis_receipt(
            receipt,
            transition_command(receipt, auth),
            auth,
        )

    assert caught.value.code == "INACTIVE_AUTHORITY"


def test_conflicting_invalidation_payload_fails_with_zero_partial_state_and_preserves_history() -> None:
    receipt = valid_receipt()
    original_bytes = canonical_json_bytes(receipt.as_dict())
    auth = authority(DiagnosisAction.INVALIDATE)
    transition = None

    with pytest.raises(RootCauseDiagnosisError) as caught:
        transition = invalidate_diagnosis_receipt(
            receipt,
            transition_command(receipt, auth, payload_sha256=digest("wrong-payload")),
            auth,
        )

    assert caught.value.code == "COMMAND_PAYLOAD_MISMATCH"
    assert transition is None
    assert canonical_json_bytes(receipt.as_dict()) == original_bytes


def test_atomic_failure_can_emit_only_a_deterministic_rejection_receipt() -> None:
    receipt = valid_receipt()
    original_bytes = canonical_json_bytes(receipt.as_dict())
    auth = authority(DiagnosisAction.INVALIDATE)
    cmd = transition_command(receipt, auth, payload_sha256=digest("wrong-payload"))
    transition = None

    with pytest.raises(RootCauseDiagnosisError) as caught:
        transition = invalidate_diagnosis_receipt(
            receipt,
            cmd,
            auth,
        )

    rejection = build_rejection_receipt(
        error=caught.value,
        command_id=cmd.command_id,
        payload_sha256=cmd.payload_sha256,
        authority_identity=auth.authority_identity,
    )

    assert transition is None
    assert rejection.error_code == "COMMAND_PAYLOAD_MISMATCH"
    assert rejection.partial_state_count == 0
    assert canonical_json_bytes(receipt.as_dict()) == original_bytes
