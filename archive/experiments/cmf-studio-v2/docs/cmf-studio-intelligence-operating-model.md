---
title: "CMF Studio Intelligence Operating Model"
status: "draft-canonical"
created_at: "2026-06-22"
runtime_target: "Python / Pydantic v2 / DSPy / Pi / FastAPI / durable workflows"
source_prd: "THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md"
source_architecture: "docs/architecture.md"
source_factory: "docs/cmf-studio-agent-factory-architecture.md"
source_pipeline_map: "docs/cmf-studio-pipeline-map.md"
requires_legacy_inventory: true
---

# CMF Studio Intelligence Operating Model

## 1. Purpose

CMF Studio is not just an agent team. It is a Factory of governed cognitive entities.

Each entity in the Factory needs a brain: standards, primitives, rules, tools, protocols, memory, skills, evaluations, receipts, and constitutions that govern what it can notice, infer, decide, do, remember, reject, and repair.

This document defines how CMF intelligence is used by each entity. It complements `docs/cmf-studio-agent-factory-architecture.md`, which defines the Factory departments and agent roles.

In product architecture terms, CMF uses "will" and "consciousness" as operational concepts:

- **Operational will** is an entity's goal vector constrained by constitution, role, stage, allowed actions, blocked actions, and proof obligations.
- **Operational consciousness** is an entity's bounded awareness of current stage, active object, source evidence, memory, identity state, constraints, tools, downstream consequences, and its own uncertainty.

This is not a claim of human sentience. It is a design discipline for building agents that behave like accountable cognitive workers rather than chat prompts.

## 2. Core Thesis

The intelligence layer must not be treated as prompt text attached to agents.

CMF intelligence is a governed substrate composed of:

- constitutions;
- standards;
- primitive registries;
- SDA/SFL ontology and function layers;
- CRAL/SCRE research;
- Context Premise and Audience Reality;
- Emotional DNA and Voice DNA;
- Matrix of Edging;
- narrative induction;
- interview engineering;
- archetype and asset derivative registries;
- scene intelligence;
- SVRE/Aurore visual research;
- JIT skill compilers;
- stable operational skills;
- tools;
- workflow protocols;
- memory;
- evaluations;
- receipts.

An entity may use only the intelligence it is explicitly bound to use, in the stage where that intelligence is valid, with the proof obligations that make its use observable.

## 3. Files and Doctrine Read

| Source | Intelligence Role |
|---|---|
| `docs/migration/legacy-inventory.md` | Declares the legacy repository as read-only doctrine, registry, fixture, example, and provider-code source. Identifies primitives, SDA/SFL, narrative intelligence, CMF engines, CRAL, CBAR, TTT, Voice DNA, and anti-draft modules as migration targets. |
| `reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md` | Defines primitives as stable transformation operators, split across Meaning Plane and Experience Plane, with basis, coalitions, trigger conditions, anti-patterns, and dual-source validation. |
| `lab/Harness_and_Orchestration_Architecture/ccp_biological_orchestration_model_v_1.md` | Defines the biological orchestration model: DNA -> RNA -> force -> delivery -> variation -> phenotype -> evaluation. |
| `lab/Specs_and_Architecture_Documentation/Context_Premise_Trigger_Matching_Layer.md` | Defines Context Premise, L1/L2/L3 audience intelligence, tribal language, structural matching, and activation seeds. |
| `THE CMF STUDIO/Matrix of Edging.md` | Defines edges as high-magnitude tension sites and distinguishes broad primary signal from post-trigger edge product formation. |
| `docs/architecture.md` | Defines the Python-first implementation truth, Command Bus boundary, orchestration objects, JIT compiler rule, CRAL rule, root-down expression rule, scene reproducibility rule, and Neo4j projection rule. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | Defines FR-CMF requirements and active intelligence per module. |
| `docs/cmf-studio-agent-factory-architecture.md` | Defines departments, agents, sub-agents, hooks, extensions, tools, stable operational skills, and JIT skills. |

## 4. The CMF Brain Stack

