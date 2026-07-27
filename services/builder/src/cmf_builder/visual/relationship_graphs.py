"""Deterministic substrate-specific graph compilation for ST-02.02."""

from __future__ import annotations

from fractions import Fraction

from cmf_builder.visual.graph_contracts import (
    CompositionVariable,
    CompositionVariableClass,
    GraphCompilationReceipt,
    GraphCompilationResult,
    GraphCycleDetected,
    GraphEdge,
    GraphKind,
    GraphNode,
    GraphPlanInvalid,
    RelationshipContradiction,
    RelationEvidence,
    SubstrateGraph,
    SubstrateGraphPlan,
    SubstrateKind,
    TemporalStateMissing,
    UntraceableGraphEdge,
    UnsupportedSubstrateRelation,
)
from cmf_builder.visual.normalization import NormalizedSpecimen, SyntaxObservation
from cmf_builder.visual.ontology import canonical_sha256, require_identifier


_SUBSTRATE_GRAPHS = {
    SubstrateKind.STATIC_VISUAL: (
        GraphKind.SPATIAL,
        GraphKind.READING_ORDER,
    ),
    SubstrateKind.TIME_BASED_VISUAL: (
        GraphKind.SPATIAL,
        GraphKind.TEMPORAL,
        GraphKind.READING_ORDER,
    ),
    SubstrateKind.STRUCTURAL_CONVERSATIONAL: (
        GraphKind.STRUCTURAL_CONVERSATIONAL,
    ),
}

_RELATIONS: dict[str, tuple[GraphKind, str, bool, bool]] = {
    # input relation: graph, canonical relation, reverse endpoints, symmetric
    "LEFT_OF": (GraphKind.SPATIAL, "LEFT_OF", False, False),
    "RIGHT_OF": (GraphKind.SPATIAL, "LEFT_OF", True, False),
    "ABOVE": (GraphKind.SPATIAL, "ABOVE", False, False),
    "BELOW": (GraphKind.SPATIAL, "ABOVE", True, False),
    "CONTAINS": (GraphKind.SPATIAL, "CONTAINS", False, False),
    "INSIDE": (GraphKind.SPATIAL, "CONTAINS", True, False),
    "OVERLAPS": (GraphKind.SPATIAL, "OVERLAPS", False, True),
    "ALIGNED_X": (GraphKind.SPATIAL, "ALIGNED_X", False, True),
    "ALIGNED_Y": (GraphKind.SPATIAL, "ALIGNED_Y", False, True),
    "READING_PRECEDES": (GraphKind.READING_ORDER, "READING_PRECEDES", False, False),
    "TEMPORAL_PRECEDES": (GraphKind.TEMPORAL, "TEMPORAL_PRECEDES", False, False),
    "TRANSITIONS_TO": (GraphKind.TEMPORAL, "TRANSITIONS_TO", False, False),
    "TEMPORALLY_OVERLAPS": (GraphKind.TEMPORAL, "TEMPORALLY_OVERLAPS", False, True),
    "TURN_PRECEDES": (
        GraphKind.STRUCTURAL_CONVERSATIONAL,
        "TURN_PRECEDES",
        False,
        False,
    ),
    "REPLIES_TO": (
        GraphKind.STRUCTURAL_CONVERSATIONAL,
        "REPLIES_TO",
        False,
        False,
    ),
}

_SEQUENCE_FIELDS = frozenset({"frame_index", "slide_index"})
_TEMPORAL_FIELDS = frozenset({"start_ms", "end_ms"})
_CONTENT_FIELDS = frozenset({"mask_sha256", "text_content_sha256"})


def _ratio(value: object) -> Fraction:
    return Fraction(value.numerator, value.denominator)  # type: ignore[attr-defined]


def _box(observation: SyntaxObservation) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    geometry = observation.geometry
    x = _ratio(geometry.x)
    y = _ratio(geometry.y)
    return x, y, x + _ratio(geometry.width), y + _ratio(geometry.height)


def _geometry_relation_holds(
    relation: str, source: SyntaxObservation, target: SyntaxObservation
) -> bool:
    sx1, sy1, sx2, sy2 = _box(source)
    tx1, ty1, tx2, ty2 = _box(target)
    if relation == "LEFT_OF":
        return sx2 <= tx1
    if relation == "ABOVE":
        return sy2 <= ty1
    if relation == "CONTAINS":
        return sx1 <= tx1 and sy1 <= ty1 and sx2 >= tx2 and sy2 >= ty2
    if relation == "OVERLAPS":
        return sx1 < tx2 and tx1 < sx2 and sy1 < ty2 and ty1 < sy2
    if relation == "ALIGNED_X":
        return sx1 + sx2 == tx1 + tx2
    if relation == "ALIGNED_Y":
        return sy1 + sy2 == ty1 + ty2
    return True


