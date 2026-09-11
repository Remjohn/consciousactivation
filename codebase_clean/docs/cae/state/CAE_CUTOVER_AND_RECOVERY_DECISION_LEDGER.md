# CAE Cutover and Recovery Decision Ledger

**Document ID:** `CAE_CUTOVER_AND_RECOVERY_DECISION_LEDGER`  
**Phase ID:** `CA-STATE-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/08_CA_STATE_01_AGGREGATE_AUTHORITY_MIGRATION_MANDATE.md`  
**Authority References:** `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`, `15_CAE_POSTGRES_STATE_MODEL.md`, `21_CAE_STATE_CONTROL_TEST_AND_PROOF_PROTOCOL.md`  

---

## 1. Executive Cutover Framework & Doctrine

1. **No Inferred Cutover:** No aggregate is cut over merely because a schema exists, a configuration is committed, or a staging test passed. Cutover is a governed operator action requiring a signed decision receipt.
2. **Anti-Self-Attestation Law (`HN-STATE-010`):** An operational receipt cannot self-attest a cutover without an independent external verification record.
3. **Mandatory Rollback Rehearsal (`HN-STATE-008`):** No legacy store may be moved to `LEGACY_READ_ONLY` or `RETIRED` until its deterministic rollback procedure has been rehearsed and verified in staging.
4. **Independent Per-Aggregate Decision:** Every aggregate has its own decision ledger record. Bundling multiple cutovers into an all-or-nothing operation is prohibited.

---

## 2. Per-Aggregate Cutover & Recovery Ledger

### 2.1 `DEC-CUT-WS-001`: Workspace & Actor Boundary
- **Contract:** `MC-CAE-WS-001` (`CA-ENT-001`, `CA-REL-001`)
- **Recommended Disposition:** `MIGRATE`
- **Target Authority State:** `POSTGRES_AUTHORITATIVE` (from `DUAL_VERIFY`)
- **Preconditions for Cutover:**
  1. Multi-tenant RLS schema (`cae.workspace`, `cae.actor`) active in production PostgreSQL.
  2. 100% pass on cross-tenant denial countertests (`HN-STATE-002`).
  3. All operational roles mapped to valid workspace memberships.
- **Cutover Criterion:** Zero RLS bypasses across 1,000 synthetic multi-tenant requests.
- **Deterministic Recovery / Rollback:** If tenant resolution fails, revert API router to local config provider; PostgreSQL remains available for read-only diagnostics without data loss.
- **Operator Decision Status:** `PENDING_OPERATOR_APPROVAL_AT_SECTION_7_GATE`

---

### 2.2 `DEC-CUT-OPR-001`: Operator Access Governance
- **Contract:** `MC-CAE-OPR-001` (`CA-ENT-000`, `CA-POL-001`, `CA-REL-002`)
- **Recommended Disposition:** `MIGRATE`
- **Target Authority State:** `POSTGRES_AUTHORITATIVE` (from `LEGACY_ONLY`)
- **Preconditions for Cutover:**
  1. Operator tables and security definer functions deployed.
  2. Direct backend superuser credentials rotated and placed in dual-custody escrow.
  3. Ephemeral grant TTL and ticket verification automated.
- **Cutover Criterion:** Verification that ungranted operator queries return 0 rows.
- **Deterministic Recovery / Rollback:** In the event of grant subsystem failure, break-glass credentials unlocked via offline multi-party physical key ceremony.
- **Operator Decision Status:** `PENDING_OPERATOR_APPROVAL_AT_SECTION_7_GATE`

---

### 2.3 `DEC-CUT-ENG-001`: Engagement (Campaign Project Envelope)
- **Contract:** `MC-CAE-ENG-001` (`CA-ENT-004`)
- **Recommended Disposition:** `MIGRATE`
- **Target Authority State:** `DUAL_VERIFY -> POSTGRES_AUTHORITATIVE`
- **Preconditions for Cutover:**
  1. Shadow dual-write active between SQLite `CampaignRepository` and PostgreSQL `cae.project`.
  2. Zero-drift parity proof across 100 consecutive campaign orders.
  3. Format 02 campaigns quarantined per `QUAR-ENG-001`.
- **Cutover Criterion:** Automated verification query returns 0 count mismatch and 0 state mismatch.
- **Deterministic Recovery / Rollback:** Revert API router to SQLite `CampaignRepository`; replay missing campaign orders from PostgreSQL `cae.event` log.
- **Operator Decision Status:** `PENDING_OPERATOR_APPROVAL_AT_SECTION_7_GATE`

---

### 2.4 `DEC-CUT-GST-001`: Guest Identity & Locality
- **Contract:** `MC-CAE-GST-001` (`CA-ENT-003`)
- **Recommended Disposition:** `MIGRATE` (Workspace-local only; Cross-workspace link `RETAIN_OUT_OF_SCOPE`)
- **Target Authority State:** `DUAL_VERIFY -> POSTGRES_AUTHORITATIVE`
- **Preconditions for Cutover:**
  1. Workspace-local composite key `(workspace_id, guest_id)` enforced by database constraints.
  2. Cross-workspace identity auto-merging prohibited and verified by `HN-STATE-003` countertest.
  3. `GuestIdentityLink` runtime resolution disabled.
