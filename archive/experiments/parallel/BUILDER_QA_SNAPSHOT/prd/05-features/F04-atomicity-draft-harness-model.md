---
title: F04 — Atomicity Classification and Draft Harness Model
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F04
governing_decisions:
- D008
- D009
- D010
- D011
- D030
- D031
- D033
user_journeys:
- UJ-03
- UJ-04
- UJ-06
functional_requirement_count: 9
---

# F04 — Atomicity Classification and Draft Harness Model

**User outcome:** A Harness Architect can approve one evidence-backed product boundary and receive a coherent provisional model for Genesis.

## Description

This feature prevents both one-workspace-per-example duplication and premature universal engines. It converts visual, temporal, semantic, runtime, evaluation, and repair evidence into an explicit atomicity decision.

## Brownfield baseline

V2.1 supports atomicity statuses and the prior Builder bundle contains atomicity doctrine. The current system does not yet consume a full Visual Syntax IR, quantify wrong-boundary consequences, or compile the complete Draft Harness Model from one typed source.

## Required product delta

Add a typed atomicity classifier, comparative evidence packets, human ratification, and a provisional Harness IR projection that Genesis can challenge.

## Traceability

- **Decisions:** D008, D009, D010, D011, D030, D031, D033
- **User journeys:** UJ-03, UJ-04, UJ-06
- **Cross-cutting NFRs:** NFR-TRACE-001, NFR-TRACE-004, NFR-CAT-001, NFR-CAT-002, NFR-EVAL-003

## Functional Requirements

### FR-032 — Compare candidate product boundaries

**Requirement:** The Builder must compare specimens or candidate groups across production promise, persistent visual instrument, composition grammar, state machine, semantic workcell, input contract, asset program, runtime ownership, evaluation failures, and repair behavior.

**Consequences (testable):**

- The comparison exposes shared and materially different dimensions.
- Topic, labels, aspect ratio, or folder names alone cannot decide the boundary.

**Traceability:** Decisions D008; journeys UJ-03.

### FR-033 — Assign one typed atomicity status

**Requirement:** Each candidate must receive exactly one status: atomic_harness_candidate, variant_of_existing, dish_family_candidate, format_family_only, needs_clustering, needs_partition, or insufficient_evidence.

**Consequences (testable):**

- The status is schema-validated and evidence-linked.
- A non-atomic status blocks Harness Genesis for that candidate boundary.

**Traceability:** Decisions D008; journeys UJ-03.

### FR-034 — Explain merge and split recommendations

**Requirement:** For every proposed merge or split, the Builder must state what is shared, what differs, whether configuration is sufficient, which evidence supports the conclusion, and which capability or state would break under the alternative.

**Consequences (testable):**

- A merge explains why one runtime and evaluator can safely generate all members.
- A split explains the material grammar, sequencing, runtime, or failure difference.

**Traceability:** Decisions D008, D033; journeys UJ-03.

### FR-035 — Assess wrong-boundary risk

**Requirement:** The Builder must describe the likely implementation, creative, evaluation, migration, and maintenance consequences if the proposed atomicity decision is wrong.

**Consequences (testable):**

- The risk record distinguishes over-splitting from over-merging.
- High-risk uncertainty requires more evidence or a prototype-only path.

**Traceability:** Decisions D008, D027; journeys UJ-03.

### FR-036 — Require human atomicity ratification

**Requirement:** A human Harness Architect must approve, revise, or reject the proposed product boundary before the Builder compiles a Genesis-ready model.

**Consequences (testable):**

- Ratification records the chosen boundary, rejected alternatives, evidence, and rationale.
- The agent cannot self-ratify an atomicity recommendation.

**Traceability:** Decisions D002, D008; journeys UJ-03.

### FR-037 — Compile a Draft Harness Model

**Requirement:** After atomicity ratification, the Builder must compile a provisional model containing identity, production promise, syntax, composition variables, sequence grammar, draft Activative intelligence, inputs and outputs, capabilities, runtime hypotheses, evaluations, repairs, evidence gaps, and category ownership.

**Consequences (testable):**

- All fields derive from locked evidence or explicit hypotheses in the Harness IR.
- The model is complete enough to generate dependency-ready Genesis questions.

**Traceability:** Decisions D009, D011; journeys UJ-04.

### FR-038 — Mark the Draft Harness Model unratified

**Requirement:** Every constitutional field in the Draft Harness Model must carry authority and knowledge status so provisional hypotheses cannot be mistaken for approved design.

**Consequences (testable):**

- Unratified fields are visibly identified in documents and Control Tower views.
- A downstream compiler cannot consume an unratified field when its contract requires ratified authority.

**Traceability:** Decisions D009, D011; journeys UJ-04.

### FR-039 — Expose gaps, confidence, and alternatives

**Requirement:** The Draft Harness Model must retain unresolved evidence gaps, confidence, alternative hypotheses, and decisions required rather than compressing them into a falsely certain narrative.

**Consequences (testable):**

- Each unresolved item maps to a Genesis node or evidence action.
- Low confidence is not hidden by polished prose.

**Traceability:** Decisions D003, D009; journeys UJ-04.

### FR-040 — Freeze the ratified boundary for Genesis

**Requirement:** Genesis may challenge downstream constitutional fields but may not broaden, merge, or split the approved harness boundary without reopening the atomicity decision and invalidating affected work.

**Consequences (testable):**

- Boundary changes follow a formal invalidation event.
- A Genesis answer cannot silently turn an atomic harness into a category-level engine.

**Traceability:** Decisions D008, D010, D033; journeys UJ-04.

## Known failure and edge conditions

- A folder name becomes the harness identity without comparison.
- Two grammars are merged because their topics match.
- The Draft Harness Model presents hypotheses as final decisions.
- Genesis silently broadens the atomic scope.

## Explicitly out of scope

- Implementing the atomic harness.
- Certifying generality beyond the compared specimens.
- Creating category-level abstractions before repeated harness evidence exists.
