---
title: F05 — Dependency-Driven Genesis and Human Authority
product: CMF Atomic Harness Builder Next
version: 0.3.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F05
governing_decisions:
- D002
- D009
- D010
- D011
- D019
- D025
- D027
- D028
user_journeys:
- UJ-04
- UJ-09
- UJ-11
functional_requirement_count: 10
---

# F05 — Dependency-Driven Genesis and Human Authority

**User outcome:** A Harness Architect can resolve the harness constitution through one evidence-backed decision at a time, resume safely, and see downstream consequences.

## Description

Genesis is the human-governed constitutional compiler. It transforms the unratified Draft Harness Model into an authorized Harness IR through typed decisions rather than an unstructured interview or fixed universal questionnaire.

## Brownfield baseline

V2.1 already has decision definitions, dependency graphs, guided and YOLO modes, ratification, status, and cascade locking. The next Builder must bind decisions directly to IR nodes, evidence, invalidation, category profiles, skills, benchmarks, and authorization.

## Required product delta

Retain the working decision engine while formalizing decision schemas, one-question facilitation, typed effects, contradiction reopening, authority transitions, and Control Tower inspection.

## Traceability

- **Decisions:** D002, D009, D010, D011, D019, D025, D027, D028
- **User journeys:** UJ-04, UJ-09, UJ-11
- **Cross-cutting NFRs:** NFR-REL-002, NFR-TRACE-002, NFR-TRACE-004, NFR-UX-002, NFR-OBS-002

## Functional Requirements

### FR-041 — Define typed Genesis decision nodes

**Requirement:** Every Genesis choice must declare a stable decision ID, target-profile applicability, question, rationale, required evidence, dependencies, options, recommendation policy, authority owner, affected IR paths, invalidation edges, and completion rule.

**Consequences (testable):**

- Decision nodes validate before they enter a run.
- The same decision definition can be versioned without rewriting prior run history.

**Traceability:** Decisions D010, D011; journeys UJ-04.

### FR-042 — Unlock only dependency-ready decisions

**Requirement:** The decision engine must expose a node only when its prerequisite evidence, authority, contracts, and earlier decisions are satisfied.

**Consequences (testable):**

- An operator cannot accidentally answer a decision whose meaning depends on unresolved upstream choices.
- Blocked dependencies are visible with required actions.

**Traceability:** Decisions D010, D019; journeys UJ-04, UJ-09.

### FR-043 — Ask one primary constitutional question per turn

**Requirement:** Guided Genesis must present and resolve one primary decision at a time, keeping any clarification inside that decision before advancing.

**Consequences (testable):**

- The run ledger records one decision outcome per completed turn.
- The agent does not batch unrelated constitutional questions into a single approval request.

**Traceability:** Decisions D010; journeys UJ-04.

### FR-044 — Present an evidence-backed recommendation

**Requirement:** For each decision, the agent must summarize relevant evidence, current Draft Harness Model state, viable alternatives, trade-offs, downstream consequences, and a clear recommended option.

**Consequences (testable):**

- Recommendations cite stable evidence and decision references.
- The recommendation distinguishes facts from inference and does not imply human ratification.

**Traceability:** Decisions D002, D010; journeys UJ-04.

### FR-045 — Record human answer and final decision separately

**Requirement:** The Builder must preserve the operator's answer, agent interpretation, final normalized decision, rationale, authority, timestamp, and any dissent or uncertainty.

**Consequences (testable):**

- A later audit can reconstruct what the human actually said and what was written into the IR.
- Ambiguous answers remain unresolved until normalized and confirmed.

**Traceability:** Decisions D002, D010; journeys UJ-04.

### FR-046 — Update the Harness IR transactionally

**Requirement:** Completing a decision must update all declared IR fields, append a decision event, recompute dependencies, and either commit all effects or none.

**Consequences (testable):**

- Partial decision writes cannot leave the IR inconsistent.
- Generated documents are marked stale until their affected views are recompiled.

**Traceability:** Decisions D010, D011; journeys UJ-04.

### FR-047 — Reopen affected decisions on contradiction

**Requirement:** When new evidence or a later decision conflicts with a resolved node, the Builder must identify the contradiction, reopen the affected node and descendants, and preserve the prior decision as superseded history.

**Consequences (testable):**

- No contradiction is resolved by silently overwriting a ratified value.
- The Control Tower shows the reopening cause and blast radius.

**Traceability:** Decisions D010, D026; journeys UJ-04, UJ-09.

### FR-048 — Support provisional autonomous drafting with ratification

**Requirement:** The Builder may generate provisional decisions in an approved autonomous draft mode, but every required constitutional decision must be ratified before full authorization.

**Consequences (testable):**

- Provisional decisions carry a distinct authority status.
- The ratification list identifies the exact evidence, recommendation, and downstream fields for each pending decision.

**Traceability:** Decisions D002, D010, D027; journeys UJ-04.

### FR-049 — Define a cascade-locked terminal state

**Requirement:** Genesis must reach a terminal state only when all required decisions are resolved, all mandatory IR fields have sufficient authority, no blocking contradiction remains, and all provisional decisions requiring ratification are closed.

**Consequences (testable):**

- Cascade lock is computed, not declared by the agent.
- A later invalidation moves the run out of cascade-locked status.

**Traceability:** Decisions D010, D027; journeys UJ-04.

### FR-050 — Persist complete decision receipts and resumable memory

**Requirement:** The Builder must generate a decision register, per-decision receipts, dependency graph snapshot, and append-only memory sufficient to resume or audit Genesis without loading the full conversation.

**Consequences (testable):**

- A resumed run reconstructs current authority from structured state.
- Conversation prose may support audit but is not the sole memory mechanism.

**Traceability:** Decisions D010, D025; journeys UJ-04.

## Known failure and edge conditions

- A fixed questionnaire asks irrelevant questions while missing category-specific decisions.
- The agent presents several dependent decisions in one approval.
- A later contradiction overwrites history.
- Cascade lock is issued while required provisional decisions remain.

## Explicitly out of scope

- Replacing the human authority owner for constitutional decisions.
- Using Genesis to implement production code.
- Treating agent recommendations as ratification.