- **Cutover Criterion:** Zero cross-tenant guest ID collisions in staging.
- **Deterministic Recovery / Rollback:** Fall back to reading participant headers from local interview SQLite.
- **Operator Decision Status:** `PENDING_OPERATOR_APPROVAL_AT_SECTION_7_GATE`

---

### 2.5 `DEC-CUT-MED-001`: Media Asset & Evidence Lineage — *FIRST CUTOVER CANDIDATE*
- **Contract:** `MC-CAE-MED-001` (`CA-ENT-002`, `CA-EVI-001`, `CA-REL-004`, `CA-EVI-002`, `CA-REL-003`, `CA-REC-003`)
- **Recommended Disposition:** `MIGRATE` (First Cutover Candidate)
- **Target Authority State:** `POSTGRES_AUTHORITATIVE` (from `DUAL_VERIFY`)
- **Preconditions for Cutover:**
  1. Private Supabase Storage bucket `cae-media` provisioned with strict RLS policies.
  2. `InterviewExpressionSourceBridge` verified with byte-exact SHA-256 readback on all test media (`HN-STATE-007`).
  3. Atomic storage-rollback verified on metadata failure.
- **Cutover Criterion:** 100% byte-for-byte SHA-256 match and continuous causal lineage across all newly ingested media assets.
- **Deterministic Recovery / Rollback:** Legacy media files remain untouched on local disk; failed storage uploads are deleted via `InterviewExpressionSourceBridge.delete_object()`.
- **Operator Decision Status:** `RECOMMENDED_FOR_FIRST_CUTOVER_AUTHORIZATION`

---

### 2.6 `DEC-CUT-RUN-001`: Harness Run Execution State
- **Contract:** `MC-CAE-RUN-001` (`CA-STR-001`, `CA-EXE-001`)
- **Recommended Disposition:** `MIGRATE` (New CAE Runs) / `RETAIN_OUT_OF_SCOPE` (Legacy History & Templates)
- **Target Authority State:** `LEGACY_ONLY -> DUAL_VERIFY`
- **Preconditions for Cutover:**
  1. Pinned template snapshot loaded in `cae.harness_template`.
  2. State machine optimistic concurrency locking verified on `cae.state_aggregate`.
  3. Dual-write drift detection active (`HN-STATE-005`).
- **Cutover Criterion:** 50 multi-step harness executions completed in staging without state divergence.
- **Deterministic Recovery / Rollback:** Pipeline worker rolls back to legacy SQLite runner; in-flight step leases gracefully expire.
- **Operator Decision Status:** `PENDING_OPERATOR_APPROVAL_AT_SECTION_7_GATE`

---

### 2.7 `DEC-CUT-REC-001`: Receipt & Transition Lineage — *FIRST CUTOVER CANDIDATE*
- **Contract:** `MC-CAE-REC-001` (`CA-REC-001`, `CA-REC-002`, `CA-REL-005`, `CA-STA-001`, `CA-STA-002`)
- **Recommended Disposition:** `MIGRATE` (First Cutover Candidate)
- **Target Authority State:** `POSTGRES_AUTHORITATIVE` (from `DUAL_VERIFY`)
- **Preconditions for Cutover:**
  1. `FirstSliceSemanticOperations` deployed to production PostgreSQL.
  2. Cryptographic hash chaining validated across 10,000 consecutive staging operations.
  3. Idempotent command replay verified without duplicate receipt or link emission (`HN-STATE-004`).
- **Cutover Criterion:** Cryptographic audit tool confirms zero broken hash links in `cae.receipt`.
- **Deterministic Recovery / Rollback:** Transactions are atomic; any commit failure triggers immediate SQL `ROLLBACK`.
- **Operator Decision Status:** `RECOMMENDED_FOR_FIRST_CUTOVER_AUTHORIZATION`

---

## 3. Summary of Cutover Recommendations

| Decision ID | Target Aggregate | Recommended Cutover Sequence | Rollback Feasibility | Risk Level | First Cutover Candidate? |
|---|---|---|---|---|---|
| `DEC-CUT-MED-001` | Media Asset & Evidence Lineage | **Sequence 1** (Immediate at Slice Launch) | Immediate / Non-Destructive | Low | **YES (Recommended)** |
| `DEC-CUT-REC-001` | Receipt & Transition Lineage | **Sequence 1** (Immediate at Slice Launch) | Immediate / Transactional | Low | **YES (Recommended)** |
| `DEC-CUT-WS-001` | Workspace & Actor Root | **Sequence 2** (Following Foundation Proof) | Config Fallback | Low | No |
| `DEC-CUT-OPR-001` | Operator Access Governance | **Sequence 2** (Following Foundation Proof) | Escrow Break-Glass | Medium | No |
| `DEC-CUT-ENG-001` | Engagement (Campaign Envelope) | **Sequence 3** (Following Parity Proof) | SQLite Reversion | Medium | No |
| `DEC-CUT-GST-001` | Guest Identity & Locality | **Sequence 3** (Following Parity Proof) | SQLite Reversion | Medium | No |
| `DEC-CUT-RUN-001` | Harness Run Execution State | **Sequence 4** (Future Pipeline Phase) | Worker Reversion | High | No |

---

## 4. Non-Claims and Gate Restraints

1. **Zero Data Movement Guarantee:** No database cutover, data migration, or write redirection has occurred during this authoring phase.
2. **Operator Exclusivity:** Cutover authorization is the exclusive prerogative of the operator at the Section 7 Gate.
