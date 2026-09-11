-- WP-07: execution-receipt context and queryable evidence lineage.
-- This extends the immutable operation envelope. It never converts a receipt
-- into independent evidence, and it does not create a new current-state store.

CREATE TABLE cae.execution_receipt (
  receipt_id text PRIMARY KEY REFERENCES cae.receipt(receipt_id),
  claim_id text NOT NULL,
  component_id text NOT NULL,
  input_snapshot_sha256 text NOT NULL CHECK (input_snapshot_sha256 ~ '^[a-f0-9]{64}$'),
  output_snapshot_sha256 text NOT NULL CHECK (output_snapshot_sha256 ~ '^[a-f0-9]{64}$'),
  registry_scope text NOT NULL CHECK (registry_scope IN ('NOT_READ', 'SNAPSHOT_BOUND')),
  registry_snapshot_sha256 text CHECK (registry_snapshot_sha256 IS NULL OR registry_snapshot_sha256 ~ '^[a-f0-9]{64}$'),
  environment_fidelity text NOT NULL CHECK (environment_fidelity IN (
    'E0_SYNTHETIC', 'E1_REALISTIC_FIXTURE', 'E2_REPOSITORY_INTEGRATED',
    'E3_PRODUCTION_SHAPED', 'E4_REAL_WORLD_OBSERVED'
  )),
  environment_identity jsonb NOT NULL,
  evaluator_versions jsonb NOT NULL,
  validator_results jsonb NOT NULL,
  reward_hack_result text NOT NULL CHECK (reward_hack_result IN ('PASS', 'FAIL', 'UNVERIFIED', 'NOT_APPLICABLE')),
  taste_integrity_result text NOT NULL CHECK (taste_integrity_result IN ('PASS', 'FAIL', 'UNVERIFIED', 'NOT_APPLICABLE')),
  anti_centroid_result text NOT NULL CHECK (anti_centroid_result IN ('PASS', 'FAIL', 'UNVERIFIED', 'NOT_APPLICABLE')),
  evidence_status text NOT NULL CHECK (evidence_status IN ('TRACEABLE', 'INCOMPLETE', 'QUARANTINED', 'NOT_APPLICABLE')),
  payload_sha256 text NOT NULL CHECK (payload_sha256 ~ '^[a-f0-9]{64}$'),
  payload_canonical_json text NOT NULL,
  payload jsonb NOT NULL,
  recorded_at timestamptz NOT NULL DEFAULT now(),
  CHECK ((registry_scope = 'NOT_READ' AND registry_snapshot_sha256 IS NULL)
      OR (registry_scope = 'SNAPSHOT_BOUND' AND registry_snapshot_sha256 IS NOT NULL)),
  CHECK (jsonb_typeof(environment_identity) = 'object'),
  CHECK (jsonb_typeof(evaluator_versions) = 'object'),
  CHECK (jsonb_typeof(validator_results) = 'object')
);

CREATE TABLE cae.receipt_evidence_link (
  receipt_id text NOT NULL REFERENCES cae.receipt(receipt_id),
  evidence_id text NOT NULL REFERENCES cae.evidence_item(evidence_id),
  lineage_role text NOT NULL CHECK (lineage_role IN ('CREATED', 'AUTHENTICATES', 'SUPPORTS', 'VALIDATES', 'CONFIRMS')),
  PRIMARY KEY (receipt_id, evidence_id, lineage_role)
);

CREATE INDEX idx_execution_receipt_claim ON cae.execution_receipt(claim_id, recorded_at);
CREATE INDEX idx_receipt_evidence_link_evidence ON cae.receipt_evidence_link(evidence_id, receipt_id);

CREATE OR REPLACE VIEW cae.v_receipt_evidence_lineage
WITH (security_invoker = true)
AS
SELECT
  execution.receipt_id,
  execution.claim_id,
  execution.component_id,
  execution.environment_fidelity,
  execution.registry_scope,
  execution.registry_snapshot_sha256,
  execution.evidence_status,
  link.lineage_role,
  evidence.evidence_id,
  evidence.state AS evidence_state,
  source.source_package_id,
  asset.asset_id AS source_asset_id,
  asset.canonical_uri AS source_asset_uri,
  asset.content_sha256 AS source_asset_sha256
FROM cae.execution_receipt execution
JOIN cae.receipt_evidence_link link ON link.receipt_id = execution.receipt_id
JOIN cae.evidence_item evidence ON evidence.evidence_id = link.evidence_id
JOIN cae.source_package source ON source.source_package_id = evidence.source_package_id
JOIN cae.media_asset asset ON asset.asset_id = source.media_asset_id;

CREATE TRIGGER cae_10_execution_receipt_payload_integrity
  BEFORE INSERT OR UPDATE ON cae.execution_receipt
  FOR EACH ROW EXECUTE FUNCTION cae.verify_immutable_payload('payload_sha256');

CREATE TRIGGER cae_00_execution_receipt_immutable
  BEFORE UPDATE OR DELETE ON cae.execution_receipt
  FOR EACH ROW EXECUTE FUNCTION cae.reject_immutable_evidence_mutation();
CREATE TRIGGER cae_00_receipt_evidence_link_immutable
  BEFORE UPDATE OR DELETE ON cae.receipt_evidence_link
  FOR EACH ROW EXECUTE FUNCTION cae.reject_immutable_evidence_mutation();

ALTER TABLE cae.execution_receipt ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.receipt_evidence_link ENABLE ROW LEVEL SECURITY;
