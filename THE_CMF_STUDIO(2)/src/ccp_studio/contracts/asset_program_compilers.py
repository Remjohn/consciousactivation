"""Batch 2 asset and program compiler contracts for TS-CMF-093 through TS-CMF-119."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.composition_runtime import (
    ApprovalStatus,
    CompositionDecision,
    CompositionTemplateLayer,
    CompositionZone,
    RendererTarget,
    VideoFormatCode,
    runtime_hash,
)
from ccp_studio.contracts.orchestration import utc_now


StillFormatCode = Literal["CAR-LST", "CAR-JUX", "SIMG-QUOTE", "SIMG-ASSERTION", "SUPERVISUAL"]
AssetProgramCompilerDecision = CompositionDecision
RegistryLoadDecision = Literal["loaded", "blocked"]
ProgramStatus = Literal["draft", "compiled", "blocked", "repair_required", "approved"]

LEGACY_SKIA_RUNTIME_DEPRECATION_NOTE = (
    "Deprecated render runtime path: legacy Python/C++ Skia sidecar-era contracts are "
    "retained for migration visibility only. New render execution should route through "
    "Local Render Worker plus Remotion Node.js + @remotion/skia / FFmpeg adapter gates."
)


class RegistryBundleLoadReceipt(BaseModel):
    schema_version: Literal["cmf.registry_bundle_load_receipt.v1"] = "cmf.registry_bundle_load_receipt.v1"
    registry_bundle_load_receipt_id: UUID = Field(default_factory=uuid4)
    registry_ref: str = Field(min_length=1)
    absolute_path: str = Field(min_length=1)
    decision: RegistryLoadDecision
    entry_count: int = Field(ge=0)
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class AnimationStudioMigrationManifest(BaseModel):
    schema_version: Literal["cmf.animation_studio_migration_manifest.v1"] = "cmf.animation_studio_migration_manifest.v1"
    animation_studio_migration_manifest_id: UUID = Field(default_factory=uuid4)
    legacy_source_ref: str = Field(min_length=1)
    operator_editor_route: str = Field(min_length=1)
    rig_editor_panels: list[str] = Field(min_length=1)
    migrated_asset_refs: list[str] = Field(min_length=1)
    receipts_required: list[str] = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class RigEditOperation(BaseModel):
    schema_version: Literal["cmf.rig_edit_operation.v1"] = "cmf.rig_edit_operation.v1"
    rig_edit_operation_id: UUID = Field(default_factory=uuid4)
    operation_type: Literal["pose_adjustment", "anchor_binding", "mouth_shape_binding", "performance_state_binding"]
    target_rig_ref: str = Field(min_length=1)
    before_hash: str = Field(min_length=12)
    after_hash: str = Field(min_length=12)
    operator_id: UUID
    evidence_refs: list[str] = Field(min_length=1)
    written_at: datetime = Field(default_factory=utc_now)


class HeadlessFrameRenderRequest(BaseModel):
    """Deprecated legacy queue contract; keep readable until replacement parity tests pass."""

    schema_version: Literal["cmf.headless_frame_render_request.v1"] = "cmf.headless_frame_render_request.v1"
    headless_frame_render_request_id: UUID = Field(default_factory=uuid4)
    composition_template_id: UUID
    runtime_manifest_ref: str = Field(min_length=1)
    frame_start: int = Field(ge=0)
    frame_end: int = Field(gt=0)
    fps: int = Field(gt=0)
    output_format: Literal["png_sequence", "webp_sequence", "mp4_proxy"]
    deterministic_inputs_hash: str = Field(min_length=12)

    @model_validator(mode="after")
    def _valid_range(self) -> "HeadlessFrameRenderRequest":
        if self.frame_end <= self.frame_start:
            raise ValueError("headless frame render request end must be greater than start")
        return self


class HeadlessFrameRenderReceipt(BaseModel):
    """Deprecated legacy queue receipt; do not use as a new render execution path."""

    schema_version: Literal["cmf.headless_frame_render_receipt.v1"] = "cmf.headless_frame_render_receipt.v1"
    headless_frame_render_receipt_id: UUID = Field(default_factory=uuid4)
    headless_frame_render_request_id: UUID
    frame_manifest_ref: str = Field(min_length=1)
    preview_ref: str = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class AvatarExportWorkerJob(BaseModel):
    """Deprecated legacy avatar export worker job; superseded by gated render-worker jobs."""

    schema_version: Literal["cmf.avatar_export_worker_job.v1"] = "cmf.avatar_export_worker_job.v1"
    avatar_export_worker_job_id: UUID = Field(default_factory=uuid4)
    character_rig_ref: str = Field(min_length=1)
    performance_program_ref: str = Field(min_length=1)
    export_targets: list[Literal["alpha_png_sequence", "webm_alpha", "sprite_sheet"]] = Field(min_length=1)
    deterministic_inputs_hash: str = Field(min_length=12)


class AvatarExportReceipt(BaseModel):
    schema_version: Literal["cmf.avatar_export_receipt.v1"] = "cmf.avatar_export_receipt.v1"
    avatar_export_receipt_id: UUID = Field(default_factory=uuid4)
    avatar_export_worker_job_id: UUID
    exported_asset_refs: list[str] = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class GeometricsSceneSpec(BaseModel):
    schema_version: Literal["cmf.geometrics_scene_spec.v1"] = "cmf.geometrics_scene_spec.v1"
    geometrics_scene_spec_id: UUID = Field(default_factory=uuid4)
    scene_code: str = Field(min_length=1)
    canvas: dict[str, int] = Field(default_factory=dict)
    zones: list[CompositionZone] = Field(min_length=1)
    layers: list[CompositionTemplateLayer] = Field(min_length=1)
    skia_component_refs: list[str] = Field(min_length=1)
    sam3_mask_refs: list[str] = Field(default_factory=list)
    pretext_text_layer_refs: list[str] = Field(default_factory=list)
    primitive_validation_ids: list[str] = Field(min_length=3)
    deterministic_inputs_hash: str = Field(min_length=12)

    @model_validator(mode="after")
    def _layers_reference_zones(self) -> "GeometricsSceneSpec":
        zone_ids = {zone.zone_id for zone in self.zones}
        missing = [layer.zone_id for layer in self.layers if layer.zone_id not in zone_ids]
        if missing:
            raise ValueError(f"geometrics scene layers reference unknown zones: {missing}")
        return self


class SkiaRenderBinding(BaseModel):
    """Deprecated Skia sidecar-era binding kept for migration and old fixture coverage."""

    schema_version: Literal["cmf.skia_render_binding.v1"] = "cmf.skia_render_binding.v1"
    skia_render_binding_id: UUID = Field(default_factory=uuid4)
    source_scene_ref: str = Field(min_length=1)
    renderer_target: Literal["skia"] = "skia"
    component_refs: list[str] = Field(min_length=1)
    render_job_ref: str = Field(min_length=1)
    deterministic_inputs_hash: str = Field(min_length=12)


class SkiaRenderReceipt(BaseModel):
    """Deprecated Skia sidecar-era receipt; new render QA should use Render QA V1 receipts."""

    schema_version: Literal["cmf.skia_render_receipt.v1"] = "cmf.skia_render_receipt.v1"
    skia_render_receipt_id: UUID = Field(default_factory=uuid4)
    skia_render_binding_id: UUID
    output_asset_ref: str = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class PrimitiveTriadContract(BaseModel):
    schema_version: Literal["cmf.primitive_triad_contract.v1"] = "cmf.primitive_triad_contract.v1"
    primitive_id: str = Field(min_length=1)
    canonical_name: str = Field(min_length=1)
    role: Literal["meaning_transform", "delivery_shape", "format_material"]
    evidence_ref: str = Field(min_length=1)


class CarouselSlideAtom(BaseModel):
    schema_version: Literal["cmf.carousel_slide_atom.v1"] = "cmf.carousel_slide_atom.v1"
    slide_atom_code: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    composition_meaning: str = Field(min_length=1)
    allowed_positions: list[str] = Field(min_length=1)
    compatible_format_codes: list[str] = Field(min_length=1)
    primitive_triads: list[PrimitiveTriadContract] = Field(min_length=3)
    visual_grammar: dict[str, Any] = Field(default_factory=dict)
    query_tags: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _has_required_roles(self) -> "CarouselSlideAtom":
        roles = {item.role for item in self.primitive_triads}
        if roles != {"meaning_transform", "delivery_shape", "format_material"}:
            raise ValueError("carousel slide atom must carry one primitive for each required role")
        return self


class CarouselSlideLibrary(BaseModel):
    schema_version: Literal["cmf.carousel_slide_library.v1"] = "cmf.carousel_slide_library.v1"
    carousel_slide_library_id: UUID = Field(default_factory=uuid4)
    registry_id: str = Field(min_length=1)
    recognized_format_codes: list[str] = Field(min_length=1)
    slide_atoms: list[CarouselSlideAtom] = Field(min_length=1)
    global_rules: dict[str, Any] = Field(default_factory=dict)
    registry_load_receipt_id: UUID
    compiled_at: datetime = Field(default_factory=utc_now)


class CarouselSequencePlan(BaseModel):
    schema_version: Literal["cmf.carousel_sequence_plan.v1"] = "cmf.carousel_sequence_plan.v1"
    carousel_sequence_plan_id: UUID = Field(default_factory=uuid4)
    format_code: Literal["CAR-LST", "CAR-JUX"]
    source_context_refs: list[str] = Field(min_length=1)
    slide_atom_codes: list[str] = Field(min_length=2)
    sequence_rationale: str = Field(min_length=1)
    primitive_validation_ids: list[str] = Field(min_length=3)
    deterministic_inputs_hash: str = Field(min_length=12)


class CarouselBuilderProgram(BaseModel):
    schema_version: Literal["cmf.carousel_builder_program.v1"] = "cmf.carousel_builder_program.v1"
    carousel_builder_program_id: UUID = Field(default_factory=uuid4)
    carousel_sequence_plan_id: UUID
    slide_specs: list[dict[str, Any]] = Field(min_length=1)
    geometrics_layout_plan_ref: str = Field(min_length=1)
    # Deprecated legacy Skia sidecar-era job refs. Preserve until carousel preview/export
    # parity exists on Remotion Node.js + @remotion/skia.
    skia_render_job_refs: list[str] = Field(min_length=1)
    qwen_layered_required: bool = True
    ideogram_composition_refs: list[str] = Field(default_factory=list)
    deterministic_inputs_hash: str = Field(min_length=12)


class CarouselExportReceipt(BaseModel):
    schema_version: Literal["cmf.carousel_export_receipt.v1"] = "cmf.carousel_export_receipt.v1"
    carousel_export_receipt_id: UUID = Field(default_factory=uuid4)
    carousel_builder_program_id: UUID
    exported_slide_refs: list[str] = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class CarouselAtlasRouteReceipt(BaseModel):
    schema_version: Literal["cmf.carousel_atlas_route_receipt.v1"] = "cmf.carousel_atlas_route_receipt.v1"
    carousel_atlas_route_receipt_id: UUID = Field(default_factory=uuid4)
    composition_id: str = Field(min_length=1)
    selected_for_slide_atom_code: str = Field(min_length=1)
    supported_aspect_ratios: list[str] = Field(min_length=1)
    tool_routing: dict[str, Any] = Field(default_factory=dict)
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class SingleImageRegistrySnapshot(BaseModel):
    schema_version: Literal["cmf.single_image_registry_snapshot.v1"] = "cmf.single_image_registry_snapshot.v1"
    single_image_registry_snapshot_id: UUID = Field(default_factory=uuid4)
    registry_schema_id: str = Field(min_length=1)
    composition_ids: list[str] = Field(min_length=1)
    registry_load_receipt_id: UUID
    deterministic_inputs_hash: str = Field(min_length=12)


class SingleImageRouteDecision(BaseModel):
    schema_version: Literal["cmf.single_image_route_decision.v1"] = "cmf.single_image_route_decision.v1"
    single_image_route_decision_id: UUID = Field(default_factory=uuid4)
    composition_id: str = Field(min_length=1)
    archetype_ref: str = Field(min_length=1)
    format_code: StillFormatCode
    selected_family: str = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class SuperVisualFamilyContract(BaseModel):
    schema_version: Literal["cmf.supervisual_family_contract.v1"] = "cmf.supervisual_family_contract.v1"
    supervisual_family_contract_id: UUID = Field(default_factory=uuid4)
    family_code: str = Field(min_length=1)
    composition_ids: list[str] = Field(min_length=1)
    primitive_triads: list[PrimitiveTriadContract] = Field(min_length=3)
    visual_pressure_policy: str = Field(min_length=1)
    doctrine_refs: list[str] = Field(min_length=1)


class SingleImageProviderJobPlan(BaseModel):
    schema_version: Literal["cmf.single_image_provider_job_plan.v1"] = "cmf.single_image_provider_job_plan.v1"
    single_image_provider_job_plan_id: UUID = Field(default_factory=uuid4)
    single_image_route_decision_id: UUID
    provider_jobs: list[dict[str, Any]] = Field(min_length=1)
    layer_materialization_refs: list[str] = Field(min_length=1)
    # Deprecated legacy renderer authority. New still/video render work should migrate to
    # the gated Remotion Node.js + @remotion/skia adapter path.
    final_authority: Literal["cmf_skia_renderer"] = "cmf_skia_renderer"
    deterministic_downstream_required: bool = True
    blocker_codes: list[str] = Field(default_factory=list)


class StillVisualLayerMaterialization(BaseModel):
    schema_version: Literal["cmf.still_visual_layer_materialization.v1"] = "cmf.still_visual_layer_materialization.v1"
    still_visual_layer_materialization_id: UUID = Field(default_factory=uuid4)
    source_route_decision_id: UUID
    layer_refs: list[str] = Field(min_length=1)
    qwen_layered_receipt_ref: str = Field(min_length=1)
    sam3_mask_refs: list[str] = Field(default_factory=list)
    text_layers_editable: bool = True


class SingleImageSkiaScene(BaseModel):
    """Deprecated Skia scene contract; retain as read model until template parity exists."""

    schema_version: Literal["cmf.single_image_skia_scene.v1"] = "cmf.single_image_skia_scene.v1"
    single_image_skia_scene_id: UUID = Field(default_factory=uuid4)
    single_image_route_decision_id: UUID
    canvas: dict[str, int] = Field(default_factory=dict)
    zones: list[dict[str, Any]] = Field(min_length=1)
    layer_stack: list[dict[str, Any]] = Field(min_length=1)
    rough_notation_plan: dict[str, Any] = Field(default_factory=dict)
    skia_component_refs: list[str] = Field(min_length=1)
    primitive_validation_ids: list[str] = Field(min_length=3)
    deterministic_inputs_hash: str = Field(min_length=12)


class SingleImageEvalReviewReceipt(BaseModel):
    schema_version: Literal["cmf.single_image_eval_review_receipt.v1"] = "cmf.single_image_eval_review_receipt.v1"
    single_image_eval_review_receipt_id: UUID = Field(default_factory=uuid4)
    single_image_skia_scene_id: UUID
    score: float = Field(ge=0, le=1)
    decision: AssetProgramCompilerDecision
    blocker_codes: list[str] = Field(default_factory=list)
    golden_fixture_refs: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class GoldenFixtureResult(BaseModel):
    schema_version: Literal["cmf.golden_fixture_result.v1"] = "cmf.golden_fixture_result.v1"
    golden_fixture_result_id: UUID = Field(default_factory=uuid4)
    fixture_ref: str = Field(min_length=1)
    target_object_ref: str = Field(min_length=1)
    passed: bool
    diff_summary: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)


class VideoEditScene(BaseModel):
    schema_version: Literal["cmf.video_edit_scene.v1"] = "cmf.video_edit_scene.v1"
    scene_code: str = Field(min_length=1)
    video_format_code: VideoFormatCode
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    composition_template_ref: str = Field(min_length=1)
    transcript_beat_refs: list[str] = Field(min_length=1)
    layer_stack_refs: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def _valid_scene_timing(self) -> "VideoEditScene":
        if self.end_seconds <= self.start_seconds:
            raise ValueError("video edit scene must end after it starts")
        return self


class OTIOAuditManifest(BaseModel):
    schema_version: Literal["cmf.otio_audit_manifest.v1"] = "cmf.otio_audit_manifest.v1"
    otio_audit_manifest_id: UUID = Field(default_factory=uuid4)
    timeline_ref: str = Field(min_length=1)
    scene_refs: list[str] = Field(min_length=1)
    marker_refs: list[str] = Field(default_factory=list)
    deterministic_inputs_hash: str = Field(min_length=12)
    audit_notes: list[str] = Field(default_factory=list)


class VideoRenderContract(BaseModel):
    schema_version: Literal["cmf.video_render_contract.v1"] = "cmf.video_render_contract.v1"
    video_render_contract_id: UUID = Field(default_factory=uuid4)
    render_target: RendererTarget
    render_tier: Literal["proxy", "final"]
    timeline_ref: str = Field(min_length=1)
    expected_output_ref: str = Field(min_length=1)
    deterministic_inputs_hash: str = Field(min_length=12)


class VideoEditProgram(BaseModel):
    schema_version: Literal["cmf.video_edit_program.v1"] = "cmf.video_edit_program.v1"
    video_edit_program_id: UUID = Field(default_factory=uuid4)
    interview_asset_contract_ref: str = Field(min_length=1)
    transcript_beat_map_ref: str = Field(min_length=1)
    content_format_targets: list[VideoFormatCode] = Field(min_length=1)
    scenes: list[VideoEditScene] = Field(min_length=1)
    otio_audit_manifest: OTIOAuditManifest
    render_contracts: list[VideoRenderContract] = Field(min_length=2)
    approval_status: ApprovalStatus = ApprovalStatus.draft
    blocker_codes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _has_proxy_and_final(self) -> "VideoEditProgram":
        tiers = {contract.render_tier for contract in self.render_contracts}
        if tiers != {"proxy", "final"}:
            raise ValueError("video edit program requires both proxy and final render contracts")
        return self


class TwoDCharacterGenesis(BaseModel):
    schema_version: Literal["cmf.two_d_character_genesis.v1"] = "cmf.two_d_character_genesis.v1"
    two_d_character_genesis_id: UUID = Field(default_factory=uuid4)
    character_ref: str = Field(min_length=1)
    brand_genesis_ref: str = Field(min_length=1)
    visual_dna_refs: list[str] = Field(min_length=1)
    acting_library_refs: list[str] = Field(min_length=1)
    required_pose_count: int = Field(ge=1)
    primitive_validation_ids: list[str] = Field(min_length=3)


class TwoDCharacterRig(BaseModel):
    schema_version: Literal["cmf.two_d_character_rig.v1"] = "cmf.two_d_character_rig.v1"
    two_d_character_rig_id: UUID = Field(default_factory=uuid4)
    character_genesis_id: UUID
    rig_ref: str = Field(min_length=1)
    joint_map: dict[str, Any] = Field(default_factory=dict)
    mouth_shape_refs: list[str] = Field(default_factory=list)
    pose_state_refs: list[str] = Field(min_length=1)
    deterministic_inputs_hash: str = Field(min_length=12)


class TwoDCharacterProviderAdapterDecision(BaseModel):
    schema_version: Literal["cmf.two_d_character_provider_adapter_decision.v1"] = "cmf.two_d_character_provider_adapter_decision.v1"
    two_d_character_provider_adapter_decision_id: UUID = Field(default_factory=uuid4)
    provider_name: Literal["stretchystudio", "see_through", "rive", "lottie", "custom_skia"]
    proposed_use: str = Field(min_length=1)
    production_authority_allowed: bool = False
    adapter_boundary: str = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)


class TwoDCharacterPerformanceCue(BaseModel):
    schema_version: Literal["cmf.two_d_character_performance_cue.v1"] = "cmf.two_d_character_performance_cue.v1"
    cue_ref: str = Field(min_length=1)
    transcript_span_ref: str = Field(min_length=1)
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    pose_state_ref: str = Field(min_length=1)
    gesture: str = Field(min_length=1)
    mouth_shape_ref: str | None = None

    @model_validator(mode="after")
    def _valid_cue_timing(self) -> "TwoDCharacterPerformanceCue":
        if self.end_seconds <= self.start_seconds:
            raise ValueError("performance cue must end after it starts")
        return self


class TwoDCharacterSceneProgram(BaseModel):
    schema_version: Literal["cmf.two_d_character_scene_program.v1"] = "cmf.two_d_character_scene_program.v1"
    two_d_character_scene_program_id: UUID = Field(default_factory=uuid4)
    character_rig_id: UUID
    video_format_code: Literal["SV-EDU"] = "SV-EDU"
    papercut_materiality_ref: str = Field(min_length=1)
    performance_cues: list[TwoDCharacterPerformanceCue] = Field(min_length=1)
    rough_notation_refs: list[str] = Field(default_factory=list)
    deterministic_inputs_hash: str = Field(min_length=12)


class TwoDCharacterRenderReceipt(BaseModel):
    schema_version: Literal["cmf.two_d_character_render_receipt.v1"] = "cmf.two_d_character_render_receipt.v1"
    two_d_character_render_receipt_id: UUID = Field(default_factory=uuid4)
    two_d_character_scene_program_id: UUID
    preview_ref: str = Field(min_length=1)
    alpha_export_ref: str = Field(min_length=1)
    decision: AssetProgramCompilerDecision
    blocker_codes: list[str] = Field(default_factory=list)
    eval_receipt_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class TwoDCharacterRepairPlan(BaseModel):
    schema_version: Literal["cmf.two_d_character_repair_plan.v1"] = "cmf.two_d_character_repair_plan.v1"
    two_d_character_repair_plan_id: UUID = Field(default_factory=uuid4)
    two_d_character_render_receipt_id: UUID
    repair_actions: list[str] = Field(min_length=1)
    approval_required: bool = True
    blocker_codes: list[str] = Field(default_factory=list)


class SequencingRegistryKernel(BaseModel):
    schema_version: Literal["cmf.sequencing_registry_kernel.v1"] = "cmf.sequencing_registry_kernel.v1"
    sequencing_registry_kernel_id: UUID = Field(default_factory=uuid4)
    kernel_code: str = Field(min_length=1)
    registry_refs: list[str] = Field(min_length=1)
    primitive_policy_refs: list[str] = Field(min_length=1)
    skill_compiler_refs: list[str] = Field(default_factory=list)
    deterministic_inputs_hash: str = Field(min_length=12)


class SequenceHypothesis(BaseModel):
    schema_version: Literal["cmf.sequence_hypothesis.v1"] = "cmf.sequence_hypothesis.v1"
    hypothesis_ref: str = Field(min_length=1)
    premise: str = Field(min_length=1)
    audience_context_ref: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)


class ExpressionAcquisitionPlan(BaseModel):
    schema_version: Literal["cmf.expression_acquisition_plan.v1"] = "cmf.expression_acquisition_plan.v1"
    acquisition_plan_ref: str = Field(min_length=1)
    interview_question_refs: list[str] = Field(min_length=1)
    guest_signal_refs: list[str] = Field(min_length=1)
    coverage_targets: list[str] = Field(min_length=1)


class InterviewBriefV2Plan(BaseModel):
    schema_version: Literal["cmf.interview_brief_v2_plan.v1"] = "cmf.interview_brief_v2_plan.v1"
    interview_brief_v2_plan_id: UUID = Field(default_factory=uuid4)
    brand_context_ref: str = Field(min_length=1)
    sequence_hypotheses: list[SequenceHypothesis] = Field(min_length=1)
    expression_acquisition_plan: ExpressionAcquisitionPlan
    doctrine_refs: list[str] = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)


class CueSuppressionDecision(BaseModel):
    schema_version: Literal["cmf.cue_suppression_decision.v1"] = "cmf.cue_suppression_decision.v1"
    cue_ref: str = Field(min_length=1)
    suppressed: bool
    reason: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)


class LiveIngredientCoverageTracker(BaseModel):
    schema_version: Literal["cmf.live_ingredient_coverage_tracker.v1"] = "cmf.live_ingredient_coverage_tracker.v1"
    live_ingredient_coverage_tracker_id: UUID = Field(default_factory=uuid4)
    interview_brief_v2_plan_id: UUID
    coverage_target_refs: list[str] = Field(min_length=1)
    captured_ingredient_refs: list[str] = Field(default_factory=list)
    cue_suppression_decisions: list[CueSuppressionDecision] = Field(default_factory=list)
    decision_code: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)


class ExpressionIngredient(BaseModel):
    schema_version: Literal["cmf.expression_ingredient.v1"] = "cmf.expression_ingredient.v1"
    ingredient_ref: str = Field(min_length=1)
    ingredient_type: Literal["quote", "story", "claim", "reaction", "framework", "visual_seed"]
    source_evidence_refs: list[str] = Field(default_factory=list)
    transcript_span_ref: str | None = None
    guest_truth_claim: str | None = None


class ExpressionRelationEdge(BaseModel):
    schema_version: Literal["cmf.expression_relation_edge.v1"] = "cmf.expression_relation_edge.v1"
    source_ingredient_ref: str = Field(min_length=1)
    target_ingredient_ref: str = Field(min_length=1)
    relation_type: Literal["supports", "contrasts", "escalates", "reframes", "requires_context"]


class ExpressionIngredientInventory(BaseModel):
    schema_version: Literal["cmf.expression_ingredient_inventory.v1"] = "cmf.expression_ingredient_inventory.v1"
    expression_ingredient_inventory_id: UUID = Field(default_factory=uuid4)
    ingredients: list[ExpressionIngredient] = Field(min_length=1)
    relation_edges: list[ExpressionRelationEdge] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    deterministic_inputs_hash: str = Field(min_length=12)


class CompositionHandoffPackage(BaseModel):
    schema_version: Literal["cmf.composition_handoff_package.v1"] = "cmf.composition_handoff_package.v1"
    composition_handoff_package_id: UUID = Field(default_factory=uuid4)
    target_compiler: Literal["carousel", "single_image", "supervisual", "video_edit", "two_d_character"]
    handoff_refs: list[str] = Field(min_length=1)
    required_receipt_refs: list[str] = Field(min_length=1)
    no_fabricated_guest_truth: bool = True


class ContentSequenceProgram(BaseModel):
    schema_version: Literal["cmf.content_sequence_program.v1"] = "cmf.content_sequence_program.v1"
    content_sequence_program_id: UUID = Field(default_factory=uuid4)
    sequencing_registry_kernel_id: UUID
    expression_ingredient_inventory_id: UUID
    handoff_packages: list[CompositionHandoffPackage] = Field(min_length=1)
    sequence_slots: list[dict[str, Any]] = Field(min_length=1)
    decision: AssetProgramCompilerDecision
    blocker_codes: list[str] = Field(default_factory=list)
    deterministic_inputs_hash: str = Field(min_length=12)


class SequenceEvalReceipt(BaseModel):
    schema_version: Literal["cmf.sequence_eval_receipt.v1"] = "cmf.sequence_eval_receipt.v1"
    sequence_eval_receipt_id: UUID = Field(default_factory=uuid4)
    content_sequence_program_id: UUID
    primitive_score: float = Field(ge=0, le=1)
    doctrine_score: float = Field(ge=0, le=1)
    decision: AssetProgramCompilerDecision
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class PackageLearningReceipt(BaseModel):
    schema_version: Literal["cmf.package_learning_receipt.v1"] = "cmf.package_learning_receipt.v1"
    package_learning_receipt_id: UUID = Field(default_factory=uuid4)
    sequence_eval_receipt_id: UUID
    learned_registry_updates: list[str] = Field(default_factory=list)
    approval_required: bool = True
    written_at: datetime = Field(default_factory=utc_now)


def compiler_hash(parts: Any) -> str:
    return runtime_hash(parts)
