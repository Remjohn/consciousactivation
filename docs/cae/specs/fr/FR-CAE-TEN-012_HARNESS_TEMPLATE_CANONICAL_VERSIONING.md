# Functional Requirement — FR-CAE-TEN-012: Harness Template Canonical Versioning

**Requirement ID:** `FR-CAE-TEN-012`  
**Title:** Stateless Canonical Harness Template Versioning and Immutability  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  

---

### 1. Authoritative Source & Constitutional Owner
- **Primary Constitutional Owner:** `HarnessTemplate` (`CA-STR-001`, `Canonical Structural Grammar`)
- **Governing Constitution:** `docs/cae/constitutions/CA-CAN-01C_HARNESS_TEMPLATE.yaml`
- **Canonical Edge:** `REL-CANON-001` in `CAE_FIRST_SLICE_CANONICAL_RELATION_MAP.md`
- **Collision Closures:** `COL-MAP-002`, `COL-CAN-009` in `CAE_FIRST_SLICE_CONTRADICTION_CLOSURE.md`

---

### 2. Problem / Decision Being Protected
Protects the reproducibility and canonical integrity of CAE execution runbooks. Enforces that procedural specifications (`HarnessTemplate`) are stateless, globally versioned canonical grammars residing exclusively on the Canonical Plane. Prohibits operational executions from mutating templates or injecting tenant facts into canonical runbooks.

---

### 3. Required Behavior & Explicit Boundary
1. The system SHALL define `HarnessTemplate` as a stateless, immutable procedural definition on the Canonical Plane.
2. The template SHALL contain ZERO tenant facts: no `workspace_id`, no `guest_id`, no private storage keys, and no mutable execution state counters.
3. The template SHALL specify the step sequence, required input types, allowed semantic operations, transition preconditions, and typed recovery routes.
4. The system SHALL enforce strict semantic versioning (`major.minor.patch`) and prohibit in-place mutation of a published template version once referenced by operational runs.

---

### 4. Inputs & Outputs at Semantic Level
- **Semantic Inputs:**
  - `template_name` (string, required): Descriptive template name (e.g. `evidence_to_air_first_slice`).
  - `version` (string, semver, required): Pinned semantic version (e.g. `1.0.0`).
  - `procedural_graph` (object, required): Step definitions, operation bindings, and before-transfer validation rules.
  - `governance_signature` (string, required): Cryptographic signature of governing architecture authority.
- **Semantic Outputs:**
  - `template_id` (string, immutable): Canonical template identifier.
  - `template_digest` (string, SHA-256, immutable): Cryptographic hash of template definition.
  - `publication_state` (`DRAFT`, `PUBLISHED`, `DEPRECATED`): Lifecycle status.

---

### 5. Objects, Relations, Scope, and Authority Axes
- **Object Class:** `Canonical Structural Grammar`
- **Scope Classification:** `GLOBAL_CANONICAL` (Tenantless Canonical Plane)
- **Direct Relations:**
  - `REL-CANON-001` (`HarnessRun` $\longrightarrow$ `HarnessTemplate`, N:1 read-only reference)
- **Three Authority Axes:**
  - *Definition Source:* `CA-CAN-01C_HARNESS_TEMPLATE.yaml`, `docs/cae/runbooks/evidence_to_air_first_slice_v1.yaml`.
  - *Target Runtime Representation:* Read-only canonical registry table / versioned repository YAML artifact.
  - *Promotion Authority:* CAE Canonical Architecture Governance Committee.

---

### 6. State / Transition Implication
- **Lifecycle Graph:** `DRAFT` $\longrightarrow$ `PUBLISHED` $\longrightarrow$ `DEPRECATED`.
- **State Transition Contracts:**
  - `STC-TMPL-001`: `PUBLISH -> PUBLISHED`
  - `STC-TMPL-002`: `DEPRECATE -> DEPRECATED`

---

### 7. Authorized Operation Family
- `cae.template.publish@1.0.0`
- `cae.template.deprecate@1.0.0`

---

### 8. Evidence, Receipt, and Provenance Requirement
- Template publication SHALL record an immutable publication digest and commit hash in the canonical registry ledger.

---

### 9. Validation and Typed Failure Classes
- `ERR_TMPL_MUTATION_PROHIBITED`: Attempt to edit a published template version in-place rejected.
- `ERR_TMPL_TENANT_DATA_DETECTED`: Template definition contains workspace/guest/tenant identifiers.
- `ERR_TMPL_INVALID_SCHEMA`: Procedural graph violates canonical structural grammar rules.

---

### 10. Acceptance Propositions & Measurable Completion Condition
1. **Proposition 1:** A published template version cannot be modified post-publication.
2. **Proposition 2:** A template containing a `workspace_id` or `guest_id` fails publication validation.

---

### 11. Test Class, Minimum Fidelity, and Reward-Hack Countertest
- **Test Class:** `TC-TMPL-001` (Template Immutability & Canonical Purity)
- **Minimum Fidelity:** `E1_STATIC` / `E2_REPOSITORY_FIXTURE`
- **Reward-Hack Countertest (`HN-SPEC-009`, `HN-CAN-021`):** Verify that attempting to register a template containing a hardcoded tenant ID or mutable status field is rejected with `ERR_TMPL_TENANT_DATA_DETECTED`.

---

### 12. Brownfield Impact
- **Classification:** `NEW` / `ADAPT`
- **Impact Details:** Canonicalizes YAML runbooks (`docs/cae/runbooks/`) into versioned, immutable structural templates.

---

### 13. Migration / Rollback Dependency
- **Dependency:** Dependent on `CA-STATE-01` Canonical Registry Contract.
- **Rollback Posture:** Invalidation of draft templates; rollback to previous published semver.

---

### 14. Open Decision & Prohibited Interpretation
- **Open Decision:** None. Ratified under `CA-CAN-01C`.
- **Prohibited Interpretation:** MUST NOT treat `HarnessTemplate` as an active runtime orchestrator or a general agent framework. It is stateless procedural doctrine.
