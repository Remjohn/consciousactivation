# CAE Aggregate Authority & Migration Contract: Workspace

**Contract ID:** `MC-CAE-WS-001`  
**Aggregate ID:** `CA-ENT-001` (`Workspace`) & `CA-REL-001` (`WorkspaceMembership`)  
**Phase ID:** `CA-STATE-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/08_CA_STATE_01_AGGREGATE_AUTHORITY_MIGRATION_MANDATE.md`  
**Constitutional Owner:** `docs/cae/constitutions/CA-CAN-01A_CONSTITUTION.md`  
**Functional Requirement:** `FR-CAE-TEN-001`, `FR-CAE-TEN-003`, `FR-CAE-TEN-006`  

```yaml
contract_metadata:
  contract_id: "MC-CAE-WS-001"
  aggregate_name: "Workspace"
  single_aggregate_verified: true
  primary_class: "Entity"
  plane: "OPERATIONAL_PLANE"
  recommended_disposition: "MIGRATE"
  current_authority_state: "DUAL_VERIFY"
  zero_data_movement_guaranteed: true
  execution_action_permitted: false
  recovery_procedure_defined: true
  contract_status: "CONTRACT_RATIFIED_SPEC_ONLY"
```

---

## 1. Authority Axes Deconstruction

| Authority Axis | Specification & Provenance | Evidence Reference |
|---|---|---|
| **Canonical Definition Source** | `PRD-CAE-TEN-001` §3.1; `CA-CAN-01A_CONSTITUTION.md` §2. Defines Workspace as the sole multi-tenant root partition boundary. | `[DOCUMENT]` `PRD-CAE-TEN-001_TENANT_GUEST_OPERATIONAL_SLICE.md` |
| **Current Operational Authority** | Design documentation and staging tables (`cae.workspace`, `cae.actor`) in `docs/cae/implementation/sql/0001_cae_foundation_draft.sql:14-36`. Legacy brownfield was single-tenant without multi-tenant tables. | `[SCHEMA]` `sql/0001_cae_foundation_draft.sql` |
| **Target Runtime Representation** | PostgreSQL 17.6 relational table `cae.workspace` with RLS security functions (`has_workspace_access()`) and `cae.actor` / `cae.workspace_membership` with unique `(workspace_id, actor_id)`. | `[SCHEMA]` `sql/0002_cae_workspace_rls.sql:62` |
| **Change & Promotion Authority** | CAE Platform Administrator for workspace provisioning; Workspace Administrator for internal actor membership grants. | `[DOCUMENT]` `CAE_SCOPE_AND_AUTHORITY_MATRIX.md:31` |

---

## 2. Source Scope, Identity Mapping & Parent Chain

### Scope & Parent Chain
- **Legal Parent Chain:** Root Operational Tenant Boundary (No parent entity; `workspace_id` is the universal containment root).
- **Subordinate Aggregates:** `Actor` (`CA-ENT-005`), `Engagement` (`CA-ENT-004`), `Guest` (`CA-ENT-003`), `MediaAsset` (`CA-ENT-002`), `HarnessRun` (`CA-EXE-001`), `Receipt` (`CA-REC-001`).

### Identity Mapping Rules
- **Source Identifier:** Brownfield configuration strings (e.g. `workspace_id = "default"` or project directory names).
- **Target Identifier:** Cryptographically unique deterministic slug `ws-[a-z0-9_-]+` or UUIDv4 `workspace_id`.
- **Membership Identifier:** Composite tuple `(workspace_id, actor_id)` mapping external identity provider subjects (`external_subject`) to workspace-local actor records.
- **Anti-"Same Name" Law:** Having the same display name or tenant label does NOT prove identity. Workspaces must be created through explicit provisioning commands with verified cryptographic receipts.

---

## 3. Five-Stage Authority Progression Model

```text
+-------------------+       +-------------------+       +---------------------------+       +---------------------+       +-------------+
| 1. LEGACY_ONLY    |  -->  | 2. DUAL_VERIFY    |  -->  | 3. POSTGRES_AUTHORITATIVE |  -->  | 4. LEGACY_READ_ONLY |  -->  | 5. RETIRED  |
+-------------------+       +-------------------+       +---------------------------+       +---------------------+       +-------------+
```

### Stage 1: `LEGACY_ONLY`
- **Entry Criteria:** Single-tenant configuration active in brownfield SQLite services (`services/interview`, `services/pipeline`).
- **Read Path:** Configuration files (`.env`, config YAMLs).
- **Write Path:** Direct filesystem/config editing.
- **Receipt Requirement:** None (Legacy baseline).
- **Exit Criteria:** Staging schema `cae.workspace` and `cae.actor` provisioned; RLS allow/deny test suite passes.

