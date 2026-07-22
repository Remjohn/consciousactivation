import pytest

from ccp_studio.contracts.composition_intelligence import (
    AudienceProxyPersona,
    AudienceProxyPlacementPlan,
    AvatarPlacementPlan,
    CognitiveLoadBudget,
    CompositionIntelligenceContext,
    CompositionRole,
    LockedCompositionElements,
    PassStatus,
    ProviderEditBoundary,
    ProviderName,
    ProviderRole,
    RealLifeCutoutPlacementPlan,
    ReferenceEditContract,
    TextPlacementPlan,
)
from ccp_studio.contracts.format02_composition_intelligence import (
    Format02ConceptMotionBudget,
    Format02ConceptUnit,
    Format02SceneRole,
    Format02VisualAction,
    Format02VisualActionType,
)
from ccp_studio.contracts.format_intelligence import FormatId, GenericExtractionPacketRef
from ccp_studio.services.cognitive_load_gate_service import CognitiveLoadGateService
from ccp_studio.services.composition_commander_service import CompositionCommanderService
from ccp_studio.services.format02_format_program_to_composition_adapter_service import (
    Format02FormatProgramToCompositionAdapterService,
)
from ccp_studio.services.format02_composition_service import Format02CompositionService
from ccp_studio.services.format_intelligence_service import FormatIntelligenceService
from ccp_studio.services.provider_composition_plate_service import ProviderCompositionPlateService
from ccp_studio.services.reference_edit_contract_service import ReferenceEditContractService


def test_composition_context_requires_brand_context_version():
    with pytest.raises(Exception):
        CompositionIntelligenceContext(
            brand_id="brand_1",
            brand_context_version_id="",
            format_id="format_02_avatar_papercut_explainer",
            source_span_refs=["span_1"],
        )


def test_composition_context_requires_source_span_refs():
    with pytest.raises(Exception):
        CompositionIntelligenceContext(
            brand_id="brand_1",
            brand_context_version_id="bcv_1",
            format_id="format_02_avatar_papercut_explainer",
            source_span_refs=[],
        )


def test_text_placement_blocks_too_many_visible_words():
    with pytest.raises(Exception):
        TextPlacementPlan(
            headline_text="This scene has too many visible words for a clean animated explainer frame",
            support_labels=["extra label"],
            max_visible_words=8,
        )


def test_avatar_action_must_serve_concept():
    with pytest.raises(Exception):
        AvatarPlacementPlan(
            avatar_ref="coach_avatar",
            placement="right",
            action_ref="wave",
            action_serves_concept=False,
        )


def test_audience_proxy_requires_sfl_function():
    with pytest.raises(Exception):
        AudienceProxyPlacementPlan(
            persona=AudienceProxyPersona.CONFUSED_SEEKER,
            placement="lower_left",
            sfl_function="",
        )


def test_real_life_cutout_requires_role_and_source_ref():
    with pytest.raises(Exception):
        RealLifeCutoutPlacementPlan(
            asset_id="cup",
            source_ref="",
            role=CompositionRole.HERO_OBJECT,
            placement="left",
        )


def test_real_life_cutout_cannot_be_background_only():
    with pytest.raises(Exception):
        RealLifeCutoutPlacementPlan(
            asset_id="cup",
            source_ref="ref_1",
            role=CompositionRole.BACKGROUND,
            placement="left",
        )


def test_provider_edit_boundary_rejects_rewrite_text_allowed():
    with pytest.raises(Exception):
        ProviderEditBoundary(
            provider_name=ProviderName.FLUX,
            provider_role=ProviderRole.REFERENCE_BASED_OBJECT_EDITOR,
            allowed_edits=["rewrite_text"],
            forbidden_edits=[],
        )


def test_reference_edit_contract_requires_forbidden_drift_rules():
    cutout = RealLifeCutoutPlacementPlan(
        asset_id="cup",
        source_ref="ref_1",
        role=CompositionRole.HERO_OBJECT,
        placement="left",
    )
    locked = LockedCompositionElements(locked_text=["headline"], locked_layout_refs=["layout"], locked_avatar_refs=["avatar"])
    weak_boundary = ProviderEditBoundary(
        provider_name=ProviderName.FLUX,
        provider_role=ProviderRole.REFERENCE_BASED_OBJECT_EDITOR,
        allowed_edits=["paperize_reference"],
        forbidden_edits=["rewrite_text"],
    )
    with pytest.raises(Exception):
        ReferenceEditContract(
            composition_plate_ref="plate_1",
            reference_inputs=[cutout],
            locked_elements=locked,
            edit_boundary=weak_boundary,
        )


def test_cognitive_load_gate_blocks_overload():
    budget = CognitiveLoadBudget()
    report = CognitiveLoadGateService().evaluate(
        budget,
        visible_words=22,
        headline_words=9,
        support_labels=5,
        audience_proxies=2,
        hero_real_life_objects=2,
        support_real_life_objects=3,
        diagram_nodes=5,
        simultaneous_motion_events=4,
        negative_space_ratio=0.10,
    )
    assert report.pass_status == PassStatus.FAIL
    assert "visible_words_exceed_budget" in report.blockers
    assert "negative_space_below_minimum" in report.blockers


def test_format02_concept_unit_requires_one_concept():
    with pytest.raises(Exception):
        Format02ConceptUnit(
            concept_statement="Natural means from nature",
            source_span_refs=["span_1"],
            one_concept_only=False,
        )


def test_format02_visual_action_requires_sfl_and_primitive():
    with pytest.raises(Exception):
        Format02VisualAction(
            action_type=Format02VisualActionType.CARD_SLIDE_IN,
            concept_unit_id="concept_1",
            sfl_function="",
            primitive_function="clarity",
        )


