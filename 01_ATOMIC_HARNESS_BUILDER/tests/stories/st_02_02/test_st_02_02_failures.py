from __future__ import annotations

import pytest

from cmf_builder.visual.geometry import PixelBox
from cmf_builder.visual.graph_contracts import (
    GraphCycleDetected,
    GraphPlanInvalid,
    RelationEvidence,
    RelationshipContradiction,
    SubstrateGraphPlan,
    SubstrateKind,
    TemporalStateMissing,
    UntraceableGraphEdge,
    UnsupportedSubstrateRelation,
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
    ObservationContaminated,
    ObservationStatus,
    OntologyTerm,
    ProvenanceReference,
    ProviderOnlyClaimRejected,
    SourceReference,
    SyntaxOntology,
    Uncertainty,
    UncertaintyKind,
)
from cmf_builder.visual.relationship_graphs import compile_substrate_graphs


def prov() -> ProvenanceReference:
    return ProvenanceReference("graph_parser", "b" * 64, "derived_from")


def normalized(*specs: tuple[str, PixelBox, dict[str, int]]):
    components = tuple(
        ComponentEvidence.create(
            component_id=component_id,
            ontology_term_id="region",
            pixel_box=box,
            observation_status=ObservationStatus.MEASURED,
            knowledge_status=KnowledgeStatus.OBSERVATION,
            provenance=(prov(),),
            uncertainty=Uncertainty(
                UncertaintyKind.EXACT, 1_000_000, "exact fixture"
            ),
            applicability=Applicability(
                ApplicabilityStatus.APPLICABLE, "structural fixture"
            ),
            structural_fields=fields,
        )
        for component_id, box, fields in specs
    )
    category = "short_form_edited_video"
    policy = NormalizationPolicy(
        "policy",
        "1.0.0",
        "exact_ratio_v1",
        (category,),
        SyntaxOntology(
            "ontology", "1.0.0", (OntologyTerm("region", (category,)),)
        ),
    )
    specimen = SpecimenEvidence(
        "specimen",
        SourceReference("source", "1.0.0", "a" * 64, "authority", True),
        category,
        100,
        100,
        GovernedStatus.GOVERNED_SYNTHETIC,
        EvidenceOrigin.DETERMINISTIC_CODE,
        (prov(),),
        components,
    )
    return normalize_evidence(
        run_id="normalize", specimens=(specimen,), policy=policy
    ).specimens[0]


def lookup(specimen) -> dict[str, str]:
    return {item.component_id: item.observation_id for item in specimen.observations}


def evidence(
    relation: str,
    source: str,
    target: str,
    *,
    evidence_ids: tuple[str, ...] | None = None,
    origin: EvidenceOrigin = EvidenceOrigin.DETERMINISTIC_CODE,
    knowledge: KnowledgeStatus = KnowledgeStatus.DETERMINISTIC_DERIVATION,
) -> RelationEvidence:
    return RelationEvidence.create(
        relation=relation,
        from_observation_id=source,
        to_observation_id=target,
        evidence_observation_ids=evidence_ids or (source, target),
        observation_status=ObservationStatus.DETERMINISTICALLY_DERIVED,
        knowledge_status=knowledge,
        origin=origin,
        provenance=(prov(),),
        uncertainty=Uncertainty(
            UncertaintyKind.EXACT, 1_000_000, "deterministic relation"
        ),
        applicability=Applicability(
            ApplicabilityStatus.APPLICABLE, "declared substrate"
        ),
    )


def plan(substrate: SubstrateKind, *relations: RelationEvidence) -> SubstrateGraphPlan:
    return SubstrateGraphPlan("plan", "1.0.0", substrate, "authority", tuple(relations))


def two_nodes(*, temporal: bool = False):
    first_fields = {"start_ms": 0, "end_ms": 100} if temporal else {"frame_index": 0}
    second_fields = {"start_ms": 100, "end_ms": 200} if temporal else {"frame_index": 1}
    return normalized(
        ("first", PixelBox(0, 0, 20, 20), first_fields),
        ("second", PixelBox(30, 0, 20, 20), second_fields),
    )


def test_rejects_unsupported_relation_vocabulary() -> None:
    specimen = two_nodes()
    ids = lookup(specimen)
    with pytest.raises(UnsupportedSubstrateRelation):
        compile_substrate_graphs(
            run_id="unsupported",
            specimen=specimen,
            plan=plan(
                SubstrateKind.STATIC_VISUAL,
                evidence("MEANS", ids["first"], ids["second"]),
            ),
        )


def test_rejects_category_inappropriate_relation() -> None:
    specimen = two_nodes()
    ids = lookup(specimen)
    with pytest.raises(UnsupportedSubstrateRelation):
        compile_substrate_graphs(
            run_id="wrong_substrate",
            specimen=specimen,
            plan=plan(
                SubstrateKind.STATIC_VISUAL,
                evidence("TURN_PRECEDES", ids["first"], ids["second"]),
            ),
        )