### Stage 2: `DUAL_VERIFY` (Current Staging State)
- **Entry Criteria:** Foundation DDL applied to staging PostgreSQL; RLS policies active (`CAE_WP02A_FOUNDATION_PROOF.md`).
- **Read Path:** Applications continue reading local config; shadow verification queries execute against `cae.workspace`.
- **Write Path:** Workspace creation executed in staging PostgreSQL via typed operations; shadow validation asserts tenant isolation.
- **Receipt Requirement:** Staging verification receipts with zero RLS cross-tenant leakage.
- **Exit Criteria:** 100% pass on negative cross-tenant access countertests; operator gate approval.

### Stage 3: `POSTGRES_AUTHORITATIVE`
- **Entry Criteria:** Formal operator gate promotion (`CA-IMPL-02`).
- **Read Path:** All API routers and services resolve tenant context strictly through `cae.workspace` and `has_workspace_access()`.
- **Write Path:** Provisioning and membership mutations execute exclusively via typed semantic operations (`create_workspace`, `grant_membership`).
- **Receipt Requirement:** Immutable transition receipts for all provisioning events.
- **Exit Criteria:** 30 consecutive days of zero RLS leakage incidents.

### Stage 4: `LEGACY_READ_ONLY`
- **Entry Criteria:** Legacy config files frozen as read-only audit references.
- **Read Path:** PostgreSQL authoritative; legacy config available for historical audit only.
- **Write Path:** Legacy configs locked; PostgreSQL writes only.
- **Receipt Requirement:** Hash-signed snapshot of legacy configuration.
- **Exit Criteria:** Retention audit completed.

### Stage 5: `RETIRED`
- **Entry Criteria:** Legacy single-tenant configuration fully decommissioned.
- **Read Path / Write Path:** PostgreSQL 100% exclusive.
- **Receipt Requirement:** Final decommission receipt.

---

## 4. Transform, Loss & Idempotency Rules

### Transformation Rules
1. `workspace_id`: String trimmed, validated against `^[a-z0-9][a-z0-9_-]{2,63}$`.
2. `name`: Non-empty human-readable workspace name.
3. `status`: Set to `ACTIVE` upon initial provisioning.
4. `created_at`: Stored as immutable RFC3339 UTC timestamp.

### Loss Policy
- Zero data loss permitted. If legacy environment lacked tenant partitioning, default workspace `ws-default` is provisioned with complete audit lineage.

### Idempotency & Concurrency
- `create_workspace` requires unique `idempotency_key` per workspace.
- Replaying identical parameters returns the existing `Workspace` receipt (`idempotent_replay: true`).
- Replaying with conflicting parameters raises `SemanticOperationConflict`.

---

## 5. Automated Reconciliation & Parity Verification

```sql
-- Parity Query: Verify that every operational record belongs to a registered workspace
SELECT 'orphan_actors' AS check_name, count(*) AS failure_count
FROM cae.actor a LEFT JOIN cae.workspace w ON a.workspace_id = w.workspace_id
WHERE w.workspace_id IS NULL
UNION ALL
SELECT 'orphan_projects', count(*)
FROM cae.project p LEFT JOIN cae.workspace w ON p.workspace_id = w.workspace_id
WHERE w.workspace_id IS NULL;
```

---

## 6. Validation Failures, Quarantine & Recovery

| Failure Class | Trigger Condition | Automated Recovery / Quarantine Route |
|---|---|---|
| `TENANT_NOT_FOUND` | Command issued with non-existent `workspace_id` | Operation rejected with `SemanticOperationError`; transaction rolled back. |
| `RLS_ACCESS_DENIED` | Actor attempts access without active membership | RLS filter returns 0 rows; security audit event emitted to `cae.event`. |
| `MEMBERSHIP_CONFLICT` | Attempt to add duplicate actor membership | Idempotent replay if identical; `SemanticOperationConflict` if role differs. |

### Deterministic Emergency Rollback
If PostgreSQL RLS fails during `DUAL_VERIFY`, the API service immediately reverts tenant resolution to the local config fallback without data loss.

---

## 7. Test Fidelity & Negative Countertests

- **Required Fidelity:** `E3_STAGING_PERSISTENCE` (PostgreSQL 17.6 + Supavisor pooler + RLS security definer functions).
- **Hard Negative Countertest (`HN-STATE-002`):**
  - Attempt: Actor belonging to `workspace_alpha` executes `SELECT * FROM cae.media_asset WHERE workspace_id = 'workspace_beta'`.
  - Expected Verdict: Zero rows returned; forced bypass attempt raises SQL permission error.
  - Verification: Proven in `scripts/cae/verify_foundation_structure.py` and `CAE_WP02A_FOUNDATION_PROOF.md`.

---

## 8. Operator Decision & Gate Promotion

```yaml
operator_gate_decision:
  gate: "CA-STATE-01 -> CA-TS-01"
  required_action: "Approve MC-CAE-WS-001 Workspace Authority Contract"
  cutover_permitted_now: false
  authorizing_next_phase_only: "CA-TS-01"
```
