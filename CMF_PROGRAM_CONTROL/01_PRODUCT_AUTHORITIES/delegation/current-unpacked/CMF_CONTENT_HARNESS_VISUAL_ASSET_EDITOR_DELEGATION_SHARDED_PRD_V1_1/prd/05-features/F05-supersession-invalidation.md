---
title: F05 — Demand Supersession, Impact Analysis, and Selective Invalidation
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F05
decision_id: D005
---


# F05 — Demand Supersession, Impact Analysis, and Selective Invalidation

## User outcome

An updated demand can replace an in-flight or completed version without discarding unaffected work or promoting stale results.

## Product behavior

The protocol validates explicit supersession and authority-declared change sets; the VAE computes plan-level reuse and invalidation; shared state prevents stale promotion.

## Brownfield baseline

Both upstream PRDs define immutable versioning and repair/invalidation, but their cross-product supersession semantics are provisional.

## Required product delta

Specify change classes, impact receipts, stale-result controls, and resumable handoff behavior.

## Traceability

- **Locked decision:** `D005`

- **User journeys:** `UJ-05`, `UJ-09`, `UJ-12`

- **Cross-cutting NFRs:** `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

## Functional Requirements

### FR-033 — Explicit supersession link

**Requirement:** A new demand version shall explicitly identify the prior version it supersedes and shall be authored by the owning Content Harness.

**Testable consequences:**

- The old version enters SUPERSEDED through a valid message.

- Unlinked replacement submissions are treated as separate demands.

**Failure examples:**

- The same request ID is reused with a new body and no version link.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-034 — Typed changed-field declaration

**Requirement:** The supersession message shall enumerate changed field paths, change classes, and unchanged authority domains.

**Testable consequences:**

- Impact analysis can distinguish meaning, composition, delivery, and execution-policy changes.

- False unchanged declarations are detected against payload diffs.

**Failure examples:**

- A semantic action changes but the message claims 'delivery only'.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-035 — Supersession authority validation

**Requirement:** The boundary shall validate that every changed field is owned by the sender and allowed in a superseding demand.

**Testable consequences:**

- Unauthorized changes are rejected.

- Constitutional changes route upstream.

**Failure examples:**

- A composition runtime changes a wrong-reading lock.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-036 — Selective invalidation request

**Requirement:** The protocol shall request a VAE impact analysis that identifies reusable outputs, invalidated outputs, affected nodes, and safe resume point.

**Testable consequences:**

- The result is typed and linked to the new demand.

- Uncertainty blocks unsafe reuse.

**Failure examples:**

- The protocol itself guesses which ComfyUI nodes can be reused.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-037 — Stale-promotion prevention

**Requirement:** Once supersession is accepted, no asset result produced solely against the old demand may be promoted as satisfying the new version without revalidation.

**Testable consequences:**

- Old results remain historical.

- The lifecycle projection blocks stale acknowledgement.

**Failure examples:**

- An old result arrives late and is automatically consumed.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-038 — Reusable-work preservation

**Requirement:** The protocol shall preserve immutable evidence and VAE-certified reusable outputs that remain valid under the declared change set.

**Testable consequences:**

- Identity references may survive a composition change.

- Preserved artifacts retain original lineage.

**Failure examples:**

- Every new version forces complete asset regeneration.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-039 — Resumable execution correlation

**Requirement:** A resumed execution shall link the prior execution, new demand, invalidation receipt, and new Visual Production Plan version.

**Testable consequences:**

- Audit can explain exactly what was reused.

- Budget accounting distinguishes prior and resumed work.

**Failure examples:**

- A new run silently copies files from the old run.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-040 — Completed-result revalidation

**Requirement:** A completed result affected by supersession shall enter revalidation or replacement handling rather than being deleted or silently retained as current.

**Testable consequences:**

- Downstream consumers receive an invalidation notice.

- Published historical uses remain reproducible.

**Failure examples:**

- A previously consumed asset reference is overwritten.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

## Feature failure conditions

- Stale result promoted against new demand.

- Impact analysis lacks field-level basis.

- Unaffected work discarded without reason.

## Explicitly out of scope

- VAE internal node invalidation algorithm

- Content Harness content-revision workflow
