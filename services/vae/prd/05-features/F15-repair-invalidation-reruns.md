---
title: F15 — Typed Visual Repair, Invalidation, and Bounded Reruns
product: CMF Visual Asset Editor
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F15
governing_decisions:
- D002
- D013
- D017
- D018
- D020
- D024
user_journeys:
- UJ-07
- UJ-08
- UJ-10
- UJ-12
functional_requirement_count: 8
---


# F15 — Typed Visual Repair, Invalidation, and Bounded Reruns

**User outcome:** A failed candidate can be corrected surgically while identity, composition, environment, and other successful properties remain stable.

## Description

The VLM emits causal repair contracts; the runtime changes only permitted bindings and reruns the smallest invalidated graph region.

## Brownfield baseline

V2.1 includes repair doctrine and amendment requests; the new product needs concrete failure ownership across generation controls, deterministic edits, workflows, models, evaluation, and demand conflicts.

## Required product delta

Define failure taxonomy, repair contracts, preservation, mutable/prohibited bindings, invalidation, repair hierarchy, three-round policy, causal-change proof, learning, and escalation.

## Traceability

- **Decisions:** D002, D013, D017, D018, D020, D024
- **User journeys:** UJ-07, UJ-08, UJ-10, UJ-12
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005

## Functional Requirements

### FR-113 — Emit a typed repair contract for every quality rerun

**Requirement:** The evaluator must identify failure code, severity, evidence region/time range, responsible layer, preserved properties, permitted and prohibited changes, invalidated nodes, reusable outputs, expected correction evidence, and repair round.

**Consequences (testable):

- The runtime can validate the repair before applying it.

- Free-form 'try again' instructions cannot trigger a quality rerun.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-114 — Preserve successful properties explicitly

**Requirement:** Repair plans must freeze all accepted identities, expressions, geometry, palette, environment, text-safe regions, continuity, and semantic properties not responsible for the failure.

**Consequences (testable):

- Post-repair evaluation compares preserved properties with the parent candidate.

- A repair that fixes one failure by drifting a preserved property is rejected.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-115 — Apply the least disruptive repair hierarchy

**Requirement:** The system must prefer deterministic correction, then parameter correction, conditioning correction, workflow/capability substitution, and finally approved resolution-strategy amendment according to the failure and plan.

**Consequences (testable):

- The selected level and rejected lower levels are receipted.

- A full regeneration cannot be the default when a deterministic or local repair can resolve the issue.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-116 — Require causal production changes

**Requirement:** Every quality rerun must modify at least one binding or execution route plausibly responsible for the diagnosed failure, except evaluator-authorized stochastic seed exploration.

**Consequences (testable):

- The repair receipt records old and new values and causal hypothesis.

- Repeated identical bindings with only an unexplained new seed fail the blind-retry guard.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-117 — Rerun only invalidated nodes

**Requirement:** The Repair and Invalidation Graph must preserve valid references, masks, controls, background plates, runtime bindings, and deterministic transformations while rescheduling affected production and evaluation nodes.

**Consequences (testable):

- Repair cost and time reflect the reduced graph region.

- Unrelated expensive stages cannot be replayed without dependency invalidation.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-118 — Enforce three quality-repair rounds

**Requirement:** The system may perform at most three VLM-directed quality rounds: local correction, strengthened/substituted controls, and approved fallback route or strategy.

**Consequences (testable):

- Round exhaustion emits HUMAN_REVIEW_REQUIRED or CAPABILITY_GAP with the best evidence and attempts.

- A fourth autonomous quality round is constitutionally blocked.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-119 — Separate repair from demand amendment

**Requirement:** Repairs may use only mutable plan bindings and internal production alternatives authorized by the accepted demand; semantic or out-of-tolerance changes must become amendment proposals.

**Consequences (testable):

- The repair validator rejects prohibited field changes.

- An evaluator cannot lower a quality threshold to declare its repair successful.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

### FR-120 — Capture repair effectiveness for steering and regression

**Requirement:** Every repair must record failure context, syntax role, changed bindings, cost, latency, outcome, preserved-property regressions, and candidate/evaluator versions for later Steering Recipe and registry analysis.

**Consequences (testable):

- Repeated failure patterns can trigger routing warnings or capability-gap proposals.

- Learning evidence cannot directly mutate production defaults.

**Traceability:** Decisions D002, D013, D017, D018, D020, D024; journeys UJ-07, UJ-08, UJ-10, UJ-12.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
