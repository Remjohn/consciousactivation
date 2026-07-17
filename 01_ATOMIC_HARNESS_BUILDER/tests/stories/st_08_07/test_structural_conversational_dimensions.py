from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from cmf_builder.evaluation.structural_conversational_evaluation import (
    CONVERSATIONAL_DIMENSION_IDS,
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


EXPECTED_DIMENSIONS = (
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
        "subject_id": "synthetic-structural-public-comment",
        "subject_version": "1.0.0-development",
        "subject_sha256": digest("synthetic-structural-public-comment"),
        "fixture_id": "st-08.07-structural-synthetic-non-personal",
        "fixture_sha256": digest("st-08.07-structural-synthetic-fixture"),
        "category_id": "conversational_activation_expression",
        "profile_id": "public_comment",
        "expected_reading": "A structural invitation whose response remains human-owned.",
        "proposed_reading": "A structural invitation whose response remains human-owned.",
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


def dominant_lock() -> WrongReadingLock:
    return WrongReadingLock(
        lock_id="lock-response-remains-human-owned",
        prohibited_reading="The human has accepted the Activative Call.",
        protected_meaning_ref=ref("human-response-ownership"),
        source_and_authority_refs=(ref("wrong-reading-policy"), ref("constitution")),
        applicability="APPLICABLE",
        rejection_rule="EXACT_OR_SEMANTIC_MATCH_REJECTS_WITHOUT_COMPENSATION",
        dominant=True,
    )


def dimensions(
    *,
    status_by_dimension: dict[str, DimensionStatus] | None = None,
    not_applicable_basis_by_dimension: dict[str, GovernedEvidenceRef] | None = None,
) -> tuple[IndependentDimensionResult, ...]:
    statuses = status_by_dimension or {}
    na_bases = not_applicable_basis_by_dimension or {}
    return tuple(
        IndependentDimensionResult(
            dimension_id=dimension_id,
            status=statuses.get(dimension_id, DimensionStatus.PASS),
            evidence_refs=(ref(f"dimension:{dimension_id}"),),
            limitation="synthetic structural development evidence only",
            failure_context=(
                f"{dimension_id} did not satisfy its independent structural gate"
                if statuses.get(dimension_id) is DimensionStatus.FAIL
                else ""
            ),
            not_applicable_basis=na_bases.get(dimension_id),
        )
        for dimension_id in EXPECTED_DIMENSIONS
    )


def human_owned_artifacts() -> tuple[HumanOwnedArtifactApplicability, ...]:
    return tuple(
        HumanOwnedArtifactApplicability(
            artifact_kind=artifact_kind,
            state=ApplicabilityState.STRUCTURALLY_APPLICABLE_HUMAN_EVIDENCE_NOT_PROVIDED,
            justification="structural applicability only; actual issuance remains human-owned",
        )
        for artifact_kind in (
            "ReactionReceipt",
            "ExpressionMoment",
            "IdentityDNAAmendmentApproval",
        )
    )


def evaluate(
    *,
    governed_subject: StructuralEvaluationSubject | None = None,
    results: tuple[IndependentDimensionResult, ...] | None = None,
):
    return evaluate_structural_conversation(
        subject=governed_subject or subject(),
        locks=(dominant_lock(),),
        dimensions=dimensions() if results is None else results,
        human_owned_artifacts=human_owned_artifacts(),
        predecessor_receipts=(digest("st-08.06-implementation-receipt"),),
    )


def test_all_eleven_dimensions_are_exact_complete_and_independently_visible() -> None:
    receipt = evaluate()
    payload = receipt.as_dict()

    assert CONVERSATIONAL_DIMENSION_IDS == EXPECTED_DIMENSIONS
    assert tuple(
        item.dimension_id for item in receipt.independent_dimension_results
    ) == EXPECTED_DIMENSIONS
    assert tuple(
        item["dimension_id"] for item in payload["independent_dimension_results"]
    ) == EXPECTED_DIMENSIONS
    assert len(receipt.independent_dimension_results) == 11
    assert all(item.evidence_refs for item in receipt.independent_dimension_results)
    assert all(item.limitation for item in receipt.independent_dimension_results)
    assert "aggregate" not in payload
    assert "score" not in payload


@pytest.mark.parametrize(
    "missing_dimension",
    ("role_clarity", "pattern_match", "no_text_survival", "wrong_reading_rejection"),
)
def test_no_dimension_may_be_silently_omitted(missing_dimension: str) -> None:
    incomplete = tuple(
        item for item in dimensions() if item.dimension_id != missing_dimension
    )

    with pytest.raises(EvaluationError) as exc_info:
        evaluate(results=incomplete)

    assert exc_info.value.code == "INCOMPLETE_CONVERSATIONAL_DIMENSION_COVERAGE"
    assert missing_dimension in exc_info.value.context["missing_dimensions"]


def test_duplicate_or_unknown_dimension_is_rejected() -> None:
    governed = dimensions()

    with pytest.raises(EvaluationError) as duplicate:
        evaluate(results=(*governed, governed[0]))
    assert duplicate.value.code == "DUPLICATE_CONVERSATIONAL_DIMENSION"

    with pytest.raises(EvaluationError) as unsupported:
        replace(governed[0], dimension_id="generic_quality")
    assert unsupported.value.code == "UNKNOWN_CONVERSATIONAL_DIMENSION"


def test_one_failed_dimension_cannot_be_compensated_by_ten_passing_dimensions() -> None:
    results = dimensions(status_by_dimension={"residue": DimensionStatus.FAIL})
    receipt = evaluate(results=results)

    by_id = {
        item.dimension_id: item for item in receipt.independent_dimension_results
    }
    assert by_id["residue"].status is DimensionStatus.FAIL
    assert all(
        item.status is DimensionStatus.PASS
        for dimension_id, item in by_id.items()
        if dimension_id != "residue"
    )
    assert receipt.decision is EvaluationDecision.FAIL_STRUCTURAL_DIMENSION
    assert receipt.active is False
    assert "aggregate" not in receipt.as_dict()
    assert "score" not in receipt.as_dict()


def test_not_applicable_is_explicit_profile_specific_and_justified() -> None:
    governed = dimensions(
        status_by_dimension={"no_text_survival": DimensionStatus.NOT_APPLICABLE},
        not_applicable_basis_by_dimension={
            "no_text_survival": ref("public-comment-no-text-survival-na-basis")
        },
    )

    receipt = evaluate(results=governed)
    result = next(
        item
        for item in receipt.independent_dimension_results
        if item.dimension_id == "no_text_survival"
    )
    assert result.status is DimensionStatus.NOT_APPLICABLE
    assert result.not_applicable_basis is not None
    assert "public-comment" in result.not_applicable_basis.ref_id
    assert receipt.decision is EvaluationDecision.PASS_STRUCTURAL_DEVELOPMENT_ONLY


def test_not_applicable_without_a_basis_is_not_missing_evidence_disguised() -> None:
    with pytest.raises(EvaluationError) as exc_info:
        dimensions(
            status_by_dimension={"no_text_survival": DimensionStatus.NOT_APPLICABLE}
        )
    assert exc_info.value.code == "MISSING_NOT_APPLICABLE_BASIS"


def test_structural_synthetic_non_personal_uncertified_classification_is_explicit() -> None:
    receipt = evaluate()
    classification = receipt.as_dict()["subject"]["fixture_classification"]

    assert classification == {
        "repository_owned": True,
        "synthetic": True,
        "structural_only": True,
        "non_personal": True,
        "non_production": True,
        "uncertified": True,
    }
    assert receipt.production_ready is False
    assert receipt.certified is False


@pytest.mark.parametrize(
    "profile_id",
    ("public_comment", "reply_dm", "reelcast_expression", "interview_expression"),
)
def test_all_governed_structural_conversational_profiles_preserve_category_identity(
    profile_id: str,
) -> None:
    receipt = evaluate(governed_subject=subject(profile_id=profile_id))
    payload = receipt.as_dict()

    assert payload["subject"]["category_id"] == "conversational_activation_expression"
    assert payload["subject"]["profile_id"] == profile_id
    assert receipt.decision is EvaluationDecision.PASS_STRUCTURAL_DEVELOPMENT_ONLY


@pytest.mark.parametrize(
    ("category_id", "profile_id", "expected_code"),
    (
        ("generic_non_activative", "public_comment", "UNSUPPORTED_CONVERSATIONAL_PROFILE"),
        (
            "conversational_activation_expression",
            "generic_timeline",
            "UNSUPPORTED_CONVERSATIONAL_PROFILE",
        ),
    ),
)
def test_conversation_cannot_be_flattened_into_generic_category_or_timeline_semantics(
    category_id: str,
    profile_id: str,
    expected_code: str,
) -> None:
    with pytest.raises(EvaluationError) as exc_info:
        evaluate(
            governed_subject=subject(category_id=category_id, profile_id=profile_id)
        )
    assert exc_info.value.code == expected_code


def test_independent_dimension_identity_changes_with_evidence_not_with_order() -> None:
    governed = dimensions()
    original = evaluate(results=governed)
    reordered = evaluate(results=tuple(reversed(governed)))
    changed_evidence = replace(
        governed[0],
        evidence_refs=(ref("changed-role-clarity-evidence"),),
    )
    changed = evaluate(results=(changed_evidence, *governed[1:]))

    assert reordered.receipt_identity == original.receipt_identity
    assert changed.receipt_identity != original.receipt_identity
    assert tuple(
        item["dimension_id"]
        for item in reordered.as_dict()["independent_dimension_results"]
    ) == EXPECTED_DIMENSIONS