def test_rejects_dangling_endpoint() -> None:
    specimen = two_nodes()
    ids = lookup(specimen)
    with pytest.raises(UntraceableGraphEdge):
        compile_substrate_graphs(
            run_id="dangling",
            specimen=specimen,
            plan=plan(
                SubstrateKind.STATIC_VISUAL,
                evidence(
                    "LEFT_OF",
                    ids["first"],
                    "missing_observation",
                    evidence_ids=(ids["first"], "missing_observation"),
                ),
            ),
        )


def test_rejects_evidence_that_omits_an_endpoint() -> None:
    specimen = two_nodes()
    ids = lookup(specimen)
    with pytest.raises(UntraceableGraphEdge):
        compile_substrate_graphs(
            run_id="missing_endpoint_evidence",
            specimen=specimen,
            plan=plan(
                SubstrateKind.STATIC_VISUAL,
                evidence(
                    "LEFT_OF",
                    ids["first"],
                    ids["second"],
                    evidence_ids=(ids["first"],),
                ),
            ),
        )


def test_rejects_provider_only_relation() -> None:
    specimen = two_nodes()
    ids = lookup(specimen)
    with pytest.raises(ProviderOnlyClaimRejected):
        evidence(
            "LEFT_OF",
            ids["first"],
            ids["second"],
            origin=EvidenceOrigin.PROVIDER_ONLY,
        )


def test_rejects_relation_hypothesis() -> None:
    specimen = two_nodes()
    ids = lookup(specimen)
    with pytest.raises(ObservationContaminated):
        evidence(
            "LEFT_OF",
            ids["first"],
            ids["second"],
            knowledge=KnowledgeStatus.HYPOTHESIS,
        )


def test_rejects_self_edge() -> None:
    specimen = two_nodes()
    node_id = lookup(specimen)["first"]
    with pytest.raises(GraphPlanInvalid):
        evidence("LEFT_OF", node_id, node_id)


def test_rejects_spatial_relation_that_contradicts_geometry() -> None:
    specimen = two_nodes()
    ids = lookup(specimen)
    with pytest.raises(RelationshipContradiction):
        compile_substrate_graphs(
            run_id="spatial_contradiction",
            specimen=specimen,
            plan=plan(
                SubstrateKind.STATIC_VISUAL,
                evidence("LEFT_OF", ids["second"], ids["first"]),
            ),
        )


def test_rejects_temporal_relation_without_time_states() -> None:
    specimen = two_nodes()
    ids = lookup(specimen)
    with pytest.raises(TemporalStateMissing):
        compile_substrate_graphs(
            run_id="missing_time",
            specimen=specimen,
            plan=plan(
                SubstrateKind.TIME_BASED_VISUAL,
                evidence("TEMPORAL_PRECEDES", ids["first"], ids["second"]),
            ),
        )


def test_rejects_temporal_relation_that_contradicts_time_states() -> None:
    specimen = two_nodes(temporal=True)
    ids = lookup(specimen)
    with pytest.raises(RelationshipContradiction):
        compile_substrate_graphs(
            run_id="time_contradiction",
            specimen=specimen,
            plan=plan(
                SubstrateKind.TIME_BASED_VISUAL,
                evidence("TEMPORAL_PRECEDES", ids["second"], ids["first"]),
            ),
        )


def test_rejects_reading_order_cycle() -> None:
    specimen = two_nodes()
    ids = lookup(specimen)
    with pytest.raises(GraphCycleDetected):
        compile_substrate_graphs(
            run_id="reading_cycle",
            specimen=specimen,
            plan=plan(
                SubstrateKind.STATIC_VISUAL,
                evidence("READING_PRECEDES", ids["first"], ids["second"]),
                evidence("READING_PRECEDES", ids["second"], ids["first"]),
            ),
        )


def test_rejects_conversational_turn_cycle() -> None:
    specimen = two_nodes()
    ids = lookup(specimen)
    with pytest.raises(GraphCycleDetected):
        compile_substrate_graphs(
            run_id="turn_cycle",
            specimen=specimen,
            plan=plan(
                SubstrateKind.STRUCTURAL_CONVERSATIONAL,
                evidence("TURN_PRECEDES", ids["first"], ids["second"]),
                evidence("TURN_PRECEDES", ids["second"], ids["first"]),
            ),
        )


def test_rejects_duplicate_canonical_edge_through_inverse_alias() -> None:
    specimen = two_nodes()
    ids = lookup(specimen)
    with pytest.raises(GraphPlanInvalid):
        compile_substrate_graphs(
            run_id="duplicate_alias",
            specimen=specimen,
            plan=plan(
                SubstrateKind.STATIC_VISUAL,
                evidence("LEFT_OF", ids["first"], ids["second"]),
                evidence("RIGHT_OF", ids["second"], ids["first"]),
            ),
        )

