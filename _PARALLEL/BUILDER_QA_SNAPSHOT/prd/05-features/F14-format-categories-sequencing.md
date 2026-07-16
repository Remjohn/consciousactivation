---
title: F14 — Canonical Format Categories, Format Profiles, and Activative Sequencing
product: CMF Atomic Harness Builder Next
version: 0.3.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-14'
feature_id: F14
governing_decisions:
- D004
- D007
- D008
- D013
- D030
- D031
- D032
- D033
user_journeys:
- UJ-02
- UJ-03
- UJ-05
- UJ-06
- UJ-11
- UJ-12
functional_requirement_count: 14
---

# F14 — Canonical Format Categories, Format Profiles, and Activative Sequencing

**User outcome:** Each Atomic Content Harness is compiled through the correct category and format constitution, preserving shared Activative meaning while generating category-native conversational, visual, temporal, registry, runtime, evaluation, and repair architecture.

## Description

This feature establishes the nested content architecture: Shared Activative Core → Canonical Format Category → Category Format Profile → Atomic Harness. It recognizes sequencing as intelligence, gives 2D Character Animation its own registry-driven production substrate, and recognizes Conversational Activation / Human Expression as a full category whose source material is human reaction.

## Brownfield baseline

The Visual Syntax corpus contains eight short-form editing formats, Carousel and Supervisual corpora, and reference doctrine. Existing parallel packs classify atomic harnesses, but the Builder does not yet enforce five category constitutions or category-adapted parsing and sequencing as one typed system.

## Required product delta

Create the Shared Activative Core contract, five category constitutions, format profiles, character and sequence registries, category-native skill requirements, and atomic overlay rules with regression and migration governance.

## Traceability

- **Decisions:** D004, D007, D008, D013, D030, D031, D032, D033
- **User journeys:** UJ-02, UJ-03, UJ-05, UJ-06, UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-CAT-001, NFR-CAT-002, NFR-CAT-003, NFR-EVAL-004, NFR-PORT-002

## Functional Requirements

### FR-137 — Define a constitution-complete Shared Activative Core

**Requirement:** The Builder must provide a category-independent Activative contract covering source premise, Coach or Guest Identity DNA, Context Premise, resonance, Matrix of Edging, Activative Intelligence Pack identity, hidden pressure, activation directions, roles, stance, stakes, identity urges, participation design, intended reaction, smallest useful commitment, evidence provenance, evaluation contract, and wrong-reading locks.

**Consequences (testable):**

- The shared core supplies meaning without owning final conversational, visual, or temporal form.
- Sparse downstream tokens retain references to the rich frozen Activative Intelligence objects, and category or harness layers cannot silently rewrite them.

**Traceability:** Decisions D030; journeys UJ-06.

### FR-138 — Insert a mandatory category layer

**Requirement:** Every Atomic Content Harness must bind exactly one Canonical Format Category between the Shared Activative Core and its atomic constitution.

**Consequences (testable):**

- Category selection occurs before category-specific parsing and architecture compilation.
- A harness cannot combine category laws without an explicit multi-surface product decision outside this PRD's atomic boundary.

**Traceability:** Decisions D030, D031; journeys UJ-06.

### FR-139 — Support five canonical categories

**Requirement:** The initial category registry must include Short-Form Edited Video, 2D Character Animation, Carousels, Supervisuals, and Conversational Activation / Human Expression with stable IDs and governance owners.

**Consequences (testable):**

- Every content harness maps to one of the five or blocks as an unsupported category candidate.
- Category names and IDs are used consistently across IR, documents, benchmarks, and UI.

**Traceability:** Decisions D031; journeys UJ-06.

### FR-140 — Govern versioned category constitutions

**Requirement:** Each category must own a versioned constitution defining production surface, specimen types, visual and temporal parsing, composition ontology, sequence model, runtime families, canonical skill requirements, registries, evaluation dimensions, repair classes, observability, compatibility, benchmarks, and migration policy.

**Consequences (testable):**

- A constitution change triggers impact analysis across dependent profiles and harnesses.
- No category is production-certified without its required benchmark suite.

**Traceability:** Decisions D031; journeys UJ-06, UJ-12.

### FR-141 — Support category-local format profiles

**Requirement:** A category constitution must support governed format profiles that specialize parsing, sequencing, state, runtime, skill, evaluation, and repair rules before the atomic harness overlay.

**Consequences (testable):**

- Profiles remain versioned and independently benchmarkable.
- A format profile is not treated as a cosmetic theme variable.

**Traceability:** Decisions D030, D031; journeys UJ-06.

### FR-142 — Represent the edited-video format mapping

**Requirement:** The Short-Form Edited Video category must support the governed profiles for Format 01 Story Video, Format 03 Living Commentary, Format 04 Conscious Reaction, Format 05 Silent Dialogue Theatre, Format 06 Data Scale Race, Format 07 Direct Coaching A-Roll, and Format 08 Poetic Quote Theatre.

**Consequences (testable):**

