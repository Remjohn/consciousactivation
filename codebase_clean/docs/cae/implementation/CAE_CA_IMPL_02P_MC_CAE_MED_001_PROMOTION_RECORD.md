# CA-IMPL-02P Promotion Record — `MC-CAE-MED-001` → `POSTGRES_AUTHORITATIVE`

**Phase ID:** `CA-IMPL-02P` (operator-authorized completion of CA-IMPL-02 Section 6)
**Document ID:** `CAE_CA_IMPL_02P_MC_CAE_MED_001_PROMOTION_RECORD`
**Status:** `PROMOTED_POSTGRES_AUTHORITATIVE`
**Date:** 2026-08-25
**Executed by:** CAE Governed Execution Agent (ox-alpha / ZCode), on explicit operator instruction
**Environment Class:** `E3_STAGING_SUPABASE_POOLER_PRIVATE_STORAGE`

---

## 1. Operator Decision

The Section 6 question was posed verbatim at the close of CA-IMPL-02:

> **Promote `MC-CAE-MED-001` to `POSTGRES_AUTHORITATIVE` for the approved scope and contract version, retain the documented recovery/legacy boundary, maintain all non-claims, and reject any broader authority interpretation?**

The operator answered: **"Yes do it. PROMOTE."**

This document records the execution of that answer and nothing more. No other aggregate, source, plane, API, or routing surface was touched; no source was retired.

## 2. Pre-Promotion Gates (all passed before the promotion write)

| Gate | Check | Digest / Result |
|---|---|---|
| G1 | Cutover contract checksum unchanged | `03200cea77c9625e…` (exact match) |
| G2 | Committed cutover verifier bytes == canonical-run evidence | `9dcf0858ebad77ab…` (exact match) |
| G3 | Aggregate scope exactly the authorized single aggregate | `MC-CAE-MED-001` |
| G4 | Environment class unchanged since admission | `E3_STAGING_SUPABASE_POOLER_PRIVATE_STORAGE` |
| G5 | Proven recovery route artifact present (`REHEARSED_ALL_PASSED`) | SHA-256 `b835ba2cfc7d9d70…` |

## 3. Promotion Execution (typed path only)

Executor: `scripts/cae/implementation/execute_ca_impl_02p_promotion.py`.

1. Promotion workspace provisioned through `cae.workspace.provision@1.0.0` (RLS-compliant parent row).
2. The authority transition was appended as an **immutable, replay-safe receipt** via `cae.receipt.commit@1.0.0`:

   - **Promotion receipt ID:** `rcpt_cae_receipt_commit_c5af2497e8cb3e4a894bde05`
   - **Outcome:** `COMMITTED`
   - **Transition bound in payload:** `POSTGRES_AUTHORITATIVE_PENDING_OPERATOR_PROMOTION → POSTGRES_AUTHORITATIVE`
   - **Scope boundary encoded in receipt:** `aggregates_in_scope=[MC-CAE-MED-001]`, `aggregates_out_of_scope=ALL_OTHERS_UNCHANGED`, `sources_retired=[]`, `broader_authority_interpretation=REJECTED`
   - **Operator decision token:** `OPERATOR_SECTION6_PROMOTE_APPROVED_2026-08-25`
   - **Links to cutover proof:** evidence id `38630a34-7c68-4896-8bf2-6b4a7b3e2dd8`, cutover receipt `rcpt_cae_receipt_commit_1610201dbaba990e71a6b1b2`, all five gate digests
3. Replay with identical payload returned the identical receipt — no duplicate rows.
4. Fresh read re-derived the canonical command digest and matched the stored `payload_sha256`.
5. Immutability probe: `UPDATE` on the promotion receipt was blocked by trigger `trg_prevent_receipt_mutation`.

## 4. Effective Authority State

```text
MC-CAE-MED-001 (Media Asset & Evidence Lineage)
  authority_state: POSTGRES_AUTHORITATIVE          <- effective as of promotion receipt above
  scope:            approved contract version, E3 staging environment class only
  recovery route:   retained (append-only supersession; no mutable edits)
  sources:          NONE retired; legacy/source plane untouched
```

All other aggregates remain in their prior states per `CAE_AGGREGATE_AUTHORITY_MATRIX.md`. This record does not extend authority to any neighboring aggregate, plane, or environment class.

## 5. Non-Claims Maintained

- Staging-environment proof only — no production-behavior claim.
- Fidelity findings F-01 (single-column FK on lineage links) and F-02 (table-name shadowing) remain open operator-attention items; promotion does not resolve them.
- No client API, orchestration, registry, or production routing behavior is claimed or changed.
- Count parity alone is nowhere relied upon as verification.

## 6. Hygiene

Post-promotion cleanup removed the promotion workspace's transient rows under its own slug marker; final independent probe: **0 workspaces, 0 media assets, 0 engagements, 0 receipts, 0 lineage links, 0 memberships across the entire `cae` schema**, and the phase storage prefix empty. Zero residue.

## 7. Reproduction

```bash
python scripts/cae/implementation/execute_ca_impl_02p_promotion.py
# Idempotent-by-replay; gates G1–G2 will fail closed if contract or cutover-verifier bytes drift.
```

---

**Verdict:** Operator-directed promotion of `MC-CAE-MED-001` to `POSTGRES_AUTHORITATIVE` executed and durably recorded as an immutable receipt. Phase boundary reached; execution stops here.
