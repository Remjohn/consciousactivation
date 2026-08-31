-- 0006_cae_knowledge_clusters_signals.sql
-- CAE Phase 3 Mandate M31: Knowledge Clusters + Research Signals + Context Projection

CREATE SCHEMA IF NOT EXISTS cae;

-- 1. Knowledge Clusters
CREATE TABLE IF NOT EXISTS cae.knowledge_cluster (
    workspace_id TEXT NOT NULL,
    cluster_id TEXT NOT NULL,
    cluster_label TEXT NOT NULL,
    theme TEXT NOT NULL,
    cluster_type TEXT NOT NULL,
    coherence_score_micros INTEGER NOT NULL CHECK (coherence_score_micros >= 0 AND coherence_score_micros <= 1000000),
    member_node_ids_json TEXT NOT NULL,
    cluster_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'SUPERSEDED', 'RETRACTED', 'QUARANTINED')),
    rebuild_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, cluster_id)
);

CREATE INDEX IF NOT EXISTS idx_cae_knowledge_cluster_theme
    ON cae.knowledge_cluster (workspace_id, cluster_type, status);

-- 2. Research Signals
CREATE TABLE IF NOT EXISTS cae.research_signal (
    workspace_id TEXT NOT NULL,
    signal_id TEXT NOT NULL,
    cluster_id TEXT NOT NULL,
    topic TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'SUPERSEDED', 'RETRACTED', 'EXPIRED', 'QUARANTINED')),
    temporal_window_start TIMESTAMPTZ NOT NULL,
    temporal_window_end TIMESTAMPTZ NOT NULL,
    velocity_micros INTEGER NOT NULL CHECK (velocity_micros >= 0 AND velocity_micros <= 1000000),
    acceleration_micros INTEGER NOT NULL CHECK (acceleration_micros >= 0 AND acceleration_micros <= 1000000),
    novelty_micros INTEGER NOT NULL CHECK (novelty_micros >= 0 AND novelty_micros <= 1000000),
    divergence_micros INTEGER NOT NULL CHECK (divergence_micros >= 0 AND divergence_micros <= 1000000),
    confidence_micros INTEGER NOT NULL CHECK (confidence_micros >= 0 AND confidence_micros <= 1000000),
    signal_json TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, signal_id)
);

CREATE INDEX IF NOT EXISTS idx_cae_research_signal_cluster
    ON cae.research_signal (workspace_id, cluster_id, status);

CREATE INDEX IF NOT EXISTS idx_cae_research_signal_velocity
    ON cae.research_signal (workspace_id, velocity_micros DESC);

-- 3. Context Projections
CREATE TABLE IF NOT EXISTS cae.context_projection (
    workspace_id TEXT NOT NULL,
    projection_id TEXT NOT NULL,
    signal_id TEXT NOT NULL,
    cluster_id TEXT NOT NULL,
    guest_id TEXT NOT NULL,
    audience_state_id TEXT NOT NULL,
    activation_potential_micros INTEGER NOT NULL CHECK (activation_potential_micros >= 0 AND activation_potential_micros <= 1000000),
    distribution_potential_micros INTEGER NOT NULL CHECK (distribution_potential_micros >= 0 AND distribution_potential_micros <= 1000000),
    evidence_confidence_micros INTEGER NOT NULL CHECK (evidence_confidence_micros >= 0 AND evidence_confidence_micros <= 1000000),
    composite_opportunity_score_micros INTEGER NOT NULL CHECK (composite_opportunity_score_micros >= 0 AND composite_opportunity_score_micros <= 1000000),
    hypothesis_readiness BOOLEAN NOT NULL DEFAULT TRUE,
    projection_json TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, projection_id)
);

CREATE INDEX IF NOT EXISTS idx_cae_context_projection_guest
    ON cae.context_projection (workspace_id, guest_id, composite_opportunity_score_micros DESC);

CREATE INDEX IF NOT EXISTS idx_cae_context_projection_signal
    ON cae.context_projection (workspace_id, signal_id);

-- Enable Row Level Security (RLS) on all tables
ALTER TABLE cae.knowledge_cluster ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.research_signal ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.context_projection ENABLE ROW LEVEL SECURITY;

-- RLS Policies
DROP POLICY IF EXISTS knowledge_cluster_workspace_isolation ON cae.knowledge_cluster;
CREATE POLICY knowledge_cluster_workspace_isolation ON cae.knowledge_cluster
    FOR ALL
    USING (cae.has_workspace_access(workspace_id::text));

DROP POLICY IF EXISTS research_signal_workspace_isolation ON cae.research_signal;
CREATE POLICY research_signal_workspace_isolation ON cae.research_signal
    FOR ALL
    USING (cae.has_workspace_access(workspace_id::text));

DROP POLICY IF EXISTS context_projection_workspace_isolation ON cae.context_projection;
CREATE POLICY context_projection_workspace_isolation ON cae.context_projection
    FOR ALL
    USING (cae.has_workspace_access(workspace_id::text));
