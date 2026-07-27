from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.comfy_gpu_worker import GpuWorkerStatus  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.comfy_gpu_worker_service import (  # noqa: E402
    ComfyGpuWorkerError,
    ComfyGpuWorkerService,
    register_comfy_gpu_worker_command_handlers,
)
from ccp_studio.services.provider_operations_service import ProviderOperationsService  # noqa: E402
from ccp_studio.workflows.provider_job_workflow import ProviderJobWorkflow  # noqa: E402


def _service() -> ComfyGpuWorkerService:
    provider_operations = ProviderOperationsService()
    provider_operations.seed_current_cmf_capabilities()
    return ComfyGpuWorkerService(provider_operations)


def _job_kwargs(service: ComfyGpuWorkerService):
    asset = next(iter(service.repository.workflow_assets.values()))
    return {
        "organization_id": uuid4(),
        "brand_id": uuid4(),
        "actor_id": uuid4(),
        "workflow_asset_id": asset.workflow_asset_id,
        "workflow_hash": asset.workflow_hash,
        "input_artifact_hashes": ["sha256-render-contract", "sha256-layer-manifest"],
        "typed_parameters": {"prompt_hash": "sha256-comfy-prompt", "batch_size": 2},
        "cloud_provider": "aws",
        "gpu_tier": "24gb_vram",
        "docker_image_digest": "sha256:comfyui-worker-image",
        "expected_output_count": 2,
    }


def test_worker_start_records_gpu_cloud_docker_queue_workflow_inputs_and_job_ids():
    service = _service()
    kwargs = _job_kwargs(service)

    job = service.queue_comfy_gpu_worker_job(**kwargs)
    execution = service.start_gpu_worker(job.gpu_worker_job_id, actor_id=kwargs["actor_id"])

    assert job.cloud_provider.value == "aws"
    assert job.gpu_tier.value == "24gb_vram"
    assert job.docker_image_digest == "sha256:comfyui-worker-image"
    assert job.queue_position == 1
    assert job.workflow_hash == kwargs["workflow_hash"]
    assert job.input_artifact_hashes == kwargs["input_artifact_hashes"]
    assert job.provider_job_id in service.provider_operations.repository.jobs
    assert execution.queue_depth_at_start == 1


def test_checkpoint_uploads_artifact_and_persists_progress_receipt():
    service = _service()
    kwargs = _job_kwargs(service)
    job = service.queue_comfy_gpu_worker_job(**kwargs)
    service.start_gpu_worker(job.gpu_worker_job_id, actor_id=kwargs["actor_id"])

    checkpoint = service.record_worker_checkpoint(
        gpu_worker_job_id=job.gpu_worker_job_id,
        actor_id=kwargs["actor_id"],
        output_artifact_uri="object://provider-raw/comfy/output-1.png",
        output_artifact_hash="sha256-output-1",
        completed_step="asset_1_rendered",
        cost_so_far=0.33,
    )

    updated = service.repository.jobs[job.gpu_worker_job_id]
    receipt = next(item for item in service.repository.receipts.values() if item.decision_code == "WORKER_CHECKPOINT_RECORDED")
    assert checkpoint.uploaded is True
    assert checkpoint.checkpoint_id in updated.completed_checkpoint_ids
    assert receipt.output_artifact_hashes == ["sha256-output-1"]


def test_queue_drain_shutdown_writes_cost_report_and_shutdown_receipt():
    service = _service()
    kwargs = _job_kwargs(service)
    job = service.queue_comfy_gpu_worker_job(**kwargs)
    service.start_gpu_worker(job.gpu_worker_job_id, actor_id=kwargs["actor_id"])
    for index in [1, 2]:
        service.record_worker_checkpoint(
            gpu_worker_job_id=job.gpu_worker_job_id,
            actor_id=kwargs["actor_id"],
            output_artifact_uri=f"object://provider-raw/comfy/output-{index}.png",
            output_artifact_hash=f"sha256-output-{index}",
            completed_step=f"asset_{index}_rendered",
        )

    report = service.shutdown_gpu_worker(job.gpu_worker_job_id, actor_id=kwargs["actor_id"], instance_seconds=1800)

    shutdown_receipt = next(item for item in service.repository.receipts.values() if item.decision_code == "GPU_WORKER_SHUTDOWN")
    assert service.repository.jobs[job.gpu_worker_job_id].status == GpuWorkerStatus.shutdown
    assert report.cost_amount > 0
    assert shutdown_receipt.shutdown_state == "queue_drained_shutdown"
    assert shutdown_receipt.output_artifact_hashes == ["sha256-output-1", "sha256-output-2"]


