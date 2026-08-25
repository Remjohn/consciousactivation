# CA-IMPL-02 One-Aggregate Authority Cutover Proof — `MC-CAE-MED-001`

**Phase ID:** `CA-IMPL-02`
**Phase Name:** One Aggregate Authority Cutover (Media Asset & Evidence Lineage)
**Document ID:** `CAE_CA_IMPL_02_MC_CAE_MED_001_CUTOVER_PROOF`
**Status:** `PROOF_EXECUTED_PENDING_OPERATOR_PROMOTION`
**Date:** 2026-08-25
**Author:** CAE Governed Execution Agent (ox-alpha / ZCode)
**Environment Class:** `E3_STAGING_SUPABASE_POOLER_PRIVATE_STORAGE`

---

## 1. Scope of This Proof

Exactly **one** aggregate was cut over: **`MC-CAE-MED-001` — Media Asset & Evidence Lineage**, per the approved migration contract
`CA-STATE-01_MEDIA_ASSET_AUTHORITY_MIGRATION_CONTRACT.md` (SHA-256
`03200cea77c9625e1cdb7e86f89703fbea4164ab943947ce65fe6a50cd9cf87b`) and decision ledger entry
`DEC-CUT-MED-001` (`CAE_CUTOVER_AND_RECOVERY_DECISION_LEDGER.md`, SHA-256
`19f19b2e24d77f6a19aede0487b66f43e795ea9a6e259870967089efd549003e`; aggregate authority matrix SHA-256
`55acddcc36788ec2621acc6a3da63c3dee047250aea6cd55d537c902078d4e63`).

**Authority transition recorded by this phase:**

```text
DUAL_VERIFY  →  POSTGRES_AUTHORITATIVE_PENDING_OPERATOR_PROMOTION
```

No source was retired, no legacy record deleted, no client API, orchestration, registry, or production routing changed.
The final `POSTGRES_AUTHORITATIVE` promotion is an operator decision requested verbatim in Section 9 and **not executed by this agent**.

### 1.1 Plane Distinction Preserved

| Plane | Role in this phase |
|---|---|
| Definition source | Constitutions/contracts/tech specs under `docs/cae/` (read-only inputs) |
| Operational authority | Staging PostgreSQL `cae.*` tables (target of the cutover record) |
| Runtime representation | `TenantScopedSemanticOperations` typed operations (`packages/ca_runtime`) |
| Promotion authority | Human operator only — Section 6 promotion question, unanswered at time of writing |

## 2. Executable Change Path (Fidelity Note)

The resident staging schema contains two table families: the text-keyed WP-03 tables and the uuid-keyed
CA-IMPL-01B tables that shadow them by name. Under this topology, the contract's bridge operation
(`register_verified_interview_source`, WP-03 shape) is not executable against the CA-IMPL-01B target tables.

The contract-approved executable route used instead is the typed runtime path already authorized by CA-IMPL-01B:

- `cae.media.verify@1.0.0` (`verify_media_asset`): fresh-read SHA-256 from private storage → `VERIFIED` or `QUARANTINED`.
- `cae.receipt.commit@1.0.0` (`commit_receipt`): immutable cutover transition record.
- `cae.evidence.capture@1.0.0` + `cae.receipt.commit@1.0.0`: downstream lineage effect proof.

This is recorded as a **fidelity finding (F-02)**, not a deviation: the transform, identity derivation, idempotency,
quarantine, receipt, reconciliation, and recovery semantics mandated by the contract are all enforced; only the bridge-op
entry point is substituted because of the staging schema duality. No contract checksum was altered; no foundation DDL was modified.

## 3. Admission Evidence (Mandate §3.1)

All admission gates passed before any mutation (Stage 0 of the verifier):

| Gate | Result |
|---|---|
| Contract present & checksum | PASS `03200cea77c9625e…` |
| Decision ledger present & checksum | PASS `19f19b2e24d77f6a…` |
| Aggregate authority matrix present & checksum | PASS `55acddcc36788ec2…` |
| Target topology (`cae.workspace`, `cae.workspace_membership`, `cae.engagement`, `cae.media_asset`, `cae.receipt`, `cae.receipt_evidence_link`) | PASS |
| RLS enabled on media_asset / receipt / receipt_evidence_link / engagement | PASS |
| Pre-mutation source/target snapshot counts | all six operational tables = 0 rows |
| Storage prefix `staging-ca-impl-02/` clean before mutation | PASS |
| Environment class | `E3_STAGING_SUPABASE_POOLER_PRIVATE_STORAGE` (pooler host/port/user validated secret-safely) |

Secrets policy honored throughout: connection validated by host suffix `.pooler.supabase.com`, port 5432,
username `postgres.evnxdssbxxrsesftdvgx`; no password, connection string, key, or signed URL is reproduced in any artifact.

