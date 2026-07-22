---
stepsCompleted:
  - 1
  - 2
  - 3
  - 4
  - 5
  - 6
  - 7
  - 8
inputDocuments:
  - 'THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md'
  - 'THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md'
  - 'docs/migration/legacy-inventory.md'
  - 'THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md'
  - 'THE CMF STUDIO/CCP V9 -- Interview-First Expression Engine.md'
  - 'THE CMF STUDIO/CCP V9.1 -- Expression Capture & Archetype Routing Update.md'
  - 'THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md'
  - 'THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md'
  - 'THE CMF STUDIO/CCP Archetype System Migration Proposition.docx.md'
  - 'THE CMF STUDIO/Matrix of Edging.md'
  - 'THE CMF STUDIO/Claude Ntahuga Interview Deck -- V4.docx.md'
  - 'docs/architecture/april_updates/ERA3_Epic_and_Story_Writing_Protocol.md'
  - 'docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md'
  - 'docs/architecture/april_updates/PROMPT_Spec_Build.md'
  - 'docs/architecture/april_updates/PROMPT_Spec_Audit.md'
  - 'docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md'
workflowType: 'architecture'
lastStep: 8
status: 'complete'
project_name: 'CMF STUDIO'
user_name: 'Emilio'
date: '2026-06-21'
completedAt: '2026-06-21'
---

# CMF STUDIO Architecture

**Author:** Winston, BMad Architect  
**Project:** CMF STUDIO  
**Status:** Ready for Epics, Stories, and Tech Specs  
**Date:** 2026-06-21  

This document is the canonical architecture for CMF STUDIO. It translates the completed PRD, the CMF source folder, the Legacy Inventory, and the Python/DSPy greenfield context into implementation decisions that AI agents can follow consistently.

CMF STUDIO is a Python-first, interview-first, multi-brand production system. It transforms researched human expression into governed, reproducible, reviewed, approved, and publishable media. It is not a generic clipping tool, not a prompt wrapper, not a generic editorial package engine, and not a partial launch. It must be built as the full documented system, in dependency order, with release blocked until a real brand cycle can run without manual database edits, hidden prompt surgery, direct provider tinkering, or approval bypass.

---

## 1. Project Context Analysis

### 1.1 Architectural Thesis

CMF STUDIO is a greenfield continuity project. The legacy system contains valuable intelligence, but its runtime fragmentation must not be inherited. The new architecture keeps the intelligence and replaces the runtime shape.

The governing architecture is:

```text
Human activation creates source expression.
Python contracts govern product truth.
DSPy compiles structured reasoning.
Pi orchestrates approved actions.
Durable workflows execute long-running work.
Receipts preserve every consequential transition.
Humans approve truth, taste, consent, and publication.
```

The deepest architectural correction is that media production does not start at editing. It starts before the interview, in research saturation, interviewer resonance, Matrix of Edging, and Narrative State Induction. The system therefore has two levels of extraction:

1. **Live guest extraction:** The Operator uses Narrative State Induction to help the guest access authentic, non-centroid speech.
2. **Transcript/source extraction:** DSPy and review workflows extract Expression Moments from grounded source artifacts, timestamps, anchor hits, and route evidence.

The second level is not a substitute for the first. It is downstream of it.

### 1.1A Legacy Intentional Orchestration

The old CCF and CMF modules are not only feature inventories. They are intentional orchestration modules: each one encodes a reasoned sequence for why a signal should be researched, induced, extracted, routed, rendered, validated, learned from, or rejected. CMF STUDIO must preserve that orchestration intent while replacing the old runtime.

The governing legacy organism model is:

```text
DNA / truth
-> RNA / contextual transcription
-> force
-> delivery
-> variation
-> phenotype
-> evaluation
```

For CMF STUDIO this means:

- **DNA / truth:** Emotional DNA, Voice DNA, Negative Space, SDA ontology, primitive canon, archetype constraints, Brand Context invariants, and consent policies.
- **RNA / transcription:** CRAL/SCRE findings, Context Premises, Audience Deep Trigger Maps, Trigger Matches, InvariantFieldPackets, RepresentationGeometryPackets, PrimitiveCandidatePackets, function stacks, depth profiles, variation profiles, and route recommendations.
- **Force:** primitive coalitions, edge products, emotional charge, activation steering, and anti-centroid pressure.
- **Delivery:** SFL, TTT, rhythmic structure, symbolic compression, strategic ambiguity, repetition with variation, archetype containers, and JIT Skill execution.
- **Variation:** asymmetry, salience distribution, resonance spacing, paradox retention, and controlled unpredictability.
- **Phenotype:** videos, carousels, meme visuals, poll visuals, reaction seeds, paper-cut scenes, teaching visuals, proof objects, and rendered asset packages.
- **Evaluation:** semantic, perceptual, sonic, route, commercial, memory, consent, and human-review receipts.

Every migrated legacy module that affects production must therefore preserve not only what it does, but also why it exists, where it sits in this organism, what upstream packets it requires, what downstream artifacts it authorizes, and which gates prevent misuse.

### 1.2 Functional Scope

| FR Module | Architectural Meaning |
|---|---|
| FR-CMF-01 Workspace, Tenant, Role, and Commercial Governance | Brand-scoped tenancy, RBAC, commercial policy, Command Bus enforcement |
| FR-CMF-02 Consent, Source, Likeness, and Voice Governance | Consent state machine, source truth, Voice-DNA Boost gates, lineage blocking |
| FR-CMF-03 Legacy Migration, JIT Skill Intelligence, and Spec Governance | Migration ledger, intentional orchestration records, registries, DSPy compilers, fixtures, evals, BMAD discipline |
| FR-CMF-04 Brand Genesis and Brand Context Versioning | Locked Brand Context Versions, 64-state acting library, paper-cut rig, creative libraries |
| FR-CMF-05 Research, Interview Intelligence, and Narrative State Induction | CRAL/SCRE, Emotional DNA, Context Premise, Guest Dossiers, Audience Reality Briefs, Matrix of Edging, Interview Asset Contracts |
| FR-CMF-06 Complete Expression Sessions, Extraction, Routing, and Guest Asset Packs | Recording, transcript alignment, Expression Moments, archetype routing, asset package specs |
| FR-CMF-07 Complete Editing Sessions, Scene Reproducibility, and Composition Control | SceneSpec, Ideogram 4 CompositionJob JSON, scene containers/components/subsystems, composition lineage, render contracts |
| FR-CMF-08 Provider, Renderer, GPU Worker, and Asset Assembly Operations | Provider adapters, SVRE/Aurore asset research, asset roll logic, Remotion, Motion Canvas, self-hosted ComfyUI Docker worker |
| FR-CMF-09 Evaluation, Review, Approval, and Publishing Intent | Evaluation receipts, review commands, approval gates, Publer adapter |
| FR-CMF-10 Memory, Neo4j Projection, Operations, and Recovery | Evidence-backed memory, rebuildable Neo4j projection, operations boards, recovery |

### 1.3 Non-Functional Drivers

- **Contract authority:** Pydantic models own semantic truth. TypeScript types, OpenAPI schemas, workflow payloads, renderer props, and client validators are generated projections.
- **Workflow reliability:** Long-running jobs must survive process restarts and provider failures.
- **Reproducibility:** Every output must trace from source recording and transcript through Interview Asset Contract, Expression Moment, Archetype Route, Asset Package Spec, Complete Editing Session, SceneSpec, provider jobs, render output, evaluation receipt, approval event, and Publishing Intent.
- **Consent enforcement:** Consent must be evaluated before provider processing, likeness use, Voice-DNA Boost, memory admission, publishing intent, and Publer scheduling.
- **Tenant isolation:** Organization and brand scope must apply across commands, events, storage, provider jobs, render contracts, receipts, memory, and Neo4j projections.
- **Provider replaceability:** Ideogram 4, GPT Image 2, Flux 2 Klein 9b, Qwen-Image-Layered, SAM3, ComfyUI, LavaSR, MOSS-TTS, Remotion, Motion Canvas, Telegram, transcript providers, and Publer must sit behind capability contracts.
- **No hidden autonomy:** Pi, DSPy, LLMs, Telegram, and UI surfaces must not mutate canonical state outside the Command Bus.

### 1.4 Scale and Complexity

**Primary domain:** AI media production, agentic creative operations, B2B SaaS, workflow orchestration, source-controlled media lineage.

**Complexity level:** Enterprise-grade internal production system.

**Complexity indicators:**

- multi-brand tenancy and role policy;
- consent, likeness, source truth, and synthetic voice governance;
- heavy provider orchestration and GPU worker scheduling;
- durable workflow state across interview, extraction, rendering, review, publishing, and memory;
- graph projection for relationship inspection;
- migration of 1686 legacy files into governed contracts, registries, fixtures, evals, and worker assets;
- AI reasoning programs that must be schema-validated and human-reviewable.

