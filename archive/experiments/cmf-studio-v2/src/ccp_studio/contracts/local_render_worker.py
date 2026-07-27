from __future__ import annotations

from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any
from uuid import uuid4
import hashlib

from pydantic import BaseModel, Field


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class WorkerStatus(str, Enum):
    REGISTERED = "registered"
    ONLINE = "online"
    BUSY = "busy"
    DEGRADED = "degraded"
    OFFLINE = "offline"
    UNHEALTHY = "unhealthy"


class CapabilityStatus(str, Enum):
    AVAILABLE = "available"
    DISABLED = "disabled"
    UNTESTED = "untested"
    DEGRADED = "degraded"
    MISSING = "missing"


class RenderJobType(str, Enum):
    TEMPLATE_PREVIEW_RENDER = "template_preview_render"
    AVATAR_STATE_PREVIEW_RENDER = "avatar_state_preview_render"
    PROXY_VIDEO_RENDER = "proxy_video_render"
    FINAL_VIDEO_RENDER = "final_video_render"
    THUMBNAIL_RENDER = "thumbnail_render"
    CAROUSEL_PREVIEW_RENDER = "carousel_preview_render"
    SUPERVISUAL_PREVIEW_RENDER = "supervisual_preview_render"


class RenderJobStatus(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    LEASED = "leased"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RenderResultStatus(str, Enum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class HealthStatus(str, Enum):
    PASS = "pass"
    DEGRADED = "degraded"
    FAIL = "fail"


class LocalRuntimeName(str, Enum):
    PYTHON_FAKE = "python_fake"
    REMOTION = "remotion"
    FFMPEG = "ffmpeg"
    FFPROBE = "ffprobe"
    NODE = "node"


class LocalRenderWorkerCapability(BaseModel):
    local_render_worker_capability_id: str = Field(default_factory=lambda: new_id("worker_capability"))
    capability_id: str
    display_name: str
    runtime_name: LocalRuntimeName
    enabled: bool = False
    tested: bool = False
    status: CapabilityStatus = CapabilityStatus.DISABLED
    version: str | None = None
    executable_path: str | None = None
    supports_job_types: list[RenderJobType] = Field(default_factory=list)
    last_tested_at: str | None = None
    notes: str | None = None

    @property
    def available(self) -> bool:
        return self.enabled and self.tested and self.status == CapabilityStatus.AVAILABLE

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.capability_id:
            raise ValueError("LocalRenderWorkerCapability requires capability_id")
        if self.status == CapabilityStatus.AVAILABLE and (not self.enabled or not self.tested):
            raise ValueError("Capability cannot be available unless enabled and tested")
        if self.enabled and self.tested and self.status == CapabilityStatus.DISABLED:
            raise ValueError("Enabled and tested capability cannot be disabled")


class LocalRenderWorker(BaseModel):
    local_render_worker_id: str = Field(default_factory=lambda: new_id("local_worker"))
    worker_id: str
    machine_id: str
    display_name: str
    status: WorkerStatus = WorkerStatus.REGISTERED
    capabilities: list[LocalRenderWorkerCapability] = Field(default_factory=list)
    workspace_root: str | None = None
    max_concurrent_jobs: int = Field(default=1, ge=1)
    current_job_ids: list[str] = Field(default_factory=list)
    registered_at: str = Field(default_factory=_now_iso)
    last_heartbeat_at: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.worker_id:
            raise ValueError("LocalRenderWorker requires worker_id")
        if not self.machine_id:
            raise ValueError("LocalRenderWorker requires machine_id")
        cap_ids = [cap.capability_id for cap in self.capabilities]
        if len(cap_ids) != len(set(cap_ids)):
            raise ValueError("Worker cannot contain duplicate capability IDs")
        if len(self.current_job_ids) > self.max_concurrent_jobs:
            raise ValueError("Worker current_job_ids exceeds max_concurrent_jobs")

    def supports_job_type(self, job_type: RenderJobType) -> bool:
        return any(cap.available and job_type in cap.supports_job_types for cap in self.capabilities)

    @property
    def healthy_for_leasing(self) -> bool:
        return self.status in {WorkerStatus.ONLINE, WorkerStatus.BUSY} and len(self.current_job_ids) < self.max_concurrent_jobs


class RenderJob(BaseModel):
    render_job_id: str = Field(default_factory=lambda: new_id("render_job"))
    job_type: RenderJobType
    job_name: str
    requested_by: str = "system"
    payload: dict[str, Any] = Field(default_factory=dict)
    required_capability_ids: list[str] = Field(default_factory=list)
    priority: int = Field(default=100, ge=0)
    status: RenderJobStatus = RenderJobStatus.CREATED
    provider_calls_allowed: bool = False
    external_runtime_calls_allowed: bool = False
    fake_execution_only: bool = True
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.job_name:
            raise ValueError("RenderJob requires job_name")
        if self.provider_calls_allowed:
            raise ValueError("Local render jobs cannot allow provider calls")
        if self.external_runtime_calls_allowed:
            raise ValueError("V1 render jobs cannot allow external runtime calls")
        if not self.fake_execution_only:
            raise ValueError("Local Render Worker V1 is fake execution only")
        if self.job_type == RenderJobType.FINAL_VIDEO_RENDER and not self.payload.get("final_timeline_locked", False):
            raise ValueError("Final video render job requires final_timeline_locked=True")


class RenderJobQueue(BaseModel):
    render_job_queue_id: str = Field(default_factory=lambda: new_id("render_queue"))
    queue_name: str = "local_render_queue"
    jobs: list[RenderJob] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        job_ids = [job.render_job_id for job in self.jobs]
        if len(job_ids) != len(set(job_ids)):
            raise ValueError("RenderJobQueue cannot contain duplicate jobs")

    @property
    def queued_jobs(self) -> list[RenderJob]:
        return [job for job in self.jobs if job.status == RenderJobStatus.QUEUED]


class RenderJobLease(BaseModel):
    render_job_lease_id: str = Field(default_factory=lambda: new_id("render_lease"))
    render_job_id: str
    worker_id: str
    lease_token: str = Field(default_factory=lambda: new_id("lease_token"))
    leased_at: str = Field(default_factory=_now_iso)
    expires_at: str
    active: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.render_job_id or not self.worker_id:
            raise ValueError("RenderJobLease requires render_job_id and worker_id")
        if parse_iso(self.expires_at) <= parse_iso(self.leased_at):
            raise ValueError("RenderJobLease expires_at must be after leased_at")


class RenderJobHeartbeat(BaseModel):
    render_job_heartbeat_id: str = Field(default_factory=lambda: new_id("render_heartbeat"))
    worker_id: str
    status: WorkerStatus
    active_job_ids: list[str] = Field(default_factory=list)
    observed_capability_ids: list[str] = Field(default_factory=list)
    free_disk_mb: int | None = Field(default=None, ge=0)
    free_memory_mb: int | None = Field(default=None, ge=0)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.worker_id:
            raise ValueError("RenderJobHeartbeat requires worker_id")
        if self.status == WorkerStatus.OFFLINE and self.active_job_ids:
            raise ValueError("Offline worker cannot report active jobs")


class RenderJobResult(BaseModel):
    render_job_result_id: str = Field(default_factory=lambda: new_id("render_result"))
    render_job_id: str
    worker_id: str
    lease_id: str
    result_status: RenderResultStatus
    output_uri: str | None = None
    output_sha256: str | None = None
    logs_uri: str | None = None
    error_message: str | None = None
    fake_result: bool = True
    provider_calls_executed: bool = False
    external_runtime_calls_executed: bool = False
    completed_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_calls_executed or self.external_runtime_calls_executed:
            raise ValueError("RenderJobResult V1 cannot execute providers or external runtimes")
        if self.result_status == RenderResultStatus.SUCCEEDED:
            if not self.output_uri or not self.output_sha256:
                raise ValueError("Succeeded render result requires output_uri and output_sha256")
        if self.result_status == RenderResultStatus.FAILED and not self.error_message:
            raise ValueError("Failed render result requires error_message")


class RenderWorkerHealthReceipt(BaseModel):
    render_worker_health_receipt_id: str = Field(default_factory=lambda: new_id("worker_health"))
    worker_id: str
    health_status: HealthStatus
    required_capability_ids: list[str] = Field(default_factory=list)
    available_capability_ids: list[str] = Field(default_factory=list)
    missing_capability_ids: list[str] = Field(default_factory=list)
    stale_heartbeat: bool = False
    worker_status: WorkerStatus
    blockers: list[str] = Field(default_factory=list)
    checked_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        blockers = list(self.blockers)
        if self.worker_status in {WorkerStatus.OFFLINE, WorkerStatus.UNHEALTHY}:
            blockers.append("worker_offline_or_unhealthy")
        if self.missing_capability_ids:
            blockers.append("missing_required_capabilities")
        if self.stale_heartbeat:
            blockers.append("stale_heartbeat")
        self.blockers = sorted(set(blockers))
        if self.blockers and self.health_status == HealthStatus.PASS:
            raise ValueError("Worker health cannot pass with blockers")
