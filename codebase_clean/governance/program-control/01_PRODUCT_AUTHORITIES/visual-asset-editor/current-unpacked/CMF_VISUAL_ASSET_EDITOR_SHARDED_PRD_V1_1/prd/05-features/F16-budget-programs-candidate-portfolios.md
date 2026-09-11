---
title: F16 — Budget Programs, Candidate Portfolios, and Quality-First Selection
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F16
governing_decisions:
- D002
- D019
- D020
- D021
- D022
- D025
user_journeys:
- UJ-02
- UJ-05
- UJ-06
- UJ-10
functional_requirement_count: 8
---


# F16 — Budget Programs, Candidate Portfolios, and Quality-First Selection

**User outcome:** Operators and callers can choose how much exploration, learning, cost, and latency a demand receives without weakening quality authority.

## Description

Budget Programs configure candidate counts, parallelism, repair limits, workflow variation, evaluator depth, experimentation, and cost/time ceilings.

## Brownfield baseline

The current architecture has cost profiles but not a product-level menu connecting compute budgets to candidate portfolio design and controlled learning.

## Required product delta

Define six programs, custom policies, estimates, portfolio classes, controlled variation, quality-first selection, early stop, adaptive expansion, cost receipts, and authorization.

## Traceability

- **Decisions:** D002, D019, D020, D021, D022, D025
- **User journeys:** UJ-02, UJ-05, UJ-06, UJ-10
- **Cross-cutting NFRs:** NFR-PERF-001, NFR-PERF-002, NFR-PERF-003, NFR-PERF-004, NFR-PERF-005, NFR-COST-001, NFR-COST-002, NFR-COST-003, NFR-COST-004, NFR-COST-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-COMPUTE-001, NFR-COMPUTE-002, NFR-COMPUTE-003, NFR-COMPUTE-004, NFR-COMPUTE-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-121 — Register six Budget Programs

**Requirement:** The product must define Lean, Standard, Premium, Exploration, Capability Learning, and Custom programs with candidate, parallelism, workflow diversity, evaluator, repair, time, cost, and learning semantics.

**Consequences (testable):

- Each run pins one program version in its plan and receipt.

- A raw GPU setting without program semantics cannot be selected as the primary policy.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-122 — Expose program selection in the supervisory menu

**Requirement:** Authorized operators and callers must be able to select an eligible Budget Program and see expected cost, latency, candidate count, evaluator depth, experimental scope, and learning outputs before execution.

**Consequences (testable):

- The UI distinguishes production and learning budgets.

- High-cost or experimental programs require the caller authority defined by policy.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-123 — Compile bounded candidate portfolios

**Requirement:** Each plan must declare initial and maximum candidates, maximum parallel jobs, exploration dimensions, fixed properties, candidate classes, selection policy, and budget ceilings.

**Consequences (testable):

- The scheduler cannot exceed portfolio or Budget Program limits.

- Candidate generation without declared purpose or limit is prohibited.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-124 — Use controlled variation for exploration

**Requirement:** Exploration and Capability Learning portfolios must vary declared factors while preserving comparable baselines, fixed variables, hypothesis, and measurement plan.

**Consequences (testable):

- The system can attribute quality differences to tested interventions.

- Indiscriminate random prompt/seed sweeps do not qualify as learning evidence.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-125 — Filter hard-gate failures before ranking

**Requirement:** Every candidate must pass technical, semantic, Activative, composition, and applicable continuity/temporal hard gates before quality/cost/latency ranking.

**Consequences (testable):

- Ineligible candidates remain available for diagnosis but cannot win.

- The first completed candidate or highest aesthetic score cannot override failed gates.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-126 — Select the best validated candidate within budget

**Requirement:** Among eligible candidates, the selector must use the registered ranking profile across fidelity, effectiveness, continuity, distinctiveness, technical quality, editability, repair risk, cost, and latency.

**Consequences (testable):

- The selected candidate and credible alternatives are receipted.

- Completion speed is only a declared constraint or tie-breaker, never the sole winner criterion.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-127 — Support adaptive expansion and early stopping

**Requirement:** The portfolio may expand when evidence shows valuable unresolved uncertainty and may stop when a passing candidate exceeds high-confidence thresholds and further expected value is low.

**Consequences (testable):

- Expansion and early stop decisions include evaluator evidence and remaining budget.

- The system cannot exhaust a high budget automatically when a strong accepted asset already exists.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

### FR-128 — Emit complete budget and portfolio receipts

**Requirement:** Each run must report estimated versus actual cost/time, GPU seconds, candidates created/evaluated/passing, parallelism, repairs, early stopping, selected asset, and learning artifacts.

**Consequences (testable):

- Operators can compare quality gain per additional cost across programs.

- Hidden candidate or evaluator cost fails cost-governance validation.

**Traceability:** Decisions D002, D019, D020, D021, D022, D025; journeys UJ-02, UJ-05, UJ-06, UJ-10.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