### 1.5 Cross-Cutting Concerns

- Consent and source truth block unsafe execution across every module.
- Brand Context Version immutability blocks visual identity drift.
- Receipt Chain records every meaningful workflow transition.
- Command Bus is the only state mutation path.
- Legacy migration can inform production only through approved migration targets.
- Neo4j is included now, but only as a rebuildable projection from canonical events.
- JIT Skill compilers are privileged intelligence modules, not generic few-shot prompt snippets.
- Scene reproducibility requires both legacy CMF manifest lineage and Ideogram 4 CompositionJob JSON lineage.
- Intentional orchestration rationale is required for migrated CCF/CMF modules: organism layer, source doctrine, inputs, outputs, gates, downstream proof, and known failure modes.
- CRAL/SCRE and SVRE/Aurore are engines, not background references. They must be expressed as typed contracts, provider/research adapters, fixtures, receipts, and eval targets when used.

---

## 2. Starter Template Evaluation

### 2.1 Selected Starter Strategy

CMF STUDIO should not use a generic full-stack SaaS starter as the architectural foundation. The product has unusual constraints that common starters do not encode: Pydantic-first contract authority, DSPy program registry, Pi command orchestration, durable media workflows, provider receipt chains, rebuildable graph projection, and CMF render lineage.

The selected starter strategy is:

```text
Custom Python-first hybrid monorepo scaffold
```

This is not from-scratch improvisation. It is a controlled scaffold derived from the Greenfield Agent Context and implemented with boring, well-supported tools.

### 2.2 Version Verification Notes

Version checks were performed on 2026-06-21 against official project or package sources. Package versions must still be pinned in the lockfiles at implementation time.

| Area | Decision | Current Verification |
|---|---|---|
| Python runtime | Pin core services to Python 3.13 initially; maintain CI lane for Python 3.14 when dependency matrix passes | Python 3.14.6 is latest source release; 3.13 remains active bugfix line |
| API framework | FastAPI | PyPI shows FastAPI 0.138.0, released 2026-06-20 |
| Contract models | Pydantic v2 | PyPI shows Pydantic 2.13.4, released 2026-05-06 |
| Reasoning framework | DSPy | PyPI shows DSPy 3.2.1, released 2026-05-05 |
| Durable workflows | Temporal Python SDK or approved equivalent | PyPI shows temporalio 1.29.0, released 2026-06-17 |
| ORM/mapping | SQLAlchemy 2.x with Alembic | PyPI shows SQLAlchemy 2.0.51, released 2026-06-15 |
| Canonical database | PostgreSQL 18 family | PostgreSQL docs identify 18 as current; 19 is beta only |
| Graph projection | Neo4j Python driver 6.x | Neo4j docs show Version 6 current; PyPI shows neo4j 6.2.0 |
| PWA | Next.js 16.x with React 19 | Next.js blog shows Next.js 16.2 available; React docs show React 19 line |
| Styling | Tailwind CSS 4.x | Tailwind blog shows v4.3 current |
| Testing | pytest | PyPI shows pytest 9.1.1, released 2026-06-19 |

### 2.3 Scaffold Principles

- Python package owns contracts, commands, events, workflows, registries, provider adapters, and receipts.
- TypeScript packages consume generated schemas only.
- The PWA and Telegram Mini App are UI surfaces over the same command and object model.
- Renderers are leaf runtimes. They do not own domain semantics.
- Provider adapters are replaceable capability modules.
- Legacy assets enter through migration packages, fixtures, evals, and worker assets.

### 2.4 First Initialization Step

The first implementation story should create the monorepo skeleton, Python package, contract-generation pipeline, CI checks, and initial domain envelopes. No product feature should be implemented before contract authority, command envelopes, event envelopes, and receipt envelopes exist.

---

## 3. Core Architectural Decisions

### AD-001: Python-First Harness

CMF STUDIO uses a Python-first Harness. Python owns the API, domain contracts, command validation, workflows, DSPy programs, provider adapters, migration tooling, receipt chain, and projection writers.

**Rationale:** The intelligence layer is schema-heavy and reasoning-heavy. Keeping Pydantic, DSPy, Pi orchestration, workflows, and provider adapters in one Python runtime prevents duplicated domain semantics and reduces TypeScript shadow-model risk.

### AD-002: TypeScript Is a Leaf Runtime

TypeScript is restricted to the PWA, Telegram Mini App, Telegram Bot client where needed, Remotion/Motion Canvas renderer surfaces, and generated contract consumers.

**Consequences:**

- No hand-authored TypeScript domain object may define canonical semantics.
- Generated TypeScript must be checked for drift in CI.
- Renderer props must originate from Pydantic `RenderContract`, `SceneSpec`, `LayerManifest`, `AnimationPlan`, or related contracts.

### AD-003: Pydantic Is Contract Authority

Every domain object, command, event, registry entry, workflow input, provider request, provider response, render contract, evaluation receipt, approval event, and memory admission is represented by a versioned Pydantic model.

**Consequences:**

- Unknown or incompatible fields are rejected according to model policy.
- Contract migrations are explicit and tested.
- DSPy predictions remain proposals until Pydantic validation and domain gates accept them.
- Generated clients and UI validators derive from Python models.

### AD-004: DSPy Owns Structured Reasoning, Not State

DSPy owns research synthesis, Context Premise compilation, Interview Asset Contract compilation, expression extraction, archetype routing, SceneSpec compilation, evaluation, anti-draft calibration, CBAR auditing, TTT transition evaluation, and JIT Skill compiler execution where reasoning benefits from compiled programs.

**Consequences:**

- Each production DSPy program declares an input Pydantic model, output Pydantic model, fixture set, evaluation threshold, optimizer artifact, and version.
- DSPy output cannot mutate business state directly.
- DSPy traces are evidence and telemetry, not canonical workflow state.

### AD-005: Pi Orchestrates Through Approved Tools and Commands

Pi Coding Agent is the behind-the-scenes orchestrator. Pi may retrieve context, choose approved DSPy programs, call tools, propose commands, coordinate specialist agents, and repair failed workflows. Pi may not write directly to production tables, store workflow state in chat, or invent unregistered command types.

### AD-006: Command Bus Is the Mutation Boundary

The Command Bus is the only path for state mutation. PWA, Telegram, Pi, DSPy, provider webhooks, and recovery jobs all use the same enforcement path.

Commands validate role, brand scope, consent, idempotency, cost policy, object state, provider capability policy, workflow state, and receipt writer availability.

### AD-007: PostgreSQL Is Canonical State

PostgreSQL is the canonical transactional store. It owns organizations, brand workspaces, users, roles, consent records, Brand Context Versions, source artifacts, sessions, expression moments, routes, asset package specs, editing sessions, provider jobs, render outputs, evaluation receipts, approval events, publishing intents, memory events, migration ledger entries, and event outbox.

### AD-008: Neo4j Is a Rebuildable Relationship Projection

Neo4j is included now as a relationship projection for brand, guest, session, expression, archetype, asset, approval, publishing, provider, and memory relationships.

**Boundary:** Neo4j helps answer relationship questions, but canonical truth remains PostgreSQL, events, contracts, object storage hashes, and receipts.

### AD-009: Durable Workflows Own Long-Running Execution

Temporal Python SDK or an approved equivalent durable workflow engine owns resumability, retries, signals, timers, worker coordination, and long-running state.

FastAPI enqueues or signals workflows, then returns command acknowledgement.

### AD-010: Provider Capability Registry

Every external model, renderer, transcript provider, publishing adapter, or GPU route is represented by a Provider Capability Record.

**Provider roles:**

- Ideogram 4: composition plate and `CompositionJob` JSON provider.
- GPT Image 2: image asset provider and iterative edit provider.
- Flux 2 Klein 9b: identity-preserving edit and repair provider.
- Qwen-Image-Layered: layer decomposition provider.
- SAM3: segmentation and tracking provider.
- LavaSR: audio restoration provider.
- MOSS-TTS: Voice-DNA Boost bridge provider under strict gates.
- Remotion: deterministic social video renderer.
- Motion Canvas: procedural explainer renderer.
- Self-hosted ComfyUI Docker: GPU workflow execution provider on AWS or Google Cloud, 24GB or 32GB VRAM.
- Publer: publishing adapter, never system of record.

### AD-011: Ideogram 4 CompositionJob Is First-Class Lineage

Ideogram 4 `CompositionJob` JSON is a first-class reproducibility artifact. Ideogram is a Composition Director, not the final identity renderer and not the final text authority.

Complete Editing Sessions store `CompositionJob`, prompt hash, constraints, output requirements, composition plate URI, provider metadata, composition analysis, downstream edits, selected brand layers, final text plan, evaluation receipts, and approval state.

### AD-012: Legacy Repository Is Read-Only Intelligence

The legacy repository is a read-only source for doctrine, registries, fixtures, provider templates, evaluation gates, reference implementations, and spec-writing protocols.

