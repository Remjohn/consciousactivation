---
title: F02 — Visual Asset Demand Contract, Intake, and Authority Validation
product: CMF Visual Asset Editor
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F02
governing_decisions:
- D003
- D009
- D019
- D023
- D024
- D027
- D028
user_journeys:
- UJ-01
- UJ-03
- UJ-12
- UJ-14
functional_requirement_count: 8
---


# F02 — Visual Asset Demand Contract, Intake, and Authority Validation

**User outcome:** A Content Harness can submit one immutable, typed demand that gives the editor enough authority and constraints to produce the correct asset without relying on conversational context.

## Description

The Visual Asset Demand is the provider-neutral semantic and production boundary between the requesting harness and the editor.

## Brownfield baseline

V2.1 defines an immutable Activative Visual Asset Program and delegation principles, but the new product needs a concrete asynchronous intake, validation, authority, idempotency, and versioning model.

## Required product delta

Define the canonical demand contract, optional notes policy, validation gates, caller registration, immutable versions, references to large media, execution policies, and blocker behavior.

## Traceability

- **Decisions:** D003, D009, D019, D023, D024, D027, D028
- **User journeys:** UJ-01, UJ-03, UJ-12, UJ-14
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-009 — Require a typed Visual Asset Demand

**Requirement:** Every production request must reference a schema-valid, versioned Visual Asset Demand containing asset family, harness role, Activative function, semantic intent, composition intent, continuity, wrong-reading locks, delivery, evaluation, and execution-policy fields applicable to the request.

**Consequences (testable):

- Contract validation can enumerate every missing or invalid field before plan compilation.

- Natural-language-only requests are rejected with INVALID_DEMAND.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-010 — Treat notes as non-authoritative enrichment

**Requirement:** Optional notes may explain preferences or context but must be tagged as untrusted enrichment and cannot override typed fields, hard gates, budgets, or authority.

**Consequences (testable):

- A conflict detector reports notes that contradict the typed demand and preserves the typed value.

- A note containing prompt-like instructions cannot alter workflow, tool, or evaluator policy.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-011 — Version demands immutably

**Requirement:** Once accepted for execution, a Visual Asset Demand version is immutable; material changes require a new version with supersession and amendment provenance.

**Consequences (testable):

- Each execution pins one exact demand version and retains it after completion.

- In-place edits to an accepted demand fail contract-authority validation.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-012 — Validate caller identity and delegation authority

**Requirement:** Only registered Content Harnesses, orchestration systems, or authorized operators may submit, cancel, choose high-cost programs, enable experimental capability, accept degradation, or request capability development.

**Consequences (testable):

- Submission receipts record caller identity, scope, and permitted actions.

- An unauthorized action returns a typed authorization failure without starting production.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-013 — Use idempotent submission keys

**Requirement:** The asynchronous service must require or derive an idempotency key from caller, harness, request ID, and demand version.

**Consequences (testable):

- Repeated identical submissions return the existing execution record rather than duplicating GPU work.

- A changed demand with a reused key is rejected as an idempotency conflict.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-014 — Reference large inputs by stable URI and hash

**Requirement:** Images, videos, masks, character references, composition renders, and other large inputs must remain in governed storage and enter contracts through versioned references and content hashes.

**Consequences (testable):

- The intake validator proves referenced objects exist, are readable, and match declared hashes.

- Embedded unbounded media payloads or hash mismatches block acceptance.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-015 — Return a typed submission receipt

**Requirement:** A valid submission must immediately return execution identity, accepted demand version, Budget Program, initial status, estimate class, status resource, and event endpoint information.

**Consequences (testable):

- The caller can begin observing a run without waiting for GPU completion.

- An HTTP success without a durable execution and receipt is nonconformant.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

### FR-016 — Block unresolved authority and dependency gaps

**Requirement:** Intake or pre-plan validation must identify missing upstream authority, unavailable required references, unsupported category/profile combinations, and contradictory hard constraints before production resources are committed.

**Consequences (testable):

- The service emits a typed blocker with responsible owner and next action.

- The system may not invent missing semantic or composition values to make a demand executable.

**Traceability:** Decisions D003, D009, D019, D023, D024, D027, D028; journeys UJ-01, UJ-03, UJ-12, UJ-14.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