def _time_bounds(observation: SyntaxObservation) -> tuple[int, int]:
    fields = dict(observation.structural_fields)
    start = fields.get("start_ms")
    end = fields.get("end_ms")
    if (
        not isinstance(start, int)
        or isinstance(start, bool)
        or not isinstance(end, int)
        or isinstance(end, bool)
        or start < 0
        or end <= start
    ):
        raise TemporalStateMissing(
            "temporal relations require valid start_ms and end_ms observations",
            observation_id=observation.observation_id,
        )
    return start, end


def _temporal_relation_holds(
    relation: str, source: SyntaxObservation, target: SyntaxObservation
) -> bool:
    source_start, source_end = _time_bounds(source)
    target_start, target_end = _time_bounds(target)
    if relation == "TEMPORAL_PRECEDES":
        return source_end <= target_start
    if relation == "TRANSITIONS_TO":
        return source_end == target_start
    if relation == "TEMPORALLY_OVERLAPS":
        return source_start < target_end and target_start < source_end
    return True


def _composition_variables(observation: SyntaxObservation) -> tuple[CompositionVariable, ...]:
    values: list[tuple[CompositionVariableClass, str, str | int | bool]] = []
    geometry = observation.geometry
    for name, ratio in (
        ("geometry.x", geometry.x),
        ("geometry.y", geometry.y),
        ("geometry.width", geometry.width),
        ("geometry.height", geometry.height),
    ):
        values.append(
            (
                CompositionVariableClass.NORMALIZED_GEOMETRY,
                name,
                f"{ratio.numerator}/{ratio.denominator}",
            )
        )
    for name, value in observation.structural_fields:
        if name in _SEQUENCE_FIELDS:
            variable_class = CompositionVariableClass.STRUCTURAL_SEQUENCE
        elif name in _TEMPORAL_FIELDS:
            variable_class = CompositionVariableClass.TEMPORAL_POSITION
        elif name in _CONTENT_FIELDS:
            variable_class = CompositionVariableClass.CONTENT_REFERENCE
        else:  # ST-02.01 rejects unknown structural fields; retain defense in depth.
            raise GraphPlanInvalid(
                "observation contains an unclassified composition variable",
                observation_id=observation.observation_id,
                field=name,
            )
        values.append((variable_class, name, value))
    variables: list[CompositionVariable] = []
    for variable_class, name, value in sorted(
        values, key=lambda item: (item[0].value, item[1])
    ):
        payload = {
            "variable_class": variable_class.value,
            "name": name,
            "value": value,
            "observation_id": observation.observation_id,
            "provenance": [item.as_dict() for item in observation.provenance],
            "uncertainty": observation.uncertainty.as_dict(),
        }
        variables.append(
            CompositionVariable(
                variable_id=canonical_sha256(payload),
                variable_class=variable_class,
                name=name,
                value=value,
                observation_id=observation.observation_id,
                provenance=observation.provenance,
                uncertainty=observation.uncertainty,
            )
        )
    return tuple(variables)


