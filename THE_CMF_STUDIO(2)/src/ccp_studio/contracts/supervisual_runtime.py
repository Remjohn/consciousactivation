from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def reject_delivery_frame_profile(frame_profile: str) -> None:
    if frame_profile.startswith("16:9"):
        raise ValueError("16:9 is source-only and cannot be used as a SuperVisual delivery frame profile")


class SuperVisualProjectStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    APPROVED = "approved"
    EXPORTED = "exported"
    ARCHIVED = "archived"
    FAILED = "failed"


class SuperVisualVariantStatus(str, Enum):
    DRAFT = "draft"
    CONTEXT_READY = "context_ready"
    PREPRODUCTION_READY = "preproduction_ready"
    REFERENCE_BOARD_READY = "reference_board_ready"
    COMPOSITION_OPTIONS_READY = "composition_options_ready"
    COMPOSITION_LOCKED = "composition_locked"
    MATERIALIZATION_PLANNED = "materialization_planned"
    ASSETS_MATERIALIZED = "assets_materialized"
    RENDER_READY = "render_ready"
    RENDERED = "rendered"
    EVALUATED = "evaluated"
    REVISION_REQUIRED = "revision_required"
    APPROVAL_READY = "approval_ready"
    APPROVED = "approved"
    EXPORTED = "exported"
    ARCHIVED = "archived"
    FAILED = "failed"


class BuildRunStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepRunStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    SKIPPED = "skipped"


class CommandStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    DUPLICATE = "duplicate"


class SuperVisualRunMode(str, Enum):
    FULL_BUILD = "full_build"
    RESUME = "resume"
    SINGLE_STEP = "single_step"
    REVISION = "revision"
    RENDER_ONLY = "render_only"
    EVAL_ONLY = "eval_only"
    EXPORT_ONLY = "export_only"


class SuperVisualBlocker(BaseModel):
    blocker_id: str = Field(default_factory=lambda: new_id("sv_blocker"))
    code: str
    message: str
    severity: str = "blocking"
    repair_action: str | None = None


class SuperVisualLineage(BaseModel):
    source_context_refs: list[str] = Field(default_factory=list)
    primitive_coalition_contract_id: str | None = None
    visual_preproduction_packet_id: str | None = None
    asset_reference_board_id: str | None = None
    style_route_decision_id: str | None = None
    route_production_spec_ids: list[str] = Field(default_factory=list)
    provider_job_blueprint_ids: list[str] = Field(default_factory=list)
    provider_job_receipt_ids: list[str] = Field(default_factory=list)
    composition_decision_receipt_id: str | None = None
    layer_plan_id: str | None = None
    render_contract_id: str | None = None
    render_receipt_id: str | None = None
    evaluation_receipt_id: str | None = None
    approval_receipt_id: str | None = None
    export_pack_id: str | None = None


class SuperVisualProject(BaseModel):
    supervisual_project_id: str = Field(default_factory=lambda: new_id("sv_project"))
    brand_id: str
    brand_context_version_id: str
    title: str
    source_context_refs: list[str] = Field(default_factory=list)
    target_platforms: list[str] = Field(default_factory=list)
    default_frame_profile: str = "1:1_SOFT_ROUNDED_EDITORIAL"
    status: SuperVisualProjectStatus = SuperVisualProjectStatus.DRAFT
    current_variant_id: str | None = None
    created_by_actor_id: str | None = None
    created_at: str = Field(default_factory=_now_iso)
    updated_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_id:
            raise ValueError("SuperVisualProject.brand_id is required")
        if not self.brand_context_version_id:
            raise ValueError("SuperVisualProject.brand_context_version_id is required")
        reject_delivery_frame_profile(self.default_frame_profile)


class SuperVisualVariant(BaseModel):
    supervisual_variant_id: str = Field(default_factory=lambda: new_id("sv_variant"))
    supervisual_project_id: str
    brand_id: str
    brand_context_version_id: str
    variant_label: str = "Variant A"
    frame_profile: str = "1:1_SOFT_ROUNDED_EDITORIAL"
    status: SuperVisualVariantStatus = SuperVisualVariantStatus.DRAFT
    lineage: SuperVisualLineage = Field(default_factory=SuperVisualLineage)
    current_snapshot_id: str | None = None
    approval_status: str = "not_ready"
    created_at: str = Field(default_factory=_now_iso)
    updated_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("SuperVisualVariant.brand_context_version_id is required")
        reject_delivery_frame_profile(self.frame_profile)


class SuperVisualSnapshot(BaseModel):
    supervisual_snapshot_id: str = Field(default_factory=lambda: new_id("sv_snapshot"))
    supervisual_project_id: str
    supervisual_variant_id: str
    brand_id: str
    brand_context_version_id: str
    status: SuperVisualVariantStatus
    step: str
    preview_ref: str | None = None
    display_payload: dict[str, Any] = Field(default_factory=dict)
    blockers: list[SuperVisualBlocker] = Field(default_factory=list)
    available_actions: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)


class SuperVisualBuildRun(BaseModel):
    supervisual_build_run_id: str = Field(default_factory=lambda: new_id("sv_build_run"))
    supervisual_project_id: str
    supervisual_variant_id: str
    brand_id: str
    brand_context_version_id: str
    run_mode: SuperVisualRunMode = SuperVisualRunMode.FULL_BUILD
    requested_steps: list[str] = Field(default_factory=list)
    status: BuildRunStatus = BuildRunStatus.CREATED
    started_at: str = Field(default_factory=_now_iso)
    completed_at: str | None = None
    error_summary: str | None = None


