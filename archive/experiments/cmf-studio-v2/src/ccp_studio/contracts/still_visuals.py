"""Still visual parent program contracts for TS-CMF-133 and TS-CMF-135."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.asset_program_compilers import compiler_hash
from ccp_studio.contracts.composition_runtime import ApprovalStatus, CompositionDecision
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.supervisual_grammar import SuperVisualSubtype


StillVisualFormatFamily = Literal["carousel", "supervisual", "visual_poll", "tweet_quote", "meme", "reaction_still"]
StillVisualStageCode = Literal["request", "route", "materialize", "render", "evaluate", "review", "approval", "export"]
StillVisualStageStatus = Literal["pending", "ready", "completed", "blocked", "waived"]


class StillVisualCompositionRequest(BaseModel):
    schema_version: Literal["cmf.still_visual_composition_request.v1"] = "cmf.still_visual_composition_request.v1"
    still_visual_composition_request_id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    brand_context_version_ref: str = Field(min_length=1)
    source_evidence_refs: list[str] = Field(min_length=1)
    target_format_family: StillVisualFormatFamily
    package_slot: str = Field(min_length=1)
    content_sequence_program_ref: str | None = None
    platform: Literal["instagram", "linkedin", "youtube_shorts", "x"] = "instagram"


class StillVisualStageState(BaseModel):
    schema_version: Literal["cmf.still_visual_stage_state.v1"] = "cmf.still_visual_stage_state.v1"
    stage_code: StillVisualStageCode
    status: StillVisualStageStatus
    artifact_refs: list[str] = Field(default_factory=list)
    receipt_refs: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=utc_now)


class StillVisualFamilyRoute(BaseModel):
    schema_version: Literal["cmf.still_visual_family_route.v1"] = "cmf.still_visual_family_route.v1"
    still_visual_family_route_id: UUID = Field(default_factory=uuid4)
    program_id: UUID
    selected_family: StillVisualFormatFamily
    selected_builder_ref: str = Field(min_length=1)
    atlas_binding_ref: str = Field(min_length=1)
    grammar_binding_ref: str | None = None
    primitive_validation_ids: list[str] = Field(min_length=3)
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class ProviderMaterializationPlan(BaseModel):
    schema_version: Literal["cmf.provider_materialization_plan.v1"] = "cmf.provider_materialization_plan.v1"
    provider_materialization_plan_id: UUID = Field(default_factory=uuid4)
    program_id: UUID
    provider_job_refs: list[str] = Field(min_length=1)
    layer_materialization_refs: list[str] = Field(min_length=1)
    final_authority: Literal["cmf_skia_renderer"] = "cmf_skia_renderer"
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)


class StillVisualRenderManifest(BaseModel):
    schema_version: Literal["cmf.still_visual_render_manifest.v1"] = "cmf.still_visual_render_manifest.v1"
    still_visual_render_manifest_id: UUID = Field(default_factory=uuid4)
    program_id: UUID
    skia_scene_ref: str = Field(min_length=1)
    runtime_lock_ref: str = Field(min_length=1)
    render_ref: str = Field(min_length=1)
    render_hash: str = Field(min_length=12)
    deterministic_replay_required: bool = True


class StillVisualEvalSummary(BaseModel):
    schema_version: Literal["cmf.still_visual_eval_summary.v1"] = "cmf.still_visual_eval_summary.v1"
    still_visual_eval_summary_id: UUID = Field(default_factory=uuid4)
    program_id: UUID
    primitive_score: float = Field(ge=0, le=1)
    doctrine_score: float = Field(ge=0, le=1)
    grammar_score: float = Field(ge=0, le=1)
    source_truth_score: float = Field(ge=0, le=1)
    platform_fit_score: float = Field(ge=0, le=1)
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    receipt_refs: list[str] = Field(default_factory=list)


class StillVisualCompositionProgram(BaseModel):
    schema_version: Literal["cmf.still_visual_composition_program.v1"] = "cmf.still_visual_composition_program.v1"
    still_visual_composition_program_id: UUID = Field(default_factory=uuid4)
    request: StillVisualCompositionRequest
    manifest_snapshot_ref: str = Field(min_length=1)
    stage_states: list[StillVisualStageState] = Field(min_length=1)
    family_route: StillVisualFamilyRoute | None = None
    provider_plan: ProviderMaterializationPlan | None = None
    render_manifest: StillVisualRenderManifest | None = None
    eval_summary: StillVisualEvalSummary | None = None
    approval_status: ApprovalStatus = ApprovalStatus.draft
    blocker_codes: list[str] = Field(default_factory=list)
    program_hash: str = Field(min_length=12)
    created_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def _source_backed(self) -> "StillVisualCompositionProgram":
        if not self.request.source_evidence_refs:
            raise ValueError("still visual programs require source evidence")
        return self


class StillVisualReviewReadModel(BaseModel):
    schema_version: Literal["cmf.still_visual_review_read_model.v1"] = "cmf.still_visual_review_read_model.v1"
    still_visual_review_read_model_id: UUID = Field(default_factory=uuid4)
    program_id: UUID
    approval_status: ApprovalStatus
    stage_states: list[StillVisualStageState]
    preview_refs: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    repair_commands: list[str] = Field(default_factory=list)
    approval_eligible: bool = False
    updated_at: datetime = Field(default_factory=utc_now)


class TelegramStillVisualReviewCard(BaseModel):
    schema_version: Literal["cmf.telegram_still_visual_review_card.v1"] = "cmf.telegram_still_visual_review_card.v1"
    telegram_still_visual_review_card_id: UUID = Field(default_factory=uuid4)
    program_id: UUID
    title: str = Field(min_length=1)
    preview_ref: str = Field(min_length=1)
    blocker_count: int = Field(ge=0)
    commands: list[str] = Field(min_length=1)


class StillVisualApprovalReceipt(BaseModel):
    schema_version: Literal["cmf.still_visual_approval_receipt.v1"] = "cmf.still_visual_approval_receipt.v1"
    still_visual_approval_receipt_id: UUID = Field(default_factory=uuid4)
    program_id: UUID
    operator_id: UUID
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class StillVisualRevisionCommand(BaseModel):
    schema_version: Literal["cmf.still_visual_revision_command.v1"] = "cmf.still_visual_revision_command.v1"
    still_visual_revision_command_id: UUID = Field(default_factory=uuid4)
    program_id: UUID
    revision_scope: Literal["route", "provider", "layer", "text", "primitive", "render", "export"]
    reason: str = Field(min_length=1)
    command_ref: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=utc_now)


class StillVisualExportManifest(BaseModel):
    schema_version: Literal["cmf.still_visual_export_manifest.v1"] = "cmf.still_visual_export_manifest.v1"
    still_visual_export_manifest_id: UUID = Field(default_factory=uuid4)
    program_id: UUID
    exported_asset_refs: list[str] = Field(min_length=1)
    package_handoff_ref: str = Field(min_length=1)
    approval_receipt_ref: str = Field(min_length=1)
    written_at: datetime = Field(default_factory=utc_now)


def still_visual_hash(parts: Any) -> str:
    return compiler_hash(parts)
