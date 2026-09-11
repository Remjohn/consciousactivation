# CAE Aggregate Authority & Migration Contract: Operator Access Governance

**Contract ID:** `MC-CAE-OPR-001`  
**Aggregate ID:** `CA-ENT-000` (`OperatorOrganization`), `CA-POL-001` (`OperatorAccessPolicy`), `CA-REL-002` (`OperatorAccessGrant`)  
**Phase ID:** `CA-STATE-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/08_CA_STATE_01_AGGREGATE_AUTHORITY_MIGRATION_MANDATE.md`  
**Constitutional Owner:** `docs/cae/constitutions/CA-CAN-01A_CONSTITUTION.md`  
**Functional Requirement:** `FR-CAE-TEN-002`, `FR-CAE-TEN-004`, `FR-CAE-TEN-005`  

```yaml
contract_metadata:
  contract_id: "MC-CAE-OPR-001"
  aggregate_name: "OperatorAccessGovernance"
  single_aggregate_verified: true
  primary_class: "Entity / Policy / Relation"
  plane: "OPERATIONAL_PLANE"
  recommended_disposition: "MIGRATE"
  current_authority_state: "LEGACY_ONLY"
  zero_data_movement_guaranteed: true
  execution_action_permitted: false
  recovery_procedure_defined: true
  contract_status: "CONTRACT_RATIFIED_SPEC_ONLY"
```

---

## 1. Authority Axes Deconstruction

| Authority Axis | Specification & Provenance | Evidence Reference |
|---|---|---|
| **Canonical Definition Source** | `PRD-CAE-TEN-001` §3.2; `CA-CAN-01A_CONSTITUTION.md` §3; Bundle v3 `08_CAE_IMPLEMENTATION_GATE.md`. Defines platform governance, access policies, and audited ephemeral grants. | `[DOCUMENT]` `PRD-CAE-TEN-001_TENANT_GUEST_OPERATIONAL_SLICE.md` |
| **Current Operational Authority** | Design documentation only; absent from brownfield SQLite DDL. Platform operators previously had unrestricted backend root access. | `[DOCUMENT]` `CAE_SCOPE_AND_AUTHORITY_MATRIX.md:30, 33-34` |
| **Target Runtime Representation** | PostgreSQL relational tables: `cae.operator_organization`, `cae.operator_access_policy`, `cae.operator_access_grant` (with mandatory `expires_at`, `ticket_id`, and `reason`). | `[SCHEMA]` Future PostgreSQL foundation schema |
| **Change & Promotion Authority** | CAE Platform Security Officer & Compliance Committee via dual-custody governance. | `[DOCUMENT]` `CAE_SCOPE_AND_AUTHORITY_MATRIX.md:33-34` |

---

## 2. Source Scope, Identity Mapping & Parent Chain

### Scope & Parent Chain
- **Legal Parent Chain:** Root Operational Governance Boundary (`operator_org_id` -> `OperatorOrganization`).
- **Subordinate Relational Chain:** `OperatorAccessPolicy` (`policy_id`) -> `OperatorAccessGrant` (`grant_id`, scoped to `workspace_id` x `operator_actor_id`).

### Identity Mapping Rules
- **Operator Identity:** Global actor identifier `opr-[a-z0-9_-]+` bound to `OperatorOrganization`.
- **Grant Identity:** Ephemeral cryptographic token `oag-[a-z0-9_-]+` with strict time bounding (max 4 hours duration).
- **Anti-Bypass Law:** No standing operator bypass is permitted. An operator role attempting to read tenant data without an active, non-expired `OperatorAccessGrant` matching the target `workspace_id` MUST be blocked by RLS.

---

## 3. Five-Stage Authority Progression Model

### Stage 1: `LEGACY_ONLY` (Current State)
- **Entry Criteria:** Legacy unconstrained operator access active in developer environments.
- **Read Path:** Direct database / storage access credentials.
- **Write Path:** Direct SQL / filesystem mutation.
- **Receipt Requirement:** None.
- **Exit Criteria:** Operator governance DDL authored; RLS bypass-prevention policy validated in staging.

### Stage 2: `DUAL_VERIFY`
- **Entry Criteria:** Operator tables created in staging PostgreSQL; security definer functions active.
- **Read Path:** Operators must request grants in staging; audit log captures all attempted access.
- **Write Path:** Grant issuance via typed operation `request_operator_grant`.
- **Receipt Requirement:** Ephemeral grant issuance receipt with reason, ticket ID, and expiration timestamp.
- **Exit Criteria:** 100% verification of automated grant expiration and RLS enforcement.

