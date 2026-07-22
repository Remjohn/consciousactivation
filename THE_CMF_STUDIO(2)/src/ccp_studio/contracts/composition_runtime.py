"""Batch 1 composition runtime contracts for TS-CMF-072 through TS-CMF-092."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


VideoFormatCode = Literal["SV-CSC", "SV-EDU", "SV-FRB", "SV-RRC"]
CompositionDecision = Literal["approved", "blocked", "repair_required"]
RendererTarget = Literal["remotion", "motion_canvas", "skia", "manim", "ffmpeg", "open_timeline_io"]


class ApprovalStatus(str, Enum):
    draft = "draft"
    blocked = "blocked"
    repair_required = "repair_required"
    approved = "approved"


class AdapterDecision(str, Enum):
    approved_adapter = "approved_adapter"
    sandbox_only = "sandbox_only"
    rejected = "rejected"


class SceneTemplateBinding(BaseModel):
    schema_version: Literal["cmf.scene_template_binding.v1"] = "cmf.scene_template_binding.v1"
    scene_template_binding_id: UUID = Field(default_factory=uuid4)
    scene_spec_id: UUID
    reaction_template_route_id: UUID | None = None
    template_code: str = Field(min_length=1)
    content_format_code: str = Field(min_length=1)
    scene_pattern: str = Field(min_length=1)
    renderer_route: str = Field(min_length=1)
    composition_id: str = Field(min_length=1)
    live_clip_slots: list[dict[str, Any]] = Field(min_length=1)
    motion_grammar: dict[str, Any] = Field(default_factory=dict)
    primitive_eval_obligations: list[str] = Field(min_length=1)
    source_lineage_refs: list[str] = Field(min_length=1)
    created_at: datetime = Field(default_factory=utc_now)


class SceneTemplateBindingReceipt(BaseModel):
    schema_version: Literal["cmf.scene_template_binding_receipt.v1"] = "cmf.scene_template_binding_receipt.v1"
    scene_template_binding_receipt_id: UUID = Field(default_factory=uuid4)
    scene_template_binding_id: UUID | None = None
    scene_spec_id: UUID
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    actor_id: UUID
    written_at: datetime = Field(default_factory=utc_now)


class CompositionZone(BaseModel):
    schema_version: Literal["cmf.composition_zone.v1"] = "cmf.composition_zone.v1"
    zone_id: str = Field(min_length=1)
    role: str = Field(min_length=1)
    x: float = Field(ge=0, le=1)
    y: float = Field(ge=0, le=1)
    width: float = Field(gt=0, le=1)
    height: float = Field(gt=0, le=1)
    safe_area: bool = True
    timing_ref: str | None = None

    @model_validator(mode="after")
    def _inside_frame(self) -> "CompositionZone":
        if self.x + self.width > 1.0 or self.y + self.height > 1.0:
            raise ValueError("composition zone must remain inside the normalized frame")
        return self


class CompositionTemplateLayer(BaseModel):
    schema_version: Literal["cmf.composition_template_layer.v1"] = "cmf.composition_template_layer.v1"
    layer_id: str = Field(min_length=1)
    layer_type: str = Field(min_length=1)
    zone_id: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)
    z_index: int = Field(ge=0)
    editable: bool = True
    timing_ref: str | None = None
    style_tokens: list[str] = Field(default_factory=list)


class CompositionTemplateJson(BaseModel):
    schema_version: Literal["cmf.composition_template_json.v1"] = "cmf.composition_template_json.v1"
    composition_template_id: UUID = Field(default_factory=uuid4)
    template_family_code: str = Field(min_length=1)
    content_format_code: str = Field(min_length=1)
    aspect_ratio: str = Field(min_length=1)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    fps: int = Field(gt=0)
    duration_seconds: float = Field(gt=0)
    zones: list[CompositionZone] = Field(min_length=1)
    layers: list[CompositionTemplateLayer] = Field(min_length=1)
    source_lineage_refs: list[str] = Field(min_length=1)
    primitive_validation_ids: list[str] = Field(min_length=3)
    visual_feel_contract_id: UUID | None = None
    preview_asset_refs: list[str] = Field(default_factory=list)
    composition_json_hash: str = Field(min_length=12)
    approval_status: ApprovalStatus = ApprovalStatus.draft

    @model_validator(mode="after")
    def _layers_reference_zones(self) -> "CompositionTemplateJson":
        zone_ids = {zone.zone_id for zone in self.zones}
        missing = [layer.zone_id for layer in self.layers if layer.zone_id not in zone_ids]
        if missing:
            raise ValueError(f"layers reference unknown composition zones: {missing}")
        return self


class CompositionTemplateApprovalReceipt(BaseModel):
    schema_version: Literal["cmf.composition_template_approval_receipt.v1"] = "cmf.composition_template_approval_receipt.v1"
    composition_template_approval_receipt_id: UUID = Field(default_factory=uuid4)
    composition_template_id: UUID
    composition_json_hash: str = Field(min_length=12)
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(min_length=1)
    actor_id: UUID
    written_at: datetime = Field(default_factory=utc_now)


class SubjectCutoutLayer(BaseModel):
    schema_version: Literal["cmf.subject_cutout_layer.v1"] = "cmf.subject_cutout_layer.v1"
    subject_ref: str = Field(min_length=1)
    role: Literal["guest", "interviewer", "guest_reaction", "interviewer_reaction"]
    zone_id: str = Field(min_length=1)
    mask_ref: str = Field(min_length=1)
    background_removed: bool
    eye_line: str = Field(min_length=1)
    upper_body_only: bool = True


class ReactionClipRendererProps(BaseModel):
    schema_version: Literal["cmf.reaction_clip_renderer_props.v1"] = "cmf.reaction_clip_renderer_props.v1"
    composition_template_id: UUID
    content_format_code: str = Field(min_length=1)
    upper_reaction_ui_zone_id: str = Field(min_length=1)
    lower_human_cutout_zone_id: str = Field(min_length=1)
    subject_cutouts: list[SubjectCutoutLayer] = Field(min_length=1)
    beat_cue_refs: list[str] = Field(min_length=1)
    caption_policy: str = Field(min_length=1)
    audio_policy: str = Field(min_length=1)


class ReactionClipRenderManifest(BaseModel):
    schema_version: Literal["cmf.reaction_clip_render_manifest.v1"] = "cmf.reaction_clip_render_manifest.v1"
    render_manifest_id: UUID = Field(default_factory=uuid4)
    renderer_target: RendererTarget = "remotion"
    renderer_props: ReactionClipRendererProps
    frame_size: str = Field(min_length=1)
    deterministic_inputs_hash: str = Field(min_length=12)
    receipts_required: list[str] = Field(min_length=1)
    created_at: datetime = Field(default_factory=utc_now)


class CompositionApprovalBlocker(BaseModel):
    schema_version: Literal["cmf.composition_approval_blocker.v1"] = "cmf.composition_approval_blocker.v1"
    blocker_code: str = Field(min_length=1)
    severity: Literal["soft", "hard"]
    message: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)


class CompositionApprovalReadModel(BaseModel):
    schema_version: Literal["cmf.composition_approval_read_model.v1"] = "cmf.composition_approval_read_model.v1"
    review_read_model_id: UUID = Field(default_factory=uuid4)
    scene_template_binding: SceneTemplateBinding
    composition_template: CompositionTemplateJson
    preview_refs: list[str] = Field(default_factory=list)
    eval_receipt_refs: list[str] = Field(default_factory=list)
    blockers: list[CompositionApprovalBlocker] = Field(default_factory=list)
    approval_status: ApprovalStatus
    operator_commands: list[str] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=utc_now)


class IntegrationCandidate(BaseModel):
    schema_version: Literal["cmf.integration_candidate.v1"] = "cmf.integration_candidate.v1"
    integration_candidate_id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1)
    repo_url: str = Field(min_length=1)
    category: str = Field(min_length=1)
    proposed_use: str = Field(min_length=1)
    license_family: str = Field(min_length=1)
    deterministic_boundary: str = Field(min_length=1)
    production_authority_allowed: bool = False
    evidence_refs: list[str] = Field(default_factory=list)


class IntegrationAdapterDecision(BaseModel):
    schema_version: Literal["cmf.integration_adapter_decision.v1"] = "cmf.integration_adapter_decision.v1"
    integration_adapter_decision_id: UUID = Field(default_factory=uuid4)
    integration_candidate_id: UUID
    decision: AdapterDecision
    score: float = Field(ge=0, le=1)
    criteria_scores: dict[str, float] = Field(default_factory=dict)
    adapter_boundary: str = Field(min_length=1)
    sandbox_required: bool = True
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class FourVideoSlotRequirement(BaseModel):
    schema_version: Literal["cmf.four_video_slot_requirement.v1"] = "cmf.four_video_slot_requirement.v1"
    slot_code: VideoFormatCode
    slot_name: str = Field(min_length=1)
    route_purpose: str = Field(min_length=1)
    required_dependencies: list[str] = Field(min_length=1)
    doctrine_refs: list[str] = Field(min_length=1)
    composition_rules: list[str] = Field(min_length=1)


class VideoFormatRouteReceipt(BaseModel):
    schema_version: Literal["cmf.video_format_route_receipt.v1"] = "cmf.video_format_route_receipt.v1"
    video_format_route_receipt_id: UUID = Field(default_factory=uuid4)
    slot_code: VideoFormatCode
    expression_moment_id: UUID
    selected: bool
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class FourVideoFormatPlan(BaseModel):
    schema_version: Literal["cmf.four_video_format_plan.v1"] = "cmf.four_video_format_plan.v1"
    four_video_format_plan_id: UUID = Field(default_factory=uuid4)
    organization_id: UUID
    brand_id: UUID
    guest_asset_pack_id: UUID | None = None
    slot_requirements: list[FourVideoSlotRequirement] = Field(min_length=4, max_length=4)
    route_receipts: list[VideoFormatRouteReceipt] = Field(default_factory=list)
    approval_blockers: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class PrimitiveValidationResult(BaseModel):
    schema_version: Literal["cmf.primitive_validation_result.v1"] = "cmf.primitive_validation_result.v1"
    primitive_id: str = Field(min_length=1)
    primitive_name: str = Field(min_length=1)
    role: Literal["meaning_transform", "delivery_shape", "format_material"]
    score: float = Field(ge=0, le=1)
    threshold: float = Field(ge=0, le=1)
    evidence_ref: str = Field(min_length=1)
    composition_element_ref: str = Field(min_length=1)
    decision: Literal["pass", "fail"]


class VisualFeelContract(BaseModel):
    schema_version: Literal["cmf.visual_feel_contract.v1"] = "cmf.visual_feel_contract.v1"
    visual_feel_contract_id: UUID = Field(default_factory=uuid4)
    route_id: VideoFormatCode
    required_distinct_feel: str = Field(min_length=1)
    minimum_validated_primitives: int = Field(default=3, ge=3)
    primitive_obligations: list[str] = Field(min_length=3)
    forbidden_style_collapses: list[str] = Field(default_factory=list)
    source_doctrine_refs: list[str] = Field(min_length=1)


class CompositionPreflightReceipt(BaseModel):
    schema_version: Literal["cmf.composition_preflight_receipt.v1"] = "cmf.composition_preflight_receipt.v1"
    composition_preflight_receipt_id: UUID = Field(default_factory=uuid4)
    composition_id: str = Field(min_length=1)
    route_id: VideoFormatCode
    visual_feel_contract_id: UUID
    minimum_validated_primitives: int = Field(default=3, ge=3)
    primitive_validation_count: int = Field(ge=0)
    primitive_results: list[PrimitiveValidationResult] = Field(default_factory=list)
    role_coverage: dict[str, bool] = Field(default_factory=dict)
    hard_failure_codes: list[str] = Field(default_factory=list)
    decision: CompositionDecision
    written_at: datetime = Field(default_factory=utc_now)


class BrandGenesisSubstrateBinding(BaseModel):
    schema_version: Literal["cmf.brand_genesis_substrate_binding.v1"] = "cmf.brand_genesis_substrate_binding.v1"
    brand_context_version_id: UUID
    brand_context_version_hash: str = Field(min_length=1)
    voice_dna_ref: str = Field(min_length=1)
    visual_dna_ref: str = Field(min_length=1)
    emotional_dna_ref: str = Field(min_length=1)
    micro_semiotic_anchor_refs: list[str] = Field(default_factory=list)
    negative_space_refs: list[str] = Field(default_factory=list)


class ResolvedBrandGenesisSubstrate(BaseModel):
    schema_version: Literal["cmf.resolved_brand_genesis_substrate.v1"] = "cmf.resolved_brand_genesis_substrate.v1"
    resolved_brand_genesis_substrate_id: UUID = Field(default_factory=uuid4)
    binding: BrandGenesisSubstrateBinding
    composition_constraints: dict[str, Any] = Field(default_factory=dict)
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)


class ExpressionLineageBinding(BaseModel):
    schema_version: Literal["cmf.expression_lineage_binding.v1"] = "cmf.expression_lineage_binding.v1"
    interview_asset_contract_id: UUID
    expression_moment_id: UUID
    complete_editing_session_id: UUID
    asset_route_receipt_id: UUID
    transcript_segment_refs: list[str] = Field(min_length=1)
    extraction_receipt_refs: list[str] = Field(default_factory=list)
    eval_target_refs: list[str] = Field(default_factory=list)


class ExpressionLineageBindingReceipt(BaseModel):
    schema_version: Literal["cmf.expression_lineage_binding_receipt.v1"] = "cmf.expression_lineage_binding_receipt.v1"
    expression_lineage_binding_receipt_id: UUID = Field(default_factory=uuid4)
    expression_lineage_binding: ExpressionLineageBinding
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class SourceTimestampRange(BaseModel):
    schema_version: Literal["cmf.source_timestamp_range.v1"] = "cmf.source_timestamp_range.v1"
    source_ref: str = Field(min_length=1)
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)

    @model_validator(mode="after")
    def _time_order(self) -> "SourceTimestampRange":
        if self.end_seconds <= self.start_seconds:
            raise ValueError("end_seconds must be after start_seconds")
        return self


class CompositionBeat(BaseModel):
    schema_version: Literal["cmf.composition_beat.v1"] = "cmf.composition_beat.v1"
    beat_id: str = Field(min_length=1)
    beat_role: str = Field(min_length=1)
    source_range: SourceTimestampRange
    speaker: str = Field(min_length=1)
    text: str = Field(min_length=1)
    expression_state: str = Field(min_length=1)
    primitive_refs: list[str] = Field(default_factory=list)


class LayerCue(BaseModel):
    schema_version: Literal["cmf.layer_cue.v1"] = "cmf.layer_cue.v1"
    layer_id: str = Field(min_length=1)
    cue_type: str = Field(min_length=1)
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    payload: dict[str, Any] = Field(default_factory=dict)


class TimelineCue(BaseModel):
    schema_version: Literal["cmf.timeline_cue.v1"] = "cmf.timeline_cue.v1"
    cue_id: str = Field(min_length=1)
    beat_id: str = Field(min_length=1)
    cue_type: str = Field(min_length=1)
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    target_layer_id: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _time_order(self) -> "TimelineCue":
        if self.end_seconds <= self.start_seconds:
            raise ValueError("cue end_seconds must be after start_seconds")
        return self


class CompositionBeatMap(BaseModel):
    schema_version: Literal["cmf.composition_beat_map.v1"] = "cmf.composition_beat_map.v1"
    composition_beat_map_id: UUID = Field(default_factory=uuid4)
    expression_moment_id: UUID
    beats: list[CompositionBeat] = Field(min_length=1)
    timeline_cues: list[TimelineCue] = Field(min_length=1)
    source_lineage_refs: list[str] = Field(min_length=1)
    created_at: datetime = Field(default_factory=utc_now)


class BeatMapCompilationReceipt(BaseModel):
    schema_version: Literal["cmf.beat_map_compilation_receipt.v1"] = "cmf.beat_map_compilation_receipt.v1"
    beat_map_compilation_receipt_id: UUID = Field(default_factory=uuid4)
    composition_beat_map_id: UUID
    beat_count: int = Field(ge=1)
    cue_count: int = Field(ge=1)
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class OpenSourceAdapterBinding(BaseModel):
    schema_version: Literal["cmf.open_source_adapter_binding.v1"] = "cmf.open_source_adapter_binding.v1"
    integration_adapter_decision_id: UUID
    adapter_name: str = Field(min_length=1)
    allowed_runtime_scope: str = Field(min_length=1)
    sandbox_policy: str = Field(min_length=1)


class CompositionRuntimeBinding(BaseModel):
    schema_version: Literal["cmf.composition_runtime_binding.v1"] = "cmf.composition_runtime_binding.v1"
    composition_runtime_binding_id: UUID = Field(default_factory=uuid4)
    scene_template_binding_id: UUID
    composition_template_id: UUID
    brand_genesis_substrate_id: UUID
    expression_lineage_binding_ref: str = Field(min_length=1)
    visual_feel_contract_id: UUID
    composition_beat_map_id: UUID
    open_source_adapter_bindings: list[OpenSourceAdapterBinding] = Field(default_factory=list)
    renderer_route: str = Field(min_length=1)
    approval_status: ApprovalStatus = ApprovalStatus.draft
    created_at: datetime = Field(default_factory=utc_now)


class CompositionRuntimeBindingReceipt(BaseModel):
    schema_version: Literal["cmf.composition_runtime_binding_receipt.v1"] = "cmf.composition_runtime_binding_receipt.v1"
    composition_runtime_binding_receipt_id: UUID = Field(default_factory=uuid4)
    composition_runtime_binding_id: UUID | None = None
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class CompositionTemplateFamily(BaseModel):
    schema_version: Literal["cmf.composition_template_family.v1"] = "cmf.composition_template_family.v1"
    family_code: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    supported_format_codes: list[str] = Field(min_length=1)
    template_ids: list[str] = Field(default_factory=list)
    asset_code_prefix: str = Field(min_length=1)
    route_id: VideoFormatCode


class ContentAssetCodeReservation(BaseModel):
    schema_version: Literal["cmf.content_asset_code_reservation.v1"] = "cmf.content_asset_code_reservation.v1"
    content_asset_code: str = Field(min_length=5)
    brand_id: UUID
    template_family_code: str = Field(min_length=1)
    content_format_code: str = Field(min_length=1)
    sequence_number: int = Field(ge=1)
    reserved_for_object_ref: str = Field(min_length=1)


class PerformanceStateSelection(BaseModel):
    schema_version: Literal["cmf.performance_state_selection.v1"] = "cmf.performance_state_selection.v1"
    performance_state_selection_id: UUID = Field(default_factory=uuid4)
    acting_state_code: str = Field(min_length=1)
    expression_state: str = Field(min_length=1)
    emotion: str = Field(min_length=1)
    gesture: str = Field(min_length=1)
    camera_attitude: str = Field(min_length=1)
    eligibility_score: float = Field(ge=0, le=1)
    source_evidence_refs: list[str] = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)


class PaperCutMaterialityRule(BaseModel):
    schema_version: Literal["cmf.papercut_materiality_rule.v1"] = "cmf.papercut_materiality_rule.v1"
    rule_id: str = Field(min_length=1)
    texture: str = Field(min_length=1)
    edge_policy: str = Field(min_length=1)
    shadow_policy: str = Field(min_length=1)
    allowed_style_tokens: list[str] = Field(min_length=1)


class PaperCutMotionCue(BaseModel):
    schema_version: Literal["cmf.papercut_motion_cue.v1"] = "cmf.papercut_motion_cue.v1"
    motion_cue_id: str = Field(min_length=1)
    layer_id: str = Field(min_length=1)
    motion_type: str = Field(min_length=1)
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    easing: str = Field(min_length=1)
    meaning_ref: str = Field(min_length=1)


class PaperCutSfxCue(BaseModel):
    schema_version: Literal["cmf.papercut_sfx_cue.v1"] = "cmf.papercut_sfx_cue.v1"
    sfx_cue_id: str = Field(min_length=1)
    cue_ref: str = Field(min_length=1)
    sound_family: str = Field(min_length=1)
    volume_db: float = Field(le=0)
    meaning_ref: str = Field(min_length=1)


class PaperCutRuntimeManifest(BaseModel):
    schema_version: Literal["cmf.papercut_runtime_manifest.v1"] = "cmf.papercut_runtime_manifest.v1"
    papercut_runtime_manifest_id: UUID = Field(default_factory=uuid4)
    composition_template_id: UUID
    materiality_rules: list[PaperCutMaterialityRule] = Field(min_length=1)
    motion_cues: list[PaperCutMotionCue] = Field(min_length=1)
    sfx_cues: list[PaperCutSfxCue] = Field(default_factory=list)
    rig_refs: list[str] = Field(min_length=1)
    doctrine_eval_refs: list[str] = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)


class PaperCutRuntimeReceipt(BaseModel):
    schema_version: Literal["cmf.papercut_runtime_receipt.v1"] = "cmf.papercut_runtime_receipt.v1"
    papercut_runtime_receipt_id: UUID = Field(default_factory=uuid4)
    papercut_runtime_manifest_id: UUID
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class MicroSemioticAnchorSelection(BaseModel):
    schema_version: Literal["cmf.micro_semiotic_anchor_selection.v1"] = "cmf.micro_semiotic_anchor_selection.v1"
    micro_semiotic_anchor_selection_id: UUID = Field(default_factory=uuid4)
    selected_anchor_refs: list[str] = Field(min_length=1)
    route_id: VideoFormatCode
    audience_context_ref: str = Field(min_length=1)
    risk_score: float = Field(ge=0, le=1)
    risk_notes: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)


class CompositionLayoutPlan(BaseModel):
    schema_version: Literal["cmf.composition_layout_plan.v1"] = "cmf.composition_layout_plan.v1"
    composition_layout_plan_id: UUID = Field(default_factory=uuid4)
    source_composition_job_id: UUID
    frame_plan: dict[str, Any] = Field(default_factory=dict)
    zones: list[CompositionZone] = Field(min_length=1)
    text_space_strategy: str = Field(min_length=1)
    identity_rebuild_required: bool = True


class ProductionTextPlan(BaseModel):
    schema_version: Literal["cmf.production_text_plan.v1"] = "cmf.production_text_plan.v1"
    production_text_plan_id: UUID = Field(default_factory=uuid4)
    editable_text_layers: list[str] = Field(min_length=1)
    final_copy_source_refs: list[str] = Field(min_length=1)
    downstream_renderer: RendererTarget
    baked_text_allowed: bool = False


class GeometricsHandoffPlan(BaseModel):
    schema_version: Literal["cmf.geometrics_handoff_plan.v1"] = "cmf.geometrics_handoff_plan.v1"
    geometrics_handoff_plan_id: UUID = Field(default_factory=uuid4)
    target_runtime: Literal["skia", "remotion", "motion_canvas"]
    layer_manifest_ref: str = Field(min_length=1)
    repair_queue_ref: str | None = None
    deterministic_render_required: bool = True


class IdeogramProductionBridgeReceipt(BaseModel):
    schema_version: Literal["cmf.ideogram_production_bridge_receipt.v1"] = "cmf.ideogram_production_bridge_receipt.v1"
    ideogram_production_bridge_receipt_id: UUID = Field(default_factory=uuid4)
    source_composition_job_id: UUID
    layout_plan_id: UUID
    text_plan_id: UUID
    geometrics_handoff_plan_id: UUID
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class GenerativeAssetFactoryJob(BaseModel):
    schema_version: Literal["cmf.generative_asset_factory_job.v1"] = "cmf.generative_asset_factory_job.v1"
    generative_asset_factory_job_id: UUID = Field(default_factory=uuid4)
    provider: Literal["gpt_image_2", "flux_2", "klein_9b", "qwen_layered", "sam3", "comfyui"]
    requested_asset_role: str = Field(min_length=1)
    source_context_refs: list[str] = Field(min_length=1)
    deterministic_downstream_owner: str = Field(min_length=1)


class QwenLayeredDecompositionReceipt(BaseModel):
    schema_version: Literal["cmf.qwen_layered_decomposition_receipt.v1"] = "cmf.qwen_layered_decomposition_receipt.v1"
    qwen_layered_decomposition_receipt_id: UUID = Field(default_factory=uuid4)
    source_asset_ref: str = Field(min_length=1)
    layer_count: int = Field(ge=1)
    extracted_layer_refs: list[str] = Field(min_length=1)


class SAM3SaliencyReceipt(BaseModel):
    schema_version: Literal["cmf.sam3_saliency_receipt.v1"] = "cmf.sam3_saliency_receipt.v1"
    sam3_saliency_receipt_id: UUID = Field(default_factory=uuid4)
    source_asset_ref: str = Field(min_length=1)
    mask_refs: list[str] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)


class LayerManifestEntry(BaseModel):
    schema_version: Literal["cmf.layer_manifest_entry.v1"] = "cmf.layer_manifest_entry.v1"
    layer_id: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)
    role: str = Field(min_length=1)
    bounds: dict[str, float] = Field(default_factory=dict)
    editable: bool = True


class LayerExtractionResult(BaseModel):
    schema_version: Literal["cmf.layer_extraction_result.v1"] = "cmf.layer_extraction_result.v1"
    layer_extraction_result_id: UUID = Field(default_factory=uuid4)
    source_asset_ref: str = Field(min_length=1)
    qwen_receipt_id: UUID | None = None
    sam3_receipt_id: UUID | None = None
    layers: list[LayerManifestEntry] = Field(min_length=1)
    repair_required: bool = False
    blocker_codes: list[str] = Field(default_factory=list)


class RepairJobReceipt(BaseModel):
    schema_version: Literal["cmf.repair_job_receipt.v1"] = "cmf.repair_job_receipt.v1"
    repair_job_receipt_id: UUID = Field(default_factory=uuid4)
    layer_extraction_result_id: UUID
    repair_scope: list[str] = Field(default_factory=list)
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class RendererComponentRegistration(BaseModel):
    schema_version: Literal["cmf.renderer_component_registration.v1"] = "cmf.renderer_component_registration.v1"
    component_code: str = Field(min_length=1)
    renderer_target: RendererTarget
    supported_format_codes: list[str] = Field(min_length=1)
    prop_schema_ref: str = Field(min_length=1)
    sandbox_policy: str = Field(min_length=1)


class RendererPropsManifest(BaseModel):
    schema_version: Literal["cmf.renderer_props_manifest.v1"] = "cmf.renderer_props_manifest.v1"
    renderer_props_manifest_id: UUID = Field(default_factory=uuid4)
    composition_runtime_binding_id: UUID
    renderer_target: RendererTarget
    component_code: str = Field(min_length=1)
    props: dict[str, Any] = Field(default_factory=dict)
    deterministic_inputs_hash: str = Field(min_length=12)
    asset_policy_refs: list[str] = Field(default_factory=list)


class RendererComponentCompatibilityReport(BaseModel):
    schema_version: Literal["cmf.renderer_component_compatibility_report.v1"] = "cmf.renderer_component_compatibility_report.v1"
    renderer_component_compatibility_report_id: UUID = Field(default_factory=uuid4)
    component_code: str = Field(min_length=1)
    compatible: bool
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)


class RendererPropsCompilationReceipt(BaseModel):
    schema_version: Literal["cmf.renderer_props_compilation_receipt.v1"] = "cmf.renderer_props_compilation_receipt.v1"
    renderer_props_compilation_receipt_id: UUID = Field(default_factory=uuid4)
    renderer_props_manifest_id: UUID
    compatibility_report_id: UUID
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class OpenSourceTemplateConversion(BaseModel):
    schema_version: Literal["cmf.open_source_template_conversion.v1"] = "cmf.open_source_template_conversion.v1"
    open_source_template_conversion_id: UUID = Field(default_factory=uuid4)
    integration_adapter_decision_id: UUID
    source_project: str = Field(min_length=1)
    source_template_ref: str = Field(min_length=1)
    cmf_template_family_code: str = Field(min_length=1)
    converted_component_code: str = Field(min_length=1)
    sandbox_path_ref: str = Field(min_length=1)
    direct_import_allowed: bool = False
    blocker_codes: list[str] = Field(default_factory=list)


class EvalTargetSelection(BaseModel):
    schema_version: Literal["cmf.eval_target_selection.v1"] = "cmf.eval_target_selection.v1"
    eval_target_selection_id: UUID = Field(default_factory=uuid4)
    target_object_type: str = Field(min_length=1)
    target_object_ref: str = Field(min_length=1)
    eval_family: str = Field(min_length=1)
    required_receipt_refs: list[str] = Field(default_factory=list)


class CompositionEvalSuiteRun(BaseModel):
    schema_version: Literal["cmf.composition_eval_suite_run.v1"] = "cmf.composition_eval_suite_run.v1"
    composition_eval_suite_run_id: UUID = Field(default_factory=uuid4)
    eval_target_selection: EvalTargetSelection
    primitive_preflight_receipt: CompositionPreflightReceipt | None = None
    doctrine_receipt_refs: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    decision: CompositionDecision
    score: float = Field(ge=0, le=1)
    written_at: datetime = Field(default_factory=utc_now)


class ReviewReadModel(BaseModel):
    schema_version: Literal["cmf.composition_review_read_model.v1"] = "cmf.composition_review_read_model.v1"
    review_read_model_id: UUID = Field(default_factory=uuid4)
    target_object_ref: str = Field(min_length=1)
    approval_status: ApprovalStatus
    blockers: list[CompositionApprovalBlocker] = Field(default_factory=list)
    eval_suite_run_refs: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=utc_now)


class CompositionOperatorApprovalReceipt(BaseModel):
    schema_version: Literal["cmf.composition_operator_approval_receipt.v1"] = "cmf.composition_operator_approval_receipt.v1"
    composition_operator_approval_receipt_id: UUID = Field(default_factory=uuid4)
    review_read_model_id: UUID
    operator_id: UUID
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


def runtime_hash(parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
