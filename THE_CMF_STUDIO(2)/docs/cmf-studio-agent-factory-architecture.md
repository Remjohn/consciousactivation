---
title: "CMF Studio Agent Factory Architecture"
status: "draft-canonical"
created_at: "2026-06-22"
runtime_target: "Python / Pydantic v2 / DSPy / Pi / FastAPI / durable workflows"
source_prd: "THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md"
source_architecture: "docs/architecture.md"
source_pipeline_map: "docs/cmf-studio-pipeline-map.md"
companion_intelligence_model: "docs/cmf-studio-intelligence-operating-model.md"
related_specs:
  - "docs/tech-specs/TS-CMF-001-contract-kernel-command-spine.md"
  - "docs/tech-specs/TS-CMF-002-pipeline-stage-orchestration-records.md"
  - "docs/tech-specs/TS-CMF-003-python-dspy-pi-bmad-spec-workflow.md"
  - "docs/tech-specs/TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md"
  - "docs/tech-specs/TS-CMF-028-cral-context-premise-emotional-dna-and-root-down-induction.md"
  - "docs/tech-specs/TS-CMF-036-complete-editing-session-creation-from-approved-source.md"
requires_legacy_inventory: true
---

# CMF Studio Agent Factory Architecture

## 1. Purpose

CMF Studio should not begin by inventing a list of agents. It should begin by defining the Factory: departments, production responsibilities, stage ownership, proof obligations, and the tools required for each department to act safely.

Agents are then derived from the Factory. A CMF agent is not a personality label. A CMF agent is a named, typed, accountable role contract that can be invoked only through the Python Agent Gateway, a `StageExecutionPlan`, a `ValidationContract`, and an `AgentHandoffPacket`.

This document clarifies:

- the difference between agents, sub-agents, hooks, extensions, tools, stable skills, and JIT skills;
- how agent intelligence is assembled from constitutions, standards, primitives, rules, protocols, memory, skills, tools, evaluations, and receipts;
- how Google ADK and Agents CLI patterns should influence CMF without replacing the current backend;
- which named departments and agents the Factory needs;
- which agent contracts should be built first on top of the existing backend;
- why each agent is architecturally fit for its assigned work.
- how each agent, sub-agent, hook, extension, skill, registry, and eval is named with a short traceable persona code.

The companion intelligence model is `docs/cmf-studio-intelligence-operating-model.md`. This Factory document defines who exists and what they own. The intelligence model defines how each entity thinks, perceives, decides, acts, remembers, and is governed.

## 2A. Persona Naming Standard

All Factory entities must use the canonical persona code format:

```text
DDD-XXXXXXX-TT
```

`DDD` is the three-character department code, `XXXXXXX` is the exactly seven-character service code, and `TT` is the two-character entity type. Example: `RES-VISRSCH-AG` means Research Department, Visual Research service, Agent.

The code is not decoration. It is the stable operational identity used in:

- `AgentRoleSpec.agent_key`;
- `SubAgentRoleSpec.sub_agent_key`;
- hook, extension, skill, registry, and eval specs;
- `AgentHandoffPacket`;
- `ValidationContract`;
- `SkillInvocationRecord`;
- `EvaluationReceipt`;
- audit logs, UI filters, stories, tech specs, and generated ADK/Agents CLI adapters.

Display names and personas may be human-friendly, such as "Aurore Visual Research Agent", but the code must reveal what the entity serves. Do not encode only a poetic name into the service code.

The canonical registry of names is `docs/cmf-studio-agent-factory-registry.md`.

## 2. Files and References Read

| Source | Use |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for pipeline, Agent Gateway, Pi orchestration, CCF-to-CMF continuity, pricing, and provider constraints. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF authority for agents, JIT skills, CRAL, Context Premise, Emotional DNA, extraction, routing, rendering, review, memory, and Neo4j projection. |
| `docs/cmf-studio-pipeline-map.md` | Canonical department and object spine from intake to memory. |
| `docs/architecture.md` | Architecture authority for Python, Pydantic, DSPy, Pi, Command Bus, durable workflows, Agent Gateway, and orchestration records. |
| `docs/tech-specs/TS-CMF-002-pipeline-stage-orchestration-records.md` | Existing spec for `OrchestrationRun`, `StageExecutionPlan`, `ValidationContract`, `AgentHandoffPacket`, receipts, and Pi handoff. |
| `docs/tech-specs/TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md` | Existing spec for JIT skill compiler saturation, contrastive prompt layers, anti-draft calibration, and `SkillInvocationRecord`. |
| `src/ccp_studio/contracts/orchestration.py` | Existing backend contracts for orchestration runs, stage plans, validation contracts, handoff packets, and receipts. |
| `src/ccp_studio/contracts/agent_gateway.py` | Existing backend contracts for agent action requests and gateway decisions. |
| `src/ccp_studio/contracts/skills.py` | Existing backend contracts for skill invocation records, JIT compilers, DSPy program specs, saturation bundles, and skill receipts. |
| `src/ccp_studio/services/agent_gateway.py` | Current constrained Pi Agent Gateway implementation. |
| Google ADK documentation | External design reference for agent config, sub-agent delegation, custom tools, skills, callbacks, graph workflows, routing, and Agents CLI deployment scaffolding. |

## 3. Google ADK and Agents CLI Adaptation

Google ADK is useful as an implementation and specification reference, but it is not the source of truth for CMF Studio.

What CMF should adopt:

