from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from cmf_builder.evaluation.structural_conversational_evaluation import (
    ApplicabilityState,
    ConsentState,
    DimensionStatus,
    EvaluationDecision,
    EvaluationError,
    GovernedEvidenceRef,
    HumanOwnedArtifactApplicability,
    IndependentDimensionResult,
    StructuralEvaluationSubject,
    WrongReadingLock,
    evaluate_structural_conversation,
)


DIMENSIONS = (
    "role_clarity",
    "pattern_match",
    "pattern_interruption",
    "prediction",
    "payoff",
    "affinity",
    "anticipation",
    "residue",
    "anti_cliche",
    "no_text_survival",
    "wrong_reading_rejection",
)


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def ref(label: str) -> GovernedEvidenceRef:
    return GovernedEvidenceRef(
        ref_id=f"governed:{label}",
        version="1.0.0-development",
        sha256=digest(f"{label}:bytes"),
        authority_ref=digest(f"{label}:authority"),
    )


def subject(**overrides: object) -> StructuralEvaluationSubject:
    values: dict[str, object] = {
        "subject_id": "synthetic-structural-reply-dm",
        "subject_version": "1.0.0-development",
        "subject_sha256": digest("synthetic-structural-reply-dm"),
        "fixture_id": "st-08.07-synthetic-non-personal-fixture",
        "fixture_sha256": digest("st-08.07-synthetic-fixture"),
        "category_id": "conversational_activation_expression",
        "profile_id": "reply_dm",
        "expected_reading": "A synthetic invitation whose acceptance remains human-owned.",
        "proposed_reading": "A synthetic invitation whose acceptance remains human-owned.",
        "response_ownership": "HUMAN_OWNED_EXTERNAL_NOT_PROVIDED",
        "consent_state": ConsentState.EXPLICIT_SYNTHETIC_NO_HUMAN_EVIDENCE,
        "evidence_active": True,
        "semantic_lineage_refs": (ref("activative-pack"), ref("activative-call")),
        "authority_refs": (ref("constitution"), ref("od-am-001")),
        "production_ready": False,
        "certified": False,
    }
    values.update(overrides)
    return StructuralEvaluationSubject(**values)


def dominant_lock(**overrides: object) -> WrongReadingLock:
    values: dict[str, object] = {
        "lock_id": "lock-human-acceptance-remains-external",
        "prohibited_reading": "The human accepted the Activative Call.",
        "protected_meaning_ref": ref("protected-human-acceptance"),
        "source_and_authority_refs": (ref("wrong-reading-policy"), ref("constitution")),
        "applicability": "APPLICABLE",
        "rejection_rule": "EXACT_OR_SEMANTIC_MATCH_REJECTS_WITHOUT_COMPENSATION",
        "dominant": True,
    }
    values.update(overrides)
    return WrongReadingLock(**values)


def dimensions(
    *,
    wrong_reading_status: DimensionStatus = DimensionStatus.PASS,
) -> tuple[IndependentDimensionResult, ...]:
    return tuple(
        IndependentDimensionResult(
            dimension_id=dimension_id,
            status=(
                wrong_reading_status
                if dimension_id == "wrong_reading_rejection"
                else DimensionStatus.PASS
            ),
            evidence_refs=(ref(f"dimension:{dimension_id}"),),
            limitation="synthetic structural development evidence only",
            failure_context=(
                "prohibited reading remains present"
                if dimension_id == "wrong_reading_rejection"
                and wrong_reading_status is DimensionStatus.FAIL
                else ""
            ),
        )
        for dimension_id in DIMENSIONS
    )


def human_owned_artifacts() -> tuple[HumanOwnedArtifactApplicability, ...]:
    return tuple(
        HumanOwnedArtifactApplicability(
            artifact_kind=artifact_kind,
            state=ApplicabilityState.STRUCTURALLY_APPLICABLE_HUMAN_EVIDENCE_NOT_PROVIDED,
            justification="structural applicability only; issuance remains attributable to a human",
        )
        for artifact_kind in (
            "ReactionReceipt",
            "ExpressionMoment",
            "IdentityDNAAmendmentApproval",
        )
    )


