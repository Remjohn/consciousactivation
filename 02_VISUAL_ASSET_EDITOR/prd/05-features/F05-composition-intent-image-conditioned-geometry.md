---
title: F05 — Composition Intent, Feasibility, and Image-Conditioned Geometry
product: CMF Visual Asset Editor
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F05
governing_decisions:
- D004
- D009
- D012
- D017
- D018
- D024
user_journeys:
- UJ-03
- UJ-04
- UJ-07
- UJ-12
functional_requirement_count: 8
---


# F05 — Composition Intent, Feasibility, and Image-Conditioned Geometry

**User outcome:** A Content Harness can declare where and how an asset must function, and downstream composition receives measured geometry rather than a vague visual suggestion.

## Description

The editor must translate authoritative composition intent into feasible production controls and return image-conditioned geometry without changing the requested syntactic role.

## Brownfield baseline

V2.1 already defines two geometry stages: harness-side BBOX intent plus WHY, followed by editor-side masks, gaze, safe zones, crops, depth, and final BBOX recommendations.

## Required product delta

Formalize Composition Intent, feasibility analysis, tolerance, reserved regions, protected regions, collision simulation, geometry return, conflict handling, and composition-context evaluation.

## Traceability

- **Decisions:** D004, D009, D012, D017, D018, D024
- **User journeys:** UJ-03, UJ-04, UJ-07, UJ-12
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-033 — Require typed Composition Intent

**Requirement:** Applicable demands must declare canvas profile, intended region, tolerance, layer, visual weight, depth, directional constraints, reserved regions, crop policy, protected regions, and background policy.

**Consequences (testable):

- The plan compiler can map each composition requirement to production and evaluation nodes.

- Ambiguous prose such as 'leave room for text' is insufficient when a typed field exists.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-034 — Run composition-feasibility analysis before expensive production

**Requirement:** The system must test whether subject count, camera distance, gesture, gaze, protected regions, text reservations, and intended BBOX can coexist with available capabilities and budget.

**Consequences (testable):

- Blocking conflicts are detected before full candidate generation when simulation can establish infeasibility.

- The system may not consume the full candidate budget for a geometrically impossible plan.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-035 — Compile composition controls from intent

**Requirement:** The production plan must translate composition intent into masks, regional conditioning, pose/depth/edge controls, camera constraints, background extension, transparency, and workflow-specific bindings as supported.

**Consequences (testable):

- Each compiled control traces to one demand field or feasibility result.

- Provider parameters without a governing composition reason are rejected from the canonical binding.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-036 — Return image-conditioned geometry

**Requirement:** Accepted assets must return detected subject, face, hands, gesture, object, and focal BBOXes; gaze or motion vectors; negative-space regions; safe crops; masks; depth/layer data; and collision results as applicable.

**Consequences (testable):

- Downstream composition can validate fit without rerunning the full production model.

- An asset requiring geometry that lacks the applicable geometry pack cannot be authorized for composition.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-037 — Respect composition tolerance

**Requirement:** The editor may adjust geometry only within declared tolerance or through an internal production method that preserves the requested role and function.

**Consequences (testable):

- The result contract records requested versus realized geometry and tolerance consumption.

- A change outside tolerance triggers a demand amendment proposal rather than silent relocation.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-038 — Evaluate assets in rendered composition context

**Requirement:** The evaluation graph must place candidates in the target scene, slide, or frame with text and neighboring elements before composition-effectiveness approval.

**Consequences (testable):

- Evaluation evidence includes the rendered composition hash and detected collisions or hierarchy outcomes.

- Standalone asset quality cannot substitute for composition-context evaluation.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-039 — Generate deterministic delivery geometry variants

**Requirement:** After master acceptance, the system may derive registered crop, mask, transparency, and canvas variants and return each with inherited geometry and fresh profile validation.

**Consequences (testable):

- Delivery variants retain protected regions and focal visibility.

- A crop that removes the required action or subject evidence fails variant authorization.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

### FR-040 — Return typed composition conflicts and recommendations

**Requirement:** When requirements remain infeasible after approved repairs and fallbacks, the system must return conflict evidence and nonbinding geometry or route alternatives to the owning Content Harness.

**Consequences (testable):

- The original demand remains immutable and each option states semantic and Activative impact.

- The editor cannot accept its own out-of-tolerance amendment.

**Traceability:** Decisions D004, D009, D012, D017, D018, D024; journeys UJ-03, UJ-04, UJ-07, UJ-12.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
