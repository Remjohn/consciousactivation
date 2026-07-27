// Generated top-level bindings. Do not edit manually.

export type SourceKind = "interview_expression" | "public_comment" | "direct_message_reply" | "authored_source" | "live_premise" | "research_synthesis" | "operator_supplied" | "legacy_migrated";

export interface SourceProvenance {
  source_kind: SourceKind;
}

export interface DelegationEnvelope {
  protocol_version: string;
  message_type: string;
  message_version: string;
  message_id: string;
  correlation_id: string;
  causation_id: string | null;
  sender: Record<string, unknown>;
  recipient: Record<string, unknown>;
  authority: Record<string, unknown>;
  occurred_at: string;
  idempotency_key: string | null;
  payload_hash: string;
  payload_ref: string;
  integrity: Record<string, unknown>;
}

export interface VisualAssetDemand {
  request_id: string;
  version: number;
  supersedes: Record<string, unknown> | null;
  content_harness_ref: Record<string, unknown>;
  category_profile: Record<string, unknown>;
  format_profile: Record<string, unknown>;
  asset_classification: Record<string, unknown>;
  source_provenance: SourceProvenance;
  activative_semantic_lineage: Record<string, unknown>;
  activation_contract: Record<string, unknown>;
  semantic_intent: Record<string, unknown>;
  visual_semantic_pack: Record<string, unknown>;
  visual_narrative_program: Record<string, unknown>;
  feature_contracts: Array<Record<string, unknown>>;
  somatic_route_request: Record<string, unknown>;
  activative_function: Record<string, unknown>;
  wrong_reading_locks: Array<string>;
  composition_intent: Record<string, unknown>;
  identity_continuity: Record<string, unknown>;
  reference_evidence: Array<Record<string, unknown>>;
  delivery: Record<string, unknown>;
  evaluation_policy: Record<string, unknown>;
  execution_policy: Record<string, unknown>;
  notes: string | null;
}

export interface VisualAssetSubmission {
  submission_id: string;
  demand: Record<string, unknown>;
  submitted_at: string;
  requested_priority: "LOW" | "NORMAL" | "HIGH" | "CRITICAL";
  callback_resources: Array<Record<string, unknown>>;
  idempotency_key: string;
}

export interface SubmissionValidationReceipt {
  receipt_id: string;
  submission_id: string;
  demand: Record<string, unknown>;
  status: "ACCEPTED" | "REJECTED";
  validated_at: string;
  findings: Array<Record<string, unknown>>;
  rejection: Record<string, unknown> | null;
  negotiated_profile: Record<string, unknown> | null;
}

export interface AdmissionReceipt {
  receipt_id: string;
  submission_receipt_id: string;
  execution: Record<string, unknown> | null;
  demand: Record<string, unknown>;
  status: "ACCEPTED" | "REJECTED";
  admitted_at: string;
  status_resource: Record<string, unknown> | null;
  rejection: Record<string, unknown> | null;
}

export interface VisualAssetEvent {
  event_id: string;
  execution: Record<string, unknown>;
  event_type: "STARTED" | "PROGRESS" | "REVALIDATION_STARTED";
  projected_state: "DRAFT" | "SUBMITTED" | "REJECTED" | "ACCEPTED" | "IN_PROGRESS" | "RESULT_READY" | "RESULT_REJECTED" | "COMPLETED" | "AMENDMENT_REQUIRED" | "SUPERSEDED" | "COST_APPROVAL_REQUIRED" | "CAPABILITY_GAP" | "HUMAN_REVIEW_REQUIRED" | "CANCELLATION_REQUESTED" | "CANCELLED" | "PARTIAL_RESULT_READY" | "INVALIDATED" | "REVOKED" | "REPLACED";
  occurred_at: string;
  progress_basis_points: number;
  reason: Record<string, unknown> | null;
  evidence_refs: Array<Record<string, unknown>>;
}

