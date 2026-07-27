---
title: "CMF Studio Agent Factory Registry"
status: "draft-canonical"
created_at: "2026-06-22"
source_files:
  - "docs/cmf-studio-agent-factory-architecture.md"
  - "docs/cmf-studio-agent-intelligence-contract.md"
  - "docs/cmf-studio-skill-system-contract.md"
  - "docs/cmf-studio-pipeline-map.md"
---

# CMF Studio Agent Factory Registry

## 1. Purpose

This registry turns the Factory architecture into named executable roles. The full Factory can contain many agents, but the first implementation slice should be research-to-review because it exercises the deepest CMF intelligence chain.

## 1A. Persona Code Standard

Every agent, sub-agent, hook, extension, skill, registry, and eval must have a stable persona code:

```text
DDD-XXXXXXX-TT
```

Where:

- `DDD` is the 3-character department code.
- `XXXXXXX` is the exactly 7-character service/role code.
- `TT` is the 2-character entity type.

Example:

```text
RES-VISRSCH-AG
```

This means Research Department, Visual Research service, Agent. The code is the operational identity used in logs, receipts, contracts, handoffs, UI filters, evals, stories, and agent config exports. The display persona can be human-friendly, but the code must always reveal what the entity serves.

### Department Codes

| Code | Department |
|---|---|
| `ORC` | Orchestration |
| `GOV` | Governance and spec control |
| `MIG` | Legacy migration |
| `REG` | Registries, primitives, SDA, SFL |
| `BRD` | Brand Genesis |
| `RES` | Research, CRAL/SCRE, Context Premise, visual research |
| `IND` | Interview induction, Matrix of Edging, Emotional DNA |
| `SES` | Complete Expression Session |
| `EXT` | Extraction and JIT compilation |
| `RTE` | Routing and asset derivatives |
| `PCK` | Package planning |
| `SCN` | Scene, composition, and editing session |
| `AST` | Asset candidates and provider coordination |
| `RND` | Rendering, assembly, audio, captions |
| `EVL` | Evaluations, critics, eval registries |
| `REV` | Review and approval |
| `PUB` | Publishing |
| `MEM` | Memory and Neo4j projection |
| `OPS` | Operations, recovery, readiness |

### Entity Type Codes

| Code | Entity Type |
|---|---|
| `AG` | Agent |
| `SA` | Sub-agent |
| `HK` | Hook |
| `EX` | Extension |
| `SK` | Stable operational skill |
| `JS` | JIT skill compiler |
| `EV` | Evaluation |
| `RG` | Registry |

## 1B. Canonical Persona Registry