Every entity's brain is assembled from nine layers.

| Layer | Question It Answers | Examples | Enforcement |
|---|---|---|---|
| Constitution | What may this entity never violate? | Source truth, consent, no newsletters, Command Bus, Neo4j projection-only, pricing scope, no hidden prompts | `ValidationContract`, hooks, static gates, blocked actions |
| Identity | What is this entity and what is it for? | department, role, goal, fit rationale, stage ownership | `AgentRoleSpec`, `DepartmentSpec` |
| Perception | What can this entity see? | source refs, transcripts, CRAL evidence, Brand Context, memory snapshots, route receipts | `AgentHandoffPacket`, scoped queries |
| Ontology | What categories does it think with? | SDA, SFL, primitives, archetypes, scene containers, provider capabilities | registries, Pydantic contracts |
| Protocol | How does it reason or proceed? | Matrix of Edging, Context Premise, JIT saturation, CBAR, RSCS, Complete Editing Session | stable skills, DSPy programs, workflow steps |
| Tools | What can it do? | command tools, source tools, DSPy tools, provider tools, renderer tools, review tools | `ToolCapabilitySpec`, Gateway authorization |
| Memory | What can it remember or learn from? | Brand Memory, Interviewer Memory, Route Memory, failure corpus, rejected candidates | memory access policy, admission receipts |
| Evaluation | How is quality judged? | source truth, anti-draft, route fit, identity safety, composition accuracy, render integrity | eval receipts, critic agents, thresholds |
| Receipts | How does the Factory know what happened? | `SkillInvocationReceipt`, `StageExecutionReceipt`, `EvaluationReceipt`, `FailureReceipt` | mandatory receipt closure |

No entity should execute with an incomplete brain stack. If an entity lacks constitution, perception, protocol, tools, or receipt obligations, it should not be executable.

## 5. Operational Will

An entity's will is not free-form desire. It is the intersection of:

```text
role goal
+ pipeline stage
+ active object
+ allowed actions
+ available tools
+ intelligence profile
+ memory access
+ validation contract
- blocked actions
- constitutional prohibitions
- missing evidence
= operational will
```

For example, `ExpressionMomentHunter` may want to find powerful source moments, but its will is constrained:

- it can inspect source and transcript evidence;
- it can invoke extraction JIT skills;
- it can propose expression moment candidates;
- it cannot approve them;
- it cannot route them without review;
- it cannot invent unsupported quotes;
- it must write extraction receipts.

This is how the system gives agents agency without letting them become arbitrary.

## 6. Operational Consciousness

An entity's operational consciousness is its bounded runtime self-state.

It should always know:

- who it is;
- which department it belongs to;
- which pipeline stage it is operating inside;
- which active object it is touching;
- which evidence it has;
- which memory it may read;
- which standards govern this action;
- which tools it may use;
- which actions are forbidden;
- which downstream entity depends on its output;
- which receipt it must produce;
- what it is uncertain about;
- when it must request a human handoff.

This should be represented as a typed `AgentExecutionContext`, not as hidden prompt context.

## 7. Intelligence Source Types

### 7.1 Constitutional Intelligence

Constitutional intelligence governs the whole Factory.

Examples:

- Python/Pydantic/DSPy/Pi is implementation truth.
- Command Bus is the only canonical mutation path.
- Neo4j is a rebuildable projection, not production truth.
- Consent and source truth precede provider jobs, rendering, review, publishing, and memory.
- Newsletters are not valid CMF deliverables.
- Content charges are limited to `$29/week` trial Guest Asset Packs and `$99/month` Monthly Asset Engine.
- Legacy runtime code is not imported directly.
- Hidden prompt stacks are blocked.

Consumers:

- all agents;
- all hooks;
- all tools;
- all workflows;
- all skills;
- all provider adapters.

### 7.2 Identity Intelligence

Identity intelligence defines stable truth about the brand, guest, voice, emotional architecture, and expressive boundaries.

Examples:

- Brand Context;
- Emotional DNA;
- Voice DNA;
- negative space;
- 64-state acting library;
- paper-cut rig identity;
- micro-semiotic maps;
- known-person and likeness constraints.

Consumers:

- Brand Genesis agents;
- Interview Intelligence agents;
- Extraction agents;
- Scene and Composition agents;
- Evaluation and Review agents;
- Provider and rendering agents.

### 7.3 Semantic and Primitive Intelligence

Primitive intelligence is not label decoration. It is the system's perception and transformation vocabulary.

Meaning Plane answers what truth, transformation, narrative, persuasion, humor, psychology, voice, performance, or business force is present.

Experience Plane answers how the human encounter should be triggered, paced, made safe, personalized, rewarded, repeated, or shared.

SDA/SFL add deeper structure:

- SDA gives existential invariants, representation geometries, archetypal geometries, and structural grammar.
- SFL gives compression, function profiles, signal shaping, failure corpora, and surface constraints.

Consumers:

- Matrix of Edging agents;
- Context Premise agents;
- JIT skill compilers;
- Expression extraction agents;
- Routing agents;
- Scene intelligence agents;
- Evaluation agents;
- Memory agents.

### 7.4 Research and Context Intelligence

Research and context intelligence turns external reality into usable activation material.

Examples:

- CRAL/SCRE evidence;
- research fields;
- source provenance;
- audience reality;
- Context Premise;
- L1/L2/L3 audience stratification;
- tribal language;
- contradiction maps;
- claim safety;
- freshness and confidence.

Consumers:

- `CRALResearchLead`;
- `EvidenceCartographer`;
- `AudienceRealityAnalyst`;
- `ContextPremiseArchitect`;
- `ClaimSafetyCritic`;
- `InterviewerPreInductionLead`;
- `NarrativeInductionDirector`.

### 7.5 Interview and Induction Intelligence

Interview intelligence guides the human source toward better expression before editing starts.

Examples:

- Matrix of Edging;
- Narrative State Induction;
- First-Line Anchors;
- Depth Anchors;
- Interview Asset Contracts;
- TTT transition grammar;
- guest saturation profile;
- anti-centroid checks;
- recording and elicitation briefs.

Consumers:

- Interview Intelligence Department;
- live induction JIT skills;
- interview engineering skills;
- extraction agents after the session.

### 7.6 Extraction Intelligence

Extraction intelligence operates at two levels:

1. **Transcript extraction:** what was said, where, with what timestamp, quote boundary, claim, story beat, and clip potential.
2. **Guest/narrative induction extraction:** what the guest revealed through identity, emotional path, narrative state, implicit tension, hesitation, contradiction, voice mechanics, and activation.

Examples:

- JIT skill compilers;
- saturation context;
- contrastive prompt layers;
- anti-draft calibration;
- source truth critics;
- narrative induction extractors;
- expression moment candidate detection;
- boundary control.

Consumers:

- `ExpressionMomentHunter`;
- `NarrativeInductionExtractor`;
- `PrimitiveCoalitionMapper`;
- `BoundaryControlReviewer`;
- routing agents.

### 7.7 Routing and Format Intelligence

Routing intelligence decides what an expression can become.

Examples:

- Core Content Archetype registry;
- Asset Derivative registry;
- Meme Mechanism registry;
- Reaction Archetype registry;
- CMF Render Mode registry;
- valid format rules;
- unsupported format guard;
- Guest Asset Pack policy.

Consumers:

- `ArchetypeRouteCompiler`;
- `AssetDerivativeRouter`;
- `MemeReactionRouter`;
- `GuestAssetPackPlanner`;
- `UnsupportedFormatGuard`.

### 7.8 Scene and Visual Intelligence

Scene intelligence turns approved expression and route receipts into reproducible visual production.

Examples:

- Complete Editing Session;
- SceneSpec;
- CreativeState;
- scene containers;
- scene components;
- creative subsystems;
- asset roll plan;
- Ideogram 4 `CompositionJob`;
- SVRE/Aurore visual research;
- provider capability registry;
- ComfyUI worker templates.