Every retained legacy asset has a migration ledger entry. Direct production imports from legacy runtime are blocked unless an explicit exception ADR is approved.

### AD-013: Human Review Is Product Architecture

Human review is not a manual workaround. It is a core product feature. Evaluation receipts inform but do not replace approval.

### AD-014: Canonical Pipeline Stages Govern Agent Autonomy

The repaired PRD pipeline is an architecture contract. Every autonomous action must belong to a canonical pipeline stage with an entry object, exit object, allowed actor, pre-execution validation contract, and post-execution receipt.

Pi may coordinate agents, DSPy programs, deterministic services, provider adapters, renderers, and durable workflows, but Pi cannot reorder the pipeline, skip consent/source/Brand Context/routing/evaluation/approval/publishing/memory gates, or treat a chat trace as durable state.

**Required orchestration objects:**

- `OrchestrationRun`: top-level execution record for a brand cycle, expression session, asset package, render job, migration run, or spec-writing run.
- `StageExecutionPlan`: selected stage, active object, allowed action, agent/service owner, required inputs, and expected exit object.
- `ValidationContract`: pre-execution success/failure definition, thresholds, forbidden patterns, required evidence, and required receipts.
- `AgentHandoffPacket`: structured packet passed between orchestrator, worker, validator, reviewer, provider adapter, renderer, or projection builder.
- `SkillInvocationRecord`: record of JIT skill, DSPy program, registry snapshot, compiler fingerprint, contrastive prompt layer, critic result, and synthesis result.
- `FailureReceipt`: explicit blocked, failed, partial, terminal, or quarantined execution evidence.
- `FrictionReceipt`: operational evidence that a stage required unusual manual intervention, model disagreement, missing context, provider delay, or reviewer uncertainty.
- `HumanHandoffRequest`: request for human truth, taste, consent, identity, source, cost, or publication decision.

**Consequences:**

- Epics, stories, architecture modules, and tech specs must cite the pipeline stage they implement.
- Durable workflows own wait/retry/resume behavior; Pi owns coordination and repair proposals.
- Validators cannot be the same actor as the worker for high-risk actions.
- Receipts, not chat messages, prove progress.

---

## 4. System Topology

### 4.1 Logical Architecture

```text
Operator / Reviewer
  -> PWA Control Tower
  -> Telegram Bot / Telegram Mini App

PWA / Telegram
  -> Python Agent Gateway
  -> Command Bus
  -> Durable Workflow Engine
  -> Domain Services
  -> Provider Adapters / Renderers
  -> Evaluation / Review / Approval
  -> Publishing Intent / Publer Adapter
  -> Memory Admission / Neo4j Projection
```

### 4.2 Runtime Responsibility Split

| Runtime | Owns | Must Not Own |
|---|---|---|
| Python API/Harness | contracts, commands, workflows, registries, DSPy, providers, receipts, projection writers | UI layout, renderer-specific presentation |
| PWA | deep operator workflows, review boards, forms, dashboards | canonical domain semantics |
| Telegram Bot | notifications, quick actions, status commands | separate business state |
| Telegram Mini App | lightweight previews, contextual mobile operations | deep editing or canonical persistence |
| Remotion/Motion Canvas | deterministic rendering from typed props | source truth, approval, final business state |
| ComfyUI Docker worker | approved GPU workflow execution | business decisions or direct canonical writes |
| Neo4j | derived relationship projection | canonical transactional truth |
| Publer | scheduling and publishing adapter | approval authority or asset lineage |

### 4.3 Canonical Domain Chain

```text
Organization
-> BrandWorkspace
-> ConsentRecordVersion
-> BrandGenesisSession
-> BrandContextVersion
-> ResearchField / GuestDossier / AudienceRealityBrief
-> InterviewAssetContract
-> CompleteExpressionSession
-> ExpressionMoment
-> ArchetypeRoute
-> AssetPackageSpec
-> CompleteEditingSession
-> SceneSpec
-> ProviderJob
-> RenderOutput
-> EvaluationReceipt
-> ApprovalEvent
-> PublishingIntent
-> PublerPublishingResult
-> BrandMemoryEvent / InterviewerMemoryEvent / RouteMemoryEvent
-> Neo4j projection nodes and relationships
```

### 4.4 Data Ownership Rules

- PostgreSQL owns canonical records.
- Object storage owns immutable source and derived artifacts.
- Neo4j owns derived relationship projection.
- Vector indexes, if added, are retrieval aids only.
- Provider systems own their external job state, mirrored by provider receipts.
- Publer owns external scheduling execution, mirrored by Publishing Intent outcomes.

### 4.5 Canonical Pipeline Execution Architecture

The architecture mirrors the PRD pipeline as an execution contract. Product stages are not optional phases. They are typed lanes that define which objects can move, which workflow owns movement, which agent or service may act, and which proof must exist before the next lane starts.

| Stage | Product Stage | Owning Workflow / Service | Entry Object | Exit Object | Required Proof |
|---:|---|---|---|---|---|
| 0 | Legacy inventory and migration | `MigrationWorkflow`, `MigrationService`, `SpecGovernanceService` | legacy source path, file hash, source doctrine | `MigrationLedgerEntry`, `LegacyOrchestrationIntentRecord` | migration disposition, target contract/DSPy/fixture/eval, no direct import |
| 1 | Workspace, commercial, consent, source intake | `WorkspaceService`, `CommercialPolicyService`, `ConsentPolicyService`, `SourceIngestionWorkflow` | organization, brand, guest/client, offer, source files | `BrandWorkspace`, `CommercialPolicy`, `ConsentRecordVersion`, `SourceArtifactManifest` | brand scope, role policy, `$29/week` or `$99/month`, consent receipt |
| 2 | Brand Genesis | `BrandGenesisWorkflow` | intake, consent, source media, visual/voice inputs | `BrandContextVersion`, acting library, rig manifest, creative libraries | human lock, identity/likeness receipts, immutable brand version |
| 3 | Research and context engineering | `InterviewPreparationWorkflow`, CRAL/Context DSPy programs | objective, sources, guest/audience evidence | `ResearchSnapshot`, `GuestDossier`, `AudienceRealityBrief`, `ContextPremise` | evidence provenance, freshness, contradiction notes, claim safety |
| 4 | Interview intelligence and induction planning | `InterviewPreparationWorkflow`, Matrix/Asset Contract compilers | dossier, audience reality, Context Premise, Emotional/Voice DNA | `NarrativeStateMap`, `InterviewAssetContract`, `InterviewDeck` | anti-centroid, saturation, collision, routeability, induction receipt |
| 5 | Complete Expression Session | `CompleteExpressionSessionWorkflow`, session quality service | contracts, recording config, consent, source protocol | `CompleteExpressionSession`, recording receipts, transcript jobs | source quality, consent compatibility, anchor hit log |
| 6 | Post-session extraction | `ExtractionService`, JIT Skill compilers, transcript alignment | transcript, timestamps, source artifacts, anchor hits | `ExpressionMoment`, quote candidates, extraction receipts | source-truth, boundary, anti-draft, anti-genericity, reviewer queue |
| 7 | Archetype and asset routing | `RoutingService`, archetype/derivative registries | approved Expression Moments, primitive activations | `AssetRouteReceipt`, rejected-route memory candidates | valid registry route, unsupported format rejection, route-fit score |
| 8 | Asset package planning | `AssetPackageService`, commercial policy | route receipts, offer type, source sufficiency | `AssetPackageSpec` | quota cannot force untruthful assets, no newsletters |
| 9 | Complete Editing Session | `CompleteEditingSessionWorkflow`, `SceneSpecCompiler` | package item, approved route, Brand Context Version | `CompleteEditingSession`, `SceneSpec`, `RenderContract` | source lineage, locked brand context, render policy |
| 10 | Scene planning and composition control | `SceneIntelligenceService`, Ideogram adapter | SceneSpec, asset-roll plan, scene rules | `CompositionJob`, composition analysis, layer plan | prompt hash, text-space rule, identity/text not finalized by Ideogram |
| 11 | Asset research and provider jobs | `AssetResearchService`, provider adapters, ComfyUI worker adapter | `VisualResearchQuery`, provider policy, brand assets | `AssetResearchManifest`, `ProviderReceipt`, generated/selected assets | licensing, provenance, cost, retry, worker receipt |
| 12 | Rendering and assembly | `RenderWorkflow`, Remotion/Motion Canvas, audio/caption services | RenderContract, layers, animation plan, audio/caption plan | `RenderOutput`, EDL, timeline, caption, sonic receipts | final text outside Ideogram, render manifest, source lineage |
| 13 | Evaluation, review, revision, approval | `EvaluationService`, `ReviewService`, CBAR auditor | render output, receipts, consent, evaluation targets | `EvaluationReceipt`, revision command, `ApprovalEvent` | source truth, identity, composition, voice, human approval |
| 14 | Publishing, memory, projection | `PublishingWorkflow`, `MemoryAdmissionService`, `ProjectionRebuildWorkflow` | approved asset, captions, platform variants, memory candidate | `PublishingIntent`, Publer outcome, `MemoryAdmission`, Neo4j projection event | Publer adapter receipt, evidence-backed memory, rebuildable projection |