| Code | Persona / Display Name | Entity | Serves |
|---|---|---|---|
| `ORC-PIORCHS-AG` | Pi Orchestrator | Agent | Stage selection, command proposal, handoff coordination, receipt progression |
| `ORC-VALIDCN-SA` | Validation Contract Analyst | Sub-agent | Preconditions, blocked actions, proof obligations before execution |
| `ORC-HNDOFFP-SA` | Handoff Packet Builder | Sub-agent | `AgentHandoffPacket` assembly and downstream evidence transfer |
| `GOV-SPECGOV-AG` | Spec Governance Agent | Agent | BMad/ERA3 PRD, story, architecture, tech-spec traceability |
| `MIG-MIGSTWD-AG` | Migration Steward | Agent | Legacy inventory, migration ledger, target mapping, hash review |
| `MIG-ORCHINT-SA` | Orchestration Intent Analyst | Sub-agent | Legacy module purpose, organism layer, gates, downstream proof |
| `REG-PRIMREG-AG` | Primitive Registry Curator | Agent | Primitive, SDA, SFL, crosswalk, registry activation governance |
| `BRD-BRDGENS-AG` | Brand Genesis Agent | Agent | Brand Genesis session, reusable creative universe, Brand Context lock |
| `BRD-ACTLIBR-SA` | Acting Library Specialist | Sub-agent | 64-state acting library generation, review, repair, lock |
| `BRD-PAPRIGG-SA` | Paper-Cut Rig Specialist | Sub-agent | Rig layers, pivots, mouth/eye/brow variants, preview validation |
| `BRD-MICANCH-SA` | Micro-Semiotic Anchor Specialist | Sub-agent | Props, symbolic anchors, negative space, brand semiotic consistency |
| `BRD-DNAARCH-SA` | Voice and Emotional DNA Architect | Sub-agent | Voice DNA, Emotional DNA, negative space, identity continuity |
| `RES-CRALENG-AG` | CRAL Research Engine Agent | Agent | SCRE/CRAL signal discovery, source cache, research snapshots |
| `RES-EVDCRIT-SA` | Evidence Critic | Sub-agent | Fact/inference separation, contradiction pressure, provenance checks |
| `RES-CTXPRMS-AG` | Context Premise Agent | Agent | Context Premise, Audience Reality, Audience Deep Trigger Map |
| `RES-AUDREAL-SA` | Audience Reality Analyst | Sub-agent | Audience-side pain, resistance, desire, context, belief field |
| `RES-CLAIMSF-SA` | Claim Safety Analyst | Sub-agent | Claim risk, source support, temporal sensitivity, unsafe assertions |
| `RES-CULSEMI-SA` | Cultural Semiotic Analyst | Sub-agent | Cultural fit, symbols, references, semiotic drift |
| `RES-VISRSCH-AG` | Visual Research Agent / Aurore | Agent | SVRE/Aurore visual search, candidates, licensing, fit scoring |
| `IND-PREINDC-AG` | Interviewer Pre-Induction Agent | Agent | Operator resonance, authentic curiosity, emotional bridge preparation |
| `IND-MTXEDGE-AG` | Matrix of Edging Agent | Agent | Tension sites, primitive candidates, coalition signatures, edge products |
| `IND-NARINDC-AG` | Narrative State Induction Agent | Agent | Anti-centroid induction, authentic expression activation |
| `IND-ASSETCN-AG` | Interview Asset Contract Agent | Agent | Target expression state, routeability, first-line/depth anchors |
| `SES-LIVEINT-AG` | Live Interview Assistant | Agent | In-session guidance, anchor awareness, source-expression support |
| `SES-SESSQLT-SA` | Session Quality Analyst | Sub-agent | Recording and expression-session quality checks |
| `SES-CNSMONR-SA` | Consent Monitor | Sub-agent | Current consent state during session, processing, rendering, publishing |
| `SES-RECSTWD-SA` | Recording Steward | Sub-agent | Master source, backup recording, upload route, source readiness |
| `EXT-JITCOMP-AG` | JIT Skill Compiler Agent | Agent | Saturation-bound induction, extraction, route, and eval compilers |
| `EXT-EXPMOMN-AG` | Expression Moment Agent | Agent | Transcript/source-grounded expression moment candidates |
| `EXT-TRALIGN-SA` | Transcript Alignment Analyst | Sub-agent | Transcript segments, timestamps, source artifact alignment |
| `EXT-SEMCRIT-SA` | Semantic Critic | Sub-agent | Source truth, meaning integrity, anti-draft and anti-genericity |
| `RTE-ARCHRTE-AG` | Archetype Routing Agent | Agent | Core content archetype selection and route receipts |
| `RTE-ASSTDER-SA` | Asset Derivative Router | Sub-agent | Carousels, meme visuals, poll visuals, reaction seeds, render modes |
| `RTE-MEMERTE-SA` | Meme Mechanism Router | Sub-agent | Meme mechanism fit, source support, humor/distortion constraints |
| `RTE-REACTRT-SA` | Reaction Router | Sub-agent | Reaction archetype routing and unsupported-route rejection |
| `RTE-CMFROUT-SA` | CMF Render Route Analyst | Sub-agent | CMF render mode selection, format validity, route gates |
| `PCK-PACKCMP-AG` | Package Compiler | Agent | Trial Guest Asset Pack and Monthly Asset Engine package planning |
| `SCN-EDTSESS-AG` | Complete Editing Session Agent | Agent | Editing session creation, source-route-brand lineage |
| `SCN-SCNSPEC-AG` | SceneSpec Compiler | Agent | SceneSpec, Creative State, Render Contract compilation |
| `SCN-CREATST-SA` | Creative State Analyst | Sub-agent | Brand constraints, scene intent, creative state validation |
| `SCN-CMPDIRC-SA` | Composition Director Adapter | Sub-agent | Ideogram 4 `CompositionJob`, plate analysis, text/identity boundary |
| `SCN-SCNINTL-SA` | Scene Intelligence Analyst | Sub-agent | Scene containers, components, subsystems, asset-roll orchestration |
| `AST-ASSTSCR-SA` | Asset Candidate Scorer | Sub-agent | Candidate scoring, licensing, asset-roll fit, visual risk |
| `AST-PROVADP-AG` | Provider Adapter Agent | Agent | Provider job requests, metadata, cost, retry, receipt handling |
| `RND-RENROUT-AG` | Renderer Router | Agent | Remotion, Motion Canvas, render route selection |
| `RND-REMOTON-SA` | Remotion Renderer | Sub-agent | Deterministic Remotion render output |
| `RND-MOTNCVS-SA` | Motion Canvas Renderer | Sub-agent | Deterministic Motion Canvas render output |
| `RND-AUDIOAS-SA` | Audio Assembly Agent | Sub-agent | Source audio, repaired audio, SFX, music, final mix lineage |
| `RND-CAPTIME-SA` | Caption and Timeline Agent | Sub-agent | Captions, EDL, timeline manifests, timing checks |
| `EVL-EVALREG-AG` | Eval Registry Agent | Agent | Eval target selection, primitive obligations, rubric activation |
| `EVL-EVALRUN-AG` | Evaluation Agent | Agent | EvaluationReceipt generation and blocker handoff |
| `EVL-IMGCRIT-SA` | Image Critic | Sub-agent | Likeness, composition, identity, negative space, visual fidelity |
| `EVL-VOICCRT-SA` | Voice Continuity Critic | Sub-agent | Voice DNA, audio continuity, synthetic bridge constraints |
| `EVL-CBARAUD-SA` | CBAR Auditor | Sub-agent | Constraint pressure, failure scenario, resolution proof |
| `REV-REVWBCH-AG` | Review Workbench Agent | Agent | Reviewer read model, evidence state, blockers, decision context |
| `REV-APPGATE-HK` | Approval Gate Hook | Hook | Final approval blockers and human authority enforcement |
| `PUB-PUBINTN-AG` | Publishing Intent Agent | Agent | Publishing intent, platform variants, scheduling metadata |
| `PUB-PUBLERX-EX` | Publer Adapter Extension | Extension | Publer scheduling and status tracking without canonical authority |
| `MEM-MEMADMT-AG` | Memory Admission Agent | Agent | Evidence-backed memory admission, correction, reversal, quarantine |
| `MEM-NEO4JPR-SA` | Neo4j Projection Builder | Sub-agent | Rebuildable relationship projection, lag, checkpoints |
| `OPS-OPSBRDG-AG` | Operations Board Agent | Agent | Queues, workers, failures, costs, blockers, operational status |
| `OPS-RECOVER-AG` | Recovery Agent | Agent | Retry, resume, cancel, compensate, quarantine |
| `OPS-READCHK-AG` | Readiness Check Agent | Agent | Restore, outage, worker shutdown, memory/projection rebuild, full cycle checks |

