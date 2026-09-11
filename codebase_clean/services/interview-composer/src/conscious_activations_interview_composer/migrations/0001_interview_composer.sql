CREATE TABLE IF NOT EXISTS ic_migrations(
  version INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  applied_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ic_command_results(
  idempotency_key TEXT PRIMARY KEY,
  command_type TEXT NOT NULL,
  payload_sha256 TEXT NOT NULL,
  result_json TEXT NOT NULL,
  created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ic_objects(
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
CREATE UNIQUE INDEX IF NOT EXISTS ic_objects_one_current ON ic_objects(object_id) WHERE is_current=1;
CREATE TABLE IF NOT EXISTS ic_edges(
  parent_id TEXT NOT NULL,
  child_id TEXT NOT NULL,
  relation TEXT NOT NULL,
  PRIMARY KEY(parent_id, child_id, relation)
);
