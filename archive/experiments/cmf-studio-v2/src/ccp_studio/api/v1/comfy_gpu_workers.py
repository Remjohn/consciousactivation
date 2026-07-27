"""FastAPI adapter for TS-CMF-045 ComfyUI GPU workers."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.comfy_gpu_worker import ComfyWorkflowExecution, GpuCostReport, GpuWorkerJob, WorkerCheckpoint
from ccp_studio.services.comfy_gpu_worker_service import ComfyGpuWorkerService


router = APIRouter(prefix="/api/v1/comfy-gpu-workers", tags=["comfy-gpu-workers"])
_comfy_gpu_worker_service: ComfyGpuWorkerService | None = None


class QueueComfyGpuWorkerJobRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    actor_id: UUID
    workflow_asset_id: UUID
    workflow_hash: str
    input_artifact_hashes: list[str]
    typed_parameters: dict[str, Any] = Field(default_factory=dict)
    cloud_provider: str
    gpu_tier: str
    docker_image_digest: str
    expected_output_count: int = 1


class RecordCheckpointRequest(BaseModel):
    actor_id: UUID
    output_artifact_uri: str
    output_artifact_hash: str
    completed_step: str
    cost_so_far: float | None = None


class ShutdownGpuWorkerRequest(BaseModel):
    actor_id: UUID
    instance_seconds: float


def set_comfy_gpu_worker_service(service: ComfyGpuWorkerService) -> None:
    global _comfy_gpu_worker_service
    _comfy_gpu_worker_service = service


def get_comfy_gpu_worker_service() -> ComfyGpuWorkerService:
    if _comfy_gpu_worker_service is None:
        raise RuntimeError("ComfyGpuWorkerService must be configured by the application.")
    return _comfy_gpu_worker_service


@router.post("", response_model=GpuWorkerJob)
def queue_comfy_gpu_worker_job(
    request: QueueComfyGpuWorkerJobRequest,
    service: ComfyGpuWorkerService = Depends(get_comfy_gpu_worker_service),
) -> GpuWorkerJob:
    return service.queue_comfy_gpu_worker_job(**request.model_dump())


@router.post("/{gpu_worker_job_id}/start", response_model=ComfyWorkflowExecution)
def start_gpu_worker(
    gpu_worker_job_id: UUID,
    actor_id: UUID,
    service: ComfyGpuWorkerService = Depends(get_comfy_gpu_worker_service),
) -> ComfyWorkflowExecution:
    return service.start_gpu_worker(gpu_worker_job_id, actor_id=actor_id)


@router.post("/{gpu_worker_job_id}/checkpoints", response_model=WorkerCheckpoint)
def record_checkpoint(
    gpu_worker_job_id: UUID,
    request: RecordCheckpointRequest,
    service: ComfyGpuWorkerService = Depends(get_comfy_gpu_worker_service),
) -> WorkerCheckpoint:
    return service.record_worker_checkpoint(gpu_worker_job_id=gpu_worker_job_id, **request.model_dump())


@router.post("/{gpu_worker_job_id}/shutdown", response_model=GpuCostReport)
def shutdown_gpu_worker(
    gpu_worker_job_id: UUID,
    request: ShutdownGpuWorkerRequest,
    service: ComfyGpuWorkerService = Depends(get_comfy_gpu_worker_service),
) -> GpuCostReport:
    return service.shutdown_gpu_worker(gpu_worker_job_id, actor_id=request.actor_id, instance_seconds=request.instance_seconds)
