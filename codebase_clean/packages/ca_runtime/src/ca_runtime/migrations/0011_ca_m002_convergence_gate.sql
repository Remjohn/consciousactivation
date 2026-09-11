-- Migration: 0011_ca_m002_convergence_gate.sql
-- Mandate:    CA-M002 / FR-CONV-001 — Dual-Context Convergence Gate
-- Authority:  Master 57-Question Canon Q02 → Architecture.md §10-11 → this mandate
--
-- Adds the convergence_receipts table that persists the result of every
-- ConvergenceGate.evaluate() call. This table is an operator-inspectable
-- projection; it does NOT make authority decisions. The gate itself
-- (ca_runtime.convergence_gate.ConvergenceGate) is authoritative.
--
-- Rollback: DROP TABLE IF EXISTS convergence_receipts;
--           DROP INDEX IF EXISTS idx_convergence_workspace;
--           DROP INDEX IF EXISTS idx_convergence_digest;

PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------------------
-- 1. Convergence Receipts
--    One row per successful (CONVERGED) or attempted gate evaluation.
--    The convergence_digest column provides a deterministic, unique key
--    for the exact (guest_genesis_revision_id, audience_tensions_revision_id)
--    pairing, preventing duplicate convergence receipt for the same pair.
-- -----------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS convergence_receipts (
    receipt_id                      TEXT PRIMARY KEY,
    workspace_id                    TEXT NOT NULL,
    status                          TEXT NOT NULL CHECK (status IN ('CONVERGED', 'BLOCKED', 'STALE', 'UNKNOWN')),

    -- Guest Genesis Semantic Territory binding
    guest_genesis_territory_id      TEXT NOT NULL,
    guest_genesis_revision_id       TEXT NOT NULL,
    guest_genesis_sha256            TEXT NOT NULL CHECK (length(guest_genesis_sha256) = 64),

    -- Audience Tensions binding
    audience_tensions_audience_id   TEXT NOT NULL,
    audience_tensions_revision_id   TEXT NOT NULL,
    audience_tensions_sha256        TEXT NOT NULL CHECK (length(audience_tensions_sha256) = 64),

    -- Convergence relation
    convergence_digest              TEXT NOT NULL,
    convergence_signature           TEXT NOT NULL,
    converged_at                    TEXT NOT NULL,
    gate_version                    TEXT NOT NULL DEFAULT '1.0.0',
    created_at                      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

-- Primary operator-facing query: most recent receipt per workspace
CREATE INDEX IF NOT EXISTS idx_convergence_workspace
    ON convergence_receipts(workspace_id, converged_at DESC);

-- Uniqueness guard on the convergence_digest so the same upstream pair
-- cannot produce two different receipts (content-addressed deduplication)
CREATE UNIQUE INDEX IF NOT EXISTS idx_convergence_digest
    ON convergence_receipts(convergence_digest);

-- -----------------------------------------------------------------------
-- 2. Register migration
-- -----------------------------------------------------------------------

INSERT OR IGNORE INTO schema_migrations(version, name, applied_at_utc)
VALUES (11, '0011_ca_m002_convergence_gate', strftime('%Y-%m-%dT%H:%M:%SZ', 'now'));
