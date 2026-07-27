from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.comfy_template_migration import WorkerAssetStatus  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.comfy_gpu_worker_service import ComfyGpuWorkerError, ComfyGpuWorkerService  # noqa: E402
from ccp_studio.services.comfy_template_migration_service import (  # noqa: E402
    ComfyTemplateMigrationError,
    ComfyTemplateMigrationService,
    register_comfy_template_migration_command_handlers,
)
from ccp_studio.services.provider_operations_service import ProviderOperationsService  # noqa: E402
from ccp_studio.workflows.migration_workflow import MigrationWorkflow  # noqa: E402


def _services():
    provider_operations = ProviderOperationsService()
    provider_operations.seed_current_cmf_capabilities()
    gpu = ComfyGpuWorkerService(provider_operations)
    migration = ComfyTemplateMigrationService(gpu)
    return migration, gpu


def _template_kwargs(actor_id=None):
    actor_id = actor_id or uuid4()
    return {
        "legacy_source_path": "legacy/comfy/Wan 2.2 i2v.json",
        "template_json": {"nodes": [{"id": "source_image"}, {"id": "wan_i2v"}], "edges": [["source_image", "wan_i2v"]]},
        "required_inputs": [
            {"input_name": "source_image_hash", "input_type": "artifact_hash", "required": True, "validation_rule": "sha256"},
            {"input_name": "prompt_hash", "input_type": "prompt_hash", "required": True, "validation_rule": "sha256"},
        ],
        "output_contract": {"output_contract": "cmf.render_output.v1", "version": "v1", "expected_artifact_types": ["png"]},
        "compatibility_notes": [{"note_type": "gpu", "note": "Requires 24GB or 32GB VRAM.", "severity": "high"}],
        "known_defects": ["can over-smooth hand edges"],
        "eval_target": "cmf.eval.render_artifact_integrity.v1",
        "eval_passed": True,
        "reviewer_id": uuid4(),
        "actor_id": actor_id,
    }


def test_migration_stores_source_hash_inputs_output_contract_compatibility_defects_eval_and_reviewer():
    migration, _gpu = _services()
    kwargs = _template_kwargs()

    asset = migration.migrate_template_to_worker_asset(**kwargs)

    assert asset.legacy_source_path.endswith("Wan 2.2 i2v.json")
    assert asset.content_hash
    assert asset.storage_uri.startswith("worker-assets/comfyui-workflows/")
    assert [item.input_name for item in asset.required_inputs] == ["source_image_hash", "prompt_hash"]
    assert asset.output_contract.output_contract == "cmf.render_output.v1"
    assert asset.compatibility_notes[0].note_type == "gpu"
    assert asset.known_defects == ["can over-smooth hand edges"]
    assert asset.eval_target == "cmf.eval.render_artifact_integrity.v1"
    assert asset.reviewer_id == kwargs["reviewer_id"]


def test_typed_inputs_checked_before_queueing_worker_asset():
    migration, _gpu = _services()
    asset = migration.migrate_template_to_worker_asset(**_template_kwargs())

    with pytest.raises(ComfyTemplateMigrationError) as exc:
        migration.validate_comfy_workflow_inputs(
            comfy_workflow_asset_id=asset.comfy_workflow_asset_id,
            provided_inputs={"source_image_hash": "sha256-source"},
        )

    assert exc.value.code == "COMFY_WORKFLOW_INPUT_MISSING"
    result = migration.validate_comfy_workflow_inputs(
        comfy_workflow_asset_id=asset.comfy_workflow_asset_id,
        provided_inputs={"source_image_hash": "sha256-source", "prompt_hash": "sha256-prompt"},
    )
    assert result["validated"] is True


