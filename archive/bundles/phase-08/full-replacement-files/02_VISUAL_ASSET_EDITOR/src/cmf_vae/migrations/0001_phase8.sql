CREATE TABLE IF NOT EXISTS vae_objects (
  object_id TEXT PRIMARY KEY,
  object_type TEXT NOT NULL,
  version TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS vae_edges (
  parent_id TEXT NOT NULL,
  child_id TEXT NOT NULL,
  relation TEXT NOT NULL,
  PRIMARY KEY(parent_id, child_id, relation)
);
CREATE TABLE IF NOT EXISTS vae_idempotency (
  idempotency_key TEXT PRIMARY KEY,
  payload_sha256 TEXT NOT NULL,
  result_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS vae_workers (
  worker_id TEXT PRIMARY KEY,
  capability_ids_json TEXT NOT NULL,
  attestation_sha256 TEXT NOT NULL,
  state TEXT NOT NULL,
  registered_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS vae_jobs (
  job_id TEXT PRIMARY KEY,
  idempotency_key TEXT UNIQUE NOT NULL,
  request_sha256 TEXT NOT NULL,
  request_json TEXT NOT NULL,
  required_capabilities_json TEXT NOT NULL,
  state TEXT NOT NULL,
  attempt_number INTEGER NOT NULL,
  maximum_attempts INTEGER NOT NULL,
  lease_owner TEXT,
  fencing_token TEXT,
  lease_until_ms INTEGER,
  cancellation_requested INTEGER NOT NULL DEFAULT 0,
  checkpoint_json TEXT,
  result_json TEXT,
  failure_json TEXT,
  created_at_utc TEXT NOT NULL,
  updated_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS vae_job_events (
  sequence INTEGER PRIMARY KEY AUTOINCREMENT,
  event_id TEXT UNIQUE NOT NULL,
  job_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  payload_sha256 TEXT NOT NULL,
  occurred_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS vae_outbox (
  outbox_id TEXT PRIMARY KEY,
  job_id TEXT NOT NULL,
  event_sequence INTEGER NOT NULL,
  payload_json TEXT NOT NULL,
  delivered INTEGER NOT NULL DEFAULT 0,
  created_at_utc TEXT NOT NULL
);
