import pytest

from ccp_studio.contracts.supervisual_runtime import (
    SuperVisualCommand,
    SuperVisualVariantStatus,
)
from ccp_studio.repositories.supervisual_runtime import JsonFileSuperVisualRuntimeRepository
from ccp_studio.services.supervisual_runtime_service import SuperVisualRuntimeService


def _service(tmp_path):
    return SuperVisualRuntimeService(JsonFileSuperVisualRuntimeRepository(tmp_path / "sv_runtime"))


def _project_and_variant(service):
    project = service.create_project(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        title="Test SuperVisual",
        source_context_refs=["source_1"],
        default_frame_profile="1:1_SOFT_ROUNDED_EDITORIAL",
        created_by_actor_id="actor_1",
    )
    variant = service.repository.get_variant(project.current_variant_id)
    return project, variant


def test_create_project_persists_brand_context_version(tmp_path):
    service = _service(tmp_path)
    project, variant = _project_and_variant(service)
    reloaded = SuperVisualRuntimeService(JsonFileSuperVisualRuntimeRepository(tmp_path / "sv_runtime"))
    loaded = reloaded.repository.get_project(project.supervisual_project_id)
    assert loaded.brand_context_version_id == "bcv_1"
    assert variant.brand_context_version_id == "bcv_1"


def test_brand_context_version_is_immutable(tmp_path):
    service = _service(tmp_path)
    project, _ = _project_and_variant(service)
    project.brand_context_version_id = "bcv_changed"
    with pytest.raises(Exception):
        service.repository.update_project(project)


def test_create_variant_persists_lineage(tmp_path):
    service = _service(tmp_path)
    project, _ = _project_and_variant(service)
    variant = service.create_variant(project.supervisual_project_id, variant_label="Variant B")
    assert variant.lineage.source_context_refs == ["source_1"]


def test_project_snapshot_can_be_saved_and_loaded(tmp_path):
    service = _service(tmp_path)
    _, variant = _project_and_variant(service)
    snapshot = service.save_snapshot(variant.supervisual_variant_id, step="test", display_payload={"x": 1})
    assert service.repository.get_latest_snapshot(variant.supervisual_variant_id).supervisual_snapshot_id == snapshot.supervisual_snapshot_id


def test_event_log_is_append_only(tmp_path):
    service = _service(tmp_path)
    project, variant = _project_and_variant(service)
    initial_events = service.repository.list_events(project.supervisual_project_id, variant.supervisual_variant_id)
    service.save_snapshot(variant.supervisual_variant_id, step="another")
    later_events = service.repository.list_events(project.supervisual_project_id, variant.supervisual_variant_id)
    assert len(later_events) > len(initial_events)


def test_build_run_allows_step_runs(tmp_path):
    service = _service(tmp_path)
    _, variant = _project_and_variant(service)
    run = service.start_build_run(variant.supervisual_variant_id, requested_steps=["context_hydrate"])
    step = service.run_step(run.supervisual_build_run_id, "context_hydrate")
    assert step.status.value == "succeeded"


def test_step_completion_updates_variant_status(tmp_path):
    service = _service(tmp_path)
    _, variant = _project_and_variant(service)
    run = service.start_build_run(variant.supervisual_variant_id, requested_steps=["context_hydrate"])
    service.run_step(run.supervisual_build_run_id, "context_hydrate")
    updated = service.repository.get_variant(variant.supervisual_variant_id)
    assert updated.status == SuperVisualVariantStatus.CONTEXT_READY


def test_approved_variant_cannot_mutate(tmp_path):
    service = _service(tmp_path)
    _, variant = _project_and_variant(service)
    variant.status = SuperVisualVariantStatus.APPROVAL_READY
    service.repository.update_variant(variant)
    service.approve_variant(variant.supervisual_variant_id, approval_receipt_id="approval_1")
    with pytest.raises(Exception):
        service.apply_revision(variant.supervisual_variant_id, revision_note="change it")


def test_16_9_delivery_frame_profile_rejected(tmp_path):
    service = _service(tmp_path)
    with pytest.raises(Exception):
        service.create_project(
            brand_id="brand_1",
            brand_context_version_id="bcv_1",
            title="Bad profile",
            default_frame_profile="16:9_SOURCE_INTERVIEW",
        )


def test_idempotent_command_does_not_duplicate_events(tmp_path):
    service = _service(tmp_path)
    project, variant = _project_and_variant(service)
    command = SuperVisualCommand(
        command_type="noop",
        target_type="variant",
        target_id=variant.supervisual_variant_id,
        supervisual_project_id=project.supervisual_project_id,
        supervisual_variant_id=variant.supervisual_variant_id,
        idempotency_key="idem_1",
    )
    first = service.execute_command(command)
    event_count = len(service.repository.list_events(project.supervisual_project_id, variant.supervisual_variant_id))
    second = service.execute_command(command)
    assert first.command_id == second.command_id
    assert len(service.repository.list_events(project.supervisual_project_id, variant.supervisual_variant_id)) == event_count


def test_state_machine_composition_and_approval_flow(tmp_path):
    service = _service(tmp_path)
    _, variant = _project_and_variant(service)
    run = service.start_build_run(variant.supervisual_variant_id)
    service.run_step(run.supervisual_build_run_id, "composition_hypotheses")
    service.lock_composition(variant.supervisual_variant_id, composition_decision_receipt_id="composition_1")
    service.record_render_receipt(variant.supervisual_variant_id, render_receipt_id="render_1")
    service.record_eval_receipt(variant.supervisual_variant_id, evaluation_receipt_id="eval_1", passed=True)
    approved = service.approve_variant(variant.supervisual_variant_id, approval_receipt_id="approval_1")
    assert approved.status == SuperVisualVariantStatus.APPROVED
    exported = service.create_export_pack(variant.supervisual_variant_id, export_pack_id="export_1")
    assert exported.status == SuperVisualVariantStatus.EXPORTED
