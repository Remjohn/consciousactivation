---
title: F10 — Event-Sourced, Resumable Visual Production Runtime
product: CMF Visual Asset Editor
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F10
governing_decisions:
- D013
- D015
- D017
- D018
- D019
- D021
- D023
- D027
user_journeys:
- UJ-02
- UJ-05
- UJ-07
- UJ-08
- UJ-14
functional_requirement_count: 8
---


# F10 — Event-Sourced, Resumable Visual Production Runtime

**User outcome:** A long-running visual job can execute, fail, recover, repair, and complete without losing state or replaying unrelated expensive work.

## Description

The runtime specializes the validated Builder Workflow Runtime for visual production and separates deterministic, model, VLM, compute, delivery, and human-exception nodes.

## Brownfield baseline

V2.1 has deterministic CLI lifecycle and receipts; the new editor requires asynchronous GPU jobs, production graphs, queueing, checkpoints, events, and infrastructure recovery.

## Required product delta

Define node schema, scheduler, events, checkpoint/resume, infrastructure/quality separation, timeouts, retries, cancellation, parallelism, isolation, and terminal states.

## Traceability

- **Decisions:** D013, D015, D017, D018, D019, D021, D023, D027
- **User journeys:** UJ-02, UJ-05, UJ-07, UJ-08, UJ-14
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-PERF-001, NFR-PERF-002, NFR-PERF-003, NFR-PERF-004, NFR-PERF-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-COMPUTE-001, NFR-COMPUTE-002, NFR-COMPUTE-003, NFR-COMPUTE-004, NFR-COMPUTE-005, NFR-WORKFLOW-001, NFR-WORKFLOW-002, NFR-WORKFLOW-003, NFR-WORKFLOW-004, NFR-WORKFLOW-005

## Functional Requirements

### FR-073 — Execute typed production nodes

**Requirement:** Every runtime node must declare actor type, inputs, outputs, dependencies, validations, timeout, infrastructure retries, checkpoint behavior, invalidation, event types, and eligible runtime profiles.

**Consequences (testable):

- The scheduler refuses incomplete node definitions.

- An opaque long-running job without typed stages is outside certified scope.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-074 — Persist an append-only production event stream

**Requirement:** The runtime must emit ordered typed events for plan compilation, queueing, node start/completion/failure, candidate creation, evaluation, repair, promotion, packaging, cancellation, and exceptions.

**Consequences (testable):

- Run state can be reconstructed from authoritative events plus immutable artifacts.

- A UI-only status change without an event is invalid.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-075 — Checkpoint successful nodes

**Requirement:** Committed node inputs, outputs, bindings, validation receipts, side effects, and dependency versions must be checkpointed for resume and targeted repair.

**Consequences (testable):

- An interrupted run resumes from the first invalid or incomplete node.

- Successful retrieval, control preparation, or deterministic transforms are not repeated without invalidation.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-076 — Separate infrastructure retries from quality repairs

**Requirement:** Container crashes, GPU loss, network timeout, cache corruption, or provider unavailability must use operational retry/fallback policies independent of the three VLM-directed quality rounds.

**Consequences (testable):

- Receipts report infrastructure attempts and quality rounds separately.

- An infrastructure failure cannot consume or reset the quality-repair count.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-077 — Enforce bounded timeouts, retries, and circuit breakers

**Requirement:** Each node/profile must declare timeout, retryable and non-retryable failures, maximum operational attempts, backoff, fallback, and circuit-breaker behavior.

**Consequences (testable):

- Exhaustion produces a typed terminal or exception state with preserved evidence.

- The runtime cannot loop indefinitely on an unavailable provider or recurring error.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-078 — Run dependency-safe bounded parallelism

**Requirement:** The scheduler may parallelize independent input preparation, candidate production, evaluation, or delivery work only within Budget Program concurrency and shared-resource constraints.

**Consequences (testable):

- Cancellation and failure of one branch do not corrupt valid siblings.

- Parallel nodes with shared mutable state are rejected unless an explicit merge protocol exists.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-079 — Support governed cancellation and backpressure

**Requirement:** Authorized callers may cancel non-promoted work; the service may communicate capacity, queue, and estimated-delay states without lowering quality gates.

**Consequences (testable):

- Cancellation preserves events, created artifacts, learning evidence, and cost receipts.

- Backpressure cannot silently switch to uncertified or degraded production.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

### FR-080 — Define explicit terminal states

**Requirement:** Runs must end in COMPLETED, INVALID_DEMAND, CAPABILITY_GAP, COST_APPROVAL_REQUIRED, HUMAN_REVIEW_REQUIRED, DEPENDENCY_UNAVAILABLE, PRODUCTION_FAILED, CANCELLED, or another registered terminal state.

**Consequences (testable):

- Every terminal state has required evidence, owner, and allowed next action.

- A stalled run cannot remain indefinitely in a nonterminal status without heartbeat or escalation.

**Traceability:** Decisions D013, D015, D017, D018, D019, D021, D023, D027; journeys UJ-02, UJ-05, UJ-07, UJ-08, UJ-14.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
