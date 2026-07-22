from pathlib import Path
from uuid import uuid4

import pytest
from pydantic import ValidationError

from ccp_studio.contracts.asset_program_compilers import PrimitiveTriadContract
from ccp_studio.contracts.creative_ingredients import CompositionRole, SourceReference, SourceReferenceKind
from ccp_studio.contracts.frame_profiles import DEFAULT_FRAME_PROFILES, FrameDeliveryMode, FrameProfile, FrameProfileCode
from ccp_studio.contracts.ontology import CanonicalContractPath, MigrationAction, OntologyLayer, OntologyTerm, OntologyTermType
from ccp_studio.contracts.primitive_coalition import PrimitiveCoalitionContract
from ccp_studio.contracts.style_routes import DEFAULT_STYLE_ROUTES, SourceReferenceMode, StyleFamily, StyleRoute
from ccp_studio.services.contract_convergence_service import (
    CANONICAL_CONTRACT_PATHS,
    ContractConvergenceService,
    ContractConvergenceServiceError,
)
from ccp_studio.services.registry_consolidation_service import RegistryConsolidationService


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_ontology_term_schema_supports_all_required_layers():
    required_layers = {
        "doctrine",
        "brand_workspace",
        "primitive_system",
        "reasoning_methodology",
        "research",
        "interview_intelligence",
        "content_strategy",
        "sequencing",
        "creative_ingredients",
        "asset_intelligence",
        "visual_style_motion",
        "visual_preproduction",
        "composition",
        "component_engines",
        "providers_tools",
        "render_timeline",
        "evaluation_review",
        "publishing_memory",
    }
    assert required_layers.issubset({layer.value for layer in OntologyLayer})
    term = OntologyTerm(
        term_id="ontology.term.test",
        canonical_name="Test Ontology Term",
        term_type=OntologyTermType.contract,
        layer=OntologyLayer.visual_preproduction,
        definition="A source-backed test term for ontology schema coverage.",
        source_of_truth="tests/cmf_studio/test_contract_convergence_registry_consolidation.py",
        owner_component="ontology",
        status="canonical",
        migration_action=MigrationAction.keep,
    )
    assert term.layer == OntologyLayer.visual_preproduction


def test_primitive_coalition_contract_requires_primary_binding():
    with pytest.raises(ValidationError):
        PrimitiveCoalitionContract(
            coalition_intent="Invalid empty coalition.",
            primary_bindings=[],
            coalition_signature="invalid",
            content_hash="not-valid",
        )


def test_primitive_triad_projection_creates_valid_coalition_if_existing_triad_available():
    triads = [
        PrimitiveTriadContract(
            primitive_id="PRM-meaning-transform",
            canonical_name="Meaning Transform",
            role="meaning_transform",
            evidence_ref="legacy:triad",
        ),
        PrimitiveTriadContract(
            primitive_id="PRM-delivery-shape",
            canonical_name="Delivery Shape",
            role="delivery_shape",
            evidence_ref="legacy:triad",
        ),
        PrimitiveTriadContract(
            primitive_id="PRM-format-material",
            canonical_name="Format Material",
            role="format_material",
            evidence_ref="legacy:triad",
        ),
    ]
    coalition = ContractConvergenceService().project_primitive_triad_to_coalition(
        primitive_triads=triads,
        coalition_intent="Project an existing PrimitiveTriadContract into PrimitiveCoalitionContract.",
        source_context_refs={"legacy_contract": "PrimitiveTriadContract"},
    )
    assert isinstance(coalition, PrimitiveCoalitionContract)
    assert coalition.coalition_signature.startswith("legacy:")
    assert len(coalition.primary_bindings) == 3


def test_16_9_is_source_only_and_rejected_as_short_form_delivery():
    profiles = {profile.code: profile for profile in DEFAULT_FRAME_PROFILES}
    source_profile = profiles[FrameProfileCode.source_interview_16_9]
    assert source_profile.delivery_mode == FrameDeliveryMode.source_only
    with pytest.raises(ContractConvergenceServiceError):
        ContractConvergenceService().validate_frame_profile_for_short_form(source_profile)
    with pytest.raises(ValidationError):
        FrameProfile(
            code=FrameProfileCode.source_interview_16_9,
            display_name="Invalid 16:9 Delivery",
            delivery_mode=FrameDeliveryMode.delivery,
            width=1920,
            height=1080,
            caption_policy={"placement": "none", "max_lines": 0},
        )


def test_1_1_soft_rounded_editorial_is_valid_delivery_frame():
    profile = ContractConvergenceService().validate_frame_profile_for_short_form(FrameProfileCode.square_soft_rounded_editorial)
    assert profile.delivery_mode == FrameDeliveryMode.delivery
    assert profile.inner_frame is not None
    assert profile.inner_frame.corner_radius > 0


