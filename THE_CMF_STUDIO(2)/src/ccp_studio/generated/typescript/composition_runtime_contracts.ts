// Generated consumer-facing composition runtime contracts for TS-CMF-072 through TS-CMF-092.

export type CMFVideoFormatCode = "SV-CSC" | "SV-EDU" | "SV-FRB" | "SV-RRC";
export type CompositionDecision = "approved" | "blocked" | "repair_required";
export type ApprovalStatus = "draft" | "blocked" | "repair_required" | "approved";
export type AdapterDecision = "approved_adapter" | "sandbox_only" | "rejected";

export interface CompositionZone {
  schema_version: "cmf.composition_zone.v1";
  zone_id: string;
  role: string;
  x: number;
  y: number;
  width: number;
  height: number;
  safe_area: boolean;
  timing_ref?: string | null;
}

export interface CompositionTemplateLayer {
  schema_version: "cmf.composition_template_layer.v1";
  layer_id: string;
  layer_type: string;
  zone_id: string;
  source_ref: string;
  z_index: number;
  editable: boolean;
  timing_ref?: string | null;
  style_tokens: string[];
}

export interface CompositionTemplateJson {
  schema_version: "cmf.composition_template_json.v1";
  composition_template_id: string;
  template_family_code: string;
  content_format_code: string;
  aspect_ratio: string;
  width: number;
  height: number;
  fps: number;
  duration_seconds: number;
  zones: CompositionZone[];
  layers: CompositionTemplateLayer[];
  source_lineage_refs: string[];
  primitive_validation_ids: string[];
  visual_feel_contract_id?: string | null;
  preview_asset_refs: string[];
  composition_json_hash: string;
  approval_status: ApprovalStatus;
}

export interface SceneTemplateBinding {
  schema_version: "cmf.scene_template_binding.v1";
  scene_template_binding_id: string;
  scene_spec_id: string;
  reaction_template_route_id?: string | null;
  template_code: string;
  content_format_code: string;
  scene_pattern: string;
  renderer_route: string;
  composition_id: string;
  live_clip_slots: Record<string, unknown>[];
  motion_grammar: Record<string, unknown>;
  primitive_eval_obligations: string[];
  source_lineage_refs: string[];
  created_at: string;
}

export interface CompositionApprovalBlocker {
  schema_version: "cmf.composition_approval_blocker.v1";
  blocker_code: string;
  severity: "soft" | "hard";
  message: string;
  evidence_refs: string[];
}

export interface CompositionApprovalReadModel {
  schema_version: "cmf.composition_approval_read_model.v1";
  review_read_model_id: string;
  scene_template_binding: SceneTemplateBinding;
  composition_template: CompositionTemplateJson;
  preview_refs: string[];
  eval_receipt_refs: string[];
  blockers: CompositionApprovalBlocker[];
  approval_status: ApprovalStatus;
  operator_commands: string[];
  updated_at: string;
}

export interface PrimitiveValidationResult {
  schema_version: "cmf.primitive_validation_result.v1";
  primitive_id: string;
  primitive_name: string;
  role: "meaning_transform" | "delivery_shape" | "format_material";
  score: number;
  threshold: number;
  evidence_ref: string;
  composition_element_ref: string;
  decision: "pass" | "fail";
}

export interface CompositionPreflightReceipt {
  schema_version: "cmf.composition_preflight_receipt.v1";
  composition_preflight_receipt_id: string;
  composition_id: string;
  route_id: CMFVideoFormatCode;
  visual_feel_contract_id: string;
  minimum_validated_primitives: number;
  primitive_validation_count: number;
  primitive_results: PrimitiveValidationResult[];
  role_coverage: Record<string, boolean>;
  hard_failure_codes: string[];
  decision: CompositionDecision;
  written_at: string;
}

export interface IntegrationAdapterDecision {
  schema_version: "cmf.integration_adapter_decision.v1";
  integration_adapter_decision_id: string;
  integration_candidate_id: string;
  decision: AdapterDecision;
  score: number;
  criteria_scores: Record<string, number>;
  adapter_boundary: string;
  sandbox_required: boolean;
  blocker_codes: string[];
  evidence_refs: string[];
  written_at: string;
}

export interface ReviewReadModel {
  schema_version: "cmf.composition_review_read_model.v1";
  review_read_model_id: string;
  target_object_ref: string;
  approval_status: ApprovalStatus;
  blockers: CompositionApprovalBlocker[];
  eval_suite_run_refs: string[];
  evidence_refs: string[];
  updated_at: string;
}
