# CAE Aggregate Authority & Migration Contract: Guest

**Contract ID:** `MC-CAE-GST-001`  
**Aggregate ID:** `CA-ENT-003` (`Guest`) & `CA-MAP-001` (`GuestIdentityLink`)  
**Phase ID:** `CA-STATE-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/08_CA_STATE_01_AGGREGATE_AUTHORITY_MIGRATION_MANDATE.md`  
**Constitutional Owner:** `docs/cae/constitutions/CA-CAN-01B_CONSTITUTION.md`  
**Functional Requirement:** `FR-CAE-TEN-007`, `FR-CAE-TEN-008`  

```yaml
contract_metadata:
  contract_id: "MC-CAE-GST-001"
  aggregate_name: "Guest"
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
| **Canonical Definition Source** | `PRD-CAE-TEN-001` §3.4; `CA-CAN-01B_CONSTITUTION.md` §2; `FR-CAE-TEN-007`. Defines Guest as a workspace-local entity representing qualitative interview participants. | `[DOCUMENT]` `PRD-CAE-TEN-001_TENANT_GUEST_OPERATIONAL_SLICE.md` |
| **Current Operational Authority** | Implicit in brownfield SQLite `services/interview/` interview sessions and turn records. | `[EXECUTABLE]` `services/interview/src/conscious_activations_interview_expression/` |
| **Target Runtime Representation** | PostgreSQL relational table `cae.guest` (or `cae.actor` of kind `GUEST`) with composite primary key `(workspace_id, guest_id)` and strict RLS scoping. | `[SCHEMA]` `sql/0001_cae_foundation_draft.sql:74` |
| **Change & Promotion Authority** | Workspace Engagement Lead / Participant Consent via typed operations (`register_guest`, `update_guest_profile`). | `[DOCUMENT]` `CAE_SCOPE_AND_AUTHORITY_MATRIX.md:36` |

---

## 2. Source Scope, Identity Mapping & Parent Chain

### Scope & Parent Chain
- **Legal Parent Chain:** `Workspace` (`workspace_id`) -> `Guest` (`guest_id`).
- **Subordinate Aggregates:** `InterviewSession` (`CA-SES-001`), `EvidenceItem` (`CA-EVI-002`), `GuestVoiceDNA` (`CA-DNA-001`).

### Identity Mapping Rules
- **Source Identifier:** Brownfield guest email, interview subject ID, or participant label in `services/interview/`.
- **Target Identifier:** Composite primary key `(workspace_id, guest_id)` where `guest_id = deterministic_id("gst", {workspace_id, participant_core})`.
- **Anti-Auto-Merge Law (`HN-STATE-003`):** Same email address, name, embedding, or phone number across different workspaces does NOT constitute identity proof. Automatic profile deduplication across workspaces is strictly prohibited.
- **Cross-Workspace Linking Policy:** `GuestIdentityLink` (`CA-MAP-001`) requires explicit, bilateral, cryptographic consent receipts. Runtime execution of identity links is formally **`RETAIN_OUT_OF_SCOPE`** / **`DEFERRED`** in this operational slice.

---

## 3. Five-Stage Authority Progression Model

### Stage 1: `LEGACY_ONLY` (Current State)
- **Entry Criteria:** Guest identity is implicit in interview expression recordings and campaign configurations.
- **Read Path:** Interview service reads participant data directly from local SQLite.
- **Write Path:** Participant metadata written to SQLite session tables.
- **Receipt Requirement:** None.
- **Exit Criteria:** Foundation schema active in PostgreSQL; workspace-local guest extraction script validated.

### Stage 2: `DUAL_VERIFY`
- **Entry Criteria:** Shadow extractor derives workspace-local Guest profiles and inserts to `cae.guest` with rollback testing.
- **Read Path:** Services read from SQLite; shadow queries verify PostgreSQL composite key isolation.
- **Write Path:** Dual-registration of new interview participants.
- **Receipt Requirement:** Guest registration receipts validating composite key uniqueness.
- **Exit Criteria:** Zero cross-workspace key collisions; operator review completed.

### Stage 3: `POSTGRES_AUTHORITATIVE`
- **Entry Criteria:** Formal operator gate promotion (`CA-IMPL-02`).
- **Read Path:** All interview services and AIR assessment engines query Guest profiles via `cae.guest` filtered by `workspace_id`.
- **Write Path:** Guest mutations occur exclusively via typed semantic operations.
- **Receipt Requirement:** Append-only guest profile transition receipts.
- **Exit Criteria:** 30 days of clean operational execution without identity collision.

### Stage 4: `LEGACY_READ_ONLY`
- **Entry Criteria:** Legacy interview database switched to read-only mode.
- **Read Path:** PostgreSQL authoritative; SQLite database archived for compliance audit.
- **Write Path:** PostgreSQL exclusive; legacy writes prohibited.
- **Receipt Requirement:** Hashed participant archive snapshot.
- **Exit Criteria:** Retention requirements met.

### Stage 5: `RETIRED`
- **Entry Criteria:** Legacy participant records fully decommissioned or anonymized per GDPR/privacy protocols.
- **Read Path / Write Path:** PostgreSQL exclusive.
- **Receipt Requirement:** Final participant ledger closure receipt.

---

## 4. Transform, Loss & Idempotency Rules

### Transformation Rules
1. `workspace_id`: Explicitly inherited from parent Workspace.
2. `guest_id`: Sanitized alphanumeric identifier scoped to workspace.
3. `display_name`: Human-readable participant identifier.
4. `consent_state`: Set to `EXPLICIT_CONSENT_RECORDED` with timestamp and consent receipt reference.

### Loss Policy
- Zero data loss. All biographical annotations and interview notes are stored in structured JSONB payload attributes.

### Idempotency & Concurrency
- `register_guest` is idempotent on `(workspace_id, guest_id)`. Replays with identical payload return existing record; payload conflicts raise `SemanticOperationConflict`.

---

## 5. Automated Reconciliation & Parity Verification

```sql
-- Parity Query: Verify that zero guests exist with global (non-workspace) scope
SELECT 'global_guest_violation' AS check_name, count(*) AS failure_count
FROM cae.guest
WHERE workspace_id IS NULL OR workspace_id = ''
UNION ALL
SELECT 'cross_tenant_shared_guest_id', count(*)
FROM (
  SELECT guest_id, count(DISTINCT workspace_id) AS ws_count
  FROM cae.guest
  GROUP BY guest_id
  HAVING count(DISTINCT workspace_id) > 1
) cross_tenants;
```

---

## 6. Validation Failures, Quarantine & Recovery

| Failure Class | Trigger Condition | Automated Recovery / Quarantine Route |
|---|---|---|
| `UNCONSENTED_MERGE_ATTEMPT` | System attempts to link two guest records without dual consent | Link creation rejected; defect logged to Quarantine Register. |
| `ORPHAN_GUEST_PROFILE` | Guest record created without valid `workspace_id` | Foreign key constraint rejects insert; transaction aborted. |
| `CONSENT_REVOCATION` | Guest requests GDPR data erasure / withdrawal | Profile status set to `ANONYMIZED`; relational receipts preserved. |

### Deterministic Emergency Rollback
If PostgreSQL Guest profile lookups fail during `DUAL_VERIFY`, services immediately fall back to reading legacy SQLite participant headers.

---

## 7. Test Fidelity & Negative Countertests

- **Required Fidelity:** `E3_STAGING_PERSISTENCE` (PostgreSQL 17.6 + RLS).
- **Hard Negative Countertest (`HN-STATE-003`):**
  - Attempt: Interview session in `workspace_b` attempts to link to `guest_id_01` created in `workspace_a`.
  - Expected Verdict: Foreign key / RLS rejects link; session cannot cross workspace boundaries.
  - Verification: Automated countertest in `verify_ca_state_01.py`.

---

## 8. Operator Decision & Gate Promotion

```yaml
operator_gate_decision:
  gate: "CA-STATE-01 -> CA-TS-01"
  required_action: "Approve MC-CAE-GST-001 Guest Authority Contract"
  cutover_permitted_now: false
  authorizing_next_phase_only: "CA-TS-01"
```
