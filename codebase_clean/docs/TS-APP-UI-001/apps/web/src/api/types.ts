// Health / error DTOs mirror TS-APP-API-001 §6 exactly — keep in sync.
export interface ServiceHealthItem {
  readonly service: string;
  readonly product_id: string;
  readonly product_version: string;
  readonly authority_state: string;
  readonly database_path: string;
  readonly integrity: "ok" | "error";
  readonly command_count: number;
  readonly event_count: number;
  readonly receipt_count: number;
  readonly production_authorized: boolean;
  readonly certified: boolean;
  readonly claim_ceiling: string;
}

export interface HealthResponse {
  readonly status: "ok" | "degraded" | "error";
  readonly timestamp: string;
  readonly gateway_version: string;
  readonly ca_data_root: string;
  readonly services: Readonly<Record<string, ServiceHealthItem>>;
}

export interface ErrorResponse {
  readonly error_code: string;
  readonly message: string;
  readonly service?: string | null;
  readonly timestamp: string;
}

// WebSocket message envelope union mirrors TS-APP-API-005 §6 exactly — keep in sync.
interface NodeStatus {
  readonly node_id: string;
  readonly state: string;
  readonly attempt_count: number;
  readonly dispatch_ordinal: number | null;
  readonly output_ref: Record<string, unknown> | null;
  readonly failure: Record<string, unknown> | null;
}

interface RunStatus {
  readonly run_id: string;
  readonly workflow_id: string;
  readonly state: string;
  readonly revision: number;
  readonly cancel_requested: boolean;
  readonly current_checkpoint_id: string | null;
  readonly nodes: ReadonlyArray<NodeStatus>;
}

export type WSMessage =
  | { readonly type: "snapshot"; readonly retrieved_at_utc: string; readonly run: RunStatus }
  | { readonly type: "history"; readonly retrieved_at_utc: string; readonly event_count: number; readonly event_stream_sha256: string; readonly events: ReadonlyArray<unknown> }
  | { readonly type: "node_state_changed"; readonly retrieved_at_utc: string; readonly run_id: string; readonly node: NodeStatus }
  | { readonly type: "run_state_changed"; readonly retrieved_at_utc: string; readonly run_id: string; readonly workflow_id: string; readonly state: string; readonly revision: number; readonly cancel_requested: boolean; readonly current_checkpoint_id: string | null }
  | { readonly type: "run_terminal"; readonly retrieved_at_utc: string; readonly run: RunStatus };

// Re-export of the Studio domain types this scaffold exists to make available.
// No modification. See TS-APP-UI-001 §3 ("consumed by source import").
export type {
  CampaignOrder,
  CampaignState,
  ControlTowerProjection,
  TimelineProjection,
  ChangeRequestProgram,
  ShipDecision,
  ShipRequest,
  HumanResolutionEpisode,
  AuditExportManifest,
  AutonomyMode,
  CampaignLifecycleState,
  OutputTarget,
} from "@ca/studio/domain";
