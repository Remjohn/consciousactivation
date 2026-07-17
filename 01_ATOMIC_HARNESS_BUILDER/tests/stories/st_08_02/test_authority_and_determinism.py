from __future__ import annotations

from dataclasses import replace

import pytest

from cmf_builder.evaluation.maturity_promotion import (
    MaturityPromotionError,
    PromotionAction,
    build_rejection_receipt,
    canonical_json_bytes,
    promote_development_maturity,
    validate_repeat_command,
)
from tests.stories.st_08_02.test_development_maturity_promotion import (
    ACTOR,
    authority,
    command,
    digest,
    evaluation_identity,
    protected_evidence,
)


def test_identical_governed_inputs_produce_byte_identical_receipts() -> None:
    candidate = evaluation_identity()
    evidence = protected_evidence(candidate)
    first = promote_development_maturity(
        candidate=candidate,
        evidence=evidence,
        command=command(candidate.identity),
        authority=authority(candidate.identity),
    )
    second = promote_development_maturity(
        candidate=candidate,
        evidence=evidence,
        command=command(candidate.identity),
        authority=authority(candidate.identity),
    )

    assert first.receipt_identity == second.receipt_identity
    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())


def test_changed_rubric_identity_changes_receipt_identity() -> None:
    candidate = evaluation_identity()
    changed = replace(candidate, rubric_sha256=digest("changed-rubric"))
    first = promote_development_maturity(
        candidate=candidate,
        evidence=protected_evidence(candidate),
        command=command(candidate.identity),
        authority=authority(candidate.identity),
    )
    second = promote_development_maturity(
        candidate=changed,
        evidence=protected_evidence(changed),
        command=command(changed.identity, command_id="command-002"),
        authority=authority(changed.identity),
    )

    assert first.receipt_identity != second.receipt_identity
    assert first.evaluation_identity != second.evaluation_identity


def test_exact_authority_actor_action_and_resource_are_required() -> None:
    candidate = evaluation_identity()
    evidence = protected_evidence(candidate)

    with pytest.raises(MaturityPromotionError) as actor_error:
        promote_development_maturity(
            candidate=candidate,
            evidence=evidence,
            command=replace(command(candidate.identity), actor_id="other-actor"),
            authority=authority(candidate.identity),
        )
    assert actor_error.value.code == "AUTHORITY_ACTOR_MISMATCH"

    with pytest.raises(MaturityPromotionError) as resource_error:
        promote_development_maturity(
            candidate=candidate,
            evidence=evidence,
            command=command(candidate.identity),
            authority=authority(digest("different-resource")),
        )
    assert resource_error.value.code == "AUTHORITY_RESOURCE_MISMATCH"

    with pytest.raises(MaturityPromotionError) as action_error:
        promote_development_maturity(
            candidate=candidate,
            evidence=evidence,
            command=replace(command(candidate.identity), action=PromotionAction.INVALIDATE),
            authority=authority(candidate.identity),
        )
    assert action_error.value.code == "AUTHORITY_ACTION_MISMATCH"


def test_repeat_command_returns_existing_receipt_for_identical_payload() -> None:
    candidate = evaluation_identity()
    evidence = protected_evidence(candidate)
    cmd = command(candidate.identity)
    auth = authority(candidate.identity)
    receipt = promote_development_maturity(
        candidate=candidate,
        evidence=evidence,
        command=cmd,
        authority=auth,
    )

    assert validate_repeat_command(
        existing=receipt,
        candidate=candidate,
        evidence=evidence,
        command=cmd,
        authority=auth,
    ) is receipt


def test_conflicting_repeat_command_fails_closed() -> None:
    candidate = evaluation_identity()
    evidence = protected_evidence(candidate)
    receipt = promote_development_maturity(
        candidate=candidate,
        evidence=evidence,
        command=command(candidate.identity),
        authority=authority(candidate.identity),
    )

    with pytest.raises(MaturityPromotionError) as caught:
        validate_repeat_command(
            existing=receipt,
            candidate=candidate,
            evidence=evidence,
            command=command(candidate.identity, command_id="different-command"),
            authority=authority(candidate.identity),
        )

    assert caught.value.code == "CONFLICTING_REPEAT_COMMAND"


def test_rejection_receipt_is_deterministic_and_non_promoting() -> None:
    candidate = evaluation_identity()
    evidence = protected_evidence(candidate, hard_gates_passed=False)
    cmd = command(candidate.identity)
    try:
        promote_development_maturity(
            candidate=candidate,
            evidence=evidence,
            command=cmd,
            authority=authority(candidate.identity),
        )
    except MaturityPromotionError as error:
        first = build_rejection_receipt(error, command=cmd, candidate=candidate, evidence=evidence)
        second = build_rejection_receipt(error, command=cmd, candidate=candidate, evidence=evidence)
    else:  # pragma: no cover - the assertion above must reject
        raise AssertionError("expected hard-gate rejection")

    assert first == second
    assert first["outcome"] == "REJECTED_NO_MATURITY_RECEIPT"
    assert first["production_ready"] is False
    assert first["certified"] is False
    assert first["command_identity"] == cmd.command_identity
    assert first["candidate_identity"] == candidate.identity
    assert first["evidence_receipt_identity"] == evidence.receipt_identity


def test_receipt_records_authority_without_closing_evidence_gate() -> None:
    candidate = evaluation_identity()
    evidence = protected_evidence(candidate)
    receipt = promote_development_maturity(
        candidate=candidate,
        evidence=evidence,
        command=command(candidate.identity),
        authority=authority(candidate.identity),
    )

    assert receipt.authority_identity == authority(candidate.identity).authority_identity
    assert receipt.as_dict()["evidence_gate_closed"] is False
    assert receipt.as_dict()["observations"] == [
        "ST-08.02:ProtectedEvidenceReceiptValidated",
        "ST-08.02:DevelopmentMaturityReceiptIssued",
    ]