Consumers:

- `CompleteEditingSessionProducer`;
- `SceneSpecArchitect`;
- `IdeogramCompositionDirector`;
- `SceneContainerPlanner`;
- `AssetRollChoreographer`;
- visual research and provider agents.

### 7.9 Evaluation and Review Intelligence

Evaluation intelligence gives the Factory a conscience in the operational sense: it can judge whether the output remained true to source, route, identity, and production constraints.

Examples:

- SemanticCritic;
- source truth audit;
- route fit;
- Brand Identity review;
- Voice DNA continuity;
- composition accuracy;
- render integrity;
- approval blockers;
- Telegram/PWA evidence-rich review.

Consumers:

- Evaluation and Review Department;
- all upstream departments through feedback;
- memory admission.

### 7.10 Memory and Projection Intelligence

Memory intelligence lets CMF learn without hallucinating history.

Examples:

- Brand Memory;
- Interviewer Memory;
- Route Memory;
- rejected candidate memory;
- failure corpus;
- provider performance memory;
- evaluation history;
- Neo4j relationship projection.

Rules:

- memory admission must be evidence-backed;
- memory must be reversible;
- memory must keep correction and expiry paths;
- Neo4j is projection only;
- rejected outputs are intelligence, not garbage.

Consumers:

- all agents with scoped memory access;
- memory agents;
- projection agents;
- evaluation agents;
- operations agents.

## 8. Entity Intelligence Usage

### 8.1 Factory

The Factory uses intelligence as an operating constitution.

It does not perform a stage directly. It defines:

- departments;
- stage ownership;
- allowed intelligence;
- global constitutions;
- tool families;
- memory policy;
- receipt policy;
- evaluation policy.

### 8.2 Department

A Department uses intelligence as a bounded brain domain.

For example, the Research and Context Department may use CRAL, Context Premise, Audience Reality, evidence provenance, and claim safety. It should not use provider adapter intelligence or publishing memory except as downstream context.

### 8.3 Agent

An Agent uses intelligence through an `IntelligenceProfile`.

The profile says:

- which constitutional rules are bound;
- which source docs and registries it may read;
- which primitive families it may activate;
- which memory scopes it may access;
- which stable skills it may load;
- which JIT skill modes it may invoke;
- which tools it may call;
- which sub-agents it may delegate to;
- which evaluation standards judge it.

### 8.4 Sub-Agent

A Sub-Agent uses a narrow intelligence lens.

It should not carry the whole Factory brain. It carries one precise faculty:

- critic;
- scorer;
- hunter;
- compiler;
- gatekeeper;
- adapter;
- clerk.

Example: `AntiCentroidCritic` does not need provider tools or publishing memory. It needs source evidence, primitive/edge context, anti-draft standards, and rejection criteria.

### 8.5 Hook

A Hook uses constitutional and validation intelligence.

Hooks are not creative minds. They are reflexes and boundary checks. A hook knows what must be true before or after an action, then blocks, allows, or receipts.

### 8.6 Extension

An Extension uses intelligence as a packaged capability set.

An extension may contain:

- tools;
- schemas;
- stable skills;
- fixtures;
- provider adapters;
- policies;
- evals.

It cannot grant authority by itself. Authority still comes from the Agent Gateway, stage plan, permission, and validation contract.

### 8.7 Stable Operational Skill

A Stable Operational Skill uses intelligence as a repeatable operating manual.

It should be used when an agent needs enduring know-how:

- how to audit source truth;
- how to prepare an evidence-rich review packet;
- how to recover provider jobs;
- how to evaluate scene reproducibility;
- how to inspect CRAL evidence.

### 8.8 JIT Skill Compiler

A JIT Skill Compiler uses intelligence as a run-specific synthesis engine.

It must receive saturation context and produce bounded outputs. It cannot mutate state.

Valid current use:

- live guest induction;
- interview engineering;
- narrative induction;
- transcript extraction;
- source expression contrast;
- routing support;
- evaluation support;
- Voice DNA support.