### 4.6 Pipeline-to-Architecture Mapping Rules

- API routes may expose stage actions, but they do not own stage semantics.
- Commands mutate stage state only through the Command Bus.
- Workflows coordinate stage progress; services perform bounded domain decisions; DSPy programs propose structured reasoning outputs; provider adapters perform external execution.
- Each stage has a `ValidationContract` before execution and a receipt after execution.
- If a stage fails, the system records `FailureReceipt`, `FrictionReceipt`, `HumanHandoffRequest`, or quarantine state rather than silently skipping forward.
- Neo4j projection may help inspect relationships across stages, but it cannot authorize or block production state transitions.

---

## 5. Product Module Architecture

### 5.1 Workspace and Commercial Governance

**Purpose:** Govern brand-scoped production, roles, commercial access, command permissions, cost, quota, and retention.

**Core objects:** `Organization`, `BrandWorkspace`, `UserAccount`, `RoleAssignment`, `CommercialEntitlement`, `UsageLedgerEntry`, `CostReceipt`.

**Key commands:** `CreateBrandWorkspace`, `SwitchActiveBrandContext`, `AssignRole`, `UpdateCommercialEntitlement`, `RecordUsage`.

**Rules:**

- Customer-facing content charges are only `$29/week` trial Guest Asset Packs and `$99/month` Monthly Asset Engine.
- Extra internal cost policies may exist, but not extra customer-facing content tiers.
- Brand context must bind every query, command, storage path, provider job, and receipt.

### 5.2 Consent, Source, Likeness, and Voice Governance

**Purpose:** Make consent and source truth enforceable runtime gates.

**Core objects:** `ConsentRecordVersion`, `SourceArtifact`, `TranscriptRevision`, `SourceReference`, `VoiceBoostEligibilityReport`, `VoiceBridgeManifest`.

**State gates:**

- recording allowed;
- storage allowed;
- likeness generation allowed;
- derivative generation allowed;
- provider processing allowed;
- synthetic voice allowed;
- reuse allowed;
- publication allowed;
- memory admission allowed.

**Voice-DNA Boost policy:** Voice-DNA Boost is a structural repair exception. It requires consent, repair hierarchy exhaustion, duration caps, visual covering, evaluation receipts, and claim restrictions. It cannot deliver primary claims, medical advice, or decisive confessions.

### 5.3 Legacy Migration and JIT Skill Intelligence

**Purpose:** Preserve legacy intelligence without inheriting legacy runtime disorder.

**Core objects:** `LegacyAssetInventoryItem`, `MigrationLedgerEntry`, `LegacyOrchestrationIntentRecord`, `RegistryEntry`, `DSPyProgramSpec`, `FixtureSet`, `EvaluationTarget`, `JITSkillCompiler`.

**Migration targets:**

- Pydantic registry entries;
- DSPy programs;
- fixtures;
- evaluation datasets;
- worker assets;
- reference ports;
- obsolete/deprecated records.

**JIT Skill compiler rule:** JIT Skill compilers must operate on saturation context: source docs, transcript segments, guest dossier, audience reality, brand context, primitive candidates, prior evaluations, and failure corpora. They are allowed to draft, contrast, calibrate, and evaluate. They are not allowed to invent ungrounded content or mutate state directly.

**Intent preservation rule:** Each migrated orchestration-bearing module must record its product purpose, organism layer, cognitive or narrative problem solved, required inputs, emitted packets, gating logic, downstream consumers, failure modes, and proof obligations. A migrated module cannot be activated if it is only summarized as a prompt, vibe, style preference, or feature label.

**Priority legacy orchestration sources:** PRD-02 CCF Content Factory, PRD-03 CMF Media Factory, PRD-08 Conscious Primitives, the CCP Biological Orchestration Model, CSIP v3 Voice/Emotional DNA, Sovereign CRAL, SVRE/Aurore, CMF Master Scene Intelligence, CMF Creative Subsystems, Scene Containers, Scene Components, and the Conscious Asset Strategy Guide.

### 5.4 Brand Genesis and Brand Context Versioning

**Purpose:** Manufacture and lock the brand's reusable creative universe.

**Core objects:** `BrandGenesisSession`, `BrandContextVersion`, `GenesisClearanceCertificate`, `IdentityPack`, `ActingLibraryVersion`, `ActingReference`, `RigManifest`, `MicroSemioticAnchor`, `MotionRecipe`, `SfxAsset`, `CompositionPreference`.

**Brand Genesis output:**

- 64-state acting library;
- paper-cut avatar rig;
- visual constitution;
- prop and object library;
- micro-semiotic anchor library;
- motion recipes;
- SFX library;
- composition preferences;
- locked `BrandContextVersion`.

**Lock rule:** Completed assets retain their original Brand Context Version forever. Changes fork a new version.

### 5.5 Research and Interview Intelligence

**Purpose:** Improve source expression before capture.

**Core objects:** `ResearchField`, `ResearchEvidence`, `CRALFinding`, `GuestDossier`, `AudienceRealityBrief`, `ContextPremise`, `AudienceDeepTriggerMap`, `EmotionalDNAProfile`, `VoiceDNAProfile`, `InterviewerResonanceContext`, `MatrixOfEdgingBrief`, `NarrativeStateMap`, `InterviewAssetContract`, `InterviewDeck`.

**DSPy programs:** `CRALResearchCompiler`, `GuestDossierCompiler`, `AudienceRealityBriefCompiler`, `ContextPremiseCompiler`, `AudienceDeepTriggerMapCompiler`, `EmotionalDNAExtractor`, `VoiceDNAProfileCompiler`, `MatrixOfEdgingCompiler`, `InterviewAssetContractCompiler`, `InterviewDeckCompiler`, `TTTTransitionEvaluator`.

**Induction rule:** Expression states are induction modes. Archetypes define output structure. The system must not route assets by expression state alone.

**CRAL rule:** CRAL/SCRE research must preserve the seven JIT moments and their source-discipline separation: Relevant, Believable, Undeniable, Resonant, Surprising, Irrefutable, and Relatable. Research evidence must carry provenance, category, confidence, freshness, contradiction notes, and downstream interview use.

**Root-down expression rule:** Emotional DNA is the root system for Voice DNA. Interview preparation and extraction must distinguish what the guest believes, how they construct expression, and the emotional path through which activation becomes language. Context Premise compilation must produce audience-side trigger structure that can be matched against guest or coach emotional architecture rather than generic audience persona text.

### 5.6 Complete Expression Sessions and Asset Pack Routing

**Purpose:** Capture authentic human expression and route it into supported asset package outputs.

**Core objects:** `CompleteExpressionSession`, `RecordingConfiguration`, `RecordingArtifact`, `TranscriptRevision`, `TimestampedAnchorHit`, `ExpressionMoment`, `ArchetypeRoute`, `AssetPackageSpec`.

**Guest Asset Pack standard:**

- 4 videos;
- 2 carousels;
- 2 meme visuals;
- 2 poll visuals;
- 2-3 reaction seeds when source material supports them.

**Unsupported format rule:** Deliverable formats must come from Core Content Archetype, Asset Derivative, Meme Mechanism, Reaction Archetype, and CMF Render Mode registries.

### 5.7 Complete Editing Sessions and Scene Reproducibility

**Purpose:** Compile approved expression into reproducible media production sessions.

**Core objects:** `CompleteEditingSession`, `CreativeState`, `SceneSpec`, `SceneContainerPlan`, `SceneComponentSelection`, `CreativeSubsystemDecision`, `AssetRollPlan`, `CompositionJob`, `CompositionPlan`, `AssetSelection`, `ProviderJob`, `LayerManifest`, `AnimationPlan`, `RenderContract`, `RenderOutput`, `EvaluationReceipt`.

**Reproducibility contract:** Each output must preserve source expression session ID, source expression moment ID, route, asset derivative, locked Brand Context Version, SceneSpec, Ideogram 4 `CompositionJob` JSON when used, prompt hash, provider metadata, composition plate URI, composition analysis, downstream edit jobs, selected brand layers, final text plan, render contracts, evaluation receipts, and approval state.

**Scene intelligence rule:** CMF scene planning must preserve the legacy distinction between fixed biological arc containers, interchangeable scene components, and creative subsystems. SceneSpecs must be able to explain why a HOOK, SETUP, CHALLENGE, TURNING_POINT, RESOLUTION, or VISION container exists, which component fills it, which creative subsystem gates were consulted, and how A/B/C/D/E-roll assets support the scene's narrative, sonic, visual, and cultural function.

### 5.8 Provider, Renderer, GPU Worker, and Asset Assembly