- **Agent config discipline:** ADK can load agents from config files such as `root_agent.yaml`. CMF should generate ADK-compatible configs from typed `AgentRoleSpec` records instead of hand-authoring them as the canonical source.
- **Sub-agent delegation:** ADK uses root agents with `sub_agents`, where sub-agent descriptions guide delegation. CMF should use explicit `StageExecutionPlan` and `AgentHandoffPacket` routing first, and can export ADK sub-agent descriptions only as a runtime adapter.
- **Custom tools:** ADK treats function tools, agents-as-tools, and long-running tools as first-class. CMF must build its own tools because Pi has no built-in production tools. Every tool must be a Pydantic-shaped command, query, workflow signal, provider adapter, renderer action, or review action.
- **Skills:** ADK skills are self-contained units of functionality with instructions, resources, and tools. CMF should use this idea, but not all CMF skills are JIT. Some are stable operational skills that agents need every day.
- **Callbacks:** ADK callbacks intercept before/after agent, model, and tool execution. CMF hooks should use the same lifecycle idea, but they must enforce `ValidationContract`, source evidence, permission, cost, safety, and receipt rules.
- **Graph workflows:** ADK graph workflows combine deterministic nodes and AI reasoning. CMF already needs this shape through durable workflows and the canonical pipeline. The graph should be the CMF pipeline, not a hidden mega-prompt.
- **Agents CLI:** Agents CLI can scaffold and deploy ADK projects, add deployment files, and help create cloud runtime artifacts. It should be used later as an export/deployment path, not as the initial design authority.

Decision: CMF source of truth is `AgentFactorySpec -> DepartmentSpec -> AgentRoleSpec -> SubAgentRoleSpec -> ToolCapabilitySpec -> SkillBinding -> HookSpec`. ADK/Agents CLI can consume generated adapters after the Python contracts exist.

## 4. Vocabulary

### Factory

The Factory is the operating system of CMF Studio. It is a department-based production organization mapped to the canonical pipeline, primitive systems, source objects, proof obligations, and receipts.

The Factory answers:

- what departments exist;
- what each department owns;
- which stage objects enter and exit;
- which agents are accountable;
- which tools, skills, hooks, and workflows they may use;
- which receipts prove the work happened correctly.

### Department

A Department is a bounded production capability. It owns a group of pipeline stages, objects, validations, and proof obligations.

A department is not a UI area. It is an operational boundary. For example, the Research and Context Department owns CRAL findings, evidence, Context Premises, and Audience Reality, whether the action starts from PWA, Telegram, Pi, or an internal workflow.

### Agent

An Agent is a named accountable role contract.

An agent has:

- a goal;
- a department;
- a reason it is fit for that task;
- entry objects and exit objects;
- allowed tools;
- stable skills;
- optional JIT skill modes;
- sub-agents it can call;
- hooks that govern its lifecycle;
- validation contracts and receipts.

Technically, an agent is not a chat prompt and not necessarily a separate service. The canonical runtime artifact is `AgentRoleSpec`. The implementation may be a Python class, DSPy program, ADK adapter, workflow activity, deterministic service, provider worker, or human review queue, but all of those implementations must be generated from or bound to the same spec.

An Agent executes through this spine:

```text
OrchestrationRun
-> StageExecutionPlan
-> ValidationContract
-> AgentActionRequest
-> PiAgentGateway
-> allowed tool / workflow / DSPy program / deterministic service / adapter / human queue
-> typed output
-> receipt
-> AgentHandoffPacket
```

An `AgentRoleSpec` must define:

- persona code and display identity;
- department and service role;
- active object scope;
- entry and exit object contracts;
- allowed tools and blocked actions;
- stable skill and JIT skill bindings;
- sub-agent and hook bindings;
- memory access policy;
- eval bindings and readiness requirements;
- receipt and handoff obligations;
- ADK/Agents CLI adapter export metadata when relevant.

Agents may read from scoped read models, registry snapshots, source evidence bundles, and admitted memory allowed by policy. They may mutate production state only through Command Bus commands or durable workflow commands. They must not write directly to canonical tables, publish publicly, approve their own work, or treat generated adapter configs as source of truth.

An agent does not automatically mean a separate microservice or separate model. An agent may compile to:

- a Python role class behind the Agent Gateway;
- an ADK `LlmAgent` adapter;
- a DSPy program;
- a durable workflow activity;
- a deterministic service;
- a provider worker;
- a human review queue.

### Sub-Agent

A Sub-Agent is a scoped specialist under an agent or department.

Sub-agents are used when the work needs a narrow lens, a critic, a scorer, a hunter, or a validator that should not own the whole stage. A sub-agent should have a small input contract, a small output contract, and a single proof obligation.

Examples:

- `SourceTruthCritic` under `ExpressionMomentHunter`;
- `AntiCentroidCritic` under `NarrativeInductionDirector`;
- `KnownPersonValidityScout` under `SVREAuroreResearchLead`;
- `CompositionTextSpaceInspector` under `IdeogramCompositionDirector`.

Technically, a sub-agent is represented by `SubAgentRoleSpec`. It is bound to a parent `AgentRoleSpec`, a parent pipeline stage, and a narrow task contract. Sub-agents have smaller context windows, narrower input/output models, fewer tools, and stricter mutation rules than agents.

Sub-agent execution follows this shape:

```text
Parent AgentRoleSpec
-> parent AgentHandoffPacket or internal delegation request
-> SubAgentRoleSpec
-> bounded task execution
-> typed sub-agent output
-> sub-agent receipt
-> parent synthesis, blocker, or handoff
```

A sub-agent should be read/analysis first. It can call tools only when those tools are explicitly listed in the sub-agent spec and allowed by the parent stage validation contract. Sub-agent output never becomes canonical state by itself. The parent agent must carry the result into the normal command, workflow, review, or evaluation path.

Sub-agent receipts must link to:

- parent agent code;
- parent orchestration run;
- parent stage execution plan;
- source evidence refs;
- sub-agent input hash;
- sub-agent output hash;
- confidence or status;
- downstream parent decision or blocker.

