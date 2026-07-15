---
title: F06 — Governed Multi-Method Resolution and Strategy Routing
product: CMF Visual Asset Editor
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F06
governing_decisions:
- D005
- D006
- D010
- D011
- D012
- D018
- D019
- D020
user_journeys:
- UJ-01
- UJ-02
- UJ-07
- UJ-09
- UJ-10
functional_requirement_count: 8
---


# F06 — Governed Multi-Method Resolution and Strategy Routing

**User outcome:** A demand is fulfilled through the simplest reliable route or hybrid route rather than being sent indiscriminately to generation.

## Description

The Resolution Strategy Composer chooses among reuse, retrieve, extract, transform, composite, deterministic construction, generate, animate, and request capture.

## Brownfield baseline

V2.1 allows reuse, research, editing, deterministic assets, requested capture, and grounded generation. The new product must make route selection explicit, budget-aware, benchmarked, and repairable.

## Required product delta

Define route eligibility, route planning, hybrid sequencing, route comparison, fallback, source preparation, route-level receipts, and route-learning evidence.

## Traceability

- **Decisions:** D005, D006, D010, D011, D012, D018, D019, D020
- **User journeys:** UJ-01, UJ-02, UJ-07, UJ-09, UJ-10
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-COST-001, NFR-COST-002, NFR-COST-003, NFR-COST-004, NFR-COST-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005

## Functional Requirements

### FR-041 — Register canonical production routes

**Requirement:** The capability registry must define reuse, retrieve, extract, transform, composite, deterministic construction, generate, animate, and request-capture routes with inputs, outputs, eligible families, required capabilities, evaluators, and certification status.

**Consequences (testable):

- The router can validate route eligibility before planning.

- An unregistered route cannot execute in production.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-042 — Select the least complex reliable route

**Requirement:** Strategy selection must rank eligible routes by expected semantic fidelity, Activative effectiveness, composition fit, continuity, feasibility, latency, cost, repairability, and reproducibility.

**Consequences (testable):

- The plan records selected and rejected alternatives with evidence.

- Generation-first selection without comparison fails routing evaluation when a simpler certified route can satisfy the demand.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-043 — Support governed hybrid routes

**Requirement:** A production plan may sequence multiple routes when one route cannot satisfy the demand alone, such as retrieval plus extraction plus transformation plus compositing.

**Consequences (testable):

- Every stage has typed contracts, dependencies, validators, and lineage relationships.

- A hybrid plan cannot hide an unsupported or uncertified stage.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-044 — Prefer governed asset reuse when suitable

**Requirement:** Before acquiring or generating new material, the system must query Visual Asset Memory for semantically, Activatively, compositionally, and continuity-compatible accepted assets and account for contextual recurrence.

**Consequences (testable):

- The reuse decision includes suitability and recurrence evidence.

- Low raw similarity alone cannot exclude a strong syntax-context match, and high similarity alone cannot authorize a poor role match.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-045 — Prepare and validate source/control inputs

**Requirement:** Retrieval, extraction, generation, animation, and compositing routes must normalize references, masks, pose/depth maps, identity inputs, environments, documents, frames, and control assets before downstream execution.

**Consequences (testable):

- Prepared inputs receive hashes, geometry, class, and validation status.

- A production node cannot consume unvalidated or mismatched control inputs.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-046 — Define route-specific fallback policies

**Requirement:** Each route profile must declare fallback routes, compatibility constraints, quality impact, budget impact, and conditions that prohibit fallback.

**Consequences (testable):

- Infrastructure or capability failure can select an approved alternative without changing demand authority.

- A fallback that weakens a hard semantic or composition requirement must return a conflict instead.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-047 — Emit route and strategy receipts

**Requirement:** Every run must preserve route candidates, selected strategy, expected and actual costs, capability bindings, fallbacks used, and reasons for route changes.

**Consequences (testable):

- Control Tower views can explain why a route was chosen and whether it changed during repair.

- An accepted asset without a reconstructable resolution strategy is nonconformant.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

### FR-048 — Learn route effectiveness without self-modifying silently

**Requirement:** Cross-run evidence may update routing statistics and propose Steering Recipes or profile changes only through the governed learning lifecycle.

**Consequences (testable):

- The system can compare expected and realized route performance by family and syntax context.

- One successful or failed run cannot rewrite route defaults automatically.

**Traceability:** Decisions D005, D006, D010, D011, D012, D018, D019, D020; journeys UJ-01, UJ-02, UJ-07, UJ-09, UJ-10.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