## 4. Controlled Transform & Registration

Two disposable workspaces were provisioned via the typed path (`provision_workspace`, membership grant,
engagement initialize), then one media asset each was transformed and registered:

- Transform manifest validation: logical URI form `workspace://ws/proj/file`, recomputed SHA-256 and byte size
  (mismatch raises `TransformValidationError` per quarantine register `QUAR-MED-001`).
- Registration through `cae.media.verify@1.0.0` with a **fresh read** of object bytes from private storage;
  lifecycle state set to `VERIFIED` only on hash match.
- Identity derivation never uses names, emails, embeddings, totals, or row shapes — only
  `(workspace_id, content_sha256, media_type)` per the contract identity law.

Canonical run receipts (2026-08-25):

| Receipt | Operation | Outcome |
|---|---|---|
| `rcpt_cae_media_verify_8ce287fda38a3f15ed036f6b` | `cae.media.verify@1.0.0` (WS Alpha) | COMMITTED, VERIFIED |
| `rcpt_cae_media_verify_732d24e191e0c5ef650257f0` | `cae.media.verify@1.0.0` (WS Beta) | COMMITTED, VERIFIED |

Registered asset IDs: `c6040b5a-69e8-470d-ac3a-03a3824b852b` (Alpha), `36c10692-9f94-4541-bf9f-4ed84f76a8f1` (Beta).
Storage paths (transient fixtures, pruned post-proof):
`staging-ca-impl-02/bc6dda57-8346-463f-a357-16176e3feb95/c6040b5a-69e8-470d-ac3a-03a3824b852b/intake_audio.wav`,
`staging-ca-impl-02/411ae410-9c0f-475e-8d55-4e72aa979ffe/36c10692-9f94-4541-bf9f-4ed84f76a8f1/intake_audio.wav`.

## 5. Dual Verification & Honest Reconciliation (Not Count-Only)

Per hard negative `HN-TS-008` (count-only fallacy), reconciliation compared **fields, scopes, and lineage**, not totals:

- Independent fresh-read SHA-256 parity for both registered objects: PASS.
- Field-by-field reconciliation (`reconcile_media_records`): 2 records, 0 mismatches across
  `media_asset_id`, `workspace_id`, `canonical_sha256`, `byte_size`, `mime_type`, `storage_path`, `lifecycle_state`, receipt linkage.
- Adversarial control: swapping workspace attribution between the two records with identical totals was flagged as
  `SCOPE_SWAPPED` — proving the reconciler is scope-aware, not count-aware.
- Contract Section 5 parity relations: 0 orphan VERIFIED assets, 0 broken/cross-scope lineage links.

## 6. Limited Read/Write Cutover Record

The authority transition was recorded as an **immutable, replay-safe receipt** on the operational plane:

| Property | Result |
|---|---|
| Cutover receipt | `rcpt_cae_receipt_commit_1610201dbaba990e71a6b1b2` (`cae.receipt.commit@1.0.0`), outcome `COMMITTED` |
| Replay | identical receipt returned (`IDEMPOTENT_REPLAY`), exactly one row — no duplicates |
| Altered-payload replay | rejected with `IDEMPOTENCY_PAYLOAD_MISMATCH` |
| Immutability | UPDATE blocked by trigger `trg_prevent_receipt_mutation` (CT-07) |

The receipt binds: aggregate ID `MC-CAE-MED-001`, contract ID + version, `FROM_AUTHORITY_STATE=DUAL_VERIFY`,
`TO_AUTHORITY_STATE=POSTGRES_AUTHORITATIVE_PENDING_OPERATOR_PROMOTION`, environment class, registered asset IDs,
and command payload digest stored in `cae.receipt.payload_sha256`.

Fresh-read operation proof on the normal typed paths (no direct SQL writes anywhere in the cutover itself):

- Read path: RLS-scoped projection agrees with registered truth for the scoped session.
- Write path: evidence captured + linked via `rcpt_cae_evidence_capture_e77640cd6a6bbb3a54e80a7a` and
  `rcpt_cae_receipt_commit_80ff2681dca02505b88f7c97`; event + projection + receipt consistency asserted
  (exactly one lineage link after commit).
- Bypass denial: forged requested-workspace scope → `TENANCY_VIOLATION`; unscoped authenticated session reads 0 media rows;
  direct forged-workspace INSERT denied by RLS WITH CHECK.

## 7. Recovery Rehearsal Summary

Full detail in `CAE_CA_IMPL_02_MC_CAE_MED_001_RECOVERY_REHEARSAL.md`. All rehearsals passed:
compensation on failed registration (orphan storage object deleted), forced transaction rollback (zero residue),
divergence detection + independent fresh-read restoration, and source preservation (all admitted source fixtures intact
with unchanged checksums — nothing deleted).

