# CAE Next-Aggregate Candidate Register — Phase 22 / CA-ACCEPT-10

**Status:** `REGISTERED_FOR_OPERATOR_DECISION`  
**Phase ID:** `CA-ACCEPT-10`  
**Date:** `2026-08-26T05:25:00Z`  
**Governing Mandate:** `docs/cae/gemini_execution/22_CA_ACCEPT_10_INDEPENDENT_ACCEPTANCE_AND_NEXT_AGGREGATE_MANDATE.md`

---

## 1. Candidate Qualification Rules

In accordance with Mandate 22 Section 3, exactly three candidates are qualified below from accepted `CA-STATE-01` contracts. The agent does NOT select, implement, or create an implementation plan for any candidate. Selection belongs exclusively to the operator.

---

## 2. Qualified Candidates Register (Maximum 3)

### Candidate 1: `MC-CAE-ENG-001` (Engagement & Project Context)
- **Contract & Specification:** `CTR-CAE-ENG-001` / `TS-CAE-TEN-001` Section 3.
- **Reason for Candidacy:** Direct structural parent of `MC-CAE-MED-001` in the canonical tenancy hierarchy. DDL table `cae.engagement` is already deployed in shared staging with composite primary key `(workspace_id, engagement_id)`.
- **Source / Target Authority:** Current: `SQLITE_AUTHORITATIVE` $\to$ Target: `POSTGRES_AUTHORITATIVE_STAGING_ONLY`.
- **Data Classification:** `EMPTY_OR_SYNTHETIC_ONLY` (Zero client data access).
- **Legal Parent Chain:** `cae.workspace` $\to$ `cae.engagement`.
- **Dependencies:** `MC-CAE-WS-001` (Workspace tenancy context).
- **Migration & Route Implications:** Requires binding typed runtime operations for engagement lifecycle and project token mapping.
- **E3 Prerequisites:** Disposable Postgres E3 replay with multi-tenant isolation countertests.
- **Recovery & Rollback:** PITR staging snapshot and compensating draft route.
- **Unproven Risks:** Alignment with legacy campaign router parameters (Finding F-03).
- **Operator Decision Required:** Explicit operator mandate authorizing `CA-ENG-01` scoping and evidence planning only.

---

### Candidate 2: `MC-CAE-GST-001` (Guest Profile & Subject Directory)
- **Contract & Specification:** `CTR-CAE-GST-001` / `TS-CAE-TEN-001` Section 4.
- **Reason for Candidacy:** Leaf aggregate with clean workspace-scoped tenancy and zero complex foreign-key dependencies. DDL table `cae.guest_profile` is already deployed in shared staging with composite primary key `(workspace_id, guest_id)`.
- **Source / Target Authority:** Current: `SQLITE_AUTHORITATIVE` $\to$ Target: `POSTGRES_AUTHORITATIVE_STAGING_ONLY`.
- **Data Classification:** `EMPTY_OR_SYNTHETIC_ONLY` (Synthetic guest records only).
- **Legal Parent Chain:** `cae.workspace` $\to$ `cae.guest_profile`.
- **Dependencies:** `MC-CAE-WS-001` (Workspace tenancy context).
- **Migration & Route Implications:** Typed CRUD operations for guest directory and consent state.
- **E3 Prerequisites:** Isolation countertests ensuring cross-workspace guest privacy under RLS.
- **Recovery & Rollback:** Point-in-time recovery snapshot and table purge procedures.
- **Unproven Risks:** Brownfield SQLite guest record schema alignment during future cutover.
- **Operator Decision Required:** Explicit operator mandate authorizing `CA-GST-01` scoping and evidence planning only.

---

### Candidate 3: `MC-CAE-EVN-001` (Evaluation Run & Audit Evidence)
- **Contract & Specification:** `CTR-CAE-EVN-001` / `TS-CAE-EVID-001` Section 7.
- **Reason for Candidacy:** Direct consumer of the proven immutable execution receipt ledger (`cae.receipt`) and composite FK evidence links (`cae.receipt_evidence_link`).
- **Source / Target Authority:** Current: `SQLITE_AUTHORITATIVE` $\to$ Target: `POSTGRES_AUTHORITATIVE_STAGING_ONLY`.
- **Data Classification:** `EMPTY_OR_SYNTHETIC_ONLY` (Synthetic evaluation runs only).
- **Legal Parent Chain:** `cae.workspace` $\to$ `cae.engagement` $\to$ `cae.evaluation_run`.
- **Dependencies:** `MC-CAE-WS-001`, `MC-CAE-ENG-001`, `MC-CAE-MED-001`.
- **Migration & Route Implications:** Binding evaluation harness results to canonical receipts.
- **E3 Prerequisites:** Proof of tamper-evident append-only evaluation receipts in E3 replay.
- **Recovery & Rollback:** Standard staging snapshot and forward repair route.
- **Unproven Risks:** Requires upstream engagement lifecycle completion.
- **Operator Decision Required:** Explicit operator mandate authorizing `CA-EVN-01` scoping and evidence planning only.

---

## 3. Disqualified Aggregates Register

The following aggregates are explicitly disqualified from immediate candidacy:
- **`MC-CAE-CMP-001` (Campaign Router):** Disqualified due to open finding F-03 (FastAPI bypass of typed runtime operations).
- **`MC-CAE-SFL-001` / `MC-CAE-PRM-001` (Registries):** Disqualified due to open finding F-05 (quarantined registry defects).
- **All Production Promotion Candidates:** Disqualified due to absolute prohibition on production promotion.
