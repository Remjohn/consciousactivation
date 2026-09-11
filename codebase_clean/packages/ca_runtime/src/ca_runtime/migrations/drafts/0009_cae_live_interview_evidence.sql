-- =============================================================================
-- 0009_cae_live_interview_evidence.sql
-- CAE Phase 3 Mandate M34: Live Interview Activation + Authenticated Evidence
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS cae;

-- 1. Interview Turns Table (CA-EVT-003)
CREATE TABLE IF NOT EXISTS cae.interview_turn (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    turn_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    turn_index INTEGER NOT NULL,
    speaker TEXT NOT NULL,
    question_id TEXT NOT NULL,
    stage TEXT NOT NULL,
    prompt_text TEXT NOT NULL,
    transcript_text TEXT NOT NULL,
    transcript_sha256 TEXT NOT NULL,
    is_authenticated BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, turn_id)
);

-- 2. Interview Semantic Observations Table (CAE-M07)
CREATE TABLE IF NOT EXISTS cae.interview_observation (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    observation_id TEXT NOT NULL,
    turn_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    statement_text TEXT NOT NULL,
    evidence_mode TEXT NOT NULL,
    temporal_orientation TEXT NOT NULL,
    information_completeness TEXT NOT NULL,
    specificity_micros BIGINT NOT NULL,
    authenticity_micros BIGINT NOT NULL,
    is_authenticated BOOLEAN NOT NULL DEFAULT FALSE,
    discrepancy_refs JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, observation_id)
);

-- 3. Authenticated Evidence Packages Table (CAE-M09)
CREATE TABLE IF NOT EXISTS cae.interview_evidence_package (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    package_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    brief_id TEXT NOT NULL,
    guest_id TEXT NOT NULL,
    canonical_sha256 TEXT NOT NULL,
    accepted_evidence_records JSONB NOT NULL DEFAULT '[]'::jsonb,
    downstream_candidates JSONB NOT NULL DEFAULT '[]'::jsonb,
    is_authenticated BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, package_id)
);

-- 4. Evidence Authentications Table (CA-REC-003)
CREATE TABLE IF NOT EXISTS cae.evidence_authentication (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    auth_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    evidence_package_id TEXT NOT NULL,
    evaluator_lane TEXT NOT NULL,
    evaluator_actor_id TEXT NOT NULL,
    verdict TEXT NOT NULL,
    rationale TEXT NOT NULL,
    signature TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, auth_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_cae_turn_session ON cae.interview_turn (workspace_id, session_id);
CREATE INDEX IF NOT EXISTS idx_cae_turn_index ON cae.interview_turn (workspace_id, session_id, turn_index);
CREATE INDEX IF NOT EXISTS idx_cae_observation_turn ON cae.interview_observation (workspace_id, turn_id);
CREATE INDEX IF NOT EXISTS idx_cae_observation_session ON cae.interview_observation (workspace_id, session_id);
CREATE INDEX IF NOT EXISTS idx_cae_evidence_package_session ON cae.interview_evidence_package (workspace_id, session_id);
CREATE INDEX IF NOT EXISTS idx_cae_evidence_package_brief ON cae.interview_evidence_package (workspace_id, brief_id);
CREATE INDEX IF NOT EXISTS idx_cae_evidence_auth_session ON cae.evidence_authentication (workspace_id, session_id);

-- Row-Level Security (RLS)
ALTER TABLE cae.interview_turn ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.interview_observation ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.interview_evidence_package ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.evidence_authentication ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_interview_turn_isolation') THEN
        CREATE POLICY cae_interview_turn_isolation ON cae.interview_turn
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_interview_observation_isolation') THEN
        CREATE POLICY cae_interview_observation_isolation ON cae.interview_observation
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_interview_evidence_package_isolation') THEN
        CREATE POLICY cae_interview_evidence_package_isolation ON cae.interview_evidence_package
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_evidence_authentication_isolation') THEN
        CREATE POLICY cae_evidence_authentication_isolation ON cae.evidence_authentication
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;
END $$;
