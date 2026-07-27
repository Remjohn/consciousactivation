from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_scenespec_creative_state_and_render_contract_compilation import (  # noqa: E402
    _compile,
    _scene_fixture,
)

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.composition import CompositionUsageState  # noqa: E402
from ccp_studio.providers.ideogram import Ideogram4Adapter  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.composition_service import CompositionService, register_composition_command_handlers  # noqa: E402
from ccp_studio.workflows.complete_editing_session import CompleteEditingSessionWorkflow  # noqa: E402


def _composition_fixture(provider=None):
    compiler, editing_service, org_id, brand_id, actor_id, editing_session, selected_assets = _scene_fixture()
    scene_spec = _compile(compiler, actor_id, editing_session, selected_assets)
    composition = CompositionService(compiler, provider=provider or Ideogram4Adapter())
    return composition, compiler, editing_service, org_id, brand_id, actor_id, scene_spec


def test_submit_stores_composition_job_json_prompt_hash_constraints_provider_metadata_and_correlation_id():
    composition, _compiler, _editing_service, _org_id, _brand_id, actor_id, scene_spec = _composition_fixture()

    job = composition.compile_composition_job(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)
    plate = composition.submit_ideogram_composition_job(composition_job_id=job.composition_job_id, actor_id=actor_id)
    updated_job = composition.repository.composition_jobs[job.composition_job_id]

    assert updated_job.job_json_hash
    assert updated_job.prompt_hash
    assert updated_job.constraints.final_text_policy.endswith("rendered downstream.")
    assert updated_job.provider_metadata["provider_name"] == "ideogram_4"
    assert updated_job.provider_correlation_id
    assert plate.composition_job_id == job.composition_job_id


def test_plate_stores_uri_hash_analysis_and_provider_receipt_linked_to_session():
    composition, _compiler, _editing_service, _org_id, brand_id, actor_id, scene_spec = _composition_fixture()
    job = composition.compile_composition_job(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)

    plate = composition.submit_ideogram_composition_job(composition_job_id=job.composition_job_id, actor_id=actor_id)

    receipt = next(item for item in composition.repository.receipts.values() if item.composition_plate_id == plate.composition_plate_id)
    assert plate.plate_uri.startswith(f"object://brands/{brand_id}/composition-plates/")
    assert plate.plate_hash
    assert plate.provider_receipt_id in composition.repository.provider_receipts
    assert plate.composition_analysis_id in composition.repository.analyses
    assert receipt.complete_editing_session_id == scene_spec.complete_editing_session_id


def test_final_text_or_identity_drift_restricts_plate_instead_of_final_authority():
    provider = Ideogram4Adapter(analysis_override={"baked_final_text_detected": True, "identity_drift_score": 0.2})
    composition, _compiler, _editing_service, _org_id, _brand_id, actor_id, scene_spec = _composition_fixture(provider)
    job = composition.compile_composition_job(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)

    plate = composition.submit_ideogram_composition_job(composition_job_id=job.composition_job_id, actor_id=actor_id)

    assert plate.usage_state == CompositionUsageState.background_only
    final_text_plan = composition.repository.final_text_plans[composition.repository.composition_jobs[job.composition_job_id].final_text_plan_id]
    assert final_text_plan.editable_text_required is True
    assert "downstream" in final_text_plan.text_layer_strategy


def test_downstream_edit_references_originating_composition_job_and_plate():
    composition, _compiler, _editing_service, _org_id, _brand_id, actor_id, scene_spec = _composition_fixture()
    job = composition.compile_composition_job(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)
    plate = composition.submit_ideogram_composition_job(composition_job_id=job.composition_job_id, actor_id=actor_id)

    edit = composition.link_downstream_composition_edit(
        composition_plate_id=plate.composition_plate_id,
        downstream_object_id=uuid4(),
        downstream_object_type="identity_repair_job",
        edit_type="identity_rebuild_from_locked_brand_layers",
        reason="Ideogram plate guides layout only.",
        actor_id=actor_id,
    )

    assert edit.composition_job_id == job.composition_job_id
    assert edit.composition_plate_id == plate.composition_plate_id


def test_audit_lineage_shows_job_hash_plate_analysis_downstream_edit_and_final_text_plan():
    composition, _compiler, _editing_service, _org_id, _brand_id, actor_id, scene_spec = _composition_fixture()
    job = composition.compile_composition_job(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)
    plate = composition.submit_ideogram_composition_job(composition_job_id=job.composition_job_id, actor_id=actor_id)
    composition.link_downstream_composition_edit(
        composition_plate_id=plate.composition_plate_id,
        downstream_object_id=uuid4(),
        downstream_object_type="layer_manifest",
        edit_type="layer_decomposition",
        reason="Prepare plate for downstream render.",
        actor_id=actor_id,
    )

    audit = composition.audit_composition_lineage(job.composition_job_id)

    assert audit.composition_job.job_json_hash == job.job_json_hash
    assert audit.composition_plate.plate_uri == plate.plate_uri
    assert audit.composition_analysis.composition_job_id == job.composition_job_id
    assert len(audit.downstream_edits) == 1
    assert audit.final_text_plan.text_content_ref.startswith("source_expression_moment:")


def test_workflow_stage10_composition_control_compiles_and_submits_plate():
    composition, compiler, editing_service, _org_id, _brand_id, actor_id, scene_spec = _composition_fixture()
    workflow = CompleteEditingSessionWorkflow(
        editing_service,
        scene_spec_compiler=compiler,
        composition_service=composition,
    )

    plate = workflow.stage10_composition_control(scene_spec_id=scene_spec.scene_spec_id, actor_id=actor_id)

    assert plate.composition_job_id in composition.repository.composition_jobs
    assert plate.usage_state == CompositionUsageState.approved_composition_plate


def test_composition_command_bus_emits_receipt_event():
    composition, _compiler, _editing_service, org_id, brand_id, actor_id, scene_spec = _composition_fixture()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_composition_command_handlers(bus, composition)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["production_steward"])
    envelope = new_command_envelope(
        command_type="CompileCompositionJobCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={"scene_spec_id": str(scene_spec.scene_spec_id)},
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["composition_job_id"]
    assert bus.event_outbox.events[-1].event_type == "CompileCompositionJobCommand.succeeded"