def test_format02_motion_budget_allows_one_primary_action_only():
    with pytest.raises(Exception):
        Format02ConceptMotionBudget(
            concept_unit_id="concept_1",
            primary_visual_actions=["a1", "a2"],
        )


def test_format02_service_compiles_clean_scene_program():
    scene = Format02CompositionService().compile_scene_program(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        source_span_refs=["span_1"],
        scene_id="scene_1",
        scene_role=Format02SceneRole.MYTH_SETUP,
        concept_statement="Natural does not always mean safe.",
        headline_text="Natural ≠ always safe?",
        hero_object_asset_id="tea_cup_001",
        hero_object_source_ref="visual_ref_tea_001",
    )
    assert scene.concept_unit.one_concept_only
    assert scene.composition_scene_program is not None
    assert scene.composition_scene_program.text_placement_plan.headline_text == "Natural ≠ always safe?"
    assert scene.composition_scene_program.avatar_placement_plan is not None


def test_format02_service_scene_can_pass_cognitive_load_and_lock():
    service = Format02CompositionService()
    scene = service.compile_scene_program(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        source_span_refs=["span_1"],
        scene_id="scene_2",
        scene_role=Format02SceneRole.TRUTH_DEFINE,
        concept_statement="Natural only means from nature.",
        headline_text="Natural = from nature.",
    )
    core_scene = scene.composition_scene_program
    receipt, report = service.core.compile_decision_receipt(
        core_scene,
        visible_words=4,
        headline_words=4,
        support_labels=0,
        audience_proxies=1,
        hero_real_life_objects=1,
        support_real_life_objects=0,
        diagram_nodes=0,
        simultaneous_motion_events=1,
        negative_space_ratio=0.35,
    )
    assert report.pass_status == PassStatus.PASS
    assert receipt.locked
    verdict = CompositionCommanderService().authorize(core_scene, receipt)
    assert verdict.authorized


def test_composition_commander_blocks_unlocked_or_failed_scene():
    scene = Format02CompositionService().compile_scene_program(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        source_span_refs=["span_1"],
        scene_id="scene_3",
        scene_role=Format02SceneRole.PROOF_CONTRAST,
        concept_statement="Nature includes risks.",
        headline_text="Nature includes risks.",
    )
    receipt, report = scene.composition_scene_program, None
    decision, _ = Format02CompositionService().core.compile_decision_receipt(
        scene.composition_scene_program,
        visible_words=30,
        headline_words=10,
        support_labels=5,
        audience_proxies=3,
        hero_real_life_objects=2,
        support_real_life_objects=3,
        diagram_nodes=6,
        simultaneous_motion_events=4,
        negative_space_ratio=0.10,
    )
    verdict = CompositionCommanderService().authorize(scene.composition_scene_program, decision)
    assert not verdict.authorized
    assert verdict.blockers


def test_provider_plate_contract_uses_ideogram_role():
    scene = Format02CompositionService().compile_scene_program(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        source_span_refs=["span_1"],
        scene_id="scene_4",
        scene_role=Format02SceneRole.BETTER_FRAME,
        concept_statement="Ask better questions.",
        headline_text="Ask better questions.",
    )
    locked = LockedCompositionElements(locked_text=["headline"], locked_layout_refs=["layout"], locked_avatar_refs=["avatar"])
    contract = ProviderCompositionPlateService().compile_ideogram_plate_contract(
        composition_scene_program_id=scene.composition_scene_program.composition_scene_program_id,
        locked_elements=locked,
        placeholder_object_slots=["hero_object"],
    )
    assert contract.provider_name == ProviderName.IDEOGRAM
    assert contract.provider_role == ProviderRole.COMPOSITION_PLATE_GENERATOR


def test_reference_edit_contract_uses_flux_and_reference_inputs():
    cutout = RealLifeCutoutPlacementPlan(
        asset_id="compass_001",
        source_ref="visual_ref_compass",
        role=CompositionRole.HERO_OBJECT,
        placement="center",
    )
    locked = LockedCompositionElements(locked_text=["headline"], locked_layout_refs=["layout"], locked_avatar_refs=["avatar"])
    contract = ReferenceEditContractService().compile_flux_reference_edit_contract(
        composition_plate_ref="plate_1",
        reference_inputs=[cutout],
        locked_elements=locked,
    )
    assert contract.provider_name == ProviderName.FLUX
    assert "rewrite_text" in contract.edit_boundary.forbidden_edits
    assert "change_layout" in contract.edit_boundary.forbidden_edits


def test_format02_format_program_adapter_compiles_scene_program():
    format_service = FormatIntelligenceService()
    context = format_service.hydrate_context(brand_id="brand_1", brand_context_version_id="bcv_1")
    packet = GenericExtractionPacketRef(
        extraction_packet_id="format02_packet_1",
        target_format=FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER,
        source_span_refs=["span_1"],
        payload={
            "teachable_mechanism": "capacity_without_recovery",
            "concept_nodes": ["Recovery margin protects capacity"],
            "diagram_sequence": "margin_diagram_ref",
        },
    )
    program = format_service.compile_format_program(context, packet)
    scene = Format02FormatProgramToCompositionAdapterService().compile_scene_program(
        program,
        scene_id="scene_from_format02_program",
    )

    assert scene.composition_scene_program.scene_id == "scene_from_format02_program"
    assert scene.concept_unit.source_span_refs == ["span_1"]
    assert scene.composition_scene_program.text_placement_plan.headline_text == "Recovery margin protects capacity"
    assert scene.composition_scene_program.real_life_cutout_plans[0].source_ref == "span_1"