def test_style_routes_include_cac_and_gmg_experts():
    route_codes = {route.route_code for route in DEFAULT_STYLE_ROUTES}
    assert {
        "CAC_CONSCIOUS_AMBIENT_CINEMA",
        "GMG_EXPERT_01_NEO_SCHEMATIC_ARCHITECT",
        "GMG_EXPERT_02_MONO_KINETIC_PROTAGONIST",
        "GMG_EXPERT_03_EMOTIONAL_ANIMATOR",
        "GMG_EXPERT_04_PAPER_ARCHITECT",
        "GMG_EXPERT_05_EDITORIAL_SCRIBE",
        "GMG_EXPERT_06_VISUAL_SYNTHESIZER",
    }.issubset(route_codes)


def test_cac_route_requires_real_life_reference():
    cac = next(route for route in DEFAULT_STYLE_ROUTES if route.route_code == "CAC_CONSCIOUS_AMBIENT_CINEMA")
    assert cac.requires_real_reference is True
    assert "real_life_reference" in cac.required_inputs
    with pytest.raises(ValidationError):
        StyleRoute(
            route_code="CAC_CONSCIOUS_AMBIENT_CINEMA",
            family=StyleFamily.cac,
            display_name="Invalid CAC",
            purpose="Invalid route with no real reference.",
            requires_real_reference=False,
            allowed_reference_modes=[SourceReferenceMode.source_language_reference],
        )


def test_gmg_expert_03_requires_photo_cutout_object():
    route = next(route for route in DEFAULT_STYLE_ROUTES if route.route_code == "GMG_EXPERT_03_EMOTIONAL_ANIMATOR")
    assert "photo_cutout_object" in route.required_inputs
    with pytest.raises(ValidationError):
        StyleRoute(
            route_code="GMG_EXPERT_03_EMOTIONAL_ANIMATOR",
            family=StyleFamily.gmg,
            display_name="Invalid GMG 03",
            purpose="Missing required photo cutout object.",
            requires_real_reference=True,
            allowed_reference_modes=[SourceReferenceMode.direct_real_reference],
            required_inputs=["beat_cluster", "visual_schema"],
        )


def test_provider_job_preconditions_require_source_reference_style_route_frame_profile_composition_role():
    service = ContractConvergenceService()
    source = SourceReference(
        kind=SourceReferenceKind.client_upload,
        source_ref="s3://brand/proof.png",
        rights_status="client_owned",
        description="Client-owned source reference.",
    )
    route = next(route for route in DEFAULT_STYLE_ROUTES if route.route_code == "DOCUMENTARY_PROOF")
    common = {
        "source_reference": source,
        "style_route": route,
        "frame_profile": FrameProfileCode.square_proof_card,
        "composition_role": CompositionRole.proof_insert,
        "evaluation_requirements": {"source_match": 0.9},
        "primitive_coalition_contract_id": "primitive-coalition-001",
        "source_reference_mode": SourceReferenceMode.direct_real_reference,
    }
    assert service.validate_provider_job_preconditions(**common).style_route.route_code == "DOCUMENTARY_PROOF"
    for missing_key in ("source_reference", "style_route", "frame_profile", "composition_role"):
        payload = dict(common)
        payload[missing_key] = None
        with pytest.raises(ContractConvergenceServiceError):
            service.validate_provider_job_preconditions(**payload)


def test_registry_crosswalk_resolves_legacy_to_canonical_namespace():
    service = RegistryConsolidationService.from_project_root(PROJECT_ROOT)
    crosswalk = service.resolve_canonical_registry_entry("registries/primitives/meaning_plane")
    assert crosswalk.canonical_namespace.value == "registry.primitive.meaning"
    assert crosswalk.action == "move"


def test_canonical_contract_paths_are_frozen():
    service = ContractConvergenceService()
    frozen = service.freeze_canonical_contract_paths()
    assert [item.path for item in frozen] == list(CANONICAL_CONTRACT_PATHS)
    assert all(item.frozen and item.migration_adr_required for item in frozen)
    for path in CANONICAL_CONTRACT_PATHS:
        assert Path(PROJECT_ROOT / path).exists()
        assert CanonicalContractPath(path=path, module_name=Path(path).stem).frozen is True
    docs = (PROJECT_ROOT / "docs" / "architecture" / "ontology" / "CANONICAL_CONTRACT_PATHS.md").read_text(encoding="utf-8")
    assert "should not be moved without a migration ADR" in docs or "must not be moved" in docs


def test_registry_consolidation_manifest_loads():
    service = RegistryConsolidationService.from_project_root(PROJECT_ROOT)
    manifest = service.load_consolidation_manifest()
    assert manifest.canonical_entries
    assert manifest.crosswalk
    summary = service.summarize_registry_consolidation_status()
    assert summary["canonical_registry_root"] == "registries/canonical/"
    assert summary["duplicate_entry_count"] == 0
