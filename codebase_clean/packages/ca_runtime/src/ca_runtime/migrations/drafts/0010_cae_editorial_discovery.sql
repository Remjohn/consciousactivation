-- =============================================================================
-- 0010_cae_editorial_discovery.sql
-- CAE Phase 3 Mandate M35: Evidence → Editorial Discovery with Synthetic-Proof Block
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS cae;

-- 1. Evidence Segments Table (CAE-M05)
CREATE TABLE IF NOT EXISTS cae.evidence_segment (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    segment_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    speaker TEXT NOT NULL,
    start_time_ms BIGINT NOT NULL,
    end_time_ms BIGINT NOT NULL,
    verbatim_text TEXT NOT NULL,
    boundary_type TEXT NOT NULL,
    text_sha256 TEXT NOT NULL,
    context_dependency JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_authenticated BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, segment_id)
);

-- 2. Semantic Annotations Table (CAE-M06)
CREATE TABLE IF NOT EXISTS cae.semantic_annotation (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    annotation_id TEXT NOT NULL,
    segment_id TEXT NOT NULL,
    semantic_role TEXT NOT NULL,
    epistemic_status TEXT NOT NULL,
    confidence_score_bps INTEGER NOT NULL,
    tension_ref TEXT,
    invariant_ref TEXT,
    emotional_register TEXT NOT NULL DEFAULT 'NEUTRAL',
    story_arc_geometry TEXT NOT NULL DEFAULT 'NONE',
    is_candidate_eligible BOOLEAN NOT NULL DEFAULT TRUE,
    is_publishable BOOLEAN NOT NULL DEFAULT FALSE,
    observable_evidence JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, annotation_id)
);

-- 3. Content Candidates Table (CAE-M07)
CREATE TABLE IF NOT EXISTS cae.content_candidate (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    candidate_id TEXT NOT NULL,
    candidate_type TEXT NOT NULL,
    title TEXT NOT NULL,
    hook_statement TEXT NOT NULL,
    narrative_completeness TEXT NOT NULL,
    story_arc TEXT,
    tension_ref TEXT,
    invariant_ref TEXT,
    archetypal_container TEXT,
    evidence_links JSONB NOT NULL DEFAULT '[]'::jsonb,
    cmf_score_bps JSONB NOT NULL DEFAULT '{}'::jsonb,
    production_status TEXT NOT NULL DEFAULT 'DRAFT_CANDIDATE',
    is_synthetic BOOLEAN NOT NULL DEFAULT FALSE,
    standalone_context_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, candidate_id)
);

-- 4. Candidate Clusters Table (CAE-M08)
CREATE TABLE IF NOT EXISTS cae.candidate_cluster (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    cluster_id TEXT NOT NULL,
    theme TEXT NOT NULL,
    candidate_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    redundancy_score_bps INTEGER NOT NULL,
    coverage_domain TEXT NOT NULL,
    dominant_candidate_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, cluster_id)
);

-- 5. Editorial Storyboards Table (CAE-M09)
CREATE TABLE IF NOT EXISTS cae.editorial_storyboard (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    storyboard_id TEXT NOT NULL,
    candidate_id TEXT NOT NULL,
    title TEXT NOT NULL,
    hook_statement TEXT NOT NULL,
    priority_rank INTEGER NOT NULL,
    evidence_links JSONB NOT NULL DEFAULT '[]'::jsonb,
    approved_by TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, storyboard_id)
);

-- 6. Editorial Receipts Table (CA-REC-004)
CREATE TABLE IF NOT EXISTS cae.editorial_receipt (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    receipt_id TEXT NOT NULL,
    operator_id TEXT NOT NULL,
    candidate_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    rationale TEXT NOT NULL,
    taste_delta TEXT,
    is_synthetic_blocked BOOLEAN NOT NULL DEFAULT FALSE,
    metadata_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    receipt_sha256 TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, receipt_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_cae_segment_session ON cae.evidence_segment (workspace_id, session_id);
CREATE INDEX IF NOT EXISTS idx_cae_annotation_segment ON cae.semantic_annotation (workspace_id, segment_id);
CREATE INDEX IF NOT EXISTS idx_cae_candidate_status ON cae.content_candidate (workspace_id, production_status);
CREATE INDEX IF NOT EXISTS idx_cae_cluster_theme ON cae.candidate_cluster (workspace_id, theme);
CREATE INDEX IF NOT EXISTS idx_cae_storyboard_cand ON cae.editorial_storyboard (workspace_id, candidate_id);
CREATE INDEX IF NOT EXISTS idx_cae_receipt_candidate ON cae.editorial_receipt (workspace_id, candidate_id);

-- Row-Level Security (RLS)
ALTER TABLE cae.evidence_segment ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.semantic_annotation ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.content_candidate ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.candidate_cluster ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.editorial_storyboard ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.editorial_receipt ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_evidence_segment_isolation') THEN
        CREATE POLICY cae_evidence_segment_isolation ON cae.evidence_segment
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_semantic_annotation_isolation') THEN
        CREATE POLICY cae_semantic_annotation_isolation ON cae.semantic_annotation
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_content_candidate_isolation') THEN
        CREATE POLICY cae_content_candidate_isolation ON cae.content_candidate
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_candidate_cluster_isolation') THEN
        CREATE POLICY cae_candidate_cluster_isolation ON cae.candidate_cluster
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_editorial_storyboard_isolation') THEN
        CREATE POLICY cae_editorial_storyboard_isolation ON cae.editorial_storyboard
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_editorial_receipt_isolation') THEN
        CREATE POLICY cae_editorial_receipt_isolation ON cae.editorial_receipt
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;
END $$;
