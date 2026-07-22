// Generated contract mirror for TS-CMF-061 operational readiness.

export type ReadinessCheckType =
  | "restore_drill"
  | "provider_outage"
  | "gpu_worker_shutdown"
  | "memory_rebuild"
  | "projection_rebuild"
  | "complete_brand_cycle";

export type ReadinessOverallStatus = "passed" | "failed" | "blocked";

export interface ReadinessCheckResult {
  check_type: ReadinessCheckType;
  passed: boolean;
  evidence_refs: string[];
  blocker_codes: string[];
  required_fixes: string[];
  observed_counts: Record<string, number>;
}

export interface ReadinessCheckRun {
  schema_version: "cmf.readiness_check_run.v1";
  readiness_run_id: string;
  organization_id: string;
  brand_id: string;
  triggered_by_user_id: string;
  fixture_pack_id: string;
  results: ReadinessCheckResult[];
  overall_status: ReadinessOverallStatus;
  manual_database_edits_detected: boolean;
  source_spine_refs: string[];
  created_at: string;
}

export interface ReadinessReceipt {
  schema_version: "cmf.readiness_receipt.v1";
  receipt_id: string;
  readiness_run_id: string;
  fixture_pack_id: string;
  canonical_state_verified: boolean;
  object_storage_verified: boolean;
  receipts_verified: boolean;
  projection_rebuild_verified: boolean;
  manual_database_edits_detected: boolean;
  passed_check_count: number;
  failed_check_count: number;
  blocker_codes: string[];
  evidence_refs: string[];
  receipt_hash: string;
  written_at: string;
}

export interface OperationalReadinessReport {
  schema_version: "cmf.operational_readiness_report.v1";
  readiness_report_id: string;
  run: ReadinessCheckRun;
  receipt: ReadinessReceipt;
  detailed_reports: Record<string, unknown>;
  generated_at: string;
}
