#!/usr/bin/env python3
"""Standalone staging migration script applying CA-IMPL-01A relational containment scaffolding.

Applies:
1. cae.* relational tables with composite foreign keys enforcing Workspace tenant boundaries.
2. Row-Level Security (RLS) policies enforcing Workspace isolation and ephemeral operator grants.
3. Append-only triggers on cae.receipt prohibiting UPDATE/DELETE.

Governed by TS-CAE-TEN-001, MC-CAE-WS-001 through MC-CAE-REC-001, and CA-IMPL-01A Mandate.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from urllib.parse import urlsplit

import psycopg

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ENVIRONMENT_VARIABLE = "CAE_SUPABASE_DATABASE_URL"
PROJECT_REF = "evnxdssbxxrsesftdvgx"


def load_local_environment() -> None:
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8-sig").splitlines():
            key, separator, value = line.partition("=")
            if separator and key and not key.lstrip().startswith("#"):
                os.environ.setdefault(key.strip(), value.strip())


def connection_url() -> str:
    url = os.environ.get(ENVIRONMENT_VARIABLE, "")
    if not url:
        raise RuntimeError(f"Missing environment variable: {ENVIRONMENT_VARIABLE}")
    parsed = urlsplit(url)
    if not (
        parsed.hostname
        and parsed.hostname.endswith(".pooler.supabase.com")
        and parsed.port == 5432
        and parsed.username == f"postgres.{PROJECT_REF}"
    ):
        raise RuntimeError(f"Connection endpoint is not the approved CAE staging session pooler: {parsed.hostname}")
    return url


SCAFFOLDING_DDL = """
-- Extension and schema initialization
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE SCHEMA IF NOT EXISTS cae;

-- Drop obsolete draft tables if present to ensure clean type conformance with TS-CAE-TEN-001
DROP TABLE IF EXISTS cae.receipt_evidence_link CASCADE;
DROP TABLE IF EXISTS cae.receipt CASCADE;
DROP TABLE IF EXISTS cae.harness_run CASCADE;
DROP TABLE IF EXISTS cae.harness_template CASCADE;
DROP TABLE IF EXISTS cae.media_asset CASCADE;
DROP TABLE IF EXISTS cae.guest CASCADE;
DROP TABLE IF EXISTS cae.engagement CASCADE;
DROP TABLE IF EXISTS cae.operator_access_grant CASCADE;
DROP TABLE IF EXISTS cae.operator_organization CASCADE;
DROP TABLE IF EXISTS cae.workspace_membership CASCADE;
DROP TABLE IF EXISTS cae.workspace CASCADE;