### Tool

A Tool is executable capability.

Pi does not ship with CMF production tools. CMF must build them as explicit wrappers around:

- Command Bus commands;
- FastAPI endpoints;
- repository queries;
- workflow signals;
- DSPy program invocations;
- provider adapter actions;
- renderer actions;
- review and approval commands.

Every tool must have:

- a Pydantic input model;
- a Pydantic output model;
- permission scope;
- allowed pipeline stages;
- idempotency rule;
- receipt obligation;
- failure behavior.

### Hook

A Hook is deterministic lifecycle logic attached to an event boundary.

Hooks should not do creative reasoning. They enforce conditions around execution:

- before stage;
- after stage;
- before model;
- after model;
- before tool;
- after tool;
- before provider job;
- after provider job;
- before review;
- before publishing;
- before memory admission.

CMF hooks correspond to ADK callback ideas, but they are implemented as Python policies around the Agent Gateway, Command Bus, workflows, and receipts.

### Extension

An Extension is a packaged capability set that agents can use through tools and policies.

Examples:

- `cral_research_extension`;
- `legacy_inventory_extension`;
- `svre_aurore_extension`;
- `provider_adapter_extension`;
- `remotion_render_extension`;
- `telegram_review_extension`;
- `neo4j_projection_extension`.

An extension may contain tools, stable skills, schemas, fixtures, evals, and adapters. An extension is not a free permission surface. It must still be mounted into the Agent Gateway with scoped actions.

### Stable Operational Skill

A Stable Operational Skill is an enduring instruction/resource bundle an agent uses to perform recurring work.

These are not JIT. They are operational manuals and capability packs.

Examples:

- `legacy_migration_stewardship.skill`;
- `cral_evidence_review.skill`;
- `operator_review_evidence.skill`;
- `provider_job_recovery.skill`;
- `source_truth_audit.skill`;
- `scene_reproducibility_audit.skill`.

Stable operational skills can be loaded incrementally like ADK skills, but they should be versioned, tested, and attached to specific agent roles.

### JIT Skill Compiler

A JIT Skill Compiler is a run-specific compiler that assembles extraction, induction, contrast, anti-draft, routing, or evaluation intelligence from saturation context.

Historical correction: older JIT skills focused heavily on creative script writing and visual prompts. In current CMF Studio, JIT skills must primarily serve:

- live guest narrative induction;
- interview engineering;
- transcript extraction;
- expression moment detection;
- contrastive interpretation;
- anti-draft calibration;
- route support;
- evaluation support;
- Voice DNA support.

Downstream scene and visual prompt support may exist, but only after approved source expression and route receipts exist. It cannot become a generic visual prompt generator.

Current code already supports `live_guest_induction`, `transcript_extraction`, `routing_support`, `evaluation_support`, and `voice_dna_support`. The next contract repair should add explicit use modes for `interview_engineering` and `narrative_induction`, or clarify that they are covered by `live_guest_induction`.

### DSPy Program

A DSPy Program is a typed reasoning, compiler, or evaluator unit. It may be used by an agent, sub-agent, or JIT compiler.

DSPy does not own workflow state. DSPy returns typed predictions, candidate sets, scores, or critiques that must be validated into Pydantic objects and receipted.

### Workflow

A Workflow is a durable state machine. It owns retry, wait, resume, cancel, compensation, and quarantine behavior.

Agents may trigger workflows or operate inside workflow activities, but they do not replace workflows.

## 5. Required Agent Specification Shape

Every CMF agent must be declared with this structure before implementation:

```yaml
agent_id: "expression_moment_hunter"
display_name: "Expression Moment Hunter"
department_id: "expression_extraction"
status: "planned | active | deprecated"
runtime_form:
  primary: "python_role_contract"
  adapters:
    - "adk_llm_agent_optional"
    - "dspy_program"
    - "workflow_activity"
goal: "Find source-backed expression moments that can survive routing and production."
fit_rationale:
  - "The task requires transcript evidence, source boundaries, and anti-centroid judgment."
  - "It is downstream of interview intelligence and upstream of asset routing."
pipeline_stages:
  - 6
entry_objects:
  - "CompleteExpressionSession"
  - "TranscriptSegment"
  - "InterviewAssetContract"
exit_objects:
  - "ExpressionMomentCandidate"
  - "AnchorHit"
  - "ExtractionReceipt"
allowed_tools:
  - "query_transcript_segments"
  - "invoke_jit_skill_compiler"
  - "record_expression_moment_candidate"
blocked_actions:
  - "approve_expression_moment"
  - "publish_asset"
  - "mutate_brand_memory"
stable_skills:
  - "source_truth_audit.skill"
jit_skill_modes:
  - "transcript_extraction"
  - "narrative_induction"
sub_agents:
  - "source_truth_critic"
  - "anti_centroid_critic"
hooks:
  before_tool:
    - "require_stage_execution_plan"
    - "require_source_evidence_refs"
  after_tool:
    - "write_stage_execution_receipt"
validation_contract:
  success:
    - "candidate cites source segment and timestamp"
    - "candidate maps to at least one InterviewAssetContract"
  failure:
    - "candidate is generic"
    - "candidate cannot be traced to source"
required_receipts:
  - "SkillInvocationReceipt"
  - "ExtractionReceipt"
observability:
  - "correlation_id"
  - "stage_execution_plan_id"
  - "skill_invocation_receipt_id"
```

## 6. Factory Departments

CMF Studio should define 14 departments. This is the full Factory map. Not every department needs a separate service. Each department owns role contracts and stage responsibilities.

