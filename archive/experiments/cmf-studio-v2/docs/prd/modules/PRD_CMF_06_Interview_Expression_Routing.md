---
type: prd-module
project: CMF STUDIO
module_id: PRD-CMF-06
status: canonical
source_prd: 05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
source_sections:
  - FR-CMF-05
  - FR-CMF-06
last_updated: 2026-06-22
---

# PRD-CMF-06 - Interview Intelligence, Expression Sessions, and Routing

## Module Purpose

This module covers the north star of CMF STUDIO: better source expression before capture, then grounded extraction and routeable asset packages after capture. It combines research, Context Premise, Emotional DNA, Voice DNA, Matrix of Edging, Narrative State Induction, Interview Asset Contracts, Complete Expression Sessions, Expression Moments, archetype routing, and Guest Asset Packs.

The first monthly artifact is the Conscious Interview Brief. This brief is not a list of generic questions. It is a compiled skill output that turns CCF signal intelligence, audience reality, interviewer resonance, and Matrix pressure into Interview Asset Contracts.

## Product Requirements

### PR-CMF-06.01 Research and Context Engineering

Operators can create Research Fields with evidence, citations, claims, confidence, temporal sensitivity, source provenance, contradictions, research gaps, and inference labels. The system can compile Guest Dossiers, Audience Reality Briefs, Context Premises, Audience Deep Trigger Maps, and Interviewer Resonance Contexts.

### PR-CMF-06.02 Context Premise and Emotional DNA

Context Premise must represent the audience-side reality that makes a message land. Emotional DNA and Voice DNA represent the guest or brand-side root system, construction mechanics, negative space, emotional path, and normative voice profile. The product must preserve this distinction.

### PR-CMF-06.03 Matrix of Edging

The system can produce Matrix of Edging briefs from research pass, provocation pass, authentication pass, primitive pass, coalition pass, edge pass, routing pass, and benchmark pass. It must identify tension sites, primitive candidates, coalition signatures, edge products, likely failure points, and useful induction pressure.

### PR-CMF-06.04 Narrative State Induction

Narrative State Induction is structured facilitation, not scripting or manipulation. It helps the guest access authentic speech, move away from safe abstract centroid answers, and produce extractable material that remains true to the guest.

### PR-CMF-06.05 Interview Asset Contracts

The system can compile Interview Asset Contracts with target expression state, target archetype, asset derivative, edge product, first-line anchor, depth anchor, repair followups, CMF route, evaluation logic, and source evidence.

### PR-CMF-06.05A Conscious Interview Brief Skill

The Monthly Interview Brief must be compiled by the Conscious Interview Brief Skill. The skill does not convert signals directly into questions. It composes the CCP V9/V9.1 interview intelligence stack:

```text
Guest Truth
+ Interviewer Resonance
+ Audience Reality / Context Premise
-> High-Identification Question Field
-> Research Field / Broad Primary Signal
-> Matrix of Edging pressure selection
-> target expression state
-> First-Line Anchor set
-> Depth Anchor
-> Interview Asset Contract
-> Complete Expression Session
-> landing evaluation
-> Expression Moment extraction
-> archetype / derivative / CMF route
```

Each Interview Asset Contract must reference CRAL/SCRE findings, audience conversations/comments, Audience Reality Brief, Context Premise, Audience Deep Trigger Map, Interviewer Resonance Context, Matrix of Edging, primitive candidates, invariants or coalition signatures when available, target expression states, First-Line Anchors, Depth Anchor, repair followups, landing evaluation targets, route target, intended guest reaction, intended extraction outcome, and anti-centroid checks.

The skill cannot run from a topic, content format, or persona summary alone.

### PR-CMF-06.06 Complete Expression Session

Every interview is a Complete Expression Session with recording configuration, source artifacts, transcript revisions, interview contracts, quality gates, consent state, anchor hit log, and session status.

### PR-CMF-06.07 Dual-Layer Extraction

The product must support:

- live extraction from the guest through induction, question timing, resonance, contrast, and anchor hits;
- post-session extraction from transcript, timestamps, audio/video evidence, source artifacts, and Interview Asset Contracts.

