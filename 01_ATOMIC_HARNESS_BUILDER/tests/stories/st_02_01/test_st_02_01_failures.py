from __future__ import annotations

import pytest

from cmf_builder.visual.geometry import GeometryInvalid, PixelBox
from cmf_builder.visual.normalization import (
    ComponentEvidence,
    DuplicateInflationRejected,
    NormalizationPolicy,
    SpecimenEvidence,
    SpecimenInvalid,
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
    ProviderOnlyClaimRejected,
    ProvenanceReference,
    SourceEvidenceInvalid,
    SourceReference,
    SyntaxOntology,
    Uncertainty,
    UncertaintyKind,
    UnsupportedParserOutput,
)


HASH_A = "a" * 64
HASH_B = "b" * 64
CATEGORY = "short_form_edited_video"


def provenance() -> ProvenanceReference:
    return ProvenanceReference("source_lock_v1", HASH_B, "derived_from")


def policy() -> NormalizationPolicy:
    return NormalizationPolicy(
        policy_id="syntax_observation_policy",
        version="1.0.0",
        normalization_version="exact_ratio_v1",
        allowed_categories=(CATEGORY,),
        ontology=SyntaxOntology(
            "builder_visual_syntax",
            "1.0.0",
            (OntologyTerm("headline_region", (CATEGORY,)),),
        ),
    )


def component(
    *,
    component_id: str = "headline",
    term_id: str = "headline_region",
    fields: dict[str, object] | None = None,
    box: PixelBox | None = None,
    observation_status: ObservationStatus = ObservationStatus.MEASURED,
    knowledge_status: KnowledgeStatus = KnowledgeStatus.OBSERVATION,
    applicability: Applicability | None = None,
    uncertainty: Uncertainty | None = None,
) -> ComponentEvidence:
    return ComponentEvidence.create(
        component_id=component_id,
        ontology_term_id=term_id,
        pixel_box=box or PixelBox(0, 0, 100, 50),
        observation_status=observation_status,
        knowledge_status=knowledge_status,
        provenance=(provenance(),),
        uncertainty=uncertainty
        or Uncertainty(UncertaintyKind.EXACT, 1_000_000, "exact fixture"),
        applicability=applicability
        or Applicability(ApplicabilityStatus.APPLICABLE, "governed category field"),
        structural_fields=fields or {},  # type: ignore[arg-type]
    )


def specimen(
    *,
    specimen_id: str = "specimen_alpha",
    category_id: str = CATEGORY,
    governed_status: GovernedStatus = GovernedStatus.GOVERNED_SYNTHETIC,
    origin: EvidenceOrigin = EvidenceOrigin.DETERMINISTIC_CODE,
    components: tuple[ComponentEvidence, ...] | None = None,
    source: SourceReference | None = None,
) -> SpecimenEvidence:
    return SpecimenEvidence(
        specimen_id=specimen_id,
        source=source
        or SourceReference(
            "source_fixture",
            "1.0.0",
            HASH_A,
            "repository_fixture_authority",
            True,
        ),
        category_id=category_id,
        canvas_width_px=100,
        canvas_height_px=50,
        governed_status=governed_status,
        origin=origin,
        provenance=(provenance(),),
        components=components or (component(),),
    )


def test_rejects_non_repository_owned_source() -> None:
    with pytest.raises(SourceEvidenceInvalid):
        SourceReference(
            "external_source", "1.0.0", HASH_A, "unknown_authority", False
        )


def test_rejects_unverified_specimen() -> None:
    with pytest.raises(SourceEvidenceInvalid):
        specimen(governed_status=GovernedStatus.UNVERIFIED)


def test_rejects_provider_only_claims() -> None:
    with pytest.raises(ProviderOnlyClaimRejected):
        specimen(origin=EvidenceOrigin.PROVIDER_ONLY)


@pytest.mark.parametrize(
    "field",
    [
        "meaning",
        "intent",
        "desired_reaction",
        "identity_dna",
        "reaction_receipt",
        "production_ready",
    ],
)
def test_rejects_semantic_or_authority_contamination(field: str) -> None:
    with pytest.raises(ObservationContaminated):
        component(fields={field: "unsupported claim"})


def test_rejects_unknown_parser_field() -> None:
    with pytest.raises(UnsupportedParserOutput):
        component(fields={"generic_notes": "not a typed structural field"})


def test_rejects_hypothesis_promoted_to_observation() -> None:
    with pytest.raises(ObservationContaminated):
        component(knowledge_status=KnowledgeStatus.HYPOTHESIS)


def test_rejects_mismatched_observation_and_knowledge_status() -> None:
    with pytest.raises(ObservationContaminated):
        component(
            observation_status=ObservationStatus.MEASURED,
            knowledge_status=KnowledgeStatus.DETERMINISTIC_DERIVATION,
        )


def test_rejects_unknown_ontology_term() -> None:
    with pytest.raises(UnsupportedParserOutput):
        normalize_evidence(
            run_id="unknown_term",
            specimens=(specimen(components=(component(term_id="invented_region"),)),),
            policy=policy(),
        )


def test_rejects_category_outside_policy() -> None:
    with pytest.raises(SpecimenInvalid):
        normalize_evidence(
            run_id="unsupported_category",
            specimens=(specimen(category_id="conversational_activation"),),
            policy=policy(),
        )


def test_rejects_geometry_outside_governed_canvas() -> None:
    with pytest.raises(GeometryInvalid):
        normalize_evidence(
            run_id="invalid_geometry",
            specimens=(specimen(components=(component(box=PixelBox(90, 0, 20, 10)),)),),
            policy=policy(),
        )


def test_rejects_duplicate_component_identity() -> None:
    repeated = component()
    with pytest.raises(DuplicateInflationRejected):
        specimen(components=(repeated, repeated))


def test_rejects_duplicate_specimen_identity() -> None:
    repeated = specimen()
    with pytest.raises(DuplicateInflationRejected):
        normalize_evidence(
            run_id="duplicate_specimen_id",
            specimens=(repeated, repeated),
            policy=policy(),
        )


def test_rejects_empty_normalization_input() -> None:
    with pytest.raises(SpecimenInvalid):
        normalize_evidence(run_id="empty_input", specimens=(), policy=policy())


def test_exact_source_duplicate_cannot_hide_invalid_ontology() -> None:
    valid = specimen(specimen_id="a_valid")
    invalid = specimen(
        specimen_id="z_invalid",
        components=(component(term_id="unknown_region"),),
    )
    with pytest.raises(UnsupportedParserOutput):
        normalize_evidence(
            run_id="duplicate_bypass_rejected",
            specimens=(valid, invalid),
            policy=policy(),
        )


def test_not_applicable_requires_explicit_matching_statuses() -> None:
    with pytest.raises(SpecimenInvalid):
        component(
            applicability=Applicability(
                ApplicabilityStatus.NOT_APPLICABLE, "not used by this structural profile"
            )
        )

