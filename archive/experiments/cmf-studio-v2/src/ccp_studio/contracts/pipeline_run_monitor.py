from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class PipelineRunStatusReadModel(BaseModel):
    pipeline_run_id: str
    orchestration_run_id: str | None = None
    golden_path_run_id: str | None = None
    recipe_id: str
    recipe_version: str
    brand_context_version_id: str
    workspace_id: str | None = None
    status: str
    started_at: str | None = None
    completed_at: str | None = None
    current_step_id: str | None = None
    progress_percent: int = 0
    source_mode: str = "synthetic"
    blocker_count: int = 0
    pending_approval_count: int = 0


class PipelineBlockerReadModel(BaseModel):
    blocker_id: str
    code: str
    message: str
    severity: str
    step_id: str | None = None
    recoverable: bool = True


class PipelineStageReceiptReadModel(BaseModel):
    step_id: str
    step_name: str
    step_kind: str
    status: str
    pass_status: str
    receipt_id: str | None = None
    orchestration_stage_execution_id: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    message: str | None = None
    blockers: list[PipelineBlockerReadModel] = Field(default_factory=list)


class PipelineArtifactReadModel(BaseModel):
    artifact_id: str
    artifact_ref_id: str | None = None
    pipeline_artifact_ref_id: str | None = None
    role: str
    uri: str
    storage_state: str
    sha256: str | None = None
    source_ref_ids: list[str] = Field(default_factory=list)
    linked_preview_type: str = "none"
    linked_preview_url: str | None = None
    raw_bytes_included: bool = False


class PipelineApprovalReadModel(BaseModel):
    gate_id: str
    gate_type: str
    required: bool
    status: str
    approved_by: str | None = None
    pending_reason: str | None = None
    blockers: list[PipelineBlockerReadModel] = Field(default_factory=list)
    required_sample_types: list[str] = Field(default_factory=list)
    approved_sample_types: list[str] = Field(default_factory=list)


class PipelineSceneOutputLinkReadModel(BaseModel):
    scene_id: str
    step_id: str
    template_preview_url: str | None = None
    video_preview_url: str | None = None
    artifact_refs: list[str] = Field(default_factory=list)
    status: str = "preview_available"


class PipelineRunMonitorReadModel(BaseModel):
    schema_version: str = "cmf.pipeline_run_monitor.v1"
    run_status: PipelineRunStatusReadModel
    stage_receipts: list[PipelineStageReceiptReadModel] = Field(default_factory=list)
    artifacts: list[PipelineArtifactReadModel] = Field(default_factory=list)
    blockers: list[PipelineBlockerReadModel] = Field(default_factory=list)
    approvals: list[PipelineApprovalReadModel] = Field(default_factory=list)
    scene_output_links: list[PipelineSceneOutputLinkReadModel] = Field(default_factory=list)
    summary: dict[str, Any] | None = None
    provider_calls_executed: bool = False
    renderer_calls_executed: bool = False
    local_worker_jobs_executed: bool = False
    created_at: str = Field(default_factory=_now_iso)


class GoldenPathRunDetailReadModel(BaseModel):
    schema_version: str = "cmf.golden_path_run_detail.v1"
    golden_path_run_id: str
    pipeline_run_id: str | None = None
    orchestration_run_id: str | None = None
    brand_context_version_id: str
    recipe_id: str = "format02_golden_path"
    input_fixture_refs: list[str] = Field(default_factory=list)
    narrative_outputs: list[dict[str, Any]] = Field(default_factory=list)
    format_outputs: list[dict[str, Any]] = Field(default_factory=list)
    composition_scene_outputs: list[dict[str, Any]] = Field(default_factory=list)
    avatar_outputs: list[dict[str, Any]] = Field(default_factory=list)
    timeline_outputs: list[dict[str, Any]] = Field(default_factory=list)
    render_outputs: list[dict[str, Any]] = Field(default_factory=list)
    approval_outputs: list[dict[str, Any]] = Field(default_factory=list)
    scene_output_links: list[PipelineSceneOutputLinkReadModel] = Field(default_factory=list)
    receipts: list[dict[str, Any]] = Field(default_factory=list)
    blockers: list[PipelineBlockerReadModel] = Field(default_factory=list)
    approvals: list[PipelineApprovalReadModel] = Field(default_factory=list)
    source_mode: str = "synthetic"
    provider_calls_executed: bool = False
    renderer_calls_executed: bool = False
    local_worker_jobs_executed: bool = False
    created_at: str = Field(default_factory=_now_iso)
