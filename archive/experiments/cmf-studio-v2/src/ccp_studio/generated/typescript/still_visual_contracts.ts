// Generated consumer-facing still visual and SuperVisual contracts for TS-CMF-133 through TS-CMF-135.

export type CompositionDecision = "approved" | "blocked" | "repair_required";
export type ApprovalStatus = "draft" | "blocked" | "approved";
export type StillVisualFormatFamily = "carousel" | "supervisual" | "visual_poll" | "tweet_quote" | "meme" | "reaction_still";
export type StillVisualStageCode = "request" | "route" | "materialize" | "render" | "evaluate" | "review" | "approval" | "export";
export type StillVisualStageStatus = "pending" | "ready" | "completed" | "blocked" | "waived";
export type SuperVisualSubtype = "SPV-CON" | "SPV-SYM" | "SPV-PRM";

export interface PrimitiveTriadContract {
  schema_version: "cmf.primitive_triad_contract.v1";
  primitive_id: string;
  canonical_name: string;
  role: "meaning_transform" | "delivery_shape" | "format_material";
  evidence_ref: string;
}

export interface SuperVisualGrammarRecord {
  schema_version: "cmf.supervisual_grammar_record.v1";
  supervisual_grammar_record_id: string;
  grammar_code: string;
  subtype: SuperVisualSubtype;
  display_name: string;
  composition_purpose: string;
  required_zones: string[];
  required_contrast_axes: string[];
  symbol_explanation_required: boolean;
  authority_evidence_required: boolean;
  skia_scene_obligations: string[];
  primitive_triads: PrimitiveTriadContract[];
}

export interface SuperVisualFeelMatrixEntry {
  schema_version: "cmf.supervisual_feel_matrix_entry.v1";
  subtype: SuperVisualSubtype;
  required_feel: string;
  must_avoid: string[];
  minimum_primitive_score: number;
}

export interface SuperVisualGrammarRouteRequest {
  schema_version: "cmf.supervisual_grammar_route_request.v1";
  supervisual_grammar_route_request_id: string;
  program_ref: string;
  brand_context_ref: string;
  archetype_ref: string;
  target_subtype_hint?: SuperVisualSubtype | null;
  platform: "instagram" | "linkedin" | "youtube_shorts" | "x";
  source_evidence_refs: string[];
}

export interface SuperVisualGrammarRouteDecision {
  schema_version: "cmf.supervisual_grammar_route_decision.v1";
  supervisual_grammar_route_decision_id: string;
  route_request_id: string;
  selected_grammar_code: string;
  selected_subtype: SuperVisualSubtype;
  primitive_coverage_ids: string[];
  feel_matrix_ref: string;
  skia_scene_obligation_refs: string[];
  decision_code: string;
  blocker_codes: string[];
  written_at: string;
}

export interface SuperVisualPrimitiveCoverageReceipt {
  schema_version: "cmf.supervisual_primitive_coverage_receipt.v1";
  supervisual_primitive_coverage_receipt_id: string;
  route_decision_id: string;
  primitive_score: number;
  role_coverage: Record<string, boolean>;
  decision_code: string;
  blocker_codes: string[];
  written_at: string;
}

export interface StillVisualCompositionRequest {
  schema_version: "cmf.still_visual_composition_request.v1";
  still_visual_composition_request_id: string;
  workspace_id: string;
  brand_context_version_ref: string;
  source_evidence_refs: string[];
  target_format_family: StillVisualFormatFamily;
  package_slot: string;
  content_sequence_program_ref?: string | null;
  platform: "instagram" | "linkedin" | "youtube_shorts" | "x";
}

export interface StillVisualStageState {
  schema_version: "cmf.still_visual_stage_state.v1";
  stage_code: StillVisualStageCode;
  status: StillVisualStageStatus;
  artifact_refs: string[];
  receipt_refs: string[];
  blocker_codes: string[];
  updated_at: string;
}

export interface StillVisualFamilyRoute {
  schema_version: "cmf.still_visual_family_route.v1";
  still_visual_family_route_id: string;
  program_id: string;
  selected_family: StillVisualFormatFamily;
  selected_builder_ref: string;
  atlas_binding_ref: string;
  grammar_binding_ref?: string | null;
  primitive_validation_ids: string[];
  decision_code: string;
  blocker_codes: string[];
  written_at: string;
}

export interface ProviderMaterializationPlan {
  schema_version: "cmf.provider_materialization_plan.v1";
  provider_materialization_plan_id: string;
  program_id: string;
  provider_job_refs: string[];
  layer_materialization_refs: string[];
  final_authority: "cmf_skia_renderer";
  decision_code: string;
  blocker_codes: string[];
}

export interface StillVisualRenderManifest {
  schema_version: "cmf.still_visual_render_manifest.v1";
  still_visual_render_manifest_id: string;
  program_id: string;
  skia_scene_ref: string;
  runtime_lock_ref: string;
  render_ref: string;
  render_hash: string;
  deterministic_replay_required: boolean;
}

export interface StillVisualEvalSummary {
  schema_version: "cmf.still_visual_eval_summary.v1";
  still_visual_eval_summary_id: string;
  program_id: string;
  primitive_score: number;
  doctrine_score: number;
  grammar_score: number;
  source_truth_score: number;
  platform_fit_score: number;
  decision: CompositionDecision;
  blocker_codes: string[];
  receipt_refs: string[];
}

export interface StillVisualCompositionProgram {
  schema_version: "cmf.still_visual_composition_program.v1";
  still_visual_composition_program_id: string;
  request: StillVisualCompositionRequest;
  manifest_snapshot_ref: string;
  stage_states: StillVisualStageState[];
  family_route?: StillVisualFamilyRoute | null;
  provider_plan?: ProviderMaterializationPlan | null;
  render_manifest?: StillVisualRenderManifest | null;
  eval_summary?: StillVisualEvalSummary | null;
  approval_status: ApprovalStatus;
  blocker_codes: string[];
  program_hash: string;
  created_at: string;
}

export interface StillVisualReviewReadModel {
  schema_version: "cmf.still_visual_review_read_model.v1";
  still_visual_review_read_model_id: string;
  program_id: string;
  approval_status: ApprovalStatus;
  stage_states: StillVisualStageState[];
  preview_refs: string[];
  blockers: string[];
  repair_commands: string[];
  approval_eligible: boolean;
  updated_at: string;
}

export interface TelegramStillVisualReviewCard {
  schema_version: "cmf.telegram_still_visual_review_card.v1";
  telegram_still_visual_review_card_id: string;
  program_id: string;
  title: string;
  preview_ref: string;
  blocker_count: number;
  commands: string[];
}

export interface StillVisualApprovalReceipt {
  schema_version: "cmf.still_visual_approval_receipt.v1";
  still_visual_approval_receipt_id: string;
  program_id: string;
  operator_id: string;
  decision: CompositionDecision;
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}

export interface StillVisualRevisionCommand {
  schema_version: "cmf.still_visual_revision_command.v1";
  still_visual_revision_command_id: string;
  program_id: string;
  revision_scope: "route" | "provider" | "layer" | "text" | "primitive" | "render" | "export";
  reason: string;
  command_ref: string;
  created_at: string;
}

export interface StillVisualExportManifest {
  schema_version: "cmf.still_visual_export_manifest.v1";
  still_visual_export_manifest_id: string;
  program_id: string;
  exported_asset_refs: string[];
  package_handoff_ref: string;
  approval_receipt_ref: string;
  written_at: string;
}
