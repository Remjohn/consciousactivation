# CAE Aggregate Authority & Migration Contract: Receipt & State Transition Lineage

**Contract ID:** `MC-CAE-REC-001`  
**Aggregate ID:** `CA-REC-001` (`Receipt`), `CA-REC-002` (`ExecutionReceipt`), `CA-REL-005` (`ReceiptEvidenceLink`), `CA-STA-001` (`StateAggregate`), `CA-STA-002` (`StateTransition`)  
**Phase ID:** `CA-STATE-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/08_CA_STATE_01_AGGREGATE_AUTHORITY_MIGRATION_MANDATE.md`  
**Constitutional Owner:** `docs/cae/constitutions/CA-CAN-01C_CONSTITUTION.md`  
**Functional Requirement:** `FR-CAE-TEN-014`, `FR-CAE-TEN-015`  
**First Cutover Candidate:** `YES — RECOMMENDED FIRST CUTOVER CANDIDATE`  

```yaml
contract_metadata:
  contract_id: "MC-CAE-REC-001"
  aggregate_name: "ReceiptAndStateTransitionLineage"
  single_aggregate_verified: true
  primary_class: "Receipt / State Aggregate / Relation"
  plane: "OPERATIONAL_PLANE"
  recommended_disposition: "MIGRATE"
  current_authority_state: "DUAL_VERIFY"
  zero_data_movement_guaranteed: true
  execution_action_permitted: false
  recovery_procedure_defined: true
  contract_status: "CONTRACT_RATIFIED_SPEC_ONLY"
  is_first_cutover_candidate: true
```

---

## 1. Authority Axes Deconstruction

| Authority Axis | Specification & Provenance | Evidence Reference |
|---|---|---|
| **Canonical Definition Source** | `PRD-CAE-TEN-001` §3.7; `CA-CAN-01C_CONSTITUTION.md` §4; Bundle v3 `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`, `15_CAE_POSTGRES_STATE_MODEL.md`. Defines append-only cryptographic receipts, execution receipts, causal links, and optimistic state versioning. | `[DOCUMENT]` `PRD-CAE-TEN-001_TENANT_GUEST_OPERATIONAL_SLICE.md` |
| **Current Operational Authority** | SQLite database `receipts`, `commands`, `events` in `packages/ca_runtime/src/ca_runtime/database.py:141-258`. | `[EXECUTABLE]` `packages/ca_runtime/src/ca_runtime/database.py` |
| **Target Runtime Representation** | PostgreSQL relational tables: `cae.command`, `cae.event`, `cae.receipt`, `cae.execution_receipt`, `cae.receipt_evidence_link`, `cae.state_aggregate`, `cae.state_transition`, and lineage view `cae.v_receipt_evidence_lineage`. | `[SCHEMA]` `sql/0004_cae_first_slice_semantic_operations.sql`, `sql/0008_cae_execution_receipt_lineage.sql` |
| **Change & Promotion Authority** | Transactional Operation Adapter (`FirstSliceSemanticOperations._transition()`) at atomic transaction commit time. | `[EXECUTABLE]` `packages/ca_runtime/src/ca_runtime/semantic_operations.py:576-765` |

---

## 2. Source Scope, Identity Mapping & Parent Chain

### Scope & Parent Chain
- **Legal Parent Chain:** `Workspace` (`workspace_id`) -> `Command` (`command_id`) -> `Event` (`event_id`) -> `Receipt` (`receipt_id`) -> `ExecutionReceipt` (`execution_receipt_id`) -> `ReceiptEvidenceLink` (`receipt_id`, `evidence_id`).
- **Optimistic State Chain:** `Workspace` (`workspace_id`) -> `StateAggregate` (`aggregate_type`, `aggregate_id`) -> `StateTransition` (`transition_id`, `sequence`).

### Identity Mapping Rules
- **Command Identity:** `cmd-[a-z0-9_-]+` derived from deterministic hash of command payload.
- **Event Identity:** `evt-[a-z0-9_-]+` minted per atomic transition.
- **Receipt Identity:** `rec-[a-z0-9_-]+` containing canonical SHA-256 of the transition payload, previous receipt hash, and execution timestamp.
- **Execution Receipt Identity:** `exec-rec-[a-z0-9_-]+` containing distinct evaluator actor signature and evidence item references.
- **Anti-Self-Attestation Law (`HN-STATE-010`):** A receipt CANNOT self-attest a cutover or migration claim. Target tables, mock fixtures, URLs, and status flags are not independent migration proof. Every cutover requires an external, evidence-bearing operator review record.

---

## 3. Five-Stage Authority Progression Model

### Stage 1: `LEGACY_ONLY`
- **Entry Criteria:** SQLite database `ProductDatabase` handles transition logging in single-tenant mode.
- **Read Path:** SQLite queries on `receipts` table.
- **Write Path:** `ProductDatabase.record_transition()` writes atomically to SQLite.
- **Receipt Requirement:** SQLite cryptographic hash chain.
- **Exit Criteria:** Foundation schema and typed semantic operations deployed to staging PostgreSQL.

