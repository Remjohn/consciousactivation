---
title: F01 — Governed Protocol Boundary and Deterministic Boundary Services
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F01
decision_id: D001
---


# F01 — Governed Protocol Boundary and Deterministic Boundary Services

## User outcome

Independent products can delegate visual work through an enforced boundary without creating a third creative authority.

## Product behavior

The protocol provides deterministic contract, authority, compatibility, lifecycle, routing, idempotency, and audit services while leaving semantic decisions with the Content Harness and production decisions with the Visual Asset Editor.

## Brownfield baseline

The validated Builder and Visual Asset Editor PRDs already establish three independent compilation targets and prohibit cross-product authority leakage. Their shared boundary remains provisional.

## Required product delta

Formalize the shared boundary as a product-level protocol with explicit owned and prohibited responsibilities.

## Traceability

- **Locked decision:** `D001`

- **User journeys:** `UJ-01`, `UJ-03`, `UJ-14`

- **Cross-cutting NFRs:** `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

## Functional Requirements

### FR-001 — Canonical delegation boundary

**Requirement:** The system shall expose a versioned Delegation Protocol as the sole supported production boundary between registered Content Harnesses and registered Visual Asset Editors.

**Testable consequences:**

- A conformant submission enters through a registered protocol endpoint or transport adapter.

- Direct unvalidated production invocation is rejected and receipted.

**Failure examples:**

- A harness calls a ComfyUI worker directly and bypasses authority validation.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-002 — Deterministic boundary responsibilities

**Requirement:** The protocol shall deterministically perform schema validation, authority validation, compatibility negotiation, idempotency resolution, lifecycle validation, routing, and audit persistence.

**Testable consequences:**

- Each responsibility emits a machine-readable result.

- No model judgment is required for a valid/invalid boundary decision.

**Failure examples:**

- An LLM decides whether an unsupported contract version is acceptable.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-003 — No third creative authority

**Requirement:** The protocol shall not originate, reinterpret, rank, or amend semantic intent, Activative purpose, sequence role, composition intent, or visual-production strategy.

**Testable consequences:**

- Protocol outputs contain only validations, projections, receipts, and routed product messages.

- A creative change is rejected unless authored by the owning product.

**Failure examples:**

- The boundary service rewrites a character action to improve feasibility.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-004 — Independent product preservation

**Requirement:** The protocol shall preserve independent versioning, deployment, state machines, and internal implementation authority for the Content Harness and Visual Asset Editor.

**Testable consequences:**

- Internal VAE node names are not required in the public lifecycle.

- A VAE patch can deploy without a Builder release when contracts remain compatible.

**Failure examples:**

- The shared protocol requires identical product version numbers.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-005 — Canonical shared ABI

**Requirement:** The protocol shall publish a machine-readable registry of every supported message type, version, producer, consumer, and authority scope.

**Testable consequences:**

- Unregistered message types are rejected.

- The registry identifies the canonical schema URI and hash.

**Failure examples:**

- A product invents a new status payload without registration.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-006 — Boundary receipts

**Requirement:** Every accepted or rejected boundary action shall emit an immutable validation or audit receipt linked to the triggering message.

**Testable consequences:**

- The receipt records every performed validation.

- Rejected messages do not mutate lifecycle state.

**Failure examples:**

- A malformed submission is only written to an application log.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-007 — Transport independence

**Requirement:** The protocol shall preserve identical semantics across supported HTTP, queue, event-stream, local-process, and fixture transports.

**Testable consequences:**

- Transport adapters pass the same conformance suite.

- No transport may weaken integrity or authority checks.

**Failure examples:**

- Local file fixtures bypass signature and lifecycle validation in production mode.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-008 — Architecture-preservation enforcement

**Requirement:** The protocol shall evaluate proposed schemas and services against the frozen Builder and Visual Asset Editor Architecture Preservation Contracts.

**Testable consequences:**

- A conflicting change produces an upstream amendment requirement.

- The preservation check is a release hard gate.

**Failure examples:**

- A delegation release locally changes Content Harness semantic authority.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

## Feature failure conditions

- Boundary logic performs creative inference.

- A product bypasses protocol validation.

- Protocol state diverges from authoritative product messages.

## Explicitly out of scope

- Content-generation reasoning

- Visual-production planning

- ComfyUI orchestration

- Final composition authoring
