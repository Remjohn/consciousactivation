---
type: modular-prd
module: PRD-10
title: CMF Interview Intelligence - Research, Context Premise, Matrix, and Interview Briefs
author: John (Product Manager)
date: 2026-06-22
status: Draft Source of Truth
version: 1.0
dependencies:
  - docs/prd/modules/PRD_INDEX.md
  - docs/prd/modules/PRD_02_CCF_Content_Factory.md
  - docs/prd/modules/PRD_08_Conscious_Primitives.md
  - THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
  - THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md
source_documents:
  - THE CMF STUDIO/CCP V9 -- Interview-First Expression Engine.md
  - THE CMF STUDIO/CCP V9.1 -- Expression Capture & Archetype Routing Update.md
  - THE CMF STUDIO/Matrix of Edging.md
  - THE CMF STUDIO/Claude Ntahuga Interview Deck -- V4.docx.md
  - docs/architecture/Sovereign_CRAL_Research_Engine_TechSpec_V1.md
  - docs/prd/modules/PRD_02_CCF_Content_Factory.md
  - docs/prd/modules/PRD_08_Conscious_Primitives.md
active_primitives:
  meaning_plane: [STR, PRS, CON, PSY, VOC, ACT]
  experience_plane: [TRG, FRC, SAF, PER]
capability_areas: [CMF-INT, CMF-RESEARCH, CMF-MATRIX, CMF-BRIEF]
---

# PRD-10: CMF Interview Intelligence - Research, Context Premise, Matrix, and Interview Briefs

**Version:** 1.0 | **Status:** Draft Source of Truth | **Date:** 2026-06-22

## 1. Purpose and Architectural Claim

CMF Studio's north star is not the rendered asset. The north star is better source expression before capture. The system exists to help an Operator produce interviews that would not happen through ordinary Q&A: interviews with pressure, specificity, emotional access, routeability, source truth, and reusable production value.

This module defines the upstream intelligence system that turns research into interview preparation. It formalizes the chain from sovereign research to Interview Brief:

```text
SCRE / CRAL Sovereign Signal Discovery
-> ResearchField and ResearchEvidence
-> GuestDossier
-> AudienceRealityBrief
-> ContextPremise
-> AudienceDeepTriggerMap
-> MatrixOfEdgingBrief
-> NarrativeStateMap
-> InterviewAssetContracts
-> InterviewBrief
-> InterviewDeck
```

The Interview Brief is the practical north-star artifact. It is the Operator-facing and machine-readable synthesis that explains what should be explored, why it matters, which emotional state the guest must be helped into, what source expression the system is trying to capture, which asset routes the expression could later support, and which evaluation obligations will prove the interview was production-ready.

The system must not collapse this into a generic guest research memo. Research is not a summary. Context Premise is not a persona. Matrix of Edging is not a hook generator. Interview Briefs are not scripts. They are production contracts for eliciting authentic, routeable human expression.

## 2. Core Runtime Model

### 2.1 Sovereign Research Spine

CMF uses SCRE/CRAL as the textual research engine. It uses self-hosted SearXNG category routing, seven CRAL moment executors, autocomplete polling, Finding-Linked Source Cache, and Epistemic Friction Swarm.

The seven CRAL moments remain:

- Relevant;
- Believable;
- Undeniable;
- Resonant;
- Surprising;
- Irrefutable;
- Relatable.

Each finding must preserve source discipline, evidence refs, freshness, confidence, contradiction notes, and inference boundaries. Serper and Tavily are legacy-deprecated search APIs and must not be reintroduced as active architecture.

### 2.2 Context Premise

Context Premise converts evidence into a temporary working hypothesis for the interview. It carries:

- trigger depth;
- hermeneutical gap;
- moral-emotional vector;
- coping trajectory;
- audience/guest match logic;
- confidence;
- expiry;
- evidence refs;
- contradiction notes.

The Context Premise is allowed to be partial when evidence is incomplete. It must not invent psychological certainty.

### 2.3 Matrix of Edging

The Matrix of Edging selects the meaningful human pressure. Its eight passes are:

1. Research pass.
2. Provocation pass.
3. Authentication pass.
4. Primitive pass.
5. Coalition pass.
6. Edge pass.
7. Routing pass.
8. Benchmark pass.

The Matrix emits broad primary signals, tension sites, primitive candidates, coalition signatures, edge products, likely failure points, and route implications. It is the bridge from research pressure to interview design.

### 2.4 Interview Brief

An Interview Brief is the synthesis layer for the Operator. It includes:

- interview objective;
- guest truth and source constraints;
- audience reality;
- active Context Premises;
- CRAL finding summary with evidence refs;
- Matrix pressure field;
- primitive candidates and coalition signatures;
- desired narrative state transitions;
- First-Line Anchors;
- Depth Anchors;
- Interview Asset Contracts;
- repair follow-ups;
- route candidates and valid content families;
- source capture requirements;
- eval obligations;
- review warnings.

The brief must be readable by a human interviewer and loadable by Pi, DSPy programs, and review surfaces.

