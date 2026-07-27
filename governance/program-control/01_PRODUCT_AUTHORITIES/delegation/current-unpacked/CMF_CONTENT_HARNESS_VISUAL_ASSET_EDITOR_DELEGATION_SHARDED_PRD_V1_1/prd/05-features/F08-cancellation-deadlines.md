---
title: F08 — Cancellation, Deadlines, Safe Checkpointing, and Race Resolution
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F08
decision_id: D008
---


# F08 — Cancellation, Deadlines, Safe Checkpointing, and Race Resolution

## User outcome

Obsolete delegated work stops safely, preserves valuable evidence, and cannot produce a stale consumable result.

## Product behavior

The Content Harness authoritatively requests cancellation; the protocol orders races; the VAE stops at a safe boundary and returns a disposition receipt.

## Brownfield baseline

The VAE PRD defines resumable node graphs and immutable artifacts, but cross-product cancellation remains shared protocol behavior.

## Required product delta

Specify request/receipt contracts, deadline policies, disposition classes, and deterministic ordering.

## Traceability

- **Locked decision:** `D008`

- **User journeys:** `UJ-08`, `UJ-05`

- **Cross-cutting NFRs:** `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

## Functional Requirements

### FR-057 — Cancellation authority

**Requirement:** The owning Content Harness or authorized operator policy shall be able to request cancellation of a delegation or permitted Delegation Set scope.

**Testable consequences:**

- Authority is validated before state change.

- Unauthorized cancellation is rejected.

**Failure examples:**

- An unrelated harness cancels a GPU job.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-058 — Block new work on acceptance

**Requirement:** Once a valid cancellation is accepted, the VAE shall stop scheduling new production and candidate-expansion nodes for the affected scope.

**Testable consequences:**

- Queued jobs are cancelled where safe.

- The shared state becomes CANCELLATION_REQUESTED.

**Failure examples:**

- The system continues Exploration candidates after cancellation.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-059 — Nearest safe checkpoint

**Requirement:** In-flight work shall stop at the nearest safe atomic boundary according to the declared stop policy.

**Testable consequences:**

- Partial files are not promoted.

- Atomic completion under a small remaining-time threshold may be allowed.

**Failure examples:**

- A container is killed mid-write and corrupts shared storage.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-060 — Artifact disposition classification

**Requirement:** The cancellation receipt shall classify accepted assets, candidates, references, masks, geometry, learning evidence, caches, and incomplete artifacts.

**Testable consequences:**

- Reusable evidence can enter governed memory.

- Cancelled outputs are not consumption-authorized.

**Failure examples:**

- All files are deleted, including a validated identity mask.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-061 — Deadline policy semantics

**Requirement:** The protocol shall distinguish target completion, hard cutoff, and expiry, with explicit behavior for each.

**Testable consequences:**

- Soft misses notify but do not mutate quality gates.

- Expiry can trigger cancellation.

**Failure examples:**

- Every deadline miss destroys the run.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-062 — Deterministic race ordering

**Requirement:** Cancellation, supersession, result readiness, and acknowledgement races shall resolve from accepted message order, causation, and precedence rules.

**Testable consequences:**

- A valid supersession outranks ordinary cancellation when specified.

- A result emitted after cancellation cannot be promoted.

**Failure examples:**

- Whichever network response arrives first wins.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-063 — Stale-promotion prevention

**Requirement:** A cancelled delegation shall prohibit downstream consumption authorization for subsequently produced outputs under that correlation.

**Testable consequences:**

- Historical candidates remain traceable.

- A new demand may reuse them only through explicit validation.

**Failure examples:**

- A late VAE result is acknowledged because it passed quality.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-064 — Cancellation and compute receipt

**Requirement:** Terminal cancellation shall report stopped execution, last checkpoint, retained artifacts, consumed/avoided cost, and downstream authorization state.

**Testable consequences:**

- The Control Tower projection closes cleanly.

- Receipts support operational review.

**Failure examples:**

- Cancellation is represented only as an HTTP 204.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

## Feature failure conditions

- Unsafe hard kill.

- Late stale asset promoted.

- Cancellation loses evidence and compute accountability.

## Explicitly out of scope

- Internal GPU cancellation primitives

- User-facing content-project deletion
