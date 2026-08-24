-- WP-04: immutable, source-lineage-preserving registry authority tables.
-- Registry data is global CAE canonical input, not workspace-owned operational state.

CREATE TABLE cae.registry_import_run (
  registry_import_run_id text PRIMARY KEY,
  importer_version text NOT NULL,
  source_set_sha256 text NOT NULL CHECK (source_set_sha256 ~ '^[a-f0-9]{64}$'),
  source_summary jsonb NOT NULL,
  outcome text NOT NULL CHECK (outcome IN ('IMPORTED', 'QUARANTINED', 'FAILED')),
  recorded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE cae.registry_snapshot (
  registry_snapshot_id text PRIMARY KEY,
  registry_id text NOT NULL,
  registry_kind text NOT NULL CHECK (registry_kind IN ('SDA', 'SFL', 'PRIMITIVE')),
  source_version text NOT NULL,
  source_locator text NOT NULL,
  source_archive_sha256 text NOT NULL CHECK (source_archive_sha256 ~ '^[a-f0-9]{64}$'),
  source_manifest_sha256 text NOT NULL CHECK (source_manifest_sha256 ~ '^[a-f0-9]{64}$'),
  item_count integer NOT NULL CHECK (item_count >= 0),
  validation_status text NOT NULL CHECK (validation_status IN ('VALID', 'QUARANTINED')),
  imported_by_run_id text NOT NULL REFERENCES cae.registry_import_run(registry_import_run_id),
  imported_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (registry_id, source_version, source_archive_sha256)
);

CREATE TABLE cae.registry_item (
  registry_item_id text PRIMARY KEY,
  registry_snapshot_id text NOT NULL REFERENCES cae.registry_snapshot(registry_snapshot_id),
  source_registry text NOT NULL,
  source_id text NOT NULL,
  registry_source_version text NOT NULL,
  source_record_version text,
  source_path text NOT NULL,
  source_hash text NOT NULL CHECK (source_hash ~ '^[a-f0-9]{64}$'),
  canonical_id text NOT NULL,
  record_kind text NOT NULL,
  source_raw_text text NOT NULL,
  payload jsonb NOT NULL,
  migration_status text NOT NULL CHECK (migration_status IN ('IMPORTED', 'QUARANTINED')),
  lineage_preserved boolean NOT NULL CHECK (lineage_preserved),
  validation_status text NOT NULL CHECK (validation_status IN ('VALID', 'QUARANTINED')),
  crosswalk_status text NOT NULL CHECK (crosswalk_status IN ('NOT_APPLICABLE', 'VALID', 'UNRESOLVED', 'EXTERNAL_DEPENDENCY')),
  known_gaps jsonb NOT NULL DEFAULT '[]'::jsonb,
  replacement_id text,
  migration_notes text NOT NULL DEFAULT '',
  imported_by_run_id text NOT NULL REFERENCES cae.registry_import_run(registry_import_run_id),
  imported_at timestamptz NOT NULL DEFAULT now(),
  -- Source IDs are deliberately not unique here. A duplicate inherited ID is
  -- retained as separate immutable evidence and quarantined by the importer.
  -- Runtime resolution refuses ambiguous canonical IDs.
  UNIQUE (registry_snapshot_id, source_path, source_hash)
);

CREATE TABLE cae.registry_reference (
  registry_reference_id text PRIMARY KEY,
  source_registry_item_id text NOT NULL REFERENCES cae.registry_item(registry_item_id),
  relation_type text NOT NULL,
  target_registry_kind text,
  target_id text NOT NULL,
  target_snapshot_id text REFERENCES cae.registry_snapshot(registry_snapshot_id),
  validation_status text NOT NULL CHECK (validation_status IN ('RESOLVED', 'UNRESOLVED_INTERNAL', 'EXTERNAL_DEPENDENCY')),
  rationale text,
  detail jsonb NOT NULL DEFAULT '{}'::jsonb,
  imported_by_run_id text NOT NULL REFERENCES cae.registry_import_run(registry_import_run_id),
  imported_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE cae.registry_integrity_issue (
  registry_integrity_issue_id text PRIMARY KEY,
  registry_snapshot_id text NOT NULL REFERENCES cae.registry_snapshot(registry_snapshot_id),
  registry_item_id text REFERENCES cae.registry_item(registry_item_id),
  issue_code text NOT NULL,
  severity text NOT NULL CHECK (severity IN ('BLOCKING', 'REVIEW', 'INFO')),
  status text NOT NULL CHECK (status IN ('OPEN', 'QUARANTINED', 'RESOLVED')),
  detail jsonb NOT NULL,
  source_hash text CHECK (source_hash IS NULL OR source_hash ~ '^[a-f0-9]{64}$'),
  imported_by_run_id text NOT NULL REFERENCES cae.registry_import_run(registry_import_run_id),
  recorded_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (registry_snapshot_id, registry_item_id, issue_code, detail)
);

CREATE INDEX idx_registry_item_lookup
  ON cae.registry_item(registry_snapshot_id, canonical_id, migration_status);
CREATE INDEX idx_registry_reference_source
  ON cae.registry_reference(source_registry_item_id, validation_status);
CREATE INDEX idx_registry_issue_status
  ON cae.registry_integrity_issue(registry_snapshot_id, status, severity);

CREATE OR REPLACE FUNCTION cae.reject_immutable_registry_mutation()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  RAISE EXCEPTION 'CAE immutable registry table % cannot be %', TG_TABLE_NAME, TG_OP;
END;
$$;

CREATE TRIGGER cae_00_registry_import_run_immutable
  BEFORE UPDATE OR DELETE ON cae.registry_import_run
  FOR EACH ROW EXECUTE FUNCTION cae.reject_immutable_registry_mutation();
CREATE TRIGGER cae_00_registry_snapshot_immutable
  BEFORE UPDATE OR DELETE ON cae.registry_snapshot
  FOR EACH ROW EXECUTE FUNCTION cae.reject_immutable_registry_mutation();
CREATE TRIGGER cae_00_registry_item_immutable
  BEFORE UPDATE OR DELETE ON cae.registry_item
  FOR EACH ROW EXECUTE FUNCTION cae.reject_immutable_registry_mutation();
CREATE TRIGGER cae_00_registry_reference_immutable
  BEFORE UPDATE OR DELETE ON cae.registry_reference
  FOR EACH ROW EXECUTE FUNCTION cae.reject_immutable_registry_mutation();
CREATE TRIGGER cae_00_registry_integrity_issue_immutable
  BEFORE UPDATE OR DELETE ON cae.registry_integrity_issue
  FOR EACH ROW EXECUTE FUNCTION cae.reject_immutable_registry_mutation();

ALTER TABLE cae.registry_import_run ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.registry_snapshot ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.registry_item ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.registry_reference ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.registry_integrity_issue ENABLE ROW LEVEL SECURITY;
