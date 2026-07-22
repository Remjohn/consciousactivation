// Generated contract mirror for TS-CMF-057 memory governance.

export type MemoryGovernanceActionType =
  | "correct"
  | "reverse"
  | "expire"
  | "quarantine"
  | "release_from_quarantine";

export type MemoryGovernanceStatus = "active" | "corrected" | "reversed" | "expired" | "quarantined";
export type MemoryUsagePolicy = "allowed" | "blocked";

export interface MemoryGovernanceAction {
  schema_version: "cmf.memory_governance_action.v1";
  action_id: string;
  memory_event_id: string;
  action_type: MemoryGovernanceActionType;
  reason: string;
  evidence_refs: string[];
  requested_by_user_id: string;
  corrected_statement?: string | null;
  created_at: string;
}

export interface MemoryGovernanceEvent {
  schema_version: "cmf.memory_governance_event.v1";
  event_id: string;
  action_id: string;
  memory_event_id: string;
  resulting_status: MemoryGovernanceStatus;
  superseding_memory_event_id?: string | null;
  reason: string;
  evidence_refs: string[];
  created_at: string;
}

export interface MemoryReviewState {
  schema_version: "cmf.memory_review_state.v1";
  memory_event_id: string;
  evidence_refs: string[];
  source_refs: string[];
  route_refs: string[];
  confidence: number;
  consent_compatible: boolean;
  created_event_id: string;
  downstream_usage_refs: string[];
  governance_status: MemoryGovernanceStatus;
  superseding_memory_event_id?: string | null;
  governance_history: MemoryGovernanceEvent[];
}

export interface MemoryGovernanceReceipt {
  schema_version: "cmf.memory_governance_receipt.v1";
  memory_governance_receipt_id: string;
  action_id: string;
  memory_event_id: string;
  superseding_memory_event_id?: string | null;
  action_type: MemoryGovernanceActionType;
  reason: string;
  actor_id: string;
  evidence_refs: string[];
  prior_status: MemoryGovernanceStatus;
  resulting_status: MemoryGovernanceStatus;
  downstream_usage_effect: string;
  projection_event_id?: string | null;
  receipt_hash: string;
  written_at: string;
}
