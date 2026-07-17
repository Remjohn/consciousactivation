from __future__ import annotations

from cmf_builder.visual.geometry import PixelBox
from cmf_builder.visual.graph_contracts import (
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
    canonical_json_bytes,
)
from cmf_builder.visual.relationship_graphs import compile_substrate_graphs


def prov(name: str, character: str) -> ProvenanceReference:
    return ProvenanceReference(name, character * 64, "derived_from")


def fixture():
    category = "short_form_edited_video"
    components = tuple(
        ComponentEvidence.create(
            component_id=component_id,
            ontology_term_id="region",
            pixel_box=box,
            observation_status=ObservationStatus.MEASURED,
            knowledge_status=KnowledgeStatus.OBSERVATION,
            provenance=(prov("parser", "b"),),
            uncertainty=Uncertainty(
                UncertaintyKind.EXACT, 1_000_000, "exact fixture"
            ),
            applicability=Applicability(
                ApplicabilityStatus.APPLICABLE, "static fixture"
            ),
            structural_fields={"frame_index": index},
        )
        for index, (component_id, box) in enumerate(
            (
                ("left", PixelBox(0, 0, 20, 20)),
                ("middle", PixelBox(30, 0, 20, 20)),
                ("right", PixelBox(60, 0, 20, 20)),
            )
        )
    )
    evidence = SpecimenEvidence(
        "specimen",
        SourceReference("source", "1.0.0", "a" * 64, "authority", True),
        category,
        100,
        100,
        GovernedStatus.GOVERNED_SYNTHETIC,
        EvidenceOrigin.DETERMINISTIC_CODE,
        (prov("source_lock", "c"),),
        components,
    )
    policy = NormalizationPolicy(
        "policy",
        "1.0.0",
        "exact_ratio_v1",
        (category,),
        SyntaxOntology(
            "ontology", "1.0.0", (OntologyTerm("region", (category,)),)
        ),
    )
    specimen = normalize_evidence(
        run_id="normalize", specimens=(evidence,), policy=policy
    ).specimens[0]
    ids = {item.component_id: item.observation_id for item in specimen.observations}
    return specimen, ids


def relation(name: str, source: str, target: str, reverse_provenance: bool = False):
    refs = (prov("z_relation", "d"), prov("a_relation", "e"))
    if reverse_provenance:
        refs = tuple(reversed(refs))
    return RelationEvidence.create(
        relation=name,
        from_observation_id=source,
        to_observation_id=target,
        evidence_observation_ids=(target, source),
        observation_status=ObservationStatus.DETERMINISTICALLY_DERIVED,
        knowledge_status=KnowledgeStatus.DETERMINISTIC_DERIVATION,
        origin=EvidenceOrigin.DETERMINISTIC_CODE,
        provenance=refs,
        uncertainty=Uncertainty(
            UncertaintyKind.EXACT, 1_000_000, "deterministic relation"
        ),
        applicability=Applicability(
            ApplicabilityStatus.APPLICABLE, "static graph"
        ),
    )


def compile_bytes(relations: tuple[RelationEvidence, ...]) -> bytes:
    specimen, _ = fixture()
    result = compile_substrate_graphs(
        run_id="deterministic_graph_run",
        specimen=specimen,
        plan=SubstrateGraphPlan(
            "plan",
            "1.0.0",
            SubstrateKind.STATIC_VISUAL,
            "authority",
            relations,
        ),
    )
    return canonical_json_bytes(result.as_dict())


def test_identical_inputs_are_byte_identical() -> None:
    _, ids = fixture()
    relations = (
        relation("LEFT_OF", ids["left"], ids["middle"]),
        relation("LEFT_OF", ids["middle"], ids["right"]),
    )
    assert compile_bytes(relations) == compile_bytes(relations)


def test_relation_and_provenance_order_do_not_change_result_bytes() -> None:
    _, ids = fixture()
    first = relation("LEFT_OF", ids["left"], ids["middle"])
    second = relation(
        "READING_PRECEDES", ids["left"], ids["middle"], reverse_provenance=True
    )
    equivalent_first = relation(
        "LEFT_OF", ids["left"], ids["middle"], reverse_provenance=True
    )
    equivalent_second = relation(
        "READING_PRECEDES", ids["left"], ids["middle"]
    )

    assert compile_bytes((first, second)) == compile_bytes(
        (equivalent_second, equivalent_first)
    )


def test_changed_relationship_produces_new_result_identity() -> None:
    specimen, ids = fixture()
    first = compile_substrate_graphs(
        run_id="deterministic_graph_run",
        specimen=specimen,
        plan=SubstrateGraphPlan(
            "plan",
            "1.0.0",
            SubstrateKind.STATIC_VISUAL,
            "authority",
            (relation("LEFT_OF", ids["left"], ids["middle"]),),
        ),
    )
    second = compile_substrate_graphs(
        run_id="deterministic_graph_run",
        specimen=specimen,
        plan=SubstrateGraphPlan(
            "plan",
            "1.0.0",
            SubstrateKind.STATIC_VISUAL,
            "authority",
            (relation("LEFT_OF", ids["left"], ids["right"]),),
        ),
    )

    assert first.result_sha256 != second.result_sha256
    assert first.receipt.receipt_sha256 != second.receipt.receipt_sha256


def test_symmetric_relation_has_canonical_edge_identity() -> None:
    specimen, ids = fixture()
    # Use aligned boxes constructed by the same fixture row.
    forward = compile_substrate_graphs(
        run_id="symmetric_forward",
        specimen=specimen,
        plan=SubstrateGraphPlan(
            "plan_forward",
            "1.0.0",
            SubstrateKind.STATIC_VISUAL,
            "authority",
            (relation("ALIGNED_Y", ids["left"], ids["middle"]),),
        ),
    )
    reverse = compile_substrate_graphs(
        run_id="symmetric_reverse",
        specimen=specimen,
        plan=SubstrateGraphPlan(
            "plan_reverse",
            "1.0.0",
            SubstrateKind.STATIC_VISUAL,
            "authority",
            (relation("ALIGNED_Y", ids["middle"], ids["left"]),),
        ),
    )

    assert forward.graphs[0].edges[0].edge_id == reverse.graphs[0].edges[0].edge_id
    assert forward.graphs[0].edges[0].from_node_id < forward.graphs[0].edges[0].to_node_id


def test_portable_output_contains_no_absolute_workspace_path() -> None:
    _, ids = fixture()
    rendered = compile_bytes(
        (relation("LEFT_OF", ids["left"], ids["middle"]),)
    ).decode("utf-8")

    assert "D:\\" not in rendered
    assert "C:\\" not in rendered
    assert "CONSCIOUS_ACTIVATIONS" not in rendered

