---
title: F12 — Typed Amendment Proposals and Authority-Governed Resolution
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F12
decision_id: D012
---


# F12 — Typed Amendment Proposals and Authority-Governed Resolution

## User outcome

Feasibility evidence can lead to precise, reviewable changes without the VAE silently relaxing the demand.

## Product behavior

The VAE proposes immutable field-level options with authority class and predicted consequences; the Content Harness or bounded policy accepts or rejects; acceptance creates a new demand version.

## Brownfield baseline

The VAE PRD defines Constraint Conflicts and non-binding amendment proposals.

## Required product delta

Canonicalize proposal/response contracts, authority classes, auto-policy bounds, and resulting supersession.

## Traceability

- **Locked decision:** `D012`

- **User journeys:** `UJ-06`, `UJ-07`, `UJ-05`

- **Cross-cutting NFRs:** `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

## Functional Requirements

### FR-089 — Typed Amendment Proposal

**Requirement:** The VAE shall express requested demand changes as immutable options containing exact paths, current/proposed values, trigger evidence, and rationale.

**Testable consequences:**

- Options are independently identifiable.

- Free-form prose cannot change authority.

**Failure examples:**

- The editor returns 'make the box bigger' with no field path.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-090 — Authority-class classification

**Requirement:** Each proposed change shall be classified as internal production, execution policy, composition authority, semantic/Activative authority, or constitutional.

**Testable consequences:**

- The protocol routes to the correct owner.

- Misclassified fields are rejected by the authority matrix.

**Failure examples:**

- A subject change is labeled internal workflow adjustment.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-091 — Predicted consequence model

**Requirement:** Each option shall declare expected semantic, Activative, composition, cost, timing, reuse, and invalidation effects with uncertainty.

**Testable consequences:**

- The Content Harness can compare trade-offs.

- Predictions cite evidence and model version.

**Failure examples:**

- An option promises success with no basis.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-092 — Non-binding behavior

**Requirement:** An Amendment Proposal shall not mutate demand, budget, lifecycle authority, or production plan until a valid response is accepted.

**Testable consequences:**

- The original execution checkpoints safely.

- Unaccepted options expire without effect.

**Failure examples:**

- The VAE applies its preferred option while waiting.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-093 — Bounded policy-based approval

**Requirement:** The Content Harness may register narrow deterministic policies for specified fields/ranges that do not affect semantic or constitutional authority.

**Testable consequences:**

- Automatic approval cites the exact policy.

- Out-of-range changes require explicit authority.

**Failure examples:**

- A generic 'minor changes allowed' policy approves a role change.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-094 — Immutable Amendment Response

**Requirement:** Acceptance, rejection, or request-for-alternative shall be an immutable response linked to proposal and selected option.

**Testable consequences:**

- The decision owner is authenticated.

- Duplicate responses are idempotent.

**Failure examples:**

- An option selection is toggled in a mutable UI record.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-095 — Accepted amendment creates new demand

**Requirement:** Any accepted demand-owned change shall produce a new Visual Asset Demand version with supersession, source proposal, and impact analysis.

**Testable consequences:**

- The original remains unchanged.

- Selective invalidation begins from the new version.

**Failure examples:**

- The existing demand is patched in place.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-096 — Constitutional routing

**Requirement:** Proposals affecting category grammar, hard gates, authority boundaries, canonical ontology, or Builder doctrine shall be blocked from ordinary delegation and routed upstream.

**Testable consequences:**

- The protocol emits a constitutional-amendment requirement.

- No local approval can bypass it.

**Failure examples:**

- A VAE amendment alters the Minimal Coach Theatre category law.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

## Feature failure conditions

- Proposal mutates demand before acceptance.

- Authority class misroutes decision.

- Constitutional change approved locally.

## Explicitly out of scope

- Creative ranking of amendment options by the protocol

- Builder governance implementation
