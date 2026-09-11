# CAE Aggregate Authority & Migration Contract: Harness Run & Execution State

**Contract ID:** `MC-CAE-RUN-001`  
**Aggregate ID:** `CA-STR-001` (`HarnessTemplate`) & `CA-EXE-001` (`HarnessRun`)  
**Phase ID:** `CA-STATE-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/08_CA_STATE_01_AGGREGATE_AUTHORITY_MIGRATION_MANDATE.md`  
**Constitutional Owner:** `docs/cae/constitutions/CA-CAN-01C_CONSTITUTION.md`  
**Functional Requirement:** `FR-CAE-TEN-012`, `FR-CAE-TEN-013`  

```yaml
contract_metadata:
  contract_id: "MC-CAE-RUN-001"
  aggregate_name: "HarnessRunAndExecutionState"
  single_aggregate_verified: true
  primary_class: "Execution Packet / Canonical Grammar"
  plane: "OPERATIONAL_PLANE / CANONICAL_PLANE"
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
| **Canonical Definition Source** | `PRD-CAE-TEN-001` §3.6; `CA-CAN-01C_CONSTITUTION.md` §3; Bundle v3 `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`. Defines procedural orchestration runbooks and stateful run execution envelopes. | `[DOCUMENT]` `PRD-CAE-TEN-001_TENANT_GUEST_OPERATIONAL_SLICE.md` |
| **Current Operational Authority** | `services/pipeline/` SQLite database (`pipeline_workflows`, `pipeline_runs`, `pipeline_node_states`, `pipeline_run_events`, `pipeline_checkpoints` in `cmf_pipeline/migrations/0001_pipeline_core.sql:56-119`). | `[EXECUTABLE]` `services/pipeline/src/cmf_pipeline/migrations/0001_pipeline_core.sql` |
| **Target Runtime Representation** | PostgreSQL relational tables `cae.harness_template` (canonical snapshot) and `cae.harness_run`, `cae.harness_run_step` (operational runs) with RLS isolation by `workspace_id`. | `[SCHEMA]` Future PostgreSQL foundation schema |
| **Change & Promotion Authority** | CAE Architecture Governance for Template definitions; Workspace Pipeline Runner for Run execution lifecycles. | `[DOCUMENT]` `CAE_SCOPE_AND_AUTHORITY_MATRIX.md:38` |

---

## 2. Source Scope, Identity Mapping & Parent Chain

### Scope & Parent Chain
- **Template Parent Chain (Canonical):** Root Global Canonical (`template_id`, `version`).
- **Run Parent Chain (Operational):** `Workspace` (`workspace_id`) -> `Engagement` (`project_id`) -> `HarnessRun` (`run_id`) -> `HarnessRunStep` (`step_id`).

### Identity Mapping Rules
- **Template Identity:** `tmpl-[a-z0-9_-]+` pinned to git commit hash and content SHA-256.
- **Run Identity:** `run-[a-z0-9_-]+` derived as `deterministic_id("run", {workspace_id, project_id, template_ref, timestamp})`.
- **Step Identity:** `step-[a-z0-9_-]+` mapping 1:1 with pipeline node execution dispatches.
- **Historical Data Boundary:** Legacy pipeline run history (`pipeline_runs` in SQLite) is classified as **`RETAIN_OUT_OF_SCOPE`**. Only newly initiated CAE Harness Runs will execute under PostgreSQL authority.

---

## 3. Five-Stage Authority Progression Model

### Stage 1: `LEGACY_ONLY` (Current State)
- **Entry Criteria:** `cmf_pipeline` executes runs against local SQLite database.
- **Read Path:** Pipeline dashboard reads from local SQLite `pipeline_runs`.
- **Write Path:** Pipeline workers write state transitions to SQLite `pipeline_node_states`.
- **Receipt Requirement:** SQLite run events in `pipeline_run_events`.
- **Exit Criteria:** `cae.harness_run` DDL authored and validated against state machine specification.

### Stage 2: `DUAL_VERIFY`
- **Entry Criteria:** Staging pipeline runner executes shadow harness runs against PostgreSQL while logging to SQLite.
- **Read Path:** Services read from SQLite; shadow queries verify PostgreSQL state transitions.
- **Write Path:** Dual-write state updates with forced rollback validation.
- **Receipt Requirement:** Staging step receipts in `cae.receipt`.
- **Exit Criteria:** Zero state progression divergence across 50 simulated multi-step runs.

### Stage 3: `POSTGRES_AUTHORITATIVE`
- **Entry Criteria:** Formal operator gate promotion (`CA-IMPL-02`).
- **Read Path:** Pipeline scheduler reads run queue and node statuses directly from `cae.harness_run`.
- **Write Path:** Workers transition steps exclusively via typed operations (`dispatch_run_step`, `complete_run_step`).
- **Receipt Requirement:** Immutable step completion receipts in `cae.receipt`.
- **Exit Criteria:** 14 consecutive days of operational stability.

### Stage 4: `LEGACY_READ_ONLY`
- **Entry Criteria:** Legacy SQLite pipeline database locked in read-only mode.
- **Read Path:** PostgreSQL authoritative; SQLite database retained for forensic inspection.
- **Write Path:** PostgreSQL exclusive; SQLite writes prohibited.
- **Receipt Requirement:** Final SQLite pipeline snapshot hash.
- **Exit Criteria:** Archival retention period passed.

### Stage 5: `RETIRED`
- **Entry Criteria:** Legacy SQLite pipeline database archived to cold storage.
- **Read Path / Write Path:** PostgreSQL exclusive.
- **Receipt Requirement:** Pipeline retirement closure receipt.

---

## 4. Transform, Loss & Idempotency Rules

### Transformation Rules
1. `run_id`: Mapped to `cae.harness_run.run_id`.
2. `state`: Mapped from `pipeline_runs.state` (`PENDING`, `RUNNING`, `PAUSED`, `COMPLETED`, `FAILED`, `CANCELLED`).
3. `checkpoint_json`: Preserved as structured JSONB payload.
4. `attempt_count`: Monotonically increasing step retry counter.

### Loss Policy
- Zero data loss. All node output references and failure stack traces are preserved in structured JSONB payloads.

### Idempotency & Concurrency
- `dispatch_run_step` enforces unique `idempotency_key` and optimistic version locking on `cae.state_aggregate`.
- Concurrent dispatch attempts for the same step raise `SemanticOperationConflict`.

---

## 5. Automated Reconciliation & Parity Verification

```sql
-- Parity Query: Verify that all harness run steps have valid parent runs and receipts
SELECT 'orphan_run_steps' AS check_name, count(*) AS failure_count
FROM cae.harness_run_step s
LEFT JOIN cae.harness_run r ON s.run_id = r.run_id
WHERE r.run_id IS NULL
UNION ALL
SELECT 'missing_step_receipts', count(*)
FROM cae.harness_run_step s
LEFT JOIN cae.receipt rec ON s.completion_receipt_id = rec.receipt_id
WHERE s.state = 'COMPLETED' AND rec.receipt_id IS NULL;
```

---

## 6. Validation Failures, Quarantine & Recovery

| Failure Class | Trigger Condition | Automated Recovery / Quarantine Route |
|---|---|---|
| `INVALID_STATE_TRANSITION` | Attempt to advance failed run without retry dispatch | State mutation rejected; run marked `BLOCKED_EXCEPTION`. |
| `CONCURRENT_STEP_LEASE_CONFLICT` | Worker attempts to lease step already leased | Lease rejected; worker backs off via jittered retry. |
| `CORRUPT_CHECKPOINT_PAYLOAD` | Checkpoint JSON hash fails validation | Checkpoint quarantined in `cae.quarantine_record`; run paused. |

### Deterministic Emergency Rollback
If PostgreSQL runner experiences connection loss during `DUAL_VERIFY`, runs automatically pause gracefully at the last verified checkpoint without data corruption.

---

## 7. Test Fidelity & Negative Countertests

- **Required Fidelity:** `E3_STAGING_PERSISTENCE` (PostgreSQL 17.6 + RLS).
- **Hard Negative Countertest (`HN-STATE-005`):**
  - Attempt: Dual-write runner allows SQLite run state to advance to `COMPLETED` while PostgreSQL transaction fails.
  - Expected Verdict: System detects dual-write drift immediately and halts execution rather than accepting silent divergence.
  - Verification: Enforced by atomic two-phase commit wrapper and verified in `verify_ca_state_01.py`.

---

## 8. Operator Decision & Gate Promotion

```yaml
operator_gate_decision:
  gate: "CA-STATE-01 -> CA-TS-01"
  required_action: "Approve MC-CAE-RUN-001 Harness Run Authority Contract"
  cutover_permitted_now: false
  authorizing_next_phase_only: "CA-TS-01"
```
