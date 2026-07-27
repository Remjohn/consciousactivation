from __future__ import annotations

from cmf_builder.visual.geometry import PixelBox
from cmf_builder.visual.graph_contracts import (
    CompositionVariableClass,
    GraphKind,
    RelationEvidence,
    SubstrateGraphPlan,
    SubstrateKind,
)
from cmf_builder.visual.normalization import (
    ComponentEvidence,
    NormalizationPolicy,
    SpecimenEvidence,
    normalize_evidence,
)
from cmf_builder.visual.ontology import (
    Applicability,
    ApplicabilityStatus,
    EvidenceOrigin,
    GovernedStatus,
    KnowledgeStatus,
    ObservationStatus,
    OntologyTerm,
    ProvenanceReference,
    SourceReference,
    SyntaxOntology,
    Uncertainty,
    UncertaintyKind,
)
from cmf_builder.visual.relationship_graphs import compile_substrate_graphs


CATEGORY = "short_form_edited_video"


def prov(name: str, character: str) -> ProvenanceReference:
    return ProvenanceReference(name, character * 64, "derived_from")


def component(
    component_id: str,
    *,
    box: PixelBox,
    structural_fields: dict[str, int] | None = None,
) -> ComponentEvidence:
    return ComponentEvidence.create(
        component_id=component_id,
        ontology_term_id="syntax_region",
        pixel_box=box,
        observation_status=ObservationStatus.MEASURED,
        knowledge_status=KnowledgeStatus.OBSERVATION,
        provenance=(prov("parser_v1", "b"),),
        uncertainty=Uncertainty(
            UncertaintyKind.EXACT, 1_000_000, "deterministic fixture"
        ),
        applicability=Applicability(
            ApplicabilityStatus.APPLICABLE, "declared structural component"
        ),
        structural_fields=structural_fields or {"frame_index": 0},
    )


def normalized(*components: ComponentEvidence):
    policy = NormalizationPolicy(
        "syntax_policy",
        "1.0.0",
        "exact_ratio_v1",
        (CATEGORY,),
        SyntaxOntology(
            "syntax_ontology",
            "1.0.0",
            (OntologyTerm("syntax_region", (CATEGORY,)),),
        ),
    )
    evidence = SpecimenEvidence(
        specimen_id="specimen_graph",
        source=SourceReference(
            "source_graph", "1.0.0", "a" * 64, "fixture_authority", True
        ),
        category_id=CATEGORY,
        canvas_width_px=100,
        canvas_height_px=100,
        governed_status=GovernedStatus.GOVERNED_SYNTHETIC,
        origin=EvidenceOrigin.DETERMINISTIC_CODE,
        provenance=(prov("source_lock", "c"),),
        components=tuple(components),
    )
    return normalize_evidence(
        run_id="normalize_graph_fixture", specimens=(evidence,), policy=policy
    ).specimens[0]


def ids(specimen) -> dict[str, str]:
    return {
        observation.component_id: observation.observation_id
        for observation in specimen.observations
    }


def relation(
    name: str,
    source: str,
    target: str,
    *,
    evidence: tuple[str, ...] | None = None,
) -> RelationEvidence:
    return RelationEvidence.create(
        relation=name,
        from_observation_id=source,
        to_observation_id=target,
        evidence_observation_ids=evidence or (source, target),
        observation_status=ObservationStatus.DETERMINISTICALLY_DERIVED,
        knowledge_status=KnowledgeStatus.DETERMINISTIC_DERIVATION,
        origin=EvidenceOrigin.DETERMINISTIC_CODE,
        provenance=(prov("relation_parser", "d"),),
        uncertainty=Uncertainty(
            UncertaintyKind.EXACT, 1_000_000, "deterministic relationship"
        ),
        applicability=Applicability(
            ApplicabilityStatus.APPLICABLE, "relation applies to substrate"
        ),
    )


def plan(substrate: SubstrateKind, *relations: RelationEvidence) -> SubstrateGraphPlan:
    return SubstrateGraphPlan(
        plan_id="substrate_graph_plan",
        version="1.0.0",
        substrate=substrate,
        authority_ref="offline_fixture_authority",
        relations=tuple(relations),
    )


def test_static_visual_compiles_spatial_and_reading_order_graphs() -> None:
    specimen = normalized(
        component("left", box=PixelBox(0, 0, 20, 20)),
        component("right", box=PixelBox(30, 0, 20, 20)),
    )
    lookup = ids(specimen)
    result = compile_substrate_graphs(
        run_id="compile_static_graphs",
        specimen=specimen,
        plan=plan(
            SubstrateKind.STATIC_VISUAL,
            relation("LEFT_OF", lookup["left"], lookup["right"]),
            relation("READING_PRECEDES", lookup["left"], lookup["right"]),
        ),
    )

    assert [graph.graph_kind for graph in result.graphs] == [
        GraphKind.SPATIAL,
        GraphKind.READING_ORDER,
    ]
    assert [edge.relation for edge in result.graphs[0].edges] == ["LEFT_OF"]
    assert [edge.relation for edge in result.graphs[1].edges] == [
        "READING_PRECEDES"
    ]
    assert result.receipt.graph_count == 2
    assert result.receipt.node_count == 2
    assert result.receipt.edge_count == 2


