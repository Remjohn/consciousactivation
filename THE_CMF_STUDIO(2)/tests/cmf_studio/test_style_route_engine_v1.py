import pytest

from ccp_studio.contracts.style_route_runtime import (
    CACProductionSpec,
    CompositionRole,
    GMGVerbatimNounMap,
    PaperCutArtifactSpec,
    PaperCutEditorialSpec,
    PassStatus,
    ProviderCapability,
    ProviderJobBlueprint,
    RequestingComponent,
    SourceGroundingMode,
    SourceReference,
    StyleRouteDecisionRequest,
    StyleRouteEvaluationReceipt,
    StyleRouteId,
    TargetOutputType,
)
from ccp_studio.services.style_route_engine_service import StyleRouteEngineService


def test_style_route_decision_requires_brand_context_version():
    with pytest.raises(Exception):
        StyleRouteDecisionRequest(
            brand_id="brand_1",
            brand_context_version_id="",
            requesting_component=RequestingComponent.SUPERVISUAL,
            frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
            composition_role=CompositionRole.HERO_VISUAL,
            target_output_type=TargetOutputType.STILL_IMAGE,
            source_grounding_mode=SourceGroundingMode.DIRECT_REAL_REFERENCE,
        )


def test_one_provider_job_cannot_average_multiple_primary_routes():
    with pytest.raises(Exception):
        ProviderJobBlueprint(
            route_production_spec_id="route_spec_1",
            primary_style_route_id=StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA,
            secondary_style_route_ids=[StyleRouteId.GMG_EXPERT_06_VISUAL_SYNTHESIZER],
            recommended_provider_capability=ProviderCapability.FAKE_PROVIDER,
            source_references=["source_1"],
            frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
            composition_role=CompositionRole.HERO_VISUAL,
            prompt_contract="test prompt",
            idempotency_key_seed="seed",
        )


def test_cac_requires_real_life_source_reference():
    service = StyleRouteEngineService()
    request = service.create_decision_request(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        requesting_component=RequestingComponent.SUPERVISUAL,
        frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
        composition_role=CompositionRole.HERO_VISUAL,
        target_output_type=TargetOutputType.STILL_IMAGE,
        source_grounding_mode=SourceGroundingMode.DIRECT_REAL_REFERENCE,
        source_references=[],
        operator_route_hint=StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA,
    )
    report = service.validate_route_preconditions(request, StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA)
    assert "real_life_source_reference" in report.missing_inputs
    assert not report.provider_ready


def test_cac_rejects_abstract_symbolic_exception_without_real_reference():
    service = StyleRouteEngineService()
    request = service.create_decision_request(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        requesting_component=RequestingComponent.SUPERVISUAL,
        frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
        composition_role=CompositionRole.HERO_VISUAL,
        target_output_type=TargetOutputType.STILL_IMAGE,
        source_grounding_mode=SourceGroundingMode.ABSTRACT_SYMBOLIC_EXCEPTION,
        operator_route_hint=StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA,
    )
    report = service.validate_route_preconditions(request, StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA)
    assert "cac_requires_direct_or_composite_real_reference" in report.violations


def test_cac_spec_requires_anchor_contact_composition_atmosphere_imperfection_lens():
    with pytest.raises(Exception):
        CACProductionSpec(
            source_packet_id="source_packet_1",
            source_grounding_mode=SourceGroundingMode.DIRECT_REAL_REFERENCE,
            real_reference_refs=["real_ref_1"],
            mundane_anchor="",
            contact_point="hand touches notebook",
            composition_logic="desk composition",
            atmosphere="quiet",
            imperfection_cues=["coffee stain"],
            lens_language="natural lens",
            camera_distance="close",
            lighting_motivation="window",
            human_scale_space="desk",
        )


def test_gmg_expert_router_selects_one_expert():
    service = StyleRouteEngineService()
    selection = service.route_gmg_expert(source_terms=["system", "signal", "flow"], intent="explain how three systems connect")
    assert selection.selected_expert_route_id == StyleRouteId.GMG_EXPERT_01_NEO_SCHEMATIC_ARCHITECT


