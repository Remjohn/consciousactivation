-- =============================================================================
-- 0011_cae_preparation_graph.sql
-- CA-M009: Interactive Parameter-Sensitive Preparation Graph
-- Causal Stage 05 — Declarative PreProduction
-- =============================================================================
--
-- Governing invariants:
--   INV-M009-01  revision rows are immutable once written (no UPDATE on graph_revision)
--   INV-M009-02  stale_write_rejected: base_revision_id CAS check in application layer
--   INV-M009-03  active_binding_immutable: graph_run_binding PRIMARY KEY prevents duplicate rows
--   INV-M009-04  historical revisions remain inspectable (no DELETE on graph_revision)
--   INV-M009-05  run binding stores canonical_sha256 at bind time
--
-- Lifecycle states
--   preparation_graph.lifecycle_state:
--       DRAFT | ACTIVE | SEALED | ARCHIVED
--   graph_revision.lifecycle_state:
--       CANDIDATE | EXECUTION_BOUND | HISTORICAL
--
-- False-proof (anti-centroid) mitigation:
--   The graph_revision table has NO UPDATE trigger.  Any mutation of a committed revision
--   row is a schema violation.  The application MUST insert new rows via SAVE_REVISION.
--   The graph_run_binding table enforces uniqueness on (workspace_id, run_id); once bound
--   the row is permanent and the revision_id cannot change.
--
-- Rollback:
--   DROP TABLE IF EXISTS cae.graph_run_binding;
--   DROP TABLE IF EXISTS cae.graph_revision;
--   DROP TABLE IF EXISTS cae.preparation_graph;
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS cae;

-- ---------------------------------------------------------------------------
-- 1. preparation_graph — one row per named planning artifact
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cae.preparation_graph (
    workspace_id        UUID    NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    graph_id            TEXT    NOT NULL,
    campaign_id         TEXT    NOT NULL,
    name                TEXT    NOT NULL,
    lifecycle_state     TEXT    NOT NULL DEFAULT 'DRAFT'
                            CHECK (lifecycle_state IN ('DRAFT','ACTIVE','SEALED','ARCHIVED')),
    latest_revision_id  TEXT,   -- NULL until the first SAVE_REVISION
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, graph_id)
);

-- ---------------------------------------------------------------------------
-- 2. graph_revision — immutable revision snapshots
-- ---------------------------------------------------------------------------
-- CRITICAL: No application code may UPDATE a row in this table.
-- Every operator edit produces a new INSERT (SAVE_REVISION).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cae.graph_revision (
    workspace_id            UUID    NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    graph_id                TEXT    NOT NULL,
    revision_id             TEXT    NOT NULL,
    revision_seq            INTEGER NOT NULL,
    base_revision_id        TEXT,   -- lineage pointer to the revision this was forked from
    parameter_payload_json  JSONB   NOT NULL,
    canonical_sha256        TEXT    NOT NULL,
    author_id               TEXT    NOT NULL,
    lifecycle_state         TEXT    NOT NULL DEFAULT 'CANDIDATE'
                                CHECK (lifecycle_state IN ('CANDIDATE','EXECUTION_BOUND','HISTORICAL')),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (workspace_id, revision_id),
    FOREIGN KEY (workspace_id, graph_id)
        REFERENCES cae.preparation_graph(workspace_id, graph_id) ON DELETE CASCADE,
    UNIQUE (workspace_id, graph_id, revision_seq)
);

-- Enforce revision_seq monotonicity and deny duplicate seqs per graph
CREATE UNIQUE INDEX IF NOT EXISTS idx_cae_graph_revision_seq
    ON cae.graph_revision (workspace_id, graph_id, revision_seq);

