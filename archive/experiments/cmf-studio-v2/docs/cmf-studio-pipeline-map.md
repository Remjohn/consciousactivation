---
title: "CMF STUDIO Pipeline Map"
created: "2026-06-21"
status: "draft-v1"
purpose: "Canonical readable map of CMF STUDIO workflows, sub-workflows, agents, sub-agents, gates, and lineage objects"
source_files:
  - "docs/migration/legacy-inventory.md"
  - "THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md"
  - "THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md"
  - "THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md"
  - "THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md"
  - "THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md"
  - "THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md"
  - "docs/architecture.md"
  - "docs/epics.md"
---

# CMF STUDIO Pipeline Map

## 1. Purpose

CMF STUDIO needs one readable operating map that shows the whole system from intake to memory without flattening the real machinery. The pipeline is not a simple content generator. It is an orchestrated expression-to-asset system where human activation, legacy cognitive modules, typed contracts, DSPy programs, specialist agents, provider workers, evaluation receipts, and human approval all pass state forward.

This file is the first canonical map. It should be referenced by the Product Brief, PRD, architecture, epics, and tech specs.

## 2. End-to-End Spine

```text
Legacy Inventory and Migration Ledger
-> Workspace, Commercial Scope, Consent, and Brand Setup
-> Brand Genesis and Brand Context Version
-> Research and Context Engineering
-> Interview Intelligence and Narrative State Induction
-> Complete Expression Session
-> Expression Moment Extraction
-> Archetype, Derivative, Reaction, and CMF Route Selection
-> Asset Package Spec
-> Complete Editing Sessions
-> SceneSpec, Creative State, and Render Contract
-> Composition Control, Asset Research, and Provider Jobs
-> Renderer Routing, Assembly, and Render Output
-> Evaluation, Human Review, Revision, and Approval
-> Publishing Intent and Publer Scheduling
-> Brand, Interviewer, Route, Rejection, and Performance Memory
-> Neo4j Relationship Projection
```

The runtime control layer stays constant across the spine:

```text
PWA / Telegram / system event
-> Python Agent Gateway
-> scoped AgentExecutionContext
-> Pi Coding Agent orchestrator
-> DSPy program and approved tool selection
-> Pydantic AgentCommand proposal
-> policy, permission, cost, consent, and idempotency validation
-> Command Bus
-> durable workflow or synchronous application service
-> provider, renderer, publisher, or memory adapter
-> receipt, audit event, and projection update
```

## 3. Stage Map