| ID | Department | Pipeline Stages | Primary Objects | Why It Exists |
|---|---|---:|---|---|
| D00 | Command and Runtime | all | `OrchestrationRun`, `StageExecutionPlan`, `ValidationContract`, `AgentHandoffPacket`, receipts | Keeps autonomy stage-bound, typed, auditable, and recoverable. |
| D01 | Legacy Intelligence and Skill Governance | 0, 3, 4, 6, 7 | Legacy inventory, migration ledger, registry entries, JIT compilers, fixtures, evals | Preserves CCF/CMF intentional orchestration without importing old runtime disorder. |
| D02 | Workspace, Consent, and Commercial Governance | 1 | organization, brand workspace, consent records, entitlements, roles | Prevents cross-brand leakage, consent drift, and pricing drift. |
| D03 | Brand Genesis and Identity | 2 | Brand Context, Emotional DNA, Voice DNA, acting library, paper-cut rig | Locks brand and identity before production begins. |
| D04 | Research and Context | 3 | CRAL findings, research evidence, Guest Dossier, Audience Reality Brief, Context Premise | Converts evidence and audience reality into interview-useful pressure. |
| D05 | Interview Intelligence | 4 | Matrix of Edging brief, Narrative State Map, First-Line Anchors, Interview Asset Contracts | Improves source expression before editing starts. |
| D06 | Expression Session and Extraction | 5, 6 | source artifacts, transcripts, expression moments, anchor hits, extraction receipts | Separates source truth from generic content generation. |
| D07 | Routing and Package Planning | 7, 8 | archetype route, asset derivative route, Guest Asset Pack spec | Converts expression into valid deliverables without unsupported formats. |
| D08 | Scene and Composition | 9, 10 | Complete Editing Session, SceneSpec, CreativeState, CompositionJob | Preserves scene reproducibility and composition intent. |
| D09 | Visual Research and Provider Operations | 10, 11 | AssetResearchManifest, provider jobs, visual candidates, ComfyUI receipts | Executes governed asset generation and sourcing without provider drift. |
| D10 | Rendering and Assembly | 11 | RenderContract, LayerManifest, AnimationPlan, captions, audio mix, render output | Turns scene plans into reproducible media outputs. |
| D11 | Evaluation and Review | 12, 13 | EvaluationReceipt, review state, approval blockers, Telegram/PWA review evidence | Prevents unapproved, untrue, off-brand, or unsafe assets from leaving the system. |
| D12 | Publishing and Memory | 14 | PublishingIntent, Publer receipt, MemoryAdmission, Neo4j projection event | Publishes only approved assets and learns from evidence-backed outcomes. |
| D13 | Operations and Reliability | all | FailureReceipt, FrictionReceipt, recovery action, readiness check | Keeps the Factory observable, resilient, and repairable. |

## 7. Named Agent Registry

The Factory should start with 73 named agent role contracts. This does not mean 73 services or 73 LLMs. It means 73 accountable role specifications that can compile into Python roles, DSPy programs, workflow activities, deterministic services, ADK agents, or human queues.

### D00 Command and Runtime

| Agent | Goal | Why Fit |
|---|---|---|
| `FactoryConductor` | Select the next valid stage and coordinate the Factory through Pi and the Agent Gateway. | It owns no domain artifact directly, so it can stay focused on orchestration integrity. |
| `StagePlanner` | Create `StageExecutionPlan` records from the active object and requested outcome. | It is fit because stage choice is a typed pipeline decision, not creative reasoning. |
| `ValidationContractWriter` | Define pre-execution success, failure, thresholds, evidence, and required receipts. | It prevents agents from acting before proof obligations exist. |
| `HandoffPacketClerk` | Create and verify `AgentHandoffPacket` payloads. | It keeps context scoped and prevents hidden prompt state from leaking across departments. |
| `ReceiptAuditor` | Verify returned receipts against validation contracts. | It is the neutral judge of whether a stage can advance. |

### D01 Legacy Intelligence and Skill Governance

| Agent | Goal | Why Fit |
|---|---|---|
| `ArchiveCartographer` | Map legacy files, modules, prompts, fixtures, assets, and registries. | It handles inventory and source classification before any migration decision. |
| `IntentMigrationSteward` | Preserve why each CCF/CMF module exists and what downstream proof it served. | It prevents legacy intelligence from being flattened into vague prompts. |
| `SkillCompilerLibrarian` | Register stable skills, JIT compilers, DSPy program specs, fixtures, and eval targets. | It owns skill governance rather than generation output. |
| `HiddenPromptGatekeeper` | Block hidden prompt stacks and legacy runtime coupling. | It is fit because it applies architectural policy at import and activation boundaries. |
| `EvaluationFixtureCurator` | Maintain fixtures, golden sets, hard negatives, and eval corpora. | It makes skill quality measurable instead of taste-based. |

### D02 Workspace, Consent, and Commercial Governance

| Agent | Goal | Why Fit |
|---|---|---|
| `WorkspaceSteward` | Maintain organization and brand workspace lifecycle. | It owns tenant/brand scope before creative work begins. |
| `ConsentWarden` | Enforce source, identity, voice, publishing, and review consent. | It is fit because consent must block actions before providers or publishing are invoked. |
| `CommercialPolicyKeeper` | Enforce `$29/week` trial Guest Asset Pack and `$99/month` Monthly Asset Engine only. | It prevents pricing drift and unsupported commercial packaging. |
| `RolePermissionMarshal` | Resolve human and agent permissions for each command. | It keeps Operator, Pi, provider, Telegram, and review powers separate. |

### D03 Brand Genesis and Identity