Limited downstream use:

- scene prompt support only after approved expression, route receipt, and Complete Editing Session.

### 8.9 Tool

A Tool uses intelligence only as parameters and constraints.

Tools do not reason freely. A tool executes a typed operation and returns a typed result or receipt.

### 8.10 Workflow

A Workflow uses intelligence as stage sequence, retry policy, recovery logic, and wait conditions.

It owns time, durability, and compensation. It does not replace an agent's role or a critic's judgment.

### 8.11 Memory

Memory uses intelligence as admitted evidence.

Memory is not a diary of impressions. It is a governed store of approved, rejected, corrected, expired, or quarantined learning.

## 9. Department Intelligence Matrix

| Department | Primary Intelligence | Secondary Intelligence | Forbidden Use |
|---|---|---|---|
| Command and Runtime | constitutional rules, stage plans, validation contracts, receipts | operations memory, friction receipts | creative reasoning without domain agent |
| Legacy Intelligence and Skill Governance | Legacy Inventory, migration ledger, primitives, SDA/SFL, JIT specs, fixtures, evals | CBAR, RSCS, spec protocols | importing legacy runtime directly |
| Workspace, Consent, and Commercial Governance | consent constitution, pricing constitution, tenant scope, permission rules | source/identity policy | creative or route decisions |
| Brand Genesis and Identity | Brand Context, Emotional DNA, Voice DNA, micro-semiotics, acting library, paper-cut rigs | primitive families PER, VOC, ACT, VSG, SAF | per-asset identity reinvention |
| Research and Context | CRAL/SCRE, evidence, Audience Reality, Context Premise, L3 tribal language | claim safety, contradiction maps | unsupported claims or generic persona summaries |
| Interview Intelligence | Matrix of Edging, Narrative State Induction, anchors, Interview Asset Contracts, TTT | Emotional DNA, Context Premise, primitives STR/PRS/PSY/VOC | script dictation or over-shaping guest answers |
| Expression Session and Extraction | source artifacts, transcripts, timestamps, dual-layer extraction, JIT extraction, anti-draft | primitive coalitions, interview contracts | extracting ideas without source evidence |
| Routing and Package Planning | archetype registry, asset derivative registry, valid format rules, package policy | route memory, primitive signatures | newsletters or unsupported generic formats |
| Scene and Composition | Complete Editing Session, SceneSpec, scene containers/components/subsystems, CompositionJob | Brand Context, route receipt, SVRE/Aurore | rebuilding scenes from vibe or raw prompt only |
| Visual Research and Provider Operations | SVRE/Aurore, provider capability registry, identity safety, ComfyUI templates | source evidence, scene plan, asset memory | old RunningHub assumptions or unapproved provider drift |
| Rendering and Assembly | RenderContract, layer manifest, timeline, captions, audio, SFL sound doctrine | scene reproducibility, render memory | render without reproducibility metadata |
| Evaluation and Review | SemanticCritic, source truth, route fit, Brand Identity, Voice DNA, composition accuracy | rejection memory, human review evidence | self-approval by generating agent |
| Publishing and Memory | approval, consent, PublishingIntent, memory admission, Neo4j projection | platform variant rules, route memory | publishing before human approval or making Neo4j canonical |
| Operations and Reliability | failure receipts, friction receipts, recovery policy, environment parity, dependency safety | provider performance memory, workflow history | silent recovery without receipt |

## 10. First 18 Agents: Intelligence Profiles