| Stage | Sub-workflow | Primary agents or roles | Consumes | Emits | Hard gates |
|---|---|---|---|---|---|
| 0 | Legacy inventory and migration | Migration Steward, Pi Orchestrator, Architecture Reviewer | Legacy Inventory, source paths, old CMF/CCF modules, schemas, prompts, code, assets | Migration ledger entries, `LegacyOrchestrationIntentRecord`, target Pydantic/DSPy/eval targets | No direct legacy runtime import; every orchestration-bearing module must preserve why it exists |
| 1 | Workspace and commercial setup | Operator, Agent Gateway, Tenant/Policy service | Organization, brand, user, consent state, pricing plan | Brand Workspace, role assignments, entitlement and cost policies | Only `$29/week` trial Guest Asset Pack or `$99/month` Monthly Asset Engine appear as customer-facing content charges |
| 2 | Brand Genesis | Brand Intake role, Identity/Asset role, Evaluation Agent | Intake, likeness consent, source photos/video, brand notes, visual preferences, forbidden tone | Brand Context Version, Identity Pack, 64-state Acting Library, paper-cut avatar rig, props, anchors, motion and SFX libraries | Consent, photo quality, identity stability, ImageCritic, locked Brand Context Version |
| 3 | Research and context engineering | Guest Research Agent, Audience Reality Agent, Evidence Critic, Context Premise Agent, Cultural/Semiotic Agent, Claim Safety Agent | Objective, public sources, guest history, audience evidence, CRAL/SCRE findings | Guest Dossier, Audience Reality Brief, Context Premise, Audience Deep Trigger Map, Research Snapshot | Evidence provenance, recency, fact/inference separation, adversarial review, human review |
| 4 | Interview intelligence | Interviewer Pre-Induction Agent, Matrix of Edging Agent, Narrative State Induction Agent, Asset Contract Agent | Guest Dossier, Audience Reality Brief, Context Premise, Emotional DNA, Voice DNA, Matrix of Edging | Interviewer Resonance Context, Matrix brief, Narrative State Map, Interview Asset Contracts, Interview Deck | Anti-centroid risk, saturation, routeability, shallow/unsupported psychology check |
| 5 | Complete Expression Session | Operator, Live Interview Assistant, Capture workflow | Recording configuration, Interview Deck, consent, guest setup, source devices | Master recording, backup recording, transcript, timestamped anchor hits, session quality receipt | Capture quality, consent, file provenance, source truth, recording protocol |
| 6 | Post-session extraction | Post-Session Extraction Agent, JIT Skill compiler modules, Evaluation Agent | Transcript, timestamps, audio/video evidence, anchor hits, Interview Asset Contracts | Expression Moments, quote candidates, story beats, primitive activations, edge products, route candidates | Source truth, clip boundary, depth, landing, anti-draft and anti-centroid checks |
| 7 | Routing and package planning | Archetype Route Compiler, Asset Derivative Router, Meme/Reaction Router, CMF Route Router | Expression Moments, primitive coalitions, archetype registry, derivative schemas, CMF route registry | Asset Package Spec, Guest Asset Pack plan, reaction seeds, route receipts | Valid format registry, no newsletters, route fit, package feasibility |
| 8 | Complete Editing Session | CMF Asset Producer Agent, SceneSpec Compiler, Renderer Router | Approved Expression Moment, route receipt, Asset Package Spec, locked Brand Context Version | Complete Editing Session, SceneSpec, Creative State, Render Contract, revision policy | Source lineage, brand context lock, route validity, evaluation requirements |
| 9 | Scene planning and composition | Scene Intelligence role, Ideogram Composition Director adapter, Visual Research Agent | SceneSpec, narrative intent, asset-roll plan, scene container/component/subsystem rules | Ideogram 4 `CompositionJob`, composition plate, composition analysis, layer plan, asset research requests | Composition JSON preservation, prompt hash, text-space rule, identity/text not finalized by Ideogram |
| 10 | Asset research and provider jobs | SVRE/Aurore role, Visual Candidate Scorer, Provider Adapters, ComfyUI Worker Adapter | VisualResearchQuery, ImageResolutionMap, Brand Context assets, provider policy | AssetResearchManifest, VisualCandidate set, provider receipts, generated/edited assets | Licensing, provenance, brand fit, identity safety, self-hosted ComfyUI Docker policy |
| 11 | Assembly and rendering | Renderer Router, Remotion Compiler, Motion Canvas/Manim branches, Audio/Caption services | SceneSpec, layer manifest, animation plan, audio plan, caption plan, provider outputs | Render Output, timeline manifest, caption manifest, audio mix, execution receipt | Renderer route decision, audio/source voice policy, reproducibility, render integrity |
| 12 | Evaluation and review | Evaluation Agent, Reviewer, Operator, Telegram/PWA review surfaces | Render output, source quote, lineage, evaluation requirements, consent state | Evaluation Receipt, approval, revision request, rejection, sensitivity hold | Truth, dignity, likeness, composition, platform fit, routeability, publishing readiness |
| 13 | Publishing | Publishing Intent workflow, Publer Adapter, Operator | Approved asset, captions, platform variants, schedule metadata | Publishing Intent, Publer job, publish status, schedule receipt | No one-tap public publishing; human confirmation; no duplicate scheduling |
| 14 | Memory and projection | Memory Admission workflow, Brand Memory role, Neo4j projection builder | Approved outputs, rejected candidates, performance data, route outcomes, review notes | Brand Memory, Interviewer Memory, Route Memory, rejected-pattern memory, performance memory, Neo4j projection | Evidence-backed admission, correction/reversal ability, Neo4j is rebuildable projection only |