**Purpose:** Execute governed provider and renderer work without hidden scripts.

**Core objects:** `ProviderCapabilityRecord`, `ProviderRequest`, `ProviderResponse`, `ProviderReceipt`, `VisualResearchQuery`, `VisualCandidate`, `ImageResolutionMap`, `AssetResearchManifest`, `AssetRollCandidate`, `GpuWorkerJob`, `ComfyWorkflowAsset`, `TimelineManifest`, `CaptionManifest`, `AudioMixManifest`.

**ComfyUI worker rule:** The ComfyUI route uses a self-hosted Docker GPU worker on AWS or Google Cloud with 24GB or 32GB VRAM. It executes approved hashed workflow JSON templates in batch mode, writes receipts, uploads artifacts, reports cost, checkpoints per asset, and shuts down after queued work completes.

**Visual and asset research rule:** SVRE/Aurore-style visual research is preserved as a sovereign asset-research engine. It retrieves, scores, licenses, and routes candidates by emotional state, symbolic role, contradiction value, cultural proximity, known-person validity, source quality, and brand alignment. In CMF STUDIO it must be adapted to the approved provider stack and self-hosted ComfyUI worker; superseded legacy execution services are context only.

**Asset roll rule:** A-Roll, B-Roll, C-Roll, D-Roll, and E-Roll are not loose media buckets. They are intentional asset roles: narrative/emotional anchor, cinematic/emotional layer, visual explanation layer, authentic lived-reality layer, and cultural/status/pattern-interrupt layer. Asset assembly must preserve the selected role and the reason it was selected.

### 5.9 Evaluation, Review, Approval, and Publishing

**Purpose:** Ensure quality, truth, identity, consent, and publication authority are reviewable.

**Core objects:** `EvaluationReceipt`, `ReviewDecision`, `RevisionRequest`, `ApprovalEvent`, `PublishingIntent`, `PublerJob`, `PublishingOutcome`.

**Evaluation layers:** source truth, archetype fit, expression depth, identity consistency, likeness, composition, style, motion restraint, platform fit, negative space, micro-semiotic anchor fit, routeability, and publishing readiness.

**Publishing rule:** Publer receives approved Publishing Intents. Publer is never the canonical approval state, caption truth, source lineage, or publication authority.

### 5.10 Memory, Neo4j Projection, Operations, and Recovery

**Purpose:** Learn from evidence while keeping memory reversible and operations recoverable.

**Core objects:** `MemoryAdmissionCandidate`, `BrandMemoryEvent`, `InterviewerMemoryEvent`, `RouteMemoryEvent`, `RejectedPatternMemoryEvent`, `PublishingPerformanceMemoryEvent`, `ProjectionCheckpoint`, `OperationalIncident`, `RecoveryAction`.

**Memory rule:** Memory admission requires source evidence, provenance, consent compatibility, confidence, scope, and reversal ability.

**Neo4j projection nodes:** Brand, Guest, Session, ExpressionMoment, Archetype, AssetDerivative, RenderMode, CompleteEditingSession, ProviderJob, EvaluationReceipt, ApprovalEvent, PublishingIntent, MemoryEvent.

### 5.11 Orchestration and Spec Compiler Kernel

**Purpose:** Make autonomous execution and spec generation auditable, stage-bound, and compatible with the legacy BMAD/ERA3 discipline updated for Python/Pydantic/DSPy/Pi.

**Core orchestration objects:** `OrchestrationRun`, `StageExecutionPlan`, `ValidationContract`, `AgentHandoffPacket`, `SkillInvocationRecord`, `FailureReceipt`, `FrictionReceipt`, `HumanHandoffRequest`.

**Core spec-governance objects:** `SpecWritingProtocol`, `TechSpecWorkflow`, `TechSpecSourcePacket`, `FilesReadReceipt`, `RequirementTrace`, `PipelineStageTrace`, `CBARCheck`, `SpecAuditReceipt`.

**DSPy programs:** `EpicStoryCompiler`, `TechSpecCompiler`, `TechSpecAuditor`, `CBARAuditor`, `RequirementTraceCompiler`.

**Rules:**

- BMAD remains the workflow shell: it orders PRD, architecture, epics, stories, and tech specs.
- CMF architecture remains the implementation authority: Python contracts, DSPy programs, Pi orchestration, durable workflows, provider adapters, receipts, and tests define how specs are realized.
- Every generated tech spec must cite exact files read, FR-CMF requirements, PRD pipeline stage, architecture module, commands, contracts, workflows, services, provider boundaries, tests, and legacy migration context where applicable.
- A tech spec cannot be accepted if it omits CBAR tension/failure/resolution/proof, skips source files, relies on old TypeScript-first assumptions, or fails to name Pydantic/DSPy/Pi implications.

---

## 6. API and Command Surface

### 6.1 API Groups

FastAPI exposes the external API. Routes are grouped by product boundary:

```text
/api/v1/health
/api/v1/auth
/api/v1/organizations
/api/v1/brands
/api/v1/consent
/api/v1/legacy-migration
/api/v1/registries
/api/v1/brand-genesis
/api/v1/research
/api/v1/interviews
/api/v1/expression-sessions
/api/v1/expression-moments
/api/v1/asset-packages
/api/v1/editing-sessions
/api/v1/scenes
/api/v1/provider-jobs
/api/v1/renders
/api/v1/evaluations
/api/v1/reviews
/api/v1/publishing-intents
/api/v1/memory
/api/v1/operations
/api/v1/orchestration
/api/v1/projections
/api/v1/spec-governance
/api/v1/webhooks/telegram
/api/v1/webhooks/providers
/api/v1/webhooks/publer
```

### 6.2 Command Pattern

Every state-changing endpoint wraps a command:

```json
{
  "command_id": "cmd_...",
  "command_type": "CreateCompleteExpressionSession",
  "organization_id": "org_...",
  "brand_id": "brand_...",
  "actor_id": "usr_...",
  "idempotency_key": "idem_...",
  "payload": {},
  "requested_at": "2026-06-21T00:00:00Z"
}
```

### 6.3 Command Validation Order

Commands validate in this order:

1. schema version;
2. actor authentication;
3. role permission;
4. organization and brand scope;
5. object existence;
6. object state transition;
7. consent policy;
8. cost and quota policy;
9. idempotency;
10. provider capability policy if applicable;
11. confirmation requirement;
12. receipt writer availability.

### 6.4 Error Envelope

All API errors use a consistent envelope:

```json
{
  "error": {
    "code": "CONSENT_SCOPE_BLOCKED",
    "message": "The requested action is not allowed by the current consent record.",
    "details": {},
    "correlation_id": "corr_...",
    "retryable": false
  }
}
```

### 6.5 Event Naming

Domain events use past-tense names:

```text
BrandWorkspaceCreated
ConsentRecordVersioned
BrandContextVersionLocked
InterviewAssetContractCompiled
CompleteExpressionSessionStarted
ExpressionMomentApproved
AssetPackageSpecGenerated
CompleteEditingSessionCreated
SceneSpecCompiled
ProviderJobCompleted
EvaluationReceiptCreated
ApprovalEventRecorded
PublishingIntentConfirmed
MemoryAdmissionApproved
Neo4jProjectionUpdated
OrchestrationRunStarted
StageExecutionPlanCreated
ValidationContractRecorded
AgentHandoffPacketCreated
SkillInvocationRecorded
FailureReceiptCreated
HumanHandoffRequested
TechSpecCompiled
SpecAuditReceiptCreated
```

---

## 7. Data Architecture

### 7.1 Database Strategy

PostgreSQL is canonical. SQLAlchemy models map database persistence, but Pydantic contracts remain semantic authority. Alembic or an equivalent migration system owns schema evolution.

### 7.2 Core Table Families

```text
identity:
  organizations
  brand_workspaces
  user_accounts
  role_assignments
  commercial_entitlements

governance:
  consent_record_versions
  command_log
  domain_events
  audit_receipts
  cost_receipts

orchestration:
  orchestration_runs
  stage_execution_plans
  validation_contracts
  agent_handoff_packets
  skill_invocation_records
  failure_receipts
  friction_receipts
  human_handoff_requests

legacy:
  legacy_inventory_items
  migration_ledger_entries
  migrated_registry_entries
  fixture_sets
  evaluation_targets

spec_governance:
  spec_writing_protocols
  tech_spec_workflows
  tech_spec_source_packets
  files_read_receipts
  requirement_traces
  pipeline_stage_traces
  cbar_checks
  spec_audit_receipts

brand_genesis:
  brand_genesis_sessions
  brand_context_versions
  genesis_clearance_certificates
  acting_references
  acting_library_versions
  rig_manifests
  micro_semiotic_anchors
  motion_recipes
  sfx_assets
  composition_preferences

research:
  research_fields
  research_evidence
  guest_dossiers
  audience_reality_briefs
  context_premises
  interviewer_resonance_contexts
  matrix_of_edging_briefs
  interview_asset_contracts
  interview_decks

expression:
  complete_expression_sessions
  recording_artifacts
  transcript_revisions
  timestamped_anchor_hits
  expression_moments
  archetype_routes
  asset_package_specs

production:
  complete_editing_sessions
  creative_states
  scene_specs
  composition_jobs
  composition_plans
  asset_selections
  provider_jobs
  layer_manifests
  animation_plans
  render_contracts
  render_outputs

review_publish:
  evaluation_receipts
  review_decisions
  revision_requests
  approval_events
  publishing_intents
  publer_jobs
  publishing_outcomes

memory_ops:
  memory_admission_candidates
  memory_events
  projection_checkpoints
  operational_incidents
  recovery_actions
```

