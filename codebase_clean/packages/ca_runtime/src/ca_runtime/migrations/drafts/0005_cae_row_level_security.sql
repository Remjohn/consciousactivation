-- STATUS: APPLIED_STAGING
-- DO NOT EXECUTE DIRECTLY OUTSIDE AN AUTHORIZED APPLICATION MANDATE
-- Migration ID: MIG-0005
-- Title: CAE Row-Level Security Enablement and Tenant Isolation Policies
-- Predecessor: MIG-0004
-- Preconditions: MIG-0004 applied; all 10 cae tables created
-- Data Action Class: SECURITY_ONLY_NO_DML
-- Governing Phase: CA-MIG-03

-- Enable RLS across all 10 core tables
ALTER TABLE cae.workspace ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.workspace_membership ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.operator_organization ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.operator_access_grant ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.engagement ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.guest ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.media_asset ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.harness_template ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.harness_run ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.receipt ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.receipt_evidence_link ENABLE ROW LEVEL SECURITY;

-- 1. cae.workspace Isolation Policy
DROP POLICY IF EXISTS p_workspace_isolation ON cae.workspace;
CREATE POLICY p_workspace_isolation ON cae.workspace
    FOR ALL
    USING (
        workspace_id::text = current_setting('app.current_workspace_id', true)
        OR current_setting('app.is_system_operator', true) = 'true'
    );

-- 2. cae.workspace_membership Isolation Policy
DROP POLICY IF EXISTS p_membership_isolation ON cae.workspace_membership;
CREATE POLICY p_membership_isolation ON cae.workspace_membership
    FOR ALL
    USING (
        workspace_id::text = current_setting('app.current_workspace_id', true)
        OR current_setting('app.is_system_operator', true) = 'true'
    );

-- 3. cae.operator_access_grant Policy
DROP POLICY IF EXISTS p_operator_grant_isolation ON cae.operator_access_grant;
CREATE POLICY p_operator_grant_isolation ON cae.operator_access_grant
    FOR ALL
    USING (
        workspace_id::text = current_setting('app.current_workspace_id', true)
        OR current_setting('app.is_system_operator', true) = 'true'
    );

-- 4. cae.engagement Isolation Policy
DROP POLICY IF EXISTS p_engagement_isolation ON cae.engagement;
CREATE POLICY p_engagement_isolation ON cae.engagement
    FOR ALL
    USING (
        workspace_id::text = current_setting('app.current_workspace_id', true)
        OR current_setting('app.is_system_operator', true) = 'true'
    );

-- 5. cae.guest Isolation Policy
DROP POLICY IF EXISTS p_guest_isolation ON cae.guest;
CREATE POLICY p_guest_isolation ON cae.guest
    FOR ALL
    USING (
        workspace_id::text = current_setting('app.current_workspace_id', true)
        OR current_setting('app.is_system_operator', true) = 'true'
    );

-- 6. cae.media_asset Isolation Policy
DROP POLICY IF EXISTS p_media_asset_isolation ON cae.media_asset;
CREATE POLICY p_media_asset_isolation ON cae.media_asset
    FOR ALL
    USING (
        workspace_id::text = current_setting('app.current_workspace_id', true)
        OR current_setting('app.is_system_operator', true) = 'true'
    );

-- 7. cae.harness_template Isolation Policy
DROP POLICY IF EXISTS p_template_isolation ON cae.harness_template;
CREATE POLICY p_template_isolation ON cae.harness_template
    FOR ALL
    USING (
        workspace_id::text = current_setting('app.current_workspace_id', true)
        OR current_setting('app.is_system_operator', true) = 'true'
    );

-- 8. cae.harness_run Isolation Policy
DROP POLICY IF EXISTS p_run_isolation ON cae.harness_run;
CREATE POLICY p_run_isolation ON cae.harness_run
    FOR ALL
    USING (
        workspace_id::text = current_setting('app.current_workspace_id', true)
        OR current_setting('app.is_system_operator', true) = 'true'
    );

-- 9. cae.receipt Isolation Policy
DROP POLICY IF EXISTS p_receipt_isolation ON cae.receipt;
CREATE POLICY p_receipt_isolation ON cae.receipt
    FOR ALL
    USING (
        workspace_id::text = current_setting('app.current_workspace_id', true)
        OR current_setting('app.is_system_operator', true) = 'true'
    );

-- 10. cae.receipt_evidence_link Isolation Policy
DROP POLICY IF EXISTS p_link_isolation ON cae.receipt_evidence_link;
CREATE POLICY p_link_isolation ON cae.receipt_evidence_link
    FOR ALL
    USING (
        workspace_id::text = current_setting('app.current_workspace_id', true)
        OR current_setting('app.is_system_operator', true) = 'true'
    );