## 4. Agent and Sub-Agent Map

These are logical roles, not a mandate to create separate services. The greenfield context explicitly allows one runtime with role-specific contracts.

| Layer | Agent or sub-agent | Main responsibility | Key emitted objects |
|---|---|---|---|
| Runtime orchestration | Pi Coding Agent Orchestrator | Plans work, selects tools and DSPy programs, coordinates specialist roles, proposes typed commands, observes results | `AgentCommand`, repair plans, workflow signals |
| Runtime boundary | Python Agent Gateway | Scope, auth, thread, context, permissions, tool availability, command proposal, audit logging | `AgentExecutionContext`, agent messages, audit events |
| Reasoning substrate | DSPy Program Registry | Runs typed reasoning programs for research, Context Premise, contracts, extraction, routing, SceneSpec, evaluation | DSPy predictions validated into Pydantic objects |
| Migration | Migration Steward | Converts legacy doctrine/assets into greenfield contracts and fixtures | `MigrationLedgerEntry`, `LegacyOrchestrationIntentRecord` |
| Research | Guest Research Agent | Builds guest truth and public-context dossier | `GuestDossier`, evidence packets |
| Research | Audience Reality Agent | Researches audience anxieties, language, objections, tensions | `AudienceRealityBrief`, audience evidence |
| Research | Evidence Critic | Separates fact/inference and attacks weak evidence | contradiction notes, evidence critique |
| Research | Context Premise Agent | Converts evidence into temporary working hypotheses | `ContextPremise`, question implications |
| Research | Cultural/Semiotic Agent | Detects cultural codes, symbols, metaphors, audience language | semiotic candidates, cultural notes |
| Research | Claim Safety Agent | Prevents content from strengthening claims beyond evidence | claim safety receipt |
| Interview | Interviewer Pre-Induction Agent | Interviews the operator to discover resonance and avoidance zones | `InterviewerResonanceContext` |
| Interview | Matrix of Edging Agent | Finds broad signal, tension sites, primitive candidates, coalition signatures, edge products | `MatrixOfEdgingBrief`, primitive candidate packets |
| Interview | Narrative State Induction Agent | Maps expression state, state transitions, First-Line Anchors, Depth Anchors | `NarrativeStateMap`, induction rationale |
| Interview | Asset Contract Agent | Turns questions into production-bound routing contracts | `InterviewAssetContract`, Interview Deck |
| Interview | Live Interview Assistant | Supports live cues, followups, markers, and timestamp hints | live cue events, anchor hit markers |
| Extraction | Post-Session Extraction Agent | Extracts expression moments, beats, quotes, primitive activations, edge products | `ExpressionMoment`, route candidates |
| Compilation | JIT Skill compiler modules | Apply legacy drafting, contrastive prompting, anti-draft, narrative induction, and expression-extraction lenses | extraction/evaluation packets, hard negatives |
| Routing | Archetype and Asset Routers | Map moments to archetypes, derivatives, meme mechanisms, reaction seeds, and CMF render modes | `AssetRouteReceipt`, `AssetPackageSpec` |
| CMF planning | CMF Asset Producer Agent | Converts package specs into editing sessions and render jobs | `CompleteEditingSession`, provider jobs |
| Scene intelligence | SceneSpec Compiler | Builds SceneSpec, creative state, scene containers/components/subsystems, asset rolls | `SceneSpec`, `CreativeState`, `RenderContract` |
| Composition | Ideogram 4 Composition Director adapter | Produces composition plate and layout plan, not final identity or final text | `CompositionJob`, composition analysis |
| Asset research | SVRE/Aurore role | Searches, ranks, licenses, and routes found visual candidates | `VisualResearchQuery`, `AssetResearchManifest`, `VisualCandidate` |
| Provider execution | Provider adapters | Execute approved model/provider jobs with receipts | provider job receipts, output assets |
| GPU execution | ComfyUI Worker Adapter | Runs approved ComfyUI JSON templates on self-hosted Docker GPU workers | ComfyUI execution receipt, generated asset |
| Rendering | Renderer Router | Chooses Remotion, Motion Canvas, Manim, HyperFrames, SCAIL-2, or video branch by task need | renderer route decision |
| Rendering | Remotion/Motion/Audio/Caption services | Assemble deterministic video, captions, audio, layer manifests, packaging | render output, timeline manifest |
| Evaluation | Evaluation Agent | Scores source truth, archetype fit, identity, composition, style, routeability, publishing readiness | `EvaluationReceipt`, fix instructions |
| Review | Reviewer and Operator | Approve, reject, revise, escalate, or hold assets | approval/revision events |
| Publishing | Publer Adapter | Schedules approved publishing intents | Publer status and receipt |
| Memory | Memory Admission workflow | Admits only evidence-backed brand/interviewer/route/rejection/performance memory | memory events, projection events |