| Agent | Core Brain Package |
|---|---|
| `FactoryConductor` | constitution, pipeline map, stage transition rules, Gateway policy, receipt policy, recovery memory |
| `StagePlanner` | PRD stage map, architecture stage table, active object rules, entry/exit object contracts |
| `ValidationContractWriter` | FR-CMF requirements, stage proof obligations, CBAR failure scenarios, eval thresholds |
| `HandoffPacketClerk` | context scoping rules, evidence refs, upstream receipts, allowed/blocked actions |
| `ReceiptAuditor` | validation contracts, receipt schemas, status transitions, failure/friction/human handoff rules |
| `ArchiveCartographer` | Legacy Inventory, file hashes, registry families, migration target taxonomy |
| `IntentMigrationSteward` | legacy intentional orchestration, biological model, product purpose, downstream proof obligations |
| `SkillCompilerLibrarian` | stable skills, JIT compilers, DSPy program specs, fixtures, eval targets, anti-hidden-prompt gates |
| `CRALResearchLead` | CRAL/SCRE, evidence provenance, seven JIT moments, source-discipline separation |
| `ContextPremiseArchitect` | Audience Reality, L1/L2/L3 stratification, tribal language, Context Premise, trigger matching |
| `InterviewerPreInductionLead` | Context Premise, Emotional DNA, Voice DNA, Matrix of Edging, interview preparation protocol |
| `MatrixOfEdgingNavigator` | broad primary signal, edge product formation, primitive activation, anti-centroid pressure |
| `NarrativeInductionDirector` | live guest induction, narrative state, anchors, TTT, interview engineering JIT skills |
| `SourceIngestionSteward` | source artifact policy, transcript alignment, consent state, provenance, source quality |
| `ExpressionMomentHunter` | transcript extraction, source truth, Interview Asset Contracts, JIT extraction, anti-draft |
| `NarrativeInductionExtractor` | guest-level meaning, hesitation/contradiction patterns, Emotional DNA traces, narrative state |
| `ArchetypeRouteCompiler` | archetype registry, primitive coalitions, asset derivative registry, valid format constitution |
| `SemanticCritic` | source truth, route fit, meaning preservation, anti-genericity, evaluation receipts |

## 11. Intelligence Profile Contract

Every executable entity should have an `IntelligenceProfile`.

```yaml
intelligence_profile_id: "expression_moment_hunter.brain.v1"
entity_id: "expression_moment_hunter"
entity_type: "agent"
department_id: "expression_session_and_extraction"
constitution_bindings:
  - "source_truth_constitution.v1"
  - "command_bus_constitution.v1"
  - "no_hidden_prompt_constitution.v1"
  - "no_self_approval_constitution.v1"
perception_scope:
  source_refs:
    - "CompleteExpressionSession"
    - "TranscriptSegment"
    - "InterviewAssetContract"
  memory_scopes:
    - "rejected_candidate_memory.read"
    - "route_memory.read"
ontology_bindings:
  primitive_families:
    - "STR"
    - "PRS"
    - "PSY"
    - "VOC"
    - "CON"
  sda:
    - "representation_geometries"
    - "existential_invariants"
  sfl:
    - "failure_corpus"
    - "function_profiles"
protocol_bindings:
  - "source_truth_audit.skill"
  - "anti_centroid_check.protocol"
  - "jit_saturation_context.protocol"
stable_skills:
  - "source_truth_audit.skill"
jit_skill_modes:
  - "transcript_extraction"
  - "narrative_induction"
tools:
  - "query_transcript_segments"
  - "invoke_jit_skill_compiler"
  - "record_expression_moment_candidate"
forbidden_tools:
  - "approve_expression_moment"
  - "create_publishing_intent"
evaluation_profile:
  required_evals:
    - "source_truth_eval"
    - "anti_draft_eval"
    - "route_readiness_eval"
receipt_profile:
  required_receipts:
    - "SkillInvocationReceipt"
    - "ExtractionReceipt"
uncertainty_policy:
  request_human_handoff_when:
    - "source evidence is contradictory"
    - "candidate boundary is unclear"
    - "guest identity claim is unsupported"
```

## 12. Intelligence Selection Flow

Each agent should select intelligence in this order:

1. Load constitutional bindings.
2. Load active stage and validation contract.
3. Load active object and source evidence.
4. Load department intelligence profile.
5. Load agent intelligence profile.
6. Load relevant stable operational skills.
7. Query registries and memory within scope.
8. If needed, assemble saturation context.
9. Invoke JIT skill compiler or DSPy program.
10. Run critic/eval.
11. Write receipt.
12. Return output or human handoff request.