- The mapping is canonical and does not silently include Format 02.
- Each profile may resolve into one or more atomic harnesses through evidence-based classification.

**Traceability:** Decisions D030, D031; journeys UJ-06.

### FR-143 — Represent Format 02 under 2D Character Animation

**Requirement:** The 2D Character Animation category must initially contain the Format 02 Minimal Coach Theatre profile and must not be collapsed into generic edited video.

**Consequences (testable):**

- Its category profile requires character-performance and continuity architecture.
- General icon or data animation does not automatically enter the character category.

**Traceability:** Decisions D030, D031; journeys UJ-06.

### FR-144 — Compile 2D character-performance registries

**Requirement:** The Format 02 profile must require versioned character identity, pose, expression, gesture, gaze, prop and attachment, animation primitive, character state, scene relationship, camera and framing, transition, sonic cue, and compatibility registries as applicable.

**Consequences (testable):**

- Semantic character states resolve to stable registry IDs before runtime composition.
- Invalid pose, expression, gesture, or prop combinations fail compatibility validation.

**Traceability:** Decisions D030, D031; journeys UJ-06.

### FR-145 — Use category-specific syntax parsing

**Requirement:** The syntax-parsing capability must load category and format ontologies appropriate to the production substrate, including conversational turn and Expression Moment parsing where applicable.

**Consequences (testable):**

- Carousels parse slide roles; Supervisuals parse one-frame hierarchy; video parses time states; 2D animation parses character performance; conversational harnesses parse Activative Calls, reactions, turn relationships, timecodes, expression functions, landings, and micro-commitments.
- The canonical parser procedure remains reusable while category output fields remain distinct.

**Traceability:** Decisions D007, D030, D031; journeys UJ-02, UJ-06.

### FR-146 — Use category-specific temporal, conversational, and sequence parsing

**Requirement:** Sequence-bearing categories must derive observed and hypothesized structure using category-native state, beat, turn, transition, continuity, pacing, silence, and sonic relationships.

**Consequences (testable):**

- Carousels represent swipe sequence without pretending to have frame-time motion.
- Supervisuals declare one-frame attention order, while conversational profiles represent question → reaction → follow-up → elevation/close without scripting the guest landing.

**Traceability:** Decisions D030, D031; journeys UJ-02, UJ-06.

### FR-147 — Compile category-adapted Activative Sequencing Intelligence

**Requirement:** Every sequence-bearing harness must receive a format-adapted capability that translates ratified Activative meaning and parsed syntax into viewer or participant roles, state beats, prediction gaps, scene, slide, or conversational-turn roles, transitions, asset or expression states, pacing, silence or sonic cues, payoff, intended reaction, and smallest useful commitment.

**Consequences (testable):**

- Sequence decisions cite Activative contracts and category-native syntax.
- Sequencing is independently evaluated and repairable rather than hidden inside final composition or generic question generation.

**Traceability:** Decisions D030; journeys UJ-06.

### FR-148 — Compile category-owned runtime, evaluation, and repair rules

**Requirement:** Each category and profile must contribute its own runtime constraints, invariant tests, quality dimensions, wrong-reading classes, continuity checks, repair ownership, and required telemetry.

**Consequences (testable):**

- A Supervisual is not evaluated by video pacing metrics.
- A 2D character continuity failure routes to character-state or scene composition rather than generic visual style repair.

**Traceability:** Decisions D031; journeys UJ-06, UJ-10.

### FR-149 — Preserve atomic creative ownership

**Requirement:** The atomic harness overlay must own its exact production promise, semantic workcell, visual or temporal grammar, legal variables, composition templates, evaluation thresholds, and repair behavior that are not proven category mechanisms.

**Consequences (testable):**

- Category abstractions cannot absorb atomic creative policy merely because two harnesses look related.
- Proposed reuse requires implemented evidence and regression coverage.

**Traceability:** Decisions D008, D030, D033; journeys UJ-03, UJ-06.

### FR-150 — Govern category and profile migration

**Requirement:** Category and format-profile changes must generate compatibility analysis, dependent-harness regression plans, migration artifacts, deprecation policy, and receipts.

**Consequences (testable):**

- Stable dependent harnesses remain pinned until explicitly migrated.
- A category change cannot silently alter an authorized Development Capsule.

**Traceability:** Decisions D031; journeys UJ-06, UJ-12.

## Known failure and edge conditions

- Format 02 is listed as a cosmetic short-form style.
- Interview Expression or ReelCast blocks as unsupported because the registry recognizes only visual surfaces.
- Conversational questions are generated from topics without a typed Activative Intelligence Pack.
- One universal parser prompt ignores character state or temporal grammar.
- Carousel sequencing is treated as static template duplication.
- Atomic creative logic is moved into a shared category engine before reuse is proven.
- Activative sequencing is reduced to a timeline export step.

## Explicitly out of scope

- Defining every future format profile in Release 1.
- Merging the five categories into one schema with mostly optional fields.
- Building the actual character assets or render runtime inside the Builder.
