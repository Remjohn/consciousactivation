import pytest

from ccp_studio.contracts.visual_preproduction import (
    CameraMoralStance,
    ConstraintGateCReport,
    ConstraintViolation,
    FamiliarityElementId,
    KineticVerb,
    LightingPreset,
    PRIMALAnalysis,
    PassStatus,
    PreproductionDepth,
    REQUIRED_FAMILIARITY_ELEMENTS,
    ShotType,
    SourceAuthorityLevel,
    SourceRef,
    StoryboardCommanderVerdict,
    TargetComponent,
    TCode,
    VAEDecoderReport,
    VCode,
    VisualAnalystReport,
    VisualBeatPlan,
    VisualFamiliarityElementAssessment,
    VisualPreproductionPacket,
    VisualPreproductionRequest,
    VisualSchema,
)
from ccp_studio.services.visual_preproduction_service import VisualPreproductionService


def _all_elements():
    return [
        VisualFamiliarityElementAssessment(
            element_id=element,
            finding=f"finding for {element.value}",
            score=0.75,
        )
        for element in FamiliarityElementId
    ]


def test_visual_schema_requires_brand_context_version():
    with pytest.raises(Exception):
        VisualSchema(
            brand_id="brand_1",
            brand_context_version_id="",
            target_component=TargetComponent.SUPERVISUAL,
            preproduction_depth=PreproductionDepth.LITE,
            visual_familiarity_elements=_all_elements(),
            environment_logic="desk context",
            source_authority_map={"environment_logic": SourceAuthorityLevel.RESEARCH_SUPPORTED},
        )


def test_visual_schema_covers_16_familiarity_elements_or_marks_not_applicable():
    schema = VisualSchema(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        target_component=TargetComponent.SUPERVISUAL,
        preproduction_depth=PreproductionDepth.LITE,
        visual_familiarity_elements=_all_elements(),
        environment_logic="human-scale desk context",
        source_authority_map={"environment_logic": SourceAuthorityLevel.RESEARCH_SUPPORTED},
    )
    assert {e.element_id.value for e in schema.visual_familiarity_elements} == REQUIRED_FAMILIARITY_ELEMENTS

    with pytest.raises(Exception):
        VisualSchema(
            brand_id="brand_1",
            brand_context_version_id="bcv_1",
            target_component=TargetComponent.SUPERVISUAL,
            preproduction_depth=PreproductionDepth.LITE,
            visual_familiarity_elements=_all_elements()[:-1],
            environment_logic="desk context",
            source_authority_map={"environment_logic": SourceAuthorityLevel.RESEARCH_SUPPORTED},
        )


def test_visual_schema_claims_require_source_evidence():
    with pytest.raises(Exception):
        VisualSchema(
            brand_id="brand_1",
            brand_context_version_id="bcv_1",
            target_component=TargetComponent.SUPERVISUAL,
            preproduction_depth=PreproductionDepth.LITE,
            visual_familiarity_elements=_all_elements(),
            environment_logic="desk context",
            source_authority_map={},
        )


def test_storyboard_ingredients_emit_asset_requirements():
    service = VisualPreproductionService()
    request = service.create_request(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        target_component=TargetComponent.SUPERVISUAL,
        preproduction_depth=PreproductionDepth.LITE,
    )
    schema = service.compile_visual_schema(request, environment_logic="source-backed desk")
    ingredients = service.compile_storyboard_ingredients(schema)
    requirements = service.emit_asset_requirements(ingredients)
    assert len(requirements) >= 1
    assert requirements[0].ingredient_kind == "proof_object"


def test_primal_analysis_requires_feeling_body_truth_environment():
    with pytest.raises(Exception):
        PRIMALAnalysis(
            visual_beat_plan_id="beat_1",
            feeling="",
            body_truth="hands hesitate",
            environment="desk",
            timestamp_or_temporal_context="morning",
            uniqueness="marked notebook",
        )


def test_vae_blocks_generic_cliche_visual():
    with pytest.raises(Exception):
        VAEDecoderReport(
            visual_beat_plan_id="beat_1",
            semantic_check="legible",
            shadow_filter="ok",
            anti_cliche_gate="failed",
            generic_visual_risks=["generic founder skyline"],
            pass_status=PassStatus.PASS,
        )

    report = VAEDecoderReport(
        visual_beat_plan_id="beat_1",
        semantic_check="legible",
        shadow_filter="ok",
        anti_cliche_gate="failed",
        generic_visual_risks=["generic founder skyline"],
        recommended_repairs=["replace with source-backed proof object"],
        pass_status=PassStatus.FAIL,
    )
    assert report.pass_status == PassStatus.FAIL


def test_constraint_gate_c_blocks_missing_character_anchor():
    with pytest.raises(Exception):
        ConstraintGateCReport(
            target_ref="beat_1",
            checks={"character_anchor_vs_beat_action": False},
            violations=[
                ConstraintViolation(
                    check_id="character_anchor_vs_beat_action",
                    severity="blocking",
                    message="missing character anchor",
                )
            ],
            pass_status=PassStatus.PASS,
        )


def test_constraint_gate_c_blocks_source_authority_failure():
    service = VisualPreproductionService()
    report = service.run_constraint_gate_c(target_ref="beat_1", source_authority_pass=False)
    assert report.pass_status == PassStatus.FAIL
    assert report.blocking_violations


