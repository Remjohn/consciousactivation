// Generated consumer-facing production orchestration contracts for TS-CMF-120 through TS-CMF-132.

export type CompositionDecision = "approved" | "blocked" | "repair_required";
export type ApprovalDecision = "approved" | "rejected" | "waived" | "blocked";
export type ReferenceAdapterDecision = "architectural_reference_only" | "sandbox_adapter_allowed" | "blocked";
export type ProviderCapabilityKind =
  | "image_generation"
  | "layer_decomposition"
  | "masking"
  | "rendering"
  | "video_editing"
  | "footage_retrieval"
  | "qa"
  | "storage";
export type SourceScope = "internal" | "external" | "self_hosted";
export type CostClass = "low" | "medium" | "high";
export type RendererTarget = "remotion" | "motion_canvas" | "skia" | "manim" | "ffmpeg" | "open_timeline_io";
export type MediaUseMode = "inspiration_reference" | "source_footage" | "b_roll" | "brand_asset";

export interface OpenMontageReferenceCandidate {
  schema_version: "cmf.openmontage_reference_candidate.v1";
  openmontage_reference_candidate_id: string;
  repo_url: string;
  license_family: string;
  proposed_patterns: string[];
  source_evidence_refs: string[];
  direct_import_requested: boolean;
  guest_data_execution_requested: boolean;
}

export interface OpenMontageAdapterDecisionReceipt {
  schema_version: "cmf.openmontage_adapter_decision_receipt.v1";
  openmontage_adapter_decision_receipt_id: string;
  candidate_id: string;
  decision: ReferenceAdapterDecision;
  adopted_patterns: string[];
  boundary_statement: string;
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}

export interface ProductionStageSpec {
  schema_version: "cmf.production_stage_spec.v1";
  stage_code: string;
  stage_name: string;
  owner_agent_ref: string;
  allowed_skill_refs: string[];
  allowed_tool_refs: string[];
  required_input_refs: string[];
  required_output_artifact_types: string[];
  required_receipt_types: string[];
  approval_required: boolean;
}

export interface ProductionPipelineManifestDraft {
  schema_version: "cmf.production_pipeline_manifest_draft.v1";
  production_pipeline_manifest_draft_id: string;
  manifest_code: string;
  project_type: "interview_first_asset_pack" | "existing_interview_asset_pack" | "still_visual_program";
  stage_specs: ProductionStageSpec[];
  doctrine_refs: string[];
  source_policy_refs: string[];
  created_at: string;
}

export interface ProductionPipelineManifestSnapshot {
  schema_version: "cmf.production_pipeline_manifest_snapshot.v1";
  production_pipeline_manifest_snapshot_id: string;
  draft_id: string;
  manifest_code: string;
  stage_specs: ProductionStageSpec[];
  manifest_hash: string;
  active: boolean;
  continuity_gate_passed: boolean;
  blocker_codes: string[];
  written_at: string;
}

export interface ProductionManifestActivationReceipt {
  schema_version: "cmf.production_manifest_activation_receipt.v1";
  production_manifest_activation_receipt_id: string;
  snapshot_id: string;
  decision: CompositionDecision;
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}

export interface StageDirectorSkillSpec {
  schema_version: "cmf.stage_director_skill_spec.v1";
  stage_director_skill_spec_id: string;
  skill_ref: string;
  stage_code: string;
  responsibility: string;
  allowed_tool_refs: string[];
  required_context_refs: string[];
  output_artifact_types: string[];
  authority_boundary: string;
}

export interface StageDirectorContextBundle {
  schema_version: "cmf.stage_director_context_bundle.v1";
  stage_director_context_bundle_id: string;
  manifest_snapshot_id: string;
  stage_code: string;
  source_context_refs: string[];
  provider_menu_ref?: string | null;
  workspace_ref?: string | null;
}

export interface StageSkillInvocationCommand {
  schema_version: "cmf.stage_skill_invocation_command.v1";
  stage_skill_invocation_command_id: string;
  skill_ref: string;
  context_bundle_id: string;
  requested_output_artifact_type: string;
  command_ref: string;
}

export interface StageSkillOutputEnvelope {
  schema_version: "cmf.stage_skill_output_envelope.v1";
  stage_skill_output_envelope_id: string;
  artifact_ref: string;
  artifact_type: string;
  source_refs: string[];
  eval_refs: string[];
  deterministic_hash: string;
}

export interface StageSkillInvocationReceipt {
  schema_version: "cmf.stage_skill_invocation_receipt.v1";
  stage_skill_invocation_receipt_id: string;
  command_id: string;
  output_envelope_id?: string | null;
  decision: CompositionDecision;
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}