| Agent | Goal | Why Fit |
|---|---|---|
| `BrandGenesisArchitect` | Compile Brand Context from intake, evidence, identity assets, and micro-semiotics. | It owns the brand foundation before any source session or scene production. |
| `EmotionalDNAExtractor` | Identify root-down emotional structure, not generic tone. | It is fit because Emotional DNA is upstream of Voice DNA and interview activation. |
| `VoiceDNAProfiler` | Compile voice mechanics, negative space, rhythm, and expression constraints. | It keeps voice continuity grounded in evidence and reusable across stages. |
| `MicroSemioticCartographer` | Map visual symbols, identity cues, paper-cut signals, and brand semiotics. | It bridges Brand Genesis into scene and asset production. |
| `ActingLibraryDirector` | Govern 64-state acting library and expressive identity assets. | It preserves repeatable identity states instead of per-clip reinvention. |
| `PaperCutRigSupervisor` | Validate paper-cut rigs, anchors, layers, and preview readiness. | It is fit because rig integrity is structural, not prompt-based. |

### D04 Research and Context

| Agent | Goal | Why Fit |
|---|---|---|
| `CRALResearchLead` | Compile CRAL/SCRE evidence and seven JIT moments. | It owns source-discipline separation and epistemic friction. |
| `EvidenceCartographer` | Track provenance, confidence, contradiction, freshness, and inference boundaries. | It keeps research usable by agents without hallucinated certainty. |
| `AudienceRealityAnalyst` | Build audience reality from evidence rather than persona filler. | It is fit because CMF needs audience-side activation structure. |
| `ContextPremiseArchitect` | Convert evidence into Context Premises and trigger structures. | It bridges research into interview engineering and route readiness. |
| `CulturalSemioticScout` | Detect cultural, symbolic, and semiotic pressure relevant to the guest and audience. | It supplies nuance without allowing generic cultural assumptions. |
| `ClaimSafetyCritic` | Separate facts, claims, inferences, risks, and unsupported leaps. | It protects interviews and assets from brittle or false claims. |

### D05 Interview Intelligence

| Agent | Goal | Why Fit |
|---|---|---|
| `InterviewerPreInductionLead` | Prepare the Operator to activate better source expression. | It owns the pre-session bridge between research and human conversation. |
| `MatrixOfEdgingNavigator` | Apply the Matrix of Edging to pressure-map safe, abstract, or anti-centroid answers. | It is fit because it detects where the interview must move. |
| `NarrativeInductionDirector` | Guide live narrative induction from the guest before and during the session. | It owns the guest-level induction layer that generic script tools miss. |
| `AnchorSmith` | Produce First-Line Anchors, Depth Anchors, and follow-up moves. | It converts intelligence into usable interview action. |
| `InterviewAssetContractCompiler` | Define what production-ready expression must be captured. | It makes the interview accountable to downstream asset needs. |

### D06 Expression Session and Extraction

| Agent | Goal | Why Fit |
|---|---|---|
| `SourceIngestionSteward` | Ingest source artifacts, transcripts, timestamps, and provenance. | It owns source truth before extraction begins. |
| `TranscriptAlignmentSteward` | Align transcript segments to audio/video evidence. | It prevents quote and clip boundaries from drifting. |
| `ExpressionMomentHunter` | Detect source-backed expression moments. | It is fit because it hunts evidence, not generic ideas. |
| `NarrativeInductionExtractor` | Extract narrative state and guest-side meaning from transcript and guest context. | It captures the second extraction layer beyond raw transcript extraction. |
| `PrimitiveCoalitionMapper` | Map expression to primitives, SDA/SFL, and route-relevant coalitions. | It ties expression to the legacy primitive system. |
| `BoundaryControlReviewer` | Review extraction boundaries, unsupported claims, and clip limits. | It blocks weak or overextended extraction before routing. |

### D07 Routing and Package Planning

| Agent | Goal | Why Fit |
|---|---|---|
| `ArchetypeRouteCompiler` | Route expression moments into valid archetypes. | It owns format validity and prevents generic unsupported formats. |
| `AssetDerivativeRouter` | Map archetypes into videos, carousels, meme visuals, poll visuals, and reaction seeds. | It is fit because it owns the derivative registry, not content taste. |
| `MemeReactionRouter` | Select meme, reaction, and social-native routes when source supports them. | It keeps social formats grounded in route logic. |
| `GuestAssetPackPlanner` | Compile the trial Guest Asset Pack plan. | It enforces the documented package without adding newsletters or extra offers. |
| `UnsupportedFormatGuard` | Reject newsletters and unsupported generic deliverables. | It is the explicit anti-drift policy agent for format scope. |

### D08 Scene and Composition

| Agent | Goal | Why Fit |
|---|---|---|
| `CompleteEditingSessionProducer` | Create Complete Editing Sessions from approved source and route receipts. | It owns the wrapper that preserves why the asset exists. |
| `SceneSpecArchitect` | Compile SceneSpec, CreativeState, RenderContract, scene containers, and components. | It converts narrative intent into reproducible production instructions. |
| `IdeogramCompositionDirector` | Preserve Ideogram 4 `CompositionJob` JSON and composition plates when used. | It is fit because composition control is lineage-critical. |
| `SceneContainerPlanner` | Select scene containers, components, and creative subsystems. | It carries legacy CMF scene intelligence into typed production choices. |
| `AssetRollChoreographer` | Plan asset rolls, layer needs, movement, and media sourcing requests. | It bridges SceneSpec to visual research and rendering. |

### D09 Visual Research and Provider Operations