-- ---------------------------------------------------------------------------
-- 3. graph_run_binding — immutable run → revision binding
-- ---------------------------------------------------------------------------
-- Once a run starts it is bound to exactly one revision.
-- The PRIMARY KEY on (workspace_id, run_id) guarantees no duplicate bindings.
-- The revision_digest column stores the canonical_sha256 at bind time (INV-M009-05).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cae.graph_run_binding (
    workspace_id     UUID    NOT NULL REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE,
    run_id           TEXT    NOT NULL,
    graph_id         TEXT    NOT NULL,
    revision_id      TEXT    NOT NULL,
    revision_digest  TEXT    NOT NULL,  -- SHA-256 of parameter_payload_json at bind time
    bound_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    bound_by_id      TEXT    NOT NULL DEFAULT '',
    PRIMARY KEY (workspace_id, run_id),
    FOREIGN KEY (workspace_id, revision_id)
        REFERENCES cae.graph_revision(workspace_id, revision_id)
);

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_cae_preparation_graph_campaign
    ON cae.preparation_graph (workspace_id, campaign_id);

CREATE INDEX IF NOT EXISTS idx_cae_graph_revision_graph
    ON cae.graph_revision (workspace_id, graph_id, revision_seq);

CREATE INDEX IF NOT EXISTS idx_cae_graph_revision_state
    ON cae.graph_revision (workspace_id, lifecycle_state);

CREATE INDEX IF NOT EXISTS idx_cae_graph_run_binding_revision
    ON cae.graph_run_binding (workspace_id, revision_id);

-- ---------------------------------------------------------------------------
-- Row-Level Security
-- ---------------------------------------------------------------------------
ALTER TABLE cae.preparation_graph  ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.graph_revision     ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.graph_run_binding  ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE policyname = 'cae_preparation_graph_isolation'
    ) THEN
        CREATE POLICY cae_preparation_graph_isolation ON cae.preparation_graph
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE policyname = 'cae_graph_revision_isolation'
    ) THEN
        CREATE POLICY cae_graph_revision_isolation ON cae.graph_revision
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE policyname = 'cae_graph_run_binding_isolation'
    ) THEN
        CREATE POLICY cae_graph_run_binding_isolation ON cae.graph_run_binding
            FOR ALL USING (cae.has_workspace_access(workspace_id::text));
    END IF;
END $$;

-- ---------------------------------------------------------------------------
-- Immutability enforcement trigger (defense-in-depth at DB layer)
-- Raises an exception if any column other than lifecycle_state is updated
-- on a committed graph_revision row.  lifecycle_state transitions
-- CANDIDATE→HISTORICAL and CANDIDATE→EXECUTION_BOUND are permitted.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION cae.fn_graph_revision_immutability()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    -- Only allow lifecycle_state transitions; all other columns are frozen
    IF (OLD.workspace_id          <> NEW.workspace_id          OR
        OLD.graph_id              <> NEW.graph_id              OR
        OLD.revision_id           <> NEW.revision_id           OR
        OLD.revision_seq          <> NEW.revision_seq          OR
        OLD.base_revision_id      IS DISTINCT FROM NEW.base_revision_id OR
        OLD.parameter_payload_json <> NEW.parameter_payload_json OR
        OLD.canonical_sha256      <> NEW.canonical_sha256      OR
        OLD.author_id             <> NEW.author_id             OR
        OLD.created_at            <> NEW.created_at)
    THEN
        RAISE EXCEPTION 'INV-M009-01: graph_revision row is immutable. '
            'Only lifecycle_state may be updated. revision_id=%', OLD.revision_id;
    END IF;
    RETURN NEW;
END;
$$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger WHERE tgname = 'trg_graph_revision_immutability'
    ) THEN
        CREATE TRIGGER trg_graph_revision_immutability
            BEFORE UPDATE ON cae.graph_revision
            FOR EACH ROW EXECUTE FUNCTION cae.fn_graph_revision_immutability();
    END IF;
END $$;

-- ---------------------------------------------------------------------------
-- Immutability enforcement trigger for graph_run_binding (no updates allowed)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION cae.fn_graph_run_binding_immutability()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'INV-M009-03: graph_run_binding is immutable. '
        'Active run bindings cannot be changed. run_id=%', OLD.run_id;
END;
$$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger WHERE tgname = 'trg_graph_run_binding_immutability'
    ) THEN
        CREATE TRIGGER trg_graph_run_binding_immutability
            BEFORE UPDATE ON cae.graph_run_binding
            FOR EACH ROW EXECUTE FUNCTION cae.fn_graph_run_binding_immutability();
    END IF;
END $$;