def evaluate(
    governed_subject: StructuralEvaluationSubject | None = None,
    *,
    locks: tuple[WrongReadingLock, ...] | None = None,
    results: tuple[IndependentDimensionResult, ...] | None = None,
):
    return evaluate_structural_conversation(
        subject=governed_subject or subject(),
        locks=(dominant_lock(),) if locks is None else locks,
        dimensions=dimensions() if results is None else results,
        human_owned_artifacts=human_owned_artifacts(),
        predecessor_receipts=(digest("st-08.06-implementation-receipt"),),
    )


def test_dominant_wrong_reading_lock_is_required() -> None:
    with pytest.raises(EvaluationError) as exc_info:
        evaluate(locks=())
    assert exc_info.value.code == "MISSING_DOMINANT_WRONG_READING_LOCK"

    with pytest.raises(EvaluationError) as exc_info:
        evaluate(locks=(replace(dominant_lock(), dominant=False),))
    assert exc_info.value.code == "MISSING_DOMINANT_WRONG_READING_LOCK"


@pytest.mark.parametrize(
    ("field_name", "value"),
    (
        ("lock_id", ""),
        ("prohibited_reading", ""),
        ("applicability", ""),
        ("rejection_rule", ""),
        ("source_and_authority_refs", ()),
    ),
)
def test_wrong_reading_lock_cannot_omit_governed_fields(
    field_name: str,
    value: object,
) -> None:
    with pytest.raises(EvaluationError):
        dominant_lock(**{field_name: value})


def test_matching_prohibited_reading_emits_hard_rejection_receipt() -> None:
    governed_subject = subject(
        proposed_reading="The human accepted the Activative Call.",
    )

    receipt = evaluate(governed_subject)

    assert receipt.decision is EvaluationDecision.FAIL_WRONG_READING_LOCK
    assert receipt.active is False
    assert receipt.production_ready is False
    assert receipt.certified is False
    assert any(result.matched for result in receipt.wrong_reading_lock_results)
    assert receipt.as_dict()["decision"] == "FAIL_WRONG_READING_LOCK"


def test_wrong_reading_match_is_not_compensated_by_all_passing_dimensions() -> None:
    governed_subject = subject(
        proposed_reading="The human accepted the Activative Call.",
    )
    all_passing = dimensions()
    assert all(item.status is DimensionStatus.PASS for item in all_passing)

    receipt = evaluate(governed_subject, results=all_passing)

    assert receipt.decision is EvaluationDecision.FAIL_WRONG_READING_LOCK
    assert receipt.active is False
    assert "aggregate" not in receipt.as_dict()
    assert "score" not in receipt.as_dict()


def test_failed_wrong_reading_dimension_is_independently_non_compensable() -> None:
    receipt = evaluate(
        results=dimensions(wrong_reading_status=DimensionStatus.FAIL),
    )

    assert receipt.decision is EvaluationDecision.FAIL_WRONG_READING_LOCK
    by_id = {item.dimension_id: item for item in receipt.independent_dimension_results}
    assert by_id["wrong_reading_rejection"].status is DimensionStatus.FAIL
    assert all(
        result.status is DimensionStatus.PASS
        for dimension_id, result in by_id.items()
        if dimension_id != "wrong_reading_rejection"
    )
    assert receipt.active is False


def test_silence_cannot_be_interpreted_as_consent() -> None:
    governed_subject = subject(consent_state="ASSUMED_FROM_SILENCE")

    with pytest.raises(EvaluationError) as exc_info:
        evaluate(governed_subject)
    assert exc_info.value.code == "CONSENT_CANNOT_BE_INFERRED_FROM_SILENCE"


def test_withdrawn_evidence_cannot_remain_active() -> None:
    governed_subject = subject(
        consent_state=ConsentState.WITHDRAWN,
        evidence_active=True,
    )

    with pytest.raises(EvaluationError) as exc_info:
        evaluate(governed_subject)
    assert exc_info.value.code == "WITHDRAWN_EVIDENCE_CANNOT_REMAIN_ACTIVE"


def test_withdrawn_inactive_evidence_preserves_history_but_cannot_pass() -> None:
    governed_subject = subject(
        consent_state=ConsentState.WITHDRAWN,
        evidence_active=False,
    )

    receipt = evaluate(governed_subject)

    assert receipt.decision is EvaluationDecision.BLOCKED_HUMAN_EVIDENCE_REQUIRED
    assert receipt.active is False
    assert receipt.historical_reproduction_preserved is True
    assert receipt.production_ready is False
    assert receipt.certified is False
