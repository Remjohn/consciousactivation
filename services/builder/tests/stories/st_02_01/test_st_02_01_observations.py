from __future__ import annotations

from cmf_builder.visual.geometry import PixelBox
from cmf_builder.visual.normalization import (
    ComponentEvidence,
    DuplicateKind,
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


HASH_A = "a" * 64
HASH_B = "b" * 64
HASH_C = "c" * 64
HASH_D = "d" * 64
CATEGORY = "short_form_edited_video"


def policy() -> NormalizationPolicy:
    return NormalizationPolicy(
        policy_id="syntax_observation_policy",
        version="1.0.0",
        normalization_version="exact_ratio_v1",
        allowed_categories=(CATEGORY, "format_02_animation"),
        ontology=SyntaxOntology(
            ontology_id="builder_visual_syntax",
            version="1.0.0",
            terms=(
                OntologyTerm("headline_region", (CATEGORY,)),
                OntologyTerm("subject_region", (CATEGORY, "format_02_animation")),
            ),
        ),
    )


def provenance(
    artifact_id: str = "source_lock_v1", digest: str = HASH_C
) -> ProvenanceReference:
    return ProvenanceReference(
        artifact_id=artifact_id,
        artifact_sha256=digest,
        relationship="derived_from",
    )


def component(
    component_id: str = "component_headline",
    *,
    term_id: str = "headline_region",
    box: PixelBox | None = None,
    fields: dict[str, str | int | bool] | None = None,
    observation_status: ObservationStatus = ObservationStatus.MEASURED,
    knowledge_status: KnowledgeStatus = KnowledgeStatus.OBSERVATION,
    component_provenance: tuple[ProvenanceReference, ...] | None = None,
) -> ComponentEvidence:
    return ComponentEvidence.create(
        component_id=component_id,
        ontology_term_id=term_id,
        pixel_box=box or PixelBox(x=100, y=50, width=400, height=100),
        observation_status=observation_status,
        knowledge_status=knowledge_status,
        provenance=component_provenance or (provenance("parser_v1", HASH_D),),
        uncertainty=Uncertainty(
            kind=UncertaintyKind.EXACT,
            confidence_ppm=1_000_000,
            rationale="deterministic fixture coordinates",
        ),
        applicability=Applicability(
            status=ApplicabilityStatus.APPLICABLE,
            rationale="the governed category defines this region",
        ),
        structural_fields=fields or {"frame_index": 0, "start_ms": 0},
    )


def specimen(
    specimen_id: str = "specimen_alpha",
    *,
    digest: str = HASH_A,
    components: tuple[ComponentEvidence, ...] | None = None,
) -> SpecimenEvidence:
    return SpecimenEvidence(
        specimen_id=specimen_id,
        source=SourceReference(
            source_id=f"source_{specimen_id}",
            version="1.0.0",
            content_sha256=digest,
            authority_ref="repository_fixture_authority",
            repository_owned=True,
        ),
        category_id=CATEGORY,
        canvas_width_px=1000,
        canvas_height_px=500,
        governed_status=GovernedStatus.GOVERNED_SYNTHETIC,
        origin=EvidenceOrigin.DETERMINISTIC_CODE,
        provenance=(provenance(),),
        components=components or (component(),),
    )


def test_compiles_typed_observation_with_exact_geometry_and_lineage() -> None:
    result = normalize_evidence(
        run_id="run_st_02_01", specimens=(specimen(),), policy=policy()
    )

    observation = result.specimens[0].observations[0]
    assert observation.observation_status is ObservationStatus.MEASURED
    assert observation.governed_status is GovernedStatus.GOVERNED_SYNTHETIC
    assert observation.knowledge_status is KnowledgeStatus.OBSERVATION
    assert observation.source.content_sha256 == HASH_A
    assert [item.artifact_id for item in observation.provenance] == [
        "parser_v1",
        "source_lock_v1",
    ]
    assert observation.uncertainty.kind is UncertaintyKind.EXACT
    assert observation.applicability.status is ApplicabilityStatus.APPLICABLE
    assert observation.geometry.x.as_dict() == {"numerator": 1, "denominator": 10}
    assert observation.geometry.y.as_dict() == {"numerator": 1, "denominator": 10}
    assert observation.geometry.width.as_dict() == {"numerator": 2, "denominator": 5}
    assert observation.geometry.height.as_dict() == {"numerator": 1, "denominator": 5}
    assert observation.geometry.source_width_px == 1000
    assert observation.geometry.source_height_px == 500


def test_receipt_reports_offline_evidence_pending_without_certification() -> None:
    result = normalize_evidence(
        run_id="run_receipt", specimens=(specimen(),), policy=policy()
    )

    assert result.receipt.story_id == "ST-02.01"
    assert result.receipt.development_mode == "OD_AM_001_OFFLINE_DEVELOPMENT"
    assert result.receipt.event_name == "ST-02.01:OutcomeVerified"
    assert result.receipt.evidence_gate_status == "EVIDENCE_PENDING"
    assert result.receipt.production_ready is False
    assert result.receipt.certified is False
    assert result.receipt.observation_count == 1


def test_exact_source_duplicates_are_recorded_and_suppressed() -> None:
    result = normalize_evidence(
        run_id="run_exact_duplicate",
        specimens=(specimen("specimen_alpha"), specimen("specimen_beta")),
        policy=policy(),
    )

    assert len(result.specimens) == 1
    assert result.receipt.input_specimen_count == 2
    assert result.receipt.accepted_specimen_count == 1
    assert result.receipt.observation_count == 1
    assert result.receipt.exact_duplicate_count == 1
    assert result.duplicates[0].kind is DuplicateKind.EXACT_SOURCE_HASH
    assert result.duplicates[0].contributes_to_support is False


def test_near_duplicate_structures_do_not_inflate_grammar_support() -> None:
    result = normalize_evidence(
        run_id="run_near_duplicate",
        specimens=(
            specimen("specimen_alpha", digest=HASH_A),
            specimen("specimen_beta", digest=HASH_B),
        ),
        policy=policy(),
    )

    assert len(result.specimens) == 2
    assert result.receipt.accepted_specimen_count == 2
    assert result.receipt.near_duplicate_count == 1
    assert result.receipt.grammar_support_count == 1
    assert result.support_specimen_ids == ("specimen_alpha",)
    assert result.duplicates[0].kind is DuplicateKind.NEAR_DUPLICATE_STRUCTURE


def test_distinct_geometry_counts_as_independent_structural_support() -> None:
    result = normalize_evidence(
        run_id="run_independent_support",
        specimens=(
            specimen("specimen_alpha", digest=HASH_A),
            specimen(
                "specimen_beta",
                digest=HASH_B,
                components=(
                    component(box=PixelBox(x=200, y=50, width=400, height=100)),
                ),
            ),
        ),
        policy=policy(),
    )

    assert result.receipt.near_duplicate_count == 0
    assert result.receipt.grammar_support_count == 2


def test_component_order_is_canonical_in_normalized_artifact() -> None:
    components = (
        component("z_subject", term_id="subject_region", fields={"frame_index": 1}),
        component("a_headline"),
    )
    result = normalize_evidence(
        run_id="run_component_order",
        specimens=(specimen(components=components),),
        policy=policy(),
    )

    assert [item.component_id for item in result.specimens[0].observations] == [
        "a_headline",
        "z_subject",
    ]


def test_deterministic_derived_status_remains_distinct_from_measurement() -> None:
    derived = component(
        observation_status=ObservationStatus.DETERMINISTICALLY_DERIVED,
        knowledge_status=KnowledgeStatus.DETERMINISTIC_DERIVATION,
    )
    result = normalize_evidence(
        run_id="run_derived",
        specimens=(specimen(components=(derived,)),),
        policy=policy(),
    )

    observation = result.specimens[0].observations[0]
    assert observation.observation_status is ObservationStatus.DETERMINISTICALLY_DERIVED
    assert observation.knowledge_status is KnowledgeStatus.DETERMINISTIC_DERIVATION


def test_structural_fields_are_canonical_and_not_a_generic_notes_channel() -> None:
    result = normalize_evidence(
        run_id="run_structural_fields",
        specimens=(
            specimen(
                components=(
                    component(fields={"start_ms": 0, "frame_index": 0, "end_ms": 300}),
                )
            ),
        ),
        policy=policy(),
    )

    assert result.specimens[0].observations[0].structural_fields == (
        ("end_ms", 300),
        ("frame_index", 0),
        ("start_ms", 0),
    )

