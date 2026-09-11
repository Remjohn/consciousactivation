---
title: F09 — Visual Production Plan IR and Provider-Specific Compilation
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F09
governing_decisions:
- D003
- D005
- D009
- D011
- D012
- D013
- D018
- D019
- D024
user_journeys:
- UJ-01
- UJ-02
- UJ-03
- UJ-07
- UJ-12
functional_requirement_count: 8
---


# F09 — Visual Production Plan IR and Provider-Specific Compilation

**User outcome:** A validated demand becomes one inspectable, provider-neutral execution specification before ComfyUI or any other provider receives work.

## Description

The Visual Production Plan IR is the canonical production plan, while provider graphs and API payloads are compiled artifacts.

## Brownfield baseline

V2.1 defines asset demand and resolution concepts, but not a canonical plan that separates product authority from ComfyUI graph structure.

## Required product delta

Define plan identity, objectives, route stages, capability requirements, constraints, preservation/mutability, evaluation, budget, fallbacks, provider compilation, and plan versioning.

## Traceability

- **Decisions:** D003, D005, D009, D011, D012, D013, D018, D019, D024
- **User journeys:** UJ-01, UJ-02, UJ-03, UJ-07, UJ-12
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-065 — Compile every accepted demand into a Visual Production Plan

**Requirement:** Before provider execution, the service must create a schema-valid, versioned plan referencing the exact demand, objective, route, stages, inputs, outputs, capabilities, budgets, evaluations, fallbacks, and delivery requirements.

**Consequences (testable):

- Every execution node traces to one plan node and one authoritative need.

- Direct demand-to-ComfyUI execution without a canonical plan is prohibited.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-066 — Declare preservation and mutable bindings

**Requirement:** The plan must separate fields and properties that must be preserved from provider bindings, candidate variables, and repair variables that may change.

**Consequences (testable):

- Repair validation can prove no protected property was altered.

- A binding not declared mutable cannot be changed by generation or repair.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-067 — Model typed stages and dependencies

**Requirement:** Plan stages must declare actor/executor class, dependencies, contracts, checkpoints, expected artifacts, validators, invalidation, and eligible parallelism.

**Consequences (testable):

- The plan graph validator identifies orphan outputs, unavailable capabilities, illegal cycles, and unsatisfied dependencies.

- A stage lacking an output contract cannot unlock downstream work.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-068 — Express capability requirements provider-neutrally

**Requirement:** Plans must request functions such as identity conditioning, pose control, regional conditioning, inpainting, transparent extraction, or temporal consistency rather than hard-code ComfyUI node IDs as product requirements.

**Consequences (testable):

- Capability resolution can bind a different certified provider without changing plan meaning.

- Provider-specific terminology cannot become the sole canonical representation.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-069 — Compile deterministic provider graphs

**Requirement:** A versioned compiler must bind approved workflows, models, LoRAs, controls, runtimes, parameters, inputs, and output paths into ComfyUI JSON or another provider payload.

**Consequences (testable):

- The provider artifact includes a source plan hash and compiler version.

- Manual runtime graph editing invalidates the compiled identity unless captured as a new governed profile.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-070 — Compile evaluation and repair subgraphs

**Requirement:** The plan compiler must generate the required deterministic validation, VLM evaluation, composition simulation, recurrence/continuity comparison, repair, and delivery nodes alongside production.

**Consequences (testable):

- The execution graph contains every acceptance hard gate before promotion.

- A production graph that omits the applicable evaluator cannot be certified.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-071 — Version and amend plans without mutating demands

**Requirement:** Internal route, workflow, model, control, or runtime changes permitted by the demand create a new plan version with reason and impact while preserving the demand version.

**Consequences (testable):

- Valid prior outputs are reused when dependency analysis allows.

- Demand-authority changes cannot be disguised as plan revisions.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

### FR-072 — Preserve plan-to-execution reproducibility

**Requirement:** The service must retain the plan, compiled graphs, compiler identities, bindings, input hashes, events, outputs, and receipts needed to reproduce or audit the run.

**Consequences (testable):

- A dry-run can validate plan capability and budget without GPU execution.

- An accepted asset whose executed graph cannot be reconciled with its plan fails traceability.

**Traceability:** Decisions D003, D005, D009, D011, D012, D013, D018, D019, D024; journeys UJ-01, UJ-02, UJ-03, UJ-07, UJ-12.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