## 5. Object Spine

The product stays legible when every stage can point to the object it consumes and the object it emits.

```text
MigrationLedgerEntry
-> BrandWorkspace
-> BrandGenesisSession
-> BrandContextVersion
-> ResearchField / ResearchEvidence
-> GuestDossier
-> AudienceRealityBrief
-> ContextPremise
-> AudienceDeepTriggerMap
-> EmotionalDNAProfile / VoiceDNAProfile
-> MatrixOfEdgingBrief
-> NarrativeStateMap
-> InterviewAssetContract
-> InterviewDeck
-> CompleteExpressionSession
-> SourceArtifact / Transcript
-> ExpressionMoment
-> AssetRouteReceipt
-> AssetPackageSpec
-> CompleteEditingSession
-> SceneSpec
-> CompositionJob
-> AssetResearchManifest
-> ProviderJobReceipt
-> LayerManifest / AnimationPlan / RendererRoute
-> RenderOutput
-> EvaluationReceipt
-> ApprovalEvent
-> PublishingIntent
-> MemoryAdmissionReceipt
-> Neo4jProjectionEvent
```

## 6. Sub-Workflow Detail

### 6.1 Legacy Migration Sub-Workflow

```text
discover legacy item
-> classify as doctrine, registry, prompt, code, fixture, worker asset, or dead asset
-> record source path and hash
-> identify intentional orchestration role
-> map target Pydantic contract
-> map target DSPy program when applicable
-> map fixture and eval target
-> reviewer approval
-> block direct runtime import
```

This prevents CRAL, Context Premise, Emotional DNA, Voice DNA, Matrix of Edging, SVRE/Aurore, scene intelligence, and JIT compilers from being reduced to vibes or prompt labels.

### 6.2 Brand Genesis Sub-Workflow

```text
client intake
-> likeness consent
-> photo/video upload
-> source quality check
-> identity summary
-> 64-state acting library
-> paper-cut avatar rig
-> prop/object library
-> micro-semiotic anchors
-> motion and SFX libraries
-> composition preferences
-> ImageCritic and human review
-> locked Brand Context Version
```

Brand Genesis manufactures the reusable creative substrate before production begins.

### 6.3 Research and Context Sub-Workflow

```text
define research objective
-> collect source candidates
-> de-duplicate
-> assess quality and recency
-> extract evidence
-> separate fact from inference
-> generate Guest Dossier and Audience Reality Brief
-> propose Context Premises
-> adversarial review by Evidence Critic
-> human review
-> freeze Interview Research Snapshot
```

This is where CRAL/SCRE, audience reality, Context Premise, cultural/semiotic detection, and claim safety prepare the interview field.

### 6.4 Interview Intelligence Sub-Workflow

```text
Guest Truth
+ Interviewer Resonance
+ Audience Reality
-> Matrix of Edging pressure selection
-> Narrative State Induction plan
-> First-Line Anchors
-> Depth Anchors
-> Interview Asset Contracts
-> Interview Deck
-> pre-session quality gate
```

This is the first extraction layer: extraction from the guest before transcript processing exists.

### 6.5 Complete Expression Session Sub-Workflow

