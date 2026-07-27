// Generated contract mirror for TS-CMF-056 evidence-backed memory admission.

export type MemoryEventType =
  | "brand"
  | "interviewer"
  | "route"
  | "anchor"
  | "archetype_survival"
  | "rejected_pattern"
  | "publishing_performance";

export type MemoryScope = "brand" | "guest" | "session" | "route" | "interviewer" | "global_fixture";
export type MemoryClaimScope = "supports" | "contradicts" | "contextualizes";
export type MemoryEventStatus = "approved" | "rejected" | "quarantined";
export type MemoryAdmissionPolicyResult = "proposed" | "approved" | "rejected" | "quarantined";

export interface MemoryEvidenceRef {
  schema_version: "cmf.memory_evidence_ref.v1";
  source_type: string;
  source_id: string;
  evidence_uri?: string | null;
  transcript_segment_id?: string | null;
  receipt_id?: string | null;
  claim_scope: MemoryClaimScope;
}

export interface MemoryAdmissionCandidate {
  schema_version: "cmf.memory_admission_candidate.v1";
  candidate_id: string;
  organization_id: string;
  brand_id: string;
  memory_type: MemoryEventType;
  proposed_from_event_id: string;
  proposed_statement: string;
  evidence_refs: MemoryEvidenceRef[];
  confidence: number;
  scope: MemoryScope;
  consent_record_version_id?: string | null;
  consent_compatible: boolean;
  originating_route_ref?: string | null;
  provenance_summary: string;
  proposed_by_actor_id: string;
  downstream_usage_constraints: string[];
  created_at: string;
}

export interface MemoryEvent {
  schema_version: "cmf.memory_event.v1";
  memory_event_id: string;
  candidate_id: string;
  organization_id: string;
  brand_id: string;
  memory_type: MemoryEventType;
  status: MemoryEventStatus;
  approved_by?: string | null;
  proposed_statement: string;
  scope: MemoryScope;
  originating_route_ref?: string | null;
  evidence_refs: MemoryEvidenceRef[];
  provenance_summary: string;
  confidence: number;
  consent_record_version_id?: string | null;
  created_at: string;
}

export interface MemoryAdmissionReceipt {
  schema_version: "cmf.memory_admission_receipt.v1";
  memory_admission_receipt_id: string;
  candidate_id: string;
  memory_event_id?: string | null;
  organization_id: string;
  brand_id: string;
  source_refs: string[];
  provenance_summary: string;
  confidence: number;
  consent_compatible: boolean;
  scope: MemoryScope;
  reviewer_id?: string | null;
  policy_result: MemoryAdmissionPolicyResult;
  blocker_codes: string[];
  downstream_citation_required: boolean;
  receipt_hash: string;
  written_at: string;
}
