---
title: F01 — Product Constitution, Semantic Sovereignty, and Autonomous Authority
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F01
governing_decisions:
- D001
- D002
- D004
- D010
- D028
user_journeys:
- UJ-01
- UJ-02
- UJ-05
- UJ-16
functional_requirement_count: 8
---


# F01 — Product Constitution, Semantic Sovereignty, and Autonomous Authority

**User outcome:** A registered caller can rely on an autonomous editor that resolves production without rewriting the caller’s authorized meaning.

## Description

The product constitution fixes the editor’s production promise, authority boundary, operator role, three quality gates, and exception-only human intervention.

## Brownfield baseline

V2.1 already defines semantic sovereignty, the immutable Activative Visual Asset Program, reference/production separation, geometry return, and independent editor versioning, but assumes a heavier seven-lane workcell and rights layer.

## Required product delta

Preserve the validated upstream architecture while making routine production autonomous, removing the standalone Rights Analyst, and expressing semantic non-mutation, human exceptions, and layered success as enforceable product requirements.

## Traceability

- **Decisions:** D001, D002, D004, D010, D028
- **User journeys:** UJ-01, UJ-02, UJ-05, UJ-16
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-UX-001, NFR-UX-002, NFR-UX-003, NFR-UX-004, NFR-UX-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-001 — Enforce the complete visual asset-resolution promise

**Requirement:** The service must accept an authorized Visual Asset Demand and resolve it through any approved combination of reuse, retrieval, extraction, transformation, compositing, deterministic construction, generation, animation, or capture request.

**Consequences (testable):

- A run may select and combine only routes registered as eligible for the requested family, role, and demand.

- A system limited to a single generation or manipulation route fails product-conformance validation.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-002 — Preserve semantic sovereignty

**Requirement:** No production node, specialist, memory result, workflow fallback, evaluator, repair, or operator action may change the authorized semantic intent, Activative function, sequence role, composition role, identity, continuity, or wrong-reading locks in place.

**Consequences (testable):

- Every accepted asset can be traced to unchanged authoritative demand fields or to a newer explicitly authorized demand version.

- Any silent substitution produces a constitutional hard-gate failure and blocks asset promotion.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-003 — Operate autonomously inside authorized boundaries

**Requirement:** Routine demand validation, planning, memory retrieval, capability selection, candidate production, evaluation, repair, promotion, and delivery must execute without manual intervention.

**Consequences (testable):

- A fully passing routine run reaches COMPLETED without an approval click, manual prompt edit, candidate selection, or job restart.

- A workflow that pauses for ordinary operator approval fails the no-routine-manual-work acceptance test.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-004 — Limit human intervention to typed exceptions

**Requirement:** Human review may be requested only for max-repair exhaustion, unauthorized cost, unresolved capability gaps, blocking constraint conflicts, unresolved evaluator contradiction, or explicit degraded-result authority.

**Consequences (testable):

- Every human intervention contains a typed trigger, evidence, attempted repairs, preserved state, choices, and consequences.

- Unstructured requests such as 'please review' without an authorized exception code are rejected.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-005 — Apply three acceptance gates

**Requirement:** An asset is accepted only after production validity, demand fidelity, and intended-composition effectiveness pass their required profiles.

**Consequences (testable):

- The final result receipt contains separate verdicts and evidence for all three gates.

- A high aggregate score cannot compensate for failure in any mandatory gate.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-006 — Separate human authority from production execution

**Requirement:** The operator may govern budgets, production priorities, experimental scope, cost ceilings, exception choices, and capability promotion, but does not normally manipulate ComfyUI graphs or generation parameters.

**Consequences (testable):

- The supervisory console exposes policy and exception controls while normal runs retain autonomous node execution.

- A production path requiring routine node-level operator work is outside certified scope.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-007 — Keep lightweight source provenance without a rights workcell

**Requirement:** Source type, origin reference, allowed-source policy result, generated/retrieved/supplied classification, and transformation lineage must be captured deterministically without a standalone Rights Analyst.

**Consequences (testable):

- Every delivered asset contains provenance metadata sufficient to reconstruct its source class and derivation.

- Missing provenance blocks promotion, but routine production does not enter a manual legal-review lane.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

### FR-008 — Authorize Architecture before implementation

**Requirement:** Approval of this PRD permits Architecture work only; implementation begins after the formal Visual Asset Editor Implementation Authorization Gate passes.

**Consequences (testable):

- The readiness receipt identifies the exact evidence, contracts, reference slice, compute proof, evaluators, benchmarks, and Development Capsule used for authorization.

- A PRD-approved but architecture-unvalidated package cannot receive IMPLEMENTATION_AUTHORIZED.

**Traceability:** Decisions D001, D002, D004, D010, D028; journeys UJ-01, UJ-02, UJ-05, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
