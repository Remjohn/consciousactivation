"""SuperVisual project contracts for operator-driven still visual production."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.composition_runtime import ApprovalStatus, CompositionDecision, RendererTarget
from ccp_studio.contracts.frame_profiles import FrameProfile
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.style_routes import StyleRoute


SuperVisualProjectStatus = Literal["draft", "built", "revision_requested", "approved", "exported", "blocked"]
SuperVisualContextType = Literal["interview_brief_and_transcript", "transcript_only", "manual_context"]
SuperVisualVariantStatus = Literal["draft", "built", "eval_failed", "approved", "exported", "blocked"]
SuperVisualTimelineEventKind = Literal["project_created", "variant_built", "revision_built", "approval_decided", "export_created"]


class SuperVisualContext(BaseModel):
    schema_version: Literal["cmf.supervisual_context.v1"] = "cmf.supervisual_context.v1"
    context_type: SuperVisualContextType = "manual_context"
    workspace_id: UUID
    brand_id: UUID | None = None
    brand_context_version_ref: str = Field(min_length=1)
    interview_brief_ref: str | None = None
    transcript_ref: str | None = None
    source_evidence_refs: list[str] = Field(min_length=1)
    context_payload: dict[str, Any] = Field(default_factory=dict)


class SuperVisualPrimitiveBinding(BaseModel):
    schema_version: Literal["cmf.supervisual_primitive_binding.v1"] = "cmf.supervisual_primitive_binding.v1"
    primitive_coalition_contract_id: str = Field(min_length=1)
    primitive_refs: list[str] = Field(min_length=3)
    evaluation_target_refs: list[str] = Field(min_length=1)
    source_context_refs: dict[str, str] = Field(default_factory=dict)
    binding_hash: str = Field(min_length=12)


class SuperVisualLayerEntry(BaseModel):
    schema_version: Literal["cmf.supervisual_layer_entry.v1"] = "cmf.supervisual_layer_entry.v1"
    layer_id: str = Field(min_length=1)
    role: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)
    z_index: int = Field(ge=0)
    editable: bool = True
    bounds: dict[str, float] = Field(default_factory=dict)
    primitive_ref: str | None = None


class SuperVisualLayerPlan(BaseModel):
    schema_version: Literal["cmf.supervisual_layer_plan.v1"] = "cmf.supervisual_layer_plan.v1"
    layer_plan_id: UUID = Field(default_factory=uuid4)
    frame_profile_code: str = Field(min_length=1)
    editable_fields: list[str] = Field(min_length=1)
    layers: list[SuperVisualLayerEntry] = Field(min_length=1)
    composition_semantics: dict[str, str] = Field(default_factory=dict)


class SuperVisualCompositionReceipt(BaseModel):
    schema_version: Literal["cmf.supervisual_composition_receipt.v1"] = "cmf.supervisual_composition_receipt.v1"
    composition_receipt_id: UUID = Field(default_factory=uuid4)
    composition_id: str = Field(min_length=1)
    composition_json: dict[str, Any] = Field(default_factory=dict)
    source_lineage_refs: list[str] = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    composition_hash: str = Field(min_length=12)
    written_at: datetime = Field(default_factory=utc_now)


class SuperVisualProviderReceipt(BaseModel):
    schema_version: Literal["cmf.supervisual_provider_receipt.v1"] = "cmf.supervisual_provider_receipt.v1"
    provider_code: Literal["ideogram_4", "qwen_layered", "sam3", "skia_renderer"]
    request_hash: str = Field(min_length=12)
    deterministic_seed: str = Field(min_length=12)
    output_ref: str = Field(min_length=1)
    receipt_ref: str = Field(min_length=1)
    status: Literal["completed", "blocked"] = "completed"


class SuperVisualRenderContract(BaseModel):
    schema_version: Literal["cmf.supervisual_render_contract.v1"] = "cmf.supervisual_render_contract.v1"
    render_contract_id: UUID = Field(default_factory=uuid4)
    renderer_target: RendererTarget = "skia"
    runtime_lock_ref: str = Field(min_length=1)
    frame_profile_code: str = Field(min_length=1)
    render_ref: str = Field(min_length=1)
    render_hash: str = Field(min_length=12)
    deterministic_replay_required: bool = True


class SuperVisualEvalReceipt(BaseModel):
    schema_version: Literal["cmf.supervisual_eval_receipt.v1"] = "cmf.supervisual_eval_receipt.v1"
    eval_receipt_id: UUID = Field(default_factory=uuid4)
    target_variant_ref: str = Field(min_length=1)
    primitive_score: float = Field(ge=0, le=1)
    doctrine_score: float = Field(ge=0, le=1)
    source_truth_score: float = Field(ge=0, le=1)
    frame_profile_score: float = Field(ge=0, le=1)
    style_route_score: float = Field(ge=0, le=1)
    minimum_threshold: float = Field(default=0.84, ge=0, le=1)
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    eval_receipt_hash: str = Field(min_length=12)
    written_at: datetime = Field(default_factory=utc_now)


class SuperVisualVariant(BaseModel):
    schema_version: Literal["cmf.supervisual_variant.v1"] = "cmf.supervisual_variant.v1"
    supervisual_variant_id: UUID = Field(default_factory=uuid4)
    project_id: UUID
    revision_number: int = Field(ge=0)
    revision_instruction: str | None = None
    status: SuperVisualVariantStatus
    context: SuperVisualContext
    primitive_binding: SuperVisualPrimitiveBinding
    frame_profile: FrameProfile
    style_route: StyleRoute
    composition_receipt: SuperVisualCompositionReceipt
    layer_plan: SuperVisualLayerPlan
    provider_receipts: list[SuperVisualProviderReceipt] = Field(min_length=1)
    render_contract: SuperVisualRenderContract
    eval_receipt: SuperVisualEvalReceipt
    deterministic_variant_hash: str = Field(min_length=12)
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def _variant_has_required_receipts(self) -> "SuperVisualVariant":
        if len(self.primitive_binding.primitive_refs) < 3:
            raise ValueError("SuperVisual variants require at least three primitive refs")
        if not self.provider_receipts:
            raise ValueError("SuperVisual variants require provider receipts")
        return self


class SuperVisualProject(BaseModel):
    schema_version: Literal["cmf.supervisual_project.v1"] = "cmf.supervisual_project.v1"
    supervisual_project_id: UUID = Field(default_factory=uuid4)
    project_name: str = Field(min_length=1)
    context: SuperVisualContext
    requested_frame_profile_code: str = "4:5_FEED_POSTER"
    requested_style_route_code: str = "GMG_EXPERT_05_EDITORIAL_SCRIBE"
    status: SuperVisualProjectStatus = "draft"
    variant_ids: list[UUID] = Field(default_factory=list)
    active_variant_id: UUID | None = None
    export_artifact_refs: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class SuperVisualApprovalReceipt(BaseModel):
    schema_version: Literal["cmf.supervisual_approval_receipt.v1"] = "cmf.supervisual_approval_receipt.v1"
    supervisual_approval_receipt_id: UUID = Field(default_factory=uuid4)
    project_id: UUID
    variant_id: UUID
    operator_id: UUID
    decision: CompositionDecision
    approval_status: ApprovalStatus
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class SuperVisualExportArtifact(BaseModel):
    schema_version: Literal["cmf.supervisual_export_artifact.v1"] = "cmf.supervisual_export_artifact.v1"
    supervisual_export_artifact_id: UUID = Field(default_factory=uuid4)
    project_id: UUID
    variant_id: UUID
    artifact_ref: str = Field(min_length=1)
    render_ref: str = Field(min_length=1)
    approval_receipt_ref: str = Field(min_length=1)
    stored: bool = True
    written_at: datetime = Field(default_factory=utc_now)


class SuperVisualTimelineEvent(BaseModel):
    schema_version: Literal["cmf.supervisual_timeline_event.v1"] = "cmf.supervisual_timeline_event.v1"
    supervisual_timeline_event_id: UUID = Field(default_factory=uuid4)
    project_id: UUID
    event_kind: SuperVisualTimelineEventKind
    object_ref: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class SuperVisualTimelineReadModel(BaseModel):
    schema_version: Literal["cmf.supervisual_timeline_read_model.v1"] = "cmf.supervisual_timeline_read_model.v1"
    project_id: UUID
    active_variant_id: UUID | None = None
    events: list[SuperVisualTimelineEvent] = Field(default_factory=list)
    variant_refs: list[str] = Field(default_factory=list)
    export_artifact_refs: list[str] = Field(default_factory=list)
    approval_blockers: list[str] = Field(default_factory=list)


def supervisual_hash(parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