class SuperVisualStepRun(BaseModel):
    supervisual_step_run_id: str = Field(default_factory=lambda: new_id("sv_step_run"))
    supervisual_build_run_id: str
    supervisual_project_id: str
    supervisual_variant_id: str
    brand_id: str
    brand_context_version_id: str
    step_name: str
    status: StepRunStatus = StepRunStatus.CREATED
    input_refs: list[str] = Field(default_factory=list)
    output_refs: list[str] = Field(default_factory=list)
    receipt_refs: list[str] = Field(default_factory=list)
    started_at: str = Field(default_factory=_now_iso)
    completed_at: str | None = None
    error_summary: str | None = None


class SuperVisualEvent(BaseModel):
    supervisual_event_id: str = Field(default_factory=lambda: new_id("sv_event"))
    supervisual_project_id: str
    supervisual_variant_id: str | None = None
    brand_id: str
    brand_context_version_id: str
    event_type: str
    actor_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=_now_iso)


class SuperVisualCommand(BaseModel):
    command_id: str = Field(default_factory=lambda: new_id("sv_command"))
    command_type: str
    target_type: str
    target_id: str
    supervisual_project_id: str | None = None
    supervisual_variant_id: str | None = None
    actor_id: str | None = None
    idempotency_key: str
    payload: dict[str, Any] = Field(default_factory=dict)
    status: CommandStatus = CommandStatus.CREATED
    result_refs: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)
    completed_at: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.idempotency_key:
            raise ValueError("SuperVisualCommand.idempotency_key is required")


class CreateSuperVisualProjectRequest(BaseModel):
    brand_id: str
    brand_context_version_id: str
    title: str
    source_context_refs: list[str] = Field(default_factory=list)
    target_platforms: list[str] = Field(default_factory=lambda: ["instagram"])
    default_frame_profile: str = "1:1_SOFT_ROUNDED_EDITORIAL"
    created_by_actor_id: str | None = None
    actor_id: str | None = None
    create_initial_variant: bool = True
    idempotency_key: str | None = None


class UpdateSuperVisualProjectRequest(BaseModel):
    title: str | None = None
    brand_context_version_id: str | None = None
    source_context_refs: list[str] | None = None
    target_platforms: list[str] | None = None
    default_frame_profile: str | None = None
    actor_id: str | None = None
    idempotency_key: str | None = None


class CreateSuperVisualVariantRequest(BaseModel):
    variant_label: str = "Variant A"
    frame_profile: str | None = None
    clone_from_variant_id: str | None = None
    actor_id: str | None = None
    idempotency_key: str | None = None


class StartSuperVisualBuildRunRequest(BaseModel):
    run_mode: SuperVisualRunMode = SuperVisualRunMode.FULL_BUILD
    requested_steps: list[str] = Field(default_factory=list)
    actor_id: str | None = None
    idempotency_key: str | None = None


class RunSuperVisualStepRequest(BaseModel):
    input_refs: list[str] = Field(default_factory=list)
    output_refs: list[str] = Field(default_factory=list)
    receipt_refs: list[str] = Field(default_factory=list)
    target_status: SuperVisualVariantStatus | None = None
    actor_id: str | None = None
    idempotency_key: str | None = None


class LockSuperVisualCompositionRequest(BaseModel):
    composition_decision_receipt_id: str
    actor_id: str | None = None
    idempotency_key: str


class CreateSuperVisualCompositionHypothesesRequest(BaseModel):
    composition_options: list[dict[str, Any]] = Field(default_factory=list)
    actor_id: str | None = None
    idempotency_key: str | None = None


class RecordProviderBlueprintRequest(BaseModel):
    provider_job_blueprint_id: str
    actor_id: str | None = None
    idempotency_key: str


class RecordReceiptRequest(BaseModel):
    receipt_id: str
    passed: bool = True
    actor_id: str | None = None
    idempotency_key: str | None = None


class SubmitSuperVisualRevisionRequest(BaseModel):
    revision_note: str
    actor_id: str | None = None
    idempotency_key: str


class SuperVisualCommandRequest(BaseModel):
    command_type: str
    target_type: str
    target_id: str
    payload: dict[str, Any] = Field(default_factory=dict)
    actor_id: str | None = None
    idempotency_key: str


class ApproveSuperVisualVariantRequest(BaseModel):
    approval_receipt_id: str
    actor_id: str | None = None
    idempotency_key: str


class ExportSuperVisualVariantRequest(BaseModel):
    export_pack_id: str
    actor_id: str | None = None
    idempotency_key: str


class SuperVisualProjectDetailResponse(BaseModel):
    project: SuperVisualProject
    current_variant: SuperVisualVariant | None = None
    latest_snapshot: SuperVisualSnapshot | None = None
    events: list[SuperVisualEvent] = Field(default_factory=list)
    available_actions: list[str] = Field(default_factory=list)
    blockers: list[SuperVisualBlocker] = Field(default_factory=list)


class SuperVisualVariantDetailResponse(BaseModel):
    variant: SuperVisualVariant
    latest_snapshot: SuperVisualSnapshot | None = None
    events: list[SuperVisualEvent] = Field(default_factory=list)
    available_actions: list[str] = Field(default_factory=list)
    blockers: list[SuperVisualBlocker] = Field(default_factory=list)
