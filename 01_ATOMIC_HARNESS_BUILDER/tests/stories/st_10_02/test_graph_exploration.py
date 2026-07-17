import pytest

from cmf_builder.application.graph_exploration import (
    EdgeType,
    GraphEdge,
    GraphExplorationError,
    GraphFamily,
    GraphNode,
    GraphProjection,
    SemanticNodeType,
    ValidityState,
    direct_neighbors,
    explain_dependency_path,
    filter_graph,
    stale_projection,
    traverse_predecessors,
    traverse_successors,
)


def node(local_id, family=GraphFamily.PHASE_GRAPH, semantic_type=SemanticNodeType.PHASE, **attrs):
    return GraphNode(
        local_id=local_id,
        graph_family=family,
        semantic_type=semantic_type,
        source_record=f"source:{local_id}",
        evidence_ref=f"receipt:{local_id}",
        validity_state=attrs.pop("validity_state", ValidityState.ACTIVE),
        source_revision="rev:1",
        attributes=attrs,
    )


def edge(source, target, family=GraphFamily.PHASE_GRAPH, edge_type=EdgeType.PRECEDES, **kwargs):
    return GraphEdge(source, target, family, edge_type, f"source:{source}:{target}", f"evidence:{source}:{target}", ValidityState.ACTIVE, "rev:1", **kwargs)


def test_phase_graph_preserves_ordering_and_traversal():
    projection = GraphProjection(
        GraphFamily.PHASE_GRAPH,
        "rev:1",
        "source-revision:1",
        (node("phase:1", ordering=1), node("phase:2", ordering=2), node("phase:3", ordering=3)),
        (edge("phase:1", "phase:2"), edge("phase:2", "phase:3")),
    )

    assert projection.projection_identity
    assert [item.local_id for item in direct_neighbors(projection, "phase:2")] == ["phase:1", "phase:3"]
    assert [item.local_id for item in traverse_successors(projection, "phase:1", depth=2)] == ["phase:2", "phase:3"]
    assert [item.local_id for item in traverse_predecessors(projection, "phase:3", depth=2)] == ["phase:1", "phase:2"]


def test_context_graph_represents_redaction_invalidation_and_filtering():
    active = node("context:active", GraphFamily.CONTEXT_GRAPH, SemanticNodeType.CONTEXT_UNIT)
    redacted = node("context:redacted", GraphFamily.CONTEXT_GRAPH, SemanticNodeType.CONTEXT_UNIT, validity_state=ValidityState.REDACTED)
    invalidated = node("context:invalidated", GraphFamily.CONTEXT_GRAPH, SemanticNodeType.CONTEXT_UNIT, validity_state=ValidityState.INVALIDATED)
    projection = GraphProjection(GraphFamily.CONTEXT_GRAPH, "rev:1", "source-revision:1", (active, redacted, invalidated), (), acyclic_required=True)

    filtered = filter_graph(projection, validity_state=ValidityState.REDACTED)

    assert [item.local_id for item in filtered.nodes] == ["context:redacted"]
    assert invalidated.as_dict()["validity_state"] == "INVALIDATED"


def test_dependency_graph_explains_paths_without_claiming_external_ownership():
    story = node("story:st-10.03", GraphFamily.DEPENDENCY_GRAPH, SemanticNodeType.STORY_DEPENDENCY)
    receipt = node("receipt:st-10.02", GraphFamily.DEPENDENCY_GRAPH, SemanticNodeType.RECEIPT_DEPENDENCY)
    evidence = node("evidence:bd-007", GraphFamily.DEPENDENCY_GRAPH, SemanticNodeType.EXTERNAL_DEPENDENCY)
    projection = GraphProjection(
        GraphFamily.DEPENDENCY_GRAPH,
        "rev:1",
        "source-revision:1",
        (story, receipt, evidence),
        (
            edge("story:st-10.03", "receipt:st-10.02", GraphFamily.DEPENDENCY_GRAPH, EdgeType.DEPENDS_ON),
            edge("receipt:st-10.02", "evidence:bd-007", GraphFamily.DEPENDENCY_GRAPH, EdgeType.BLOCKED_BY),
        ),
    )

    path = explain_dependency_path(projection, "story:st-10.03", "evidence:bd-007")
    assert [item.target_id for item in path] == ["receipt:st-10.02", "evidence:bd-007"]

    with pytest.raises(GraphExplorationError) as exc:
        edge("story:st-10.03", "evidence:bd-007", GraphFamily.DEPENDENCY_GRAPH, EdgeType.BLOCKED_BY, external_dependency_builder_owned=True)
    assert exc.value.code == "EXTERNAL_DEPENDENCY_CLAIMED_BUILDER_OWNED"


def test_graph_family_flattening_dangling_edges_and_cycles_fail_closed():
    with pytest.raises(GraphExplorationError) as family:
        GraphProjection(GraphFamily.PHASE_GRAPH, "rev:1", "source-revision:1", (node("context:1", GraphFamily.CONTEXT_GRAPH, SemanticNodeType.CONTEXT_UNIT),), ())
    assert family.value.code == "GRAPH_FAMILY_FLATTENING_REJECTED"

    with pytest.raises(GraphExplorationError) as dangling:
        GraphProjection(GraphFamily.PHASE_GRAPH, "rev:1", "source-revision:1", (node("phase:1"),), (edge("phase:1", "phase:missing"),))
    assert dangling.value.code == "DANGLING_EDGE_REJECTED"

    with pytest.raises(GraphExplorationError) as cycle:
        GraphProjection(GraphFamily.PHASE_GRAPH, "rev:1", "source-revision:1", (node("a"), node("b")), (edge("a", "b"), edge("b", "a")))
    assert cycle.value.code == "CYCLE_REJECTED"


def test_missing_provenance_invalidated_active_and_stale_projection_are_rejected_or_visible():
    with pytest.raises(GraphExplorationError) as missing:
        GraphNode("phase:bad", GraphFamily.PHASE_GRAPH, SemanticNodeType.PHASE, "", "evidence", ValidityState.ACTIVE, "rev:1")
    assert missing.value.code == "MISSING_GOVERNED_FIELD"

    with pytest.raises(GraphExplorationError) as active:
        node("phase:invalid", invalidated=True)
    assert active.value.code == "INVALIDATED_NODE_REPRESENTED_ACTIVE"

    projection = GraphProjection(GraphFamily.PHASE_GRAPH, "rev:1", "source-revision:1", (node("phase:1"),), ())
    assert stale_projection(projection, "rev:2") is True
