---
title: F10 — Delegation Sets, Shared Continuity, Dependencies, and Group Evaluation
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F10
decision_id: D010
---


# F10 — Delegation Sets, Shared Continuity, Dependencies, and Group Evaluation

## User outcome

Related assets can be produced independently while preserving scene-level identity, continuity, geometry, and completion guarantees.

## Product behavior

A Delegation Set coordinates member demands, shared constraints, dependency edges, completion policy, assembled evaluation, cancellation, and selective invalidation.

## Brownfield baseline

The VAE PRD supports multi-asset composition and immutable asset lineage. Format 02 requires characters, backgrounds, props, and overlays to work together.

## Required product delta

Define a shared set contract without merging member demands or lifecycles.

## Traceability

- **Locked decision:** `D010`

- **User journeys:** `UJ-09`, `UJ-04`, `UJ-12`

- **Cross-cutting NFRs:** `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

## Functional Requirements

### FR-073 — Typed Delegation Set

**Requirement:** The Content Harness shall be able to create an immutable versioned Delegation Set referencing independently versioned member demands.

**Testable consequences:**

- Every member retains its own correlation and asset lineage.

- The set has a stable owner and context.

**Failure examples:**

- One giant demand embeds all assets as mutable children.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-074 — Member lifecycle independence

**Requirement:** Each member shall retain independent submission, execution, evaluation, repair, result, and acknowledgement state.

**Testable consequences:**

- One failed prop does not erase an accepted background.

- Set status is derived from member states and policy.

**Failure examples:**

- All members share one undifferentiated status.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-075 — Shared constraint authority

**Requirement:** The set may define identity, environment, palette, lighting, camera axis, scale, world state, and Visual Syntax constraints that members may refine but not contradict.

**Testable consequences:**

- Contradictions produce a typed set conflict.

- Shared constraints cite their authority source.

**Failure examples:**

- Two characters use incompatible lighting without a conflict.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-076 — Typed dependency edges

**Requirement:** The set shall express directional relationships such as lighting reference, interaction geometry, identity continuity, or ordered production.

**Testable consequences:**

- Dependency changes drive selective invalidation.

- Cycles are detected or explicitly supported.

**Failure examples:**

- A character relies on a prop geometry that is not declared.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-077 — Completion policies

**Requirement:** The set shall support independent, partial_allowed, atomic_required, and ordered_release policies with required-role definitions.

**Testable consequences:**

- Consumption behavior is deterministic.

- The policy is fixed by the Content Harness.

**Failure examples:**

- The VAE decides to return a partial set because one asset is hard.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-078 — Set-level composition evaluation

**Requirement:** Required members shall be assembled in a composition simulation and evaluated for cross-asset consistency and Activative effectiveness where policy requires.

**Testable consequences:**

- Individual passes cannot hide group interaction failure.

- The set evaluation emits a typed receipt.

**Failure examples:**

- A hand and prop each pass separately but never align in composition.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-079 — Set-level selective invalidation

**Requirement:** A changed or failed member shall invalidate only dependent members and set evaluations supported by the dependency graph.

**Testable consequences:**

- Unrelated accepted members remain valid.

- A shared palette change can invalidate all affected members.

**Failure examples:**

- Any member update restarts the entire set.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-080 — Set cancellation and supersession

**Requirement:** The protocol shall support cancelling or superseding one member, optional members, or the complete set according to completion policy.

**Testable consequences:**

- Remaining members' consumability is recomputed.

- Every action is authority-validated.

**Failure examples:**

- Cancelling an optional overlay cancels a completed character asset.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

## Feature failure conditions

- Set erases member lineage.

- Shared constraints conflict silently.

- Individual passes bypass required assembled evaluation.

## Explicitly out of scope

- VAE internal asset batch scheduling

- Final scene composition runtime