def _canonical_edge(
    relation: RelationEvidence,
    *,
    observations: dict[str, SyntaxObservation],
    substrate: SubstrateKind,
) -> GraphEdge:
    relation_contract = _RELATIONS.get(relation.relation)
    if relation_contract is None:
        raise UnsupportedSubstrateRelation(
            "relation is not part of the governed substrate vocabulary",
            relation=relation.relation,
        )
    graph_kind, canonical_relation, reverse, symmetric = relation_contract
    if graph_kind not in _SUBSTRATE_GRAPHS[substrate]:
        raise UnsupportedSubstrateRelation(
            "relation is inappropriate for the declared substrate",
            relation=relation.relation,
            substrate=substrate.value,
        )
    missing = tuple(
        sorted(
            observation_id
            for observation_id in (
                relation.from_observation_id,
                relation.to_observation_id,
                *relation.evidence_observation_ids,
            )
            if observation_id not in observations
        )
    )
    if missing:
        raise UntraceableGraphEdge(
            "graph edge references observations outside the normalized specimen",
            missing_observation_ids=missing,
        )
    if not {
        relation.from_observation_id,
        relation.to_observation_id,
    }.issubset(relation.evidence_observation_ids):
        raise UntraceableGraphEdge(
            "relation evidence must include both endpoint observations"
        )

    from_id = relation.from_observation_id
    to_id = relation.to_observation_id
    if reverse:
        from_id, to_id = to_id, from_id
    if symmetric and to_id < from_id:
        from_id, to_id = to_id, from_id
    source_observation = observations[from_id]
    target_observation = observations[to_id]

    if graph_kind is GraphKind.SPATIAL and not _geometry_relation_holds(
        canonical_relation, source_observation, target_observation
    ):
        raise RelationshipContradiction(
            "declared spatial relation contradicts measured geometry",
            relation=canonical_relation,
            from_observation_id=from_id,
            to_observation_id=to_id,
        )
    if graph_kind is GraphKind.TEMPORAL and not _temporal_relation_holds(
        canonical_relation, source_observation, target_observation
    ):
        raise RelationshipContradiction(
            "declared temporal relation contradicts measured time states",
            relation=canonical_relation,
            from_observation_id=from_id,
            to_observation_id=to_id,
        )

    evidence_provenance = {
        provenance
        for observation_id in relation.evidence_observation_ids
        for provenance in observations[observation_id].provenance
    }
    provenance = tuple(
        sorted(
            {*relation.provenance, *evidence_provenance},
            key=lambda item: (
                item.artifact_id,
                item.relationship,
                item.artifact_sha256,
            ),
        )
    )
    source = source_observation.source
    if any(
        observations[item].source.content_sha256 != source.content_sha256
        for item in relation.evidence_observation_ids
    ):
        raise UntraceableGraphEdge(
            "one specimen graph cannot combine unrelated source identities"
        )
    payload = {
        "graph_kind": graph_kind.value,
        "relation": canonical_relation,
        "from_node_id": from_id,
        "to_node_id": to_id,
        "evidence_observation_ids": list(relation.evidence_observation_ids),
        "source": source.as_dict(),
        "observation_status": relation.observation_status.value,
        "knowledge_status": relation.knowledge_status.value,
        "origin": relation.origin.value,
        "provenance": [item.as_dict() for item in provenance],
        "uncertainty": relation.uncertainty.as_dict(),
        "applicability": relation.applicability.as_dict(),
    }
    return GraphEdge(
        edge_id=canonical_sha256(payload),
        graph_kind=graph_kind,
        relation=canonical_relation,
        from_node_id=from_id,
        to_node_id=to_id,
        evidence_observation_ids=relation.evidence_observation_ids,
        source=source,
        observation_status=relation.observation_status,
        knowledge_status=relation.knowledge_status,
        origin=relation.origin,
        provenance=provenance,
        uncertainty=relation.uncertainty,
        applicability=relation.applicability,
    )


def _cycle_groups(graph_kind: GraphKind, edges: tuple[GraphEdge, ...]) -> tuple[tuple[GraphEdge, ...], ...]:
    if graph_kind is GraphKind.SPATIAL:
        return tuple(
            tuple(edge for edge in edges if edge.relation == relation)
            for relation in ("LEFT_OF", "ABOVE", "CONTAINS")
        )
    if graph_kind is GraphKind.TEMPORAL:
        return (
            tuple(
                edge
                for edge in edges
                if edge.relation in {"TEMPORAL_PRECEDES", "TRANSITIONS_TO"}
            ),
        )
    if graph_kind is GraphKind.READING_ORDER:
        return (edges,)
    return tuple(
        tuple(edge for edge in edges if edge.relation == relation)
        for relation in ("TURN_PRECEDES", "REPLIES_TO")
    )


def _assert_acyclic(graph_kind: GraphKind, edges: tuple[GraphEdge, ...]) -> None:
    for group in _cycle_groups(graph_kind, edges):
        adjacency: dict[str, set[str]] = {}
        for edge in group:
            adjacency.setdefault(edge.from_node_id, set()).add(edge.to_node_id)
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node_id: str) -> None:
            if node_id in visiting:
                raise GraphCycleDetected(
                    "substrate relationship cycle is prohibited",
                    graph_kind=graph_kind.value,
                )
            if node_id in visited:
                return
            visiting.add(node_id)
            for target in sorted(adjacency.get(node_id, set())):
                visit(target)
            visiting.remove(node_id)
            visited.add(node_id)

        for node_id in sorted(adjacency):
            visit(node_id)


