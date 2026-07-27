---
title: F14 — Principal Identity, Message Integrity, Replay Protection, and Audit Chain
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F14
decision_id: D014
---


# F14 — Principal Identity, Message Integrity, Replay Protection, and Audit Chain

## User outcome

Only authorized systems can create state changes, and every accepted action can be verified and reconstructed.

## Product behavior

The protocol registers principals and scopes, verifies signatures/hashes/nonces/expiry, distinguishes idempotent retry from replay, minimizes payloads, and emits append-only chained receipts.

## Brownfield baseline

Both upstream PRDs require receipts, hashes, provenance, and event sourcing, but the shared trust model is not yet canonical.

## Required product delta

Define principal registry, integrity envelope, validation order, replay rules, audit chain, and security incidents.

## Traceability

- **Locked decision:** `D014`

- **User journeys:** `UJ-13`, `UJ-01`, `UJ-14`

- **Cross-cutting NFRs:** `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

## Functional Requirements

### FR-105 — Registered delegation principals

**Requirement:** Every state-changing sender and recipient shall be a registered principal with product type, version, permitted actions, prohibited actions, credential reference, and status.

**Testable consequences:**

- Inactive principals are rejected.

- Scope can be evaluated deterministically.

**Failure examples:**

- Any internal service account can submit demands.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-106 — Message signing and hashing

**Requirement:** State-changing messages shall include verifiable envelope/payload hashes and an authenticated signature or equivalent architecture-approved integrity proof.

**Testable consequences:**

- Tampering is detected before state mutation.

- Signing identity is in the audit receipt.

**Failure examples:**

- Payload hash is optional on the internal queue.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-107 — Replay protection

**Requirement:** The protocol shall use message ID, nonce, expiry, idempotency key, payload hash, correlation, and lifecycle context to distinguish benign retries from replay.

**Testable consequences:**

- A retry returns the existing receipt.

- A replay produces a security failure.

**Failure examples:**

- The same signed cancellation is accepted twice in different states.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-108 — Deterministic validation order

**Requirement:** Boundary services shall verify identity, integrity, replay/expiry, protocol compatibility, schema, authority, and lifecycle before persistence or routing.

**Testable consequences:**

- Failure stage is receipted.

- No later validation can compensate for an earlier failure.

**Failure examples:**

- Schema-valid forged messages change state before signature verification.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-109 — Append-only audit chain

**Requirement:** Every accepted or rejected state-changing message shall create an append-only audit receipt with sequence, previous hash, validations, and resulting transition.

**Testable consequences:**

- A chain can detect gaps or reordering.

- Projection can be reconstructed.

**Failure examples:**

- Audit is a mutable table with deleted rejection rows.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-110 — Data minimization

**Requirement:** Messages shall carry only required contractual data and stable references/hashes, excluding secrets, large media, unnecessary prompts, weights, and private traces.

**Testable consequences:**

- Recipients retrieve authorized resources separately.

- Payload policies are testable.

**Failure examples:**

- A ComfyUI prompt history and model credential are embedded in an event.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-111 — Credential lifecycle

**Requirement:** Architecture shall support principal credential issuance, rotation, revocation, and overlap without invalidating historical signature verification.

**Testable consequences:**

- Rotation events are audited.

- Compromised principals can be disabled.

**Failure examples:**

- Rotating a key makes old audit receipts unverifiable.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-112 — Security-incident behavior

**Requirement:** Identity, integrity, replay, or isolation violations shall block state change, preserve forensic metadata, and emit a typed incident outside ordinary repair flows.

**Testable consequences:**

- No automatic production retry occurs.

- Control Tower escalates severity.

**Failure examples:**

- A signature failure is treated as a transient provider timeout.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

## Feature failure conditions

- Unsigned message changes state.

- Retry confused with replay.

- Audit chain has gaps or mutable history.

## Explicitly out of scope

- Organization-wide IAM platform

- Encryption implementation details reserved for Architecture
