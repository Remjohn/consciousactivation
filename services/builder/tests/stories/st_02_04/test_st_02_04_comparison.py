from cmf_builder.visual.atomicity_contracts import (
    BoundaryOptionKind,
    ComparisonDimension,
    EvidenceStatus,
    RiskDirection,
    RiskDomain,
)

from tests.stories.st_02_04.fixtures import comparison_result, grammar_result


def test_compiles_all_visible_alternatives_and_dimensions() -> None:
    result = comparison_result()

    assert {item.option_kind for item in result.packet.candidates} == set(
        BoundaryOptionKind
    )
    for candidate in result.packet.candidates:
        assert {item.dimension for item in candidate.dimensions} == set(
            ComparisonDimension
        )
        assert {item.domain for item in candidate.risks} == set(RiskDomain)
    assert {
        risk.direction for item in result.packet.candidates for risk in item.risks
    } == set(RiskDirection)


def test_preserves_exact_provisional_grammar_lineage() -> None:
    source = grammar_result()
    result = comparison_result(source=source)
    evidence = result.packet.grammar_evidence

    assert evidence.grammar_id == source.grammar.grammar_id
    assert evidence.grammar_artifact_sha256 == source.grammar.artifact_sha256
    assert evidence.induction_receipt_id == source.receipt.receipt_id
    assert evidence.induction_receipt_sha256 == source.receipt.receipt_sha256
    assert evidence.source_graph_ids == tuple(
        item.graph_id for item in source.grammar.source_graphs
    )
    for candidate in result.packet.candidates:
        for dimension in candidate.dimensions:
            if dimension.evidence_status is EvidenceStatus.DETERMINISTIC_SYNTAX:
                assert dimension.motif_ids
                assert not dimension.hypothesis_ids
            elif dimension.evidence_status is EvidenceStatus.PROVISIONAL_HYPOTHESIS:
                assert dimension.hypothesis_ids
                assert not dimension.motif_ids


def test_packet_is_unratified_and_cannot_authorize_descendants() -> None:
    packet = comparison_result().packet

    assert packet.knowledge_status == "PROVISIONAL_COMPARISON"
    assert packet.decision_status == "UNRATIFIED"
    assert packet.evidence_gate_status == "EVIDENCE_PENDING"
    assert packet.human_decision_required is True
    assert packet.genesis_authorized is False
    assert packet.production_ready is False
    assert packet.certified is False


def test_receipt_is_exactly_bound_to_packet_and_source() -> None:
    result = comparison_result()
    receipt = result.receipt

    assert receipt.packet_id == result.packet.packet_id
    assert receipt.packet_artifact_sha256 == result.packet.artifact_sha256
    assert receipt.grammar_id == result.packet.grammar_evidence.grammar_id
    assert receipt.induction_receipt_sha256 == (
        result.packet.grammar_evidence.induction_receipt_sha256
    )
    assert receipt.candidate_count == 4
    assert receipt.dimension_count_per_candidate == 10
