---
title: F04 — Stable External Lifecycle and Deterministic Projection
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F04
decision_id: D004
---


# F04 — Stable External Lifecycle and Deterministic Projection

## User outcome

Both products and operators can understand the shared commitment without coupling to internal production nodes.

## Product behavior

The protocol owns a compact external lifecycle projected from authoritative product messages and validates every transition, timeout, and terminal state.

## Brownfield baseline

Content Harness and VAE each own richer internal state machines. The VAE PRD already defines production stages and events.

## Required product delta

Define the public lifecycle, transition table, product-to-protocol projections, timeout semantics, and illegal-transition tests.

## Traceability

- **Locked decision:** `D004`

- **User journeys:** `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14`

- **Cross-cutting NFRs:** `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

## Functional Requirements

### FR-025 — Canonical external states

**Requirement:** The protocol shall define stable states including DRAFT, SUBMITTED, ACCEPTED, IN_PROGRESS, RESULT_READY, COMPLETED, and governed exceptional states.

**Testable consequences:**

- States have explicit definitions and owners.

- Arbitrary product status strings cannot become protocol state.

**Failure examples:**

- The public lifecycle exposes 'model_loading_flux'.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-026 — Authoritative state projection

**Requirement:** A shared-state change shall be derived only from an accepted authoritative product message mapped through a registered projection rule.

**Testable consequences:**

- The protocol never invents progress.

- Projection records the source message.

**Failure examples:**

- The boundary marks RESULT_READY because a timeout estimate elapsed.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-027 — Transition validation

**Requirement:** Every state transition shall be checked against a deterministic lifecycle machine before persistence.

**Testable consequences:**

- Illegal forward and backward transitions are rejected.

- Transition receipts record from-state, to-state, and rule.

**Failure examples:**

- COMPLETED transitions directly back to IN_PROGRESS.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-028 — Terminal-state enforcement

**Requirement:** Terminal states shall reject ordinary progress messages and require explicit post-completion notice types for invalidation, revocation, or replacement.

**Testable consequences:**

- Late events do not reopen completed delegations.

- Post-completion governance remains auditable.

**Failure examples:**

- A late candidate event changes a completed result.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-029 — Exceptional lifecycle paths

**Requirement:** The lifecycle shall govern rejection, amendment, supersession, budget approval, capability gap, human review, cancellation, partial result, invalidation, revocation, and replacement.

**Testable consequences:**

- Each exception has allowed entry and exit transitions.

- Decision authority is explicit.

**Failure examples:**

- CAPABILITY_GAP is emitted as an arbitrary string with no next action.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-030 — Timeout semantics

**Requirement:** The protocol shall distinguish target miss, heartbeat loss, production estimate overrun, approval timeout, hard cutoff, and expiry.

**Testable consequences:**

- Timeouts emit typed events.

- Timeout does not silently lower quality or cancel unless policy says so.

**Failure examples:**

- A soft deadline automatically accepts a degraded candidate.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-031 — Lifecycle reconstruction

**Requirement:** The current projection shall be reproducible from the accepted append-only message and audit sequence.

**Testable consequences:**

- Projection rebuild matches stored state.

- Corrupt projections can be repaired without product mutation.

**Failure examples:**

- The lifecycle exists only as a mutable row with no event history.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-032 — Lifecycle receipts and observability

**Requirement:** Each accepted transition shall emit a lifecycle receipt and update the Control Tower projection within the defined freshness SLO.

**Testable consequences:**

- Operators can identify the latest authoritative cause.

- Stalled states are detectable.

**Failure examples:**

- A transition occurs without an observable event or receipt.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

## Feature failure conditions

- Public state couples to internal workflow nodes.

- Illegal transition accepted.

- Terminal state reopened by ordinary event.

## Explicitly out of scope

- Internal VAE production graph

- Internal Content Harness sequencing states
