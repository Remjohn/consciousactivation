---
title: F01 — Governed Product Lifecycle and Run Constitution
product: CMF Atomic Harness Builder Next
version: 0.3.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F01
governing_decisions:
- D001
- D002
- D004
- D006
- D025
- D027
- D033
user_journeys:
- UJ-01
- UJ-04
- UJ-09
- UJ-11
- UJ-12
functional_requirement_count: 8
---

# F01 — Governed Product Lifecycle and Run Constitution

**User outcome:** A Harness Architect can create, resume, inspect, and govern a compilation run whose target, lifecycle, authority, and legal transitions are explicit.

## Description

This feature turns the Builder from a collection of commands into a governed compiler product. It establishes the run as a versioned constitutional object rather than an informal agent session.

## Brownfield baseline

V2.1 already initializes runs, resolves sources, tracks a decision graph, supports guided and provisional modes, compiles OpenSpec, and issues readiness results. Its lifecycle is valuable but does not yet govern all new IR, category, skill, benchmark, observability, and downstream-certification states.

## Required product delta

Extend the working lifecycle into a target-profiled state machine with explicit events, waivers, resumability, constitutional boundaries, and downstream certification feedback.

## Traceability

- **Decisions:** D001, D002, D004, D006, D025, D027, D033
- **User journeys:** UJ-01, UJ-04, UJ-09, UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-TRACE-002, NFR-OBS-001

## Functional Requirements

### FR-001 — Select one explicit compilation target

**Requirement:** The Builder must require each run to select exactly one target profile: Atomic Content Harness, Visual Asset Editor, or Content↔Asset Delegation Contract.

**Consequences (testable):**

- Initialization fails when no target or multiple targets are supplied.
- The selected profile governs required sources, phases, decisions, artifacts, evaluations, and authorization gates.

**Traceability:** Decisions D004, D006; journeys UJ-01.

### FR-002 — Create a stable run identity

**Requirement:** The Builder must create a stable run identifier, target identifier, compiler version binding, operator identity, timestamps, and status before any evidence work begins.

**Consequences (testable):**

- All events and artifacts reference the same run identifier.
- A resumed run preserves identity rather than creating a hidden replacement run.

**Traceability:** Decisions D005, D025; journeys UJ-01.

### FR-003 — Enforce a typed lifecycle state machine

**Requirement:** The Builder must represent the approved lifecycle as typed states and transitions whose prerequisites, actors, outputs, and terminal conditions are machine-validated.

**Consequences (testable):**

- A transition cannot occur when its declared prerequisites are incomplete.
- Illegal transitions produce a blocking event and do not mutate authoritative state.

**Traceability:** Decisions D006, D027; journeys UJ-01, UJ-09.

### FR-004 — Apply target-specific lifecycle profiles

**Requirement:** The shared top-level lifecycle must delegate internal phases, decision nodes, artifacts, and gates to the selected target profile without flattening target-specific behavior.

**Consequences (testable):**

- The three targets can share lifecycle names while producing different required work.
- A target profile cannot omit a shared constitutional stage without an approved waiver.

**Traceability:** Decisions D004, D006; journeys UJ-01.

### FR-005 — Govern lifecycle waivers

**Requirement:** The Builder must support explicit human-authorized lifecycle waivers that state the skipped obligation, rationale, risk, affected decisions, downstream provisional states, and expiration condition.

**Consequences (testable):**

- A waiver generates a receipt and appears in the Control Tower.
- A waiver cannot convert a blocked production gate into full authorization unless the target profile permits that exact waiver class.

**Traceability:** Decisions D002, D006, D027; journeys UJ-09.

### FR-006 — Emit an event for every authoritative transition

**Requirement:** Every state transition, blocker, waiver, decision, invalidation, repair, authorization, and certification update must append a typed event to the Run Ledger.

**Consequences (testable):**

- The current run state can be reconstructed from the IR snapshot plus ledger events.
- No UI-only state change is accepted as authoritative.

**Traceability:** Decisions D025; journeys UJ-09.

### FR-007 — Resume without replaying human decisions

**Requirement:** The Builder must resume an interrupted run from its latest valid checkpoint while preserving ratified decisions, evidence locks, event history, and outstanding actions.

**Consequences (testable):**

- A resumed run does not ask already resolved Genesis questions unless their dependencies were invalidated.
- Corrupted or incompatible checkpoints block with a diagnostic rather than silently resetting.

**Traceability:** Decisions D010, D025; journeys UJ-04.

### FR-008 — Enforce the Builder product boundary

**Requirement:** The lifecycle must prevent the Builder from silently crossing from harness-development compilation into final production-harness implementation.

**Consequences (testable):**

- Generated production logic is rejected unless it is explicitly authorized prototype scaffolding or a deterministic compiler-owned mechanism.
- The Development Capsule records implementation scope and exclusions.

**Traceability:** Decisions D001, D029, D033; journeys UJ-11.

## Known failure and edge conditions

- A target profile is selected after evidence has already been interpreted.
- A lifecycle stage is skipped without a waiver receipt.
- The UI reports progress that is absent from the ledger.
- A resumed run loses or silently rewrites a ratified decision.

## Explicitly out of scope

- Implementing the final content, asset, or delegation runtime.
- General-purpose project management outside the three target profiles.
- Technology selection for storage, queues, or deployment; these belong to Architecture.
