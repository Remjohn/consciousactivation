from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_layer_manifests_animation_plans_edl_captions_and_sonic_plans import _assembly_fixture  # noqa: E402

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.deterministic_rendering import DeterministicRenderer  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.deterministic_rendering_service import (  # noqa: E402
    DeterministicRenderError,
    DeterministicRenderService,
    register_deterministic_render_command_handlers,
)
from ccp_studio.services.provider_operations_service import ProviderOperationsService  # noqa: E402
from ccp_studio.workflows.render_workflow import RenderWorkflow  # noqa: E402


def _render_fixture():
    planner, compiler, org_id, brand_id, actor_id, scene_spec = _assembly_fixture()
    render_contract = compiler.render_contract_for_scene(scene_spec.scene_spec_id)
    assembly_plan = planner.compile_assembly_plan(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)
    composition = planner.composition_service
    provider_operations = ProviderOperationsService()
    provider_operations.seed_current_cmf_capabilities()
    service = DeterministicRenderService(
        scene_spec_compiler=compiler,
        assembly_planner=planner,
        composition_service=composition,
        provider_operations=provider_operations,
    )
    return service, planner, compiler, org_id, brand_id, actor_id, scene_spec, render_contract, assembly_plan


def test_renderer_props_consume_brand_layers_rig_text_captions_motion_audio_timing_and_variants():
    service, planner, compiler, _org_id, _brand_id, actor_id, scene_spec, render_contract, assembly_plan = _render_fixture()

    bundle = service.build_renderer_props_bundle(
        render_contract_id=render_contract.render_contract_id,
        assembly_plan_id=assembly_plan.assembly_plan_id,
        actor_id=actor_id,
    )

    payload = bundle.props_payload
    assert bundle.renderer == DeterministicRenderer.remotion
    assert bundle.layer_manifest_id == assembly_plan.layer_manifest_id
    assert bundle.animation_plan_id == assembly_plan.animation_plan_id
    assert bundle.timeline_manifest_id == assembly_plan.timeline_manifest_id
    assert bundle.caption_manifest_id == assembly_plan.caption_manifest_id
    assert bundle.audio_mix_manifest_id == assembly_plan.audio_mix_manifest_id
    assert bundle.rig_manifest_id == compiler.editing_session_service.brand_context_service.repository.versions[scene_spec.brand_context_version_id].asset_bundle.rig_manifest_id
    assert payload["final_text"]["rendered_by"] == "remotion"
    assert payload["caption_manifest"]["cues"]
    assert payload["audio_mix_manifest"]["components"]
    assert len(payload["platform_variants"]) == len(scene_spec.platform_variant_ids)
    assert bundle.generated_typescript_contract_hash
    assert "deterministic_renderer_props.ts" in bundle.generated_typescript_contract_ref


def test_final_text_is_rendered_deterministically_not_by_provider_image():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, _scene_spec, render_contract, assembly_plan = _render_fixture()

    bundle = service.build_renderer_props_bundle(
        render_contract_id=render_contract.render_contract_id,
        assembly_plan_id=assembly_plan.assembly_plan_id,
        actor_id=actor_id,
    )

    assert bundle.props_payload["final_text"]["provider_image_text_allowed"] is False
    assert bundle.props_payload["final_text"]["text_layer_strategy"].startswith("render_downstream")
    assert bundle.final_text_plan_id


def test_unapproved_brand_layer_fails_renderer_input_validation():
    service, planner, _compiler, _org_id, _brand_id, actor_id, _scene_spec, render_contract, assembly_plan = _render_fixture()
    layer_manifest = planner.repository.layer_manifests[assembly_plan.layer_manifest_id]
    broken_layer = layer_manifest.layers[0].model_copy(update={"brand_context_asset_id": uuid4()})
    planner.repository.layer_manifests[assembly_plan.layer_manifest_id] = layer_manifest.model_copy(update={"layers": [broken_layer, *layer_manifest.layers[1:]]})

    with pytest.raises(DeterministicRenderError) as exc:
        service.build_renderer_props_bundle(
            render_contract_id=render_contract.render_contract_id,
            assembly_plan_id=assembly_plan.assembly_plan_id,
            actor_id=actor_id,
        )

    assert exc.value.code == "BRAND_CONTEXT_ASSET_NOT_APPROVED"
    assert list(service.repository.receipts.values())[-1].decision_code == "DETERMINISTIC_RENDER_BLOCKED"


