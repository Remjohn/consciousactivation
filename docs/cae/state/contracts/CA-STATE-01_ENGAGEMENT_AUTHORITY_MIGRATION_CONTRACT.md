# CAE Aggregate Authority & Migration Contract: Engagement

**Contract ID:** `MC-CAE-ENG-001`  
**Aggregate ID:** `CA-ENT-004` (`Engagement` / Campaign Project Envelope)  
**Phase ID:** `CA-STATE-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/08_CA_STATE_01_AGGREGATE_AUTHORITY_MIGRATION_MANDATE.md`  
**Constitutional Owner:** `docs/cae/constitutions/CA-CAN-01A_CONSTITUTION.md`  
**Functional Requirement:** `FR-CAE-TEN-003`, `FR-CAE-TEN-006`  

```yaml
contract_metadata:
  contract_id: "MC-CAE-ENG-001"
  aggregate_name: "Engagement"
  single_aggregate_verified: true
  primary_class: "Entity"
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
| **Canonical Definition Source** | `PRD-CAE-TEN-001` §3.3; `CA-CAN-01A_CONSTITUTION.md` §4; `api/domain/campaign.py`. Defines Engagement as the scoped operational container for creative missions. | `[DOCUMENT]` `PRD-CAE-TEN-001_TENANT_GUEST_OPERATIONAL_SLICE.md` |
| **Current Operational Authority** | SQLite database `campaign_orders` and `campaign_states` tables in `api/services/campaign_repository.py:21-39`. | `[EXECUTABLE]` `api/services/campaign_repository.py` |
| **Target Runtime Representation** | PostgreSQL relational table `cae.project` / `cae.engagement` with composite constraint `(workspace_id, project_id)` and optimistic versioning. | `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:20-26` |
| **Change & Promotion Authority** | Workspace Principal / Engagement Lead via typed operations (`create_engagement`, `update_engagement_state`). | `[DOCUMENT]` `CAE_SCOPE_AND_AUTHORITY_MATRIX.md:35` |

---

## 2. Source Scope, Identity Mapping & Parent Chain

### Scope & Parent Chain
- **Legal Parent Chain:** `Workspace` (`workspace_id`) -> `Engagement` (`project_id` / `engagement_id`).
- **Subordinate Aggregates:** `InterviewSession` (`CA-SES-001`), `HarnessRun` (`CA-EXE-001`), `MediaAsset` (`CA-ENT-002`).

### Identity Mapping Rules
- **Source Identifier:** `order_id` / `campaign_id` in SQLite `campaign_orders` (`campaign-order:<sha24>`).
- **Target Identifier:** `project_id` / `engagement_id` in `cae.project` preserving deterministic derivation `deterministic_id("project", {workspace_id, order_core})`.
- **Legacy Lineage:** Target record preserves `legacy_order_id`, `legacy_campaign_id`, and source payload hash in `cae.legacy_import_record`.
- **Anti-"Same Name" Law:** Campaign title equality across workspaces does NOT authorize identity merging. Every engagement is strictly partitioned by `workspace_id`.

---

## 3. Five-Stage Authority Progression Model

### Stage 1: `LEGACY_ONLY` (Current State)
- **Entry Criteria:** `api/services/campaign_repository.py` SQLite database is live operational authority.
- **Read Path:** `api/routers/campaigns.py` reads from local SQLite `CampaignRepository`.
- **Write Path:** FastAPI endpoints write to local SQLite via `CampaignRepository.create()` and `.update_state()`.
- **Receipt Requirement:** Command results in SQLite `campaign_command_results`.
- **Exit Criteria:** Foundation schema active in PostgreSQL; shadow import extractor validated.

### Stage 2: `DUAL_VERIFY`
- **Entry Criteria:** Shadow writer replicates campaign orders to `cae.project` with force-rollback comparison.
- **Read Path:** API continues serving reads from SQLite; shadow telemetry compares PostgreSQL output.
- **Write Path:** Dual-write adapter writes to SQLite (authoritative) and staging PostgreSQL (shadow).
- **Receipt Requirement:** Shadow parity verification receipts; zero field mismatches across 100 consecutive campaign orders.
- **Exit Criteria:** Zero unresolved differences; rollback drill verified; operator gate approval.

### Stage 3: `POSTGRES_AUTHORITATIVE`
- **Entry Criteria:** Formal operator gate promotion (`CA-IMPL-02`).
- **Read Path:** API reads exclusively from `cae.project` via `has_workspace_access()`.
- **Write Path:** Campaign lifecycle mutations execute exclusively via typed semantic operations against PostgreSQL.
- **Receipt Requirement:** Append-only transition receipts in `cae.receipt`.
- **Exit Criteria:** 14 consecutive days of zero state divergence.

### Stage 4: `LEGACY_READ_ONLY`
- **Entry Criteria:** SQLite database switched to read-only mode (`PRAGMA query_only = ON`).
- **Read Path:** PostgreSQL authoritative; SQLite database retained for forensic audit.
- **Write Path:** PostgreSQL exclusive; SQLite writes prohibited.
- **Receipt Requirement:** Final SQLite database snapshot SHA-256 signed.
- **Exit Criteria:** Retention period satisfied.

### Stage 5: `RETIRED`
- **Entry Criteria:** SQLite archive moved to cold storage.
- **Read Path / Write Path:** PostgreSQL exclusive.
- **Receipt Requirement:** Archival completion receipt.

---

## 4. Transform, Loss & Idempotency Rules

### Transformation Rules
1. `workspace_id`: Exact string match to parent Workspace.
2. `project_id`: Derived from source `project_id` or `deterministic_id("project", order_payload)`.
3. `name`: Preserved from source `objective` / title.
4. `lifecycle_state`: Direct mapping from `campaign_states.lifecycle_state` (`DRAFT`, `LAUNCHED`, `RUNNING`, `AWAITING_REVIEW`, `BLOCKED_EXCEPTION`, `READY_TO_SHIP`, `SHIPPED`, `CANCELLED`).
5. `version`: Exact integer mapping from `campaign_states.version`.

### Loss Policy
- Zero data loss. All auxiliary order parameters (budget units, initial seed, autonomy policy) are preserved in structured JSONB columns with cryptographic payload hashes.

### Idempotency & Concurrency
- `create_engagement` uses `idempotency_key` scoped to `(workspace_id, operation_id, idempotency_key)`.
- Concurrent updates guard `expected_version`; stale updates raise `SemanticOperationConflict`.

---

## 5. Automated Reconciliation & Parity Verification

```sql
-- Parity Query: Verify 1:1 match between SQLite source manifest and PostgreSQL projection
SELECT 'count_mismatch' AS check_name,
  (SELECT count(*) FROM sqlite_campaign_states) - (SELECT count(*) FROM cae.project) AS difference