export interface CapabilityRecord {
  schema_version: "cmf.capability_record.v1";
  capability_record_id: string;
  provider_code: string;
  capability_kind: ProviderCapabilityKind;
  tool_ref: string;
  cost_class: CostClass;
  reproducibility_score: number;
  doctrine_fit_score: number;
  source_scope: SourceScope;
  available: boolean;
  blocker_codes: string[];
}

export interface ProviderMenuSnapshot {
  schema_version: "cmf.provider_menu_snapshot.v1";
  provider_menu_snapshot_id: string;
  capability_records: CapabilityRecord[];
  menu_hash: string;
  unavailable_provider_codes: string[];
  written_at: string;
}

export interface CapabilityRouteRequest {
  schema_version: "cmf.capability_route_request.v1";
  capability_route_request_id: string;
  required_capability_kind: ProviderCapabilityKind;
  source_scope_allowed: SourceScope[];
  max_cost_class: CostClass;
  minimum_reproducibility_score: number;
  minimum_doctrine_fit_score: number;
  evidence_refs: string[];
}

export interface ProviderCandidateScore {
  schema_version: "cmf.provider_candidate_score.v1";
  capability_record_id: string;
  provider_code: string;
  score: number;
  criteria_scores: Record<string, number>;
  blocker_codes: string[];
}

export interface ProviderRouteDecisionReceipt {
  schema_version: "cmf.provider_route_decision_receipt.v1";
  provider_route_decision_receipt_id: string;
  capability_route_request_id: string;
  selected_provider_code?: string | null;
  candidate_scores: ProviderCandidateScore[];
  decision: CompositionDecision;
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}

export interface ProductionWorkspace {
  schema_version: "cmf.production_workspace.v1";
  production_workspace_id: string;
  organization_id: string;
  brand_id: string;
  guest_id?: string | null;
  manifest_snapshot_id: string;
  workspace_ref: string;
  object_storage_prefix: string;
  artifact_slot_refs: string[];
  created_at: string;
}

export interface WorkspaceArtifactSlot {
  schema_version: "cmf.workspace_artifact_slot.v1";
  workspace_artifact_slot_id: string;
  workspace_id: string;
  stage_code: string;
  artifact_type: string;
  artifact_ref: string;
  receipt_refs: string[];
}

export interface WorkspaceCheckpoint {
  schema_version: "cmf.workspace_checkpoint.v1";
  workspace_checkpoint_id: string;
  workspace_id: string;
  stage_code: string;
  checkpoint_state_hash: string;
  valid: boolean;
  blocker_codes: string[];
  written_at: string;
}

export interface WorkspaceResumeDecision {
  schema_version: "cmf.workspace_resume_decision.v1";
  workspace_resume_decision_id: string;
  workspace_id: string;
  checkpoint_id?: string | null;
  decision: "resume" | "restart" | "blocked";
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}

export interface ReferenceMediaIntakeRecord {
  schema_version: "cmf.reference_media_intake_record.v1";
  reference_media_intake_record_id: string;
  media_ref: string;
  declared_use_mode: MediaUseMode;
  source_evidence_refs: string[];
  consent_scope_ref?: string | null;
  media_hash: string;
}

export interface ReferenceMediaClassificationReceipt {
  schema_version: "cmf.reference_media_classification_receipt.v1";
  reference_media_classification_receipt_id: string;
  record_id: string;
  classified_use_mode: MediaUseMode;
  downstream_use_allowed: boolean;
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}

export interface ReferenceMediaInspectionReceipt {
  schema_version: "cmf.reference_media_inspection_receipt.v1";
  reference_media_inspection_receipt_id: string;
  record_id: string;
  duration_seconds: number;
  resolution: string;
  audio_present: boolean;
  transcription_ready: boolean;
  composition_lessons: string[];
  blocker_codes: string[];
  written_at: string;
}

export interface FootageSearchRequest {
  schema_version: "cmf.footage_search_request.v1";
  footage_search_request_id: string;
  query: string;
  visual_role: string;
  source_evidence_refs: string[];
  allowed_license_families: string[];
}

export interface FootageCandidate {
  schema_version: "cmf.footage_candidate.v1";
  footage_candidate_id: string;
  search_request_id: string;
  source_url: string;
  license_family: string;
  media_hash: string;
  relevance_score: number;
  visual_role: string;
  evidence_refs: string[];
}

export interface FootageSelectionReceipt {
  schema_version: "cmf.footage_selection_receipt.v1";
  footage_selection_receipt_id: string;
  candidate_id: string;
  selected: boolean;
  decision: CompositionDecision;
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}