### 7.3 Object Storage

Object storage holds immutable and derived artifacts:

```text
brands/{brand_id}/source/
brands/{brand_id}/transcripts/
brands/{brand_id}/brand-genesis/
brands/{brand_id}/acting-library/
brands/{brand_id}/rigs/
brands/{brand_id}/composition-plates/
brands/{brand_id}/render-previews/
brands/{brand_id}/render-finals/
brands/{brand_id}/provider-raw/
brands/{brand_id}/receipts/
brands/{brand_id}/publishing/
brands/{brand_id}/orchestration/
brands/{brand_id}/spec-governance/
```

All stored artifacts carry source hash, content hash, brand ID, object ID, and retention policy.

### 7.4 Immutability Rules

- Source artifacts are immutable after upload confirmation.
- Transcript revisions are append-only.
- Locked Brand Context Versions are immutable.
- Approved Expression Moments are immutable except for supersession records.
- Provider receipts are immutable.
- Evaluation receipts are immutable.
- Approval events are immutable.
- Publishing outcomes are immutable.

### 7.5 Projection Rules

The domain event outbox drives Neo4j, search indexes, vector retrieval indexes if introduced, analytics, and operational dashboard summaries.

Projection failures do not roll back canonical commands. They create projection incidents and retry jobs.

---

## 8. Durable Workflow Architecture

### 8.1 Workflow Engine Responsibility

Durable workflows own long-running execution, provider retries, batch GPU worker control, signals from PWA and Telegram, checkpoints, timeout policy, compensation, and terminal failure states.

### 8.2 Core Workflows

#### BrandGenesisWorkflow

```text
create BrandGenesisSession
-> validate consent and source media
-> generate identity/acting candidates
-> evaluate and repair acting references
-> create paper-cut rig candidates
-> validate rig previews
-> create creative libraries
-> request human review
-> lock BrandContextVersion
-> write GenesisClearanceCertificate
```

#### InterviewPreparationWorkflow

```text
create ResearchField
-> gather ResearchEvidence
-> compile GuestDossier
-> compile AudienceRealityBrief
-> compile ContextPremise
-> compile InterviewerResonanceContext
-> compile MatrixOfEdgingBrief
-> compile InterviewAssetContracts
-> compile InterviewDeck
-> pass pre-session quality gate
```

#### CompleteExpressionSessionWorkflow

```text
create CompleteExpressionSession
-> validate recording configuration and consent
-> ingest recording artifacts
-> align transcript revisions
-> detect anchor hits
-> extract ExpressionMoment candidates
-> route candidates
-> request reviewer decisions
-> generate AssetPackageSpec
```

#### CompleteEditingSessionWorkflow

```text
create CompleteEditingSession
-> freeze source and Brand Context Version
-> compile SceneSpec
-> create CompositionJob if Ideogram route is used
-> run provider jobs
-> build layer manifests and animation plans
-> render previews/finals
-> evaluate outputs
-> request review
-> record approval or revision
```

#### PublishingWorkflow

```text
draft PublishingIntent
-> validate consent, approval, captions, platform variants
-> confirm human approval
-> submit to Publer
-> track Publer status
-> write publishing outcome
-> propose memory admission
```

#### MigrationWorkflow

```text
inventory legacy asset
-> classify asset type
-> hash source
-> assign migration target
-> convert or port if approved
-> create fixtures/evals
-> review migration
-> activate or deprecate
```

#### ProjectionRebuildWorkflow

```text
select projection checkpoint
-> read canonical events
-> rebuild Neo4j graph
-> validate counts and relationships
-> publish projection health
```

#### OrchestrationRunWorkflow

```text
open OrchestrationRun
-> read active production object
-> resolve PRD pipeline stage
-> create StageExecutionPlan
-> create ValidationContract
-> dispatch allowed agent, DSPy program, service, provider adapter, renderer, or workflow
-> receive receipt
-> validate receipt against ValidationContract
-> advance, retry, block, quarantine, or request human handoff
-> close stage with audit event
```

#### TechSpecCompilerWorkflow

```text
open TechSpecWorkflow
-> require linked epic and story
-> collect Files Read from PRD, architecture, Product Brief, Legacy Inventory, and source docs
-> compile RequirementTrace and PipelineStageTrace
-> resolve contracts, commands, workflows, tables, providers, renderers, and tests
-> run TechSpecCompiler DSPy program
-> run CBARAuditor and RSCS signal-density checks
-> create SpecAuditReceipt
-> request human review when source coverage, CBAR proof, or architecture alignment is incomplete
-> mark accepted, revision_requested, or blocked
```

### 8.3 Failure Taxonomy

| Failure | Handling |
|---|---|
| provider timeout | retry with policy, then terminal failure or manual review |
| partial provider output | preserve completed artifacts and receipts, retry only missing work |
| consent change | block future processing, quarantine affected pending jobs |
| source artifact corruption | terminal failure requiring re-upload |
| evaluation hard fail | route to revision or rejection |
| GPU worker interruption | resume from checkpoint or requeue incomplete asset |
| Publer failure | keep Publishing Intent internal and mark external failure |
| Neo4j projection failure | continue canonical workflows and retry projection |
| orchestration stage mismatch | block execution and require corrected StageExecutionPlan |
| missing ValidationContract | block agent/provider/renderer execution |
| missing Files Read or source trace in spec workflow | block tech spec acceptance |
| CBAR hard fail | require spec/story repair before implementation |

---

## 9. Application Surface Architecture

### 9.1 PWA Control Tower

The PWA is the primary deep-work surface.

Required areas:

- Portfolio Dashboard;
- Brand Dashboard;
- Brand Genesis Wizard;
- Consent and Source Review;
- Migration Ledger;
- Registry Browser;
- Interview Intelligence Studio;
- Live Interview Mode;
- Expression Session Review;
- Asset Package Board;
- Production Board;
- Scene Review;
- Render Review;
- Evaluation Receipt Viewer;
- Publishing Calendar;
- Memory Review;
- Operations Board.

### 9.2 Telegram Bot

Telegram Bot handles render-ready notifications, batch-finished notifications, failed worker alerts, quick approve/reject/regenerate actions, consent or approval blockers, Publer scheduling confirmation, and links back into the PWA.

Telegram Bot does not own separate state.

### 9.3 Telegram Mini App

Telegram Mini App handles lightweight previews, contextual render status, mobile review snippets, quick decision support, object deep links, and authenticated continuity with PWA state.

It is not the deep editing surface.

### 9.4 Optional Client Review

Client or guest review may be added only as a governed review surface with scoped access, consent-aware previews, and no canonical editing authority unless explicitly added by a future approved requirement.

---

## 10. Provider and Rendering Architecture

### 10.1 Provider Adapter Interface

Every provider adapter implements:

```text
validate_capability(request)
estimate_cost(request)
submit_job(request)
poll_or_receive_result(job_id)
normalize_response(response)
write_provider_receipt(response)
```

### 10.2 Provider Receipt Fields

Provider receipts include provider name, capability ID, model or workflow version, adapter version, input artifact hashes, prompt hash if applicable, parameters, output artifact hashes, cost, retry count, status, failure details, correlation ID, and created domain event.

### 10.3 Ideogram 4 Route

Ideogram 4 produces composition plates and composition analysis. It never owns final identity or final text.

Fast route:

```text
SceneSpec
-> CompositionJob
-> Ideogram composition plate
-> evaluation
-> background/plate use if allowed
```

Premium route:

```text
SceneSpec
-> CompositionJob
-> Ideogram composition plate
-> composition analysis
-> approved brand layers
-> Remotion/Motion Canvas text and assembly
-> evaluation
-> approval
```

### 10.4 Deterministic Renderer Routes

Remotion and Motion Canvas consume typed render contracts:

- selected brand layers;
- rig manifest;
- final text plan;
- captions;
- motion recipes;
- SFX plan;
- scene timings;
- audio mix manifest;
- platform variants.

### 10.5 Self-Hosted ComfyUI Docker Route

ComfyUI jobs are batch-first:

```text
queued typed job
-> start GPU worker
-> load hashed workflow JSON
-> bind typed inputs
-> execute
-> checkpoint outputs
-> upload artifacts
-> write receipts
-> report costs
-> shut down when queue drains
```

