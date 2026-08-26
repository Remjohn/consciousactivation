-- STATUS: DRAFT_NOT_APPLIED
-- DO NOT EXECUTE DIRECTLY OUTSIDE AN AUTHORIZED APPLICATION MANDATE
-- Migration ID: MIG-0006
-- Title: CAE Performance Indexes and Integrity Constraints
-- Predecessor: MIG-0005
-- Preconditions: MIG-0005 applied; tables and RLS configured
-- Data Action Class: PERFORMANCE_INDEXES_NO_DML
-- Governing Phase: CA-MIG-03

-- Workspace & Actor Lookups
CREATE INDEX IF NOT EXISTS idx_workspace_slug ON cae.workspace (slug);
CREATE INDEX IF NOT EXISTS idx_membership_actor ON cae.workspace_membership (actor_id);
CREATE INDEX IF NOT EXISTS idx_membership_workspace ON cae.workspace_membership (workspace_id);

-- Ephemeral Grant Lookups
CREATE INDEX IF NOT EXISTS idx_grant_active ON cae.operator_access_grant (workspace_id, operator_actor_id)
    WHERE revoked_at IS NULL;

-- Domain Entity Lookups
CREATE INDEX IF NOT EXISTS idx_engagement_workspace_state ON cae.engagement (workspace_id, lifecycle_state);
CREATE INDEX IF NOT EXISTS idx_guest_workspace_ref ON cae.guest (workspace_id, external_ref);
CREATE INDEX IF NOT EXISTS idx_media_workspace_checksum ON cae.media_asset (workspace_id, sha256_checksum);

-- Execution & Receipt Lookups
CREATE INDEX IF NOT EXISTS idx_harness_run_workspace_status ON cae.harness_run (workspace_id, status);
CREATE INDEX IF NOT EXISTS idx_receipt_workspace_created ON cae.receipt (workspace_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_evidence_link_receipt ON cae.receipt_evidence_link (workspace_id, receipt_id);