## 3. Data Contracts

| Contract | Purpose |
|---|---|
| `ResearchField` | Planned research scope for the interview |
| `ResearchEvidence` | Cited evidence with provenance, confidence, freshness, and contradiction metadata |
| `CRALFinding` | Distilled moment finding from SCRE/CRAL |
| `GuestDossier` | Guest truth, role, story material, constraints, and known risks |
| `AudienceRealityBrief` | Audience pressures, objections, language, anxieties, and expectations |
| `ContextPremise` | Evidence-backed temporary hypothesis for interview pressure |
| `AudienceDeepTriggerMap` | Audience-side trigger depth and match logic |
| `MatrixOfEdgingBrief` | Eight-pass tension, primitive, coalition, edge, and routing artifact |
| `NarrativeStateMap` | Desired expression states and transitions |
| `InterviewAssetContract` | Question-level production contract |
| `InterviewBrief` | Operator-facing synthesis and machine-readable plan |
| `InterviewDeck` | Sequenced questions, anchors, follow-ups, and route obligations |

## 4. Functional Requirements

### FR-CMF-INT-01 Sovereign Research Intake

The system shall create Research Fields and Research Evidence from approved SCRE/CRAL findings, public sources, guest sources, and audience evidence. Each evidence item must include provenance, confidence, temporal sensitivity, claim scope, contradiction notes, and evidence refs.

### FR-CMF-INT-02 Context Premise Compilation

The system shall compile Guest Dossiers, Audience Reality Briefs, Context Premises, and Audience Deep Trigger Maps from approved research. Context Premises must preserve trigger depth and audience/guest match logic rather than generic persona summaries.

### FR-CMF-INT-03 Matrix of Edging Briefs

The system shall compile Matrix of Edging briefs with broad primary signals, tension sites, primitive candidates, coalition signatures, edge products, likely failure points, route implications, and evaluation scores.

### FR-CMF-INT-04 Narrative State Map

The system shall define target expression states, state transitions, First-Line Anchors, Depth Anchors, and live induction risks for each interview objective.

### FR-CMF-INT-05 Interview Asset Contract Compilation

The system shall compile question-level Interview Asset Contracts with target expression state, target archetype, asset derivative, edge product, anchors, repair follow-ups, CMF route, and evaluation logic.

### FR-CMF-INT-06 Interview Brief Generation

The system shall generate an Interview Brief that synthesizes CRAL findings, Guest Dossier, Audience Reality, Context Premise, Matrix of Edging, Narrative State Map, and Interview Asset Contracts into one Operator-ready artifact.

### FR-CMF-INT-07 Brief Approval and Revision

Operators shall review, request revision, approve, or hold Interview Briefs. Approval must require evidence completeness, source/inference separation, routeability, anti-centroid pressure, and valid registry references.

### FR-CMF-INT-08 Brief-to-Deck Handoff

The system shall compile approved Interview Briefs into Interview Decks with sequenced questions, anchors, live follow-up logic, source capture requirements, and route/eval obligations.

## 5. Epics and Stories

### Epic INT-1: Sovereign Research to Context Premise

**Outcome:** The Operator has evidence-backed guest and audience context before any Matrix or brief is compiled.

- Story INT-1.1: Create Research Field from interview objective and guest scope.
- Story INT-1.2: Ingest SCRE/CRAL findings with evidence provenance and contradiction notes.
- Story INT-1.3: Compile Guest Dossier and Audience Reality Brief.
- Story INT-1.4: Compile Context Premise with trigger depth, hermeneutical gap, moral-emotional vector, and expiry.
- Story INT-1.5: Review and approve context artifacts before Matrix use.

### Epic INT-2: Matrix of Edging for Interview Pressure

**Outcome:** The system identifies the human pressure that can create routeable expression.

- Story INT-2.1: Run the eight Matrix passes.
- Story INT-2.2: Generate primitive candidate packets from evidence and context.
- Story INT-2.3: Select coalition signatures and edge products.
- Story INT-2.4: Evaluate Matrix saturation, collision strength, specificity, anti-centroid risk, and routeability.
- Story INT-2.5: Approve Matrix brief for Interview Brief compilation.

### Epic INT-3: Interview Brief and Deck

**Outcome:** The Operator receives a practical, reviewed, source-grounded Interview Brief and Deck.

- Story INT-3.1: Compile Narrative State Map from Matrix and Context Premise.
- Story INT-3.2: Compile Interview Asset Contracts.
- Story INT-3.3: Generate Interview Brief with evidence, pressure, routes, anchors, and eval obligations.
- Story INT-3.4: Review, revise, and approve Interview Brief.
- Story INT-3.5: Compile Interview Deck from approved brief.

## 6. Non-Goals and Forbidden Drift

- No generic research summaries as substitutes for Context Premise.
- No interview scripts that force guest speech.
- No Matrix output without primitive candidate and coalition evidence.
- No hidden search provider calls outside SCRE/CRAL.
- No Interview Deck generated without approved Interview Brief.
- No newsletters as content routes.
- No MVP reduction of the interview intelligence chain.