| Agent | Goal | Why Fit |
|---|---|---|
| `SVREAuroreResearchLead` | Retrieve, score, license, and route visual candidates. | It preserves sovereign visual research instead of generic image search. |
| `VisualCandidateScorer` | Score candidates by source quality, symbolic role, identity safety, and brand fit. | It separates visual taste from evidence-backed candidate selection. |
| `ProviderRouter` | Select approved providers by capability and policy. | It prevents provider drift and old RunningHub assumptions. |
| `ComfyUIWorkerCaptain` | Run approved hashed ComfyUI JSON workflows on self-hosted Docker GPU workers. | It is fit because ComfyUI execution is operational and receipt-heavy. |
| `IdentitySafetyInspector` | Protect known-person, guest, client, and brand identity constraints. | It blocks identity-risky provider outputs before review. |

### D10 Rendering and Assembly

| Agent | Goal | Why Fit |
|---|---|---|
| `RendererRouter` | Choose Remotion, Motion Canvas, Manim, or other approved renderer branches. | It owns deterministic render route selection. |
| `RemotionMotionCompiler` | Compile Remotion/Motion Canvas render inputs from SceneSpec and layer manifests. | It bridges typed scene plans into executable render artifacts. |
| `AudioCaptionTimelineEngineer` | Compile audio, captions, timeline, EDL, and mix plans. | It preserves voice, rhythm, and sound doctrine during assembly. |
| `LayerManifestAssembler` | Assemble layer manifests from provider outputs and source assets. | It keeps rendering reproducible and inspectable. |
| `RenderIntegrityInspector` | Validate render output, manifest integrity, and replayability. | It provides proof before evaluation and review. |

### D11 Evaluation and Review

| Agent | Goal | Why Fit |
|---|---|---|
| `SemanticCritic` | Evaluate source truth, route fit, and meaning preservation. | It is the primary reasoning critic for semantic quality. |
| `SourceTruthAuditor` | Verify every claim, quote, clip, and visual implication against source evidence. | It prevents assets from outrunning the interview. |
| `RouteFitCritic` | Evaluate whether the selected archetype and derivative truly fit. | It catches route mismatch before production waste compounds. |
| `BrandIdentityReviewer` | Evaluate identity, voice, visual consistency, and Emotional DNA continuity. | It protects the brand context lock. |
| `OperatorReviewConductor` | Prepare evidence-rich PWA and Telegram review packets. | It keeps the human Operator as final arbiter. |
| `VoiceDNABoostAdvisor` | Recommend Voice-DNA Boost only when a structural gap is detected. | It prevents voice repair from becoming arbitrary rewriting. |

### D12 Publishing and Memory

| Agent | Goal | Why Fit |
|---|---|---|
| `PublishingIntentSteward` | Create PublishingIntent only after approval, consent, lineage, and platform checks. | It keeps publishing human-approved and policy-bound. |
| `PublerAdapterOperator` | Queue approved posts through Publer and write outcome receipts. | It isolates external publishing integration from canonical state. |
| `MemoryAdmissionCurator` | Admit only evidence-backed memory. | It prevents memory from becoming ungrounded lore. |
| `MemoryCorrectionArchivist` | Correct, expire, reverse, or quarantine memory when evidence changes. | It keeps long-term learning reversible. |
| `Neo4jProjectionBuilder` | Rebuild relationship projection from canonical events. | It uses Neo4j as inspection/projection, not canonical write model. |

### D13 Operations and Reliability

| Agent | Goal | Why Fit |
|---|---|---|
| `RecoveryCoordinator` | Retry, resume, cancel, compensate, or quarantine failed workflows. | It owns recovery rather than hiding errors inside agents. |
| `FrictionTelemetryAnalyst` | Convert repeated agent friction into structured improvement signals. | It exposes where the Factory architecture is unclear or brittle. |
| `DependencySafetyOfficer` | Govern dependency additions, audits, and package risk. | It protects autonomous coding and runtime environments. |
| `EnvironmentParityInspector` | Verify local, CI, worker, and production parity. | It prevents agents from optimizing against false environments. |
| `OperationalReadinessMarshal` | Run readiness checks, restore drills, provider outage checks, and rollback planning. | It makes launch safety observable. |

## 8. Sub-Agent Patterns

Sub-agents should be created only when the work needs a narrow and reusable lens. The default sub-agent patterns are:

| Pattern | Use | Example Names |
|---|---|---|
| Hunter | Finds candidates from large source space. | `AnchorHitHunter`, `ExpressionMomentHunterLens`, `VisualEvidenceHunter` |
| Critic | Rejects weak, unsafe, generic, unsupported, or off-route outputs. | `AntiCentroidCritic`, `ClaimSafetyCritic`, `RouteFitCritic` |
| Scorer | Produces ranked scores against a rubric. | `VisualCandidateScorer`, `CompositionAccuracyScorer`, `VoiceContinuityScorer` |
| Compiler | Produces typed objects from saturated context. | `ContextPremiseCompiler`, `InterviewDeckCompiler`, `SceneSpecCompiler` |
| Gatekeeper | Blocks invalid transitions. | `ConsentGatekeeper`, `UnsupportedFormatGuard`, `ProviderPolicyGatekeeper` |
| Adapter | Translates between CMF contracts and external systems. | `PublerAdapter`, `TelegramReviewAdapter`, `ComfyUIWorkerAdapter` |
| Clerk | Creates receipts, handoff packets, and audit records. | `HandoffPacketClerk`, `ReceiptWriter`, `FilesReadReceiptClerk` |

Do not create a sub-agent if a deterministic validator, policy, repository query, or Pydantic model can do the work.

## 9. Skill Taxonomy

CMF should support four skill classes.

