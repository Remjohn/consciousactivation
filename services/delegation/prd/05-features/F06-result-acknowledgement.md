---
title: F06 — Production Acceptance and Downstream Consumption Acknowledgement
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F06
decision_id: D006
---


# F06 — Production Acceptance and Downstream Consumption Acknowledgement

## User outcome

A production-certified asset enters composition only when it is still valid for current downstream state.

## Product behavior

The VAE owns production acceptance; the Content Harness or composition runtime owns compatibility acknowledgement; the protocol validates both without duplicating visual evaluation.

## Brownfield baseline

The VAE PRD defines layered asset effectiveness and Asset Result Contracts. The Content Harness owns sequence and composition state.

## Required product delta

Formalize RESULT_READY, acknowledgement, stable rejection reasons, and completion semantics.

## Traceability

- **Locked decision:** `D006`

- **User journeys:** `UJ-04`, `UJ-12`

- **Cross-cutting NFRs:** `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

## Functional Requirements

### FR-041 — VAE production acceptance authority

**Requirement:** Only the VAE shall assert production acceptance for assets that passed its certified evaluation and delivery gates.

**Testable consequences:**

- Result contracts reference evaluation and production receipts.

- The protocol validates VAE authority.

**Failure examples:**

- The Content Harness marks a raw candidate as production accepted.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-042 — Consumption acknowledgement authority

**Requirement:** Only the owning Content Harness or authorized composition runtime shall acknowledge downstream consumption compatibility.

**Testable consequences:**

- Acknowledgement identifies current demand, sequence, and composition versions.

- The result is not consumable before acknowledgement.

**Failure examples:**

- The VAE unilaterally inserts an asset into Remotion.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-043 — Automatic acknowledgement

**Requirement:** The Content Harness shall automatically acknowledge results when demand identity, dependencies, role, geometry, receipts, references, and non-supersession checks pass.

**Testable consequences:**

- Routine completion requires no human.

- Each check is machine-readable.

**Failure examples:**

- An operator must click approve for every accepted character pose.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-044 — Stable rejection taxonomy

**Requirement:** A result rejection shall use protocol codes such as stale version, missing receipt, incompatible geometry, unavailable asset, or invalidated dependency.

**Testable consequences:**

- Rejection identifies the next action.

- Unstructured aesthetic preference is not a valid rejection.

**Failure examples:**

- The harness returns 'I don't like it'.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-045 — No duplicate visual evaluation

**Requirement:** The Content Harness shall not re-run the VAE's full semantic, Activative, or visual-quality evaluation as part of acknowledgement.

**Testable consequences:**

- Only downstream compatibility is checked.

- Quality disputes route through demand amendment or evaluator-dispute flows.

**Failure examples:**

- The harness launches a second general VLM and overrides the certified evaluator.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-046 — Current dependency verification

**Requirement:** Acknowledgement shall validate the result against current demand, sequence, composition, category profile, and required upstream dependencies.

**Testable consequences:**

- Stale composition geometry is detected.

- Pinned versions appear in the receipt.

**Failure examples:**

- A result is consumed after the scene layout changed.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-047 — Immutable acknowledgement record

**Requirement:** Acknowledgement or rejection shall be an immutable message linked to the exact result and downstream state.

**Testable consequences:**

- Repeated identical acknowledgement is idempotent.

- Later invalidation creates a new notice.

**Failure examples:**

- An acknowledgement field is toggled in place.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-048 — Completion after acknowledgement

**Requirement:** The shared lifecycle shall reach COMPLETED only after a valid production-accepted result is acknowledged or a declared terminal partial-completion policy is satisfied.

**Testable consequences:**

- RESULT_READY remains non-terminal.

- Completion receipts identify consumed assets.

**Failure examples:**

- The protocol marks complete as soon as the VAE finishes packaging.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

## Feature failure conditions

- Production acceptance confused with consumption authority.

- Subjective duplicate review blocks result.

- Stale composition accepted.

## Explicitly out of scope

- VAE quality-scoring internals

- Final publication approval
