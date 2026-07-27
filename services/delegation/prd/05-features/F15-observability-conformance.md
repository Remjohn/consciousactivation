---
title: F15 — Delegation Observability, SLOs, Conformance, and Resilience
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F15
decision_id: D015
---


# F15 — Delegation Observability, SLOs, Conformance, and Resilience

## User outcome

Operators and release gates can prove that cross-product delegation is healthy, compatible, secure, and recoverable.

## Product behavior

The validated Harness Control Tower gains protocol projections; explicit SLOs and executable producer/consumer, authority, lifecycle, compatibility, resilience, and Format 02 suites protect the boundary.

## Brownfield baseline

The Builder and VAE PRDs already mandate event-sourced Control Tower views and benchmark-based certification.

## Required product delta

Specify protocol projections, metrics/SLOs, conformance suites, failure injection, and incident integration.

## Traceability

- **Locked decision:** `D015`

- **User journeys:** `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13`

- **Cross-cutting NFRs:** `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

## Functional Requirements

### FR-113 — Control Tower delegation projection

**Requirement:** The protocol shall project correlation lifecycle, products, negotiated versions, authority, budget, timing, latest event, exceptions, acknowledgements, and invalidation impact into the existing Control Tower.

**Testable consequences:**

- Projection references canonical messages and receipts.

- No separate operational source of truth is created.

**Failure examples:**

- A standalone dashboard maintains its own delegation status.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-114 — Reliability and health metrics

**Requirement:** The system shall measure acceptance, delivery, duplicate suppression, transition validity, acknowledgement, event delivery, audit completeness, and stalled/orphaned work.

**Testable consequences:**

- Metrics are dimensioned by product and version.

- Release gates can consume them.

**Failure examples:**

- Only HTTP request count is measured.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-115 — Latency and freshness SLOs

**Requirement:** The protocol shall define and report SLOs for submission receipt, event delivery, projection freshness, acknowledgement, cancellation, amendment, and critical invalidation propagation.

**Testable consequences:**

- Breaches create operational events.

- Quality thresholds are not weakened to meet SLOs.

**Failure examples:**

- Latency is measured only for completed happy paths.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-116 — Producer and consumer contract tests

**Requirement:** Every product shall pass executable fixtures for all message versions it claims to emit or consume.

**Testable consequences:**

- Fixtures include valid and invalid cases.

- Contract release is blocked on failure.

**Failure examples:**

- Schemas are reviewed manually without runtime tests.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-117 — Authority and lifecycle tests

**Requirement:** The conformance suite shall exercise prohibited actors, illegal transitions, stale messages, idempotency, replay, and terminal-state behavior.

**Testable consequences:**

- Every prohibited action is rejected deterministically.

- Expected audit receipts are asserted.

**Failure examples:**

- Only valid happy-path submissions are tested.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-118 — Compatibility and migration tests

**Requirement:** The suite shall cover same-version, minor compatibility, lossless adapter, migration-required, unsupported feature, and deprecated-version behavior.

**Testable consequences:**

- Manifest claims are evidence-backed.

- Semantic preservation is asserted.

**Failure examples:**

- A migration is tested only for JSON validity.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-119 — Resilience and fault-injection tests

**Requirement:** The suite shall inject duplicate/out-of-order messages, bus interruption, service restart, audit-store interruption, timeouts, and delayed acknowledgement.

**Testable consequences:**

- No duplicate production or illegal state results.

- Recovery receipts identify actions.

**Failure examples:**

- Boundary restart loses correlations.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-120 — Format 02 end-to-end conformance

**Requirement:** Release 1 shall include single-asset, Delegation Set, supersession, escalation, amendment, cancellation, acknowledgement, invalidation/replacement, authority, and migration scenarios for Minimal Coach Theatre.

**Testable consequences:**

- All scenarios are automated and traceable to requirements.

- Downstream Remotion consumption is represented.

**Failure examples:**

- Format 02 certification covers only one successful asset.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

## Feature failure conditions

- Control Tower projection diverges from audit history.

- Compatibility claimed without tests.

- Fault injection creates duplicate VAE production.

## Explicitly out of scope

- VAE internal GPU monitoring

- Builder-wide observability beyond delegation