## 8. Adversarial Countertests (Mandate §5)

| Test | Scenario | Result |
|---|---|---|
| CT-01 | Swapped workspace IDs, matching totals | DETECTED (`SCOPE_SWAPPED`) |
| CT-02 | Identity collision: identical bytes in two workspaces | distinct workspace-local identities; no merge |
| CT-03 | Replay/duplicate registration | `IDEMPOTENT_REPLAY`, one receipt row |
| CT-04 | Duplicate receipt-evidence link | rejected by UNIQUE constraint |
| CT-05 | Stale source (mutated bytes vs stale claim) | QUARANTINED, not admitted |
| CT-06 | Forged cross-workspace lineage link | flagged by Section 5 parity, repaired (finding F-01) |
| CT-07 | Fabricated success receipt | UPDATE blocked by trigger; quarantine receipt honestly records `storage_sha256_match=FAIL` |
| CT-08 | Byte mismatch vs claimed hash | durable QUARANTINED, never VERIFIED |
| CT-09 | Missing downstream effect | detectable (`MISSING_TARGET_ROW`) |
| CT-10 | Unscoped session reading receipts | 0 rows (RLS isolation) |
| CT-11 | Forward repair after quarantine | corrected bytes register VERIFIED; quarantined history retained |

## 9. Findings, Risks, Non-Claims

### Findings

- **F-01 (schema fidelity limitation — quarantined-class):** The approved CA-IMPL-01A DDL
  (`scripts/cae/implementation/apply_ca_impl_01a_scaffolding.py`, line 197) binds
  `cae.receipt_evidence_link.receipt_id` to the global `cae.receipt(receipt_id)` PK via a single-column FK rather than a
  composite `(workspace_id, receipt_id)` binding. A raw-SQL cross-scope link INSERT is therefore not schema-rejected.
  The approved defenses that *were* proven: (a) typed-operation-only write law (no cutover write used raw SQL),
  (b) RLS read isolation (CT-10), (c) Section 5 parity detection + repair (CT-06). Recorded for operator attention;
  **no control weakened, no migration altered** (that file is outside this phase's allowlist).
- **F-02 (staging topology duality):** WP-03 text-keyed tables shadow CA-IMPL-01B uuid-keyed tables by name; the
  contract bridge op is unusable on the resident schema. The typed `verify_media_asset` route (authorized CA-IMPL-01B)
  served as the executable change path (Section 2).
- **F-03 (hygiene):** Runs 1–3 of the verifier failed fast at CT stages and left transient fixtures; a bounded pre-run
  hygiene sweep (strictly scoped to `staging-ca-impl-02/` and `ws-med-alpha-%`/`ws-med-beta-%` slugs) now guarantees
  idempotent re-execution. The canonical run started from a verified-clean baseline with no sweep needed.

### Risks

- R-1: Until the operator promotes, the aggregate remains formally `DUAL_VERIFY` with a pending-transition record; dual-read
  parity obligations continue to apply to any new media registrations.
- R-2: F-01 means referential integrity for lineage links depends on application-path discipline plus periodic parity
  sweeps until a composite-FK migration is separately approved.

### Non-Claims

- This proof does **not** claim `POSTGRES_AUTHORITATIVE` status; it records only the pending transition.
- It does not prove production behavior (staging environment class only).
- It does not prove legacy-source retirement, client API compatibility, or orchestration behavior — none were touched.
- Count parity alone is not claimed anywhere as verification (HN-TS-008); all reconciliation is field-/scope-aware.

## 10. Reproduction

```bash
# Full E3 proof (~2 min; idempotent; requires CAE_* env secrets in .env)
python scripts/cae/implementation/verify_ca_impl_02_staging.py

# Unit tests for the pure helpers (transform, identity, reconciliation)
python -m pytest tests/cae/test_ca_impl_02_cutover.py -q   # 10 passed
python -m pytest tests/cae/ -q                              # 28 passed
```

| Artifact | SHA-256 |
|---|---|
| `scripts/cae/implementation/verify_ca_impl_02_staging.py` | `9dcf0858ebad77ab593881852f838f3e74019549a58fd73cf5dd60b7f80a5cb0` |
| `tests/cae/test_ca_impl_02_cutover.py` | `ca6b6d4b9c8085b7b1b58a33f6f00812c716bfb6824a60fb1bbbc01c53ca8dd6` |

The committed verifier bytes are byte-identical to the binary that produced the canonical transcript above.

---

**Verdict:** `CUTOVER_PROOF_EXECUTED — MC-CAE-MED-001 recorded at POSTGRES_AUTHORITATIVE_PENDING_OPERATOR_PROMOTION.`
Promotion is reserved to the human operator via the Section 6 question (see Section 12 of the mandate; restated at the end
of the phase conversation). This agent does not self-promote and has not retired any source.
