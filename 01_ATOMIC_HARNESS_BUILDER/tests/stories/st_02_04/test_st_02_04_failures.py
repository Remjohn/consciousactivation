from dataclasses import replace

import pytest

from cmf_builder.visual.atomicity_contracts import (
    AtomicityStatus,
    AlternativesIncomplete,
    BoundaryEvidenceInvalid,
    BoundaryOptionKind,
    ComparisonDimension,
    DimensionAssessment,
    EvidenceStatus,
    RecommendationDisposition,
    RiskDirection,
    UnsupportedCertaintyRejected,
)

from tests.stories.st_02_04.fixtures import (
    all_candidates,
    candidate,
    comparison_result,
    grammar_result,
)


def test_rejects_hidden_or_duplicate_alternative() -> None:
    source = grammar_result()
    candidates = all_candidates(source.grammar)

    with pytest.raises(AlternativesIncomplete):
        comparison_result(source=source, candidates=candidates[:-1])
    with pytest.raises(AlternativesIncomplete):
        comparison_result(
            source=source,
            candidates=(candidates[0], candidates[0], candidates[2], candidates[3]),
        )


def test_rejects_missing_dimension() -> None:
    source = grammar_result()
    candidates = list(all_candidates(source.grammar))
    candidates[0] = replace(candidates[0], dimensions=candidates[0].dimensions[:-1])

    with pytest.raises(AlternativesIncomplete):
        comparison_result(source=source, candidates=tuple(candidates))


def test_rejects_crosswired_or_unknown_evidence() -> None:
    source = grammar_result()
    candidates = list(all_candidates(source.grammar))
    dimensions = list(candidates[0].dimensions)
    dimensions[0] = replace(dimensions[0], source_graph_ids=("unknown_graph",))
    candidates[0] = replace(candidates[0], dimensions=tuple(dimensions))

    with pytest.raises(BoundaryEvidenceInvalid):
        comparison_result(source=source, candidates=tuple(candidates))


def test_missing_evidence_cannot_support_a_decisive_status() -> None:
    source = grammar_result()
    incomplete = candidate(
        source.grammar,
        BoundaryOptionKind.MERGE,
        status=AtomicityStatus.ATOMIC_HARNESS_CANDIDATE,
        recommendation=RecommendationDisposition.SUPPORT,
        unavailable_dimension=ComparisonDimension.RUNTIME_OWNERSHIP,
    )
    candidates = tuple(
        incomplete if item.option_kind is BoundaryOptionKind.MERGE else item
        for item in all_candidates(source.grammar)
    )

    with pytest.raises(BoundaryEvidenceInvalid):
        comparison_result(source=source, candidates=candidates)


def test_rejects_uncalibrated_protected_boundary_claim() -> None:
    source = grammar_result()
    candidates = list(all_candidates(source.grammar))
    dimensions = list(candidates[0].dimensions)
    dimensions[0] = replace(dimensions[0], protected_boundary_claim=True)
    candidates[0] = replace(candidates[0], dimensions=tuple(dimensions))

    with pytest.raises(UnsupportedCertaintyRejected):
        comparison_result(source=source, candidates=tuple(candidates))


def test_identifier_only_calibration_reference_cannot_create_protected_certainty() -> None:
    source = grammar_result()
    candidates = list(all_candidates(source.grammar))
    dimensions = list(candidates[0].dimensions)
    dimensions[0] = replace(
        dimensions[0],
        protected_boundary_claim=True,
        calibration_receipt_ref="unverified_calibration_receipt",
    )
    candidates[0] = replace(candidates[0], dimensions=tuple(dimensions))

    with pytest.raises(UnsupportedCertaintyRejected, match="no independently verifiable"):
        comparison_result(source=source, candidates=tuple(candidates))


def test_rejects_ratification_production_and_certification_claims() -> None:
    source = grammar_result()
    for forbidden in (
        "The boundary is a ratified boundary.",
        "This is production ready.",
        "This is certified output.",
        "Genesis authorized this alternative.",
    ):
        candidates = list(all_candidates(source.grammar))
        candidates[0] = replace(candidates[0], consequence=forbidden)
        with pytest.raises(UnsupportedCertaintyRejected):
            comparison_result(source=source, candidates=tuple(candidates))


@pytest.mark.parametrize(
    "forbidden",
    [
        "This boundary is approved for release and may proceed to Genesis.",
        "Owner sign-off cleared this boundary for deployment.",
    ],
)
def test_governed_reserved_authority_vocabulary_rejects_paraphrases(
    forbidden: str,
) -> None:
    source = grammar_result()
    candidates = list(all_candidates(source.grammar))
    candidates[0] = replace(candidates[0], consequence=forbidden)

    with pytest.raises(UnsupportedCertaintyRejected, match="authority-reserved"):
        comparison_result(source=source, candidates=tuple(candidates))