### PR-CMF-06.08 Expression Moment Review

Reviewers can approve, reject, fix boundaries, split, merge, annotate, sensitivity-hold, or quarantine Expression Moments. Every candidate must include source timestamp, transcript segment, source artifact reference, induction context, primitive activation, and route rationale.

### PR-CMF-06.09 Archetype and Asset Routing

Approved Expression Moments can route through Core Content Archetype, Asset Derivative, Meme Mechanism, Reaction Archetype, and CMF Render Mode registries. Unsupported formats are rejected. Newsletters are not CMF deliverables.

Every routed content asset must receive an operator-facing content asset code in addition to its internal ID. The code must expose brand workspace, guest/client, session, package scope, content format, sequence, and version so Operators and Reviewers can distinguish assets across guests and brands without relying on ambiguous thumbnails or generic titles.

Canonical code shape:

```text
{BRD}-{GST}-{SES}-{PKG}-{FMT}-{SEQ}-V{VER}
```

Example:

```text
CEL-CLDNTA-S01-GAP-SV-CSC-001-V01
```

The content-format registry must include the documented CMF families:

- short videos;
- carousels;
- visual polls;
- tweet-like quotes;
- memes;
- Super Visuals;
- reaction seeds.

The short-video family must include four package-level subformats when source material supports them: Cinematic Story Commentary, Educational Explainer, Challenger / Frame Breaker, and Reaction / Recognition Clip.

### PR-CMF-06.09A Reaction Editing Template Routing

Conscious Reactions are not only social prompts. In CMF STUDIO they are live-filmed editing grammars that convert approved Expression Moments into animated social video and visual formats such as versus split screens, tier lists, blind rankings, proposal rankings, elimination brackets, mirror quizzes, authority quizzes, Would You Rather polls, and Goal-style ranking clips.

The system must route eligible Expression Moments through a governed `ReactionEditingTemplateRegistry` after asset routing and before SceneSpec compilation when a reaction-editing format is selected. Each template must define:

- template code and display name;
- compatible content format codes;
- legacy/source app reference, such as `apps/react-debate`, `apps/react-tierlist`, `apps/react-ranking-quiz`, `apps/react-blind-rank`, `apps/react-elimination`, `apps/react-authority-quiz`, or `apps/react-mirror-quiz`;
- interview question instruction;
- live clip slot requirements;
- motion grammar;
- primitive evaluation obligations;
- SceneSpec requirement patch.

Interview Asset Contracts may target a reaction editing template before filming. In that case, the question must be engineered so the live guest answer produces the exact slots the template needs: options, rankable items, verdicts, audience mirror statements, authority-test distinctions, or elimination winners. Existing-interview ingestion may still use these templates, but only when the transcript/video already contains the necessary source-backed material.

### PR-CMF-06.10 Guest Asset Pack

Trial Guest Asset Packs can include 4 videos, 2 carousels, 2 meme visuals, 2 poll visuals, and 2-3 reaction seeds when source material supports them. The broader content-format registry also supports tweet-like quotes and Super Visuals when routed and approved by documented format rules. Quotas cannot force fabricated or unsupported assets.

## Functional Requirements Covered

- FR-CMF-05.01 through FR-CMF-05.10.
- FR-CMF-06.01 through FR-CMF-06.08.

## Acceptance Gates

- Interview Asset Contracts must be evaluated for saturation, collision strength, anti-centroid risk, specificity, routeability, guest truth, expression-state fit, anchor quality, repair readiness, and landing evaluation clarity.
- Conscious Interview Brief contracts must show their source intelligence: CRAL/SCRE signal, audience conversation evidence, Context Premise, Interviewer Resonance Context, Matrix pressure, primitive/invariant/coalition obligation, First-Line Anchors, Depth Anchor, intended guest reaction, intended extraction outcome, and route target.
- Reaction editing template routes must prove source support, live slot fit, content-format compatibility, and primitive obligations before SceneSpec compilation.
- Expression Moments cannot route without source evidence.
- Asset Package Specs cannot include unsupported formats or assets without readable content asset codes.
- Rejected candidates and coalition failures can become learning evidence but not truth.