def test_time_based_visual_compiles_spatial_temporal_and_reading_graphs() -> None:
    specimen = normalized(
        component(
            "first",
            box=PixelBox(0, 0, 20, 20),
            structural_fields={"start_ms": 0, "end_ms": 100},
        ),
        component(
            "second",
            box=PixelBox(30, 0, 20, 20),
            structural_fields={"start_ms": 100, "end_ms": 200},
        ),
    )
    lookup = ids(specimen)
    result = compile_substrate_graphs(
        run_id="compile_time_graphs",
        specimen=specimen,
        plan=plan(
            SubstrateKind.TIME_BASED_VISUAL,
            relation("LEFT_OF", lookup["first"], lookup["second"]),
            relation("TRANSITIONS_TO", lookup["first"], lookup["second"]),
            relation("READING_PRECEDES", lookup["first"], lookup["second"]),
        ),
    )

    assert [graph.graph_kind for graph in result.graphs] == [
        GraphKind.SPATIAL,
        GraphKind.TEMPORAL,
        GraphKind.READING_ORDER,
    ]
    assert result.receipt.graph_count == 3


def test_conversational_substrate_is_structural_not_a_timeline() -> None:
    specimen = normalized(
        component("turn_one", box=PixelBox(0, 0, 20, 20)),
        component("turn_two", box=PixelBox(0, 30, 20, 20)),
    )
    lookup = ids(specimen)
    result = compile_substrate_graphs(
        run_id="compile_conversation_graph",
        specimen=specimen,
        plan=plan(
            SubstrateKind.STRUCTURAL_CONVERSATIONAL,
            relation("TURN_PRECEDES", lookup["turn_one"], lookup["turn_two"]),
            relation("REPLIES_TO", lookup["turn_two"], lookup["turn_one"]),
        ),
    )

    assert len(result.graphs) == 1
    assert result.graphs[0].graph_kind is GraphKind.STRUCTURAL_CONVERSATIONAL
    assert {edge.relation for edge in result.graphs[0].edges} == {
        "TURN_PRECEDES",
        "REPLIES_TO",
    }


def test_graph_nodes_preserve_full_observation_evidence_and_uncertainty() -> None:
    specimen = normalized(component("subject", box=PixelBox(10, 10, 50, 50)))
    result = compile_substrate_graphs(
        run_id="preserve_node_evidence",
        specimen=specimen,
        plan=plan(SubstrateKind.STATIC_VISUAL),
    )

    node = result.graphs[0].nodes[0]
    original = specimen.observations[0]
    assert node.observation == original
    assert node.observation.source == original.source
    assert node.observation.provenance == original.provenance
    assert node.observation.uncertainty == original.uncertainty
    assert node.observation.applicability == original.applicability
    assert node.observation.knowledge_status is KnowledgeStatus.OBSERVATION


def test_graph_edges_preserve_relation_and_source_observation_lineage() -> None:
    specimen = normalized(
        component("left", box=PixelBox(0, 0, 20, 20)),
        component("right", box=PixelBox(30, 0, 20, 20)),
    )
    lookup = ids(specimen)
    result = compile_substrate_graphs(
        run_id="preserve_edge_evidence",
        specimen=specimen,
        plan=plan(
            SubstrateKind.STATIC_VISUAL,
            relation("LEFT_OF", lookup["left"], lookup["right"]),
        ),
    )

    edge = result.graphs[0].edges[0]
    assert edge.evidence_observation_ids == tuple(sorted(lookup.values()))
    assert edge.source.content_sha256 == "a" * 64
    assert edge.uncertainty.kind is UncertaintyKind.EXACT
    assert {item.artifact_id for item in edge.provenance} == {
        "parser_v1",
        "relation_parser",
        "source_lock",
    }


def test_composition_variables_are_typed_without_semantic_inference() -> None:
    specimen = normalized(
        component(
            "segment",
            box=PixelBox(10, 20, 30, 40),
            structural_fields={"start_ms": 0, "end_ms": 100, "frame_index": 2},
        )
    )
    result = compile_substrate_graphs(
        run_id="composition_variables",
        specimen=specimen,
        plan=plan(SubstrateKind.TIME_BASED_VISUAL),
    )
    variables = result.graphs[0].nodes[0].composition_variables

    assert {item.variable_class for item in variables} == {
        CompositionVariableClass.NORMALIZED_GEOMETRY,
        CompositionVariableClass.TEMPORAL_POSITION,
        CompositionVariableClass.STRUCTURAL_SEQUENCE,
    }
    assert all(item.observation_id == specimen.observations[0].observation_id for item in variables)
    assert not any(item.name in {"meaning", "intent", "why"} for item in variables)


def test_receipt_is_observable_but_never_claims_evidence_closure() -> None:
    specimen = normalized(component("subject", box=PixelBox(10, 10, 50, 50)))
    result = compile_substrate_graphs(
        run_id="receipt_observability",
        specimen=specimen,
        plan=plan(SubstrateKind.STATIC_VISUAL),
    )

    assert result.receipt.story_id == "ST-02.02"
    assert result.receipt.authority_identity == "offline_fixture_authority"
    assert result.receipt.outcome == "OUTCOME_VERIFIED"
    assert result.receipt.failure_context == "NONE"
    assert result.receipt.evidence_gate_status == "EVIDENCE_PENDING"
    assert result.receipt.production_ready is False
    assert result.receipt.certified is False

