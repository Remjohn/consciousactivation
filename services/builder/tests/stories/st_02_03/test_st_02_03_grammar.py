from __future__ import annotations

from cmf_builder.visual.grammar_contracts import GrammarMaturity, ProjectionMode
from cmf_builder.visual.graph_contracts import GraphKind, SubstrateKind
from cmf_builder.visual.induction import induce_provisional_grammar
from cmf_builder.visual.ontology import KnowledgeStatus

from fixtures import induction_policy, provisional_hypothesis, supported_graphs


def test_induces_only_cross_specimen_supported_substrate_motif() -> None:
    graphs = supported_graphs()
    result = induce_provisional_grammar(
        run_id="induce_supported_grammar",
        graphs=graphs,
        policy=induction_policy(),
    )

    assert len(result.grammar.motifs) == 1
    motif = result.grammar.motifs[0]
    assert motif.substrate is SubstrateKind.STATIC_VISUAL
    assert motif.graph_kind is GraphKind.SPATIAL
    assert motif.relation == "LEFT_OF"
    assert motif.from_ontology_term_id == "primary_region"
    assert motif.to_ontology_term_id == "secondary_region"
    assert motif.distinct_specimen_support == 2
    assert motif.knowledge_status is KnowledgeStatus.DETERMINISTIC_DERIVATION


def test_preserves_rich_source_graph_and_observation_references() -> None:
    graphs = supported_graphs()
    grammar = induce_provisional_grammar(
        run_id="preserve_rich_sources", graphs=graphs, policy=induction_policy()
    ).grammar

    assert {item.graph_id for item in grammar.source_graphs} == {
        graph.graph_id for graph in graphs
    }
    for graph_reference in grammar.source_graphs:
        assert graph_reference.artifact_sha256
        assert graph_reference.plan_sha256
        assert graph_reference.source_content_sha256
        assert graph_reference.source_content_sha256 == (
            graph_reference.observations[0].source.content_sha256
        )
        assert len(graph_reference.observations) == 2
        for observation in graph_reference.observations:
            assert observation.source.content_sha256
            assert observation.provenance
            assert observation.uncertainty.rationale
            assert observation.applicability.rationale
            assert observation.geometry_sha256
            assert observation.knowledge_status == "OBSERVATION"


def test_unsupported_meaning_remains_visibly_provisional() -> None:
    graphs = supported_graphs()
    hypothesis = provisional_hypothesis(graphs)
    grammar = induce_provisional_grammar(
        run_id="provisional_meaning",
        graphs=graphs,
        policy=induction_policy(),
        hypotheses=(hypothesis,),
    ).grammar

    emitted = grammar.hypotheses[0]
    assert emitted.knowledge_status is KnowledgeStatus.HYPOTHESIS
    assert emitted.maturity is GrammarMaturity.PROVISIONAL
    assert emitted.source_graph_ids == tuple(sorted(graph.graph_id for graph in graphs))
    assert emitted.source_edge_ids
    assert emitted.source_observation_ids
    assert grammar.production_ready is False
    assert grammar.certified is False


def test_temporal_sequence_motif_remains_temporal_and_not_flattened() -> None:
    graphs = supported_graphs(
        substrate=SubstrateKind.TIME_BASED_VISUAL,
        graph_kind=GraphKind.TEMPORAL,
        relation_name="TRANSITIONS_TO",
    )
    grammar = induce_provisional_grammar(
        run_id="temporal_grammar", graphs=graphs, policy=induction_policy()
    ).grammar

    motif = grammar.motifs[0]
    assert motif.substrate is SubstrateKind.TIME_BASED_VISUAL
    assert motif.graph_kind is GraphKind.TEMPORAL
    assert motif.relation == "TRANSITIONS_TO"
    assert grammar.projection_mode is ProjectionMode.SUBSTRATE_SPECIFIC


def test_receipt_exposes_identity_authority_version_and_provenance() -> None:
    graphs = supported_graphs()
    result = induce_provisional_grammar(
        run_id="receipt_fields", graphs=graphs, policy=induction_policy()
    )

    assert result.receipt.story_id == "ST-02.03"
    assert result.receipt.grammar_id == result.grammar.grammar_id
    assert result.receipt.grammar_version == result.grammar.version
    assert result.receipt.authority_identity == "offline_grammar_authority"
    assert result.receipt.source_graph_count == 2
    assert result.receipt.motif_count == 1
    assert result.receipt.provenance
    assert result.receipt.failure_context == "NONE"


def test_grammar_is_explicitly_provisional_and_evidence_pending() -> None:
    grammar = induce_provisional_grammar(
        run_id="maturity_boundary",
        graphs=supported_graphs(),
        policy=induction_policy(),
    ).grammar

    assert grammar.maturity is GrammarMaturity.PROVISIONAL
    assert grammar.evidence_gate_status == "EVIDENCE_PENDING"
    assert grammar.version.startswith("0.0.0-development+")
    assert grammar.production_ready is False
    assert grammar.certified is False
