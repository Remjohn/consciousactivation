from __future__ import annotations

from cmf_builder.visual.geometry import PixelBox, normalize_box
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


CATEGORY = "short_form_edited_video"


def make_policy() -> NormalizationPolicy:
    return NormalizationPolicy(
        "syntax_policy",
        "1.0.0",
        "exact_ratio_v1",
        (CATEGORY,),
        SyntaxOntology(
            "visual_syntax",
            "1.0.0",
            (
                OntologyTerm("subject_region", (CATEGORY,)),
                OntologyTerm("headline_region", (CATEGORY,)),
            ),
        ),
    )


def prov(name: str, character: str) -> ProvenanceReference:
    return ProvenanceReference(name, character * 64, "derived_from")


def make_component(
    component_id: str,
    term_id: str,
    x: int,
    provenance: tuple[ProvenanceReference, ...],
) -> ComponentEvidence:
    return ComponentEvidence.create(
        component_id=component_id,
        ontology_term_id=term_id,
        pixel_box=PixelBox(x, 20, 200, 100),
        observation_status=ObservationStatus.MEASURED,
        knowledge_status=KnowledgeStatus.OBSERVATION,
        provenance=provenance,
        uncertainty=Uncertainty(
            UncertaintyKind.EXACT, 1_000_000, "deterministic fixture parser"
        ),
        applicability=Applicability(
            ApplicabilityStatus.APPLICABLE, "governed syntax component"
        ),
        structural_fields={"frame_index": 0},
    )


def make_specimen(
    specimen_id: str,
    digest_character: str,
    *,
    component_order: tuple[str, ...] = ("subject", "headline"),
    provenance_order: tuple[str, ...] = ("b", "a"),
) -> SpecimenEvidence:
    component_map = {
        "subject": make_component(
            "subject", "subject_region", 100, tuple(prov(name, name) for name in provenance_order)
        ),
        "headline": make_component(
            "headline", "headline_region", 400, (prov("c", "c"),)
        ),
    }
    return SpecimenEvidence(
        specimen_id=specimen_id,
        source=SourceReference(
            f"source_{specimen_id}",
            "1.0.0",
            digest_character * 64,
            "fixture_authority",
            True,
        ),
        category_id=CATEGORY,
        canvas_width_px=1000,
        canvas_height_px=500,
        governed_status=GovernedStatus.GOVERNED_SYNTHETIC,
        origin=EvidenceOrigin.DETERMINISTIC_CODE,
        provenance=(prov("source_lock", "d"),),
        components=tuple(component_map[name] for name in component_order),
    )


def result_bytes(specimens: tuple[SpecimenEvidence, ...]) -> bytes:
    return canonical_json_bytes(
        normalize_evidence(
            run_id="deterministic_run", specimens=specimens, policy=make_policy()
        ).as_dict()
    )


def test_repeated_compilation_is_byte_identical() -> None:
    inputs = (make_specimen("alpha", "e"), make_specimen("beta", "f"))
    assert result_bytes(inputs) == result_bytes(inputs)


def test_specimen_and_component_input_order_do_not_change_identity() -> None:
    alpha_one = make_specimen("alpha", "e", component_order=("subject", "headline"))
    alpha_two = make_specimen("alpha", "e", component_order=("headline", "subject"))
    beta = make_specimen("beta", "f")

    assert result_bytes((alpha_one, beta)) == result_bytes((beta, alpha_two))


def test_provenance_order_does_not_change_observation_identity() -> None:
    first = make_specimen("alpha", "e", provenance_order=("b", "a"))
    second = make_specimen("alpha", "e", provenance_order=("a", "b"))

    assert result_bytes((first,)) == result_bytes((second,))


def test_changed_source_bytes_produce_new_result_and_receipt_identities() -> None:
    first = normalize_evidence(
        run_id="deterministic_run",
        specimens=(make_specimen("alpha", "e"),),
        policy=make_policy(),
    )
    second = normalize_evidence(
        run_id="deterministic_run",
        specimens=(make_specimen("alpha", "f"),),
        policy=make_policy(),
    )

    assert first.result_sha256 != second.result_sha256
    assert first.receipt.receipt_id != second.receipt.receipt_id
    assert first.receipt.receipt_sha256 != second.receipt.receipt_sha256


def test_exact_ratio_serialization_uses_no_floating_point_values() -> None:
    box = normalize_box(PixelBox(1, 1, 1, 1), canvas_width=3, canvas_height=7)

    assert box.x.as_dict() == {"numerator": 1, "denominator": 3}
    assert box.y.as_dict() == {"numerator": 1, "denominator": 7}
    assert b"." not in canonical_json_bytes(box.as_dict())


def test_policy_identity_is_independent_of_declared_category_order() -> None:
    ontology = SyntaxOntology(
        "ontology",
        "1.0.0",
        (OntologyTerm("region", ("category_b", "category_a")),),
    )
    first = NormalizationPolicy(
        "policy", "1.0.0", "normalization_v1", ("category_b", "category_a"), ontology
    )
    second = NormalizationPolicy(
        "policy", "1.0.0", "normalization_v1", ("category_a", "category_b"), ontology
    )

    assert first.policy_sha256 == second.policy_sha256

