---
title: F07 — Budget Authorization, Allocation, Escalation, and Cost Receipts
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F07
decision_id: D007
---


# F07 — Budget Authorization, Allocation, Escalation, and Cost Receipts

## User outcome

The requester controls maximum spend and policy purpose while the VAE autonomously optimizes production within that authority.

## Product behavior

The Content Harness authorizes a budget envelope; the VAE chooses internal allocation; the protocol validates programs, ceilings, escalation, checkpointing, and final receipts.

## Brownfield baseline

The VAE PRD defines six Budget Programs and candidate portfolios. The Content Harness controls demand policy.

## Required product delta

Create immutable budget authorization and escalation contracts with no silent overrun or quality degradation.

## Traceability

- **Locked decision:** `D007`

- **User journeys:** `UJ-07`, `UJ-14`

- **Cross-cutting NFRs:** `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

## Functional Requirements

### FR-049 — Budget-envelope ownership

**Requirement:** The Content Harness shall authorize the Budget Program, policy priority, cost/time/GPU ceilings, experimental policy, and escalation rules.

**Testable consequences:**

- Authorization is signed and versioned.

- Unauthorized Premium or Capability Learning requests are rejected.

**Failure examples:**

- The VAE chooses an unlimited budget based on asset importance.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-050 — VAE allocation autonomy

**Requirement:** The VAE may allocate candidate count, parallelism, workflows, providers, models, evaluators, and repairs inside the authorized envelope.

**Testable consequences:**

- Internal choices need not be specified by the harness.

- Actual usage remains observable.

**Failure examples:**

- The harness dictates exact GPU model and seed count in the shared contract.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-051 — Budget Program validation

**Requirement:** The protocol shall validate selected programs against the canonical registry, caller authority, category certification, and supported VAE capabilities.

**Testable consequences:**

- Unknown or incompatible programs block acceptance.

- Custom programs require complete bounds.

**Failure examples:**

- A free-form 'ultra' budget string is accepted.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-052 — Typed escalation request and response

**Requirement:** Predicted budget insufficiency shall produce a typed escalation with evidence, requested extension, expected outcome, and alternatives.

**Testable consequences:**

- Approval creates a new immutable authorization version.

- Denial preserves checkpointed work.

**Failure examples:**

- The editor silently spends above the ceiling then reports it.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-053 — No silent overrun

**Requirement:** The boundary shall prevent starting work that would exceed a hard authorized ceiling without an accepted extension.

**Testable consequences:**

- The execution enters COST_APPROVAL_REQUIRED.

- No new expensive nodes begin while awaiting approval.

**Failure examples:**

- A third-party provider invoice exceeds the ceiling because actual use was not checked.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-054 — Capability Learning authorization

**Requirement:** Transition into a Capability Learning purpose shall require explicit Content Harness policy or operator authority.

**Testable consequences:**

- Ordinary production cannot silently become experimentation.

- Learning receipts state controlled variables.

**Failure examples:**

- A failed image triggers a 30-candidate experiment automatically.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-055 — Quality-gate preservation

**Requirement:** Budget exhaustion or deadline pressure shall not permit the protocol or VAE to lower constitutional quality gates without a new authorized demand or degradation decision.

**Testable consequences:**

- Stopping without an asset is permitted.

- A passing existing candidate may be returned.

**Failure examples:**

- The system accepts a wrong action to remain under budget.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-056 — Final budget receipt

**Requirement:** Every terminal delegation shall include authorization versions, actual spend, GPU/time usage, candidate counts, repairs, compliance, and avoided cost where measurable.

**Testable consequences:**

- Receipt reconciles to VAE execution data.

- Control Tower exposes budget state.

**Failure examples:**

- Only estimated cost is retained after completion.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

## Feature failure conditions

- Silent budget overrun.

- Content Harness leaks internal compute control.

- Capability Learning begins without authority.

## Explicitly out of scope

- Cloud-provider billing implementation

- Project-wide financial accounting outside delegation