-- 1. cae.workspace (Tenant Isolation Root)
CREATE TABLE cae.workspace (
    workspace_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(64) UNIQUE NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

-- 2. cae.workspace_membership (Actor Binding)
CREATE TABLE cae.workspace_membership (
    membership_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    actor_id VARCHAR(128) NOT NULL,
    role VARCHAR(32) NOT NULL DEFAULT 'MEMBER',
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_membership_actor UNIQUE (workspace_id, actor_id)
);

-- 3. cae.operator_organization (Governance Root - Platform Scope)
CREATE TABLE cae.operator_organization (
    operator_org_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_name VARCHAR(255) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

-- 4. cae.operator_access_grant (Ephemeral Support Grant)
CREATE TABLE cae.operator_access_grant (
    grant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    operator_org_id UUID NOT NULL REFERENCES cae.operator_organization(operator_org_id),
    operator_actor_id VARCHAR(128) NOT NULL,
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    justification TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);

-- 5. cae.engagement (Project Envelope)
CREATE TABLE cae.engagement (
    engagement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    lifecycle_state VARCHAR(32) NOT NULL DEFAULT 'PLANNED',
    version BIGINT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_engagement UNIQUE (workspace_id, engagement_id)
);

-- 6. cae.guest (Strictly Workspace-Local Participant)
CREATE TABLE cae.guest (
    guest_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    external_reference_id VARCHAR(128),
    pseudonym VARCHAR(128) NOT NULL,
    consent_status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_guest UNIQUE (workspace_id, guest_id)
);

-- 7. cae.media_asset (Relational Verification Metadata)
CREATE TABLE cae.media_asset (
    media_asset_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    engagement_id UUID,
    storage_path TEXT NOT NULL,
    canonical_sha256 VARCHAR(64) NOT NULL,
    byte_size BIGINT NOT NULL,
    mime_type VARCHAR(128) NOT NULL,
    lifecycle_state VARCHAR(32) NOT NULL DEFAULT 'REGISTERED',
    version BIGINT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_media_asset UNIQUE (workspace_id, media_asset_id),
    CONSTRAINT fk_media_asset_engagement FOREIGN KEY (workspace_id, engagement_id)
        REFERENCES cae.engagement(workspace_id, engagement_id) ON DELETE SET NULL
);

-- 8. cae.harness_template (Canonical Structural Grammar - Canonical Plane)
CREATE TABLE cae.harness_template (
    template_id VARCHAR(64) NOT NULL,
    version VARCHAR(32) NOT NULL,
    definition_yaml TEXT NOT NULL,
    definition_sha256 VARCHAR(64) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    PRIMARY KEY (template_id, version)
);

-- 9. cae.harness_run (Operational Run State Machine)
CREATE TABLE cae.harness_run (
    run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    engagement_id UUID NOT NULL,
    template_id VARCHAR(64) NOT NULL,
    template_version VARCHAR(32) NOT NULL,
    current_step VARCHAR(64) NOT NULL,
    lifecycle_state VARCHAR(32) NOT NULL DEFAULT 'INITIALIZED',
    version BIGINT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_harness_run UNIQUE (workspace_id, run_id),
    CONSTRAINT fk_harness_run_engagement FOREIGN KEY (workspace_id, engagement_id)
        REFERENCES cae.engagement(workspace_id, engagement_id) ON DELETE CASCADE,
    CONSTRAINT fk_harness_run_template FOREIGN KEY (template_id, template_version)
        REFERENCES cae.harness_template(template_id, version)
);

-- 10. cae.receipt (Immutable Execution & Audit Ledger)
CREATE TABLE cae.receipt (
    receipt_id VARCHAR(128) PRIMARY KEY,
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    operation_id VARCHAR(128) NOT NULL,
    idempotency_key VARCHAR(128) NOT NULL,
    actor_id VARCHAR(128) NOT NULL,
    canonical_payload TEXT NOT NULL,
    payload_jsonb JSONB NOT NULL,
    payload_sha256 VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_receipt_idemp UNIQUE (workspace_id, operation_id, idempotency_key)
);

-- 11. cae.receipt_evidence_link (Reality Contact Junction)
CREATE TABLE cae.receipt_evidence_link (
    link_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    receipt_id VARCHAR(128) NOT NULL REFERENCES cae.receipt(receipt_id) ON DELETE CASCADE,
    evidence_item_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_receipt_evidence_link UNIQUE (workspace_id, receipt_id, evidence_item_id)
);

-- Append-only trigger for cae.receipt
CREATE OR REPLACE FUNCTION cae.prevent_receipt_mutation()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'RECEIPT_MUTATION_FORBIDDEN: Receipts in cae.receipt are append-only immutable records.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_prevent_receipt_mutation ON cae.receipt;
CREATE TRIGGER trg_prevent_receipt_mutation
BEFORE UPDATE OR DELETE ON cae.receipt
FOR EACH ROW
EXECUTE FUNCTION cae.prevent_receipt_mutation();

-- Enable Row-Level Security on all operational tables
ALTER TABLE cae.workspace ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.workspace_membership ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.operator_access_grant ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.engagement ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.guest ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.media_asset ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.harness_run ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.receipt ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.receipt_evidence_link ENABLE ROW LEVEL SECURITY;

-- Helper function for operator access grant validation
CREATE OR REPLACE FUNCTION cae.has_active_operator_grant(target_workspace_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
    IF current_setting('app.is_operator', true) = 'true' THEN
        RETURN EXISTS (
            SELECT 1 FROM cae.operator_access_grant g
            WHERE g.grant_id = NULLIF(current_setting('app.current_operator_grant_id', true), '')::uuid
              AND g.workspace_id = target_workspace_id
              AND g.expires_at > clock_timestamp()
              AND g.revoked_at IS NULL
        );
    END IF;
    RETURN FALSE;
EXCEPTION
    WHEN OTHERS THEN
        RETURN FALSE;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

-- RLS Policies for Tenant Isolation Root (cae.workspace)
DROP POLICY IF EXISTS p_workspace_tenant_isolation ON cae.workspace;
CREATE POLICY p_workspace_tenant_isolation ON cae.workspace
FOR ALL
USING (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
)
WITH CHECK (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
);

-- RLS Policies for child operational tables
DROP POLICY IF EXISTS p_membership_tenant_isolation ON cae.workspace_membership;
CREATE POLICY p_membership_tenant_isolation ON cae.workspace_membership
FOR ALL
USING (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
)
WITH CHECK (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
);

DROP POLICY IF EXISTS p_operator_grant_tenant_isolation ON cae.operator_access_grant;
CREATE POLICY p_operator_grant_tenant_isolation ON cae.operator_access_grant
FOR ALL
USING (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR current_setting('app.is_operator', true) = 'true'
)
WITH CHECK (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR current_setting('app.is_operator', true) = 'true'
);

DROP POLICY IF EXISTS p_engagement_tenant_isolation ON cae.engagement;
CREATE POLICY p_engagement_tenant_isolation ON cae.engagement
FOR ALL
USING (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
)
WITH CHECK (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
);

DROP POLICY IF EXISTS p_guest_tenant_isolation ON cae.guest;
CREATE POLICY p_guest_tenant_isolation ON cae.guest
FOR ALL
USING (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
)
WITH CHECK (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
);

DROP POLICY IF EXISTS p_media_asset_tenant_isolation ON cae.media_asset;
CREATE POLICY p_media_asset_tenant_isolation ON cae.media_asset
FOR ALL
USING (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
)
WITH CHECK (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
);

DROP POLICY IF EXISTS p_harness_run_tenant_isolation ON cae.harness_run;
CREATE POLICY p_harness_run_tenant_isolation ON cae.harness_run
FOR ALL
USING (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
)
WITH CHECK (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
);

DROP POLICY IF EXISTS p_receipt_tenant_isolation ON cae.receipt;
CREATE POLICY p_receipt_tenant_isolation ON cae.receipt
FOR ALL
USING (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
)
WITH CHECK (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
);

DROP POLICY IF EXISTS p_receipt_link_tenant_isolation ON cae.receipt_evidence_link;
CREATE POLICY p_receipt_link_tenant_isolation ON cae.receipt_evidence_link
FOR ALL
USING (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
)
WITH CHECK (
    workspace_id = NULLIF(current_setting('app.current_workspace_id', true), '')::uuid
    OR cae.has_active_operator_grant(workspace_id)
);

-- Grants for Supabase authenticated and service_role execution
GRANT USAGE ON SCHEMA cae TO authenticated, anon, service_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA cae TO authenticated, anon, service_role;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA cae TO authenticated, anon, service_role;
GRANT ALL PRIVILEGES ON ALL ROUTINES IN SCHEMA cae TO authenticated, anon, service_role;
"""


def apply_scaffolding() -> int:
    load_local_environment()
    ddl_sha256 = hashlib.sha256(SCAFFOLDING_DDL.encode("utf-8")).hexdigest()
    print("================================================================================")
    print("   CAE STAGING SCAFFOLDING MIGRATION: CA-IMPL-01A                               ")
    print("================================================================================")
    print(f"Target endpoint: {connection_url().split('@')[-1]}")
    print(f"Scaffolding DDL SHA-256: {ddl_sha256}")

    try:
        with psycopg.connect(connection_url(), connect_timeout=15) as conn:
            with conn.cursor() as cur:
                cur.execute(SCAFFOLDING_DDL)
            conn.commit()
        print("Scaffolding DDL status: APPLIED_SUCCESSFULLY")
        return 0
    except Exception as exc:
        print(f"Scaffolding DDL status: FAILED ({type(exc).__name__}: {exc})")
        return 1


if __name__ == "__main__":
    raise SystemExit(apply_scaffolding())
