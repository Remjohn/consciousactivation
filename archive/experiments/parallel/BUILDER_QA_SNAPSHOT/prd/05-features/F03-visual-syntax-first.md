---
title: F03 — Visual Syntax First and Draft Activative Understanding
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F03
governing_decisions:
- D003
- D007
- D011
- D012
- D013
- D014
- D030
- D031
user_journeys:
- UJ-02
- UJ-03
- UJ-06
- UJ-09
functional_requirement_count: 13
---

# F03 — Visual Syntax First and Draft Activative Understanding

**User outcome:** A Harness Architect can inspect a provenance-preserving draft of what is visibly and temporally present before the Builder generalizes format grammar or proposes Activative meaning.

## Description

This feature introduces Visual Syntactic Parsing as a mandatory hybrid capability. It separates measured and observed composition from function hypotheses, cross-specimen grammar, sequence hypotheses, and draft Activative intelligence.

## Brownfield baseline

The existing Builder doctrine requires Visual Syntax First and BBOX + WHY, but it does not yet implement a production-grade multimodal parse IR, category-adapted temporal parsing, knowledge-status transitions, or interactive overlays.

## Required product delta

Create deterministic specimen preprocessing, typed multimodal parsing, parsing ontologies, validators, independent evaluators, cross-specimen induction, and selective human correction before atomicity.

## Traceability

- **Decisions:** D003, D007, D011, D012, D013, D014, D030, D031
- **User journeys:** UJ-02, UJ-03, UJ-06, UJ-09
- **Cross-cutting NFRs:** NFR-TRACE-001, NFR-TRACE-004, NFR-EVAL-001, NFR-EVAL-002, NFR-CAT-001

## Functional Requirements

### FR-019 — Normalize every visual specimen

**Requirement:** The Builder must deterministically derive stable specimen and frame or slide identities, canvas metadata, aspect ratios, ordering, hashes, and analysis-ready representations.

**Consequences (testable):**

- Every parse output references a normalized specimen identity.
- Normalization failures remain visible and block complete specimen coverage.

**Traceability:** Decisions D007; journeys UJ-02.

### FR-020 — Detect duplicate and near-duplicate visual evidence

**Requirement:** The Builder must calculate exact duplicate relationships and may propose near-duplicate clusters without discarding provenance.

**Consequences (testable):**

- Exact duplicates are not counted as independent support for an invariant.
- Near-duplicate proposals retain confidence and human-review status.

**Traceability:** Decisions D007, D023; journeys UJ-02.

### FR-021 — Produce a typed specimen-level visual syntactic parse

**Requirement:** For every visual specimen, the Builder must identify major components, regions, containers, overlays, sequence markers, images, text roles, and category-relevant state elements using a typed schema.

**Consequences (testable):**

- Every salient component has a stable component ID and knowledge status.
- Omitted or uncertain components are represented explicitly rather than invented or hidden.

**Traceability:** Decisions D007, D012; journeys UJ-02.

### FR-022 — Use a canonical parsing ontology with category adaptations

**Requirement:** Visual Syntactic Parsing must use a canonical capability ontology extended by the selected category and format profile rather than one universal vision prompt.

**Consequences (testable):**

- Carousel parsing can represent slide roles while 2D Character Animation can represent character states.
- Category vocabulary does not leak into unrelated categories.

**Traceability:** Decisions D030, D031; journeys UJ-02, UJ-06.

### FR-023 — Measure normalized component geometry

**Requirement:** Every major spatial component must include validated normalized bounding boxes or an explicit geometry-unavailable status.

**Consequences (testable):**

- BBOX coordinates remain inside the canvas and use one declared coordinate system.
- Geometry validation is deterministic and independent of semantic interpretation.

**Traceability:** Decisions D007, D012; journeys UJ-02.

### FR-024 — Build a spatial relationship graph

**Requirement:** The Builder must record relationships such as alignment, containment, pairing, overlap, anchoring, ordering, gaze, and category-specific scene relations between valid component IDs.

