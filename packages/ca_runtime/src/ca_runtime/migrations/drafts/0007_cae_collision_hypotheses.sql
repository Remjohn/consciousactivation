-- =============================================================================
-- 0007_cae_collision_hypotheses.sql
-- CAE Phase 3 Mandate M32: Audience x Guest Resonance + Matrix of Edging + Collision Hypothesis
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS cae;

-- 1. Matrix of Edging Table
CREATE TABLE IF NOT EXISTS cae.matrix_of_edging (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    matrix_id TEXT NOT NULL,
    broad_signal TEXT NOT NULL,
    hidden_pressure TEXT NOT NULL,
    surviving_edge TEXT NOT NULL,
    identity_gap TEXT NOT NULL,
    audience_reality TEXT NOT NULL,
    desired_recognition TEXT NOT NULL,
    smallest_useful_movement TEXT NOT NULL,
    counteractivation_risks JSONB NOT NULL DEFAULT '[]'::jsonb,
    source_refs JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, matrix_id)
);

-- 2. Collision Hypothesis Table
CREATE TABLE IF NOT EXISTS cae.collision_hypothesis (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    hypothesis_id TEXT NOT NULL,
    title TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    audience_id TEXT NOT NULL,
    audience_tension_ref TEXT NOT NULL,
    guest_id TEXT NOT NULL,
    guest_lived_proof_citation TEXT NOT NULL,
    research_signal_id TEXT NOT NULL,
    sda_invariant TEXT NOT NULL DEFAULT 'SDA-INV-001_ACTIVE_TENSION',
    oblique_lens JSONB,
    bridge_statement TEXT NOT NULL,
    evidence_references JSONB NOT NULL DEFAULT '[]'::jsonb,
    novelty_assessment JSONB NOT NULL,
    falsification_condition JSONB NOT NULL,
    heritage_eval JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'PENDING',
    approval_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, hypothesis_id)
);

-- 3. Collision Hypothesis Portfolio Table
CREATE TABLE IF NOT EXISTS cae.collision_hypothesis_portfolio (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    portfolio_id TEXT NOT NULL,
    candidate_hypothesis_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    diversity_signature JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'DRAFT',
    selected_hypothesis_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, portfolio_id)
);

-- 4. Hypothesis Evaluation Receipt Table
CREATE TABLE IF NOT EXISTS cae.hypothesis_evaluation_receipt (
    workspace_id UUID NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    receipt_id TEXT NOT NULL,
    portfolio_id TEXT NOT NULL,
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
CREATE INDEX IF NOT EXISTS idx_cae_collision_hypothesis_rel ON cae.collision_hypothesis (workspace_id, relation_type);
CREATE INDEX IF NOT EXISTS idx_cae_collision_hypothesis_status ON cae.collision_hypothesis (workspace_id, status);
CREATE INDEX IF NOT EXISTS idx_cae_collision_hypothesis_guest ON cae.collision_hypothesis (workspace_id, guest_id);
CREATE INDEX IF NOT EXISTS idx_cae_collision_hypothesis_audience ON cae.collision_hypothesis (workspace_id, audience_id);
CREATE INDEX IF NOT EXISTS idx_cae_collision_portfolio_status ON cae.collision_hypothesis_portfolio (workspace_id, status);

-- Row-Level Security (RLS)
ALTER TABLE cae.matrix_of_edging ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.collision_hypothesis ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.collision_hypothesis_portfolio ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.hypothesis_evaluation_receipt ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_matrix_of_edging_isolation') THEN
        CREATE POLICY cae_matrix_of_edging_isolation ON cae.matrix_of_edging
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_collision_hypothesis_isolation') THEN
        CREATE POLICY cae_collision_hypothesis_isolation ON cae.collision_hypothesis
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_collision_portfolio_isolation') THEN
        CREATE POLICY cae_collision_portfolio_isolation ON cae.collision_hypothesis_portfolio
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'cae_hypothesis_receipt_isolation') THEN
        CREATE POLICY cae_hypothesis_receipt_isolation ON cae.hypothesis_evaluation_receipt
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;
END $$;