def test_interruption_recovery_preserves_outputs_and_requeues_incomplete_job():
    service = _service()
    kwargs = _job_kwargs(service)
    job = service.queue_comfy_gpu_worker_job(**kwargs)
    service.start_gpu_worker(job.gpu_worker_job_id, actor_id=kwargs["actor_id"])
    checkpoint = service.record_worker_checkpoint(
        gpu_worker_job_id=job.gpu_worker_job_id,
        actor_id=kwargs["actor_id"],
        output_artifact_uri="object://provider-raw/comfy/output-1.png",
        output_artifact_hash="sha256-output-1",
        completed_step="asset_1_rendered",
    )

    requeued = service.requeue_incomplete_gpu_job(job.gpu_worker_job_id, actor_id=kwargs["actor_id"])

    assert requeued.requeued_from_gpu_worker_job_id == job.gpu_worker_job_id
    assert requeued.preserved_checkpoint_ids == [checkpoint.checkpoint_id]
    assert service.repository.checkpoints[checkpoint.checkpoint_id].output_artifact_hash == "sha256-output-1"
    assert service.repository.jobs[job.gpu_worker_job_id].status == GpuWorkerStatus.requeued


def test_unapproved_template_is_blocked_before_provider_job_creation():
    service = _service()
    kwargs = _job_kwargs(service)
    kwargs["workflow_hash"] = "sha256-mutated-runtime-graph"

    with pytest.raises(ComfyGpuWorkerError) as exc:
        service.queue_comfy_gpu_worker_job(**kwargs)

    assert exc.value.code == "UNAPPROVED_COMFY_WORKFLOW"
    assert not service.provider_operations.repository.jobs
    assert list(service.repository.receipts.values())[-1].decision_code == "UNAPPROVED_COMFY_WORKFLOW_BLOCKED"


def test_gpu_policy_accepts_only_aws_or_google_cloud_24gb_or_32gb_pinned_docker():
    service = _service()
    kwargs = _job_kwargs(service)
    kwargs["gpu_tier"] = "16gb_vram"

    with pytest.raises(ValueError):
        service.queue_comfy_gpu_worker_job(**kwargs)

    kwargs = _job_kwargs(service)
    kwargs["cloud_provider"] = "running_service"
    with pytest.raises(ValueError):
        service.queue_comfy_gpu_worker_job(**kwargs)

    kwargs = _job_kwargs(service)
    kwargs["docker_image_digest"] = "latest"
    with pytest.raises(ValueError):
        service.queue_comfy_gpu_worker_job(**kwargs)


def test_workflow_and_command_bus_queue_and_checkpoint_gpu_worker():
    service = _service()
    kwargs = _job_kwargs(service)
    workflow = ProviderJobWorkflow(service.provider_operations, comfy_gpu_worker_service=service)

    job = workflow.stage11_comfy_gpu_worker(**kwargs)

    assert job.gpu_worker_job_id in service.repository.jobs

    bus = create_in_memory_command_bus()
    bus.brands.add_scope(kwargs["organization_id"], kwargs["brand_id"])
    register_comfy_gpu_worker_command_handlers(bus, service)
    actor = ActorContext(actor_id=kwargs["actor_id"], actor_type=ActorType.human, role_ids=["production_steward"])
    start = new_command_envelope(
        command_type="StartGpuWorkerCommand",
        organization_id=kwargs["organization_id"],
        brand_id=kwargs["brand_id"],
        actor=actor,
        payload={"gpu_worker_job_id": str(job.gpu_worker_job_id)},
    )

    result = bus.submit(start)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["gpu_worker_job_id"] == str(job.gpu_worker_job_id)
    assert bus.event_outbox.events[-1].event_type == "StartGpuWorkerCommand.succeeded"