UNION ALL
SELECT 'state_mismatch', count(*)
FROM sqlite_campaign_states s
JOIN cae.project p ON s.project_id = p.project_id
WHERE s.lifecycle_state <> p.lifecycle_state;
```

---

## 6. Validation Failures, Quarantine & Recovery

| Failure Class | Trigger Condition | Automated Recovery / Quarantine Route |
|---|---|---|
| `ILLEGAL_TRANSITION` | Attempt to transition between invalid lifecycle states | Rejected with `CampaignValidationError`; current state untouched. |
| `STALE_VERSION_CONFLICT` | `expected_version` does not match current state version | Mutation aborted; fresh state read returned to caller. |
| `ORPHAN_ENGAGEMENT` | Attempt to insert engagement with non-existent `workspace_id` | Foreign key constraint rejects insert; quarantined in `cae.legacy_import_record`. |

### Deterministic Emergency Rollback
If PostgreSQL engagement write fails during `DUAL_VERIFY`, the API immediately routes writes exclusively to SQLite and logs the discrepancy for triage.

---

## 7. Test Fidelity & Negative Countertests

- **Required Fidelity:** `E3_STAGING_PERSISTENCE` (PostgreSQL 17.6 + RLS).
- **Hard Negative Countertest (`HN-STATE-001`):**
  - Attempt: Declare engagement cutover while SQLite order counts exceed PostgreSQL project counts.
  - Expected Verdict: Cutover validator rejects transition; state remains in `DUAL_VERIFY`.
  - Verification: Automated parity validator `verify_ca_state_01.py`.

---

## 8. Operator Decision & Gate Promotion

```yaml
operator_gate_decision:
  gate: "CA-STATE-01 -> CA-TS-01"
  required_action: "Approve MC-CAE-ENG-001 Engagement Authority Contract"
  cutover_permitted_now: false
  authorizing_next_phase_only: "CA-TS-01"
```