| Skill Class | JIT? | Purpose | Example |
|---|---:|---|---|
| Stable Operational Skill | No | Reusable instructions/resources for an agent's recurring operational behavior. | `source_truth_audit.skill`, `provider_job_recovery.skill` |
| Migrated Legacy Skill | No, until activated | Preserved legacy doctrine, prompts, rules, or configs awaiting conversion. | Old archetype prompts, CMF scene intelligence, SVRE/Aurore doctrine |
| JIT Skill Compiler | Yes | Compiles run-specific extraction, induction, interview, contrast, routing, or evaluation intelligence from saturation context. | `transcript_expression_extraction.jit`, `live_guest_induction.jit` |
| Tool-Linked Skill | Usually no | Teaches an agent how to use a specific tool family correctly. | `telegram_review_operations.skill`, `comfyui_worker_operations.skill` |

### JIT Skill Use Modes

Current code has:

- `live_guest_induction`;
- `transcript_extraction`;
- `routing_support`;
- `evaluation_support`;
- `voice_dna_support`.

Recommended next additions:

- `interview_engineering`;
- `narrative_induction`;
- `source_expression_contrast`;
- `scene_prompt_support_after_route`.

The last one must be blocked unless the asset has an approved `ExpressionMoment`, route receipt, and Complete Editing Session.

## 10. Required Tool Families

Because Pi has no built-in CMF tools, the harness must expose these tool families through explicit contracts.

| Tool Family | Required For | Example Tools |
|---|---|---|
| Stage and orchestration tools | all agents | `open_orchestration_run`, `create_stage_execution_plan`, `record_validation_contract`, `create_agent_handoff_packet`, `write_stage_receipt` |
| Command Bus tools | all mutating work | `submit_command`, `check_command_status`, `write_audit_receipt` |
| Source tools | extraction and review | `query_source_artifact`, `query_transcript_segments`, `get_timestamp_evidence`, `write_source_provenance` |
| Registry tools | routing, skills, providers | `query_archetype_registry`, `query_asset_derivative_registry`, `query_provider_capabilities`, `query_skill_registry` |
| DSPy tools | reasoning stages | `run_context_premise_compiler`, `run_matrix_compiler`, `run_extraction_compiler`, `run_route_selector`, `run_semantic_critic` |
| JIT skill tools | induction and extraction | `invoke_jit_skill_compiler`, `validate_saturation_context`, `record_skill_invocation_receipt` |
| Workflow tools | durable operations | `signal_workflow`, `resume_workflow`, `cancel_workflow`, `quarantine_workflow`, `compensate_workflow` |
| Provider tools | media generation | `create_provider_job`, `retry_provider_job`, `cancel_provider_job`, `record_provider_receipt` |
| Rendering tools | assembly | `compile_render_contract`, `run_render_job`, `validate_render_manifest` |
| Review tools | human gates | `create_review_packet`, `record_operator_decision`, `request_voice_dna_boost`, `record_approval_blocker` |
| Publishing tools | approved output only | `create_publishing_intent`, `queue_publer_draft`, `record_publer_outcome` |
| Memory and projection tools | learning | `submit_memory_candidate`, `correct_memory`, `rebuild_neo4j_projection` |
| Operations tools | reliability | `write_failure_receipt`, `write_friction_receipt`, `run_readiness_check`, `open_recovery_action` |

## 11. Hook System

Hooks are mandatory because agents should not carry safety rules in prompts only.

| Hook | Runs When | Responsibility |
|---|---|---|
| `before_stage_plan` | Before `StageExecutionPlan` creation | Verify active object and requested outcome are stage-compatible. |
| `before_agent_handoff` | Before `AgentHandoffPacket` creation | Verify department, agent status, permissions, required inputs, and blocked actions. |
| `before_model_call` | Before any LLM/DSPy model call | Assemble scoped context, strip forbidden hidden instructions, enforce token and evidence policy. |
| `after_model_call` | After model output | Validate schema, evidence refs, confidence, contradiction notes, and anti-genericity. |
| `before_tool_call` | Before tool execution | Verify Pydantic input, stage, permission, idempotency key, and cost/policy scope. |
| `after_tool_call` | After tool execution | Write receipt, attach evidence, update workflow state, or open failure/friction receipt. |
| `before_provider_job` | Before provider execution | Verify consent, identity, provider capability, cost policy, prompt hash, and approved template. |
| `after_provider_job` | After provider execution | Store provider metadata, output URI, cost, prompt hash, and provider receipt. |
| `before_review_packet` | Before PWA/Telegram review | Verify evidence-rich packet and remove unsupported actions. |
| `before_publish` | Before Publer or platform scheduling | Verify human approval, consent, lineage, evaluation, and platform variant. |
| `before_memory_admission` | Before memory update | Verify evidence, reversibility, correction path, and projection-only Neo4j rule. |

## 12. Runtime Architecture

The runtime should follow this sequence:

```text
PWA / Telegram / System Event
-> Python Agent Gateway
-> AgentFactoryRegistry
-> StageExecutionPlan
-> ValidationContract
-> AgentHandoffPacket
-> Tool / DSPy Program / JIT Skill / Workflow / Human Queue
-> Receipt
-> Command Bus or Workflow State Update
-> Next Stage or Human Handoff
```

The Agent Factory Registry must store:

- `DepartmentSpec`;
- `AgentRoleSpec`;
- `SubAgentRoleSpec`;
- `ToolCapabilitySpec`;
- `HookSpec`;
- `ExtensionSpec`;
- `SkillSpec`;
- `AgentSkillBinding`;
- `AgentRuntimeProfile`;
- `AgentEvaluationProfile`.

The Agent Gateway should refuse an action when:

- the agent is not registered;
- the department does not own the stage;
- the requested action is not in `allowed_actions`;
- the action is in `blocked_actions`;
- required stable skills are unavailable;
- a JIT skill is requested outside its approved use mode;
- the tool lacks a Pydantic contract;
- a required hook fails;
- the validation contract is missing;
- source evidence is missing;
- the action tries to bypass the Command Bus;
- the action tries to use Neo4j as canonical production state.

