-- STATUS: APPLIED_STAGING
-- DO NOT EXECUTE DIRECTLY OUTSIDE AN AUTHORIZED APPLICATION MANDATE
-- Migration ID: MIG-0005
-- Title: CAE Knowledge Nodes, Edges, Projections, Provenance Links, and Search Index
-- Predecessor: MIG-0004
-- Preconditions: MIG-0004 applied; cae.workspace table exists
-- Data Action Class: SCHEMA_ONLY_NO_DML
-- Governing Phase: CA-MIG-03 / Phase 3 M30

-- 12. cae.knowledge_node (Authoritative Curated Knowledge Entity)
CREATE TABLE IF NOT EXISTS cae.knowledge_node (
    node_id VARCHAR(128) NOT NULL,
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    canonical_label VARCHAR(255) NOT NULL,
    category VARCHAR(64) NOT NULL DEFAULT 'concept',
    definition TEXT NOT NULL,
    lifecycle_status VARCHAR(32) NOT NULL DEFAULT 'active',
    authority_class VARCHAR(64) NOT NULL DEFAULT 'derived_validated_knowledge',
    lineage_sha256 CHAR(64) NOT NULL,
    version BIGINT NOT NULL DEFAULT 1,
    supersedes_node_id VARCHAR(128),
    retraction_reason TEXT,
    node_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT pk_knowledge_node PRIMARY KEY (workspace_id, node_id)
);

-- 13. cae.knowledge_edge (Relational Edge Between Knowledge Entities)
CREATE TABLE IF NOT EXISTS cae.knowledge_edge (
    edge_id VARCHAR(128) NOT NULL,
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    source_node_id VARCHAR(128) NOT NULL,
    target_node_id VARCHAR(128) NOT NULL,
    relation_type VARCHAR(64) NOT NULL,
    confidence_score BIGINT NOT NULL DEFAULT 100,
    adjudicated BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT pk_knowledge_edge PRIMARY KEY (workspace_id, edge_id)
);

-- 14. cae.knowledge_projection (Authoritative Operational Query Projection)
CREATE TABLE IF NOT EXISTS cae.knowledge_projection (
    projection_id VARCHAR(128) NOT NULL,
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    node_id VARCHAR(128) NOT NULL,
    source_kind VARCHAR(64) NOT NULL DEFAULT 'research_knowledge',
    authority_state VARCHAR(32) NOT NULL DEFAULT 'current',
    lifecycle_state VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    title VARCHAR(255) NOT NULL,
    summary TEXT NOT NULL,
    content_sha256 CHAR(64) NOT NULL,
    projection_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    rebuild_count BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT pk_knowledge_projection PRIMARY KEY (workspace_id, projection_id)
);

-- 15. cae.knowledge_provenance_link (Lineage Link to Immutable Source Records)
CREATE TABLE IF NOT EXISTS cae.knowledge_provenance_link (
    link_id VARCHAR(128) NOT NULL,
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    node_id VARCHAR(128) NOT NULL,
    source_id VARCHAR(128) NOT NULL,
    source_sha256 CHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT pk_knowledge_provenance_link PRIMARY KEY (workspace_id, link_id)
);

-- 16. cae.knowledge_search_index (Token & Term Search Index)
CREATE TABLE IF NOT EXISTS cae.knowledge_search_index (
    index_id VARCHAR(128) NOT NULL,
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    node_id VARCHAR(128) NOT NULL,
    tokens_text TEXT NOT NULL,
    exact_terms_text TEXT NOT NULL,
    category VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    CONSTRAINT pk_knowledge_search_index PRIMARY KEY (workspace_id, index_id)
);

-- Enable RLS on all knowledge tables
ALTER TABLE cae.knowledge_node ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.knowledge_edge ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.knowledge_projection ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.knowledge_provenance_link ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.knowledge_search_index ENABLE ROW LEVEL SECURITY;

-- Grant SELECT permissions to authenticated users
GRANT SELECT ON cae.knowledge_node, cae.knowledge_edge, cae.knowledge_projection,
    cae.knowledge_provenance_link, cae.knowledge_search_index TO authenticated;

-- Row Level Security Scoping Policies
CREATE POLICY knowledge_node_read ON cae.knowledge_node
    FOR SELECT TO authenticated
    USING (cae.has_workspace_access(workspace_id::text));

CREATE POLICY knowledge_edge_read ON cae.knowledge_edge
    FOR SELECT TO authenticated
    USING (cae.has_workspace_access(workspace_id::text));

CREATE POLICY knowledge_projection_read ON cae.knowledge_projection
    FOR SELECT TO authenticated
    USING (cae.has_workspace_access(workspace_id::text));

CREATE POLICY knowledge_provenance_link_read ON cae.knowledge_provenance_link
    FOR SELECT TO authenticated
    USING (cae.has_workspace_access(workspace_id::text));

CREATE POLICY knowledge_search_index_read ON cae.knowledge_search_index
    FOR SELECT TO authenticated
    USING (cae.has_workspace_access(workspace_id::text));
