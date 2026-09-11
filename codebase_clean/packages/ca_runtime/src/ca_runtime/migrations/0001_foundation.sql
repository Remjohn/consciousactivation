PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    applied_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS product_metadata (
    product_id TEXT PRIMARY KEY,
    product_version TEXT NOT NULL,
    authority_state TEXT NOT NULL,
    development_authorized INTEGER NOT NULL CHECK (development_authorized IN (0, 1)),
    production_authorized INTEGER NOT NULL CHECK (production_authorized IN (0, 1)),
    certified INTEGER NOT NULL CHECK (certified IN (0, 1)),
    initialized_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS commands (
    command_id TEXT PRIMARY KEY,
    command_type TEXT NOT NULL,
    idempotency_key TEXT NOT NULL UNIQUE,
    envelope_json TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    payload_sha256 TEXT NOT NULL,
    submitted_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    aggregate_id TEXT NOT NULL,
    aggregate_version INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    envelope_json TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    payload_sha256 TEXT NOT NULL,
    causation_id TEXT NOT NULL,
    correlation_id TEXT NOT NULL,
    occurred_at_utc TEXT NOT NULL,
    UNIQUE (aggregate_id, aggregate_version),
    FOREIGN KEY (causation_id) REFERENCES commands(command_id)
);

CREATE TABLE IF NOT EXISTS receipts (
    receipt_id TEXT PRIMARY KEY,
    command_id TEXT NOT NULL UNIQUE,
    envelope_json TEXT NOT NULL,
    outcome TEXT NOT NULL,
    recorded_at_utc TEXT NOT NULL,
    receipt_sha256 TEXT NOT NULL,
    FOREIGN KEY (command_id) REFERENCES commands(command_id)
);

CREATE INDEX IF NOT EXISTS idx_events_aggregate ON events(aggregate_id, aggregate_version);
CREATE INDEX IF NOT EXISTS idx_commands_correlation ON commands(command_id);
