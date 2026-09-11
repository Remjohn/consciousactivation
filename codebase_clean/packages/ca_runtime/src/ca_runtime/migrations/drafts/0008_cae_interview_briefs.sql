-- =============================================================================
-- 0008_cae_interview_briefs.sql
-- CAE Phase 3 Mandate M33: Interview Semantic Program + Existing Composer Boundary
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS cae;

-- 1. Activative Interview Briefs Table
CREATE TABLE IF NOT EXISTS cae.interview_brief (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    brief_id TEXT NOT NULL,
    hypothesis_id TEXT NOT NULL,
    guest_name TEXT NOT NULL,
    research_package_ref JSONB NOT NULL,
    brand_context_ref JSONB,
    voice_dna_ref JSONB,
    tension_hypothesis TEXT NOT NULL,
    matrix_of_edging_seed JSONB NOT NULL,
    planned_questions JSONB NOT NULL DEFAULT '[]'::jsonb,
    expression_targets JSONB NOT NULL DEFAULT '[]'::jsonb,
    composer_authority JSONB NOT NULL,
    canonical_sha256 TEXT NOT NULL,
    lifecycle_state TEXT NOT NULL DEFAULT 'SEALED',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, brief_id)
);

-- 2. Interview Sessions Table
CREATE TABLE IF NOT EXISTS cae.interview_session (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    session_id TEXT NOT NULL,
    brief_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'INITIALIZED',
    turns_count INTEGER NOT NULL DEFAULT 0,
    evidence_package_ref JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, session_id)
);

-- 3. Interview Semantic Receipts Table
CREATE TABLE IF NOT EXISTS cae.interview_semantic_receipt (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    receipt_id TEXT NOT NULL,
    brief_id TEXT NOT NULL,
    hypothesis_id TEXT NOT NULL,
    evaluator_lane TEXT NOT NULL,
    decision TEXT NOT NULL,
    score_breakdown_micros JSONB NOT NULL DEFAULT '{}'::jsonb,
    gate_checks JSONB NOT NULL DEFAULT '[]'::jsonb,
    signature TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, receipt_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_cae_interview_brief_hyp ON cae.interview_brief (workspace_id, hypothesis_id);
CREATE INDEX IF NOT EXISTS idx_cae_interview_brief_state ON cae.interview_brief (workspace_id, lifecycle_state);
CREATE INDEX IF NOT EXISTS idx_cae_interview_session_brief ON cae.interview_session (workspace_id, brief_id);
CREATE INDEX IF NOT EXISTS idx_cae_interview_session_status ON cae.interview_session (workspace_id, status);
CREATE INDEX IF NOT EXISTS idx_cae_interview_receipt_brief ON cae.interview_semantic_receipt (workspace_id, brief_id);

-- Row-Level Security (RLS)
ALTER TABLE cae.interview_brief ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.interview_session ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.interview_semantic_receipt ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_interview_brief_isolation') THEN
        CREATE POLICY cae_interview_brief_isolation ON cae.interview_brief
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_interview_session_isolation') THEN
        CREATE POLICY cae_interview_session_isolation ON cae.interview_session
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_interview_receipt_isolation') THEN
        CREATE POLICY cae_interview_receipt_isolation ON cae.interview_semantic_receipt
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;
END $$;
