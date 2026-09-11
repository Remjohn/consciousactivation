-- STATUS: APPLIED_STAGING
-- DO NOT EXECUTE DIRECTLY OUTSIDE AN AUTHORIZED APPLICATION MANDATE
-- Migration ID: MIG-0003
-- Title: CAE Domain Entities (Engagement, Guest, Media Asset)
-- Predecessor: MIG-0002
-- Preconditions: MIG-0002 applied; cae.workspace table exists
-- Data Action Class: SCHEMA_ONLY_NO_DML
-- Governing Phase: CA-MIG-03

-- 5. cae.engagement (Project Envelope)
CREATE TABLE IF NOT EXISTS cae.engagement (
    engagement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    lifecycle_state VARCHAR(32) NOT NULL DEFAULT 'PLANNED',
    version BIGINT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_engagement UNIQUE (workspace_id, engagement_id)
);

-- 6. cae.guest (Subject Entity)
CREATE TABLE IF NOT EXISTS cae.guest (
    guest_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    external_ref VARCHAR(128) NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_guest UNIQUE (workspace_id, guest_id)
);

-- 7. cae.media_asset (Artifact & Evidence Entity)
CREATE TABLE IF NOT EXISTS cae.media_asset (
    media_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    engagement_id UUID,
    media_type VARCHAR(64) NOT NULL,
    storage_path VARCHAR(512) NOT NULL,
    byte_size BIGINT NOT NULL,
    sha256_checksum CHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'UNVERIFIED',
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT uq_workspace_media UNIQUE (workspace_id, media_id),
    CONSTRAINT uq_workspace_storage_path UNIQUE (workspace_id, storage_path)
);
