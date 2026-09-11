-- STATUS: APPLIED_STAGING
-- DO NOT EXECUTE DIRECTLY OUTSIDE AN AUTHORIZED APPLICATION MANDATE
-- Migration ID: MIG-0009
-- Title: CAE RLS Completion and Target Schema Reconciliation
-- Predecessor: MIG-0008
-- Preconditions: MIG-0008 applied; canonical UUID schema and quarantine structures active
-- Data Action Class: SECURITY_AND_SCHEMA_COMPLETION_NO_DML
-- Governing Mandate: CA-TWC-01 (Sub-workstream T1)

-- 1. Restore canonical table names for workspace and media_asset if renamed by MIG-0008
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cae' AND table_name = 'legacy_wp03_workspace') THEN
        ALTER TABLE cae.legacy_wp03_workspace RENAME TO workspace;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'cae' AND table_name = 'legacy_wp03_media_asset') THEN
        ALTER TABLE cae.legacy_wp03_media_asset RENAME TO media_asset;
    END IF;
END $$;

-- 2. Preserve legacy quarantine markers as explicit archive structures
CREATE TABLE IF NOT EXISTS cae.legacy_wp03_workspace (
    legacy_id VARCHAR(128) PRIMARY KEY,
    archived_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    quarantine_reason VARCHAR(255) NOT NULL DEFAULT 'REPLACED_BY_CANONICAL_UUID_SCHEMA'
);

CREATE TABLE IF NOT EXISTS cae.legacy_wp03_media_asset (
    legacy_id VARCHAR(128) PRIMARY KEY,
    archived_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    quarantine_reason VARCHAR(255) NOT NULL DEFAULT 'REPLACED_BY_CANONICAL_UUID_SCHEMA'
);

CREATE TABLE IF NOT EXISTS cae.legacy_wp03_execution_receipt (
    legacy_id VARCHAR(128) PRIMARY KEY,
    archived_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    quarantine_reason VARCHAR(255) NOT NULL DEFAULT 'REPLACED_BY_CANONICAL_UUID_SCHEMA'
);

-- 3. Create guest_profile canonical view for guest domain entity
CREATE OR REPLACE VIEW cae.guest_profile AS
    SELECT 
        guest_id AS guest_profile_id,
        guest_id,
        workspace_id,
        external_ref,
        display_name,
        status,
        created_at,
        updated_at
    FROM cae.guest;

-- 4. Complete RLS on operator_organization and harness_template
ALTER TABLE cae.operator_organization ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS p_operator_org_isolation ON cae.operator_organization;
CREATE POLICY p_operator_org_isolation ON cae.operator_organization
    FOR ALL
    USING (
        status = 'ACTIVE'
        OR current_setting('app.is_system_operator', true) = 'true'
    );


ALTER TABLE cae.harness_template ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS p_template_isolation ON cae.harness_template;
CREATE POLICY p_template_isolation ON cae.harness_template
    FOR ALL
    USING (
        workspace_id::text = current_setting('app.current_workspace_id', true)
        OR current_setting('app.is_system_operator', true) = 'true'
    );

-- 5. Force Row-Level Security across all tenant tables (enforces RLS on table owners/superusers)
ALTER TABLE cae.workspace FORCE ROW LEVEL SECURITY;
ALTER TABLE cae.workspace_membership FORCE ROW LEVEL SECURITY;
ALTER TABLE cae.operator_organization FORCE ROW LEVEL SECURITY;
ALTER TABLE cae.operator_access_grant FORCE ROW LEVEL SECURITY;
ALTER TABLE cae.engagement FORCE ROW LEVEL SECURITY;
ALTER TABLE cae.guest FORCE ROW LEVEL SECURITY;
ALTER TABLE cae.media_asset FORCE ROW LEVEL SECURITY;
ALTER TABLE cae.harness_template FORCE ROW LEVEL SECURITY;
ALTER TABLE cae.harness_run FORCE ROW LEVEL SECURITY;
ALTER TABLE cae.receipt FORCE ROW LEVEL SECURITY;
ALTER TABLE cae.receipt_evidence_link FORCE ROW LEVEL SECURITY;
ALTER TABLE cae.legacy_wp03_workspace ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.legacy_wp03_workspace FORCE ROW LEVEL SECURITY;
ALTER TABLE cae.legacy_wp03_media_asset ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.legacy_wp03_media_asset FORCE ROW LEVEL SECURITY;
ALTER TABLE cae.legacy_wp03_execution_receipt ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.legacy_wp03_execution_receipt FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS p_legacy_workspace_system_only ON cae.legacy_wp03_workspace;
CREATE POLICY p_legacy_workspace_system_only ON cae.legacy_wp03_workspace
    FOR ALL USING (current_setting('app.is_system_operator', true) = 'true');

DROP POLICY IF EXISTS p_legacy_media_system_only ON cae.legacy_wp03_media_asset;
CREATE POLICY p_legacy_media_system_only ON cae.legacy_wp03_media_asset
    FOR ALL USING (current_setting('app.is_system_operator', true) = 'true');

DROP POLICY IF EXISTS p_legacy_receipt_system_only ON cae.legacy_wp03_execution_receipt;
CREATE POLICY p_legacy_receipt_system_only ON cae.legacy_wp03_execution_receipt
    FOR ALL USING (current_setting('app.is_system_operator', true) = 'true');


-- 6. Grant Schema and Table permissions to Supabase authenticated and anon roles
GRANT USAGE ON SCHEMA cae TO authenticated, anon;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA cae TO authenticated, anon;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA cae TO authenticated, anon;
GRANT ALL PRIVILEGES ON ALL ROUTINES IN SCHEMA cae TO authenticated, anon;


