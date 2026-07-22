// Generated consumer-facing review state contracts for TS-CMF-051.

export type EvidencePanelType =
  | "preview"
  | "source_quote"
  | "transcript"
  | "archetype_route"
  | "brand_context"
  | "selected_assets"
  | "render_output"
  | "evaluation"
  | "revision_history"
  | "consent_state";

export type EvidenceCompleteness = "complete" | "missing" | "conflicting";
export type TelegramComplexity = "quick_allowed" | "pwa_required";

export interface EvidencePanel {
  schema_version: "cmf.evidence_panel.v1";
  panel_type: EvidencePanelType;
  object_refs: string[];
  summary: string;
  completeness: EvidenceCompleteness;
  blocker_codes: string[];
}

export interface EvaluationFailureView {
  schema_version: "cmf.evaluation_failure_view.v1";
  evaluation_receipt_id: string;
  category: string;
  failure_code: string;
  evidence_refs: string[];
  repair_recommendation: string;
}

export interface RevisionHistoryItem {
  schema_version: "cmf.revision_history_item.v1";
  revision_request_id?: string | null;
  revision_version_id?: string | null;
  target_object_type: string;
  target_object_id: string;
  prior_version_id?: string | null;
  reason: string;
  decision_code?: string | null;
  created_at: string;
}

export interface ConsentCompatibilitySnapshot {
  schema_version: "cmf.consent_compatibility_snapshot.v1";
  consent_record_version_id: string;
  status: string;
  compatible: boolean;
  changed_after_render: boolean;
  blocker_codes: string[];
}

export interface PwaDeepLinkTarget {
  schema_version: "cmf.deep_link_target.v1";
  target_surface: "pwa";
  route: string;
  object_type: string;
  object_id: string;
  brand_id: string;
  required_reason: string;
}

export interface ReviewEvidenceState {
  schema_version: "cmf.review_evidence_state.v1";
  review_state_id: string;
  organization_id: string;
  brand_id: string;
  object_type: string;
  object_id: string;
  approval_evidence_view_id: string;
  panels: EvidencePanel[];
  evaluation_failures: EvaluationFailureView[];
  revision_history: RevisionHistoryItem[];
  consent_snapshot: ConsentCompatibilitySnapshot;
  brand_context_version_id?: string | null;
  selected_asset_refs: string[];
  render_output_refs: string[];
  pwa_route: string;
  telegram_complexity: TelegramComplexity;
  pwa_deep_link?: PwaDeepLinkTarget | null;
  generated_at: string;
}

export interface ReviewStateReceipt {
  schema_version: "cmf.review_state_receipt.v1";
  review_state_receipt_id: string;
  review_state_id: string;
  organization_id: string;
  brand_id: string;
  object_type: string;
  object_id: string;
  panel_completeness: Record<string, string>;
  consent_compatible: boolean;
  evaluation_failure_ids: string[];
  revision_history_hash: string;
  surface_route: string;
  evidence_refs: string[];
  command_id?: string | null;
  receipt_hash: string;
  written_at: string;
}