def test_render_output_stores_uris_hash_renderer_version_provider_receipt_and_render_receipt():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, _scene_spec, render_contract, assembly_plan = _render_fixture()
    bundle = service.build_renderer_props_bundle(
        render_contract_id=render_contract.render_contract_id,
        assembly_plan_id=assembly_plan.assembly_plan_id,
        actor_id=actor_id,
    )

    output = service.start_deterministic_render(
        renderer_props_bundle_id=bundle.renderer_props_bundle_id,
        actor_id=actor_id,
        idempotency_key="render:one",
    )

    receipt = next(item for item in service.repository.receipts.values() if item.render_output_id == output.render_output_id)
    assert output.preview_uri.startswith("object://renders/")
    assert output.final_uri.endswith(".final.mp4")
    assert output.output_hash
    assert output.renderer_version == "remotion:deterministic_props_v1"
    assert output.provider_receipt_id in service.provider_operations.repository.receipts
    assert receipt.output_hashes == [output.output_hash]
    assert receipt.input_manifest_hashes == output.manifest_hashes


def test_retry_preserves_completed_preview_and_final_artifacts():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, _scene_spec, render_contract, assembly_plan = _render_fixture()
    bundle = service.build_renderer_props_bundle(
        render_contract_id=render_contract.render_contract_id,
        assembly_plan_id=assembly_plan.assembly_plan_id,
        actor_id=actor_id,
    )
    output = service.start_deterministic_render(
        renderer_props_bundle_id=bundle.renderer_props_bundle_id,
        actor_id=actor_id,
        idempotency_key="render:retry-source",
    )

    replay = service.start_deterministic_render(
        renderer_props_bundle_id=bundle.renderer_props_bundle_id,
        actor_id=actor_id,
        idempotency_key="render:retry-new",
        retry_count=1,
    )

    assert replay.render_output_id == output.render_output_id
    assert replay.preview_uri == output.preview_uri
    assert replay.final_uri == output.final_uri
    assert list(service.repository.receipts.values())[-1].decision_code == "DETERMINISTIC_RENDER_REPLAYED"


def test_motion_canvas_route_uses_motion_canvas_provider_capability_and_version():
    service, _planner, _compiler, _org_id, _brand_id, actor_id, _scene_spec, render_contract, assembly_plan = _render_fixture()

    bundle = service.build_renderer_props_bundle(
        render_contract_id=render_contract.render_contract_id,
        assembly_plan_id=assembly_plan.assembly_plan_id,
        actor_id=actor_id,
        preferred_renderer=DeterministicRenderer.motion_canvas,
    )
    output = service.start_deterministic_render(
        renderer_props_bundle_id=bundle.renderer_props_bundle_id,
        actor_id=actor_id,
        idempotency_key="render:motion-canvas",
    )

    provider_receipt = service.provider_operations.repository.receipts[output.provider_receipt_id]
    assert bundle.renderer == DeterministicRenderer.motion_canvas
    assert output.renderer_version == "motion_canvas:deterministic_props_v1"
    assert provider_receipt.provider_capability_id == "motion_canvas.programmatic_animation.v1"


def test_render_workflow_and_command_bus_execute_stage12_deterministic_render():
    service, _planner, _compiler, org_id, brand_id, actor_id, _scene_spec, render_contract, assembly_plan = _render_fixture()
    workflow = RenderWorkflow(service.assembly_planner, deterministic_render_service=service)

    output = workflow.stage12_deterministic_render(
        render_contract_id=render_contract.render_contract_id,
        assembly_plan_id=assembly_plan.assembly_plan_id,
        actor_id=actor_id,
        idempotency_key="render:workflow",
    )

    assert output.output_hash

    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_deterministic_render_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["production_steward"])
    bundle = next(item for item in service.repository.props_bundles.values() if item.render_contract_id == render_contract.render_contract_id)
    envelope = new_command_envelope(
        command_type="StartDeterministicRenderCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "renderer_props_bundle_id": str(bundle.renderer_props_bundle_id),
            "render_idempotency_key": "render:command",
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["render_output_id"] == str(output.render_output_id)
    assert bus.event_outbox.events[-1].event_type == "StartDeterministicRenderCommand.succeeded"