```text
recording configuration
-> guest setup and consent check
-> live interview with optional agent cues
-> master recording and backup capture
-> transcript alignment
-> timestamped anchor hits
-> session quality receipt
```

The Complete Expression Session is the upstream human-expression wrapper. It is not a media render job.

### 6.6 Extraction and Routing Sub-Workflow

```text
Complete Expression Session
-> transcript and source artifacts
-> Post-Session Extraction Agent
-> JIT skill compiler lenses
-> Expression Moments
-> primitive activations and edge products
-> archetype route candidates
-> asset derivative candidates
-> meme and reaction candidates
-> CMF render route candidates
-> Asset Package Spec
```

This is the second extraction layer: extraction from transcript and source artifacts.

### 6.7 Complete Editing Session Sub-Workflow

```text
approved Expression Moment
-> route receipt
-> locked Brand Context Version
-> Complete Editing Session
-> SceneSpec
-> Creative State
-> Render Contract
-> revision policy
-> evaluation requirements
```

Each asset route becomes its own Complete Editing Session, preserving why the asset exists and how it should be produced.

### 6.8 Scene, Composition, and Asset Sub-Workflow

```text
SceneSpec
-> scene container selection
-> scene component selection
-> creative subsystem gates
-> A/B/C/D/E-roll asset role plan
-> Ideogram 4 CompositionJob when useful
-> composition plate and analysis
-> SVRE/Aurore visual research
-> provider/generative job selection
-> asset candidate scoring
-> licensing and provenance check
-> layer manifest
```

Ideogram 4 is a Composition Director. It creates layout intelligence. It does not become the final identity renderer or final text authority.

### 6.9 Rendering Sub-Workflow

```text
Render Contract
-> Renderer Router
-> Remotion default branch
-> Motion Canvas / Manim procedural branch when needed
-> HyperFrames branch for rapid HTML motion when needed
-> SCAIL-2 or video-generation branch only for eligible cases
-> audio mix and caption plan
-> render output
-> execution receipt
```

The renderer is chosen from task requirements, not agent preference.

### 6.10 Evaluation, Review, Publishing, and Memory Sub-Workflow

```text
render output
-> evaluation receipt
-> human review
-> approve, revise, reject, or hold
-> Publishing Intent
-> Publer scheduling
-> performance and publishing receipt
-> memory admission
-> Neo4j projection update
```

Memory admission is evidence-backed and reversible. Neo4j is a rebuildable relationship projection, not the canonical production database.

## 7. Critical Integration Rules

1. **BMAD remains the workflow shell for spec creation**, but CMF STUDIO's implementation truth is Python/Pydantic/DSPy/Pi.
2. **Agents are role contracts, not service sprawl.** Specialist roles can run under one Agent Gateway and Pi orchestration boundary.
3. **Every workflow transition must carry a Pydantic object.** No invisible handoff through chat text.
4. **DSPy compiles and evaluates reasoning, but does not persist workflow state.**
5. **Durable workflows own retries, timers, long-running execution, and resumability.**
6. **The Product Brief needs a compressed version of this map.** Without it, the product doctrine is strong but the operating system is hard to inspect end to end.
7. **Legacy modules must preserve intentional order.** Research before induction, induction before extraction, primitive coalitions before routing, scene containers before components, and evaluation before approval.

## 8. Pi Harness Orchestration Model

Pi does not orchestrate CMF STUDIO by behaving like a large manager prompt. Pi orchestrates by reading the current production object, selecting the next valid stage, resolving the correct role contract or compiled skill, issuing a typed command, and waiting for receipts from workers, validators, workflows, and human gates.

The older Pi-extension doctrine remains useful as orchestration behavior, but the greenfield implementation must be Python-first:

| Older Pi extension idea | Greenfield CMF STUDIO interpretation |
|---|---|
| `InteractComp` ambiguity stop | Pydantic command validation, required input checks, and missing-evidence halt |
| `TillDone` assurance loop | Bounded validation loop for reversible local fixes such as schema correction, section repair, or format repair |
| `DamageControl` self-healing | Retry, compensate, quarantine, or issue a `FailureReceipt` through durable workflow policy |
| `ModelRouter` | Provider/model policy selected by task class, cost policy, privacy, latency, and required reasoning depth |
| `TeamOrchestrator` | Parallel role fanout only when roles are independently valid, such as draft/critic/synthesis, candidate scoring, or review agents |
| `SystemSelect` persona swap | Role-contract selection from the Agent Gateway, never hidden persona drift in a single prompt |
| `MemoryFolder` | Context compression and memory admission through explicit receipts; not direct database mutation by Pi |

### 8.1 Macro DAG, Micro Loop

The harness uses strict workflow state for macro production and small autonomous loops inside bounded stages.

| Layer | Pattern | Where it applies | Why |
|---|---|---|---|
| Macro pipeline | Durable DAG/state machine | Brand Genesis, Complete Expression Session, Complete Editing Session, provider jobs, rendering, approval, publishing, memory admission | These stages cross systems, money, identity, consent, storage, providers, or public publishing. They must be replayable and recoverable. |
| Micro task | Bounded dumb loop | schema repair, section assembly, extraction refinement, caption formatting, prompt-hash repair, visual candidate scoring, local render retries | These are reversible local convergence problems. They should not become fragile multi-agent trees. |
| Evaluation | Independent validator | expression quality, route fit, source truth, composition, identity, render readiness, publishing readiness | The worker must not approve its own work. |
| Learning | Outer feedback loop | rejected candidates, performance data, route survival, evaluator disagreements, friction receipts | The system improves from receipts without letting runtime state become chat memory. |

### 8.2 Orchestration Cycle

```text
1. Event arrives
   PWA, Telegram, scheduled workflow, provider callback, or system event.

2. Agent Gateway builds context
   organization, brand, active object, role permissions, relevant registry slices,
   frozen Brand Context Version, available tools, cost policy, and current workflow state.

3. Pi selects next valid stage
   Pi reads the pipeline state and chooses only from allowed transitions.

4. Pi resolves execution recipe
   If a compiled JIT skill, DSPy program, provider adapter, or workflow template exists
   for the stage/context, Pi references it. If missing or stale, Pi triggers compilation
   or migration workflow before execution.

5. Pi writes a Validation Contract
   Done-ness is defined before the worker runs.

6. Pi proposes a Pydantic AgentCommand
   No direct database mutation, no hidden provider call, no public publishing.

7. Command Bus and workflow policy validate
   permissions, idempotency, reversibility, consent, cost, brand scope, and required inputs.

8. Worker role executes
   A specialist role, DSPy program, deterministic service, provider adapter, or renderer runs.

9. Validator role evaluates independently
   Validation uses the pre-written contract, primitives, source evidence, and stage gates.

10. Harness decides next action
   pass -> persist receipt and advance;
   reversible failure -> bounded repair loop;
   missing truth -> failure receipt and quarantine;
   irreversible or sensitive action -> human handoff.

11. Receipts update observability and memory
   execution receipt, evaluation receipt, friction receipt, approval event,
   memory admission receipt, and rebuildable relationship projection.
```

### 8.3 Required Orchestration Objects

| Object | Purpose |
|---|---|
| `OrchestrationRun` | One top-level run across a brand cycle, expression session, asset package, or render job. |
| `StageExecutionPlan` | The chosen stage, role contracts, required inputs, tools, workflows, and exit conditions. |
| `ValidationContract` | Pre-generation definition of success, failure, thresholds, forbidden patterns, and required receipts. |
| `AgentHandoffPacket` | Structured handoff from orchestrator to worker or worker to validator. |
| `SkillInvocationRecord` | Which JIT skill, DSPy program, adapter set, registry snapshot, and fingerprint were used. |
| `FailureReceipt` | Structured failure with failed gate, root cause, retry policy, quarantine status, and next action. |
| `FrictionReceipt` | Agent-reported operational blockage such as missing dependency, ambiguous state, invalid schema, or unavailable tool. |
| `HumanHandoffRequest` | Explicit request for operator review when action is irreversible, evidence is missing, or policy requires consent. |