No agent should begin from an open-ended model call.

## 13. Intelligence Conflict Resolution

Conflicts should be resolved by authority order:

1. Consent, privacy, source, identity, safety, and legal constraints.
2. PRD/architecture constitutions.
3. Active `ValidationContract`.
4. Source evidence.
5. Locked Brand Context and identity records.
6. Interview Asset Contracts and route receipts.
7. Primitive/SDA/SFL interpretation.
8. Stable operational skill.
9. JIT skill compiler output.
10. Memory suggestion.
11. Model preference or style suggestion.

If a lower layer contradicts a higher layer, the lower layer is rejected or quarantined.

## 14. Agent Fit Evaluation

An agent is fit for a task only if:

- it owns or is allowed on the pipeline stage;
- its department owns the object type;
- it has the needed ontology and protocols;
- it has exactly enough memory, not broad memory access;
- it has tool bindings for required actions;
- it has blocked actions for dangerous shortcuts;
- it has evals matching its failure modes;
- its output has a downstream consumer;
- its work can be receipted.

An agent is not fit if:

- it needs hidden context to succeed;
- it uses generic model judgment where a registry exists;
- it has authority to approve its own output;
- it uses memory without evidence;
- it can mutate canonical state directly;
- it cannot explain which intelligence layer shaped its output.

## 15. Conscious Factory Design Rules

1. Every entity must have a brain stack before execution.
2. Intelligence is not prompt text. It is typed, versioned, scoped, evaluated, and receipted.
3. Primitives are faculties, not labels.
4. JIT skills are runtime compilers, not generic prompt templates.
5. Stable operational skills are allowed and necessary.
6. Memory is admitted evidence, not accumulated vibes.
7. Constitutions govern agent will.
8. Execution context governs agent consciousness.
9. Tools are capabilities, not permissions.
10. Hooks enforce reflexes and boundaries.
11. DSPy reasons; Pydantic validates; Pi orchestrates; workflows endure; the Command Bus mutates.
12. The Operator remains final arbiter for truth-sensitive, taste-sensitive, identity-sensitive, and publishing-sensitive decisions.

## 16. Required Build Additions

Add these contracts:

- `IntelligenceProfile`;
- `ConstitutionBinding`;
- `OntologyBinding`;
- `PrimitiveActivationPolicy`;
- `MemoryAccessPolicy`;
- `StableSkillBinding`;
- `JITSkillModeBinding`;
- `ToolCapabilityBinding`;
- `EvaluationProfile`;
- `ReceiptProfile`;
- `UncertaintyPolicy`.

Add these registries:

- `AgentIntelligenceRegistry`;
- `ConstitutionRegistry`;
- `StableSkillRegistry`;
- `JITSkillRegistry`;
- `PrimitiveRegistryAdapter`;
- `MemoryScopeRegistry`;
- `ToolCapabilityRegistry`.

Add these gates:

- `IntelligenceProfileCompletenessGate`;
- `ConstitutionConflictGate`;
- `SourceEvidencePresenceGate`;
- `MemoryScopeGate`;
- `JITModeAuthorizationGate`;
- `PrimitiveActivationJustificationGate`;
- `SelfApprovalBlockGate`.

## 17. Next Implementation Sequence

1. Extend Agent Factory contracts with `IntelligenceProfile`.
2. Seed constitutions for Command Bus, source truth, consent, no hidden prompts, no self-approval, no newsletters, pricing scope, and Neo4j projection-only.
3. Seed department-level intelligence profiles.
4. Seed the first 18 agent intelligence profiles.
5. Add stable operational skill registry.
6. Add explicit JIT modes for `interview_engineering`, `narrative_induction`, and `source_expression_contrast`.
7. Update Agent Gateway to refuse handoff if the agent lacks an intelligence profile.
8. Add tests proving agents cannot act with missing constitution, missing evidence, unauthorized memory, unauthorized JIT mode, or self-approval.