def _build_graph(
    *,
    graph_kind: GraphKind,
    substrate: SubstrateKind,
    specimen: NormalizedSpecimen,
    plan: SubstrateGraphPlan,
    nodes: tuple[GraphNode, ...],
    edges: tuple[GraphEdge, ...],
) -> SubstrateGraph:
    _assert_acyclic(graph_kind, edges)
    core = {
        "graph_kind": graph_kind.value,
        "substrate": substrate.value,
        "specimen_id": specimen.specimen_id,
        "specimen_artifact_sha256": specimen.artifact_sha256,
        "plan_sha256": plan.plan_sha256,
        "nodes": [item.as_dict() for item in nodes],
        "edges": [item.as_dict() for item in edges],
    }
    artifact_sha256 = canonical_sha256(core)
    return SubstrateGraph(
        graph_id=f"ST-02.02:{graph_kind.value}:{artifact_sha256}",
        graph_kind=graph_kind,
        substrate=substrate,
        specimen_id=specimen.specimen_id,
        specimen_artifact_sha256=specimen.artifact_sha256,
        plan_sha256=plan.plan_sha256,
        nodes=nodes,
        edges=edges,
        artifact_sha256=artifact_sha256,
    )


def compile_substrate_graphs(
    *,
    run_id: str,
    specimen: NormalizedSpecimen,
    plan: SubstrateGraphPlan,
) -> GraphCompilationResult:
    """Compile only explicitly evidenced substrate relations into immutable graphs."""

    require_identifier(run_id, "run_id")
    observations = {
        observation.observation_id: observation for observation in specimen.observations
    }
    if not observations:
        raise GraphPlanInvalid("normalized specimen has no syntax observations")
    if len(observations) != len(specimen.observations):
        raise GraphPlanInvalid("normalized specimen observation identities must be unique")
    nodes = tuple(
        GraphNode(
            node_id=observation.observation_id,
            observation=observation,
            composition_variables=_composition_variables(observation),
        )
        for observation in sorted(
            specimen.observations, key=lambda item: item.observation_id
        )
    )
    edges = tuple(
        sorted(
            (
                _canonical_edge(
                    relation,
                    observations=observations,
                    substrate=plan.substrate,
                )
                for relation in plan.relations
            ),
            key=lambda item: item.edge_id,
        )
    )
    edge_ids = tuple(item.edge_id for item in edges)
    if len(edge_ids) != len(set(edge_ids)):
        raise GraphPlanInvalid("duplicate canonical relationships are prohibited")

    graphs = tuple(
        _build_graph(
            graph_kind=graph_kind,
            substrate=plan.substrate,
            specimen=specimen,
            plan=plan,
            nodes=nodes,
            edges=tuple(edge for edge in edges if edge.graph_kind is graph_kind),
        )
        for graph_kind in _SUBSTRATE_GRAPHS[plan.substrate]
    )
    result_core = {
        "run_id": run_id,
        "story_id": "ST-02.02",
        "development_mode": "OD_AM_001_OFFLINE_DEVELOPMENT",
        "specimen_artifact_sha256": specimen.artifact_sha256,
        "plan_sha256": plan.plan_sha256,
        "graphs": [graph.as_dict() for graph in graphs],
        "evidence_gate_status": "EVIDENCE_PENDING",
        "production_ready": False,
        "certified": False,
    }
    result_sha256 = canonical_sha256(result_core)
    provenance = tuple(
        sorted(
            {
                reference
                for observation in specimen.observations
                for reference in observation.provenance
            },
            key=lambda item: (
                item.artifact_id,
                item.relationship,
                item.artifact_sha256,
            ),
        )
    )
    receipt = GraphCompilationReceipt(
        receipt_id=f"ST-02.02:OfflineGraphs:{result_sha256}",
        run_id=run_id,
        result_sha256=result_sha256,
        specimen_artifact_sha256=specimen.artifact_sha256,
        plan_sha256=plan.plan_sha256,
        authority_identity=plan.authority_ref,
        graph_count=len(graphs),
        node_count=len(nodes),
        edge_count=len(edges),
        provenance=provenance,
    )
    return GraphCompilationResult(
        result_sha256=result_sha256,
        graphs=graphs,
        receipt=receipt,
    )