def test_gmg_verbatim_noun_map_uses_source_terms():
    noun_map = GMGVerbatimNounMap(source_terms=["system", "signal"], approved_nouns=["system"], rejected_nouns=["dragon"])
    assert noun_map.approved_nouns == ["system"]
    with pytest.raises(Exception):
        GMGVerbatimNounMap(source_terms=["system", "signal"], approved_nouns=["dragon"])


def test_gmg_expert_03_requires_photo_cutout_object():
    service = StyleRouteEngineService()
    request = service.create_decision_request(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        requesting_component=RequestingComponent.VIDEO,
        frame_profile="9:16_FULL_VERTICAL",
        composition_role=CompositionRole.FOREGROUND_INSERT,
        target_output_type=TargetOutputType.MOTION_INSERT,
        source_grounding_mode=SourceGroundingMode.SOURCE_LANGUAGE_REFERENCE,
        operator_route_hint=StyleRouteId.GMG_EXPERT_03_EMOTIONAL_ANIMATOR,
        asset_candidate_refs=[],
    )
    report = service.validate_route_preconditions(request, StyleRouteId.GMG_EXPERT_03_EMOTIONAL_ANIMATOR)
    assert "photo_cutout_object" in report.missing_inputs


def test_gmg_expert_04_requires_document_or_archive_artifact():
    service = StyleRouteEngineService()
    request = service.create_decision_request(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        requesting_component=RequestingComponent.VIDEO,
        frame_profile="9:16_FULL_VERTICAL",
        composition_role=CompositionRole.FOREGROUND_INSERT,
        target_output_type=TargetOutputType.MOTION_INSERT,
        source_grounding_mode=SourceGroundingMode.DIRECT_REAL_REFERENCE,
        source_references=[SourceReference(source_kind="photo", description="person at desk", is_real_life_reference=True)],
        operator_route_hint=StyleRouteId.GMG_EXPERT_04_PAPER_ARCHITECT,
    )
    report = service.validate_route_preconditions(request, StyleRouteId.GMG_EXPERT_04_PAPER_ARCHITECT)
    assert "document_evidence_archive_input" in report.missing_inputs


def test_gmg_expert_05_rejects_3d_glass_neon():
    service = StyleRouteEngineService()
    receipt = service.evaluate_route_output(route_id=StyleRouteId.GMG_EXPERT_05_EDITORIAL_SCRIBE, forbidden_patterns_detected=["3d", "glass", "neon"])
    assert receipt.pass_status == PassStatus.FAIL


def test_gmg_expert_06_rejects_gold_and_photo_objects():
    service = StyleRouteEngineService()
    receipt = service.evaluate_route_output(route_id=StyleRouteId.GMG_EXPERT_06_VISUAL_SYNTHESIZER, forbidden_patterns_detected=["gold", "photo object"])
    assert receipt.pass_status == PassStatus.FAIL


def test_paper_cut_artifact_requires_source_object():
    with pytest.raises(Exception):
        PaperCutArtifactSpec(
            source_object_refs=[],
            cutout_requirements=["clean cutout"],
            paper_edge_treatment="torn edge",
            shadow_treatment="hard shadow",
            semantic_role="proof object",
            composition_role=CompositionRole.PAPER_CUT_OBJECT,
        )


def test_paper_cut_editorial_requires_layer_hierarchy():
    with pytest.raises(Exception):
        PaperCutEditorialSpec(
            visual_hierarchy=["headline"],
            paper_surface="grain paper",
            layer_system=["background_only"],
            type_label_treatment="label",
            mobile_readability_notes="readable",
            frame_profile="4:5_FEED_POSTER",
        )


