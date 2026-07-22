---
type: modular-prd
module: PRD-11
title: CMF JIT Skill Compiler - Interview Brief, Induction, Extraction, and Contrast
author: John (Product Manager)
date: 2026-06-22
status: Draft Source of Truth
version: 1.0
dependencies:
  - docs/prd/modules/PRD_INDEX.md
  - docs/prd/modules/PRD_10_CMF_Interview_Intelligence.md
  - docs/prd/modules/PRD_02_CCF_Content_Factory.md
  - docs/prd/modules/PRD_08_Conscious_Primitives.md
  - docs/tech-specs/TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md
source_documents:
  - THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md
  - THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
  - THE CMF STUDIO/CCP V9 -- Interview-First Expression Engine.md
  - THE CMF STUDIO/CCP V9.1 -- Expression Capture & Archetype Routing Update.md
  - docs/migration/legacy-inventory.md
  - docs/prd/modules/PRD_02_CCF_Content_Factory.md
  - docs/tech-specs/TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md
active_primitives:
  meaning_plane: [STR, PRS, CON, PSY, VOC, ACT]
  experience_plane: [TRG, FRC, PER, SAF]
capability_areas: [CMF-JIT, CMF-BRIEF, CMF-INDUCTION, CMF-EXTRACTION]
---

# PRD-11: CMF JIT Skill Compiler - Interview Brief, Induction, Extraction, and Contrast

**Version:** 1.0 | **Status:** Draft Source of Truth | **Date:** 2026-06-22

## 1. Purpose and Architectural Claim

The legacy JIT Skill Compiler doctrine remains valuable, but CMF Studio changes its center of gravity. The JIT system is no longer primarily a script generation helper. It is an interview intelligence compiler.

Its north-star output is the Interview Brief: a source-grounded, operator-readable, machine-loadable artifact that turns research saturation into interview pressure, narrative induction moves, Interview Asset Contracts, extraction lenses, route obligations, and evaluation targets.

JIT skills still support final outputs when needed, but that is downstream. The first job is to improve the human expression that will become the source material.

The governing claim is:

```text
JIT Skill Compilers do not write from prompts.
They compile specialized execution from saturation context, contrast, primitives, evidence, and failure corpora.
```

## 2. Skill Families

### 2.1 Stable Operational Skills

Stable operational skills are reusable agent procedures:

- registry lookup;
- source evidence review;
- consent inspection;
- command proposal;
- receipt comparison;
- blocker inspection;
- review read-model assembly.

These are not JIT. They are stable capabilities bound to agents.

### 2.2 JIT Skill Compilers

JIT skill compilers are saturation-bound specialist programs used when context must be compiled into a precise task output.

Required CMF modes:

- `research_distillation`;
- `context_premise_refinement`;
- `interview_brief_synthesis`;
- `narrative_induction_move_design`;
- `interview_question_contrast`;
- `expression_extraction_lens`;
- `route_candidate_comparison`;
- `voice_dna_support`;
- `emotional_dna_support`;
- `evaluation_support`.

## 3. Interview Brief Compiler Mode

The Interview Brief Compiler consumes:

- Research Field;
- CRAL findings;
- Guest Dossier;
- Audience Reality Brief;
- Context Premise;
- Audience Deep Trigger Map;
- Matrix of Edging Brief;
- primitive candidate packets;
- coalition signatures;
- edge products;
- Voice DNA or Emotional DNA where available;
- legacy skill fixtures;
- failure corpus and hard negatives;
- valid route registries.

It emits:

- Interview Brief;
- Interview Asset Contract candidates;
- induction moves;
- contrast questions;
- First-Line Anchors;
- Depth Anchors;
- repair follow-ups;
- extraction targets;
- route/eval obligations;
- SkillInvocationRecord.

## 4. Functional Requirements

### FR-CMF-JIT-01 Skill Registry Separation

The system shall distinguish stable operational skills from JIT skill compilers. Stable skills support recurring agent operations. JIT compilers produce context-specific outputs from saturation bundles.

