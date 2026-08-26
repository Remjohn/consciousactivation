-- STATUS: APPLIED_STAGING
-- DO NOT EXECUTE DIRECTLY OUTSIDE AN AUTHORIZED APPLICATION MANDATE
-- Migration ID: MIG-0004
-- Title: CAE Harness Execution and Append-Only Receipt Ledger
-- Predecessor: MIG-0003
-- Preconditions: MIG-0003 applied; domain tables exist
-- Data Action Class: SCHEMA_ONLY_NO_DML
-- Governing Phase: CA-MIG-03

-- 8. cae.harness_template (Execution Blueprint)
CREATE TABLE IF NOT EXISTS cae.harness_template (
    template_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(32) NOT NULL DEFAULT '1.0.0',
    config_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_template UNIQUE (workspace_id, template_id)
);

-- 9. cae.harness_run (Pipeline Instance)
CREATE TABLE IF NOT EXISTS cae.harness_run (
    run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL,
    template_id UUID NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    parameters JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_run UNIQUE (workspace_id, run_id),
    CONSTRAINT fk_harness_run_template FOREIGN KEY (workspace_id, template_id)
        REFERENCES cae.harness_template(workspace_id, template_id) ON DELETE CASCADE
);

-- 10. cae.receipt (Immutable Execution Receipt)
CREATE TABLE IF NOT EXISTS cae.receipt (
    receipt_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    action_type VARCHAR(64) NOT NULL,
    actor_id VARCHAR(128) NOT NULL,
    result_status VARCHAR(32) NOT NULL,
    payload_hash CHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_receipt UNIQUE (workspace_id, receipt_id)
);

-- 11. cae.receipt_evidence_link (Lineage Link)
CREATE TABLE IF NOT EXISTS cae.receipt_evidence_link (
    link_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL,
    receipt_id UUID NOT NULL REFERENCES cae.receipt(receipt_id) ON DELETE CASCADE,
    evidence_type VARCHAR(64) NOT NULL,
    evidence_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_receipt_evidence UNIQUE (workspace_id, receipt_id, evidence_type, evidence_id)
);

-- Append-Only Immutability Guard Trigger Function
CREATE OR REPLACE FUNCTION cae.fn_prevent_receipt_mutation()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'EX_RECEIPT_IMMUTABLE: cae.receipt records are strictly append-only; UPDATE and DELETE are prohibited.'
        USING ERRCODE = '55000';
END;
$$ LANGUAGE plpgsql;

-- Bind Immutability Trigger to cae.receipt
DROP TRIGGER IF EXISTS trg_receipt_append_only ON cae.receipt;
CREATE TRIGGER trg_receipt_append_only
    BEFORE UPDATE OR DELETE ON cae.receipt
    FOR EACH ROW
    EXECUTE FUNCTION cae.fn_prevent_receipt_mutation();