The architecture explicitly excludes RunningHub as the execution route.

---

## 11. Security, Privacy, and Governance

### 11.1 Data Classes

- public generated assets;
- private source recordings;
- private transcripts;
- likeness assets;
- voice assets;
- synthetic voice artifacts;
- provider credentials;
- publishing credentials;
- memory events;
- migration artifacts;
- receipts and audit logs.

### 11.2 Core Security Rules

- Encrypt sensitive data at rest and in transit.
- Use scoped, short-lived object access.
- Store provider tokens in managed secrets.
- Validate Telegram `initData` server-side.
- Apply organization and brand scope to every command.
- Require confirmation for high-impact commands.
- Enforce consent before provider processing and publishing.
- Keep Publer credentials separate from publication authority.

### 11.3 Prompt and External Content Safety

Research documents, transcripts, source uploads, and external provider outputs are untrusted content. They may be used as evidence, but they cannot override system policy, command validation, consent policy, or architecture rules.

### 11.4 Voice and Likeness Governance

Voice-DNA Boost and likeness generation are controlled by explicit consent, source reference, repair hierarchy, eligibility receipt, visual covering, duration cap, claim restriction, and human approval.

---

## 12. Implementation Patterns and Consistency Rules

### 12.1 Naming

| Area | Pattern | Example |
|---|---|---|
| Python packages | snake_case | `ccp_studio.contracts.expression` |
| Pydantic models | PascalCase | `CompleteExpressionSession` |
| Commands | imperative PascalCase | `CreateCompleteEditingSession` |
| Events | past-tense PascalCase | `ExpressionMomentApproved` |
| Tables | snake_case plural | `complete_expression_sessions` |
| Columns | snake_case | `brand_context_version_id` |
| API routes | kebab-case plural | `/api/v1/expression-sessions` |
| JSON fields | snake_case | `source_artifact_id` |
| TypeScript components | PascalCase | `RenderReviewPanel` |
| TypeScript files | kebab-case | `render-review-panel.tsx` |

### 12.2 Contract Pattern

- Pydantic models live under `ccp_studio/contracts`.
- Shared fields use common base types.
- All models have version policy.
- All state-changing payloads have explicit command models.
- All external payloads are normalized before entering domain state.
- Generated TypeScript is generated by CI or a deterministic script, never hand-edited.

### 12.3 Service Pattern

Domain services:

- accept validated Pydantic input;
- do not parse raw HTTP payloads;
- do not call provider SDKs directly unless they are provider adapter services;
- emit domain events through the event writer;
- write receipts for consequential actions.

### 12.4 Repository Pattern

Repositories:

- hide SQLAlchemy query details;
- require `organization_id` and `brand_id` for brand-scoped objects;
- never return cross-brand data;
- support optimistic concurrency where state transitions are sensitive;
- do not perform business decisions.

### 12.5 Error Codes

Stable error codes include:

```text
VALIDATION_FAILED
PERMISSION_DENIED
BRAND_SCOPE_VIOLATION
CONSENT_SCOPE_BLOCKED
STATE_TRANSITION_INVALID
PROVIDER_CAPABILITY_UNAVAILABLE
PROVIDER_JOB_FAILED
EVALUATION_HARD_FAIL
APPROVAL_REQUIRED
PUBLISHING_BLOCKED
PROJECTION_LAGGING
LEGACY_IMPORT_BLOCKED
```

### 12.6 Status Pattern

State machines use explicit statuses, not loose booleans:

```text
draft
ready_for_review
approved
rejected
revision_requested
blocked
terminal_failed
completed
```

### 12.7 Receipt Pattern

Every receipt includes receipt ID, receipt type, command ID or workflow ID, actor ID, organization ID, brand ID, object reference, source references, decision, evidence, created event ID, correlation ID, and created timestamp.

### 12.8 Testing Pattern

Tests are organized by risk:

- unit tests for contracts and domain services;
- contract tests for Pydantic schema compatibility and generated TypeScript drift;
- workflow tests for state transitions, retries, and compensation;
- integration tests for API command paths;
- provider adapter tests with fake provider responses;
- golden tests for migrated legacy fixtures;
- eval tests for DSPy programs and JIT Skill compilers;
- end-to-end tests for a full brand cycle.

### 12.9 Legacy Pattern

Legacy code can only appear as source path in migration ledger, hashed fixture, reference implementation note, worker asset if approved, generated registry entry, DSPy program source material, or eval target. It cannot be imported as production runtime.

---

## 13. Project Structure and Boundaries

### 13.1 Complete Project Tree

```text
ccp-studio/
  README.md
  pyproject.toml
  uv.lock
  package.json
  pnpm-lock.yaml
  docker-compose.yml
  .env.example
  .github/
    workflows/
      ci.yml
      contract-drift.yml
      evals.yml
  docs/
    architecture.md
    bmm-workflow-status.yaml
    sprint-artifacts/
    adr/
  ccp_studio/
    api/
      main.py
      dependencies.py
      routers/
    contracts/
      base.py
      identity.py
      tenancy.py
      commercial.py
      consent.py
      source.py
      legacy.py
      registries.py
      brand_genesis.py
      creative_libraries.py
      research.py
      interview.py
      expression.py
      archetype_routes.py
      asset_packages.py
      production.py
      providers.py
      rendering.py
      evaluation.py
      approval.py
      publishing.py
      memory.py
      operations.py
      orchestration.py
      spec_governance.py
      commands.py
      events.py
      receipts.py
    domain/
      command_bus.py
      policies/
      services/
      repositories/
    dspy_programs/
      registry.py
      guest_dossier_compiler.py
      audience_reality_brief_compiler.py
      context_premise_compiler.py
      matrix_of_edging_compiler.py
      interview_asset_contract_compiler.py
      expression_moment_extractor.py
      archetype_router.py
      scene_spec_compiler.py
      semantic_critic.py
      anti_draft_calibration_program.py
      cbar_auditor.py
      ttt_transition_evaluator.py
      epic_story_compiler.py
      tech_spec_compiler.py
      tech_spec_auditor.py
      requirement_trace_compiler.py
      jit_skill_compilers/
    workflows/
      worker.py
      brand_genesis.py
      interview_preparation.py
      complete_expression_session.py
      complete_editing_session.py
      publishing.py
      migration.py
      orchestration.py
      tech_spec_compiler.py
      projection_rebuild.py
    providers/
      capability_registry.py
      base.py
      ideogram.py
      gpt_image_2.py
      flux_2_klein_9b.py
      qwen_image_layered.py
      sam3.py
      comfyui_worker.py
      lavasr.py
      moss_tts.py
      transcript_provider.py
      publer.py
    rendering/
      render_router.py
      timeline_manifest.py
      caption_manifest.py
      audio_mix_manifest.py
    persistence/
      database.py
      models/
      migrations/
      outbox.py
      object_storage.py
    projections/
      neo4j_writer.py
      neo4j_schema.py
      projection_worker.py
    observability/
    security/
    cli/
  apps/
    pwa/
      app/
      components/
      features/
      generated/
      lib/
      tests/
    telegram-miniapp/
      src/
      generated/
      tests/
    telegram-bot/
      src/
      tests/
    remotion-renderer/
      src/
      generated/
      tests/
    motion-canvas-renderer/
      src/
      generated/
      tests/
  packages/
    generated-types/
    generated-openapi/
    ui/
    renderer-contracts/
  worker-assets/
    comfyui-workflows/
    fixtures/
  tests/
    unit/
    integration/
    contracts/
    workflows/
    providers/
    evals/
    e2e/
    spec_governance/
```

### 13.2 Requirement to Structure Mapping

| Requirement Module | Primary Locations |
|---|---|
| FR-CMF-01 | `contracts/tenancy.py`, `contracts/commercial.py`, `domain/policies`, `api/routers/brands.py` |
| FR-CMF-02 | `contracts/consent.py`, `contracts/source.py`, `domain/policies/consent_policy.py` |
| FR-CMF-03 | `contracts/legacy.py`, `contracts/spec_governance.py`, `dspy_programs/jit_skill_compilers`, `dspy_programs/tech_spec_compiler.py`, `worker-assets/fixtures`, `tests/evals`, `tests/spec_governance` |
| FR-CMF-04 | `contracts/brand_genesis.py`, `contracts/creative_libraries.py`, `workflows/brand_genesis.py` |
| FR-CMF-05 | `contracts/research.py`, `contracts/interview.py`, `dspy_programs/*compiler.py` |
| FR-CMF-06 | `contracts/expression.py`, `contracts/archetype_routes.py`, `contracts/asset_packages.py` |
| FR-CMF-07 | `contracts/production.py`, `contracts/rendering.py`, `providers/ideogram.py` |
| FR-CMF-08 | `providers/`, `rendering/`, `worker-assets/comfyui-workflows` |
| FR-CMF-09 | `contracts/evaluation.py`, `contracts/approval.py`, `contracts/publishing.py`, `providers/publer.py` |
| FR-CMF-10 | `contracts/memory.py`, `contracts/orchestration.py`, `projections/`, `domain/services/operations_service.py`, `workflows/orchestration.py` |

