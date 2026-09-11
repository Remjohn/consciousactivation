CREATE TABLE IF NOT EXISTS ie_migrations(
  version INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  applied_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ie_command_results(
  idempotency_key TEXT PRIMARY KEY,
  command_type TEXT NOT NULL,
  payload_sha256 TEXT NOT NULL,
  result_json TEXT NOT NULL,
  created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ie_objects(
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
  PRIMARY KEY(object_id, revision)
);
CREATE UNIQUE INDEX IF NOT EXISTS ie_objects_one_current ON ie_objects(object_id) WHERE is_current=1;
CREATE TABLE IF NOT EXISTS ie_edges(
  parent_id TEXT NOT NULL,
  child_id TEXT NOT NULL,
  relation TEXT NOT NULL,
  PRIMARY KEY(parent_id, child_id, relation)
);
CREATE TABLE IF NOT EXISTS ie_events(
  event_id TEXT PRIMARY KEY,
  aggregate_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  event_type TEXT NOT NULL,
  payload_sha256 TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  previous_event_sha256 TEXT,
  occurred_at_utc TEXT NOT NULL,
  idempotency_key TEXT NOT NULL UNIQUE,
  UNIQUE(aggregate_id, sequence)
);
CREATE TABLE IF NOT EXISTS ie_session_snapshots(
  session_id TEXT NOT NULL,
  sequence INTEGER NOT NULL,
  snapshot_sha256 TEXT NOT NULL,
  snapshot_json TEXT NOT NULL,
  created_at_utc TEXT NOT NULL,
  PRIMARY KEY(session_id, sequence)
);
