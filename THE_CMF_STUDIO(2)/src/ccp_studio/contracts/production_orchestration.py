"""Batch 3 production orchestration contracts for TS-CMF-120 through TS-CMF-132."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.asset_program_compilers import compiler_hash
from ccp_studio.contracts.composition_runtime import CompositionDecision, RendererTarget
from ccp_studio.contracts.orchestration import utc_now


StageStatus = Literal["draft", "ready", "running", "blocked", "completed", "approved"]
ReferenceAdapterDecision = Literal["architectural_reference_only", "sandbox_adapter_allowed", "blocked"]
ProviderCapabilityKind = Literal["image_generation", "layer_decomposition", "masking", "rendering", "video_editing", "footage_retrieval", "qa", "storage"]
ApprovalDecision = Literal["approved", "rejected", "waived", "blocked"]
MediaUseMode = Literal["inspiration_reference", "source_footage", "b_roll", "brand_asset"]


class OpenMontageReferenceCandidate(BaseModel):
    schema_version: Literal["cmf.openmontage_reference_candidate.v1"] = "cmf.openmontage_reference_candidate.v1"
    openmontage_reference_candidate_id: UUID = Field(default_factory=uuid4)
    repo_url: str = Field(min_length=1)
    license_family: str = Field(min_length=1)
    proposed_patterns: list[str] = Field(min_length=1)
    source_evidence_refs: list[str] = Field(min_length=1)
    direct_import_requested: bool = False
    guest_data_execution_requested: bool = False


class OpenMontageAdapterDecisionReceipt(BaseModel):
    schema_version: Literal["cmf.openmontage_adapter_decision_receipt.v1"] = "cmf.openmontage_adapter_decision_receipt.v1"
    openmontage_adapter_decision_receipt_id: UUID = Field(default_factory=uuid4)
    candidate_id: UUID
    decision: ReferenceAdapterDecision
    adopted_patterns: list[str] = Field(default_factory=list)
    boundary_statement: str = Field(min_length=1)
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class ProductionStageSpec(BaseModel):
    schema_version: Literal["cmf.production_stage_spec.v1"] = "cmf.production_stage_spec.v1"
    stage_code: str = Field(min_length=1)
    stage_name: str = Field(min_length=1)
    owner_agent_ref: str = Field(min_length=1)
    allowed_skill_refs: list[str] = Field(min_length=1)
    allowed_tool_refs: list[str] = Field(min_length=1)
    required_input_refs: list[str] = Field(default_factory=list)
    required_output_artifact_types: list[str] = Field(min_length=1)
    required_receipt_types: list[str] = Field(min_length=1)
    approval_required: bool = True


class ProductionPipelineManifestDraft(BaseModel):
    schema_version: Literal["cmf.production_pipeline_manifest_draft.v1"] = "cmf.production_pipeline_manifest_draft.v1"
    production_pipeline_manifest_draft_id: UUID = Field(default_factory=uuid4)
    manifest_code: str = Field(min_length=1)
    project_type: Literal["interview_first_asset_pack", "existing_interview_asset_pack", "still_visual_program"]
    stage_specs: list[ProductionStageSpec] = Field(min_length=1)
    doctrine_refs: list[str] = Field(min_length=1)
    source_policy_refs: list[str] = Field(min_length=1)
    created_at: datetime = Field(default_factory=utc_now)


class ProductionPipelineManifestSnapshot(BaseModel):
    schema_version: Literal["cmf.production_pipeline_manifest_snapshot.v1"] = "cmf.production_pipeline_manifest_snapshot.v1"
    production_pipeline_manifest_snapshot_id: UUID = Field(default_factory=uuid4)
    draft_id: UUID
    manifest_code: str = Field(min_length=1)
    stage_specs: list[ProductionStageSpec] = Field(min_length=1)
    manifest_hash: str = Field(min_length=12)
    active: bool = False
    continuity_gate_passed: bool = False
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class ProductionManifestActivationReceipt(BaseModel):
    schema_version: Literal["cmf.production_manifest_activation_receipt.v1"] = "cmf.production_manifest_activation_receipt.v1"
    production_manifest_activation_receipt_id: UUID = Field(default_factory=uuid4)
    snapshot_id: UUID
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class StageDirectorSkillSpec(BaseModel):
    schema_version: Literal["cmf.stage_director_skill_spec.v1"] = "cmf.stage_director_skill_spec.v1"
    stage_director_skill_spec_id: UUID = Field(default_factory=uuid4)
    skill_ref: str = Field(min_length=1)
    stage_code: str = Field(min_length=1)
    responsibility: str = Field(min_length=1)
    allowed_tool_refs: list[str] = Field(min_length=1)
    required_context_refs: list[str] = Field(min_length=1)
    output_artifact_types: list[str] = Field(min_length=1)
    authority_boundary: str = Field(min_length=1)


class StageDirectorContextBundle(BaseModel):
    schema_version: Literal["cmf.stage_director_context_bundle.v1"] = "cmf.stage_director_context_bundle.v1"
    stage_director_context_bundle_id: UUID = Field(default_factory=uuid4)
    manifest_snapshot_id: UUID
    stage_code: str = Field(min_length=1)
    source_context_refs: list[str] = Field(min_length=1)
    provider_menu_ref: str | None = None
    workspace_ref: str | None = None


class StageSkillInvocationCommand(BaseModel):
    schema_version: Literal["cmf.stage_skill_invocation_command.v1"] = "cmf.stage_skill_invocation_command.v1"
    stage_skill_invocation_command_id: UUID = Field(default_factory=uuid4)
    skill_ref: str = Field(min_length=1)
    context_bundle_id: UUID
    requested_output_artifact_type: str = Field(min_length=1)
    command_ref: str = Field(min_length=1)


class StageSkillOutputEnvelope(BaseModel):
    schema_version: Literal["cmf.stage_skill_output_envelope.v1"] = "cmf.stage_skill_output_envelope.v1"
    stage_skill_output_envelope_id: UUID = Field(default_factory=uuid4)
    artifact_ref: str = Field(min_length=1)
    artifact_type: str = Field(min_length=1)
    source_refs: list[str] = Field(min_length=1)
    eval_refs: list[str] = Field(default_factory=list)
    deterministic_hash: str = Field(min_length=12)


class StageSkillInvocationReceipt(BaseModel):
    schema_version: Literal["cmf.stage_skill_invocation_receipt.v1"] = "cmf.stage_skill_invocation_receipt.v1"
    stage_skill_invocation_receipt_id: UUID = Field(default_factory=uuid4)
    command_id: UUID
    output_envelope_id: UUID | None = None
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class CapabilityRecord(BaseModel):
    schema_version: Literal["cmf.capability_record.v1"] = "cmf.capability_record.v1"
    capability_record_id: UUID = Field(default_factory=uuid4)
    provider_code: str = Field(min_length=1)
    capability_kind: ProviderCapabilityKind
    tool_ref: str = Field(min_length=1)
    cost_class: Literal["low", "medium", "high"]
    reproducibility_score: float = Field(ge=0, le=1)
    doctrine_fit_score: float = Field(ge=0, le=1)
    source_scope: Literal["internal", "external", "self_hosted"]
    available: bool = True
    blocker_codes: list[str] = Field(default_factory=list)


class ProviderMenuSnapshot(BaseModel):
    schema_version: Literal["cmf.provider_menu_snapshot.v1"] = "cmf.provider_menu_snapshot.v1"
    provider_menu_snapshot_id: UUID = Field(default_factory=uuid4)
    capability_records: list[CapabilityRecord] = Field(min_length=1)
    menu_hash: str = Field(min_length=12)
    unavailable_provider_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class ProviderAvailabilityGateReceipt(BaseModel):
    schema_version: Literal["cmf.provider_availability_gate_receipt.v1"] = "cmf.provider_availability_gate_receipt.v1"
    provider_availability_gate_receipt_id: UUID = Field(default_factory=uuid4)
    provider_menu_snapshot_id: UUID
    provider_code: str = Field(min_length=1)
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class CapabilityRouteRequest(BaseModel):
    schema_version: Literal["cmf.capability_route_request.v1"] = "cmf.capability_route_request.v1"
    capability_route_request_id: UUID = Field(default_factory=uuid4)
    required_capability_kind: ProviderCapabilityKind
    source_scope_allowed: list[Literal["internal", "external", "self_hosted"]] = Field(min_length=1)
    max_cost_class: Literal["low", "medium", "high"]
    minimum_reproducibility_score: float = Field(ge=0, le=1)
    minimum_doctrine_fit_score: float = Field(ge=0, le=1)
    evidence_refs: list[str] = Field(min_length=1)


class ProviderCandidateScore(BaseModel):
    schema_version: Literal["cmf.provider_candidate_score.v1"] = "cmf.provider_candidate_score.v1"
    capability_record_id: UUID
    provider_code: str = Field(min_length=1)
    score: float = Field(ge=0, le=1)
    criteria_scores: dict[str, float] = Field(default_factory=dict)
    blocker_codes: list[str] = Field(default_factory=list)


class ProviderRouteDecisionReceipt(BaseModel):
    schema_version: Literal["cmf.provider_route_decision_receipt.v1"] = "cmf.provider_route_decision_receipt.v1"
    provider_route_decision_receipt_id: UUID = Field(default_factory=uuid4)
    capability_route_request_id: UUID
    selected_provider_code: str | None = None
    candidate_scores: list[ProviderCandidateScore] = Field(default_factory=list)
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class ProductionWorkspace(BaseModel):
    schema_version: Literal["cmf.production_workspace.v1"] = "cmf.production_workspace.v1"
    production_workspace_id: UUID = Field(default_factory=uuid4)
    organization_id: UUID
    brand_id: UUID
    guest_id: UUID | None = None
    manifest_snapshot_id: UUID
    workspace_ref: str = Field(min_length=1)
    object_storage_prefix: str = Field(min_length=1)
    artifact_slot_refs: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class WorkspaceArtifactSlot(BaseModel):
    schema_version: Literal["cmf.workspace_artifact_slot.v1"] = "cmf.workspace_artifact_slot.v1"
    workspace_artifact_slot_id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    stage_code: str = Field(min_length=1)
    artifact_type: str = Field(min_length=1)
    artifact_ref: str = Field(min_length=1)
    receipt_refs: list[str] = Field(default_factory=list)


class WorkspaceCheckpoint(BaseModel):
    schema_version: Literal["cmf.workspace_checkpoint.v1"] = "cmf.workspace_checkpoint.v1"
    workspace_checkpoint_id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    stage_code: str = Field(min_length=1)
    checkpoint_state_hash: str = Field(min_length=12)
    valid: bool = True
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class WorkspaceResumeDecision(BaseModel):
    schema_version: Literal["cmf.workspace_resume_decision.v1"] = "cmf.workspace_resume_decision.v1"
    workspace_resume_decision_id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    checkpoint_id: UUID | None = None
    decision: Literal["resume", "restart", "blocked"]
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class ReferenceMediaIntakeRecord(BaseModel):
    schema_version: Literal["cmf.reference_media_intake_record.v1"] = "cmf.reference_media_intake_record.v1"
    reference_media_intake_record_id: UUID = Field(default_factory=uuid4)
    media_ref: str = Field(min_length=1)
    declared_use_mode: MediaUseMode
    source_evidence_refs: list[str] = Field(min_length=1)
    consent_scope_ref: str | None = None
    media_hash: str = Field(min_length=12)


class ReferenceMediaClassificationReceipt(BaseModel):
    schema_version: Literal["cmf.reference_media_classification_receipt.v1"] = "cmf.reference_media_classification_receipt.v1"
    reference_media_classification_receipt_id: UUID = Field(default_factory=uuid4)
    record_id: UUID
    classified_use_mode: MediaUseMode
    downstream_use_allowed: bool
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class ReferenceMediaInspectionReceipt(BaseModel):
    schema_version: Literal["cmf.reference_media_inspection_receipt.v1"] = "cmf.reference_media_inspection_receipt.v1"
    reference_media_inspection_receipt_id: UUID = Field(default_factory=uuid4)
    record_id: UUID
    duration_seconds: float = Field(gt=0)
    resolution: str = Field(min_length=1)
    audio_present: bool
    transcription_ready: bool
    composition_lessons: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class FootageSearchRequest(BaseModel):
    schema_version: Literal["cmf.footage_search_request.v1"] = "cmf.footage_search_request.v1"
    footage_search_request_id: UUID = Field(default_factory=uuid4)
    query: str = Field(min_length=1)
    visual_role: str = Field(min_length=1)
    source_evidence_refs: list[str] = Field(min_length=1)
    allowed_license_families: list[str] = Field(min_length=1)


class FootageCandidate(BaseModel):
    schema_version: Literal["cmf.footage_candidate.v1"] = "cmf.footage_candidate.v1"
    footage_candidate_id: UUID = Field(default_factory=uuid4)
    search_request_id: UUID
    source_url: str = Field(min_length=1)
    license_family: str = Field(min_length=1)
    media_hash: str = Field(min_length=12)
    relevance_score: float = Field(ge=0, le=1)
    visual_role: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)


class FootageSelectionReceipt(BaseModel):
    schema_version: Literal["cmf.footage_selection_receipt.v1"] = "cmf.footage_selection_receipt.v1"
    footage_selection_receipt_id: UUID = Field(default_factory=uuid4)
    candidate_id: UUID
    selected: bool
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class RenderRuntimeCandidate(BaseModel):
    schema_version: Literal["cmf.render_runtime_candidate.v1"] = "cmf.render_runtime_candidate.v1"
    runtime_code: RendererTarget
    supported_output_types: list[str] = Field(min_length=1)
    deterministic_replay_score: float = Field(ge=0, le=1)
    cost_class: Literal["low", "medium", "high"]
    available: bool = True


class RenderRuntimeSelectionRequest(BaseModel):
    schema_version: Literal["cmf.render_runtime_selection_request.v1"] = "cmf.render_runtime_selection_request.v1"
    render_runtime_selection_request_id: UUID = Field(default_factory=uuid4)
    output_type: str = Field(min_length=1)
    source_program_ref: str = Field(min_length=1)
    allowed_runtime_codes: list[RendererTarget] = Field(min_length=1)
    minimum_replay_score: float = Field(ge=0, le=1)


class RenderRuntimeLock(BaseModel):
    schema_version: Literal["cmf.render_runtime_lock.v1"] = "cmf.render_runtime_lock.v1"
    render_runtime_lock_id: UUID = Field(default_factory=uuid4)
    selection_request_id: UUID
    runtime_code: RendererTarget
    locked_runtime_hash: str = Field(min_length=12)
    locked_dependency_refs: list[str] = Field(min_length=1)
    final_render_allowed: bool = True
    written_at: datetime = Field(default_factory=utc_now)


class RenderRuntimeDriftReceipt(BaseModel):
    schema_version: Literal["cmf.render_runtime_drift_receipt.v1"] = "cmf.render_runtime_drift_receipt.v1"
    render_runtime_drift_receipt_id: UUID = Field(default_factory=uuid4)
    render_runtime_lock_id: UUID
    observed_runtime_hash: str = Field(min_length=12)
    drift_detected: bool
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class DeliveryPromise(BaseModel):
    schema_version: Literal["cmf.delivery_promise.v1"] = "cmf.delivery_promise.v1"
    delivery_promise_id: UUID = Field(default_factory=uuid4)
    source_program_ref: str = Field(min_length=1)
    promised_format: str = Field(min_length=1)
    composition_family_ref: str = Field(min_length=1)
    required_runtime_lock_ref: str = Field(min_length=1)
    required_eval_refs: list[str] = Field(min_length=1)


class PreComposeRiskGateReceipt(BaseModel):
    schema_version: Literal["cmf.pre_compose_risk_gate_receipt.v1"] = "cmf.pre_compose_risk_gate_receipt.v1"
    pre_compose_risk_gate_receipt_id: UUID = Field(default_factory=uuid4)
    delivery_promise_id: UUID
    risk_score: float = Field(ge=0, le=1)
    slideshow_risk: bool
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class PreComposeRepairPlan(BaseModel):
    schema_version: Literal["cmf.pre_compose_repair_plan.v1"] = "cmf.pre_compose_repair_plan.v1"
    pre_compose_repair_plan_id: UUID = Field(default_factory=uuid4)
    pre_compose_risk_gate_receipt_id: UUID
    repair_actions: list[str] = Field(min_length=1)
    approval_required: bool = True


class RenderedAssetReviewRequest(BaseModel):
    schema_version: Literal["cmf.rendered_asset_review_request.v1"] = "cmf.rendered_asset_review_request.v1"
    rendered_asset_review_request_id: UUID = Field(default_factory=uuid4)
    render_ref: str = Field(min_length=1)
    runtime_lock_ref: str = Field(min_length=1)
    source_program_ref: str = Field(min_length=1)
    expected_render_hash: str = Field(min_length=12)


class MediaProbeResult(BaseModel):
    schema_version: Literal["cmf.media_probe_result.v1"] = "cmf.media_probe_result.v1"
    media_probe_result_id: UUID = Field(default_factory=uuid4)
    render_ref: str = Field(min_length=1)
    observed_render_hash: str = Field(min_length=12)
    duration_seconds: float = Field(gt=0)
    resolution: str = Field(min_length=1)
    text_overlap_detected: bool = False
    blank_frame_detected: bool = False


class PostRenderQAReceipt(BaseModel):
    schema_version: Literal["cmf.post_render_qa_receipt.v1"] = "cmf.post_render_qa_receipt.v1"
    post_render_qa_receipt_id: UUID = Field(default_factory=uuid4)
    rendered_asset_review_request_id: UUID
    media_probe_result_id: UUID
    score: float = Field(ge=0, le=1)
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    repair_command_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class RenderRepairCommand(BaseModel):
    schema_version: Literal["cmf.render_repair_command.v1"] = "cmf.render_repair_command.v1"
    render_repair_command_id: UUID = Field(default_factory=uuid4)
    post_render_qa_receipt_id: UUID
    repair_scope: list[str] = Field(min_length=1)
    command_ref: str = Field(min_length=1)


class BudgetCostEstimate(BaseModel):
    schema_version: Literal["cmf.budget_cost_estimate.v1"] = "cmf.budget_cost_estimate.v1"
    budget_cost_estimate_id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    provider_code: str = Field(min_length=1)
    estimated_units: float = Field(ge=0)
    estimated_cost_usd: float = Field(ge=0)
    cap_usd: float = Field(ge=0)
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)


class BudgetReservationReceipt(BaseModel):
    schema_version: Literal["cmf.budget_reservation_receipt.v1"] = "cmf.budget_reservation_receipt.v1"
    budget_reservation_receipt_id: UUID = Field(default_factory=uuid4)
    budget_cost_estimate_id: UUID
    reserved_cost_usd: float = Field(ge=0)
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class BudgetReconciliationReceipt(BaseModel):
    schema_version: Literal["cmf.budget_reconciliation_receipt.v1"] = "cmf.budget_reconciliation_receipt.v1"
    budget_reconciliation_receipt_id: UUID = Field(default_factory=uuid4)
    budget_reservation_receipt_id: UUID
    actual_cost_usd: float = Field(ge=0)
    variance_usd: float
    decision: CompositionDecision
    blocker_codes: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


class CanonicalStageArtifact(BaseModel):
    schema_version: Literal["cmf.canonical_stage_artifact.v1"] = "cmf.canonical_stage_artifact.v1"
    canonical_stage_artifact_id: UUID = Field(default_factory=uuid4)
    workspace_id: UUID
    stage_code: str = Field(min_length=1)
    artifact_type: str = Field(min_length=1)
    artifact_ref: str = Field(min_length=1)
    source_refs: list[str] = Field(min_length=1)
    eval_receipt_refs: list[str] = Field(default_factory=list)
    render_receipt_refs: list[str] = Field(default_factory=list)


class StageArtifactReviewRequest(BaseModel):
    schema_version: Literal["cmf.stage_artifact_review_request.v1"] = "cmf.stage_artifact_review_request.v1"
    stage_artifact_review_request_id: UUID = Field(default_factory=uuid4)
    artifact_id: UUID
    reviewer_id: UUID
    required_human_approval: bool = True
    requested_at: datetime = Field(default_factory=utc_now)


class ReviewerFinding(BaseModel):
    schema_version: Literal["cmf.reviewer_finding.v1"] = "cmf.reviewer_finding.v1"
    reviewer_finding_id: UUID = Field(default_factory=uuid4)
    review_request_id: UUID
    severity: Literal["info", "warning", "critical"]
    finding_code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    waived: bool = False


class HumanApprovalReceipt(BaseModel):
    schema_version: Literal["cmf.human_approval_receipt.v1"] = "cmf.human_approval_receipt.v1"
    human_approval_receipt_id: UUID = Field(default_factory=uuid4)
    review_request_id: UUID
    reviewer_id: UUID
    decision: ApprovalDecision
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime = Field(default_factory=utc_now)


def production_hash(parts: Any) -> str:
    return compiler_hash(parts)
