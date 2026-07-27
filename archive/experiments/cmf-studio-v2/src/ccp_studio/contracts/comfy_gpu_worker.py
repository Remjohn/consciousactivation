"""Self-hosted ComfyUI Docker GPU worker contracts for TS-CMF-045."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class GpuWorkerStatus(str, Enum):
    queued = "queued"
    starting = "starting"
    running = "running"
    draining = "draining"
    shutdown = "shutdown"
    failed = "failed"
    requeued = "requeued"
    blocked = "blocked"


class CloudProvider(str, Enum):
    aws = "aws"
    google_cloud = "google_cloud"


class GpuTier(str, Enum):
    vram_24gb = "24gb_vram"
    vram_32gb = "32gb_vram"


class ComfyWorkflowAsset(BaseModel):
    schema_version: Literal["cmf.comfy_workflow_asset.v1"]
    workflow_asset_id: UUID
    name: str = Field(min_length=1)
    workflow_hash: str = Field(min_length=1)
    template_uri: str = Field(min_length=1)
    migrated_from_legacy_template: str = Field(min_length=1)
    approved: bool
    approved_at: datetime


class GpuWorkerJob(BaseModel):
    schema_version: Literal["cmf.gpu_worker_job.v1"]
    gpu_worker_job_id: UUID
    provider_job_id: UUID
    organization_id: UUID
    brand_id: UUID
    actor_id: UUID
    cloud_provider: CloudProvider
    gpu_tier: GpuTier
    docker_image_digest: str = Field(min_length=1)
    workflow_asset_id: UUID
    workflow_hash: str = Field(min_length=1)
    input_artifact_hashes: list[str] = Field(min_length=1)
    typed_parameters: dict[str, Any] = Field(default_factory=dict)
    queue_position: int | None = None
    expected_output_count: int = Field(ge=1)
    completed_checkpoint_ids: list[UUID] = Field(default_factory=list)
    requeued_from_gpu_worker_job_id: UUID | None = None
    preserved_checkpoint_ids: list[UUID] = Field(default_factory=list)
    status: GpuWorkerStatus
    queued_at: datetime
    updated_at: datetime

    @model_validator(mode="after")
    def docker_digest_should_be_pinned(self):
        if not self.docker_image_digest.startswith("sha256:"):
            raise ValueError("docker_image_digest must be pinned with sha256:")
        return self


class ComfyWorkflowExecution(BaseModel):
    schema_version: Literal["cmf.comfy_workflow_execution.v1"]
    comfy_workflow_execution_id: UUID
    gpu_worker_job_id: UUID
    queue_depth_at_start: int
    started_at: datetime
    completed_at: datetime | None = None
    status: GpuWorkerStatus
    executed_step_count: int = Field(ge=0)


class WorkerCheckpoint(BaseModel):
    schema_version: Literal["cmf.worker_checkpoint.v1"]
    checkpoint_id: UUID
    gpu_worker_job_id: UUID
    output_artifact_uri: str = Field(min_length=1)
    output_artifact_hash: str = Field(min_length=1)
    completed_step: str = Field(min_length=1)
    uploaded: bool
    cost_so_far: float | None = Field(default=None, ge=0)
    recorded_at: datetime


class GpuCostReport(BaseModel):
    schema_version: Literal["cmf.gpu_cost_report.v1"]
    gpu_cost_report_id: UUID
    gpu_worker_job_id: UUID
    cloud_provider: CloudProvider
    gpu_tier: GpuTier
    instance_seconds: float = Field(ge=0)
    cost_amount: float = Field(ge=0)
    queue_depth_at_start: int = Field(ge=0)
    shutdown_at: datetime


class GpuWorkerReceipt(BaseModel):
    schema_version: Literal["cmf.gpu_worker_receipt.v1"]
    gpu_worker_receipt_id: UUID
    gpu_worker_job_id: UUID | None = None
    provider_job_id: UUID | None = None
    workflow_asset_id: UUID | None = None
    workflow_hash: str | None = None
    cloud_provider: CloudProvider | None = None
    gpu_tier: GpuTier | None = None
    docker_image_digest: str | None = None
    input_artifact_hashes: list[str] = Field(default_factory=list)
    checkpoint_ids: list[UUID] = Field(default_factory=list)
    output_artifact_hashes: list[str] = Field(default_factory=list)
    gpu_cost_report_id: UUID | None = None
    cost_amount: float | None = Field(default=None, ge=0)
    status: GpuWorkerStatus
    shutdown_state: str | None = None
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    actor_id: UUID
    command_id: UUID | None = None
    written_at: datetime


def comfy_worker_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_gpu_worker_receipt(
    *,
    actor_id: UUID,
    status: GpuWorkerStatus,
    decision_code: str,
    evidence_refs: list[str],
    gpu_worker_job_id: UUID | None = None,
    provider_job_id: UUID | None = None,
    workflow_asset_id: UUID | None = None,
    workflow_hash: str | None = None,
    cloud_provider: CloudProvider | None = None,
    gpu_tier: GpuTier | None = None,
    docker_image_digest: str | None = None,
    input_artifact_hashes: list[str] | None = None,
    checkpoint_ids: list[UUID] | None = None,
    output_artifact_hashes: list[str] | None = None,
    gpu_cost_report_id: UUID | None = None,
    cost_amount: float | None = None,
    shutdown_state: str | None = None,
    command_id: UUID | None = None,
) -> GpuWorkerReceipt:
    return GpuWorkerReceipt(
        schema_version="cmf.gpu_worker_receipt.v1",
        gpu_worker_receipt_id=uuid4(),
        gpu_worker_job_id=gpu_worker_job_id,
        provider_job_id=provider_job_id,
        workflow_asset_id=workflow_asset_id,
        workflow_hash=workflow_hash,
        cloud_provider=cloud_provider,
        gpu_tier=gpu_tier,
        docker_image_digest=docker_image_digest,
        input_artifact_hashes=input_artifact_hashes or [],
        checkpoint_ids=checkpoint_ids or [],
        output_artifact_hashes=output_artifact_hashes or [],
        gpu_cost_report_id=gpu_cost_report_id,
        cost_amount=cost_amount,
        status=status,
        shutdown_state=shutdown_state,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        actor_id=actor_id,
        command_id=command_id,
        written_at=utc_now(),
    )
