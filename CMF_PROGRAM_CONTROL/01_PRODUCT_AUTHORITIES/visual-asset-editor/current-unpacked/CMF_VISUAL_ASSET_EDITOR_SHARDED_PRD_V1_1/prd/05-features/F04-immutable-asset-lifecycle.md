---
title: F04 — Immutable Asset Lifecycle, Lineage, Supersession, and Delivery Variants
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F04
governing_decisions:
- D007
- D008
- D013
- D014
- D017
- D018
- D023
- D027
user_journeys:
- UJ-01
- UJ-04
- UJ-07
- UJ-09
- UJ-14
functional_requirement_count: 8
---


# F04 — Immutable Asset Lifecycle, Lineage, Supersession, and Delivery Variants

**User outcome:** A downstream consumer can always identify the exact accepted master, understand how it was made, and determine whether a newer version supersedes it.

## Description

The asset lifecycle separates reference, planning, candidate, evaluation, repair, acceptance, delivery, consumption, rejection, and supersession states.

## Brownfield baseline

V2.1 defines production asset artifacts, asset memory, usage receipts, and geometry packs. The new system needs an immutable lifecycle across autonomous production and repair.

## Required product delta

Define state transitions, immutable versions, parent/child derivation, master/variant roles, supersession notifications, in-progress invalidation, and historical preservation.

## Traceability

- **Decisions:** D007, D008, D013, D014, D017, D018, D023, D027
- **User journeys:** UJ-01, UJ-04, UJ-07, UJ-09, UJ-14
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005

## Functional Requirements

### FR-025 — Create immutable asset versions

**Requirement:** Every material candidate, repair, composite, accepted master, or meaningfully changed output must receive an immutable asset ID/version and content hash.

**Consequences (testable):

- A version can be reproduced or audited after later repairs and supersession.

- Overwriting asset bytes under an existing accepted version is prohibited.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-026 — Enforce explicit lifecycle transitions

**Requirement:** Asset state changes must follow registered transitions from Reference Evidence or Resolution Planned through Candidate, Evaluation, Accepted Production Asset, Delivery Variant, and Consumed states, with typed failure states.

**Consequences (testable):

- Illegal transitions are rejected and emitted to the Control Tower.

- A rejected candidate cannot jump directly to accepted without new evaluation.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-027 — Record typed derivation relationships

**Requirement:** Every version must declare parents and relationships such as generated-from, extracted-from, transformed-from, composited-from, targeted-repair-of, delivery-variant-of, or supersedes.

**Consequences (testable):

- Lineage traversal reconstructs all sources and production steps.

- An accepted asset with an orphaned material parent fails promotion.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-028 — Separate accepted masters from delivery variants

**Requirement:** The accepted master is the canonical production asset; deterministic crops, codecs, masks, previews, thumbnails, and profile-specific outputs are immutable variants linked to it.

**Consequences (testable):

- Consumers can request a declared variant without changing master identity.

- A variant cannot silently become the new master.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-029 — Notify downstream consumers of supersession

**Requirement:** When a new accepted version supersedes another, in-progress dependent compositions receive an event and revalidation requirement while published content remains bound to its historical version.

**Consequences (testable):

- The system can list all affected in-progress and completed consumers.

- Supersession may not mutate already-published artifacts automatically.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-030 — Preserve evaluation and production receipts by version

**Requirement:** Each asset version must reference its exact plan, workflow, compute, candidate, geometry, evaluator, repair, budget, and acceptance receipts.

**Consequences (testable):

- A reviewer can prove why one version passed and another failed.

- Receipts from a parent version cannot be reused as acceptance evidence for an altered child without revalidation.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-031 — Support deterministic reuse of valid variants

**Requirement:** Repeated requests for an existing valid delivery profile may return the stored immutable variant when source master, profile version, and dependencies are unchanged.

**Consequences (testable):

- Idempotent variant generation avoids duplicate transformations.

- A profile-version change creates and evaluates a new variant rather than overwriting the old one.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

### FR-032 — Expose lifecycle and lineage in the Control Tower

**Requirement:** The supervisory console must render asset state, versions, parents, repairs, accepted master, variants, usage, supersession, and pending invalidations.

**Consequences (testable):

- Operators can navigate from a result contract to every contributing artifact and receipt.

- A lifecycle status shown without authoritative event or record is invalid.

**Traceability:** Decisions D007, D008, D013, D014, D017, D018, D023, D027; journeys UJ-01, UJ-04, UJ-07, UJ-09, UJ-14.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
