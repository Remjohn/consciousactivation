"""Self-hosted ComfyUI Docker GPU worker service for TS-CMF-045."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.comfy_gpu_worker import (
    CloudProvider,
    ComfyWorkflowAsset,
    ComfyWorkflowExecution,
    GpuCostReport,
    GpuTier,
    GpuWorkerJob,
    GpuWorkerReceipt,
    GpuWorkerStatus,
    WorkerCheckpoint,
    comfy_worker_hash,
    new_gpu_worker_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.comfy_gpu_worker import InMemoryComfyGpuWorkerRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.provider_operations_service import ProviderOperationsService


class ComfyGpuWorkerError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


def default_comfy_workflow_assets() -> list[ComfyWorkflowAsset]:
    now = utc_now()
    templates = [
        ("Wan 2.2 i2v.json", "worker-assets/comfyui/wan-2-2-i2v.json"),
        ("qwen-image-layered-image2image.json", "worker-assets/comfyui/qwen-image-layered-image2image.json"),
    ]
    return [
        ComfyWorkflowAsset(
            schema_version="cmf.comfy_workflow_asset.v1",
            workflow_asset_id=uuid4(),
            name=name,
            workflow_hash=comfy_worker_hash({"legacy_template": name, "template_uri": uri, "approved": True}),
            template_uri=uri,
            migrated_from_legacy_template=name,
            approved=True,
            approved_at=now,
        )
        for name, uri in templates
    ]


@dataclass
class ComfyGpuWorkerService:
    provider_operations: ProviderOperationsService
    repository: InMemoryComfyGpuWorkerRepository = field(default_factory=InMemoryComfyGpuWorkerRepository)

    def __post_init__(self) -> None:
        if not self.provider_operations.repository.capabilities:
            self.provider_operations.seed_current_cmf_capabilities()
        if not self.repository.workflow_assets:
            for asset in default_comfy_workflow_assets():
                self.repository.put_workflow_asset(asset)

    def queue_comfy_gpu_worker_job(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        actor_id: UUID,
        workflow_asset_id: UUID,
        workflow_hash: str,
        input_artifact_hashes: list[str],
        typed_parameters: dict[str, Any],
        cloud_provider: CloudProvider | str,
        gpu_tier: GpuTier | str,
        docker_image_digest: str,
        expected_output_count: int,
        command_id: UUID | None = None,
    ) -> GpuWorkerJob:
        cloud = CloudProvider(cloud_provider)
        tier = GpuTier(gpu_tier)
        asset = self._approved_workflow_asset(workflow_asset_id, workflow_hash, actor_id, command_id)
        provider_job = self.provider_operations.submit_provider_job(
            provider_capability_id="comfyui_docker_gpu.render_worker.v1",
            organization_id=organization_id,
            brand_id=brand_id,
            requested_by_actor_id=actor_id,
            input_artifact_hashes=[workflow_hash, *input_artifact_hashes],
            input_types=["workflow_json", "render_contract"],
            parameters={"estimated_cost_amount": 0.0, "cloud_provider": cloud.value, "gpu_tier": tier.value},
            idempotency_key=f"comfy-gpu:{workflow_hash}:{comfy_worker_hash(input_artifact_hashes)}",
            command_id=command_id,
        )
        queue_position = 1 + len([job for job in self.repository.jobs.values() if job.status == GpuWorkerStatus.queued])
        now = utc_now()
        job = self.repository.put_job(
            GpuWorkerJob(
                schema_version="cmf.gpu_worker_job.v1",
                gpu_worker_job_id=uuid4(),
                provider_job_id=provider_job.provider_job_id,
                organization_id=organization_id,
                brand_id=brand_id,
                actor_id=actor_id,
                cloud_provider=cloud,
                gpu_tier=tier,
                docker_image_digest=docker_image_digest,
                workflow_asset_id=asset.workflow_asset_id,
                workflow_hash=asset.workflow_hash,
                input_artifact_hashes=input_artifact_hashes,
                typed_parameters=typed_parameters,
                queue_position=queue_position,
                expected_output_count=expected_output_count,
                status=GpuWorkerStatus.queued,
                queued_at=now,
                updated_at=now,
            )
        )
        self._write_job_receipt(
            job,
            actor_id=actor_id,
            decision_code="COMFY_GPU_WORKER_JOB_QUEUED",
            evidence_refs=[asset.workflow_hash, docker_image_digest],
            command_id=command_id,
        )
        return job

    def start_gpu_worker(self, gpu_worker_job_id: UUID, *, actor_id: UUID, command_id: UUID | None = None) -> ComfyWorkflowExecution:
        job = self._job(gpu_worker_job_id)
        queue_depth = len([item for item in self.repository.jobs.values() if item.status == GpuWorkerStatus.queued])
        job = job.model_copy(update={"status": GpuWorkerStatus.running, "updated_at": utc_now()})
        self.repository.put_job(job)
        execution = self.repository.put_execution(
            ComfyWorkflowExecution(
                schema_version="cmf.comfy_workflow_execution.v1",
                comfy_workflow_execution_id=uuid4(),
                gpu_worker_job_id=job.gpu_worker_job_id,
                queue_depth_at_start=queue_depth,
                started_at=utc_now(),
                status=GpuWorkerStatus.running,
                executed_step_count=0,
            )
        )
        self._write_job_receipt(job, actor_id=actor_id, decision_code="GPU_WORKER_STARTED", evidence_refs=[str(execution.comfy_workflow_execution_id)], command_id=command_id)
        return execution

    def record_worker_checkpoint(
        self,
        *,
        gpu_worker_job_id: UUID,
        actor_id: UUID,
        output_artifact_uri: str,
        output_artifact_hash: str,
        completed_step: str,
        cost_so_far: float | None = None,
        command_id: UUID | None = None,
    ) -> WorkerCheckpoint:
        job = self._job(gpu_worker_job_id)
        if job.status not in {GpuWorkerStatus.running, GpuWorkerStatus.draining}:
            raise ComfyGpuWorkerError("GPU_WORKER_NOT_RUNNING", "Worker checkpoints require a running worker.")
        checkpoint = self.repository.put_checkpoint(
            WorkerCheckpoint(
                schema_version="cmf.worker_checkpoint.v1",
                checkpoint_id=uuid4(),
                gpu_worker_job_id=job.gpu_worker_job_id,
                output_artifact_uri=output_artifact_uri,
                output_artifact_hash=output_artifact_hash,
                completed_step=completed_step,
                uploaded=True,
                cost_so_far=cost_so_far,
                recorded_at=utc_now(),
            )
        )
        job = job.model_copy(
            update={
                "completed_checkpoint_ids": [*job.completed_checkpoint_ids, checkpoint.checkpoint_id],
                "status": GpuWorkerStatus.draining if len(job.completed_checkpoint_ids) + 1 >= job.expected_output_count else GpuWorkerStatus.running,
                "updated_at": utc_now(),
            }
        )
        self.repository.put_job(job)
        self._write_job_receipt(
            job,
            actor_id=actor_id,
            decision_code="WORKER_CHECKPOINT_RECORDED",
            checkpoint_ids=[checkpoint.checkpoint_id],
            output_artifact_hashes=[checkpoint.output_artifact_hash],
            evidence_refs=[checkpoint.output_artifact_uri, checkpoint.output_artifact_hash],
            command_id=command_id,
        )
        return checkpoint

    def shutdown_gpu_worker(
        self,
        gpu_worker_job_id: UUID,
        *,
        actor_id: UUID,
        instance_seconds: float,
        command_id: UUID | None = None,
    ) -> GpuCostReport:
        job = self._job(gpu_worker_job_id)
        if len(job.completed_checkpoint_ids) < job.expected_output_count:
            raise ComfyGpuWorkerError("GPU_QUEUE_NOT_DRAINED", "Worker cannot shut down until expected outputs are checkpointed.")
        execution = self._execution_for_job(job.gpu_worker_job_id)
        rate = 3.20 if job.gpu_tier == GpuTier.vram_24gb else 4.75
        report = self.repository.put_cost_report(
            GpuCostReport(
                schema_version="cmf.gpu_cost_report.v1",
                gpu_cost_report_id=uuid4(),
                gpu_worker_job_id=job.gpu_worker_job_id,
                cloud_provider=job.cloud_provider,
                gpu_tier=job.gpu_tier,
                instance_seconds=instance_seconds,
                cost_amount=round((instance_seconds / 3600) * rate, 4),
                queue_depth_at_start=execution.queue_depth_at_start,
                shutdown_at=utc_now(),
            )
        )
        job = job.model_copy(update={"status": GpuWorkerStatus.shutdown, "updated_at": report.shutdown_at})
        self.repository.put_job(job)
        execution = execution.model_copy(update={"status": GpuWorkerStatus.shutdown, "completed_at": report.shutdown_at, "executed_step_count": len(job.completed_checkpoint_ids)})
        self.repository.put_execution(execution)
        self._write_job_receipt(
            job,
            actor_id=actor_id,
            decision_code="GPU_WORKER_SHUTDOWN",
            gpu_cost_report_id=report.gpu_cost_report_id,
            cost_amount=report.cost_amount,
            shutdown_state="queue_drained_shutdown",
            checkpoint_ids=job.completed_checkpoint_ids,
            output_artifact_hashes=[self.repository.checkpoints[item].output_artifact_hash for item in job.completed_checkpoint_ids],
            evidence_refs=[str(report.gpu_cost_report_id), f"cost:{report.cost_amount}"],
            command_id=command_id,
        )
        return report

    def requeue_incomplete_gpu_job(self, gpu_worker_job_id: UUID, *, actor_id: UUID, command_id: UUID | None = None) -> GpuWorkerJob:
        job = self._job(gpu_worker_job_id)
        if len(job.completed_checkpoint_ids) >= job.expected_output_count:
            raise ComfyGpuWorkerError("GPU_JOB_ALREADY_COMPLETE", "Complete jobs do not need requeue.")
        original = job.model_copy(update={"status": GpuWorkerStatus.requeued, "updated_at": utc_now()})
        self.repository.put_job(original)
        provider_job = self.provider_operations.submit_provider_job(
            provider_capability_id="comfyui_docker_gpu.render_worker.v1",
            organization_id=job.organization_id,
            brand_id=job.brand_id,
            requested_by_actor_id=actor_id,
            input_artifact_hashes=[job.workflow_hash, *job.input_artifact_hashes],
            input_types=["workflow_json", "render_contract"],
            parameters={"estimated_cost_amount": 0.0, "requeued_from": str(job.gpu_worker_job_id)},
            idempotency_key=f"comfy-gpu-requeue:{job.gpu_worker_job_id}:{len(job.completed_checkpoint_ids)}",
            command_id=command_id,
        )
        now = utc_now()
        requeued = self.repository.put_job(
            job.model_copy(
                update={
                    "gpu_worker_job_id": uuid4(),
                    "provider_job_id": provider_job.provider_job_id,
                    "queue_position": 1 + len([item for item in self.repository.jobs.values() if item.status == GpuWorkerStatus.queued]),
                    "completed_checkpoint_ids": [],
                    "requeued_from_gpu_worker_job_id": job.gpu_worker_job_id,
                    "preserved_checkpoint_ids": job.completed_checkpoint_ids,
                    "status": GpuWorkerStatus.queued,
                    "queued_at": now,
                    "updated_at": now,
                }
            )
        )
        self._write_job_receipt(
            requeued,
            actor_id=actor_id,
            decision_code="INCOMPLETE_GPU_JOB_REQUEUED",
            checkpoint_ids=requeued.preserved_checkpoint_ids,
            output_artifact_hashes=[self.repository.checkpoints[item].output_artifact_hash for item in requeued.preserved_checkpoint_ids],
            evidence_refs=["completed_outputs_preserved", str(job.gpu_worker_job_id)],
            command_id=command_id,
        )
        return requeued

    def block_unapproved_comfy_workflow(
        self,
        *,
        workflow_asset_id: UUID,
        workflow_hash: str,
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> GpuWorkerReceipt:
        return self.repository.put_receipt(
            new_gpu_worker_receipt(
                actor_id=actor_id,
                status=GpuWorkerStatus.blocked,
                decision_code="UNAPPROVED_COMFY_WORKFLOW_BLOCKED",
                workflow_asset_id=workflow_asset_id,
                workflow_hash=workflow_hash,
                evidence_refs=["APPROVED_WORKFLOW_ASSET_REQUIRED"],
                command_id=command_id,
            )
        )

    def _approved_workflow_asset(self, workflow_asset_id: UUID, workflow_hash: str, actor_id: UUID, command_id: UUID | None) -> ComfyWorkflowAsset:
        asset = self.repository.workflow_assets.get(workflow_asset_id)
        if asset is None or not asset.approved or asset.workflow_hash != workflow_hash:
            self.block_unapproved_comfy_workflow(
                workflow_asset_id=workflow_asset_id,
                workflow_hash=workflow_hash,
                actor_id=actor_id,
                command_id=command_id,
            )
            raise ComfyGpuWorkerError("UNAPPROVED_COMFY_WORKFLOW", "ComfyUI workflow must be an approved hashed worker asset.")
        return asset

    def _write_job_receipt(
        self,
        job: GpuWorkerJob,
        *,
        actor_id: UUID,
        decision_code: str,
        evidence_refs: list[str],
        checkpoint_ids: list[UUID] | None = None,
        output_artifact_hashes: list[str] | None = None,
        gpu_cost_report_id: UUID | None = None,
        cost_amount: float | None = None,
        shutdown_state: str | None = None,
        command_id: UUID | None = None,
    ) -> GpuWorkerReceipt:
        return self.repository.put_receipt(
            new_gpu_worker_receipt(
                actor_id=actor_id,
                status=job.status,
                decision_code=decision_code,
                gpu_worker_job_id=job.gpu_worker_job_id,
                provider_job_id=job.provider_job_id,
                workflow_asset_id=job.workflow_asset_id,
                workflow_hash=job.workflow_hash,
                cloud_provider=job.cloud_provider,
                gpu_tier=job.gpu_tier,
                docker_image_digest=job.docker_image_digest,
                input_artifact_hashes=job.input_artifact_hashes,
                checkpoint_ids=checkpoint_ids or job.completed_checkpoint_ids,
                output_artifact_hashes=output_artifact_hashes or [],
                gpu_cost_report_id=gpu_cost_report_id,
                cost_amount=cost_amount,
                shutdown_state=shutdown_state,
                evidence_refs=evidence_refs,
                command_id=command_id,
            )
        )

    def _job(self, gpu_worker_job_id: UUID) -> GpuWorkerJob:
        job = self.repository.jobs.get(gpu_worker_job_id)
        if job is None:
            raise ComfyGpuWorkerError("GPU_WORKER_JOB_REQUIRED", "GPU worker job is required.")
        return job

    def _execution_for_job(self, gpu_worker_job_id: UUID) -> ComfyWorkflowExecution:
        execution = next((item for item in self.repository.executions.values() if item.gpu_worker_job_id == gpu_worker_job_id), None)
        if execution is None:
            raise ComfyGpuWorkerError("GPU_WORKER_EXECUTION_REQUIRED", "Worker execution is required.")
        return execution


@dataclass
class ComfyGpuWorkerCommandHandler:
    command_type: str
    service: ComfyGpuWorkerService
    aggregate_type: str = "gpu_worker"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "QueueComfyGpuWorkerJobCommand":
            return self.service.queue_comfy_gpu_worker_job(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                actor_id=envelope.actor.actor_id,
                workflow_asset_id=UUID(payload["workflow_asset_id"]),
                workflow_hash=payload["workflow_hash"],
                input_artifact_hashes=payload["input_artifact_hashes"],
                typed_parameters=payload.get("typed_parameters", {}),
                cloud_provider=payload["cloud_provider"],
                gpu_tier=payload["gpu_tier"],
                docker_image_digest=payload["docker_image_digest"],
                expected_output_count=int(payload.get("expected_output_count", 1)),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "StartGpuWorkerCommand":
            return self.service.start_gpu_worker(
                UUID(payload["gpu_worker_job_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type in {"RecordWorkerCheckpointCommand", "UploadWorkerOutputCommand"}:
            return self.service.record_worker_checkpoint(
                gpu_worker_job_id=UUID(payload["gpu_worker_job_id"]),
                actor_id=envelope.actor.actor_id,
                output_artifact_uri=payload["output_artifact_uri"],
                output_artifact_hash=payload["output_artifact_hash"],
                completed_step=payload["completed_step"],
                cost_so_far=payload.get("cost_so_far"),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "RequeueIncompleteGpuJobCommand":
            return self.service.requeue_incomplete_gpu_job(
                UUID(payload["gpu_worker_job_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "ShutdownGpuWorkerCommand":
            return self.service.shutdown_gpu_worker(
                UUID(payload["gpu_worker_job_id"]),
                actor_id=envelope.actor.actor_id,
                instance_seconds=float(payload["instance_seconds"]),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "BlockUnapprovedComfyWorkflowCommand":
            return self.service.block_unapproved_comfy_workflow(
                workflow_asset_id=UUID(payload["workflow_asset_id"]),
                workflow_hash=payload["workflow_hash"],
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        raise ComfyGpuWorkerError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("gpu_worker_job_id") or payload.get("workflow_asset_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_comfy_gpu_worker_command_handlers(bus: CommandBus, service: ComfyGpuWorkerService) -> None:
    for command_type in [
        "QueueComfyGpuWorkerJobCommand",
        "StartGpuWorkerCommand",
        "RecordWorkerCheckpointCommand",
        "UploadWorkerOutputCommand",
        "RequeueIncompleteGpuJobCommand",
        "ShutdownGpuWorkerCommand",
        "BlockUnapprovedComfyWorkflowCommand",
    ]:
        bus.register_handler(ComfyGpuWorkerCommandHandler(command_type=command_type, service=service))
