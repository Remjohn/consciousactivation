---
title: F16 — Delegation Readiness, Development Capsule, and Production Certification
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F16
decision_id: D016
---


# F16 — Delegation Readiness, Development Capsule, and Production Certification

## User outcome

Implementation begins only when the shared boundary is complete, testable, architecture-preserving, and proven across both products.

## Product behavior

The formal gate requires product-boundary proof, full contract family, authority/lifecycle/compatibility artifacts, Format 02 fixtures, integrity/resilience evidence, Control Tower projection, conformance suite, and Development Capsule.

## Brownfield baseline

The upstream PRDs both define formal Implementation Authorization Gates and explicitly defer final shared contract ownership to this PRD.

## Required product delta

Compile delegation-specific readiness states, hard gates, prohibitions, Development Capsule requirements, and production certification path.

## Traceability

- **Locked decision:** `D016`

- **User journeys:** `UJ-14`, `UJ-01`, `UJ-02`

- **Cross-cutting NFRs:** `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

## Functional Requirements

### FR-121 — Architecture-preservation gate

**Requirement:** Implementation authorization shall require a passing machine-readable preservation check against the validated Builder, Content Harness, and VAE authority boundaries.

**Testable consequences:**

- Conflicts block authorization.

- Amendment routes are documented.

**Failure examples:**

- A protocol service acquires creative ranking authority.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-122 — Decision and requirements completeness

**Requirement:** All 16 decisions, FRs, NFRs, non-goals, traceability, glossary, assumptions, and success metrics shall be complete and mechanically validated.

**Testable consequences:**

- No orphan requirement remains.

- Open blockers are explicit.

**Failure examples:**

- Implementation starts from conversation notes only.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-123 — Shared contract-family gate

**Requirement:** All required message schemas, examples, owners, versions, and registry entries shall validate before authorization.

**Testable consequences:**

- Representative positive and negative fixtures exist.

- Provisional contracts are marked accurately.

**Failure examples:**

- The result-acknowledgement contract is designed during coding.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-124 — Authority and lifecycle executable proof

**Requirement:** The Authority Matrix and Lifecycle Machine shall be executable and pass prohibited-action and illegal-transition tests.

**Testable consequences:**

- Field-level authority is covered.

- Every exceptional path has a terminal or recovery route.

**Failure examples:**

- Authority exists only as prose.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-125 — Compatibility and integrity proof

**Requirement:** At least one reference Content Harness and VAE compatibility manifest, negotiation, adapter, migration, signature, replay, and audit-chain path shall pass.

**Testable consequences:**

- Pinned versions are demonstrated.

- Failure cases are included.

**Failure examples:**

- Only same-version unsigned fixtures are tested.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-126 — Format 02 cross-product fixture readiness

**Requirement:** The Minimal Coach Theatre reference slice shall provide the complete scenario portfolio and valid contracts needed by both products.

**Testable consequences:**

- Fixtures use real Visual Syntax and character/scene roles.

- Set-level and replacement flows are included.

**Failure examples:**

- Reference fixtures are generic stock-image examples.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-127 — Development Capsule completeness

**Requirement:** The package shall define the required approved PRD, Architecture/ADRs, schemas, matrices, lifecycle, taxonomy, fixtures, conformance suite, deployment, observability, migration, rollback, epics, stories, specs, and authorization receipt.

**Testable consequences:**

- Each artifact traces to requirements.

- Implementation teams do not invent shared semantics.

**Failure examples:**

- A repository scaffold is delivered without authority or compatibility artifacts.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-128 — Staged certification states

**Requirement:** The protocol shall progress through PRD approval, Architecture, contract validation, cross-product fixtures, passing conformance, implementation authorization, Format 02 certification, and production certification.

**Testable consequences:**

- No state is skipped silently.

- Certification scope and limitations are explicit.

**Failure examples:**

- One successful request is labeled production-certified.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

## Feature failure conditions

- Implementation authorized without complete contract family.

- Protocol changes frozen architectures.

- Certification scope overstated.

## Explicitly out of scope

- Implementing final products

- Certifying non-Format02 categories in Release 1