### 8.4 Role Segregation

Pi is the orchestrator, not the worker and not the judge.

| Role | Does | Must not do |
|---|---|---|
| Orchestrator | Selects stage, resolves recipes, writes validation contract, proposes commands, coordinates roles | Generate final artifacts and approve them in the same execution scope |
| Worker | Produces the artifact, extraction, route, scene, render, or repair | Decide final acceptance |
| Validator | Scores against the validation contract, primitives, evidence, policies, and hard gates | Inherit the worker's hidden reasoning or rubber-stamp completion |
| Human reviewer | Approves sensitive, public, identity, billing, publishing, or unresolved truth decisions | Manually reconstruct missing lineage that the system should preserve |

### 8.5 Autonomy Boundaries

Autonomous agents can run freely only inside reversible boundaries.

Reversible autonomous actions:

- draft or extraction candidate generation;
- local schema repair;
- visual candidate search and ranking;
- non-public render trials;
- caption formatting;
- provider retry within cost limits;
- JIT skill assembly section repair;
- evaluation simulation.

Human-gated or policy-gated actions:

- approving likeness or identity use;
- changing locked Brand Context Versions;
- charging, changing, or presenting customer-facing pricing;
- publishing or scheduling public content;
- deleting production artifacts;
- accepting unsupported psychological claims;
- overriding a failed consent, source-truth, or identity gate;
- deploying infrastructure or changing provider policy.

### 8.6 Example: Expression Moment Extraction

```text
CompleteExpressionSession.completed
-> Agent Gateway scopes brand, session, source artifacts, transcript, contracts, and permissions
-> Pi selects `expression_moment_extraction`
-> Pi resolves Post-Session Extraction role + JIT extraction compiler + relevant primitive/eval packets
-> Pi writes ValidationContract:
   source timestamp required,
   anchor hit or depth rationale required,
   source truth cannot be strengthened,
   routeability must be scored,
   unsupported claims must be flagged
-> Command Bus validates inputs
-> Worker extracts ExpressionMoment candidates
-> Validator runs source-truth, anti-centroid, primitive, routeability, and clip-boundary checks
-> pass: ExpressionMoment saved with receipt
-> partial: bounded repair loop
-> missing evidence: FailureReceipt + Reviewer task
-> accepted moment advances to archetype and asset routing
```

### 8.7 Example: Complete Editing Session Render

```text
AssetPackageSpec.item.approved
-> Pi selects `complete_editing_session_compile`
-> Pi resolves SceneSpecCompiler, RendererRouter, Ideogram route policy, SVRE/Aurore role, and provider policy
-> Pi writes ValidationContract:
   source expression lineage required,
   locked Brand Context Version required,
   CompositionJob preserved when used,
   final text rendered outside Ideogram,
   identity assets must be approved,
   render must produce evaluation receipt
-> Worker compiles SceneSpec and RenderContract
-> Renderer/Provider workers execute through durable workflow
-> Validator scores identity, composition, negative space, source truth, style, platform fit, and publishing readiness
-> pass: review queue
-> repairable failure: bounded render/provider repair
-> unrepairable or sensitive failure: human review
```

### 8.8 The Practical Answer

Pi orchestrates the pipeline by continuously answering five questions:

1. What production object is active?
2. What stage is valid next?
3. What typed recipe, JIT skill, DSPy program, or deterministic service owns this stage?
4. What validation contract must exist before work begins?
5. Is the next action reversible, repairable, quarantined, or human-gated?

This is how autonomous agents operate like a team without becoming a pile of independent chatbots.

## 9. Product Brief Insertion Recommendation

Add a new Product Brief section after `5. Product Architecture and Execution Doctrine`:

```text
5A. Canonical Pipeline and Agent Orchestration Map
```

The insertion should include:

- the end-to-end spine from Section 2;
- the 14-stage map compressed to one table;
- the logical agent map;
- the object spine;
- the rule that agents are role contracts under one Python Agent Gateway;
- the rule that every stage emits a typed object, receipt, or human decision.

This should become a P0 repair in the Product Brief MCDA.
