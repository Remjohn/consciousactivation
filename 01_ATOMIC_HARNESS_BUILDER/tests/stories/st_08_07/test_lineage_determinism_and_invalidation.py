from __future__ import annotations

from dataclasses import replace
import os
from pathlib import Path
import subprocess
import sys

import pytest

from cmf_builder.evaluation.structural_conversational_evaluation import (
    EvaluationError,
    StructuralAuthorityStatus,
    StructuralEvaluationAction,
    StructuralEvaluationAuthority,
    StructuralEvaluationCommand,
    canonical_json_bytes,
    compute_structural_invalidation_payload_sha256,
    compute_structural_issue_payload_sha256,
    invalidate_structural_evaluation_receipt,
    issue_structural_evaluation_receipt,
    validate_repeat_structural_evaluation,
)
from tests.stories.st_08_07.test_wrong_reading_rejection import digest, evaluate, subject


def authority(action: StructuralEvaluationAction, status: StructuralAuthorityStatus = StructuralAuthorityStatus.ACTIVE):
    return StructuralEvaluationAuthority("od-am-001-st-08.07", "1.0.0-development", digest("st-08.07-authority"), (action,), status)


def issue(receipt=None):
    candidate = receipt or evaluate()
    governed = authority(StructuralEvaluationAction.ISSUE)
    command = StructuralEvaluationCommand("issue-st-08.07", StructuralEvaluationAction.ISSUE, candidate.receipt_identity, compute_structural_issue_payload_sha256(candidate), governed.authority_identity)
    return issue_structural_evaluation_receipt(candidate, command, governed)


def test_identical_issue_is_byte_deterministic_and_idempotent() -> None:
    first, second = issue(), issue()
    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())
    assert validate_repeat_structural_evaluation(first, second) is first


def test_changed_governed_lineage_changes_receipt_identity() -> None:
    first = issue()
    changed = issue(evaluate(subject(semantic_lineage_refs=tuple(reversed(subject().semantic_lineage_refs)))))
    assert changed.receipt_identity != first.receipt_identity


def test_conflicting_repeat_fails_closed() -> None:
    with pytest.raises(EvaluationError) as caught:
        validate_repeat_structural_evaluation(issue(), issue(evaluate(subject(expected_reading="Changed governed expected reading."))))
    assert caught.value.code == "CONFLICTING_REPEAT_COMMAND"


def test_nested_evidence_tamper_is_detected() -> None:
    receipt = issue()
    object.__setattr__(receipt.subject.semantic_lineage_refs[0], "sha256", digest("tampered"))
    with pytest.raises(EvaluationError) as caught:
        receipt.as_dict()
    assert caught.value.code == "MUTATED_GOVERNED_OBJECT"


def test_invalidation_preserves_history_and_exact_scope() -> None:
    receipt = issue()
    historical = canonical_json_bytes(receipt.as_dict())
    governed = authority(StructuralEvaluationAction.INVALIDATE)
    scope = ("STRUCTURAL_SYNTHETIC_NON_PERSONAL_UNCERTIFIED",)
    command = StructuralEvaluationCommand("invalidate-st-08.07", StructuralEvaluationAction.INVALIDATE, receipt.receipt_identity, compute_structural_invalidation_payload_sha256(receipt.receipt_identity, scope), governed.authority_identity)
    result = invalidate_structural_evaluation_receipt(receipt, command, governed, scope)
    assert result.active_after is False
    assert result.historical_reproduction_preserved is True
    assert result.affected_scope == scope
    assert canonical_json_bytes(receipt.as_dict()) == historical


@pytest.mark.parametrize(("field", "code"), (("resource_id", "COMMAND_RESOURCE_MISMATCH"), ("payload_sha256", "COMMAND_PAYLOAD_MISMATCH"), ("expected_authority_identity", "AUTHORITY_IDENTITY_MISMATCH")))
def test_invalidation_command_is_exactly_bound(field: str, code: str) -> None:
    receipt = issue(); governed = authority(StructuralEvaluationAction.INVALIDATE); scope = ("STRUCTURAL_SYNTHETIC_NON_PERSONAL_UNCERTIFIED",)
    command = StructuralEvaluationCommand("invalidate-st-08.07", StructuralEvaluationAction.INVALIDATE, receipt.receipt_identity, compute_structural_invalidation_payload_sha256(receipt.receipt_identity, scope), governed.authority_identity)
    with pytest.raises(EvaluationError) as caught:
        invalidate_structural_evaluation_receipt(receipt, replace(command, **{field: digest("wrong")}), governed, scope)
    assert caught.value.code == code


def test_stale_authority_cannot_invalidate() -> None:
    receipt = issue(); governed = authority(StructuralEvaluationAction.INVALIDATE, StructuralAuthorityStatus.SUPERSEDED); scope = ("STRUCTURAL_SYNTHETIC_NON_PERSONAL_UNCERTIFIED",)
    command = StructuralEvaluationCommand("invalidate-st-08.07", StructuralEvaluationAction.INVALIDATE, receipt.receipt_identity, compute_structural_invalidation_payload_sha256(receipt.receipt_identity, scope), governed.authority_identity)
    with pytest.raises(EvaluationError) as caught:
        invalidate_structural_evaluation_receipt(receipt, command, governed, scope)
    assert caught.value.code == "INACTIVE_AUTHORITY"


def test_fresh_process_reproduces_exact_receipt_bytes() -> None:
    repository = Path(__file__).resolve().parents[3]
    environment = dict(os.environ); environment["PYTHONPATH"] = os.pathsep.join((str(repository / "src"), str(repository)))
    script = "from tests.stories.st_08_07.test_lineage_determinism_and_invalidation import issue; from cmf_builder.evaluation.structural_conversational_evaluation import canonical_json_bytes; import sys; sys.stdout.buffer.write(canonical_json_bytes(issue().as_dict()))"
    fresh = subprocess.check_output([sys.executable, "-c", script], cwd=repository, env=environment)
    assert fresh == canonical_json_bytes(issue().as_dict())