### Stage 3: `POSTGRES_AUTHORITATIVE`
- **Entry Criteria:** Formal operator gate promotion (`CA-IMPL-02`). Direct superuser access disabled.
- **Read Path:** All platform maintenance operations execute under audited, time-bounded grants.
- **Write Path:** Grants issued exclusively through typed semantic operations with dual-authorization receipts.
- **Receipt Requirement:** Append-only audit logs in `cae.event` and `cae.receipt`.
- **Exit Criteria:** Zero unauthenticated operator queries across audit window.

### Stage 4: `LEGACY_READ_ONLY`
- **Entry Criteria:** Legacy administrative credentials revoked.
- **Read Path:** Governed PostgreSQL grants only.
- **Write Path:** No legacy admin paths exist.
- **Receipt Requirement:** Credential revocation audit receipt.
- **Exit Criteria:** Audit period complete.

### Stage 5: `RETIRED`
- **Entry Criteria:** Legacy unconstrained access fully decommissioned.
- **Read Path / Write Path:** Governed PostgreSQL model exclusive.
- **Receipt Requirement:** Governance closure receipt.

---

## 4. Transform, Loss & Idempotency Rules

### Transformation Rules
1. `operator_org_id`: String validated against `^org-[a-z0-9_-]+$`.
2. `policy_id`: String validated against `^pol-[a-z0-9_-]+$`.
3. `grant_id`: Deterministic hash `deterministic_id("oag", {operator_actor_id, workspace_id, ticket_id, granted_at})`.
4. `duration_minutes`: Integer clamped between 15 and 240 (max 4 hours).

### Loss Policy
- Zero data loss. Historical platform administration logs are archived as read-only audit records.

### Idempotency & Concurrency
- `request_operator_grant` is idempotent based on `(operator_actor_id, workspace_id, ticket_id)`. Re-requesting within active grant window returns existing grant with remaining TTL.

---

## 5. Automated Reconciliation & Parity Verification

```sql
-- Audit Query: Verify that zero operator reads occurred without a valid active grant
SELECT count(*) AS unauthorized_operator_queries
FROM cae.event e
WHERE e.event_type = 'OperatorDataAccess'
  AND NOT EXISTS (
    SELECT 1 FROM cae.operator_access_grant g
    WHERE g.operator_actor_id = e.actor_id
      AND g.workspace_id = e.workspace_id
      AND e.occurred_at_utc BETWEEN g.granted_at_utc AND g.expires_at_utc
  );
```

---

## 6. Validation Failures, Quarantine & Recovery

| Failure Class | Trigger Condition | Automated Recovery / Quarantine Route |
|---|---|---|
| `GRANT_EXPIRED` | Operator attempts read with expired grant timestamp | RLS denies read immediately; security warning event emitted. |
| `INVALID_TICKET` | Grant requested without verified ticket/reason | Grant request rejected with `SemanticOperationError`. |
| `CROSS_TENANT_BREACH_ATTEMPT` | Operator attempts cross-workspace read without matching grant | Query aborted; high-severity incident logged to `cae.event`. |

### Deterministic Emergency Rollback
Emergency operational break-glass credentials remain in hardware security custody, requiring multi-party offline quorum to activate.

---

## 7. Test Fidelity & Negative Countertests

- **Required Fidelity:** `E3_STAGING_PERSISTENCE` (PostgreSQL RLS with Supavisor pooler).
- **Hard Negative Countertest (`HN-STATE-006`):**
  - Attempt: Operator actor `opr-admin-1` attempts `SELECT * FROM cae.interview_session WHERE workspace_id = 'ws-client-9'` without an active grant.
  - Expected Verdict: Zero rows returned; access logged as denied.
  - Verification: Enforced by RLS security policy and verified in `verify_wp02a_foundation.py`.

---

## 8. Operator Decision & Gate Promotion

```yaml
operator_gate_decision:
  gate: "CA-STATE-01 -> CA-TS-01"
  required_action: "Approve MC-CAE-OPR-001 Operator Access Authority Contract"
  cutover_permitted_now: false
  authorizing_next_phase_only: "CA-TS-01"
```
