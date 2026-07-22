// Generated consumer contract artifact for TS-CMF-007.
// Python/Pydantic remains the source of truth.

export type SurfaceKey = "pwa" | "telegram_bot" | "telegram_mini_app";

export interface ObjectStateSnapshot {
  schema_version: "cmf.object_state_snapshot.v1";
  object_type: string;
  object_id: string;
  organization_id: string;
  brand_id: string;
  state: string;
  state_version: string;
  evidence_sufficient_for_surface: boolean;
  evidence_refs: string[];
}

export interface SurfaceActionEnvelope {
  schema_version: "cmf.surface_action.v1";
  surface_action_id: string;
  source_surface: SurfaceKey;
  actor_id: string;
  organization_id: string;
  brand_id: string;
  command_type: string;
  idempotency_key: string;
  object_snapshot: ObjectStateSnapshot;
  payload: Record<string, unknown>;
  requested_at: string;
}

export interface SurfaceCommandResult {
  schema_version: "cmf.surface_command_result.v1";
  surface_action_id: string;
  command_id: string | null;
  accepted: boolean;
  result_code: string;
  message: string;
  latest_state: ObjectStateSnapshot | null;
  receipt_id: string | null;
}