### 13.3 Boundary Rules

- `contracts/` has no dependency on API, persistence, providers, UI, or workflows.
- `domain/` depends on contracts and repositories, not provider SDKs directly.
- `providers/` depends on contracts and writes receipts through approved domain paths.
- `workflows/` orchestrates domain services and provider adapters.
- `apps/` consumes generated types and API clients, not Python domain packages.
- `rendering/` consumes render contracts and emits render artifacts, not business decisions.

---

## 14. Tech Spec and Story Handoff Rules

The architecture must feed BMad epics and stories before implementation tech specs.

### 14.1 Epic Rules

- Epics must be user-value oriented, not technical layers.
- Each epic maps to specific FR-CMF requirements.
- Each epic names the canonical PRD pipeline stages it covers.
- Each epic names architecture components and active primitive families.
- Each epic includes downstream tech-spec implications, validation contracts, and receipt obligations.

### 14.2 Story Rules

Each story must include:

- `As a [role], I want [action], so that [benefit]`;
- BDD acceptance criteria;
- technical notes with contracts, commands, tables, routes, and workflow references;
- canonical pipeline stage, entry object, exit object, and receipt;
- active primitive or legacy intelligence mapping;
- failure examples for critical gates.

### 14.3 Tech Spec Rules

Every tech spec must be compiled through the CMF-updated BMAD/ERA3 discipline. BMAD provides workflow order; the CMF architecture provides implementation truth. A valid tech spec therefore cannot preserve old TypeScript-first assumptions or generic backend-integration sections.

Every tech spec must include:

1. Files Read;
2. Overview;
3. Context for Development;
4. PRD and FR-CMF Requirement Trace;
5. Canonical Pipeline Stage Trace;
6. Greenfield Integration and Legacy Migration Context;
7. Architecture Component Map;
8. Implementation Plan;
9. Primary Pydantic Output Schema;
10. Commands, Events, Workflows, and Receipts;
11. DSPy Programs, JIT Skills, or Deterministic Services;
12. Provider, Renderer, Projection, or Worker Boundaries where applicable;
13. CBAR Constraint Pass;
14. Acceptance Criteria with failure examples;
15. Dependencies;
16. Testing Strategy;
17. Observability, Recovery, and Rollback;
18. Spec Audit Receipt.

For CMF, the old "Existing Backend Integration" section becomes "Greenfield Integration and Legacy Migration Context." It must list exact Pydantic contracts, command models, services, durable workflows, DSPy programs, JIT skills, legacy source paths, migration targets, provider boundaries, renderer boundaries, projection boundaries, and tests.

### 14.4 Tech Spec Compiler Workflow Rules

The `TechSpecCompilerWorkflow` is required for implementation specs:

1. Open a `TechSpecWorkflow` linked to an approved epic/story.
2. Collect `FilesReadReceipt` entries for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, and feature-specific source docs.
3. Compile `RequirementTrace` entries to FR-CMF modules and acceptance criteria.
4. Compile `PipelineStageTrace` entries naming stage, entry object, exit object, validation contract, receipt, and allowed actor/service.
5. Run `TechSpecCompiler` to draft the spec from saturated source context.
6. Run `CBARAuditor` using tension, failure scenario, resolution demand, and downstream proof.
7. Run `TechSpecAuditor` for architecture drift, legacy import risk, provider boundary risk, missing tests, and receipt gaps.
8. Produce `SpecAuditReceipt` with accepted, revision_requested, or blocked status.

### 14.5 Tech Spec Rejection Conditions

A tech spec is rejected if it:

- omits exact files read;
- lacks an FR-CMF requirement trace;
- lacks a PRD pipeline stage trace;
- uses direct legacy runtime imports;
- uses old TypeScript-first core assumptions;
- calls provider SDKs from domain logic;
- lacks Pydantic schema ownership;
- treats DSPy output as canonical state;
- allows Pi, Telegram, Publer, Neo4j, provider adapters, or renderers to bypass the Command Bus;
- omits CBAR proof or failure examples;
- omits tests for consent, brand scope, receipts, recovery, and projection behavior where relevant.

---

## 15. Architecture Validation Results

### 15.1 Coherence Validation

**Status:** Passed.

The architecture is coherent because contract authority, command mutation, durable workflows, provider adapters, receipts, review gates, and projection rules all point to the same source-of-truth model:

```text
Pydantic contracts -> Command Bus -> domain events -> receipts -> projections
```

There is no competing persistence path for Pi, DSPy, provider adapters, Telegram, or Publer.

The repaired architecture also enforces the PRD pipeline as an execution contract:

```text
Pipeline stage -> StageExecutionPlan -> ValidationContract -> typed command/workflow/service -> receipt -> next stage or human handoff
```

### 15.2 Requirements Coverage

**Status:** Passed.

All 10 FR modules are mapped to product modules, contract families, workflows, service boundaries, and project structure locations. All major NFRs are covered: performance, reliability, security, scalability, provider interoperability, auditability, accessibility, maintainability, and contract governance.

### 15.3 Implementation Readiness

**Status:** Ready for epics and stories.

Architecture is ready to feed the BMad epic/story workflow and downstream tech specs. The next output should be `docs/epics.md`, repaired so every epic and story maps to FR-CMF modules, canonical pipeline stages, entry/exit objects, validation contracts, receipts, legacy sources, and architecture components.

### 15.4 Gap Register

| Gap | Severity | Resolution |
|---|---|---|
| No separate UX specification exists yet | Important | Stories should use PRD journeys, PWA surface list, Telegram cockpit doctrine, and Brand Genesis V3 until a dedicated UX spec is created |
| Exact transcript provider is not selected | Important | Keep behind `TranscriptProvider` capability contract |
| Exact cloud primary can be AWS or Google Cloud | Important | Architecture supports both; ComfyUI worker must run as Docker GPU job on 24GB/32GB VRAM |
| Exact local model artifacts are not pinned | Important | Pin model artifact, tokenizer, serving image, quantization, and eval threshold in Provider Capability Registry |
| Exact auth provider is not selected | Important | Preserve FastAPI auth boundary, Telegram `initData` verification, RBAC, and short-lived asset access |

### 15.5 Architecture Completeness Checklist

- [x] Project context analyzed.
- [x] PRD FR modules mapped.
- [x] Legacy Inventory incorporated.
- [x] Python/Pydantic/DSPy/Pi runtime decision applied.
- [x] PRD canonical pipeline mirrored as architecture execution contract.
- [x] Orchestration objects defined: OrchestrationRun, StageExecutionPlan, ValidationContract, AgentHandoffPacket, SkillInvocationRecord, FailureReceipt, FrictionReceipt, and HumanHandoffRequest.
- [x] Neo4j included as rebuildable projection.
- [x] Ideogram 4 `CompositionJob` JSON included as first-class lineage.
- [x] Self-hosted ComfyUI Docker GPU worker included.
- [x] Provider names corrected to GPT Image 2 and Flux 2 Klein 9b.
- [x] RunningHub excluded.
- [x] External unsupported content formats excluded.
- [x] No partial launch framing.
- [x] Legacy BMAD/ERA3 tech-spec workflow updated for Python/Pydantic/DSPy/Pi.
- [x] Implementation patterns defined.
- [x] Project structure defined.
- [x] Handoff rules for epics, stories, and tech specs defined.

---

## 16. Architecture Completion Summary

### 16.1 Workflow Completion

**Architecture Decision Workflow:** Complete  
**Total Steps Completed:** 8  
**Document Location:** `docs/architecture.md`  

### 16.2 Final Architecture Deliverables

- Complete architecture decision document.
- Product module architecture for all 10 FR-CMF modules.
- Pydantic/DSPy/Pi/FastAPI/Temporal/PostgreSQL/Neo4j architecture decisions.
- Provider and renderer architecture.
- Scene reproducibility and Ideogram 4 lineage rules.
- Legacy migration and JIT Skill compiler rules.
- Canonical pipeline execution architecture and orchestration objects.
- Python/DSPy/Pi-compatible tech-spec compiler workflow.
- Implementation patterns for AI agent consistency.
- Project structure and boundaries.
- Validation and handoff rules.

### 16.3 First Implementation Priority

The first implementation story must scaffold the Python-first monorepo, Pydantic contract kernel, command/event/receipt envelopes, generated TypeScript pipeline, CI contract-drift checks, and initial test structure.

No feature implementation should begin before the contract and command spine exists.

### 16.4 Next Work Product

Proceed to BMad epics and stories:

```text
PRD -> Architecture -> Epics and Stories -> Tech Specs -> Implementation
```

The architecture is now ready to serve as the technical source of truth for `docs/epics.md`.