## 2. First Executable Team

| Agent | Goal | Fit rationale | Primary outputs |
|---|---|---|---|
| Pi Orchestrator | Coordinate stage plans and handoffs | Owns orchestration through Python Agent Gateway and typed commands | `StageExecutionPlan`, `AgentHandoffPacket`, command proposals |
| SCRE/CRAL Research Agent | Run sovereign textual research | Owns SearXNG category routing, CRAL moments, source cache, and autocomplete polling | `CRALFinding`, `ResearchSnapshot` |
| Evidence Critic | Attack weak evidence | Protects fact/inference separation and epistemic friction | contradiction notes, evidence critique |
| Context Premise Agent | Compile audience and guest context into premise | Converts evidence into routeable psychological and cultural premise | `ContextPremise`, `AudienceDeepTriggerMap` |
| Matrix of Edging Agent | Generate tension, primitive, coalition, and edge products | Owns broad signal, primitive pass, coalition survival, and route implications | `MatrixOfEdgingBrief`, `MatrixReceipt` |
| JIT Skill Compiler Agent | Run saturation-bound specialist compilers | Applies extraction, induction, contrast, and anti-draft skill modes | `SkillInvocationRecord`, calibration report |
| Expression Extraction Agent | Extract source-bound expression moments | Owns transcript/source extraction, quote boundaries, and depth checks | `ExpressionMoment`, extraction receipt |
| Route Candidate Agent | Select valid routes from active registries | Owns archetype, derivative, reaction, and CMF route candidate generation | `RouteCandidate`, `AssetRouteReceipt` |
| Eval Registry Agent | Select eval targets | Owns eval definitions, target bindings, primitive obligations, and run policies | `EvalTargetSelection`, `EvalSuggestion` |
| Evaluation Agent | Generate immutable evaluation receipts | Owns scores, evidence, hard failures, and approval-blocker handoff | `EvaluationReceipt`, `EvaluationApprovalBlocker` |
| Review Workbench Agent | Assemble reviewer evidence surface | Makes receipts, blockers, source, route, consent, and primitive failures legible | `ReviewEvidenceState`, review read model |

## 3. Shared Rules

Every agent:

- operates from active registries;
- cites source evidence;
- preserves primitive obligations;
- writes or consumes receipts;
- obeys consent and role policy;
- cannot approve final publication;
- cannot invent content formats outside valid route registries;
- treats Neo4j as rebuildable projection only.

## 4. Adapter Strategy

Google ADK and Agents CLI can consume generated adapter files after this registry becomes a typed contract. The source of truth remains CMF `AgentRoleSpec`, not hand-authored ADK YAML.
