---
title: F13 — Post-Completion Invalidation, Revocation, Supersession, and Replacement
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F13
decision_id: D013
---


# F13 — Post-Completion Invalidation, Revocation, Supersession, and Replacement

## User outcome

Previously accepted assets remain historically reproducible while current and future consumption responds correctly to new evidence.

## Product behavior

The protocol preserves immutable results and changes only their authorization state through typed invalidation, revocation, supersession, replacement, and recall-review notices.

## Brownfield baseline

The VAE PRD defines immutable asset versions, Visual Asset Memory, regression detection, and revocation needs. The Content Harness owns current sequence use.

## Required product delta

Create post-completion notices, impact graph traversal, replacement compatibility, and acknowledgement tracking.

## Traceability

- **Locked decision:** `D013`

- **User journeys:** `UJ-12`, `UJ-04`, `UJ-14`

- **Cross-cutting NFRs:** `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

## Functional Requirements

### FR-097 — Typed invalidation notice

**Requirement:** An owning product shall be able to mark a result as requiring revalidation when dependencies or authority context change without asserting that the asset is defective.

**Testable consequences:**

- New and active consumption can be blocked pending review.

- Historical use remains intact.

**Failure examples:**

- The asset file is deleted when a composition version changes.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-098 — Typed revocation notice

**Requirement:** The VAE or authorized integrity owner shall be able to revoke an asset for critical defect, integrity, security, evaluator-regression, or withdrawn-capability reasons.

**Testable consequences:**

- New consumption is blocked immediately.

- Severity and effective time are explicit.

**Failure examples:**

- A critical identity mismatch is only logged as a warning.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-099 — Supersession and replacement notices

**Requirement:** The protocol shall distinguish a newer preferred result from a mandatory replacement and link old/new assets and results.

**Testable consequences:**

- Older versions remain historical.

- Future retrieval uses current authorization state.

**Failure examples:**

- A new binary overwrites the old asset URI.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-100 — Downstream impact analysis

**Requirement:** The protocol shall traverse consumption links from result to variants, compositions, scenes/slides, sequences, outputs, and publications.

**Testable consequences:**

- Affected active and published scopes are reported separately.

- Required actions are typed.

**Failure examples:**

- An invalidation cannot identify where the asset was used.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-101 — Replacement compatibility validation

**Requirement:** A replacement shall be checked against current demand, geometry, masks, timing, Visual Syntax context, and composition before substitution.

**Testable consequences:**

- Replacement is not assumed drop-in.

- Selective composition reevaluation is triggered.

**Failure examples:**

- A character replacement with different BBOX is swapped without testing.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-102 — Historical reproducibility

**Requirement:** Invalidated or revoked artifacts, hashes, receipts, and actual historical consumption links shall remain retained under policy.

**Testable consequences:**

- Past outputs can be rebuilt exactly.

- Restricted access may apply for integrity/security.

**Failure examples:**

- Revocation removes evidence of what shipped.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-103 — Negative-evidence retention

**Requirement:** Revoked, rejected, or superseded assets may remain available to evaluators and learning systems as negative or historical evidence but shall be excluded from ordinary reuse.

**Testable consequences:**

- Memory query respects authorization state.

- Failure lessons retain provenance.

**Failure examples:**

- A revoked pose is retrieved as a normal reuse candidate.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-104 — Recall-review support

**Requirement:** For already-published outputs, the protocol shall issue review recommendations and track acknowledgement without silently editing publication records.

**Testable consequences:**

- Human or policy owner decides recall action.

- Audit shows unresolved published impacts.

**Failure examples:**

- The protocol automatically republishes edited content.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

## Feature failure conditions

- Historical artifact overwritten or deleted.

- Revoked asset reused normally.

- Replacement assumed composition-compatible.

## Explicitly out of scope

- Publication-management system

- VAE internal asset-regression investigation
