# CAE Phase 18 / CA-TOPO-06: Operator Decision Packet

**Phase ID:** `CA-TOPO-06`  
**Document Class:** `OPERATOR_DECISION_PACKET`  
**Status:** `UNBUNDLED — PENDING OPERATOR SELECTION`  
**Governing Mandate:** `docs/cae/gemini_execution/18_CA_TOPO_06_TABLE_FAMILY_TOPOLOGY_RECONCILIATION_MANDATE.md`  

---

## 1. Executive Summary & Required Operator Choice

The technical investigation under `CA-TOPO-06` confirmed that finding `F-02` arises from a direct conflict between two distinct relational table families:
1. `WP03_TEXT_FAMILY` (legacy string-keyed tables: `cae.workspace`, `cae.project`, `cae.media_asset`, `cae.execution_receipt`).
2. `CA_IMPL_UUID_FAMILY` (modern UUID-keyed tables: `cae.workspace`, `cae.workspace_membership`, `cae.guest_profile`, `cae.engagement`, `cae.media_asset`, `cae.receipt`, `cae.receipt_evidence_link`).

Because `register_verified_interview_source` cannot execute against the CA-IMPL UUID schema, and the typed `verify_media_asset` route was authorized only as a bounded cutover workaround, the operator must now select exactly one canonical topology route to be implemented and proven under `CA-TOPO-07`.

---

## 2. Unbundled Topology Options

### Option A: Adopt CA-IMPL UUID-Keyed Schema as Canonical Target (Recommended)

- **Option Token:** `DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET`
- **Architectural Scope:**
  - Designate `CA_IMPL_UUID_FAMILY` as the single authoritative relational model for CAE.
  - Author forward migration `MIG-0008` to rename/quarantine legacy WP-03 staging tables (`legacy_wp03_*`).
  - Upgrade `interview_source_bridge.py` and `FirstSliceSemanticOperations` into a modern adapter invoking `TenantScopedSemanticOperations.verify_media_asset`.
- **Impact Matrix:**
  - **Authority & Identity:** Preserves UUID tenancy model and `POSTGRES_AUTHORITATIVE_STAGING_ONLY` cutover status for `MC-CAE-MED-001`.
  - **Migration / DDL:** Applies non-destructive rename in staging; zero data loss.
  - **Contracts & Runtime:** Modernizes legacy bridge contracts to output UUID-keyed receipts.
  - **RLS & Receipts:** Retains composite FKs, append-only triggers, and RLS session isolation.
  - **Recovery & Teardown:** Fully verifiable in isolated disposable PostgreSQL environment (`CA-TOPO-07`).

---

### Option B: Retain WP-03 Text-Keyed Schema as Canonical Baseline

- **Option Token:** `DECISION_TOPO_OPTION_B_RETAIN_WP03_TEXT_BASELINE`
- **Architectural Scope:**
  - Designate `WP03_TEXT_FAMILY` as canonical; revert CA-IMPL models and DDL to string keys.
  - Reintroduce `cae.project` table across all tenant packages.
  - Deprecate CA-IMPL UUID composite foreign key and RLS foundation.
- **Impact Matrix:**
  - **Authority & Identity:** Breaks `TS-CAE-TEN-001` specifications and reverts multi-tenancy model.
  - **Migration / DDL:** Requires rewriting DDL migrations `MIG-0001` through `MIG-0007`.
  - **Contracts & Runtime:** Re-enables legacy `register_verified_interview_source` without code changes, but breaks modern tenant operations.
  - **RLS & Receipts:** Reverts to un-enforced text receipts; invalidates F-01 composite FK repair.
  - **Recovery & Teardown:** High regression risk across entire repository test suite.

---

### Option C: Formal Namespaced Dual Coexistence

- **Option Token:** `DECISION_TOPO_OPTION_C_NAMESPACED_DUAL_COEXISTENCE`
- **Architectural Scope:**
  - Maintain both table families concurrently in partitioned PostgreSQL schemas: `cae_legacy` and `cae_v2`.
  - Configure database connection routing based on caller context.
- **Impact Matrix:**
  - **Authority & Identity:** Splits authority across two distinct schema namespaces.
  - **Migration / DDL:** Requires schema relocation migrations in staging.
  - **Contracts & Runtime:** Zero immediate code changes, but requires dual client maintenance.
  - **RLS & Receipts:** RLS isolated to `cae_v2`; `cae_legacy` remains unscoped.
  - **Recovery & Teardown:** Requires dual-schema disposable verification harnesses.

---

## 3. Decision Matrix & Operator Action

| Option | Token | Canonical Target | Tenancy / RLS Compliance | Migration Effort | Operational Risk |
|---|---|---|---|---|---|
| **Option A** | `DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET` | CA-IMPL UUID (`cae.*`) | Complete (`TS-CAE-TEN-001`) | Low (Rename + Adapter) | Low |
| **Option B** | `DECISION_TOPO_OPTION_B_RETAIN_WP03_TEXT_BASELINE` | WP-03 Text (`cae.*`) | Non-compliant | High (Full Refactor) | Critical |
| **Option C** | `DECISION_TOPO_OPTION_C_NAMESPACED_DUAL_COEXISTENCE` | Dual (`cae_legacy` / `cae_v2`) | Partial (Partitioned) | Medium (Schema Splitting) | Medium |

---

## 4. Operator Decision Gate

The operator is requested to select one option to govern `CA-TOPO-07`:

> **Select one CA-TOPO-06 topology option and its named canonical route/identity boundary for the F-02-affected relations, preserve all other options and non-claims as rejected or deferred, and authorize CA-TOPO-07 only to implement and prove that selected topology in a new disposable environment—without moving client data, altering shared staging, or changing operational authority?**
