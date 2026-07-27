from __future__ import annotations

from cmf_builder.visual.geometry import PixelBox
from cmf_builder.visual.grammar_contracts import (
    GrammarInductionPolicy,
    HypothesisScope,
    ProvisionalMeaningHypothesis,
)
from cmf_builder.visual.graph_contracts import (
    GraphKind,
    RelationEvidence,
    SubstrateGraph,
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
AUTHORITY = "offline_grammar_authority"
PROPOSER = "bounded_hypothesis_agent"


def provenance(name: str, character: str) -> ProvenanceReference:
    return ProvenanceReference(name, character * 64, "derived_from")


def induction_policy(
    *, category_id: str = CATEGORY, minimum_support: int = 2
) -> GrammarInductionPolicy:
    return GrammarInductionPolicy(
        policy_id="provisional_grammar_policy",
        version="1.0.0",
        category_id=category_id,
        minimum_distinct_specimen_support=minimum_support,
        induction_authority_ref=AUTHORITY,
        allowed_hypothesis_proposers=(PROPOSER,),
    )


def _component(
    component_id: str,
    term_id: str,
    box: PixelBox,
    fields: dict[str, int],
) -> ComponentEvidence:
    return ComponentEvidence.create(
        component_id=component_id,
        ontology_term_id=term_id,
        pixel_box=box,
        observation_status=ObservationStatus.MEASURED,
        knowledge_status=KnowledgeStatus.OBSERVATION,
        provenance=(provenance("fixture_parser", "b"),),
        uncertainty=Uncertainty(
            UncertaintyKind.EXACT, 1_000_000, "deterministic fixture"
        ),
        applicability=Applicability(
            ApplicabilityStatus.APPLICABLE, "governed structural evidence"
        ),
        structural_fields=fields,
    )


def graph_fixture(
    index: int,
    *,
    substrate: SubstrateKind = SubstrateKind.STATIC_VISUAL,
    graph_kind: GraphKind = GraphKind.SPATIAL,
    category_id: str = CATEGORY,
    relation_name: str = "LEFT_OF",
    geometry_offset: int = 0,
    source_id: str | None = None,
    source_content_sha256: str | None = None,
) -> SubstrateGraph:
    if substrate is SubstrateKind.TIME_BASED_VISUAL:
        first_fields = {"start_ms": 0, "end_ms": 100}
        second_fields = {"start_ms": 100, "end_ms": 200}
    else:
        first_fields = {"frame_index": 0}
        second_fields = {"frame_index": 1}
    components = (
        _component(
            "primary",
            "primary_region",
            PixelBox(geometry_offset, 0, 20, 20),
            first_fields,
        ),
        _component(
            "secondary",
            "secondary_region",
            PixelBox(40 + geometry_offset, 0, 20, 20),
            second_fields,
        ),
    )
    normalization_policy = NormalizationPolicy(
        "normalization_policy",
        "1.0.0",
        "exact_ratio_v1",
        (category_id,),
        SyntaxOntology(
            "syntax_ontology",
            "1.0.0",
            (
                OntologyTerm("primary_region", (category_id,)),
                OntologyTerm("secondary_region", (category_id,)),
            ),
        ),
    )
    specimen = SpecimenEvidence(
        specimen_id=f"specimen_{index}",
        source=SourceReference(
            source_id or f"source_{index}",
            "1.0.0",
            source_content_sha256 or f"{index + 1:x}" * 64,
            "repository_fixture_authority",
            True,
        ),
        category_id=category_id,
        canvas_width_px=100,
        canvas_height_px=100,
        governed_status=GovernedStatus.GOVERNED_SYNTHETIC,
        origin=EvidenceOrigin.DETERMINISTIC_CODE,
        provenance=(provenance(f"source_lock_{index}", "c"),),
        components=components,
    )
    normalized = normalize_evidence(
        run_id=f"normalize_{index}",
        specimens=(specimen,),
        policy=normalization_policy,
    ).specimens[0]
    observations = {
        item.component_id: item.observation_id for item in normalized.observations
    }
    relation = RelationEvidence.create(
        relation=relation_name,
        from_observation_id=observations["primary"],
        to_observation_id=observations["secondary"],
        evidence_observation_ids=(
            observations["primary"],
            observations["secondary"],
        ),
        observation_status=ObservationStatus.DETERMINISTICALLY_DERIVED,
        knowledge_status=KnowledgeStatus.DETERMINISTIC_DERIVATION,
        origin=EvidenceOrigin.DETERMINISTIC_CODE,
        provenance=(provenance("relationship_parser", "d"),),
        uncertainty=Uncertainty(
            UncertaintyKind.EXACT, 1_000_000, "deterministic graph relation"
        ),
        applicability=Applicability(
            ApplicabilityStatus.APPLICABLE, "declared substrate relation"
        ),
    )
    result = compile_substrate_graphs(
        run_id=f"graph_{index}",
        specimen=normalized,
        plan=SubstrateGraphPlan(
            plan_id=f"plan_{index}",
            version="1.0.0",
            substrate=substrate,
            authority_ref="offline_graph_authority",
            relations=(relation,),
        ),
    )
    return next(graph for graph in result.graphs if graph.graph_kind is graph_kind)


def supported_graphs(**kwargs) -> tuple[SubstrateGraph, SubstrateGraph]:
    return graph_fixture(0, **kwargs), graph_fixture(1, **kwargs)


def provisional_hypothesis(
    graphs: tuple[SubstrateGraph, ...],
    *,
    statement: str = "The supported ordering may focus attention before the secondary region.",
    proposer: str = PROPOSER,
) -> ProvisionalMeaningHypothesis:
    edges = tuple(edge for graph in graphs for edge in graph.edges)
    return ProvisionalMeaningHypothesis.create(
        scope=HypothesisScope.ACTIVATIVE_ROLE,
        statement=statement,
        proposer_authority_ref=proposer,
        source_graph_ids=tuple(graph.graph_id for graph in graphs),
        source_edge_ids=tuple(edge.edge_id for edge in edges),
        source_observation_ids=tuple(
            observation_id
            for edge in edges
            for observation_id in edge.evidence_observation_ids
        ),
        alternatives=(
            "The ordering may be compositional without an Activative effect.",
        ),
        provenance=(provenance("hypothesis_capsule", "e"),),
        uncertainty=Uncertainty(
            UncertaintyKind.BOUNDED_MEASUREMENT,
            500_000,
            "meaning has not been ratified",
        ),
    )
