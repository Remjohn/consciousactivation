---
title: F07 — Dynamic Specialist Workcell and Authority Boundaries
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F07
governing_decisions:
- D002
- D010
- D012
- D013
- D017
- D018
- D022
user_journeys:
- UJ-02
- UJ-05
- UJ-07
- UJ-12
functional_requirement_count: 8
---


# F07 — Dynamic Specialist Workcell and Authority Boundaries

**User outcome:** A demand activates only the analysis and production authorities needed for its actual route while preserving isolated evaluation and deterministic command.

## Description

The workcell compiles from explicit authorities rather than one general visual editor agent or one mandatory fixed chain.

## Brownfield baseline

V2.1 defines seven authority lanes including a Rights Analyst. The new design retains the valuable responsibilities, removes the standalone rights layer, adds autonomous command, and makes activation conditional.

## Required product delta

Define authority manifests, activation rules, typed handoffs, the Asset Commander, specialist boundaries, deterministic policy services, independent evaluation, and no hidden orchestration.

## Traceability

- **Decisions:** D002, D010, D012, D013, D017, D018, D022
- **User journeys:** UJ-02, UJ-05, UJ-07, UJ-12
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-049 — Register specialist authorities

**Requirement:** The product must define Asset Intelligence Hunter, Activative Visual Analyst, Composition Feasibility Analyst, Resolution Strategy Composer, Editor/Materializer, Independent Visual Evaluator, and Asset Commander authority manifests.

**Consequences (testable):

- Each manifest declares owned decisions, inputs, outputs, tools, prohibited decisions, maturity, and evaluation profile.

- A specialist cannot act outside its declared authority.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-050 — Compile the smallest sufficient workcell

**Requirement:** The Asset Commander must activate specialists based on demand, route, capability, evaluation, and repair needs rather than run every specialist for every request.

**Consequences (testable):

- A simple crop may skip research and generation; a new character scene activates the required analysis, plan, production, and evaluation authorities.

- Unnecessary specialist activation is visible in cost and workflow tests.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-051 — Keep semantic interpretation bounded

**Requirement:** The Activative Visual Analyst may translate authorized intent into production-facing visible requirements and failure indicators but may not change the demand.

**Consequences (testable):

- Its output traces each production-facing requirement to a demand field.

- A newly invented subject, message, sequence role, or wrong-reading rule is rejected.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-052 — Keep feasibility analysis measurable

**Requirement:** The Composition Feasibility Analyst must output geometry constraints, conflicts, tolerances, supported controls, and evidence rather than aesthetic preference alone.

**Consequences (testable):

- Its result can be validated against simulation or candidate geometry.

- An unsupported qualitative feasibility conclusion cannot block or redirect production.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-053 — Separate strategy from materialization

**Requirement:** The Resolution Strategy Composer owns the typed route and capability plan; Editor/Materializer nodes execute the approved plan and cannot independently redesign it.

**Consequences (testable):

- Execution receipts prove which plan and bindings were materialized.

- Materializer-side changes beyond permitted runtime variation require a plan amendment.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-054 — Use deterministic policy services for source and registry checks

**Requirement:** Source classification, provenance capture, allowed-source policy, registry compatibility, budget enforcement, contract validation, and lifecycle transitions must be code-owned services rather than reasoning-agent lanes.

**Consequences (testable):

- Policy outcomes are reproducible and independently testable.

- No routine Rights Analyst or manual rights queue appears in the certified workcell.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-055 — Keep evaluation independent from production

**Requirement:** The Independent Visual Evaluator must receive the demand, candidate, composition render, relevant context, and profile without production-model self-approval or unnecessary producer reasoning history.

**Consequences (testable):

- Evaluator identity and profile are pinned in the acceptance receipt.

- A candidate approved only by its producing model is ineligible.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

### FR-056 — Make the Asset Commander a workflow authority, not a creative agent

**Requirement:** The Asset Commander controls state, routing, budgets, node validation, evaluation invocation, repair limits, promotion, and escalation but does not perform specialist creative analysis itself.

**Consequences (testable):

- Commander decisions are deterministic or based on typed specialist/evaluator contracts.

- A general-agent Commander that silently combines all roles fails authority-separation tests.

**Traceability:** Decisions D002, D010, D012, D013, D017, D018, D022; journeys UJ-02, UJ-05, UJ-07, UJ-12.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