### FR-CMF-JIT-02 Saturation Context Bundle

Every JIT compiler run shall require a Saturation Context Bundle containing relevant source docs, evidence refs, context artifacts, primitive candidates, prior evals, route constraints, and failure corpus refs.

### FR-CMF-JIT-03 Interview Brief Synthesis

The system shall provide a JIT compiler mode that generates Interview Briefs from CRAL, Context Premise, Matrix of Edging, Narrative State requirements, primitive obligations, and valid route registries.

### FR-CMF-JIT-04 Narrative Induction Move Design

The system shall use JIT compilers to produce live induction moves, First-Line Anchors, Depth Anchors, and repair follow-ups without scripting or impersonating the guest.

### FR-CMF-JIT-05 Contrastive Question Layer

The system shall generate contrast questions and hard-negative alternatives to expose generic, safe, overly abstract, or centroid answers before the interview begins.

### FR-CMF-JIT-06 Expression Extraction Lenses

The system shall compile extraction lenses that later help identify Expression Moments in transcripts using the approved Interview Brief, contracts, anchors, Matrix outputs, and primitive obligations.

### FR-CMF-JIT-07 Anti-Draft Calibration

Every JIT compiler output shall pass anti-draft calibration that checks genericness, unsupported specificity, source drift, Voice DNA drift, primitive collapse, and route overreach.

### FR-CMF-JIT-08 Skill Invocation Receipt

Every JIT compiler run shall write a SkillInvocationRecord with compiler version, registry snapshot, input hashes, evidence refs, output schema, eval state, and reviewer state.

## 5. Epics and Stories

### Epic JIT-1: Skill System Governance

**Outcome:** Agents know which skills are stable and which require JIT saturation.

- Story JIT-1.1: Define stable skill manifest schema.
- Story JIT-1.2: Define JIT Skill Compiler manifest schema.
- Story JIT-1.3: Register allowed JIT compiler modes.
- Story JIT-1.4: Enforce missing-context rejection.
- Story JIT-1.5: Write SkillInvocationRecord for every JIT run.

### Epic JIT-2: Interview Brief Compiler

**Outcome:** The system can compile Interview Briefs as the primary JIT output.

- Story JIT-2.1: Build Saturation Context Bundle for interview prep.
- Story JIT-2.2: Compile Interview Brief from research, context, Matrix, and route registries.
- Story JIT-2.3: Generate First-Line Anchors, Depth Anchors, and repair follow-ups.
- Story JIT-2.4: Generate contrastive interview questions and hard negatives.
- Story JIT-2.5: Attach eval obligations and extraction targets to the brief.

### Epic JIT-3: Extraction and Routing Support

**Outcome:** Post-session extraction uses the same brief intelligence that shaped the interview.

- Story JIT-3.1: Compile expression extraction lenses from approved Interview Briefs.
- Story JIT-3.2: Score transcript segments against Interview Asset Contracts.
- Story JIT-3.3: Compare route candidates using primitive and edge-product evidence.
- Story JIT-3.4: Reject ungrounded route suggestions.
- Story JIT-3.5: Preserve failed extraction patterns as future hard negatives.

## 6. Quality Standard

The JIT compiler is judged by the quality of the interview it enables, not by the polish of its generated text. A good JIT output helps the Operator ask the question that unlocks source expression. A bad JIT output sounds clever while producing generic answers.

Primitive obligations are the quality standard. Each JIT output must preserve intended primitive candidates, coalition logic, anti-centroid pressure, route implications, and evidence refs.

## 7. Non-Goals and Forbidden Drift

- No generic few-shot scripts.
- No JIT output without evidence refs.
- No Interview Brief generated from thin prompts.
- No live induction guidance that impersonates or over-controls guest speech.
- No route suggestion without active registry refs.
- No hidden prompt stacks outside compiler contracts.
- No JIT compiler mutating canonical state directly.

