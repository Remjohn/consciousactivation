# Functional Requirement — FR-CAE-TEN-006: Engagement Project Containment

**Requirement ID:** `FR-CAE-TEN-006`  
**Title:** Engagement Campaign and Project Containment Envelope  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `Engagement` (`CA-ENT-004`, `Entity`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01A_ENGAGEMENT.yaml`
- **Canonical Edge:** `REL-OP-003`, `REL-OP-004` in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-007` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects the operational grouping of activation runs, campaigns, and studies. Prevents cross-engagement data mixing and enforces that an `Engagement` is strictly contained within its parent `Workspace` without becoming a standalone multi-tenant root.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL require every `Engagement` to be created within exactly one parent `workspace_id`.
2. The system SHALL enforce that all subordinate execution runs (`HarnessRun`), participant sessions, and assessments inherit the engagement's `workspace_id` and `engagement_id`.
3. The system SHALL maintain a stateful lifecycle for engagements (`PLANNED` $\rightarrow$ `ACTIVE` $\rightarrow$ `PAUSED` $\rightarrow$ `COMPLETED` $\rightarrow$ `ARCHIVED`).
4. The system SHALL prohibit an engagement from referencing guests, media assets, or runs belonging to a different workspace.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `workspace_id` (UUID, required): Parent workspace.
  - `title` (string, required): Engagement / project title.
  - `campaign_type` (string, required): Operational study or campaign typology.
  - `lead_actor_id` (UUID, required): Lead engagement actor.
- **Semantic Outputs:**
  - `engagement_id` (UUID, immutable): Unique engagement identifier.
  - `lifecycle_state` (`PLANNED`, `ACTIVE`, `PAUSED`, `COMPLETED`, `ARCHIVED`): Current state.
  - `created_at` (timestamp, ISO 8601): Creation timestamp.
  - `receipt_id` (UUID): Cryptographic receipt.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Entity`
- **Scope Classification:** `ENGAGEMENT_SCOPED` (Workspace-Contained)
- **Direct Relations:**
  - `REL-OP-003` (`Workspace` $\longrightarrow$ `Engagement`, 1:N)
  - `REL-OP-004` (`Engagement` $\longrightarrow$ `HarnessRun`, 1:N)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01A_ENGAGEMENT.yaml`.
  - *Target Runtime Representation:* Relational projection with composite foreign key `(workspace_id, engagement_id)`.
  - *Promotion Authority:* Workspace Engagement Lead.

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `PLANNED` $\longleftrightarrow$ `ACTIVE` $\longleftrightarrow$ `PAUSED` $\longleftrightarrow$ `COMPLETED` $\longrightarrow$ `ARCHIVED`.
- **State Transition Contracts:**
  - `STC-ENG-001`: `PLANNED -> ACTIVE` upon study launch.
  - `STC-ENG-002`: `ACTIVE -> PAUSED` / `PAUSED -> ACTIVE`.
  - `STC-ENG-003`: `ACTIVE -> COMPLETED` upon run finalization.
  - `STC-ENG-004`: `COMPLETED -> ARCHIVED`.

---

### 7. Authorized Operation Family
- `cae.engagement.create@1.0.0`
- `cae.engagement.transition-state@1.0.0`
- `cae.engagement.archive@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- Every engagement lifecycle state change SHALL emit an immutable `Receipt` (`CA-REC-001`) recording prior state, next state, and authorizing actor.

---

### 9. Validation and Typed Failure Classes
- `ERR_ENG_INVALID_STATE_TRANSITION`: Attempted state move violates the lifecycle graph.
- `ERR_ENG_CROSS_WORKSPACE_REF`: Attempt to link guest or run from another workspace rejected.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** An engagement cannot exist without a valid parent `workspace_id`.
2. **Proposition 2:** Runs created under an engagement strictly inherit its `workspace_id`.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-ENG-001` (Engagement Lifecycle & Scoping)
- **Minimum Fidelity:** `E3_STAGING_PERSISTENCE`
- **Reward-Hack Countertest (`HN-SPEC-008`):** Verify that attempting to add a Guest from Workspace B to an Engagement in Workspace A raises `ERR_ENG_CROSS_WORKSPACE_REF`.

---

### 12. Brownfield Impact
- **Classification:** `ADAPT`
- **Impact Details:** Reconciles existing `api/domain/campaign.py` and `services/pipeline` campaign structures into the formal `Engagement` entity.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on `CA-STATE-01` Engagement Aggregate Contract.
- **Rollback Posture:** Invalidation of active campaign state machines; revert to previous stable snapshot.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** None. Ratified under `CA-CAN-01A`.
- **Prohibited Interpretation:** MUST NOT treat `Engagement` as a tenant root. It is strictly subordinate to `Workspace`.
