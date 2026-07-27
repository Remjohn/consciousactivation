// Generated contract mirror for TS-CMF-059 Operations Board.

export interface QueueSnapshot {
  schema_version: "cmf.queue_snapshot.v1";
  queue_name: string;
  depth: number;
  active_count: number;
  failed_count: number;
  oldest_job_age_seconds?: number | null;
}

export interface WorkerStatusSnapshot {
  schema_version: "cmf.worker_status_snapshot.v1";
  worker_id: string;
  worker_type: string;
  status: "idle" | "running" | "draining" | "failed" | "offline";
  gpu_tier?: string | null;
  active_job_ids: string[];
  current_cost_estimate_usd?: number | null;
  shutdown_status?: string | null;
}

export interface BlockerSummary {
  schema_version: "cmf.blocker_summary.v1";
  blocker_type: "consent" | "approval" | "publishing" | "memory" | "projection";
  blocker_code: string;
  object_ref: string;
  receipt_id: string;
  required_action: string;
  allowed_command_type: string;
}

export interface OperationsBoardState {
  schema_version: "cmf.operations_board_state.v1";
  board_state_id: string;
  organization_id: string;
  brand_id?: string | null;
  queues: QueueSnapshot[];
  workers: WorkerStatusSnapshot[];
  blockers: BlockerSummary[];
  provider_statuses: unknown[];
  incident_ids: string[];
  projection_health: string;
  generated_at: string;
}
