---
type: prd-module
module_id: PRD-CMF-12
title: "Conscious Sequencing and Expression Acquisition"
status: canonical
source_prd: 05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
source_bundle:
  - "THE CMF STUDIO/CCP_CONSCIOUS_SEQUENCING_AND_EXPRESSION_ACQUISITION_ENGINE_V1_BUNDLE"
created_at: 2026-06-25
---

# PRD-CMF-12: Conscious Sequencing and Expression Acquisition

## 1. Product Requirement

CMF Studio must treat sequencing as a first-class production intelligence layer between interview planning and composition. The system must determine which semantic, emotional, evidentiary, visual, and brand-continuity ingredients should be acquired before and during an interview, then compile approved captured ingredients into viewer-facing sequence programs for videos, carousels, single-image posts, reactions, packages, and series.

This module formalizes the Conscious Sequencing and Expression Acquisition Engine as a canonical CMF requirement family. It extends PRD-CMF-06 and PRD-CMF-07 without replacing their ownership of interview sessions, extraction, routing, composition, or rendering.

## 2. Scope

The module owns:

- sequencing registries and contract kernel;
- Interview Brief V2 procurement;
- sequence hypotheses and expression acquisition plans;
- live ingredient coverage and cue suppression;
- expression ingredient inventory and relation graph;
- content sequence program compilation;
- sequence evaluation receipts;
- package sequencing and learning recommendations.

The module does not own:

- raw video editing runtime;
- renderer implementation;
- source transcription and diarization;
- final publishing integrations;
- generic agent factory behavior.

## 3. Non-Negotiable Laws

| Law | Requirement |
|---|---|
| Interview-state sequencing is not viewer-state sequencing | The guest's live journey must preserve safety, memory, vulnerability, authority, teaching, humor, and invitation. |
| Viewer-state sequencing is not package sequencing | One asset guides a viewer through a meaning arc; a package guides trust and future expectation over time. |
| Missing human truth cannot be fabricated | Final sequences may only use captured, approved, sourced, retrieved, pickup-requested, or non-human contextual ingredients. |
| Coverage must not become interrogation | Live coverage supports the interviewer; it cannot turn the session into a checklist. |
| Composition cannot rewrite meaning | Composition adapters may make sequence beats spatial or temporal but cannot change semantic order, source claim, or payoff without a new approved sequence version. |

## 4. Functional Requirements

### FR-CMF-12.01 Sequencing Contract Kernel

The system must normalize sequence registries, schemas, source law invariants, primitive bindings, and evaluation gates into a versioned kernel with activation receipts.

### FR-CMF-12.02 Interview Brief V2 Procurement

The system must compile the first monthly artifact as Interview Brief V2: a source-backed procurement plan containing asset portfolio intent, sequence hypotheses, expression acquisition plan, interview-state sequence, Interview Asset Contract V2 drafts, safety constraints, and coverage policy.

### FR-CMF-12.03 Live Ingredient Coverage

The system must track ingredient coverage during the Complete Expression Session and propose or suppress cues according to guest state, emotional peak, sensitivity, redundancy, and checklist-pressure rules.

### FR-CMF-12.04 Expression Ingredient Inventory

The system must extract, score, approve, freeze, and relate source-grounded expression ingredients from transcript, media, approved evidence, visual assets, and brand memory.

### FR-CMF-12.05 Content Sequence Program Compiler

The system must compile approved ingredients into `ContentSequenceProgram` objects that bind viewer-state beats, loops, source evidence, primitive coalitions, format adapters, and composition handoff contracts.

### FR-CMF-12.06 Sequence Eval, Package Sequencing, and Learning

The system must evaluate sequence programs, block false or manipulative payoff structures, assemble package/series ordering, and store learning recommendations without mutating historical receipts or active registries without approval.

## 5. Tech Spec Crosswalk

| Requirement | Tech Spec |
|---|---|
| FR-CMF-12.01 | `TS-CMF-114-conscious-sequencing-contract-kernel-and-registries.md` |
| FR-CMF-12.02 | `TS-CMF-115-interview-brief-v2-sequence-hypothesis-and-expression-acquisition-plan.md` |
| FR-CMF-12.03 | `TS-CMF-116-live-ingredient-coverage-tracker-and-cue-suppression-policy.md` |
| FR-CMF-12.04 | `TS-CMF-117-expression-ingredient-inventory-and-relation-graph.md` |
| FR-CMF-12.05 | `TS-CMF-118-content-sequence-program-compiler-and-composition-handoff.md` |
| FR-CMF-12.06 | `TS-CMF-119-sequence-eval-gates-learning-and-package-sequencing.md` |