## 13. Initial Executable Team

The first executable team should be 18 agents, not all 73. The rest should be registered as planned role contracts.

| Build Order | Agent | Why First |
|---:|---|---|
| 1 | `FactoryConductor` | Nothing autonomous is safe until orchestration is stage-bound. |
| 2 | `StagePlanner` | Every action needs stage trace. |
| 3 | `ValidationContractWriter` | Agents need success/failure proof before acting. |
| 4 | `HandoffPacketClerk` | Context must be scoped before delegation. |
| 5 | `ReceiptAuditor` | Stage advancement depends on receipt verification. |
| 6 | `ArchiveCartographer` | Legacy Inventory remains mandatory context. |
| 7 | `IntentMigrationSteward` | Preserves why old CCF/CMF modules exist. |
| 8 | `SkillCompilerLibrarian` | JIT and stable skill governance must exist before skill execution. |
| 9 | `CRALResearchLead` | Context Premise and research pressure feed interview quality. |
| 10 | `ContextPremiseArchitect` | Converts evidence into working hypotheses. |
| 11 | `InterviewerPreInductionLead` | Starts the interview engineering layer. |
| 12 | `MatrixOfEdgingNavigator` | Core differentiation for non-centroid source expression. |
| 13 | `NarrativeInductionDirector` | Handles guest-level induction before and during session. |
| 14 | `SourceIngestionSteward` | Source provenance must exist before extraction. |
| 15 | `ExpressionMomentHunter` | First core extraction agent. |
| 16 | `NarrativeInductionExtractor` | Second extraction layer from transcript and guest context. |
| 17 | `ArchetypeRouteCompiler` | Valid route decisions are needed before asset planning. |
| 18 | `SemanticCritic` | Early evaluation prevents shallow outputs from propagating. |

After this team works end to end, add `GuestAssetPackPlanner`, `CompleteEditingSessionProducer`, `SceneSpecArchitect`, `IdeogramCompositionDirector`, `ProviderRouter`, `SVREAuroreResearchLead`, `RendererRouter`, `OperatorReviewConductor`, `PublishingIntentSteward`, and `MemoryAdmissionCurator`.

## 14. Build Sequence

### Step 1: Agent Factory Contracts

Add Pydantic contracts:

- `DepartmentSpec`;
- `AgentRoleSpec`;
- `SubAgentRoleSpec`;
- `ToolCapabilitySpec`;
- `HookSpec`;
- `ExtensionSpec`;
- `SkillSpec`;
- `AgentSkillBinding`;
- `AgentRuntimeProfile`.

### Step 2: Agent Factory Registry

Add repository and migration tables for the contracts. Seed the 14 departments and 73 planned agent role specs.

### Step 3: Gateway Integration

Update `PiAgentGateway` to resolve agent specs from the registry before creating `AgentHandoffPacket`.

### Step 4: Tool Registry

Wrap existing services and workflows as Pydantic tool capabilities. No agent can call an unregistered tool.

### Step 5: Stable Skill Loader

Add stable operational skills for the first 18 agents. These skills are not JIT. They describe operational procedure and evidence policy.

### Step 6: JIT Skill Repair

Repair `SkillUseMode` to explicitly support interview engineering and narrative induction. Keep JIT outputs evidence-backed, contrastive, and non-mutating.

### Step 7: Hook Engine

Implement before/after stage, agent, model, tool, provider, review, publishing, and memory hooks.

### Step 8: ADK/Agents CLI Export

Only after the Python registry exists, generate optional ADK artifacts:

- `root_agent.yaml`;
- per-agent config;
- tool adapters;
- skill package adapters;
- `GEMINI.md` or equivalent development guide;
- deployment scaffolding if using Agents CLI.

The generated ADK project should be an adapter around CMF contracts, not a second source of truth.

## 15. Acceptance Criteria

- Each agent has a department, goal, fit rationale, input contract, output contract, tool list, skill bindings, hooks, blocked actions, validation contract, and required receipts.
- Sub-agents are scoped lenses with small input/output contracts.
- Operational skills and JIT skills are separated.
- JIT skills are repositioned toward extraction, narrative induction, interview engineering, contrast, route support, and evaluation.
- Pi cannot act unless the requested agent, tool, stage, and validation contract are registered.
- All mutating actions go through Command Bus or a durable workflow that writes receipts.
- ADK/Agents CLI artifacts are generated from CMF specs, not hand-maintained as canonical runtime truth.

## 16. Open Design Repairs

1. Extend `SkillUseMode` or define aliases so `interview_engineering` and `narrative_induction` are first-class.
2. Add `AgentFactoryRegistry` contracts and migrations.
3. Decide whether stable operational skills live in `docs/agent-skills/`, `src/ccp_studio/agent_skills/`, or a database-backed registry with filesystem fixtures.
4. Define which role specs export to ADK immediately and which remain Python-only.
5. Add MCDA or CBAR eval criteria for agent-fit quality before implementation.

## 17. External References Checked

- Google ADK home: `https://adk.dev/`
- Google ADK Agent Config: `https://adk.dev/agents/config/`
- Google ADK Agent Team tutorial: `https://adk.dev/tutorials/agent-team/`
- Google ADK Custom Tools: `https://adk.dev/tools-custom/`
- Google ADK Skills: `https://adk.dev/skills/`
- Google ADK Callbacks: `https://adk.dev/callbacks/`
- Google ADK Graph Workflows: `https://adk.dev/graphs/`
- Google ADK Agent Routing: `https://adk.dev/agents/routing/`
- Google ADK Agents CLI deployment guide: `https://adk.dev/deploy/agent-runtime/agents-cli/`
