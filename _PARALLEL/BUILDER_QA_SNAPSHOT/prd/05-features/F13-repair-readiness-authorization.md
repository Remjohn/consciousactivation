---
title: F13 — Repair, Invalidation, Readiness, and Implementation Authorization
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F13
governing_decisions:
- D003
- D019
- D021
- D024
- D025
- D026
- D027
- D033
user_journeys:
- UJ-09
- UJ-10
- UJ-11
- UJ-12
functional_requirement_count: 10
---

# F13 — Repair, Invalidation, Readiness, and Implementation Authorization

**User outcome:** A reviewer can resolve failures at the smallest responsible layer and authorize only the exact implementation scope supported by evidence, architecture, skill maturity, benchmarks, and human decisions.

## Description

This feature separates failure diagnosis, repair, readiness, and authorization. It prevents whole-run resets, symptom patches, false completion, and implementation that outruns its evidence.

## Brownfield baseline

V2.1 produces readiness receipts and supports non-PASS states. The next Builder must connect every failure to typed repair ownership, precise invalidation, targeted regression, prototype-only authorization, and Control Tower evidence.

## Required product delta

Create failure taxonomy, root-cause protocol, Repair and Invalidation Graph, escalation, readiness hard gates, authorization outcomes, prototype charters, and immutable receipts.

## Traceability

- **Decisions:** D003, D019, D021, D024, D025, D026, D027, D033
- **User journeys:** UJ-09, UJ-10, UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-REL-004, NFR-TRACE-003, NFR-EVAL-003, NFR-OBS-002, NFR-SEC-001

## Functional Requirements

### FR-127 — Define a typed failure taxonomy

**Requirement:** The Builder must classify evidence, visual parse, atomicity, authority, contract, module, skill, capsule, benchmark, budget, provider, observability, migration, and downstream implementation failures with stable codes.

**Consequences (testable):**

- Every blocking failure maps to one primary taxonomy entry.
- Unknown failures remain explicit and require triage rather than being forced into an unrelated repair route.

**Traceability:** Decisions D026; journeys UJ-09, UJ-10.

### FR-128 — Require root-cause investigation before repair

**Requirement:** A repair may not be proposed until the Builder records the observed symptom, reproduction or evidence, affected boundary, competing hypotheses, and selected root cause with confidence.

**Consequences (testable):**

- The repair receipt links to the root-cause record.
- Repeated guess-and-patch attempts trigger escalation.

**Traceability:** Decisions D026; journeys UJ-10.

### FR-129 — Compile a Repair and Invalidation Graph

**Requirement:** For each known failure class, the Builder must define the responsible phase or capability, permitted repair fields, frozen state, invalidated descendants, regression suite, escalation conditions, and authority needed.

**Consequences (testable):**

- A repair cannot edit fields outside its permitted scope.
- All declared descendants become stale or invalidated after the repair.

**Traceability:** Decisions D026; journeys UJ-10.

### FR-130 — Preserve unaffected upstream state

**Requirement:** Targeted repairs must retain source locks, measured observations, ratified decisions, contracts, and artifacts that remain supported by evidence.

**Consequences (testable):**

- The repair plan lists preserved and invalidated state before mutation.
- A local rendering defect cannot rewrite Activative policy.

**Traceability:** Decisions D026, D033; journeys UJ-10.

### FR-131 — Rerun targeted regression suites

**Requirement:** After repair, the Builder must rerun all tests and benchmarks required by the repaired capability and every affected descendant, including protected cases where policy permits.

**Consequences (testable):**

- A repair is not complete until required regressions pass or remain visibly blocked.
- Regression scope is derived from dependency impact rather than manually guessed.

**Traceability:** Decisions D021, D026; journeys UJ-10.

### FR-132 — Escalate repeated or constitutional failures

**Requirement:** The Builder must require human review when a repair changes a ratified constitutional decision, broadens the harness boundary, modifies a stable canonical skill, encounters contradictory doctrine, or fails repeatedly beyond the configured threshold.

**Consequences (testable):**

- Escalation freezes further automated repair of the affected scope.
- The Control Tower displays options, evidence, and affected authority.

**Traceability:** Decisions D002, D026; journeys UJ-09, UJ-10.

### FR-133 — Evaluate an evidence-backed readiness gate

**Requirement:** Readiness must validate evidence saturation, atomicity, constitutional authority, Harness IR consistency, phases, contexts, contracts, modules, skill maturity, benchmark results, repair coverage, observability, budgets, and target-specific requirements.

**Consequences (testable):**

- Document completeness alone cannot satisfy readiness.
- Each readiness result lists every passed and failed hard gate.

**Traceability:** Decisions D003, D027; journeys UJ-11.

### FR-134 — Issue typed authorization outcomes

**Requirement:** The Builder must issue AUTHORIZED_FOR_IMPLEMENTATION, AUTHORIZED_FOR_PROTOTYPE_ONLY, NEEDS_RATIFICATION, BLOCKED_EVIDENCE, BLOCKED_SKILL_MATURITY, BLOCKED_BENCHMARK, BLOCKED_ARCHITECTURE, or another target-profiled blocking status.

**Consequences (testable):**

- Only the full authorized state permits production implementation.
- The status is recomputed after invalidation or new evidence.

**Traceability:** Decisions D027; journeys UJ-11.

### FR-135 — Govern prototype-only authorization

**Requirement:** A prototype authorization must define the empirical question, allowed implementation scope, permitted artifacts, provisional decisions, required evidence return, disposal or migration policy, budget, and promotion conditions.

**Consequences (testable):**

- Prototype code cannot be mistaken for authorized production logic.
- Prototype results flow back to the relevant decision, benchmark, or architecture node.

**Traceability:** Decisions D027, D032; journeys UJ-11, UJ-12.

### FR-136 — Generate immutable readiness and authorization receipts

**Requirement:** Every readiness and authorization decision must bind the exact Harness IR, source lock, category and profile versions, skill and benchmark receipts, waivers, compiler version, status, scope, and signatories.

**Consequences (testable):**

- Implementation can verify the capsule and receipt identity before starting.
- A changed dependency invalidates the prior authorization.

**Traceability:** Decisions D021, D027, D029; journeys UJ-11.

## Known failure and edge conditions

- The Builder reruns the full pipeline for a local parse defect.
- A repair changes a ratified decision without reopening Genesis.
- Readiness passes because every file exists.
- Prototype-only work is deployed as production.
- An authorization receipt remains valid after its source IR changes.

## Explicitly out of scope

- Automatically resolving all implementation contradictions without human or architecture review.
- Guaranteeing that an authorized design will never require a governed delta.
- Treating a prototype as a substitute for benchmark certification.