### Stage 2: `DUAL_VERIFY` (Current Staging State)
- **Entry Criteria:** `FirstSliceSemanticOperations` validated on staging PostgreSQL (`CAE_WP03_OPERATION_PROOF.md` and `CAE_WP07_RECEIPT_LINEAGE_RECORD.md`).
- **Read Path:** Applications continue reading local SQLite receipts; shadow verification queries execute against `cae.v_receipt_evidence_lineage`.
- **Write Path:** Typed semantic operations execute transactions in PostgreSQL; receipts emitted with hash chaining and causal links.
- **Receipt Requirement:** Cryptographic verification receipt proving 100% hash chain continuity.
- **Exit Criteria:** Zero hash chain breaks across 10,000 staging operations; operator cutover authorization.

### Stage 3: `POSTGRES_AUTHORITATIVE` (Target Production State)
- **Entry Criteria:** Formal operator gate promotion (`CA-IMPL-02`).
- **Read Path:** All audit verification and compliance tooling queries `cae.receipt` and `cae.v_receipt_evidence_lineage`.
- **Write Path:** All state transitions execute exclusively through `FirstSliceSemanticOperations._transition()`.
- **Receipt Requirement:** Append-only cryptographic ledger in PostgreSQL.
- **Exit Criteria:** Zero state-drift incidents across 30 operational days.

### Stage 4: `LEGACY_READ_ONLY`
- **Entry Criteria:** Legacy SQLite receipt tables set to read-only.
- **Read Path:** PostgreSQL authoritative; SQLite database retained for historical baseline audit.
- **Write Path:** PostgreSQL exclusive; SQLite writes prohibited.
- **Receipt Requirement:** Final SQLite ledger hash seal.
- **Exit Criteria:** Audit retention period satisfied.

### Stage 5: `RETIRED`
- **Entry Criteria:** Legacy SQLite ledger archived to secure cryptographic cold vault.
- **Read Path / Write Path:** PostgreSQL exclusive.
- **Receipt Requirement:** Final ledger archival receipt.

---

## 4. Transform, Loss & Idempotency Rules

### Transformation Rules
1. `receipt_id`: Preserved or minted with prefix `rec-`.
2. `aggregate_type` & `aggregate_id`: Scoped strictly by `workspace_id`.
3. `previous_receipt_sha256`: Preserves continuous hash chaining.
4. `evidence_item_ids`: Preserved as structured causal links in `cae.receipt_evidence_link`.

### Loss Policy
- Zero data loss. Every event payload, causation ID, and actor attestation is written to immutable append-only tables with trigger-level deletion guards.

### Idempotency & Concurrency (`HN-STATE-004`)
- Command deduplication is enforced by `cae.command` unique constraint on `(workspace_id, operation_id, idempotency_key)`.
- Idempotent replay returns the existing cached `OperationReceipt` without creating duplicate events, receipts, or `receipt_evidence_link` rows.

---

## 5. Automated Reconciliation & Parity Verification

```sql
-- Parity Query: Verify that every receipt has valid causal lineage and zero broken hash links
SELECT 'broken_hash_links' AS check_name, count(*) AS failure_count
FROM cae.receipt r1
JOIN cae.receipt r2 ON r1.receipt_id = r2.previous_receipt_id
WHERE r2.previous_receipt_sha256 <> r1.receipt_sha256
UNION ALL
SELECT 'orphan_evidence_links', count(*)
FROM cae.receipt_evidence_link rel
LEFT JOIN cae.receipt r ON rel.receipt_id = r.receipt_id
WHERE r.receipt_id IS NULL;
```

---

## 6. Validation Failures, Quarantine & Recovery

| Failure Class | Trigger Condition | Automated Recovery / Quarantine Route |
|---|---|---|
| `HASH_CHAIN_BREAK` | `previous_receipt_sha256` does not match prior receipt | Transaction aborted; integrity incident logged to `cae.event`. |
| `IDEMPOTENT_REPLAY_CONFLICT` | Identical `idempotency_key` submitted with different payload | Operation rejected with `SemanticOperationConflict`. |
| `STALE_AGGREGATE_VERSION` | `state_aggregate.version` <> `expected_version` | Optimistic concurrency conflict; transaction aborted. |

### Deterministic Emergency Rollback
Every semantic operation executes within a strict PostgreSQL database transaction. Any failure during event, receipt, or link creation triggers an immediate, atomic `ROLLBACK` leaving the state aggregate untouched.

---

## 7. Test Fidelity & Negative Countertests

- **Required Fidelity:** `E3_STAGING_PERSISTENCE` (PostgreSQL 17.6 + RLS).
- **Hard Negative Countertest (`HN-STATE-004`):**
  - Attempt: Submit identical command with identical `idempotency_key` twice in succession.
  - Expected Verdict: Second call returns original receipt without inserting additional rows into `cae.receipt` or `cae.receipt_evidence_link`.
  - Verification: Enforced by `_transition()` in `semantic_operations.py:601` and tested in `verify_ca_state_01.py`.

---

## 8. Operator Decision & Gate Promotion

```yaml
operator_gate_decision:
  gate: "CA-STATE-01 -> CA-TS-01"
  required_action: "Approve MC-CAE-REC-001 as Recommended First Cutover Candidate"
  cutover_permitted_now: false
  authorizing_next_phase_only: "CA-TS-01"
```