**Consequences (testable):**

- Relationship targets must exist and pass schema validation.
- The graph distinguishes observed spatial relations from inferred functional relations.

**Traceability:** Decisions D007, D014; journeys UJ-02.

### FR-025 — Parse hierarchy and reading order

**Requirement:** The Builder must draft attention hierarchy, reading order, typography roles, color roles, negative-space behavior, and density using evidence-linked fields.

**Consequences (testable):**

- The parse can explain which component dominates first attention and why that conclusion is provisional or measured.
- Typography and color roles are not promoted into invariants from a single unexplained instance.

**Traceability:** Decisions D007; journeys UJ-02.

### FR-026 — Classify composition variables

**Requirement:** The Builder must classify material visual properties as invariant, controlled variable, content slot, optional component, specimen anomaly, or unknown with confidence and supporting specimens.

**Consequences (testable):**

- A topic, niche, or replacement copy cannot become a layout invariant without cross-specimen evidence.
- Single-instance features default to anomaly or unknown unless another authority justifies promotion.

**Traceability:** Decisions D007, D008; journeys UJ-02, UJ-03.

### FR-027 — Parse temporal syntax for time-based evidence

**Requirement:** For video and animation categories, the Builder must identify appearance, persistence, motion, pose or state change, transition, timing, cut, sonic relation, and disappearance across frames or shots.

**Consequences (testable):**

- Temporal relationships use stable state or beat identifiers.
- Static-only categories do not receive artificial motion requirements.

**Traceability:** Decisions D030, D031; journeys UJ-02, UJ-06.

### FR-028 — Separate BBOX observation from WHY hypotheses

**Requirement:** The Builder must store measured geometry separately from visual-function hypotheses and require evidence, confidence, alternatives, and knowledge status for every proposed WHY.

**Consequences (testable):**

- A function hypothesis cannot overwrite a measured or observed field.
- Human ratification can promote an interpretation without rewriting its original provenance.

**Traceability:** Decisions D007, D011; journeys UJ-02.

### FR-029 — Induce cross-specimen visual grammar

**Requirement:** After all relevant specimens are parsed, the Builder must compare them to propose persistent instruments, component grammar, variants, optional branches, anomalies, and forbidden mutations.

**Consequences (testable):**

- Every candidate invariant cites multiple supporting specimens or an explicit canonical authority.
- Competing grammar hypotheses and unresolved evidence are retained for atomicity and Genesis.

**Traceability:** Decisions D007, D008; journeys UJ-02, UJ-03.

### FR-030 — Draft category-native sequence grammar

**Requirement:** The Builder must propose slide-role, scene-role, state-transition, pacing, and operator grammar appropriate to the selected category and format profile.

**Consequences (testable):**

- The sequence draft references observed temporal or cross-frame evidence.
- Sequencing hypotheses remain provisional until Genesis.

**Traceability:** Decisions D007, D030, D031; journeys UJ-02, UJ-06.

### FR-031 — Draft Activative hypotheses after syntax

**Requirement:** Only after syntactic and function parsing may the Builder propose recognition mechanism, hidden pressure, viewer role, prediction gap, intended reaction, memetic expression, and wrong-reading risks.

**Consequences (testable):**

- Activative fields are marked hypothesized and cite the visual or source evidence that motivated them.
- Generated subject matter or business strategy cannot masquerade as specimen observation.

**Traceability:** Decisions D007, D030; journeys UJ-02, UJ-04.

## Known failure and edge conditions

- Semantic meaning is assigned before the component inventory is complete.
- A generated dish example is treated as source evidence.
- One decorative element is promoted into an invariant.
- A video format is parsed only as static screenshots without temporal states.
- Character pose or gaze is ignored in the 2D Character Animation category.

## Explicitly out of scope

- Final media generation.
- Automatic ratification of visual meaning.
- Replacing expert visual review when confidence or category impact is high.
