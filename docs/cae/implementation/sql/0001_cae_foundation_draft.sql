-- CAE WP-02 reviewed design draft. Do not apply to a shared or production
-- database until WP-02a provisions a disposable environment and records proof.
-- PostgreSQL 15+ / Supabase-compatible; all timestamps are UTC timestamptz.

CREATE SCHEMA IF NOT EXISTS cae;

CREATE TABLE cae.schema_migrations (
  version text PRIMARY KEY,
  checksum_sha256 text NOT NULL CHECK (checksum_sha256 ~ '^[a-f0-9]{64}$'),
  applied_at timestamptz NOT NULL DEFAULT now(),
  applied_by text NOT NULL
);

CREATE TABLE cae.workspace (
  workspace_id text PRIMARY KEY,
  display_name text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE cae.project (
  project_id text PRIMARY KEY,
  workspace_id text NOT NULL REFERENCES cae.workspace(workspace_id),
  display_name text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (workspace_id, project_id)
);

CREATE TABLE cae.actor (
  actor_id text PRIMARY KEY,
  workspace_id text NOT NULL REFERENCES cae.workspace(workspace_id),
  actor_kind text NOT NULL CHECK (actor_kind IN ('HUMAN', 'SERVICE', 'AGENT', 'EXTERNAL_SYSTEM')),
  external_subject text,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (workspace_id, external_subject),
  UNIQUE (workspace_id, actor_id)
);

CREATE TABLE cae.media_asset (
  asset_id text PRIMARY KEY,
  workspace_id text NOT NULL REFERENCES cae.workspace(workspace_id),
  project_id text,
  storage_provider text NOT NULL CHECK (storage_provider IN ('SUPABASE_STORAGE', 'S3_COMPATIBLE')),
  storage_bucket text NOT NULL,
  storage_object_key text NOT NULL,
  canonical_uri text NOT NULL UNIQUE,
  content_sha256 text NOT NULL CHECK (content_sha256 ~ '^[a-f0-9]{64}$'),
  byte_size bigint NOT NULL CHECK (byte_size >= 0),
  media_type text NOT NULL,
  lifecycle_state text NOT NULL CHECK (lifecycle_state IN ('STAGED', 'VERIFIED', 'QUARANTINED', 'RETIRED')),
  created_by_actor_id text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  verified_at timestamptz,
  UNIQUE (storage_provider, storage_bucket, storage_object_key),
  UNIQUE (workspace_id, content_sha256),
  FOREIGN KEY (workspace_id, project_id) REFERENCES cae.project(workspace_id, project_id),
  FOREIGN KEY (workspace_id, created_by_actor_id) REFERENCES cae.actor(workspace_id, actor_id)
);

CREATE TABLE cae.source_package (
  source_package_id text PRIMARY KEY,
  workspace_id text NOT NULL REFERENCES cae.workspace(workspace_id),
  media_asset_id text NOT NULL REFERENCES cae.media_asset(asset_id),
  transcript_asset_id text REFERENCES cae.media_asset(asset_id),
  source_kind text NOT NULL,
  canonical_sha256 text NOT NULL CHECK (canonical_sha256 ~ '^[a-f0-9]{64}$'),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (workspace_id, canonical_sha256)
);

CREATE TABLE cae.interview_session (
  session_id text PRIMARY KEY,
  workspace_id text NOT NULL REFERENCES cae.workspace(workspace_id),
  project_id text,
  guest_actor_id text,
  state text NOT NULL CHECK (state IN ('PLANNED', 'ACTIVE', 'COMPLETED', 'CANCELLED', 'QUARANTINED')),
  created_at timestamptz NOT NULL DEFAULT now(),
  FOREIGN KEY (workspace_id, project_id) REFERENCES cae.project(workspace_id, project_id),
  FOREIGN KEY (workspace_id, guest_actor_id) REFERENCES cae.actor(workspace_id, actor_id)
);

CREATE TABLE cae.interview_turn (
  turn_id text PRIMARY KEY,
  session_id text NOT NULL REFERENCES cae.interview_session(session_id),
  ordinal integer NOT NULL CHECK (ordinal >= 0),
  speaker_actor_id text REFERENCES cae.actor(actor_id),
  source_package_id text REFERENCES cae.source_package(source_package_id),
  text_content text,
  started_at timestamptz,
  ended_at timestamptz,
  UNIQUE (session_id, ordinal),
  CHECK (ended_at IS NULL OR started_at IS NULL OR ended_at >= started_at)
);

CREATE TABLE cae.evidence_item (
  evidence_id text PRIMARY KEY,
  workspace_id text NOT NULL REFERENCES cae.workspace(workspace_id),
  source_package_id text NOT NULL REFERENCES cae.source_package(source_package_id),
  evidence_kind text NOT NULL,
  capture_actor_id text NOT NULL,
  state text NOT NULL CHECK (state IN ('CAPTURED', 'AUTHENTICATED', 'REJECTED', 'NEEDS_REPAIR', 'SUPERSEDED')),
  canonical_sha256 text NOT NULL CHECK (canonical_sha256 ~ '^[a-f0-9]{64}$'),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (workspace_id, canonical_sha256),
  FOREIGN KEY (workspace_id, capture_actor_id) REFERENCES cae.actor(workspace_id, actor_id)
);

CREATE TABLE cae.evidence_span (
  evidence_span_id text PRIMARY KEY,
  evidence_id text NOT NULL REFERENCES cae.evidence_item(evidence_id),
  media_asset_id text REFERENCES cae.media_asset(asset_id),
  interview_turn_id text REFERENCES cae.interview_turn(turn_id),
  start_offset integer CHECK (start_offset IS NULL OR start_offset >= 0),
  end_offset integer CHECK (end_offset IS NULL OR end_offset >= start_offset),
  start_ms bigint CHECK (start_ms IS NULL OR start_ms >= 0),
  end_ms bigint CHECK (end_ms IS NULL OR end_ms >= start_ms),
  quoted_text text,
  CHECK (media_asset_id IS NOT NULL OR interview_turn_id IS NOT NULL)
);

CREATE TABLE cae.evidence_authentication (
  authentication_id text PRIMARY KEY,
  evidence_id text NOT NULL REFERENCES cae.evidence_item(evidence_id),
  decision text NOT NULL CHECK (decision IN ('AUTHENTICATED', 'REJECTED', 'NEEDS_REPAIR')),
  evaluator_actor_id text NOT NULL REFERENCES cae.actor(actor_id),
  rationale text NOT NULL,
  evidence_set_sha256 text NOT NULL CHECK (evidence_set_sha256 ~ '^[a-f0-9]{64}$'),
  decided_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE cae.semantic_assessment (
  assessment_id text NOT NULL,
  workspace_id text NOT NULL REFERENCES cae.workspace(workspace_id),
  assessment_kind text NOT NULL,
  revision integer NOT NULL CHECK (revision >= 1),
  epistemic_state text NOT NULL CHECK (epistemic_state IN ('PLANNED', 'OBSERVED', 'INFERRED', 'OPERATOR_CONFIRMED', 'REJECTED', 'SUPERSEDED')),
  lifecycle_state text NOT NULL CHECK (lifecycle_state IN ('PROPOSED', 'VALIDATED', 'APPROVED', 'REJECTED', 'SUPERSEDED')),
  validator_id text NOT NULL,
  validator_version text NOT NULL,
  payload jsonb NOT NULL,
  canonical_sha256 text NOT NULL CHECK (canonical_sha256 ~ '^[a-f0-9]{64}$'),
  created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (assessment_id, revision),
  UNIQUE (assessment_id, canonical_sha256)
);

CREATE TABLE cae.assessment_evidence_link (
  assessment_id text NOT NULL,
  assessment_revision integer NOT NULL,
  evidence_id text NOT NULL REFERENCES cae.evidence_item(evidence_id),
  relation_type text NOT NULL CHECK (relation_type IN ('SUPPORTS', 'CONTRADICTS', 'CONTEXTUALIZES')),
  PRIMARY KEY (assessment_id, assessment_revision, evidence_id, relation_type),
  FOREIGN KEY (assessment_id, assessment_revision) REFERENCES cae.semantic_assessment(assessment_id, revision)
);

CREATE TABLE cae.semantic_operation (
  operation_id text PRIMARY KEY,
  operation_version text NOT NULL,
  owning_layer text NOT NULL,
  input_contract_ref text NOT NULL,
  output_contract_ref text NOT NULL,
  UNIQUE (operation_id, operation_version)
);

CREATE TABLE cae.command (
  command_id text PRIMARY KEY,
  workspace_id text NOT NULL REFERENCES cae.workspace(workspace_id),
  operation_id text NOT NULL,
  operation_version text NOT NULL,
  actor_id text NOT NULL,
  idempotency_key text NOT NULL,
  payload_sha256 text NOT NULL CHECK (payload_sha256 ~ '^[a-f0-9]{64}$'),
  submitted_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (workspace_id, operation_id, idempotency_key),
  FOREIGN KEY (operation_id, operation_version) REFERENCES cae.semantic_operation(operation_id, operation_version),
  FOREIGN KEY (workspace_id, actor_id) REFERENCES cae.actor(workspace_id, actor_id)
);

CREATE TABLE cae.state_aggregate (
  aggregate_id text PRIMARY KEY,
  workspace_id text NOT NULL REFERENCES cae.workspace(workspace_id),
  aggregate_type text NOT NULL,
  current_state text NOT NULL,
  version integer NOT NULL CHECK (version >= 0),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE cae.state_transition_contract (
  contract_id text NOT NULL,
  contract_version text NOT NULL,
  aggregate_type text NOT NULL,
  from_state text NOT NULL,
  to_state text NOT NULL,
  semantic_operation_id text NOT NULL,
  semantic_operation_version text NOT NULL,
  requires_operator_decision boolean NOT NULL DEFAULT false,
  requires_independent_evidence boolean NOT NULL DEFAULT true,
  active boolean NOT NULL DEFAULT true,
  PRIMARY KEY (contract_id, contract_version),
  FOREIGN KEY (semantic_operation_id, semantic_operation_version) REFERENCES cae.semantic_operation(operation_id, operation_version)
);

CREATE TABLE cae.state_transition (
  transition_id text PRIMARY KEY,
  aggregate_id text NOT NULL REFERENCES cae.state_aggregate(aggregate_id),
  contract_id text NOT NULL,
  contract_version text NOT NULL,
  command_id text NOT NULL UNIQUE REFERENCES cae.command(command_id),
  actor_id text NOT NULL,
  from_state text NOT NULL,
  to_state text NOT NULL,
  expected_version integer NOT NULL CHECK (expected_version >= 0),
  resulting_version integer NOT NULL CHECK (resulting_version >= 1),
  occurred_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (aggregate_id, resulting_version),
  FOREIGN KEY (contract_id, contract_version) REFERENCES cae.state_transition_contract(contract_id, contract_version),
  FOREIGN KEY (actor_id) REFERENCES cae.actor(actor_id)
);

CREATE TABLE cae.event (
  event_id text PRIMARY KEY,
  workspace_id text NOT NULL REFERENCES cae.workspace(workspace_id),
  aggregate_id text NOT NULL REFERENCES cae.state_aggregate(aggregate_id),
  aggregate_version integer NOT NULL CHECK (aggregate_version >= 1),
  event_type text NOT NULL,
  command_id text NOT NULL REFERENCES cae.command(command_id),
  correlation_id text NOT NULL,
  causation_id text NOT NULL,
  payload_sha256 text NOT NULL CHECK (payload_sha256 ~ '^[a-f0-9]{64}$'),
  occurred_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (aggregate_id, aggregate_version)
);

CREATE TABLE cae.receipt (
  receipt_id text PRIMARY KEY,
  command_id text NOT NULL UNIQUE REFERENCES cae.command(command_id),
  transition_id text REFERENCES cae.state_transition(transition_id),
  outcome text NOT NULL CHECK (outcome IN ('ACCEPTED', 'REJECTED', 'CONFLICT', 'QUARANTINED')),
  evidence_summary_sha256 text NOT NULL CHECK (evidence_summary_sha256 ~ '^[a-f0-9]{64}$'),
  recorded_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE cae.legacy_import_run (
  import_run_id text PRIMARY KEY,
  source_system text NOT NULL,
  source_manifest_sha256 text NOT NULL CHECK (source_manifest_sha256 ~ '^[a-f0-9]{64}$'),
  target_schema_version text NOT NULL,
  started_at timestamptz NOT NULL DEFAULT now(),
  completed_at timestamptz,
  state text NOT NULL CHECK (state IN ('PLANNED', 'RUNNING', 'RECONCILING', 'SUCCEEDED', 'FAILED', 'ROLLED_BACK'))
);

CREATE TABLE cae.legacy_import_record (
  import_run_id text NOT NULL REFERENCES cae.legacy_import_run(import_run_id),
  source_system text NOT NULL,
  source_locator text NOT NULL,
  source_sha256 text NOT NULL CHECK (source_sha256 ~ '^[a-f0-9]{64}$'),
  target_table text,
  target_identity text,
  outcome text NOT NULL CHECK (outcome IN ('IMPORTED', 'SKIPPED', 'QUARANTINED', 'FAILED')),
  reason text,
  recorded_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (import_run_id, source_system, source_locator)
);

CREATE INDEX idx_media_asset_workspace_state ON cae.media_asset(workspace_id, lifecycle_state);
CREATE INDEX idx_evidence_item_source_state ON cae.evidence_item(source_package_id, state);
CREATE INDEX idx_assessment_state ON cae.semantic_assessment(workspace_id, lifecycle_state, epistemic_state);
CREATE INDEX idx_transition_aggregate ON cae.state_transition(aggregate_id, resulting_version);
CREATE INDEX idx_event_aggregate ON cae.event(aggregate_id, aggregate_version);
CREATE INDEX idx_legacy_import_outcome ON cae.legacy_import_record(import_run_id, outcome);
