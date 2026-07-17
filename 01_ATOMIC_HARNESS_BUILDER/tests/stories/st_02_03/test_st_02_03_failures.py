from __future__ import annotations

from dataclasses import replace

import pytest

from cmf_builder.visual.grammar_contracts import (
    GenericFlatteningRejected,
    GrammarAuthorityRejected,
    GrammarInductionPolicy,
    GraphEvidenceInvalid,
    InsufficientGraphSupport,
    KnowledgePromotionRejected,
    ProjectionMode,
)
from cmf_builder.visual.induction import induce_provisional_grammar
from cmf_builder.visual.ontology import canonical_sha256

from fixtures import (
    AUTHORITY,
    CATEGORY,
    PROPOSER,
    graph_fixture,
    induction_policy,
    provenance,
    provisional_hypothesis,
    supported_graphs,
)


def _rehash_edge(edge, **overrides):
    changed = replace(edge, **overrides)
    payload = {
        "graph_kind": changed.graph_kind.value,
        "relation": changed.relation,
        "from_node_id": changed.from_node_id,
        "to_node_id": changed.to_node_id,
        "evidence_observation_ids": list(changed.evidence_observation_ids),
        "source": changed.source.as_dict(),
        "observation_status": changed.observation_status.value,
        "knowledge_status": changed.knowledge_status.value,
        "origin": changed.origin.value,
        "provenance": [item.as_dict() for item in changed.provenance],
        "uncertainty": changed.uncertainty.as_dict(),
        "applicability": changed.applicability.as_dict(),
    }
    return replace(changed, edge_id=canonical_sha256(payload))


def _rehash_graph(graph, *, edges=None, nodes=None):
    changed = replace(
        graph,
        edges=graph.edges if edges is None else edges,
        nodes=graph.nodes if nodes is None else nodes,
    )
    payload = {
        "graph_kind": changed.graph_kind.value,
        "substrate": changed.substrate.value,
        "specimen_id": changed.specimen_id,
        "specimen_artifact_sha256": changed.specimen_artifact_sha256,
        "plan_sha256": changed.plan_sha256,
        "nodes": [item.as_dict() for item in changed.nodes],
        "edges": [item.as_dict() for item in changed.edges],
    }
    artifact_sha256 = canonical_sha256(payload)
    return replace(
        changed,
        artifact_sha256=artifact_sha256,
        graph_id=f"ST-02.02:{changed.graph_kind.value}:{artifact_sha256}",
    )


def test_rejects_single_specimen_induction() -> None:
    with pytest.raises(InsufficientGraphSupport):
        induce_provisional_grammar(
            run_id="one_specimen",
            graphs=(graph_fixture(0),),
            policy=induction_policy(),
        )


def test_rejects_graph_set_without_repeated_motif_support() -> None:
    graphs = (graph_fixture(0), graph_fixture(1, relation_name="ALIGNED_Y"))
    with pytest.raises(InsufficientGraphSupport):
        induce_provisional_grammar(
            run_id="no_supported_motif", graphs=graphs, policy=induction_policy()
        )


def test_rejects_tampered_graph_hash() -> None:
    first, second = supported_graphs()
    tampered = replace(first, artifact_sha256="f" * 64)
    with pytest.raises(GraphEvidenceInvalid):
        induce_provisional_grammar(
            run_id="tampered_graph",
            graphs=(tampered, second),
            policy=induction_policy(),
        )


def test_rejects_duplicate_graph_identity() -> None:
    graph = graph_fixture(0)
    with pytest.raises(GraphEvidenceInvalid):
        induce_provisional_grammar(
            run_id="duplicate_graph",
            graphs=(graph, graph),
            policy=induction_policy(),
        )


def test_rejects_relabelled_duplicate_source_content_as_distinct_support() -> None:
    graphs = (
        graph_fixture(0),
        graph_fixture(
            1,
            source_id="relabelled_source",
            source_content_sha256="1" * 64,
        ),
    )
    with pytest.raises(GraphEvidenceInvalid, match="source content"):
        induce_provisional_grammar(
            run_id="relabelled_duplicate_source",
            graphs=graphs,
            policy=induction_policy(),
        )


def test_rejects_edge_evidence_that_omits_one_endpoint_observation() -> None:
    first, second = supported_graphs()
    edge = first.edges[0]
    cross_wired_edge = _rehash_edge(
        edge,
        evidence_observation_ids=(edge.from_node_id,),
    )
    cross_wired_graph = _rehash_graph(first, edges=(cross_wired_edge,))
    with pytest.raises(GraphEvidenceInvalid, match="endpoint observations"):
        induce_provisional_grammar(
            run_id="cross_wired_edge_observation",
            graphs=(cross_wired_graph, second),
            policy=induction_policy(),
        )


def test_rejects_edge_provenance_detached_from_its_observations() -> None:
    first, second = supported_graphs()
    detached_edge = _rehash_edge(
        first.edges[0],
        provenance=(provenance("unrelated_evidence", "f"),),
    )
    detached_graph = _rehash_graph(first, edges=(detached_edge,))
    with pytest.raises(GraphEvidenceInvalid, match="provenance"):
        induce_provisional_grammar(
            run_id="detached_edge_provenance",
            graphs=(detached_graph, second),
            policy=induction_policy(),
        )


