from __future__ import annotations

from dataclasses import replace
import hashlib
import inspect

import pytest

from cmf_builder.evaluation.independent_scoring import (
    BASE_DIMENSIONS,
    NON_COMPENSABLE_GATES,
    ControlledMutation,
    DevelopmentRubric,
    DimensionDistribution,
    DimensionScorecard,
    DimensionStatus,
    DownstreamResult,
    DownstreamResultType,
    GateResult,
    GateStatus,
    IndependentScoringError,
    IndependentScoringReceipt,
    RepeatedRunSummary,
    canonical_json_bytes,
)


GENERIC_CATEGORY = "generic_non_activative"
GENERIC_PROFILE = "synthetic_text_normalization_v1"
BUILDER_VERSION = "cmf-builder-od-am-001-development-v1"


def digest(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def rubric() -> DevelopmentRubric:
    return DevelopmentRubric(
        rubric_id="od-am-001-st-08-03-independent-dimensions",
        rubric_version="1.0.0-development",
        scoring_policy_version="1.0.0-development",
        evaluator_contract_version="offline-evaluator-v1",
        threshold_policy_reference="human_governed_not_defined",
        scoring_policy_sha256=digest("scoring-policy-v1"),
        threshold_policy_reference_sha256=digest("human-governed-threshold-policy"),
    )


def scorecards(
    *,
    visual_status: DimensionStatus = DimensionStatus.NOT_APPLICABLE,
    atomicity_score: int = 8_300,
) -> tuple[DimensionScorecard, ...]:
    cards: list[DimensionScorecard] = []
    for index, dimension in enumerate(BASE_DIMENSIONS):
        if dimension == "visual_and_temporal_understanding" and visual_status is DimensionStatus.NOT_APPLICABLE:
            cards.append(
                DimensionScorecard(
                    dimension=dimension,
                    status=DimensionStatus.NOT_APPLICABLE,
                    score_basis_points=None,
                    evidence_refs=(digest(f"{dimension}:applicability"),),
                    not_applicable_justification=(
                        "the governed generic text-normalization profile has no visual or temporal substrate"
                    ),
                )
            )
            continue
        score = atomicity_score if dimension == "atomicity" else 7_900 + (index * 100)
        cards.append(
            DimensionScorecard(
                dimension=dimension,
                status=DimensionStatus.PASSING,
                score_basis_points=score,
                evidence_refs=(digest(f"{dimension}:evidence"),),
            )
        )
    return tuple(cards)


def mutation() -> ControlledMutation:
    return ControlledMutation(
        mutation_id="mutation-preserve-topic-change-grammar",
        mutation_type="preserve_topic_change_grammar",
        base_case_sha256=digest("base-case"),
        mutated_input_sha256=digest("mutated-case"),
        changed_variables=("topic",),
        preserved_invariants=("grammar", "source_lineage", "target_contract"),
        expected_decision_sha256=digest("expected-decision"),
        source_lineage_sha256=digest("source-lineage"),
    )


def gates() -> tuple[GateResult, ...]:
    return tuple(
        GateResult(
            gate_id=gate_id,
            status=GateStatus.PASSING,
            evidence_refs=(digest(f"{gate_id}:evidence"),),
        )
        for gate_id in NON_COMPENSABLE_GATES
    )


def stability_summary() -> RepeatedRunSummary:
    return RepeatedRunSummary(
        repetition_identities=(digest("repeat-41"), digest("repeat-42"), digest("repeat-43")),
        distributions=tuple(
            DimensionDistribution(
                dimension=dimension,
                scores_basis_points=(7_900, 8_000, 8_100),
            )
            for dimension in BASE_DIMENSIONS
        ),
        dominant_failure_patterns=("none_observed_in_repository_development_fixture",),
    )


def downstream_result(
    *,
    builder_version: str = BUILDER_VERSION,
    artifact_sha256: str | None = None,
    origin_receipt_sha256: str | None = None,
) -> DownstreamResult:
    return DownstreamResult(
        result_type=DownstreamResultType.FIRST_PASS_ACCEPTANCE,
        builder_version=builder_version,
        evaluated_artifact_sha256=artifact_sha256 or digest("evaluated-artifact"),
        origin_receipt_sha256=origin_receipt_sha256 or digest("st-08-02-maturity-receipt"),
        authority_sha256=digest("downstream-result-authority"),
        payload_sha256=digest("downstream-result-payload"),
    )


def scoring_receipt(
    *,
    target_category: str = GENERIC_CATEGORY,
    target_profile: str = GENERIC_PROFILE,
    supplied_scorecards: tuple[DimensionScorecard, ...] | None = None,
    supplied_downstream: tuple[DownstreamResult, ...] | None = None,
    composite_trend_basis_points: int | None = 8_000,
    **claim_overrides: bool,
) -> IndependentScoringReceipt:
    kwargs = {
        "rubric": rubric(),
        "evaluated_artifact_sha256": digest("evaluated-artifact"),
        "builder_version": BUILDER_VERSION,
        "target_category": target_category,
        "source_ir_sha256": digest("source-ir"),
        "predecessor_maturity_receipt_sha256": digest("st-08-02-maturity-receipt"),
        "benchmark_portfolio_sha256": digest("repository-development-portfolio"),
        "case_identity_sha256": digest("generic-text-normalization-case"),
        "case_access_class": "development",
        "run_id": "st-08-03-development-run",
        "provenance_sha256": digest("case-provenance"),
        "command_identity": digest("issue-command"),
        "authority_identity": digest("offline-development-authority"),
        "scorecards": supplied_scorecards or scorecards(),
        "mutations": (mutation(),),
        "gates": gates(),
        "stability_summary": stability_summary(),
        "downstream_results": supplied_downstream or (downstream_result(),),
        "observations": (
            "ST-08.03:independent_dimension_scoring_completed",
            "ST-08.03:development_claim_ceiling_preserved",
        ),
        "composite_trend_basis_points": composite_trend_basis_points,
        **claim_overrides,
    }
    if "target_profile" in inspect.signature(IndependentScoringReceipt).parameters:
        kwargs["target_profile"] = target_profile
    return IndependentScoringReceipt(**kwargs)


def test_all_eight_dimensions_remain_independently_visible_in_canonical_order() -> None:
    receipt = scoring_receipt()
    payload = receipt.as_dict()

    assert len(BASE_DIMENSIONS) == 8
    assert tuple(item["dimension"] for item in payload["scorecards"]) == BASE_DIMENSIONS
    assert tuple(payload["rubric"]["dimensions"]) == BASE_DIMENSIONS
    assert len({card.scorecard_identity for card in receipt.scorecards}) == 8
    assert all(len(item["evidence_refs"]) >= 1 for item in payload["scorecards"])


def test_category_and_profile_applicability_are_explicit_and_identity_bound() -> None:
    parameters = inspect.signature(IndependentScoringReceipt).parameters
    assert "target_profile" in parameters, "target profile must be governed independently of category"

    original = scoring_receipt()
    changed_category = scoring_receipt(target_category="short_form_edited_video")
    changed_profile = scoring_receipt(target_profile="short_form_edited_video_v1")

    payload = original.as_dict()
    assert payload["target_category"] == GENERIC_CATEGORY
    assert payload["target_profile"] == GENERIC_PROFILE
    assert original.receipt_identity != changed_category.receipt_identity
    assert original.receipt_identity != changed_profile.receipt_identity


def test_not_applicable_is_explicit_justified_and_not_a_zero_score() -> None:
    receipt = scoring_receipt()
    visual = next(card for card in receipt.scorecards if card.dimension == "visual_and_temporal_understanding")

    assert visual.status is DimensionStatus.NOT_APPLICABLE
    assert visual.score_basis_points is None
    assert visual.not_applicable_justification
    assert visual.as_dict()["status"] == "not_applicable"
    assert visual.as_dict()["not_applicable_justification"].startswith("the governed generic")


@pytest.mark.parametrize(
    ("score", "justification", "expected_code"),
    (
        (0, "not used by this profile", "NOT_APPLICABLE_SCORE_PRESENT"),
        (None, None, "MISSING_GOVERNED_FIELD"),
    ),
)
def test_not_applicable_cannot_hide_a_score_or_missing_applicability_basis(
    score: int | None,
    justification: str | None,
    expected_code: str,
) -> None:
    with pytest.raises(IndependentScoringError) as caught:
        DimensionScorecard(
            dimension="visual_and_temporal_understanding",
            status=DimensionStatus.NOT_APPLICABLE,
            score_basis_points=score,
            evidence_refs=(digest("applicability-evidence"),),
            not_applicable_justification=justification,
        )

    assert caught.value.code == expected_code


def test_identical_canonical_inputs_produce_byte_identical_receipts() -> None:
    first = scoring_receipt()
    second = scoring_receipt()

    assert canonical_json_bytes(first.as_dict()) == canonical_json_bytes(second.as_dict())
    assert first.receipt_identity == second.receipt_identity


def test_changed_independent_dimension_changes_receipt_without_hiding_other_dimensions() -> None:
    original = scoring_receipt()
    changed_cards = tuple(
        replace(card, score_basis_points=7_100)
        if card.dimension == "atomicity"
        else card
        for card in scorecards()
    )
    changed = scoring_receipt(supplied_scorecards=changed_cards)

    assert original.receipt_identity != changed.receipt_identity
    original_payload = {item["dimension"]: item for item in original.as_dict()["scorecards"]}
    changed_payload = {item["dimension"]: item for item in changed.as_dict()["scorecards"]}
    assert changed_payload["atomicity"]["score_basis_points"] == 7_100
    for dimension in set(BASE_DIMENSIONS) - {"atomicity"}:
        assert changed_payload[dimension] == original_payload[dimension]


def test_downstream_result_must_match_builder_version_artifact_and_origin() -> None:
    mismatch_cases = (
        (downstream_result(builder_version="different-builder-version"), "DOWNSTREAM_BUILDER_VERSION_MISMATCH"),
        (downstream_result(artifact_sha256=digest("different-artifact")), "DOWNSTREAM_ARTIFACT_MISMATCH"),
        (downstream_result(origin_receipt_sha256=digest("different-origin")), "DOWNSTREAM_ORIGIN_MISMATCH"),
    )

    for result, expected_code in mismatch_cases:
        with pytest.raises(IndependentScoringError) as caught:
            scoring_receipt(supplied_downstream=(result,))
        assert caught.value.code == expected_code


def test_composite_trend_is_supplementary_and_never_authoritative() -> None:
    receipt = scoring_receipt(composite_trend_basis_points=9_999)
    payload = receipt.as_dict()

    assert payload["composite_trend_basis_points"] == 9_999
    assert payload["composite_trend_authoritative"] is False
    assert tuple(item["dimension"] for item in payload["scorecards"]) == BASE_DIMENSIONS
    assert all("score_basis_points" in item for item in payload["scorecards"])


@pytest.mark.parametrize(
    "claim_field",
    (
        "evidence_gate_closed",
        "production_threshold_defined",
        "production_ready",
        "certified",
    ),
)
def test_development_receipt_rejects_evidence_production_and_certification_claims(
    claim_field: str,
) -> None:
    with pytest.raises(IndependentScoringError) as caught:
        scoring_receipt(**{claim_field: True})

    assert caught.value.code == "PROHIBITED_PRODUCTION_OR_CERTIFICATION_CLAIM"
    assert caught.value.context["field"] == claim_field


def test_development_receipt_serializes_all_claim_ceilings_as_false() -> None:
    payload = scoring_receipt().as_dict()

    assert payload["evidence_gate_closed"] is False
    assert payload["production_threshold_defined"] is False
    assert payload["production_ready"] is False
    assert payload["certified"] is False
