from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_ideogram_4_compositionjob_lineage import _composition_fixture  # noqa: E402

from ccp_studio.contracts.assembly import AudioComponentRole  # noqa: E402
from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.services.assembly_planner import AssemblyPlanner, AssemblyPlannerError, register_assembly_command_handlers  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.workflows.render_workflow import RenderWorkflow  # noqa: E402


def _audio_components(scene_spec):
    return [
        {
            "role": AudioComponentRole.source_voice.value,
            "source_ref": f"source_expression_moment:{scene_spec.source_expression_moment_id}",
            "start_seconds": 0,
            "end_seconds": 4,
        },
        {
            "role": AudioComponentRole.interviewer_voice.value,
            "source_ref": "interviewer_prompt:opening",
            "start_seconds": 4,
            "end_seconds": 5,
        },
        {
            "role": AudioComponentRole.repaired_source_voice.value,
            "source_ref": "repaired_source:breath_cleanup",
            "start_seconds": 5,
            "end_seconds": 6,
        },
        {
            "role": AudioComponentRole.synthetic_bridge_voice.value,
            "source_ref": "synthetic_bridge:approved_connector",
            "start_seconds": 6,
            "end_seconds": 7,
        },
        {
            "role": AudioComponentRole.sfx.value,
            "source_ref": "sfx:paper_cut_rise",
            "start_seconds": 0,
            "end_seconds": 1.5,
        },
        {
            "role": AudioComponentRole.music.value,
            "source_ref": "music:licensed_bed",
            "start_seconds": 0,
            "end_seconds": 8,
        },
    ]


def _assembly_fixture():
    composition, compiler, _editing_service, org_id, brand_id, actor_id, scene_spec = _composition_fixture()
    job = composition.compile_composition_job(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)
    composition.submit_ideogram_composition_job(composition_job_id=job.composition_job_id, actor_id=actor_id)
    planner = AssemblyPlanner(compiler, composition_service=composition)
    return planner, compiler, org_id, brand_id, actor_id, scene_spec


def test_assembly_emits_layer_animation_edl_timeline_caption_and_sonic_manifests():
    planner, _compiler, _org_id, _brand_id, actor_id, scene_spec = _assembly_fixture()

    plan = planner.compile_assembly_plan(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)

    assert plan.layer_manifest_id in planner.repository.layer_manifests
    assert plan.animation_plan_id in planner.repository.animation_plans
    assert plan.edit_decision_list_id in planner.repository.edit_decision_lists
    assert plan.timeline_manifest_id in planner.repository.timeline_manifests
    assert plan.caption_manifest_id in planner.repository.caption_manifests
    assert plan.audio_mix_manifest_id in planner.repository.audio_mix_manifests
    assert plan.manifest_hashes["layer_manifest_hash"]


def test_audio_components_are_classified_and_traceable():
    planner, _compiler, _org_id, _brand_id, actor_id, scene_spec = _assembly_fixture()

    plan = planner.compile_assembly_plan(
        scene_spec_id=scene_spec.scene_spec_id,
        actor_id=actor_id,
        audio_components=_audio_components(scene_spec),
    )

    manifest = planner.repository.audio_mix_manifests[plan.audio_mix_manifest_id]
    roles = {component.role for component in manifest.components}
    assert roles == set(AudioComponentRole)
    assert all(component.source_ref for component in manifest.components)


def test_caption_timing_conflict_fails_for_repair():
    planner, _compiler, _org_id, _brand_id, actor_id, scene_spec = _assembly_fixture()

    with pytest.raises(AssemblyPlannerError) as exc:
        planner.compile_assembly_plan(
            scene_spec_id=scene_spec.scene_spec_id,
            actor_id=actor_id,
            caption_cues=[
                {
                    "text": "Too early",
                    "start_seconds": 0.5,
                    "end_seconds": 1.0,
                    "source_start_seconds": 2.0,
                    "source_end_seconds": 3.0,
                    "source_ref": f"source_expression_moment:{scene_spec.source_expression_moment_id}",
                }
            ],
        )

    assert exc.value.code == "CAPTION_SOURCE_TIMING_CONFLICT"
    assert list(planner.repository.receipts.values())[-1].decision_code == "ASSEMBLY_PLAN_BLOCKED"


def test_rig_layers_must_belong_to_locked_brand_context():
    planner, compiler, _org_id, _brand_id, actor_id, scene_spec = _assembly_fixture()
    selection_id = scene_spec.asset_selection_ids[0]
    selection = compiler.repository.asset_selections[selection_id]
    compiler.repository.asset_selections[selection_id] = selection.model_copy(update={"asset_id": uuid4(), "asset_hash": "sha256-outside"})

    with pytest.raises(AssemblyPlannerError) as exc:
        planner.compile_assembly_plan(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)

    assert exc.value.code == "BRAND_CONTEXT_ASSET_NOT_APPROVED"


def test_assembly_plan_receipt_includes_manifest_hashes_and_selected_asset_ids():
    planner, _compiler, _org_id, _brand_id, actor_id, scene_spec = _assembly_fixture()

    plan = planner.compile_assembly_plan(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)

    receipt = next(item for item in planner.repository.receipts.values() if item.assembly_plan_id == plan.assembly_plan_id)
    assert receipt.manifest_hashes == plan.manifest_hashes
    assert receipt.selected_asset_ids == plan.selected_asset_ids
    assert receipt.brand_context_version_id == scene_spec.brand_context_version_id
    assert receipt.timing_validation_passed is True
    assert receipt.caption_validation_passed is True
    assert receipt.sonic_validation_passed is True


def test_render_workflow_stage12_compiles_assembly_plan():
    planner, _compiler, _org_id, _brand_id, actor_id, scene_spec = _assembly_fixture()
    workflow = RenderWorkflow(planner)

    plan = workflow.stage12_compile_assembly_plan(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)

    assert plan.valid_for_render is True
    assert plan.assembly_plan_id in planner.repository.assembly_plans


def test_assembly_command_bus_emits_receipt_event():
    planner, _compiler, org_id, brand_id, actor_id, scene_spec = _assembly_fixture()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_assembly_command_handlers(bus, planner)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["production_steward"])
    envelope = new_command_envelope(
        command_type="CompileLayerManifestCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={"scene_spec_id": str(scene_spec.scene_spec_id)},
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["assembly_plan_id"]
    assert bus.event_outbox.events[-1].event_type == "CompileLayerManifestCommand.succeeded"
