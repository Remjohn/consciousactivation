# Functional Requirement — FR-CAE-TEN-014: Operation Receipt Immutable Ledger

**Requirement ID:** `FR-CAE-TEN-014`  
**Title:** Cryptographic Operation Execution Receipt Ledger  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `Receipt` (`CA-REC-001`, `Receipt / Evaluation Record`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01C_RECEIPT.yaml`
- **Canonical Edge:** `REL-OP-009` in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-004`, `COL-CAN-010`, `COL-CAN-011` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects the auditability and anti-reward-hacking integrity of CAE operational executions. Enforces that every consequential state change generates an append-only, cryptographic execution receipt committed atomically with state changes. Enforces the anti-self-attestation law: a receipt proves mechanical execution, NOT semantic truth or aesthetic quality.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL generate an immutable `Receipt` record atomically within the same database transaction as any state transition or command commit.
2. The receipt SHALL record `workspace_id`, `actor_id`, `command_id`, `transition_id`, `operation_id`, `contract_version`, `input_payload_sha256`, `output_payload_sha256`, and validator outcomes.
3. The system SHALL prohibit in-place mutation or deletion of committed receipts.
4. The system SHALL initialize epistemic and qualitative proof fields (`reward_hack_result`, `taste_integrity_result`) to `UNVERIFIED` / `NOT_APPLICABLE` by default, requiring separate independent evaluator records to prove semantic validity.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `workspace_id` (UUID, required): Parent workspace.
  - `actor_id` (UUID, required): Initiating actor.
  - `operation_id` (string, required): Qualified semantic operation ID.
  - `contract_version` (string, required): Semantic operation contract version.
  - `input_payload` (object, required): Operation inputs.
  - `output_payload` (object, required): Operation outputs.
- **Semantic Outputs:**
  - `receipt_id` (UUID, immutable): Unique cryptographic receipt identifier.
  - `input_sha256` (string, 64-hex): Cryptographic digest of input payload.
  - `output_sha256` (string, 64-hex): Cryptographic digest of output payload.
  - `committed_at` (timestamp, ISO 8601): Atomic transaction commit timestamp.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Receipt / Evaluation Record`
- **Scope Classification:** `WORKSPACE_SCOPED` (Audit & Verification Ledger)
- **Direct Relations:**
  - `REL-OP-009` (`Receipt` $\longrightarrow$ `StateTransition`, 1:1 atomic audit link)
  - `REL-OP-010` (`Receipt` $\longrightarrow$ `ReceiptEvidenceLink`, 1:N lineage bridge)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01C_RECEIPT.yaml`, Bundle v3 `11_CAE_PHASE_PROMOTION_AND_PROOF_PROTOCOL.md`.
  - *Target Runtime Representation:* Append-only relational table `cae.receipt` / `cae.execution_receipt`.
  - *Promotion Authority:* Transactional State Engine at commit time.

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `COMMITTED_IMMUTABLE` (Append-only; no update/delete transitions).
- **State Transition Contracts:**
  - `STC-REC-001`: `COMMIT -> COMMITTED_IMMUTABLE`

---

### 7. Authorized Operation Family
- `cae.receipt.commit@1.0.0`
- `cae.receipt.verify-integrity@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- The receipt is self-proving for mechanical execution facts and serves as primary evidence for operation auditability.

---

### 9. Validation and Typed Failure Classes
- `ERR_REC_MUTATION_DENIED`: Attempt to update or delete a committed receipt.
- `ERR_REC_MISSING_PROVENANCE`: Operation commit attempted without actor, operation, or digest data.
- `ERR_REC_UNCOMMITTED_OPERATION`: Receipt generated before database transaction commits.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** An authorized state transition cannot commit without producing an immutable execution receipt.
2. **Proposition 2:** A receipt cannot be altered or purged from the database after transaction commit.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-REC-001` (Receipt Immutability & Anti-Self-Attestation)
- **Minimum Fidelity:** `E3_STAGING_PERSISTENCE` (PostgreSQL append-only table with trigger enforcement)
- **Reward-Hack Countertest (`HN-SPEC-004`, `HN-CAN-028`):** Verify that an acceptance test requiring qualitative assessment passes ONLY when an independent evaluator record exists, and fails if relying solely on execution receipt presence.

---

### 12. Brownfield Impact
- **Classification:** `EXTEND`
- **Impact Details:** Extends `packages/ca_runtime` database receipt utility to enforce workspace isolation, contract versioning, and anti-self-attestation defaults.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on `CA-STATE-01` Receipt Ledger Aggregate Contract.
- **Rollback Posture:** Append-only; compensation receipts generated for rolled-back operations.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** None. Ratified under `CA-CAN-01C`.
- **Prohibited Interpretation:** MUST NOT treat receipt presence as independent proof of semantic truth, human truth, or aesthetic quality.
