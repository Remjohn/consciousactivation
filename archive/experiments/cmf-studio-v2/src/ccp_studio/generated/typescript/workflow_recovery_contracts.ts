// Generated contract mirror for TS-CMF-060 workflow recovery.

export type WorkflowRecoveryActionType = "retry" | "resume" | "cancel" | "compensate" | "quarantine";
export type WorkflowRecoveryStatus = "validated" | "applied" | "blocked" | "replayed";

export interface RecoveryValidationReport {
  schema_version: "cmf.workflow_recovery_validation_report.v1";
  report_id: string;
  workflow_id: string;
  failed_object_ref: string;
  safe_actions: WorkflowRecoveryActionType[];
  blocked_actions: string[];
  completed_artifact_refs: string[];
  receipt_refs: string[];
  duplicate_side_effect_risks: string[];
  consent_compatible: boolean;
  provider_cost_risk: boolean;
  publishing_side_effect_risk: boolean;
  memory_side_effect_risk: boolean;
  checked_at: string;
}

export interface WorkflowRecoveryReceipt {
  schema_version: "cmf.workflow_recovery_receipt.v1";
  receipt_id: string;
  recovery_action_id?: string | null;
  validation_report_id: string;
  incident_id: string;
  action_type: WorkflowRecoveryActionType;
  status: WorkflowRecoveryStatus;
  idempotency_key: string;
  preserved_artifact_refs: string[];
  requeued_work_refs: string[];
  quarantined_refs: string[];
  blocked_actions: string[];
  duplicate_side_effect_risks: string[];
  terminal_state?: string | null;
  decision_code: string;
  actor_id: string;
  receipt_hash: string;
  written_at: string;
}