export interface RenderRuntimeCandidate {
  schema_version: "cmf.render_runtime_candidate.v1";
  runtime_code: RendererTarget;
  supported_output_types: string[];
  deterministic_replay_score: number;
  cost_class: CostClass;
  available: boolean;
}

export interface RenderRuntimeSelectionRequest {
  schema_version: "cmf.render_runtime_selection_request.v1";
  render_runtime_selection_request_id: string;
  output_type: string;
  source_program_ref: string;
  allowed_runtime_codes: RendererTarget[];
  minimum_replay_score: number;
}

export interface RenderRuntimeLock {
  schema_version: "cmf.render_runtime_lock.v1";
  render_runtime_lock_id: string;
  selection_request_id: string;
  runtime_code: RendererTarget;
  locked_runtime_hash: string;
  locked_dependency_refs: string[];
  final_render_allowed: boolean;
  written_at: string;
}

export interface RenderRuntimeDriftReceipt {
  schema_version: "cmf.render_runtime_drift_receipt.v1";
  render_runtime_drift_receipt_id: string;
  render_runtime_lock_id: string;
  observed_runtime_hash: string;
  drift_detected: boolean;
  decision: CompositionDecision;
  blocker_codes: string[];
  written_at: string;
}

export interface PreComposeRiskGateReceipt {
  schema_version: "cmf.pre_compose_risk_gate_receipt.v1";
  pre_compose_risk_gate_receipt_id: string;
  delivery_promise_id: string;
  risk_score: number;
  slideshow_risk: boolean;
  decision: CompositionDecision;
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}

export interface PreComposeRepairPlan {
  schema_version: "cmf.pre_compose_repair_plan.v1";
  pre_compose_repair_plan_id: string;
  pre_compose_risk_gate_receipt_id: string;
  repair_actions: string[];
  approval_required: boolean;
}

export interface PostRenderQAReceipt {
  schema_version: "cmf.post_render_qa_receipt.v1";
  post_render_qa_receipt_id: string;
  rendered_asset_review_request_id: string;
  media_probe_result_id: string;
  score: number;
  decision: CompositionDecision;
  blocker_codes: string[];
  repair_command_refs: string[];
  written_at: string;
}

export interface RenderRepairCommand {
  schema_version: "cmf.render_repair_command.v1";
  render_repair_command_id: string;
  post_render_qa_receipt_id: string;
  repair_scope: string[];
  command_ref: string;
}

export interface BudgetCostEstimate {
  schema_version: "cmf.budget_cost_estimate.v1";
  budget_cost_estimate_id: string;
  workspace_id: string;
  provider_code: string;
  estimated_units: number;
  estimated_cost_usd: number;
  cap_usd: number;
  decision: CompositionDecision;
  blocker_codes: string[];
}

export interface BudgetReservationReceipt {
  schema_version: "cmf.budget_reservation_receipt.v1";
  budget_reservation_receipt_id: string;
  budget_cost_estimate_id: string;
  reserved_cost_usd: number;
  decision: CompositionDecision;
  blocker_codes: string[];
  written_at: string;
}

export interface BudgetReconciliationReceipt {
  schema_version: "cmf.budget_reconciliation_receipt.v1";
  budget_reconciliation_receipt_id: string;
  budget_reservation_receipt_id: string;
  actual_cost_usd: number;
  variance_usd: number;
  decision: CompositionDecision;
  blocker_codes: string[];
  written_at: string;
}

export interface CanonicalStageArtifact {
  schema_version: "cmf.canonical_stage_artifact.v1";
  canonical_stage_artifact_id: string;
  workspace_id: string;
  stage_code: string;
  artifact_type: string;
  artifact_ref: string;
  source_refs: string[];
  eval_receipt_refs: string[];
  render_receipt_refs: string[];
}

export interface StageArtifactReviewRequest {
  schema_version: "cmf.stage_artifact_review_request.v1";
  stage_artifact_review_request_id: string;
  artifact_id: string;
  reviewer_id: string;
  required_human_approval: boolean;
  requested_at: string;
}

export interface ReviewerFinding {
  schema_version: "cmf.reviewer_finding.v1";
  reviewer_finding_id: string;
  review_request_id: string;
  severity: "info" | "warning" | "critical";
  finding_code: string;
  message: string;
  waived: boolean;
}

export interface HumanApprovalReceipt {
  schema_version: "cmf.human_approval_receipt.v1";
  human_approval_receipt_id: string;
  review_request_id: string;
  reviewer_id: string;
  decision: ApprovalDecision;
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}
