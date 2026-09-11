-- STATUS: APPLIED_STAGING
-- DO NOT EXECUTE DIRECTLY OUTSIDE AN AUTHORIZED APPLICATION MANDATE
-- Migration ID: MIG-0002
-- Title: CAE Tenancy and Operator Access Scaffolding
-- Predecessor: MIG-0001
-- Preconditions: MIG-0001 applied; schema 'cae' exists
-- Data Action Class: SCHEMA_ONLY_NO_DML
-- Governing Phase: CA-MIG-03

-- 1. cae.workspace (Tenant Isolation Root)
CREATE TABLE IF NOT EXISTS cae.workspace (
    workspace_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(64) UNIQUE NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

-- 2. cae.workspace_membership (Actor Binding)
CREATE TABLE IF NOT EXISTS cae.workspace_membership (
    membership_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    actor_id VARCHAR(128) NOT NULL,
    role VARCHAR(32) NOT NULL DEFAULT 'MEMBER',
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_membership_actor UNIQUE (workspace_id, actor_id)
);

-- 3. cae.operator_organization (Governance Root - Platform Scope)
CREATE TABLE IF NOT EXISTS cae.operator_organization (
    operator_org_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_name VARCHAR(255) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

-- 4. cae.operator_access_grant (Ephemeral Support Grant)
CREATE TABLE IF NOT EXISTS cae.operator_access_grant (
    grant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    operator_org_id UUID NOT NULL REFERENCES cae.operator_organization(operator_org_id),
    operator_actor_id VARCHAR(128) NOT NULL,
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    justification TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);
