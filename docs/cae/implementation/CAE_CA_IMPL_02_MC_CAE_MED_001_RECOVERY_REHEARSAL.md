# CA-IMPL-02 Recovery Rehearsal — `MC-CAE-MED-001`

**Phase ID:** `CA-IMPL-02`
**Document ID:** `CAE_CA_IMPL_02_MC_CAE_MED_001_RECOVERY_REHEARSAL`
**Status:** `REHEARSED_ALL_PASSED`
**Date:** 2026-08-25
**Contract basis:** `CA-STATE-01_MEDIA_ASSET_AUTHORITY_MIGRATION_CONTRACT.md` §6 recovery routes;
`TS-CAE-TEN-001_RISK_AND_ROLLBACK_REGISTER.md` procedures RB-01/RB-02/RB-03.

---

## 1. Why Rehearse Before Promotion

The mandate blocks cutover without a proven recovery route. Every failure path below was executed for real against the
staging topology — not simulated — and each ended in a verified-safe state before the next stage was allowed to run.

## 2. Rehearsed Recovery Routes

### 2.1 Compensation on Failed Registration (RSK-TEN-002/006)

A media registration was deliberately made fail **after** its storage object existed (hash mismatch → typed op raises
`UnverifiedMediaDigestError` after quarantining). The compensation routine then:

1. deleted the orphaned private-storage object,
2. verified deletion by a fresh read expecting 404.

Result: `[PASS] compensation rehearsal: registration failure -> orphan object deleted (True)`.

### 2.2 Forced Transaction Rollback (Atomicity of Cutover Writes)

An intentional mid-flight failure inside an explicit `conn.transaction(force_rollback=True)` block containing receipt
append + projection writes. Post-abort assertions: zero new receipt rows, zero new projection rows, zero lineage links.

Result: `[PASS] forced rollback rehearsal: zero receipt/projection residue after abort`.
This proves the append-only trigger does not trap partial writes: aborted transactions leave no receipt fragments behind.

### 2.3 Divergence Detection & Safe Restoration

An expectation digest was tampered, guaranteeing expected≠observed. The reconciler flagged
`FIELD_MISMATCH:canonical_sha256`; the independent fresh-read of actual bytes re-derived truth and cleared the divergence.
This is the operational answer to "target drifts from expectation post-cutover": fresh-read wins, never the claim
(`HN-STATE-007` byte-readback law; `QUAR-MED-001`).

Result: `[PASS] divergence detection: tampered expectation flagged; independent fresh-read restores safe state`.

### 2.4 Source Preservation (Nothing Deleted)

All admitted source fixtures (both workspaces' intake audio plus the CT-05 mutated stale source) were re-hashed after all
rehearsals and compared to admission checksums — unchanged. Sources are never retired or deleted by this phase; only the
phase's own transient copies under `staging-ca-impl-02/` were pruned at cleanup.

Result: `[PASS] source preservation: admitted source fixtures intact with unchanged checksums (nothing deleted)`.

## 3. Deterministic Rollbacks Available Post-Promotion

| Route | Trigger | Procedure | Proven by |
|---|---|---|---|
| Transition-record neutralization | operator rejects promotion | append a superseding receipt recording rejection (receipts are immutable; no UPDATE exists) | CT-07 immutability + Stage 3 replay semantics |
| Schema teardown | fatal schema defect | RB-01 (`DROP SCHEMA cae CASCADE` after connection termination) — out of phase scope, documented escape hatch | foundation acceptance |
| Storage pruning | orphaned objects | bounded sweep used pre-run and at Stage 7, strictly scoped to `staging-ca-impl-02/` + `ws-med-alpha-%`/`ws-med-beta-%` slugs | Stage 7 zero-residue PASS |
| Control-state reset | governance reversal | revert `CAE_IMPLEMENTATION_CONTROL_STATE.md` entry per RB-03 | this phase's control-state update |

## 4. Residual Risk After Recovery Proof

- R-1: The pending-transition record itself cannot be edited or removed (immutability); correction is forward-only via a
  superseding receipt. Accepted: matches the append-only authority model.
- R-2: Fidelity finding F-01 (single-column FK on lineage links) means a raw-SQL forged link would require the parity-sweep
  repair demonstrated in CT-06 rather than being schema-rejected. Composite-FK hardening is deferred to a separately
  approved migration.

## 5. Closure

All four rehearsals passed on the canonical run; cleanup verified zero transient rows and zero reachable storage objects.
Recovery readiness for `MC-CAE-MED-001` is therefore evidenced, satisfying the mandate gate that blocked promotion absent a
proven recovery route.