def test_output_contract_change_requires_revalidation_and_blocks_gpu_worker_execution():
    migration, gpu = _services()
    actor_id = uuid4()
    asset = migration.migrate_template_to_worker_asset(**_template_kwargs(actor_id))
    active = migration.activate_comfy_workflow_asset(asset.comfy_workflow_asset_id, actor_id=actor_id)
    revalidation = migration.require_comfy_workflow_revalidation(
        active.comfy_workflow_asset_id,
        actor_id=actor_id,
        reason="output contract changed to cmf.render_output.v2",
    )

    with pytest.raises(ComfyGpuWorkerError) as exc:
        gpu.queue_comfy_gpu_worker_job(
            organization_id=uuid4(),
            brand_id=uuid4(),
            actor_id=actor_id,
            workflow_asset_id=revalidation.comfy_workflow_asset_id,
            workflow_hash=revalidation.content_hash,
            input_artifact_hashes=["sha256-render-contract"],
            typed_parameters={"source_image_hash": "sha256-source", "prompt_hash": "sha256-prompt"},
            cloud_provider="aws",
            gpu_tier="24gb_vram",
            docker_image_digest="sha256:comfy",
            expected_output_count=1,
        )

    assert revalidation.status == WorkerAssetStatus.revalidation_required
    assert exc.value.code == "UNAPPROVED_COMFY_WORKFLOW"


def test_failed_eval_template_remains_inactive_and_activation_is_blocked():
    migration, _gpu = _services()
    kwargs = _template_kwargs()
    kwargs["eval_passed"] = False
    asset = migration.migrate_template_to_worker_asset(**kwargs)

    with pytest.raises(ComfyTemplateMigrationError) as exc:
        migration.activate_comfy_workflow_asset(asset.comfy_workflow_asset_id, actor_id=kwargs["actor_id"])

    assert exc.value.code == "COMFY_WORKFLOW_EVAL_NOT_PASSED"
    assert migration.repository.assets[asset.comfy_workflow_asset_id].status == WorkerAssetStatus.inactive


def test_gpu_worker_receipt_includes_migrated_template_hash():
    migration, gpu = _services()
    kwargs = _template_kwargs()
    asset = migration.migrate_template_to_worker_asset(**kwargs)
    active = migration.activate_comfy_workflow_asset(asset.comfy_workflow_asset_id, actor_id=kwargs["actor_id"])

    job = gpu.queue_comfy_gpu_worker_job(
        organization_id=uuid4(),
        brand_id=uuid4(),
        actor_id=kwargs["actor_id"],
        workflow_asset_id=active.comfy_workflow_asset_id,
        workflow_hash=active.content_hash,
        input_artifact_hashes=["sha256-render-contract"],
        typed_parameters={"source_image_hash": "sha256-source", "prompt_hash": "sha256-prompt"},
        cloud_provider="google_cloud",
        gpu_tier="32gb_vram",
        docker_image_digest="sha256:comfy",
        expected_output_count=1,
    )

    receipt = next(item for item in gpu.repository.receipts.values() if item.gpu_worker_job_id == job.gpu_worker_job_id)
    assert receipt.workflow_hash == active.content_hash
    assert receipt.workflow_asset_id == active.comfy_workflow_asset_id


def test_workflow_stage0_migrates_template_to_worker_asset():
    migration, _gpu = _services()
    workflow = MigrationWorkflow(comfy_template_migration_service=migration)
    kwargs = _template_kwargs()

    asset = workflow.stage0_comfy_template_to_worker_asset(**kwargs)

    assert asset.comfy_workflow_asset_id in migration.repository.assets
    assert asset.storage_uri.startswith("worker-assets/comfyui-workflows/")


def test_command_bus_migrates_and_activates_worker_asset_with_receipt_event():
    migration, _gpu = _services()
    kwargs = _template_kwargs()
    org_id = uuid4()
    brand_id = uuid4()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_comfy_template_migration_command_handlers(bus, migration)
    actor = ActorContext(actor_id=kwargs["actor_id"], actor_type=ActorType.human, role_ids=["migration_steward"])
    envelope = new_command_envelope(
        command_type="MigrateComfyTemplateToWorkerAssetCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={key: value for key, value in kwargs.items() if key != "actor_id"},
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["comfy_workflow_asset_id"]
    assert bus.event_outbox.events[-1].event_type == "MigrateComfyTemplateToWorkerAssetCommand.succeeded"
