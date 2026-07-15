---
title: F19 — Asynchronous Visual Asset Service and Delegation Boundary
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F19
governing_decisions:
- D003
- D008
- D009
- D023
- D024
- D027
- D028
user_journeys:
- UJ-01
- UJ-04
- UJ-08
- UJ-12
- UJ-14
functional_requirement_count: 8
---


# F19 — Asynchronous Visual Asset Service and Delegation Boundary

**User outcome:** A Content Harness can submit, observe, cancel, amend, and consume visual production through stable contracts without understanding internal ComfyUI workflows.

## Description

The service boundary exposes demands, receipts, events, exceptions, and results while preserving product independence and preparing the separate Delegation PRD.

## Brownfield baseline

V2.1 contains a content-asset delegation module and schemas, but the Visual Editor PRD must define service obligations and leave shared schema ownership to the Delegation PRD.

## Required product delta

Define API behavior, submissions, idempotency, status/events, object references, cancellation, backpressure, result delivery, caller authorization, compatibility, and shared-boundary handoff.

## Traceability

- **Decisions:** D003, D008, D009, D023, D024, D027, D028
- **User journeys:** UJ-01, UJ-04, UJ-08, UJ-12, UJ-14
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-145 — Expose an asynchronous submission API

**Requirement:** The service must accept an authorized demand reference, execution policy, callbacks or event subscription, and idempotency key, then return a durable execution ID and submission receipt without holding the connection for GPU completion.

**Consequences (testable):

- Long-running candidate, repair, and learning runs remain observable after submission.

- A synchronous request-response-only interface is insufficient.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-146 — Publish versioned execution status

**Requirement:** The service must expose registered states from ACCEPTED through validation, planning, capability resolution, queue, production, evaluation, repair, promotion, packaging, and completion plus typed terminal exceptions.

**Consequences (testable):

- Callers can poll or subscribe without controlling internal nodes.

- Unregistered ambiguous states cannot appear in the public contract.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-147 — Emit versioned Visual Asset Events

**Requirement:** Events must identify event/run/demand versions, state, candidate/round when applicable, reason/failure, references, timestamps, and compatibility version.

**Consequences (testable):

- Consumers can rebuild relevant delegation state from events.

- Internal log prose cannot serve as the only integration event.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-148 — Return a provenance-complete Asset Result Contract

**Requirement:** Completed results must list accepted assets and variants, geometry, evaluations, production, budget, syntax-context, authorization, limitations, and downstream action.

**Consequences (testable):

- Downstream composition can validate every referenced artifact and hash.

- A raw image URL alone is not a completed service response.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-149 — Support authorized cancellation

**Requirement:** Registered callers may cancel non-promoted work according to state and policy; cancellation preserves events, artifacts, compute receipts, and reusable learning evidence.

**Consequences (testable):

- The final cancellation receipt identifies work stopped and work retained.

- Cancellation cannot delete accepted historical assets or canonical evidence.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-150 — Communicate backpressure without quality degradation

**Requirement:** The service may return queue depth, capacity, expected delay, runtime alternatives, and scheduling policy while preserving quality thresholds and demand authority.

**Consequences (testable):

- Callers can choose to wait, cancel, or authorize a compatible cost/latency change.

- Load cannot silently route to uncertified capabilities or reduce candidate/evaluator gates.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-151 — Enforce delegation authorization

**Requirement:** Only authorized callers may submit demands, select high-cost or experimental programs, cancel runs, authorize amendments, accept degraded results, or request capability development.

**Consequences (testable):

- All public actions are scoped and receipted.

- An internal service identity cannot impersonate the owning Content Harness for semantic amendments.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

### FR-152 — Prepare the separate Delegation PRD handoff

**Requirement:** This PRD must enumerate required shared contracts, responsibility boundaries, versioning, compatibility, amendment flow, error taxonomy, and test fixtures while explicitly deferring final shared schema authority to the Content Harness ↔ Visual Asset Editor Delegation PRD.

**Consequences (testable):

- Architecture can proceed with representative fixtures but not silently freeze cross-product contracts as editor-only property.

- Any shared-boundary conflict is recorded for the Delegation planning session.

**Traceability:** Decisions D003, D008, D009, D023, D024, D027, D028; journeys UJ-01, UJ-04, UJ-08, UJ-12, UJ-14.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