def test_route_provider_blueprint_has_source_reference_style_route_frame_profile_composition_role():
    service = StyleRouteEngineService()
    source = SourceReference(source_kind="source_photo", source_id="photo_1", is_real_life_reference=True)
    request = service.create_decision_request(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        requesting_component=RequestingComponent.SUPERVISUAL,
        visual_preproduction_packet_id="vp_packet_1",
        frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
        composition_role=CompositionRole.HERO_VISUAL,
        target_output_type=TargetOutputType.STILL_IMAGE,
        source_grounding_mode=SourceGroundingMode.DIRECT_REAL_REFERENCE,
        source_references=[source],
        operator_route_hint=StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA,
    )
    decision = service.select_style_route(request)
    source_packet = service.compile_source_packet(request)
    cac_spec = service.compile_cac_production_spec(source_packet)
    route_spec = service.compile_route_production_spec(decision=decision, request=request, source_packet=source_packet, route_specific_spec_type="CACProductionSpec", route_specific_spec_id=cac_spec.cac_production_spec_id)
    blueprint = service.compile_provider_job_blueprint(route_spec=route_spec, source_references=[source.source_reference_id])
    assert blueprint.primary_style_route_id == StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA
    assert blueprint.frame_profile == "1:1_SOFT_ROUNDED_EDITORIAL"
    assert blueprint.composition_role == CompositionRole.HERO_VISUAL
    assert blueprint.source_references


def test_route_engine_does_not_execute_provider_job():
    with pytest.raises(Exception):
        ProviderJobBlueprint(
            route_production_spec_id="route_spec_1",
            primary_style_route_id=StyleRouteId.DETERMINISTIC_SKIA_CARD,
            recommended_provider_capability=ProviderCapability.FAKE_PROVIDER,
            source_references=["source_1"],
            frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
            composition_role=CompositionRole.HERO_VISUAL,
            prompt_contract="test",
            idempotency_key_seed="seed",
            execution_state="executed",
        )


def test_16_9_is_source_only_for_short_form_route():
    service = StyleRouteEngineService()
    request = service.create_decision_request(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        requesting_component=RequestingComponent.SUPERVISUAL,
        frame_profile="16:9_SOURCE_INTERVIEW",
        composition_role=CompositionRole.HERO_VISUAL,
        target_output_type=TargetOutputType.STILL_IMAGE,
        source_grounding_mode=SourceGroundingMode.DIRECT_REAL_REFERENCE,
        source_references=[SourceReference(source_kind="source_video", is_real_life_reference=True)],
        operator_route_hint=StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA,
    )
    report = service.validate_route_preconditions(request, StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA)
    assert "16_9_is_source_only_for_short_form_route" in report.violations


def test_style_route_eval_blocks_forbidden_pattern():
    with pytest.raises(Exception):
        StyleRouteEvaluationReceipt(route_id=StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA, forbidden_patterns_detected=["generic cinematic gloss"], pass_status=PassStatus.PASS)


def test_supervisual_can_compile_route_production_spec_from_visual_preproduction_packet():
    service = StyleRouteEngineService()
    source = SourceReference(source_kind="source_photo", source_id="photo_1", is_real_life_reference=True)
    request = service.create_decision_request(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        requesting_component=RequestingComponent.SUPERVISUAL,
        visual_preproduction_packet_id="vp_packet_1",
        visual_schema_id="visual_schema_1",
        visual_beat_plan_id="visual_beat_1",
        frame_profile="4:5_FEED_POSTER",
        composition_role=CompositionRole.HERO_VISUAL,
        target_output_type=TargetOutputType.STILL_IMAGE,
        source_grounding_mode=SourceGroundingMode.DIRECT_REAL_REFERENCE,
        source_references=[source],
        operator_route_hint=StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA,
    )
    decision = service.select_style_route(request)
    source_packet = service.compile_source_packet(request)
    cac_spec = service.compile_cac_production_spec(source_packet)
    route_spec = service.compile_route_production_spec(decision=decision, request=request, source_packet=source_packet, route_specific_spec_type="CACProductionSpec", route_specific_spec_id=cac_spec.cac_production_spec_id)
    assert route_spec.visual_preproduction_packet_id == "vp_packet_1"
    assert route_spec.visual_beat_plan_id == "visual_beat_1"
    assert route_spec.route_id == StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA
