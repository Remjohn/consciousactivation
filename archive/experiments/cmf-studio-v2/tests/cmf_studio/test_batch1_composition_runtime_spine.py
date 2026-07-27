from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_scenespec_creative_state_and_render_contract_compilation import (  # noqa: E402
    _platform_variants,
    _revision_policy,
    _scene_fixture,
)

from ccp_studio.contracts.composition_runtime import (  # noqa: E402
    AdapterDecision,
    ApprovalStatus,
    CompositionTemplateLayer,
    CompositionZone,
    IntegrationCandidate,
    RendererComponentRegistration,
)
from ccp_studio.services.composition_runtime_service import (  # noqa: E402
    CompositionRuntimeService,
    CompositionRuntimeServiceError,
)
from ccp_studio.services.reaction_editing_service import ReactionEditingTemplateService  # noqa: E402


def _batch1_fixture():
    compiler, editing_service, org_id, brand_id, actor_id, editing_session, selected_assets = _scene_fixture()
    reaction_service = ReactionEditingTemplateService(editing_service.routing_service)
    template_receipt = reaction_service.plan_template_route(
        organization_id=editing_session.organization_id,
        brand_id=editing_session.brand_id,
        asset_route_receipt_id=editing_session.asset_route_receipt_id,
        actor_id=actor_id,
        requested_template_code="VRS-SPLIT",
        content_format_code="SV-RRC",
    )
    scene_spec = compiler.compile_scene_spec(
        complete_editing_session_id=editing_session.complete_editing_session_id,
        actor_id=actor_id,
        selected_asset_refs=selected_assets,
        platform_variants=_platform_variants(),
        revision_policy=_revision_policy(),
        renderer_route=template_receipt.scene_spec_requirement_patch["renderer_route"],
        composition_requirements=template_receipt.scene_spec_requirement_patch,
        reaction_template_route_id=template_receipt.reaction_template_route_id,
        reaction_template_code=template_receipt.template_code,
    )
    runtime = CompositionRuntimeService()
    binding = runtime.bind_scene_template(
        scene_spec=scene_spec,
        reaction_template_route_receipt=template_receipt,
        actor_id=actor_id,
    )
    return runtime, compiler, editing_service, org_id, brand_id, actor_id, scene_spec, template_receipt, binding


def _segments():
    return [
        {
            "source_ref": "transcript:claude:001",
            "start_seconds": 0.4,
            "end_seconds": 4.2,
            "speaker": "interviewer",
            "text": "Was the silence betrayal, fear, or survival?",
            "expression_state": "provocation with care",
            "target_layer_id": "reaction-ui",
        },
        {
            "source_ref": "transcript:claude:002",
            "start_seconds": 4.2,
            "end_seconds": 11.8,
            "speaker": "guest",
            "text": "Sometimes silence is how people survive what they cannot name yet.",
            "expression_state": "recognition landing",
            "target_layer_id": "guest-cutout",
        },
    ]


def test_batch1_scene_binding_and_composition_json_are_canonical_and_primitive_gated():
    runtime, _compiler, _editing_service, _org_id, _brand_id, actor_id, _scene_spec, _template_receipt, binding = _batch1_fixture()

    template = runtime.register_composition_template_json(
        binding=binding,
        route_id="SV-RRC",
        actor_id=actor_id,
        preview_asset_refs=["preview://reaction-versus-layout.png"],
    )
    receipt = next(iter(runtime.repository.composition_template_approval_receipts.values()))
    preflight = next(iter(runtime.repository.composition_preflight_receipts.values()))

    assert template.approval_status == ApprovalStatus.approved
    assert template.composition_json_hash
    assert template.preview_asset_refs == ["preview://reaction-versus-layout.png"]
    assert receipt.decision == "approved"
    assert preflight.primitive_validation_count == 3
    assert all(preflight.role_coverage.values())

    with pytest.raises(CompositionRuntimeServiceError) as exc:
        runtime.register_composition_template_json(
            binding=binding,
            route_id="SV-RRC",
            actor_id=actor_id,
            primitive_results=runtime.primitive_results_for_route("SV-RRC")[:2],
        )

    assert exc.value.code == "COMPOSITION_PREFLIGHT_BLOCKED"
    assert "COMPOSITION_PRIMITIVE_MINIMUM_NOT_MET" in exc.value.message


def test_batch1_reaction_renderer_uses_upper_reaction_ui_lower_human_cutouts_and_transcript_timing():
    runtime, _compiler, _editing_service, _org_id, _brand_id, actor_id, scene_spec, _template_receipt, binding = _batch1_fixture()
    template = runtime.register_composition_template_json(binding=binding, route_id="SV-RRC", actor_id=actor_id)
    beat_map, receipt = runtime.compile_beat_map(expression_moment_id=scene_spec.source_expression_moment_id, segments=_segments())

    manifest = runtime.compile_reaction_renderer_manifest(composition_template_id=template.composition_template_id, beat_map=beat_map)

    assert receipt.decision_code == "BEAT_MAP_COMPILED"
    assert manifest.renderer_props.upper_reaction_ui_zone_id == "upper-ui"
    assert manifest.renderer_props.lower_human_cutout_zone_id == "lower-human"
    assert {item.role for item in manifest.renderer_props.subject_cutouts} == {"guest", "interviewer"}
    assert all(item.background_removed for item in manifest.renderer_props.subject_cutouts)
    assert manifest.deterministic_inputs_hash


def test_batch1_four_format_crosswalk_visual_feel_and_content_asset_codes_are_registered():
    runtime, _compiler, _editing_service, org_id, brand_id, _actor_id, scene_spec, _template_receipt, _binding = _batch1_fixture()

    plan = runtime.plan_four_video_formats(organization_id=org_id, brand_id=brand_id, expression_moment_id=scene_spec.source_expression_moment_id)
    families = runtime.register_default_template_families()
    visual_feel = runtime.default_visual_feel_contract("SV-EDU")
    reservation = runtime.reserve_content_asset_code(
        brand_id=brand_id,
        template_family_code="PPR-EDU",
        content_format_code="SV-EDU",
        sequence_number=1,
        object_ref=f"expression_moment:{scene_spec.source_expression_moment_id}",
    )

    assert {item.slot_code for item in plan.slot_requirements} == {"SV-CSC", "SV-EDU", "SV-FRB", "SV-RRC"}
    assert {item.family_code for item in families}.issuperset({"PPR-EDU", "RCT-VRS", "CIN-STORY"})
    assert visual_feel.minimum_validated_primitives == 3
    assert reservation.content_asset_code == "CMF-PPR-SV-EDU-0001"


def test_batch1_runtime_binding_carries_brand_genesis_expression_lineage_and_beat_map():
    runtime, _compiler, _editing_service, _org_id, _brand_id, actor_id, scene_spec, _template_receipt, binding = _batch1_fixture()
    template = runtime.register_composition_template_json(binding=binding, route_id="SV-RRC", actor_id=actor_id)
    beat_map, _receipt = runtime.compile_beat_map(expression_moment_id=scene_spec.source_expression_moment_id, segments=_segments())
    substrate = runtime.resolve_brand_genesis_substrate(scene_spec=scene_spec)
    lineage = runtime.bind_expression_lineage(
        interview_asset_contract_id=uuid4(),
        expression_moment_id=scene_spec.source_expression_moment_id,
        complete_editing_session_id=scene_spec.complete_editing_session_id,
        asset_route_receipt_id=scene_spec.asset_route_receipt_id,
        transcript_segment_refs=["transcript:claude:001", "transcript:claude:002"],
    )

    runtime_binding = runtime.bind_composition_runtime(
        scene_template_binding_id=binding.scene_template_binding_id,
        composition_template_id=template.composition_template_id,
        brand_genesis_substrate_id=substrate.resolved_brand_genesis_substrate_id,
        expression_lineage_binding_ref=f"expression_lineage:{lineage.expression_lineage_binding_receipt_id}",
        visual_feel_contract_id=template.visual_feel_contract_id,
        composition_beat_map_id=beat_map.composition_beat_map_id,
        renderer_route=binding.renderer_route,
    )

    assert substrate.binding.voice_dna_ref.startswith("brand_context:")
    assert lineage.decision_code == "EXPRESSION_LINEAGE_BOUND"
    assert runtime_binding.approval_status == ApprovalStatus.approved
    assert runtime.repository.runtime_binding_receipts


def test_batch1_papercut_performance_and_micro_semiotic_gates_keep_educational_format_distinct():
    runtime, _compiler, _editing_service, _org_id, _brand_id, actor_id, scene_spec, _template_receipt, binding = _batch1_fixture()
    edu_binding = binding.model_copy(
        update={
            "template_code": "PPR-EDU",
            "content_format_code": "SV-EDU",
            "composition_id": "papercut-myth-truth-explainer",
        }
    )
    template = runtime.register_composition_template_json(binding=edu_binding, route_id="SV-EDU", actor_id=actor_id)
    beat_map, _receipt = runtime.compile_beat_map(expression_moment_id=scene_spec.source_expression_moment_id, segments=_segments())

    performance = runtime.select_performance_state(
        expression_state="teaching with gentle correction",
        emotion="warm confidence",
        gesture="open palm explanation",
        evidence_refs=["acting_library:64-state", "transcript:claude:002"],
    )
    manifest, receipt = runtime.compile_papercut_runtime_manifest(
        composition_template_id=template.composition_template_id,
        rig_refs=["rig:guest-papercut-upper-body", "rig:paper-note-stack"],
        beat_map=beat_map,
    )
    anchor = runtime.select_micro_semiotic_anchors(
        route_id="SV-EDU",
        audience_context_ref="context_premise:audience-comment-cluster",
        anchor_refs=["anchor:river-metaphor", "anchor:paper-note"],
        risk_score=0.18,
    )

    assert performance.acting_state_code.startswith("ACT-")
    assert manifest.materiality_rules[0].texture == "fibrous_paper_with_visible_edge"
    assert manifest.motion_cues[0].motion_type == "paper_slide_or_pop"
    assert receipt.decision_code == "PAPERCUT_RUNTIME_READY"
    assert anchor.blocker_codes == []


def test_batch1_ideogram_layer_extraction_and_renderer_props_stay_downstream_deterministic():
    runtime, _compiler, _editing_service, _org_id, _brand_id, actor_id, scene_spec, _template_receipt, binding = _batch1_fixture()
    template = runtime.register_composition_template_json(binding=binding, route_id="SV-RRC", actor_id=actor_id)
    beat_map, _receipt = runtime.compile_beat_map(expression_moment_id=scene_spec.source_expression_moment_id, segments=_segments())
    substrate = runtime.resolve_brand_genesis_substrate(scene_spec=scene_spec)
    runtime_binding = runtime.bind_composition_runtime(
        scene_template_binding_id=binding.scene_template_binding_id,
        composition_template_id=template.composition_template_id,
        brand_genesis_substrate_id=substrate.resolved_brand_genesis_substrate_id,
        expression_lineage_binding_ref="expression_lineage:test",
        visual_feel_contract_id=template.visual_feel_contract_id,
        composition_beat_map_id=beat_map.composition_beat_map_id,
        renderer_route=binding.renderer_route,
    )

    bridge = runtime.bridge_ideogram_to_production_template(
        composition_job_id=uuid4(),
        zones=template.zones,
        layer_manifest_ref="layer_manifest:ideogram-plate-001",
    )
    _job, extraction = runtime.extract_layers(source_asset_ref="ideogram_plate:001", layer_roles=["background", "reaction_ui", "guest_cutout"])
    manifest, report, receipt = runtime.compile_renderer_props(
        runtime_binding_id=runtime_binding.composition_runtime_binding_id,
        component=RendererComponentRegistration(
            component_code="remotion-reaction-split",
            renderer_target="remotion",
            supported_format_codes=["SV-RRC"],
            prop_schema_ref="schemas/remotion/reaction-split-props.json",
            sandbox_policy="no_network_no_production_api",
        ),
    )

    assert bridge.decision_code == "IDEOGRAM_LAYOUT_BRIDGED_TO_PRODUCTION_TEMPLATE"
    assert extraction.repair_required is False
    assert report.compatible is True
    assert receipt.decision_code == "RENDERER_PROPS_COMPILED"
    assert manifest.deterministic_inputs_hash


def test_batch1_open_source_adapters_eval_conversion_and_operator_approval_are_sandboxed():
    runtime, _compiler, _editing_service, _org_id, _brand_id, actor_id, _scene_spec, _template_receipt, binding = _batch1_fixture()
    template = runtime.register_composition_template_json(binding=binding, route_id="SV-RRC", actor_id=actor_id)
    preflight = next(iter(runtime.repository.composition_preflight_receipts.values()))
    candidate = runtime.register_integration_candidate(
        IntegrationCandidate(
            name="OpenMontage",
            repo_url="https://github.com/calesthio/OpenMontage",
            category="video_editing",
            proposed_use="architectural reference for stage graph and montage sequencing",
            license_family="MIT",
            deterministic_boundary="adapter emits CMF stage manifest and never owns final render authority",
            production_authority_allowed=False,
            evidence_refs=["TS-CMF-076", "TS-CMF-091"],
        )
    )

    decision = runtime.run_integration_fit_eval(candidate.integration_candidate_id)
    conversion = runtime.convert_open_source_template(
        integration_adapter_decision_id=decision.integration_adapter_decision_id,
        source_project="OpenMontage",
        source_template_ref="montage/stage_graph",
        cmf_template_family_code="RCT-VRS",
        converted_component_code="cmf-openmontage-stage-graph",
    )
    eval_run = runtime.run_composition_eval_suite(
        target_object_type="CompositionTemplateJson",
        target_object_ref=f"composition_template:{template.composition_template_id}",
        preflight_receipt_id=preflight.composition_preflight_receipt_id,
        doctrine_receipt_refs=["doctrine:composition-route-feel"],
    )
    review = runtime.build_review_read_model(
        target_object_ref=f"composition_template:{template.composition_template_id}",
        eval_suite_run_id=eval_run.composition_eval_suite_run_id,
        evidence_refs=[template.composition_json_hash, f"conversion:{conversion.open_source_template_conversion_id}"],
    )
    approval = runtime.record_operator_approval(review_read_model_id=review.review_read_model_id, operator_id=actor_id)

    assert decision.decision == AdapterDecision.approved_adapter
    assert conversion.direct_import_allowed is False
    assert eval_run.decision == "approved"
    assert review.approval_status == ApprovalStatus.approved
    assert approval.decision == "approved"
