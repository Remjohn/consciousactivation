// Generated contract mirror for TS-CMF-058 Neo4j projection.

export type ProjectionHealthStatus = "healthy" | "lagging" | "unavailable" | "unhealthy_rebuild_required";

export interface ProjectionCheckpoint {
  schema_version: "cmf.projection_checkpoint.v1";
  checkpoint_id: string;
  event_outbox_offset: number;
  projected_event_count: number;
  projection_version: string;
  created_at: string;
}

export interface ProjectedRelationship {
  schema_version: "cmf.projected_relationship.v1";
  relationship_id: string;
  from_node_ref: string;
  to_node_ref: string;
  relationship_type: string;
  source_event_id: string;
  projection_batch_id: string;
  properties: Record<string, unknown>;
}

export interface ProjectionHealth {
  schema_version: "cmf.projection_health.v1";
  projection_name: "neo4j_relationship_projection";
  status: ProjectionHealthStatus;
  last_checkpoint_id?: string | null;
  lag_event_count: number;
  conflict_count: number;
  message: string;
  checked_at: string;
}

export interface ProjectionReceipt {
  schema_version: "cmf.projection_receipt.v1";
  projection_receipt_id: string;
  checkpoint_id?: string | null;
  event_range_start: number;
  event_range_end: number;
  node_count: number;
  relationship_count: number;
  lag_event_count: number;
  conflict_count: number;
  rebuild_result: string;
  health_status: ProjectionHealthStatus;
  receipt_hash: string;
  written_at: string;
}
