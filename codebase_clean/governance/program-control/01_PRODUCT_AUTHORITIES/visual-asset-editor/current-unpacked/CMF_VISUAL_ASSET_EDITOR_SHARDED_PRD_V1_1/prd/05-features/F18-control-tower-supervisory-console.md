---
title: F18 — Control Tower Specialization and Supervisory Console
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F18
governing_decisions:
- D002
- D014
- D019
- D020
- D021
- D022
- D023
- D024
user_journeys:
- UJ-05
- UJ-06
- UJ-07
- UJ-08
- UJ-09
- UJ-12
- UJ-16
functional_requirement_count: 8
---


# F18 — Control Tower Specialization and Supervisory Console

**User outcome:** An operator can understand and govern every autonomous production run without becoming a manual editor or trusting an opaque black box.

## Description

The existing event-sourced Harness Control Tower remains the platform architecture; this feature defines Visual Asset Editor views, controls, exception packages, and analytics.

## Brownfield baseline

The validated Builder PRD already establishes evidence-backed statuses, events, receipts, phase/contract views, and human actions. The Visual Editor adds GPU, candidate, asset, memory, and evaluation projections.

## Required product delta

Define demand/plan/run dashboards, candidate/evaluation viewers, lineage, syntax-context recurrence, compute operations, Budget Program menu, exceptions, policies, accessibility, and cross-run analytics.

## Traceability

- **Decisions:** D002, D014, D019, D020, D021, D022, D023, D024
- **User journeys:** UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16
- **Cross-cutting NFRs:** NFR-COST-001, NFR-COST-002, NFR-COST-003, NFR-COST-004, NFR-COST-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-UX-001, NFR-UX-002, NFR-UX-003, NFR-UX-004, NFR-UX-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-137 — Render a live Visual Asset Demand overview

**Requirement:** The Control Tower must show caller, demand version, harness/category/profile, asset role, Activative function, composition intent, selected Budget Program, current state, blockers, expected cost/latency, and next authorized action.

**Consequences (testable):

- Every displayed value links to its authoritative contract or event.

- The dashboard cannot infer or edit demand authority from UI-only state.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-138 — Visualize the Visual Production Plan and node graph

**Requirement:** Operators must inspect stages, dependencies, actor/executor, capabilities, bindings, status, checkpoints, invalidation, retries, runtime placement, and events.

**Consequences (testable):

- The graph distinguishes infrastructure and quality paths.

- An opaque 'generating' spinner is insufficient for production observability.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-139 — Compare candidates and evaluation evidence

**Requirement:** The console must support side-by-side candidate, composition render, score, hard-gate, evidence region/time range, failure code, recurrence, cost, and repair comparison.

**Consequences (testable):

- The selected asset and rejected alternatives retain reasons.

- The operator is not required to manually approve passing routine candidates.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-140 — Expose asset lineage and usage context

**Requirement:** Operators must navigate from accepted assets to references, candidates, repairs, master, delivery variants, geometry, prior and current syntax contexts, usage receipts, recurrence verdicts, and supersession.

**Consequences (testable):

- Published and in-progress consumers are distinguishable.

- A lineage view may not omit rejected or repaired branches needed for audit.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-141 — Expose compute, queue, and worker health

**Requirement:** The console must show queued/running jobs, runtime profile, GPU class, model cache, worker heartbeat, timeout, retries, failover, cost, and capacity conditions.

**Consequences (testable):

- Operational failures can be diagnosed without logging into the ComfyUI worker desktop.

- Secrets and unrestricted worker shell access are not exposed through standard views.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-142 — Provide policy-first operator controls

**Requirement:** Authorized users must select Budget Program, production priority, experimental policy, cost/time ceilings, post-failure behavior, cancellation, and capability-development authorization through governed controls.

**Consequences (testable):

- Actions are validated against caller scope and generate receipts.

- Routine controls do not include manual seed, prompt, LoRA-strength, or node editing.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-143 — Present typed human-exception packages

**Requirement:** After authorized escalation, the UI must show trigger, best candidate, passing and failing dimensions, attempted repairs, cost, preserved state, recommended choices, consequences, and downstream authority owner.

**Consequences (testable):

- The chosen response creates a typed event or new demand/plan version.

- An operator cannot silently override a constitutional hard gate from a generic approve button.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

### FR-144 — Provide cross-run quality and operations analytics

**Requirement:** The Control Tower must report completion, first-pass acceptance, repair rounds, human exceptions, failure codes, recurrence judgments, route/workflow/model performance, cost, latency, capability gaps, and benchmark drift by asset family and syntax context.

**Consequences (testable):

- Metrics can drive governed learning proposals and regression investigation.

- Analytics cannot update production registry policy without the promotion process.

**Traceability:** Decisions D002, D014, D019, D020, D021, D022, D023, D024; journeys UJ-05, UJ-06, UJ-07, UJ-08, UJ-09, UJ-12, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
