// Generated contract mirror for TS-CMF-055 Telegram quick review.

export type TelegramQuickActionType = "approve" | "reject" | "request_revision" | "open_pwa_review";

export type TelegramQuickReviewResultCode =
  | "notification_sent"
  | "quick_action_succeeded"
  | "pwa_handoff_required"
  | "stale_action_rejected"
  | "tamper_rejected"
  | "token_expired"
  | "action_not_allowed"
  | "command_rejected"
  | "command_failed";

export interface EvidenceSufficiencyDecision {
  schema_version: "cmf.telegram_evidence_sufficiency_decision.v1";
  decision_id: string;
  object_id: string;
  quick_actions_allowed: boolean;
  required_pwa_review: boolean;
  reasons: string[];
  review_state_id: string;
  approval_policy_report_id?: string | null;
  created_at: string;
}

export interface QuickActionToken {
  schema_version: "cmf.quick_action_token.v1";
  token_id: string;
  organization_id: string;
  brand_id: string;
  review_state_id: string;
  user_id: string;
  object_type: string;
  object_id: string;
  object_version_hash: string;
  allowed_actions: TelegramQuickActionType[];
  evidence_sufficiency_decision_id: string;
  approval_policy_report_id?: string | null;
  expires_at: string;
  idempotency_key: string;
  issued_at: string;
  revoked_at?: string | null;
}

export interface TelegramReviewNotification {
  schema_version: "cmf.telegram_review_notification.v1";
  notification_id: string;
  organization_id: string;
  brand_id: string;
  review_state_id: string;
  object_type: string;
  object_id: string;
  preview_uri: string;
  route_summary: string;
  source_snippet: string;
  consent_status: string;
  evaluation_summary: string;
  required_action: string;
  pwa_review_url: string;
  quick_action_token_id: string;
  quick_actions: TelegramQuickActionType[];
  evidence_sufficiency_decision_id: string;
  sent_at: string;
}

export interface QuickReviewReceipt {
  schema_version: "cmf.quick_review_receipt.v1";
  quick_review_receipt_id: string;
  notification_id?: string | null;
  token_id?: string | null;
  actor_id: string;
  organization_id: string;
  brand_id: string;
  review_state_id: string;
  object_type: string;
  object_id: string;
  object_version_hash: string;
  action_type: TelegramQuickActionType;
  evidence_sufficiency_decision_id?: string | null;
  quick_actions_allowed: boolean;
  result_code: TelegramQuickReviewResultCode;
  command_id?: string | null;
  command_status?: string | null;
  command_receipt_id?: string | null;
  review_decision_receipt_id?: string | null;
  pwa_handoff_required: boolean;
  pwa_deep_link?: {
    schema_version: "cmf.deep_link_target.v1";
    target_surface: "pwa";
    route: string;
    object_type: string;
    object_id: string;
    brand_id: string;
    required_reason: string;
  } | null;
  blocker_codes: string[];
  evidence_refs: string[];
  receipt_hash: string;
  written_at: string;
}