export interface DelegationSet {
  set_id: string;
  version: number;
  member_demands: Array<Record<string, unknown>>;
  dependency_edges: Array<Record<string, unknown>>;
  completion_policy: "ALL" | "MINIMUM_COUNT" | "NAMED_MEMBERS";
  minimum_completed: number;
  failure_policy: "FAIL_FAST" | "CONTINUE_INDEPENDENT" | "PAUSE_DEPENDENTS";
}

export interface BudgetAuthorization {
  authorization_id: string;
  scope: "DEMAND" | "DELEGATION_SET";
  demand: Record<string, unknown> | null;
  delegation_set_ref: Record<string, unknown> | null;
  maximum_cost: Record<string, unknown>;
  maximum_attempts: number;
  maximum_duration_seconds: number;
  valid_from: string;
  valid_until: string;
}

export interface BudgetEscalationRequest {
  request_id: string;
  execution: Record<string, unknown>;
  current_authorization_ref: Record<string, unknown>;
  requested_additional_cost: Record<string, unknown>;
  requested_additional_attempts: number;
  reason: string;
  evidence_refs: Array<Record<string, unknown>>;
}

export interface BudgetEscalationResponse {
  response_id: string;
  escalation_request_id: string;
  decision: "APPROVED" | "DENIED";
  replacement_authorization_ref: Record<string, unknown> | null;
  reason: string;
  decided_at: string;
}

export interface CancellationRequest {
  request_id: string;
  demand: Record<string, unknown>;
  execution_id: string | null;
  mode: "BEST_EFFORT" | "IMMEDIATE_IF_NOT_STARTED";
  reason: string;
  requested_at: string;
}

export interface CancellationReceipt {
  receipt_id: string;
  cancellation_request_id: string;
  demand: Record<string, unknown>;
  status: "ACCEPTED" | "REJECTED" | "COMPLETED";
  effective_at: string | null;
  reason: Record<string, unknown> | null;
  partial_artifact_refs: Array<Record<string, unknown>>;
}

export interface ConstraintConflict {
  conflict_id: string;
  execution: Record<string, unknown>;
  conflicting_paths: Array<string>;
  summary: Record<string, unknown>;
  evidence_refs: Array<Record<string, unknown>>;
  suggested_resolution: string | null;
}

export interface AmendmentProposal {
  proposal_id: string;
  demand: Record<string, unknown>;
  execution: Record<string, unknown>;
  trigger_conflict_id: string | null;
  options: Array<Record<string, unknown>>;
  expires_at: string;
  proposed_at: string;
}

export interface AmendmentResponse {
  response_id: string;
  proposal_id: string;
  selected_option_id: string | null;
  decision: "ACCEPTED" | "REJECTED" | "ALTERNATIVE_REQUESTED";
  authorized_successor_demand: Record<string, unknown> | null;
  decision_principal: Record<string, unknown>;
  reason: Record<string, unknown> | null;
  decided_at: string;
}

export interface DemandSupersession {
  supersession_id: string;
  superseded_demand: Record<string, unknown>;
  replacement_demand: Record<string, unknown>;
  invalidation_scope: Array<string>;
  reason: string;
  effective_at: string;
}

export interface SelectiveInvalidationReceipt {
  receipt_id: string;
  supersession_id: string;
  invalidated_paths: Array<string>;
  preserved_evidence_refs: Array<Record<string, unknown>>;
  invalidated_evidence_refs: Array<Record<string, unknown>>;
  recorded_at: string;
}

export interface AssetResultContract {
  result_id: string;
  version: number;
  execution: Record<string, unknown>;
  demand: Record<string, unknown>;
  artifact_ref: Record<string, unknown>;
  artifact_media_type: "image/png" | "image/jpeg" | "image/webp";
  artifact_width_px: number;
  artifact_height_px: number;
  completion_status: "COMPLETE" | "PARTIAL";
  unresolved_roles: Array<string>;
  provenance_refs: Array<Record<string, unknown>>;
  evaluation_findings: Array<Record<string, unknown>>;
  cost_consumed: Record<string, unknown>;
  attempts_consumed: number;
  declared_at: string;
}