def test_rejects_cross_category_flattening() -> None:
    graphs = supported_graphs(category_id="different_category")
    with pytest.raises(GraphEvidenceInvalid):
        induce_provisional_grammar(
            run_id="cross_category", graphs=graphs, policy=induction_policy()
        )


def test_rejects_generic_flattened_projection_policy() -> None:
    with pytest.raises(GenericFlatteningRejected):
        GrammarInductionPolicy(
            policy_id="flattened_policy",
            version="1.0.0",
            category_id=CATEGORY,
            minimum_distinct_specimen_support=2,
            induction_authority_ref=AUTHORITY,
            allowed_hypothesis_proposers=(PROPOSER,),
            projection_mode=ProjectionMode.GENERIC_FLATTENED,
        )


def test_rejects_unauthorized_hypothesis_proposer() -> None:
    graphs = supported_graphs()
    hypothesis = provisional_hypothesis(graphs, proposer="unauthorized_agent")
    with pytest.raises(GrammarAuthorityRejected):
        induce_provisional_grammar(
            run_id="unauthorized_hypothesis",
            graphs=graphs,
            policy=induction_policy(),
            hypotheses=(hypothesis,),
        )


def reissue(hypothesis, **overrides):
    values = {
        "scope": hypothesis.scope,
        "statement": hypothesis.statement,
        "proposer_authority_ref": hypothesis.proposer_authority_ref,
        "source_graph_ids": hypothesis.source_graph_ids,
        "source_edge_ids": hypothesis.source_edge_ids,
        "source_observation_ids": hypothesis.source_observation_ids,
        "alternatives": hypothesis.alternatives,
        "provenance": hypothesis.provenance,
        "uncertainty": hypothesis.uncertainty,
    }
    values.update(overrides)
    return type(hypothesis).create(**values)


def test_rejects_hypothesis_with_unknown_graph_reference() -> None:
    graphs = supported_graphs()
    hypothesis = reissue(
        provisional_hypothesis(graphs), source_graph_ids=("unknown_graph",)
    )
    with pytest.raises(GraphEvidenceInvalid):
        induce_provisional_grammar(
            run_id="unknown_graph_ref",
            graphs=graphs,
            policy=induction_policy(),
            hypotheses=(hypothesis,),
        )


def test_rejects_hypothesis_with_unknown_edge_reference() -> None:
    graphs = supported_graphs()
    hypothesis = reissue(
        provisional_hypothesis(graphs), source_edge_ids=("unknown_edge",)
    )
    with pytest.raises(GraphEvidenceInvalid):
        induce_provisional_grammar(
            run_id="unknown_edge_ref",
            graphs=graphs,
            policy=induction_policy(),
            hypotheses=(hypothesis,),
        )


def test_rejects_hypothesis_with_unknown_observation_reference() -> None:
    graphs = supported_graphs()
    hypothesis = reissue(
        provisional_hypothesis(graphs),
        source_observation_ids=("unknown_observation",),
    )
    with pytest.raises(GraphEvidenceInvalid):
        induce_provisional_grammar(
            run_id="unknown_observation_ref",
            graphs=graphs,
            policy=induction_policy(),
            hypotheses=(hypothesis,),
        )


def test_rejects_hypothesis_cross_wired_across_graph_edge_and_observation() -> None:
    graphs = supported_graphs()
    foreign_edge = graphs[1].edges[0]
    hypothesis = reissue(
        provisional_hypothesis(graphs),
        source_graph_ids=(graphs[0].graph_id,),
        source_edge_ids=(foreign_edge.edge_id,),
        source_observation_ids=foreign_edge.evidence_observation_ids,
    )
    with pytest.raises(GraphEvidenceInvalid, match="cross-wires"):
        induce_provisional_grammar(
            run_id="cross_wired_hypothesis_lineage",
            graphs=graphs,
            policy=induction_policy(),
            hypotheses=(hypothesis,),
        )


@pytest.mark.parametrize(
    "claim",
    [
        "This grammar is production ready.",
        "This pattern is certified.",
        "A Reaction Receipt issued from syntax.",
        "The human reaction is approval.",
    ],
)
def test_rejects_authority_promotion_inside_hypothesis(claim: str) -> None:
    with pytest.raises(KnowledgePromotionRejected):
        provisional_hypothesis(supported_graphs(), statement=claim)


def test_rejects_hypothesis_payload_changed_without_new_identity() -> None:
    graphs = supported_graphs()
    hypothesis = replace(
        provisional_hypothesis(graphs), statement="A different unbound statement."
    )
    with pytest.raises(KnowledgePromotionRejected):
        induce_provisional_grammar(
            run_id="hypothesis_identity_drift",
            graphs=graphs,
            policy=induction_policy(),
            hypotheses=(hypothesis,),
        )


def test_rejects_duplicate_hypothesis_identity() -> None:
    graphs = supported_graphs()
    hypothesis = provisional_hypothesis(graphs)
    with pytest.raises(KnowledgePromotionRejected):
        induce_provisional_grammar(
            run_id="duplicate_hypothesis",
            graphs=graphs,
            policy=induction_policy(),
            hypotheses=(hypothesis, hypothesis),
        )
