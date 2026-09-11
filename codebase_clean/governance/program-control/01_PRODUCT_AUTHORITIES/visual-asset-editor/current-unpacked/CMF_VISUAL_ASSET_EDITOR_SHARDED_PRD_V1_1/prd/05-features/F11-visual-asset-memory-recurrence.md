---
title: F11 — Visual Asset Memory, Syntax-Aware Reuse, and Contextual Recurrence
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F11
governing_decisions:
- D006
- D008
- D009
- D014
- D017
- D020
- D021
user_journeys:
- UJ-03
- UJ-04
- UJ-09
- UJ-15
functional_requirement_count: 8
---


# F11 — Visual Asset Memory, Syntax-Aware Reuse, and Contextual Recurrence

**User outcome:** A new demand can reuse prior assets and lessons intelligently without confusing repetition with failure or continuity with fatigue.

## Description

Memory stores immutable assets and rendered usage context, then retrieves through semantic, composition, continuity, syntax, and recurrence criteria.

## Brownfield baseline

V2.1 includes asset memory, usage receipts, fatigue records, and geometry; the new design adds VLM comparison of rendered Visual Syntax contexts and governed reuse scoring.

## Required product delta

Define memory records, usage receipts, contextual embeddings, recurrence labels, retrieval scoring, continuity, supersession, syntax fingerprints, and feedback to planning.

## Traceability

- **Decisions:** D006, D008, D009, D014, D017, D020, D021
- **User journeys:** UJ-03, UJ-04, UJ-09, UJ-15
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-MEM-001, NFR-MEM-002, NFR-MEM-003, NFR-MEM-004, NFR-MEM-005

## Functional Requirements

### FR-081 — Store rich Visual Asset Memory records

**Requirement:** Accepted assets must be indexed by family/subtype, semantic roles, Activative functions, identities, environments, palette, expression, pose, geometry, production, evaluation, lineage, lifecycle, and certified uses.

**Consequences (testable):

- The memory record can answer both production and composition suitability questions.

- A generic embedding-only asset record is insufficient.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-082 — Create one Visual Usage Receipt per rendered use

**Requirement:** Every composition use must record asset version, harness, category, format profile, scene/slide, sequence position, syntactic role, composition function, BBOX/layer, neighboring elements, Activative function, transformation, recurrence intent, and rendered-context reference.

**Consequences (testable):

- The exact rendered use is inspectable independently of the source asset.

- Usage count without context cannot drive fatigue decisions.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-083 — Generate syntax-context fingerprints

**Requirement:** The system must derive comparable representations from the Visual Syntax Parse, composition geometry, neighboring relationships, recurrence intent, and rendered appearance for each use.

**Consequences (testable):

- Retrieval and recurrence evaluation can compare different files that express the same visual pattern.

- File identity alone cannot represent contextual similarity.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-084 — Classify recurrence contextually with a VLM

**Requirement:** Recurrence must be labeled beneficial recurrence, neutral reuse, productive variation, redundant repetition, fatiguing pattern, or contradictory recurrence using rendered context and sequence function.

**Consequences (testable):

- The VLM provides evidence and comparison references for its verdict.

- Previous usage frequency cannot automatically reject a candidate.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-085 — Retrieve assets through constraint-aware suitability

**Requirement:** Reuse ranking must combine semantic, Activative, composition, geometry, identity/continuity, syntax-role, transformation feasibility, quality, lifecycle, and recurrence signals.

**Consequences (testable):

- The result explains inclusion, exclusions, recommended route, and any transformation required.

- High visual similarity cannot compensate for wrong role or continuity.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-086 — Prioritize valid reuse before new production

**Requirement:** The Resolution Strategy Composer must evaluate exact reuse, deterministic variant, transformation, and composite reuse before new acquisition or generation when they can meet the demand.

**Consequences (testable):

- The plan records why reuse passed or failed.

- New generation without a memory query is nonconformant for asset families with memory enabled.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-087 — Preserve continuity without creating false fatigue

**Requirement:** Character identity, visual world, persistent format instruments, and deliberate motifs may repeat when the current syntax context and sequence purpose justify recurrence.

**Consequences (testable):

- Continuity-positive recurrence can be exempted from raw-frequency penalties through explicit evidence.

- A model that penalizes required character identity repetition fails recurrence benchmarks.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

### FR-088 — Invalidate or warn on superseded memory

**Requirement:** Superseded, regressed, deprecated, or contextually unsafe assets and recipes must be excluded or penalized according to lifecycle policy, and affected in-progress uses must revalidate.

**Consequences (testable):

- Historical use remains visible with the version that was actually consumed.

- A superseded asset cannot be returned as current production-ready without an explicit compatibility exception.

**Traceability:** Decisions D006, D008, D009, D014, D017, D020, D021; journeys UJ-03, UJ-04, UJ-09, UJ-15.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
