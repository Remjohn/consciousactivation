# Functional Requirement — FR-CAE-TEN-015: Receipt Evidence Lineage Traceability

**Requirement ID:** `FR-CAE-TEN-015`  
**Title:** Immutable Receipt Evidence Lineage and Anti-Reward-Hacking Traceability  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `ReceiptEvidenceLink` (`CA-REL-005`, `Relation`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01C_RECEIPT_EVIDENCE_LINK.yaml`
- **Canonical Edge:** `REL-OP-010` in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-004`, `COL-CAN-010` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects the verifiable reality contact of operational runs. Prevents hallucinated or ungrounded outputs by establishing an immutable relational bridge linking execution receipts to the specific evidence items, media spans, and participant turns observed or produced during operation commit. Prohibits linking evidence across workspace boundaries.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL record `ReceiptEvidenceLink` entries linking a `receipt_id` to one or more `evidence_id` items within the same `workspace_id`.
2. The system SHALL enforce that each link records the explicit link role: `INPUT_EVIDENCE`, `OUTPUT_EVIDENCE`, or `CONTEXT_EVIDENCE`.
3. The system SHALL enforce database-level triggers preventing cross-workspace evidence linkage: attempting to link a receipt in Workspace A to evidence in Workspace B SHALL fail immediately.
4. The system SHALL provide an auditable lineage view resolving the complete chain from final activation output backward to raw media timestamps and byte hashes.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `workspace_id` (UUID, required): Parent workspace.
  - `receipt_id` (UUID, required): Parent execution receipt.
  - `evidence_id` (UUID, required): Linked evidence item.
  - `link_role` (enum, required): `INPUT_EVIDENCE`, `OUTPUT_EVIDENCE`, `CONTEXT_EVIDENCE`.
- **Semantic Outputs:**
  - `link_id` (UUID, immutable): Unique link identifier.
  - `linked_at` (timestamp, ISO 8601): Link timestamp.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Relation`
- **Scope Classification:** `WORKSPACE_SCOPED`
- **Direct Relations:**
  - `REL-OP-010` (`Receipt` $\longrightarrow$ `ReceiptEvidenceLink` $\longrightarrow$ `EvidenceItem`, N:M)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01C_RECEIPT_EVIDENCE_LINK.yaml`, WP-07 Execution Receipts & Evidence Lineage.
  - *Target Runtime Representation:* Relational junction table `cae.receipt_evidence_link` and query view `cae.v_receipt_evidence_lineage`.
  - *Promotion Authority:* Transactional State Engine at commit time.

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `COMMITTED_IMMUTABLE` (Append-only; immutable upon creation).
- **State Transition Contracts:**
  - `STC-LNK-001`: `LINK -> COMMITTED_IMMUTABLE`

---

### 7. Authorized Operation Family
- `cae.receipt.link-evidence@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- Every evidence linkage is captured directly within the execution transaction of the parent receipt.

---

### 9. Validation and Typed Failure Classes
- `ERR_LNK_CROSS_WORKSPACE`: Attempt to link receipt and evidence from different workspaces rejected.
- `ERR_LNK_EVIDENCE_NOT_FOUND`: Referenced evidence ID does not exist.
- `ERR_LNK_INVALID_ROLE`: Unrecognized evidence linkage role.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** An evidence link cannot be created across different workspaces.
2. **Proposition 2:** Querying the receipt evidence lineage view for a completed run returns the complete graph of verified media spans.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-LNK-002` (Receipt Evidence Lineage & Cross-Workspace Denial)
- **Minimum Fidelity:** `E3_STAGING_PERSISTENCE`
- **Reward-Hack Countertest (`HN-SPEC-008`, `HN-CAN-027`):** Attempt to insert a `ReceiptEvidenceLink` linking a Receipt in Workspace A with an EvidenceItem in Workspace B; verify that database trigger rejects the insert with `ERR_LNK_CROSS_WORKSPACE`.

---

### 12. Brownfield Impact
- **Classification:** `NEW`
- **Impact Details:** Introduces explicit receipt-to-evidence lineage tracking based on WP-07 staging proof.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on `CA-STATE-01` Receipt Lineage Aggregate Contract.
- **Rollback Posture:** Invalidation of erroneous links; re-link from deterministic transaction logs.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** None. Ratified under `CA-CAN-01C`.
- **Prohibited Interpretation:** MUST NOT link evidence items across workspace boundaries under any circumstance.