def test_visual_analyst_rejects_failed_checks():
    with pytest.raises(Exception):
        VisualAnalystReport(
            target_component=TargetComponent.VIDEO,
            failed_checks=["missing_t_code"],
            pass_status=PassStatus.PASS,
        )


def test_visual_analyst_validates_t_code_v_code_kinetic_verb():
    service = VisualPreproductionService()
    request = service.create_request(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        target_component=TargetComponent.SUPERVISUAL,
        preproduction_depth=PreproductionDepth.LITE,
    )
    schema = service.compile_visual_schema(request, environment_logic="source-backed desk")
    beat = service.compile_beat_visual_plan(schema)
    report = service.validate_with_visual_analyst(
        target_component=TargetComponent.SUPERVISUAL,
        beat_plans=[beat],
    )
    assert report.pass_status == PassStatus.PASS
    assert "t_code_present" in report.passed_checks
    assert "v_code_present" in report.passed_checks
    assert "kinetic_verb_present" in report.passed_checks


def test_storyboard_commander_rejects_batch_without_visual_anchor():
    service = VisualPreproductionService()
    verdict = service.authorize_with_storyboard_commander(
        visual_anchor_present=False,
        camera_moral_stance_present=True,
        montage_logic_present=True,
    )
    assert not verdict.approved_for_downstream
    assert verdict.required_repairs


def test_packet_cannot_freeze_with_blocking_violations():
    service = VisualPreproductionService()
    request = service.create_request(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        target_component=TargetComponent.SUPERVISUAL,
        preproduction_depth=PreproductionDepth.LITE,
    )
    schema = service.compile_visual_schema(request, environment_logic="source-backed desk")
    packet = service.create_packet(request=request, schema=schema)
    gate = service.run_constraint_gate_c(target_ref=packet.visual_preproduction_packet_id, asset_coverage_pass=False)
    with pytest.raises(Exception):
        service.freeze_packet(packet, gate_c_report=gate)


def test_lite_mode_can_freeze_single_supervisual_packet():
    service = VisualPreproductionService()
    request = service.create_request(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        target_component=TargetComponent.SUPERVISUAL,
        preproduction_depth=PreproductionDepth.LITE,
    )
    schema = service.compile_visual_schema(request, environment_logic="source-backed desk")
    ingredients = service.compile_storyboard_ingredients(schema)
    beat = service.compile_beat_visual_plan(schema)
    primal = service.run_primal_analysis(beat, feeling="quiet proof", body_truth="hand pauses over receipt")
    vae = service.run_vae_decoder(beat)
    gate = service.run_constraint_gate_c(target_ref=beat.visual_beat_plan_id)
    analyst = service.validate_with_visual_analyst(
        target_component=TargetComponent.SUPERVISUAL,
        beat_plans=[beat],
    )
    packet = service.create_packet(
        request=request,
        schema=schema,
        ingredients=ingredients,
        beat_plans=[beat],
        primal_reports=[primal],
        vae_reports=[vae],
        gate_c_report=gate,
        analyst_report=analyst,
    )
    frozen = service.freeze_packet(packet, gate_c_report=gate, analyst_report=analyst)
    assert frozen.packet_status.value == "frozen"
    assert frozen.frozen_at


def test_full_batch_mode_requires_commander_verdict():
    service = VisualPreproductionService()
    request = service.create_request(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        target_component=TargetComponent.VIDEO,
        preproduction_depth=PreproductionDepth.FULL_BATCH,
    )
    schema = service.compile_visual_schema(request, environment_logic="source-backed scene pack")
    packet = service.create_packet(request=request, schema=schema)
    gate = service.run_constraint_gate_c(target_ref=packet.visual_preproduction_packet_id)
    analyst = service.validate_with_visual_analyst(
        target_component=TargetComponent.VIDEO,
        beat_plans=[],
    )
    with pytest.raises(Exception):
        service.freeze_packet(packet, gate_c_report=gate, analyst_report=analyst)

    verdict = service.authorize_with_storyboard_commander(
        packet_id=packet.visual_preproduction_packet_id,
        visual_anchor_present=True,
        camera_moral_stance_present=True,
        montage_logic_present=True,
    )
    frozen = service.freeze_packet(
        packet,
        gate_c_report=gate,
        analyst_report=analyst,
        commander_verdict=verdict,
    )
    assert frozen.packet_status.value == "frozen"
    assert frozen.storyboard_commander_verdict_id == verdict.storyboard_commander_verdict_id


def test_visual_preproduction_integrates_with_asset_requirement_contracts():
    service = VisualPreproductionService()
    request = service.create_request(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        target_component=TargetComponent.CAROUSEL,
        preproduction_depth=PreproductionDepth.STANDARD,
    )
    schema = service.compile_visual_schema(
        request,
        environment_logic="source-backed workspace",
        visual_tropes_to_avoid=["generic skyline"],
    )
    ingredients = service.compile_storyboard_ingredients(schema)
    assert ingredients.asset_requirements
    assert ingredients.asset_requirements[0].source_authority_required == SourceAuthorityLevel.RESEARCH_SUPPORTED
