---
title: F15 — Traceable Development Capsule and Implementation Handoff
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F15
governing_decisions:
- D001
- D003
- D011
- D015
- D021
- D027
- D029
- D032
user_journeys:
- UJ-11
- UJ-12
functional_requirement_count: 9
---

# F15 — Traceable Development Capsule and Implementation Handoff

**User outcome:** An implementation team receives the smallest complete package needed to build the authorized harness without inventing architecture or carrying speculative boilerplate.

## Description

This feature materializes the Builder product promise. It packages the Harness IR and compiled views with contracts, skills, graphs, justified scaffolding, fixtures, vertical-slice stories, authorization, and traceability.

## Brownfield baseline

V2.1 compiles an OpenSpec package and readiness receipt, while the parallel workspaces provide empty implementation directories. The next Builder must generate an integrated, traceable capsule whose scaffolding is justified by approved responsibilities and whose stories are implementation-ready.

## Required product delta

Define capsule structure, artifact provenance, interface stubs, test assets, dependency-ordered vertical stories, implementation-delta handling, and downstream telemetry return.

## Traceability

- **Decisions:** D001, D003, D011, D015, D021, D027, D029, D032
- **User journeys:** UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-TRACE-001, NFR-TRACE-003, NFR-TEST-001, NFR-PORT-001, NFR-MAINT-001

## Functional Requirements

### FR-151 — Generate a versioned Development Capsule

**Requirement:** The Builder must package authorization, Harness IR, readable specifications, contracts, skill bindings and adaptations, runtime graphs, module manifests, tests, implementation planning, and observability configuration into one versioned handoff.

**Consequences (testable):**

- The capsule manifest lists every file, hash, source IR node, and authorization status.
- The package validates independently after export.

**Traceability:** Decisions D029; journeys UJ-11.

### FR-152 — Maintain requirement-to-artifact traceability

**Requirement:** Every generated contract, module, skill, test, story, and dashboard element must map to governing decisions, FRs or NFRs, and Harness IR nodes.

**Consequences (testable):**

- The implementation team can navigate from an acceptance criterion to its source doctrine and contract.
- Unmapped generated artifacts fail capsule validation.

**Traceability:** Decisions D011, D029; journeys UJ-11.

### FR-153 — Generate only justified scaffolding

**Requirement:** The Builder may create schema classes, interface stubs, module shells, manifests, fixtures, and configuration only when an approved IR responsibility, contract, test seam, or runtime need justifies them.

**Consequences (testable):**

- Speculative generic services and placeholder business logic are excluded.
- Every scaffold records the IR node that requires it.

**Traceability:** Decisions D001, D015, D029, D033; journeys UJ-11.

### FR-154 — Provide typed interfaces and contract examples

**Requirement:** The capsule must include machine-validatable schemas or interface definitions, positive examples, negative examples, version compatibility rules, and producer-consumer mappings for each required contract.

**Consequences (testable):**

- Examples validate against the same schema shipped to implementation.
- Breaking changes are visible and governed.

**Traceability:** Decisions D014, D029; journeys UJ-11.

### FR-155 — Provide executable test and benchmark fixtures

**Requirement:** The capsule must include contract, unit-seam, behavioral, integration, golden, adversarial, and benchmark fixtures required by the authorized implementation scope.

**Consequences (testable):**

- The first vertical slice can run meaningful tests without inventing datasets.
- Protected benchmark labels are excluded or accessed through their governed mechanism.

**Traceability:** Decisions D021, D023, D029; journeys UJ-11.

### FR-156 — Generate dependency-ordered vertical stories

**Requirement:** The implementation plan must decompose authorized scope into stories that deliver complete testable behavior, fit one development-agent context, use only previous-story dependencies, and map to FRs, NFRs, contracts, modules, and acceptance criteria.

**Consequences (testable):**

- Stories are not organized as database, API, and UI horizontal layers.
- Every FR is covered by at least one story before readiness.

**Traceability:** Decisions D029, D032; journeys UJ-11.

### FR-157 — Define a first working vertical-slice plan

**Requirement:** The capsule must identify the narrowest end-to-end reference path that proves evidence, one core transformation, one format projection, evaluation, observability, and targeted repair for the selected reference harness.

**Consequences (testable):**

- The path produces a demonstrable output and receipts.
- It does not require future stories to function.

**Traceability:** Decisions D022, D032; journeys UJ-11, UJ-12.

### FR-158 — Govern implementation-discovered deltas

**Requirement:** When implementation reveals a genuine contradiction or missing decision, the team must create a typed delta linked to the affected IR nodes rather than silently altering constitutional or creative policy in code.

**Consequences (testable):**

- The delta identifies whether PRD, Architecture, Harness IR, skill, contract, or benchmark must change.
- Affected authorization is suspended or scoped until the delta is resolved.

**Traceability:** Decisions D010, D026, D029; journeys UJ-11.

### FR-159 — Ingest implementation and certification feedback

**Requirement:** The Builder must accept structured implementation questions, delta outcomes, tests, defects, runtime metrics, repair history, and certification evidence and link them to the Builder and capsule versions that caused them.

**Consequences (testable):**

- Feedback updates benchmark and migration evidence through governed events.
- Stable doctrine is not batch-rewritten without failure-local analysis.

**Traceability:** Decisions D003, D022, D028, D029; journeys UJ-11, UJ-12.

## Known failure and edge conditions

- The capsule contains empty directories with no approved purpose.
- A story requires a future story to become testable.
- Implementation changes the production promise directly in code.
- A generated interface has no requirement or contract trace.
- The capsule's authorization hash does not match its IR.

## Explicitly out of scope

- Writing all production implementation code.
- Selecting the team's git-hosting or deployment workflow.
- Providing protected benchmark answers directly in the package.
