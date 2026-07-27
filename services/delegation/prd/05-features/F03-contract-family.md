---
title: F03 — Immutable Contract Family and Common Delegation Envelope
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F03
decision_id: D003
---


# F03 — Immutable Contract Family and Common Delegation Envelope

## User outcome

Every cross-product interaction is unambiguous, attributable, versioned, and independently validatable.

## Product behavior

The protocol uses single-purpose immutable payloads wrapped in a common envelope for identity, versions, authority, correlation, causation, integrity, and references.

## Brownfield baseline

VAE PRD contains provisional demand, event, result, conflict, and related schemas, but shared authority belongs to this protocol.

## Required product delta

Create the canonical shared contract family and a message registry with conformance fixtures.

## Traceability

- **Locked decision:** `D003`

- **User journeys:** `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13`

- **Cross-cutting NFRs:** `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

## Functional Requirements

### FR-017 — Common delegation envelope

**Requirement:** Every protocol message shall use a common envelope containing protocol version, message type/version, IDs, sender, recipient, authority scope, timestamps, idempotency, hashes, and payload reference.

**Testable consequences:**

- Envelope validation precedes payload routing.

- All message types share stable correlation semantics.

**Failure examples:**

- One message omits sender authority because it travels on an internal queue.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-018 — Single-purpose immutable payloads

**Requirement:** Each lifecycle action shall use an immutable payload dedicated to one purpose rather than a shared mutable delegation record.

**Testable consequences:**

- Submission and cancellation are separate messages.

- History is reconstructed from messages, not overwritten state.

**Failure examples:**

- A single JSON object is edited by both products.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-019 — Correlation and causation

**Requirement:** Messages shall identify correlation ID and, when caused by another message, causation ID.

**Testable consequences:**

- A complete delegation chain can be traversed.

- Retries remain distinguishable from new actions.

**Failure examples:**

- An amendment response cannot be tied to its proposal.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-020 — Authority-scoped envelope

**Requirement:** The envelope shall declare the authority exercised by the sender, and the boundary shall validate it against the principal registry.

**Testable consequences:**

- Unauthorized action is rejected before payload effects.

- Authority evidence is retained in audit receipts.

**Failure examples:**

- A Content Harness emits a production-acceptance message.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-021 — Reference-and-hash payload transport

**Requirement:** Large or canonical payloads shall be exchanged through stable references plus content hashes rather than duplicated mutable bodies.

**Testable consequences:**

- Recipients verify payload integrity.

- Object storage and contract storage remain decoupled from messaging.

**Failure examples:**

- A video binary is embedded in an event message.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-022 — Independent message versioning

**Requirement:** Protocol, envelope, and payload message types shall be independently versioned under governed compatibility rules.

**Testable consequences:**

- An optional event extension does not force a major protocol version.

- Pinned delegations retain their negotiated versions.

**Failure examples:**

- All contracts inherit the product version number.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-023 — Mandatory semantic-field protection

**Requirement:** Unknown or unsupported mandatory fields shall block compatibility rather than be silently ignored.

**Testable consequences:**

- Required-feature support is negotiated.

- Loss of authority-bearing fields produces INCOMPATIBLE.

**Failure examples:**

- A consumer ignores a required continuity constraint.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-024 — Message Type Registry

**Requirement:** The protocol shall maintain a canonical registry for message names, schemas, owners, lifecycle effects, idempotency behavior, and compatibility status.

**Testable consequences:**

- Every schema in the package has a registry entry.

- Deprecated types list replacements and timelines.

**Failure examples:**

- A new cancellation variant is deployed without registry metadata.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

## Feature failure conditions

- Mutable cross-product record.

- Uncorrelated messages.

- Unknown mandatory semantics ignored.

## Explicitly out of scope

- Transport-specific implementation details

- Internal product event schemas not crossing the boundary