def test_unavailable_evidence_carries_no_hidden_references() -> None:
    source = grammar_result()
    candidates = list(all_candidates(source.grammar))
    dimensions = list(candidates[0].dimensions)
    dimensions[0] = DimensionAssessment(
        dimension=dimensions[0].dimension,
        finding="Evidence is not available.",
        evidence_status=EvidenceStatus.UNAVAILABLE,
        source_graph_ids=(source.grammar.source_graphs[0].graph_id,),
    )
    candidates[0] = replace(
        candidates[0],
        status=AtomicityStatus.INSUFFICIENT_EVIDENCE,
        recommendation=RecommendationDisposition.MORE_EVIDENCE,
        evidence_gaps=("Missing governed evidence",),
        dimensions=tuple(dimensions),
    )

    with pytest.raises(BoundaryEvidenceInvalid):
        comparison_result(source=source, candidates=tuple(candidates))


@pytest.mark.parametrize("field", ["source_graph_ids", "hypothesis_ids"])
def test_duplicate_assessment_evidence_references_fail_closed(field: str) -> None:
    source = grammar_result()
    candidates = list(all_candidates(source.grammar))
    dimensions = list(candidates[0].dimensions)
    assessment = dimensions[0]
    value = getattr(assessment, field)
    dimensions[0] = replace(assessment, **{field: (*value, value[0])})
    candidates[0] = replace(candidates[0], dimensions=tuple(dimensions))

    with pytest.raises(BoundaryEvidenceInvalid, match="unique"):
        comparison_result(source=source, candidates=tuple(candidates))


def test_duplicate_risk_evidence_references_fail_closed() -> None:
    source = grammar_result()
    candidates = list(all_candidates(source.grammar))
    risks = list(candidates[0].risks)
    risks[0] = replace(
        risks[0],
        source_graph_ids=(*risks[0].source_graph_ids, risks[0].source_graph_ids[0]),
    )
    candidates[0] = replace(candidates[0], risks=tuple(risks))

    with pytest.raises(BoundaryEvidenceInvalid, match="unique"):
        comparison_result(source=source, candidates=tuple(candidates))


def test_insufficient_evidence_state_is_bidirectionally_consistent() -> None:
    source = grammar_result()
    complete = list(all_candidates(source.grammar))
    complete[0] = replace(
        complete[0],
        status=AtomicityStatus.INSUFFICIENT_EVIDENCE,
        recommendation=RecommendationDisposition.MORE_EVIDENCE,
        evidence_gaps=("Claimed gap without an unavailable dimension",),
    )
    with pytest.raises(BoundaryEvidenceInvalid, match="agree bidirectionally"):
        comparison_result(source=source, candidates=tuple(complete))

    unavailable = candidate(
        source.grammar,
        BoundaryOptionKind.MERGE,
        unavailable_dimension=ComparisonDimension.RUNTIME_OWNERSHIP,
    )
    inconsistent = tuple(
        replace(unavailable, evidence_gaps=())
        if item.option_kind is BoundaryOptionKind.MERGE
        else item
        for item in all_candidates(source.grammar)
    )
    with pytest.raises(BoundaryEvidenceInvalid, match="agree bidirectionally"):
        comparison_result(source=source, candidates=inconsistent)


def test_consistent_missing_evidence_remains_visible_and_unratified() -> None:
    source = grammar_result()
    incomplete = candidate(
        source.grammar,
        BoundaryOptionKind.MERGE,
        unavailable_dimension=ComparisonDimension.RUNTIME_OWNERSHIP,
    )
    candidates = tuple(
        incomplete if item.option_kind is BoundaryOptionKind.MERGE else item
        for item in all_candidates(source.grammar)
    )

    result = comparison_result(source=source, candidates=candidates)
    merge = next(
        item
        for item in result.packet.candidates
        if item.option_kind is BoundaryOptionKind.MERGE
    )
    assert merge.status is AtomicityStatus.INSUFFICIENT_EVIDENCE
    assert merge.recommendation is RecommendationDisposition.MORE_EVIDENCE
    assert merge.evidence_gaps
    assert result.packet.decision_status == "UNRATIFIED"


def test_candidate_specific_risk_direction_swap_fails_closed() -> None:
    source = grammar_result()
    candidates = list(all_candidates(source.grammar))
    merge_index = next(
        index
        for index, item in enumerate(candidates)
        if item.option_kind is BoundaryOptionKind.MERGE
    )
    merge = candidates[merge_index]
    candidates[merge_index] = replace(
        merge,
        risks=tuple(
            replace(risk, direction=RiskDirection.OVER_SPLIT) for risk in merge.risks
        ),
    )

    with pytest.raises(BoundaryEvidenceInvalid, match="does not match"):
        comparison_result(source=source, candidates=tuple(candidates))