export interface ResultAcknowledgement {
  acknowledgement_id: string;
  result: Record<string, unknown>;
  demand: Record<string, unknown>;
  decision: "ACCEPTED" | "ACCEPTED_WITH_CONCERNS" | "REJECTED";
  consumption_authorized: boolean;
  findings: Array<Record<string, unknown>>;
  acknowledged_at: string;
}

export interface InvalidationNotice {
  notice_id: string;
  result: Record<string, unknown>;
  demand: Record<string, unknown>;
  scope: Array<string>;
  reason: string;
  replacement_expected: boolean;
  effective_at: string;
}

export interface RevocationNotice {
  notice_id: string;
  result: Record<string, unknown>;
  demand: Record<string, unknown>;
  reason: string;
  consumption_must_stop: boolean;
  effective_at: string;
}

export interface ReplacementNotice {
  notice_id: string;
  replaced_result: Record<string, unknown>;
  replacement_result: Record<string, unknown>;
  demand: Record<string, unknown>;
  reason: string;
  effective_at: string;
}

export interface DelegationFailure {
  failure_id: string;
  demand: Record<string, unknown> | null;
  execution_id: string | null;
  detecting_principal: Record<string, unknown>;
  summary: Record<string, unknown>;
  evidence_refs: Array<Record<string, unknown>>;
  occurred_at: string;
}

export interface DelegationAuditReceipt {
  receipt_id: string;
  message_id: string;
  correlation_id: string;
  payload_hash: string;
  previous_receipt_hash: string | null;
  effective_state: "DRAFT" | "SUBMITTED" | "REJECTED" | "ACCEPTED" | "IN_PROGRESS" | "RESULT_READY" | "RESULT_REJECTED" | "COMPLETED" | "AMENDMENT_REQUIRED" | "SUPERSEDED" | "COST_APPROVAL_REQUIRED" | "CAPABILITY_GAP" | "HUMAN_REVIEW_REQUIRED" | "CANCELLATION_REQUESTED" | "CANCELLED" | "PARTIAL_RESULT_READY" | "INVALIDATED" | "REVOKED" | "REPLACED" | null;
  authority_verdict: "PASS" | "FAIL";
  schema_verdict: "PASS" | "FAIL";
  recorded_at: string;
}

export interface CompatibilityManifest {
  manifest_id: string;
  package_version: string;
  protocol_versions: Array<string>;
  message_versions: Array<Record<string, unknown>>;
  features: Array<string>;
  required_semantic_domains: Array<"source_provenance" | "activative_semantic_lineage" | "activation_contract" | "visual_semantic_pack" | "visual_narrative_program" | "feature_contracts" | "somatic_route_request" | "expression_moment_lineage" | "wrong_reading_locks">;
  semantic_capabilities: Array<Record<string, unknown>>;
  adapter_policy: Record<string, unknown>;
  required_signature_algorithms: Array<"Ed25519">;
  status: "RELEASE_CANDIDATE" | "PUBLISHED" | "DEPRECATED" | "REVOKED";
  published_at: string;
}

export interface ContractMigration {
  migration_id: string;
  source_message_type: string;
  source_version: string;
  target_version: string;
  source_payload_hash: string;
  target_artifacts: Array<Record<string, unknown>>;
  ordered_transformations: Array<string>;
  authority_effect_analysis: Array<Record<string, unknown>>;
  preserved_semantic_paths: Array<string>;
  behavioral_enforcement: "PASS" | "FAIL";
  source_validation: "PASS" | "FAIL";
  target_validation: "PASS" | "FAIL";
  equivalence: "PASS" | "FAIL";
  output_ref: Record<string, unknown>;
  evidence_refs: Array<Record<string, unknown>>;
  lossless: boolean;
  migrated_at: string;
}
