PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS pipeline_migrations (
    version INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    applied_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pipeline_command_results (
    idempotency_key TEXT PRIMARY KEY,
    command_type TEXT NOT NULL,
    payload_sha256 TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pipeline_objects (
    object_id TEXT NOT NULL,
    revision INTEGER NOT NULL,
    object_type TEXT NOT NULL,
    semantic_version TEXT NOT NULL,
    canonical_sha256 TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    lifecycle_state TEXT NOT NULL,
    authority_state TEXT NOT NULL,
    is_current INTEGER NOT NULL CHECK(is_current IN (0,1)),
    idempotency_key TEXT NOT NULL,
    created_at_utc TEXT NOT NULL,
    supersedes_revision INTEGER,
    PRIMARY KEY(object_id, revision),
    UNIQUE(idempotency_key),
    UNIQUE(object_id, canonical_sha256)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_pipeline_objects_current
ON pipeline_objects(object_id)
WHERE is_current = 1;

CREATE INDEX IF NOT EXISTS idx_pipeline_objects_type
ON pipeline_objects(object_type, is_current);

CREATE TABLE IF NOT EXISTS pipeline_edges (
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    evidence_json TEXT NOT NULL,
    edge_sha256 TEXT NOT NULL,
    is_current INTEGER NOT NULL CHECK(is_current IN (0,1)),
    created_at_utc TEXT NOT NULL,
    PRIMARY KEY(source_id, target_id, relation_type, edge_sha256)
);

CREATE INDEX IF NOT EXISTS idx_pipeline_edges_source ON pipeline_edges(source_id, is_current);
CREATE INDEX IF NOT EXISTS idx_pipeline_edges_target ON pipeline_edges(target_id, is_current);

CREATE TABLE IF NOT EXISTS pipeline_workflows (
    workflow_id TEXT PRIMARY KEY,
    workflow_sha256 TEXT NOT NULL,
    definition_json TEXT NOT NULL,
    created_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    state TEXT NOT NULL,
    revision INTEGER NOT NULL,
    cancel_requested INTEGER NOT NULL CHECK(cancel_requested IN (0,1)),
    run_json TEXT NOT NULL,
    current_checkpoint_id TEXT,
    created_at_utc TEXT NOT NULL,
    updated_at_utc TEXT NOT NULL,
    FOREIGN KEY(workflow_id) REFERENCES pipeline_workflows(workflow_id)
);

CREATE TABLE IF NOT EXISTS pipeline_node_states (
    run_id TEXT NOT NULL,
    node_id TEXT NOT NULL,
    state TEXT NOT NULL,
    attempt_count INTEGER NOT NULL,
    dispatch_ordinal INTEGER,
    output_ref_json TEXT,
    failure_json TEXT,
    updated_at_utc TEXT NOT NULL,
    PRIMARY KEY(run_id, node_id),
    FOREIGN KEY(run_id) REFERENCES pipeline_runs(run_id)
);

CREATE TABLE IF NOT EXISTS pipeline_run_events (
    run_id TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    event_sha256 TEXT NOT NULL,
    occurred_at_utc TEXT NOT NULL,
    PRIMARY KEY(run_id, sequence),
    FOREIGN KEY(run_id) REFERENCES pipeline_runs(run_id)
);

CREATE TABLE IF NOT EXISTS pipeline_checkpoints (
    checkpoint_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    event_sequence INTEGER NOT NULL,
    snapshot_json TEXT NOT NULL,
    snapshot_sha256 TEXT NOT NULL,
    created_at_utc TEXT NOT NULL,
    FOREIGN KEY(run_id) REFERENCES pipeline_runs(run_id)
);

CREATE TABLE IF NOT EXISTS pipeline_incidents (
    incident_id TEXT PRIMARY KEY,
    severity TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    target_ref_json TEXT NOT NULL,
    containment_state TEXT NOT NULL,
    details_json TEXT NOT NULL,
    created_at_utc TEXT NOT NULL
);
