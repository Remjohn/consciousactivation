---
stepsCompleted:
  - 0
  - 1
  - 2
  - 3
workflowType: 'create-epics-and-stories'
status: 'complete'
project_name: 'CMF STUDIO'
user_name: 'Emilio'
date: '2026-06-21'
inputDocuments:
  - 'THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md'
  - 'docs/prd/modules/PRD_INDEX.md'
  - 'docs/prd/modules/PRD_CMF_01_Strategy_Scope_Release_Gates.md'
  - 'docs/prd/modules/PRD_CMF_02_Pipeline_Agent_Orchestration.md'
  - 'docs/prd/modules/PRD_CMF_03_Workspace_Commercial_Consent_Source.md'
  - 'docs/prd/modules/PRD_CMF_04_Legacy_Primitives_JIT_Spec_Governance.md'
  - 'docs/prd/modules/PRD_CMF_05_Brand_Genesis_Context.md'
  - 'docs/prd/modules/PRD_CMF_06_Interview_Expression_Routing.md'
  - 'docs/prd/modules/PRD_CMF_07_Editing_Composition_Rendering.md'
  - 'docs/prd/modules/PRD_CMF_08_Evaluation_Review_Publishing_Memory.md'
  - 'docs/prd/modules/PRD_CMF_09_Non_Functional_Requirements.md'
  - 'docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md'
  - 'docs/cmf-studio-agent-factory-registry.md'
  - 'docs/cmf-studio-agent-intelligence-contract.md'
  - 'docs/architecture.md'
  - 'docs/cmf-studio-pipeline-map.md'
  - 'docs/evals/02-prd-mcda-eval.md'
  - 'docs/evals/03-architecture-mcda-eval.md'
  - 'docs/migration/legacy-inventory.md'
  - 'THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md'
  - 'THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md'
  - 'THE CMF STUDIO/CCP V9 -- Interview-First Expression Engine.md'
  - 'THE CMF STUDIO/CCP V9.1 -- Expression Capture & Archetype Routing Update.md'
  - 'THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md'
  - 'THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md'
  - 'THE CMF STUDIO/CCP Archetype System Migration Proposition.docx.md'
  - 'THE CMF STUDIO/Matrix of Edging.md'
  - 'reference/conscious-rivers/docs/prd/modules/PRD_02_CCF_Content_Factory.md'
  - 'reference/conscious-rivers/docs/prd/modules/PRD_03_CMF_Media_Factory.md'
  - 'reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md'
  - 'lab/Harness_and_Orchestration_Architecture/ccp_biological_orchestration_model_v_1.md'
  - 'lab/Voice_Doctrines_and_First_Principles/CSIP_v3_Voice_DNA.md'
  - 'docs/architecture/Sovereign_CRAL_Research_Engine_Architecture_Brief.md'
  - 'docs/architecture/Sovereign_Visual_Research_Engine_TechSpec_V1.md'
  - 'src/ccp/harness/intelligence/CMF_Master_Scene_Intelligence.md'
  - 'src/ccp/harness/intelligence/CMF_Creative_Subsystems_Definitions.md'
  - 'src/ccp/harness/intelligence/CMF_Scene_Containers_Definitions.md'
  - 'src/ccp/harness/intelligence/CMF_Scene_Components_Definitions.md'
  - 'src/ccp/harness/intelligence/guides/ðŸ§   The Conscious Asset Strategy Guide.md'
  - 'docs/architecture/april_updates/ERA3_Epic_and_Story_Writing_Protocol.md'
  - 'docs/architecture/spec updates/CBAR_Constraint_Based_Adversarial_Reasoning_Epics_Stories.md'
  - 'docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md'
---

# CMF STUDIO - Epics and Stories

**Author:** John, BMad Product Manager  
**Project:** CMF STUDIO  
**Status:** Ready for Story Files and Tech Specs  
**Date:** 2026-06-21  
**Project Level:** SaaS B2B, AI media production, agentic creative operations  
**Target Scale:** Multi-brand production control tower with governed interview, rendering, approval, publishing, memory, and operations workflows  

---

## 1. Context Validation

### 1.1 Loaded Inputs

This epic and story breakdown is grounded in the completed CMF STUDIO PRD, the completed architecture document, and the Legacy Inventory. It also carries forward the ERA3 epic/story writing protocol, CBAR story-drift prevention, and RSCS signal-density quality filter.

| Input | Status | Use in This Artifact |
|---|---:|---|
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | Loaded | Functional requirements, journeys, commercial scope, user roles, NFRs |
| `docs/prd/modules/PRD_INDEX.md` and `docs/prd/modules/PRD_CMF_*` | Loaded | Canonical CMF-native product modules transformed from the current PRD |
| `docs/architecture.md` | Loaded | Command Bus, Pydantic contracts, API groups, data families, workflows, provider and projection rules |
| `docs/cmf-studio-pipeline-map.md` | Loaded | Canonical stage map, sub-workflows, agent/sub-agent map, Pi orchestration model, object spine |
| `docs/evals/02-prd-mcda-eval.md` and `docs/evals/03-architecture-mcda-eval.md` | Loaded | Repair findings requiring pipeline authority, orchestration objects, validation contracts, receipts, and spec compiler workflow |
| `docs/migration/legacy-inventory.md` | Loaded | Legacy asset migration, JIT Skill compiler doctrine, ComfyUI templates, Voice DNA, CBAR, TTT, primitives |
| CMF source documents | Referenced through PRD and architecture | V9/V9.1 expression engine, Brand Genesis, Creative Pipeline, archetype routing, Matrix of Edging |
| Old CCP/CMF PRD modules and harness intelligence | Loaded | Intentional orchestration, CCF trigger-first compiler, CMF scene/media engines, Emotional DNA, CRAL, SVRE/Aurore, scene containers/components/subsystems, asset roll logic |
| UX design document | Not present | Stories include PWA, Telegram Bot, and Telegram Mini App surface requirements from architecture instead |

### 1.2 Workflow Interpretation

The BMad workflow requires epics to deliver user value rather than technical layers. CMF STUDIO still requires an initial foundation epic because the product cannot safely run consent, rendering, review, publishing, or memory without tenant-scoped commands, contracts, receipts, and canonical state. After that first epic, each epic is organized around a meaningful operator, reviewer, migration steward, production steward, guest/client, or operations outcome.

### 1.3 Non-Negotiable Story Constraints

- Every state-changing behavior flows through a Pydantic command envelope and the Command Bus.
- PostgreSQL is canonical; Neo4j is a rebuildable relationship projection.
- TypeScript is limited to PWA, Telegram Mini App, Remotion/Motion Canvas, and generated contract consumers.
- Legacy assets are read-only intelligence until migrated into typed registries, fixtures, evals, worker assets, or DSPy programs.
- JIT Skill compilers use saturation context, drafting, contrast, calibration, and evaluation. They are not generic few-shot prompt snippets.
- Valid content formats come from Core Content Archetype, Asset Derivative, Meme Mechanism, Reaction Archetype, and CMF Render Mode registries.
- Commercial customer-facing content charges are only `$29/week` trial Guest Asset Packs and `$99/month` Monthly Asset Engine.
- Ideogram 4 `CompositionJob` JSON is first-class scene lineage.
- The self-hosted ComfyUI route is a Docker GPU worker on AWS or Google Cloud with 24GB or 32GB VRAM.
- Legacy CCF/CMF modules preserve intentional orchestration, not only feature names. Stories must capture why a module exists, which organism layer it belongs to, what it receives, what it emits, what gates it runs, and what downstream proof it authorizes.
- CRAL/SCRE, Context Premise, Emotional DNA, Voice DNA, SVRE/Aurore, CMF scene intelligence, and legacy asset engines are first-class source frameworks.
- Every epic and story must map to a canonical PRD pipeline stage, entry object, exit object, allowed actor or service, validation contract, and receipt.
- Pi orchestration must use `OrchestrationRun`, `StageExecutionPlan`, `ValidationContract`, `AgentHandoffPacket`, `SkillInvocationRecord`, `FailureReceipt`, `FrictionReceipt`, and `HumanHandoffRequest` where autonomous coordination is involved.
- Story files and tech specs must inherit `PipelineStageTrace`, `RequirementTrace`, files-read evidence, CBAR pressure, and a receipt obligation.
- No story may require direct legacy runtime imports, manual database edits, hidden provider tinkering, or approval bypass.

---

## 2. Functional Requirements Inventory

### 2.1 Module Inventory

| Module | Product Outcome | Primary Story Ownership |
|---|---|---|
| FR-CMF-01 Workspace, Tenant, Role, and Commercial Governance | Govern multi-brand production without leakage or pricing drift | Epic 1 |
| FR-CMF-02 Consent, Source, Likeness, and Voice Governance | Make permission and source truth block unsafe work | Epic 2 |
| FR-CMF-03 Legacy Migration, JIT Skill Intelligence, and Spec Governance | Preserve legacy intelligence and orchestration intent as typed assets, evals, and compilers | Epic 3 |
| FR-CMF-04 Brand Genesis and Brand Context Versioning | Manufacture and lock a reusable creative universe | Epic 4 |
| FR-CMF-05 Research, Interview Intelligence, and Narrative State Induction | Improve source expression before capture through CRAL, Context Premise, Emotional DNA, and induction contracts | Epic 5 |
| FR-CMF-06 Complete Expression Sessions, Extraction, Routing, and Guest Asset Packs | Convert guided expression into routable asset packages | Epic 6 |
| FR-CMF-07 Complete Editing Sessions, Scene Reproducibility, and Composition Control | Preserve full scene lineage, composition intent, and CMF scene orchestration | Epic 7 |
| FR-CMF-08 Provider, Renderer, GPU Worker, and Asset Assembly Operations | Execute governed deterministic/generative rendering, SVRE/Aurore research, and asset assembly | Epic 8 |
| FR-CMF-09 Evaluation, Review, Approval, and Publishing Intent | Release only evidenced, approved, platform-valid assets | Epic 9 |
| FR-CMF-10 Memory, Neo4j Projection, Operations, and Recovery | Learn from evidence while keeping operations reversible | Epic 10 |

### 2.2 Sub-Requirement Inventory

| Requirement | Description |
|---|---|
| FR-CMF-01.01 | Owners/Admins manage organization and brand workspace lifecycle. |
| FR-CMF-01.02 | Owners/Admins assign role-based permissions. |
| FR-CMF-01.03 | Operators switch active brand context and bind every object/action to it. |
| FR-CMF-01.04 | System enforces `$29/week` trial Guest Asset Packs and `$99/month` Monthly Asset Engine. |
| FR-CMF-01.05 | System applies internal entitlement, quota, cost, retention, trial, and usage policy without public tier drift. |
| FR-CMF-01.06 | Every mutating command is idempotent, permission-checked, tenant-scoped, and receipt-writing. |
| FR-CMF-01.07 | PWA Control Tower and Telegram Operator Cockpit expose the same governed state. |
| FR-CMF-02.01 | Guests/clients can provide, version, narrow, expire, and revoke consent. |
| FR-CMF-02.02 | Operators configure and confirm recording setup, source, upload, safety, and quality before session start. |
| FR-CMF-02.03 | System blocks processing, provider jobs, renders, memory, review, and publishing when consent is incompatible. |
| FR-CMF-02.04 | System preserves source artifacts, transcript revisions, timestamps, claim references, and file provenance. |
| FR-CMF-02.05 | System evaluates Voice-DNA Boost eligibility against consent, evidence, hierarchy, and restrictions. |
| FR-CMF-02.06 | System distinguishes source, repaired source, synthetic bridge, interviewer, and generated audio. |
| FR-CMF-02.07 | Reviewers inspect consent lineage and source truth before approval, publishing, memory, or voice repair. |
| FR-CMF-03.01 | Migration Stewards inventory, classify, hash, map, convert, validate, approve, deprecate, or block legacy assets. |
| FR-CMF-03.02 | System migrates archetypes, primitives, SDA/SFL, Voice DNA, CBAR, TTT, subsystems, and CMF references. |
| FR-CMF-03.03 | System preserves golden examples and failure corpora as fixtures. |
| FR-CMF-03.04 | Operators and agents use migrated JIT skill compilers for extraction, drafting, contrast, anti-draft, Voice DNA, induction, routing, and evaluation. |
| FR-CMF-03.05 | JIT compilers operate on grounded saturation context. |
| FR-CMF-03.06 | System rejects direct legacy imports, stale TypeScript-first assumptions, hidden prompts, duplicate registries, and unapproved templates. |
| FR-CMF-03.07 | System runs PRD, epic/story, architecture, and tech-spec workflows using Python/DSPy/Pi-updated ERA3/BMad discipline. |
| FR-CMF-03.08 | Every migrated registry/compiler has Pydantic target, DSPy target when applicable, fixture, eval, reviewer, defects, and status. |
| FR-CMF-03.09 | System preserves intentional orchestration rationale for migrated CCF/CMF modules: purpose, organism layer, inputs, emitted packets, gates, downstream consumers, failures, and proof. |
| FR-CMF-04.01 | Operators run Brand Genesis from intake, consent, sources, brand notes, audience, offer, and negative-space inputs. |
| FR-CMF-04.02 | Operators generate, evaluate, repair, reject, approve, and lock a 64-state acting library. |
| FR-CMF-04.03 | Operators generate, evaluate, repair, approve, and lock a paper-cut avatar rig. |
| FR-CMF-04.04 | Operators govern props, micro-semiotic anchors, motion recipes, SFX, composition, platform, and publishing profiles. |
| FR-CMF-04.05 | System scores references for likeness, gesture clarity, hands, paper texture, style, negative space, and usability. |
| FR-CMF-04.06 | System forks Brand Context Versions for approved changes while preserving historical outputs. |
| FR-CMF-04.07 | System blocks production jobs using unapproved, unlocked, stale, or cross-brand identity assets. |
| FR-CMF-05.01 | Operators create Research Fields with evidence, citations, claims, confidence, temporal sensitivity, provenance, and gaps. |
| FR-CMF-05.02 | System compiles Guest Dossiers, Audience Reality Briefs, Context Premises, and Interviewer Resonance Contexts. |
| FR-CMF-05.03 | System compiles Matrix of Edging briefs. |
| FR-CMF-05.04 | Operators run interviewer pre-induction. |
| FR-CMF-05.05 | System compiles Interview Asset Contracts. |
| FR-CMF-05.06 | System distinguishes expression states from archetypes. |
| FR-CMF-05.07 | System evaluates interview plans for saturation, collision, anti-centroid risk, specificity, and routeability. |
| FR-CMF-05.08 | System uses CRAL/SCRE, Context Premise, Audience Deep Trigger Map, Emotional DNA, Voice DNA, and root-down induction logic to explain interview moves. |
| FR-CMF-06.01 | Operators manage Complete Expression Sessions. |
| FR-CMF-06.02 | System ingests, preserves, aligns, and versions recordings, audio tracks, transcripts, timestamps, and upload provenance. |
| FR-CMF-06.03 | System detects anchor hits, emotional shifts, segments, timestamps, cues, and candidate Expression Moments. |
| FR-CMF-06.04 | Reviewers approve, reject, fix, split, merge, annotate, or hold Expression Moments. |
| FR-CMF-06.05 | System routes approved Expression Moments through valid registries. |
| FR-CMF-06.06 | System generates trial Guest Asset Pack specs. |
| FR-CMF-06.07 | System rejects unsupported formats. |
| FR-CMF-06.08 | System preserves failed candidates, rejected routes, and coalition-fatality evidence. |
| FR-CMF-07.01 | Operators/workflows create Complete Editing Sessions from approved moments, routes, package items, and locked brand contexts. |
| FR-CMF-07.02 | System compiles SceneSpecs, Creative State, Render Contracts, routes, variants, and policies. |
| FR-CMF-07.03 | System preserves Ideogram 4 `CompositionJob` JSON and full composition lineage. |
| FR-CMF-07.04 | System treats Ideogram 4 as Composition Director, not final identity renderer or final text authority. |
| FR-CMF-07.05 | System selects approved acting references, identity assets, props, anchors, motion, SFX, captions, and constraints. |
| FR-CMF-07.06 | System creates and evaluates layer manifests, animation plans, renderer routes, EDLs, timeline/caption/sonic manifests, and outputs. |
| FR-CMF-07.07 | Operators request revisions without losing lineage, receipts, version history, or approvals. |
| FR-CMF-07.08 | System reconstructs why a scene looks the way it does. |
| FR-CMF-07.09 | System preserves scene-container, scene-component, creative-subsystem, and asset-roll decisions inside SceneSpec and Complete Editing Session lineage. |
| FR-CMF-08.01 | System creates provider jobs and receipts for approved providers and renderers. |
| FR-CMF-08.02 | System routes deterministic assets through Remotion or Motion Canvas. |
| FR-CMF-08.03 | System routes generative assets through provider adapters with prompt hashes, metadata, inputs, outputs, costs, retries, and evaluation. |
| FR-CMF-08.04 | System runs batch-first self-hosted ComfyUI Docker GPU workers. |
| FR-CMF-08.05 | System migrates approved ComfyUI JSON templates into worker assets. |
| FR-CMF-08.06 | System separates source, interviewer, restored, synthetic bridge, SFX, music, captions, and final mix timeline components. |
| FR-CMF-08.07 | System pauses, retries, resumes, cancels, or compensates provider jobs idempotently. |
| FR-CMF-08.08 | System adapts SVRE/Aurore and legacy asset-research logic into governed visual research, asset manifest, scoring, licensing, and candidate-selection contracts. |
| FR-CMF-09.01 | System generates evaluation receipts for truth, fit, depth, identity, likeness, composition, platform, and publishing readiness. |
| FR-CMF-09.02 | Operators review source quote, transcript, route, brand context, assets, output, evaluation, revisions, and consent. |
| FR-CMF-09.03 | Reviewers approve, reject, request revisions, escalate, or request eligible Voice-DNA Boost. |
| FR-CMF-09.04 | System blocks approval when lineage, consent, truth, identity, evaluation, platform, or format requirements fail. |
| FR-CMF-09.05 | Operators create and confirm Publishing Intent only after approval, consent, lineage, variants, captions, and scheduling metadata are valid. |
| FR-CMF-09.06 | System submits Publishing Intents to Publer and tracks outcome without making Publer canonical. |
| FR-CMF-09.07 | Telegram quick approvals show enough evidence and deep-link to PWA for complex review. |
| FR-CMF-10.01 | System admits evidence-backed brand, interviewer, route, anchor, rejected-pattern, and publishing-performance memory. |
| FR-CMF-10.02 | Operators inspect, correct, reverse, expire, or quarantine memory admissions. |
| FR-CMF-10.03 | System maintains canonical state while exposing Neo4j as rebuildable relationship projection. |
| FR-CMF-10.04 | Neo4j projection can be rebuilt and never becomes the only source of truth. |
| FR-CMF-10.05 | Operators inspect queues, workers, providers, failures, costs, blockers, checkpoints, and readiness. |
| FR-CMF-10.06 | System retries, resumes, cancels, compensates, or quarantines workflows idempotently. |
| FR-CMF-10.07 | System runs operational readiness checks for restore, outage, worker shutdown, memory rebuild, Neo4j rebuild, and a full brand cycle. |

---

## 3. Epic Structure Plan

| Epic | User Value Statement | FR Coverage | Primary Architecture Context | Dependencies |
|---|---|---|---|---|
| 1. Governed Workspace and Production Spine | Owners and Operators can run brand-scoped production without leakage, pricing drift, command bypass, or pipeline-stage drift. | FR-CMF-01 plus orchestration support for FR-CMF-03.07 | Pydantic contracts, Command Bus, OrchestrationRunWorkflow, StageExecutionPlan, ValidationContract, auth/RBAC, command_log, domain_events, audit_receipts, generated TS contracts | None |
| 2. Consent, Source, Likeness, and Voice Safety | Guests, Operators, and Reviewers can trust that source truth and permission boundaries block unsafe work. | FR-CMF-02 | Consent state machine, source storage, voice eligibility, review gates, receipt pattern | Epic 1 |
| 3. Legacy Intelligence and JIT Skill Governance | Migration Stewards and agents can recover legacy intelligence and orchestration intent without inheriting legacy runtime fragility. | FR-CMF-03 | MigrationWorkflow, orchestration intent records, registries, DSPy compilers, fixtures, evals, legacy import gates | Epic 1 |
| 4. Brand Genesis and Locked Creative Universe | Operators can create a reusable brand world that production can safely depend on. | FR-CMF-04 | BrandGenesisWorkflow, BrandContextVersion, acting library, rig manifests, creative libraries | Epics 1-3 |
| 5. Interview Intelligence and Narrative State Induction | Operators can prepare interviews that generate real expression before editing begins. | FR-CMF-05 | InterviewPreparationWorkflow, CRAL/SCRE, Context Premise, Emotional DNA, Voice DNA, research tables, DSPy compilers, RSCS and Matrix of Edging | Epics 1-4 |
| 6. Complete Expression Sessions and Guest Asset Packs | Operators and Reviewers can transform guided interviews into source-backed routable packages. | FR-CMF-06 | CompleteExpressionSessionWorkflow, transcript alignment, ExpressionMoment, registry routing | Epics 1-5 |
| 7. Complete Editing Sessions and Reproducible Scenes | Production Stewards can create scenes whose lineage, composition intent, and revisions remain reconstructable. | FR-CMF-07 | CompleteEditingSessionWorkflow, SceneSpec, scene containers/components/subsystems, CompositionJob, RenderContract, evaluation receipts | Epics 1-6 |
| 8. Governed Rendering and Provider Operations | Production Stewards can execute deterministic/generative rendering and asset research with receipts, costs, retries, and worker control. | FR-CMF-08 | ProviderCapabilityRecord, SVRE/Aurore contracts, provider adapters, Remotion/Motion Canvas, ComfyUI Docker worker | Epics 1-7 |
| 9. Review, Approval, and Publishing Intent | Reviewers can approve, reject, revise, and publish only when evidence proves readiness. | FR-CMF-09 | EvaluationReceipt, review commands, approval events, PublishingIntent, Publer adapter | Epics 1-8 |
| 10. Evidence Memory, Neo4j Projection, and Recovery | Operators can learn from approved evidence, inspect relationships, and recover work without hidden scripts. | FR-CMF-10 | Memory admissions, Neo4j projection, operations board, recovery actions, readiness checks | Epics 1-9 |
| 11. Agent Factory Persona Runtime | Operators, builders, and agents can trace every agent, sub-agent, hook, extension, skill, registry, and eval by a compact persona code, responsibility contract, and runtime proof obligation. | PRD-CMF-10 plus PRD-CMF-02.03 through PRD-CMF-02.05 | AgentFactorySpec, DepartmentSpec, AgentRoleSpec, SubAgentRoleSpec, HookSpec, ExtensionSpec, SkillBinding, ToolCapabilitySpec, AgentReadinessEval, ADK adapter export | Epics 1-10 |

### 3.1 Epic-to-Pipeline Trace

| Epic | Canonical Pipeline Stage(s) | Entry Object(s) | Exit Object(s) | Required Proof |
|---|---|---|---|---|
| 1 | Stage 1 plus cross-cutting orchestration | organization, brand, actor, command request | `BrandWorkspace`, `CommercialPolicy`, `OrchestrationRun`, `StageExecutionPlan` | brand scope, role policy, command receipt, validation contract |
| 2 | Stages 1, 5, 13, 14 consent gates | guest/client, source files, consent request, voice repair request | `ConsentRecordVersion`, `SourceArtifactManifest`, `VoiceBoostEligibilityReport` | consent receipt, source provenance, voice eligibility receipt |
| 3 | Stage 0 plus spec-governance overlay | legacy source path, source docs, story/spec request | `MigrationLedgerEntry`, `LegacyOrchestrationIntentRecord`, `SpecAuditReceipt` | file hash, migration target, files-read receipt, CBAR proof |
| 4 | Stage 2 | intake, consent, brand/source assets | `BrandContextVersion`, acting library, rig manifest, creative libraries | genesis clearance, identity/likeness receipts, lock receipt |
| 5 | Stages 3-4 | research evidence, guest/audience sources, brand context | `ResearchSnapshot`, `ContextPremise`, `NarrativeStateMap`, `InterviewAssetContract` | evidence provenance, saturation/collision gate, induction receipt |
| 6 | Stages 5-8 | approved contracts, recording artifacts, transcript, approved moments | `CompleteExpressionSession`, `ExpressionMoment`, `AssetRouteReceipt`, `AssetPackageSpec` | source alignment, extraction receipt, route receipt, unsupported-format gate |
| 7 | Stages 9-10 and 12 | approved route, package item, locked brand context | `CompleteEditingSession`, `SceneSpec`, `CompositionJob`, `RenderContract` | source lineage, brand lock, composition lineage, scene reproducibility receipt |
| 8 | Stages 11-12 | render contract, provider policy, visual research query | `ProviderReceipt`, `AssetResearchManifest`, `RenderOutput` | provider receipt, license/provenance, cost/retry receipt, worker checkpoint |
| 9 | Stages 13-14 | render output, source lineage, consent, platform variant | `EvaluationReceipt`, `ApprovalEvent`, `PublishingIntent`, Publer outcome | evaluation receipt, human approval, publishing intent receipt |
| 10 | Stage 14 plus operations/recovery overlay | approved outputs, events, incidents, projection checkpoint | `MemoryAdmission`, `Neo4jProjectionEvent`, `RecoveryAction` | evidence-backed memory, projection rebuild proof, recovery receipt |
| 11 | all stages plus agent-factory overlay | department, role, active object, tool, skill, hook, extension, eval requirement | `AgentFactorySpec`, `AgentRoleSpec`, `SubAgentRoleSpec`, `HookSpec`, `ExtensionSpec`, `SkillBinding`, adapter export | persona-code validation, bounded authority proof, readiness eval, adapter drift gate |

### 3.2 Story-to-Pipeline Trace Matrix

| Story | Stage(s) | Entry Object | Exit Object | Validation Contract | Required Receipt |
|---|---|---|---|---|---|
| 1.1 | 1 / cross-cutting | command request | command log, event, audit receipt | command envelope and brand scope | audit receipt |
| 1.2 | 1 | organization / brand request | `BrandWorkspace` lifecycle event | owner/admin role and brand scope | workspace receipt |
| 1.3 | 1 | user and role request | `RoleAssignment` | permission policy | role assignment receipt |
| 1.4 | 1 / 8 | entitlement request | `CommercialPolicy`, cost receipt | `$29/week` or `$99/month` guardrail | commercial receipt |
| 1.5 | 1 / 13 | PWA or Telegram action | canonical command result | same state and role validation | command receipt |
| 1.6 | all stages | active object and requested action | `OrchestrationRun`, `StageExecutionPlan`, receipt | stage/object/actor validation | stage execution receipt |
| 2.1 | 1 / 13 / 14 | consent request | `ConsentRecordVersion` | consent scope model | consent receipt |
| 2.2 | 1 / 5 | recording setup | `SourceArtifactManifest` | source quality and provenance | source intake receipt |
| 2.3 | all gated stages | consent-sensitive command | blocked or allowed state | current consent compatibility | consent blocker receipt |
| 2.4 | 12 / 13 | voice repair request | `VoiceBoostEligibilityReport`, audio manifest | repair hierarchy and claim restrictions | voice eligibility receipt |
| 2.5 | 13 | asset under review | approval-ready evidence view | source and consent completeness | review evidence receipt |
| 3.1 | 0 | legacy source path | `MigrationLedgerEntry` | hash and migration target | migration receipt |
| 3.2 | 0 | approved legacy asset | registry, fixture, eval target | schema/eval activation gate | registry activation receipt |
| 3.3 | 3 / 4 / 6 / 7 | saturation context | `SkillInvocationRecord` and proposals | grounded context and anti-draft gate | skill invocation receipt |
| 3.4 | 0 / all stages | import/template/spec reference | blocked or approved reference | greenfield rule and template hash | gate failure or approval receipt |
| 3.5 | spec-governance overlay | epic/story/spec request | `SpecAuditReceipt` | files-read, FR trace, pipeline trace, CBAR | spec audit receipt |
| 3.6 | 0 | orchestration-bearing module | `LegacyOrchestrationIntentRecord` | organism layer and proof obligations | orchestration intent receipt |
| 4.1 | 2 | brand intake and consent | `BrandGenesisSession` | source/consent completeness | genesis start receipt |
| 4.2 | 2 | brand source and generation request | acting library version | likeness/gesture/style gate | acting library receipt |
| 4.3 | 2 | creative generation request | rig and creative libraries | layer/anchor/preview validation | creative library receipt |
| 4.4 | 2 | approved genesis assets | locked/forked `BrandContextVersion` | review and version immutability | genesis clearance receipt |
| 4.5 | 9 / 10 | production job request | allowed or blocked SceneSpec compile | locked brand context | brand context gate receipt |
| 5.1 | 3 | research evidence | `ResearchField`, `ResearchEvidence` | provenance/freshness gate | research evidence receipt |
| 5.2 | 3 | approved research | dossier, audience brief, Context Premise | evidence and inference validation | context compilation receipt |
| 5.3 | 3 / 4 | dossier and audience reality | `MatrixOfEdgingBrief` | collision and specificity gate | Matrix receipt |
| 5.4 | 4 | session plan | `PreInductionPlan` | anti-centroid and manipulation gate | pre-induction receipt |
| 5.5 | 4 | preparation artifacts | `InterviewAssetContract`, deck | routeability and expression/archetype separation | contract compilation receipt |
| 5.6 | 3 / 4 | CRAL/context/DNA evidence | `InductionRationale` | supported psychology and root-down evidence | induction rationale receipt |
| 6.1 | 5 | approved contracts and setup | `CompleteExpressionSession` | consent and recording readiness | session start receipt |
| 6.2 | 5 | recordings/transcripts | aligned source/transcript artifacts | source integrity and transcript alignment | ingestion receipt |
| 6.3 | 6 | aligned transcript/source | candidate Expression Moments | source truth and JIT skill validation | extraction receipt |
| 6.4 | 6 | moment candidates | approved/superseded Expression Moments | reviewer boundary gate | expression review receipt |
| 6.5 | 7 | approved Expression Moment | `AssetRouteReceipt` | registry route and source support | routing receipt |
| 6.6 | 8 | route receipts and offer | `AssetPackageSpec` | source sufficiency and commercial guardrail | package spec receipt |
| 6.7 | 6 / 7 / 14 | rejected candidate/route | failure corpus or memory candidate | consent and non-truth admission gate | rejection receipt |
| 7.1 | 9 | approved moment, route, brand context | `CompleteEditingSession` | source approval and brand lock | editing session receipt |
| 7.2 | 9 | editing session | `SceneSpec`, `CreativeState`, `RenderContract` | asset/variant/revision validation | SceneSpec receipt |
| 7.3 | 10 | SceneSpec and Ideogram route | `CompositionJob`, plate, analysis | text-space and identity boundary | composition receipt |
| 7.4 | 12 | approved SceneSpec | layer, animation, timeline, caption, sonic manifests | brand layer and timing validation | assembly-plan receipt |
| 7.5 | 9 / 12 / 13 | revision request | revision chain and audit view | lineage preservation | revision receipt |
| 7.6 | 9 / 10 | scene intent | scene container/component/subsystem/asset-roll plan | CMF scene orchestration gate | scene intelligence receipt |
| 8.1 | 11 | provider request | provider job and receipt | capability and cost policy | provider receipt |
| 8.2 | 12 | RenderContract | deterministic render output | renderer props and brand layer validation | render receipt |
| 8.3 | 11 | generative provider request | generated/edited asset | provider metadata and consent compatibility | provider receipt |
| 8.4 | 11 | ComfyUI queued job | worker output and cost report | approved template and GPU policy | GPU worker receipt |
| 8.5 | 0 / 11 | ComfyUI template | worker asset | hash, compatibility, eval target | template migration receipt |
| 8.6 | 12 | audio/caption/timeline plan | manifests and final mix | voice/caption/timing validation | sonic/timeline receipt |
| 8.7 | 11 / 12 | failed or active provider job | retry/resume/cancel/compensation state | idempotency and duplicate-cost gate | recovery receipt |
| 8.8 | 11 | `VisualResearchQuery` | `AssetResearchManifest`, `ImageResolutionMap` | license/provenance/asset-roll gate | asset research receipt |
| 9.1 | 13 | render/package ready for review | `EvaluationReceipt` | category thresholds and evidence | evaluation receipt |
| 9.2 | 13 | asset under review | evidence-rich review state | consent/source/eval completeness | review state receipt |
| 9.3 | 13 | reviewer decision | review command or approval event | role/evidence/voice eligibility | review decision receipt |
| 9.4 | 13 | approval request | blocked or approved state | lineage/consent/format/evaluation gate | approval blocker receipt |
| 9.5 | 14 | approved asset | `PublishingIntent`, Publer outcome | approval/consent/platform validation | publishing receipt |
| 9.6 | 13 / 14 | Telegram quick action | command result or PWA handoff | evidence sufficiency and idempotency | quick review receipt |
| 10.1 | 14 | approved event or rejected pattern | `MemoryAdmission` | evidence and consent compatibility | memory admission receipt |
| 10.2 | 14 | memory event | corrected/expired/quarantined memory | provenance and reversal gate | memory governance receipt |
| 10.3 | 14 | domain event checkpoint | Neo4j projection event | rebuild and lag validation | projection receipt |
| 10.4 | operations overlay | queues/incidents/jobs | operations board state | canonical-state-only reads | operations receipt |
| 10.5 | operations overlay | failed workflow/job | `RecoveryAction` | idempotent safe-action validation | recovery receipt |
| 10.6 | release readiness overlay | system fixtures and production chain | readiness report | full brand-cycle and rebuild gates | readiness receipt |
| 11.1 | agent-factory overlay | department and entity naming request | persona code registry | `DDD-XXXXXXX-TT` code validation | persona registry receipt |
| 11.2 | agent-factory overlay | department and production responsibility | `AgentRoleSpec` catalog | goal, active object, tool, memory, eval, receipt completeness | agent role spec receipt |
| 11.3 | agent-factory overlay | parent agent and specialist task | `SubAgentRoleSpec` binding | bounded authority and parent-stage compatibility | sub-agent binding receipt |
| 11.4 | all gated stages | lifecycle boundary and integration request | `HookSpec`, `ExtensionSpec` | no canonical-state bypass and lifecycle contract | hook/extension receipt |
| 11.5 | stages 3-8 and 13 | agent role and skill need | `SkillBinding`, JIT compiler mode binding | stable-vs-JIT distinction and invocation record requirement | skill binding receipt |
| 11.6 | agent-factory overlay | agent intelligence profile | `AgentReadinessEval` | standards, primitives, tools, memory, evals, receipts, blocked actions | readiness eval receipt |
| 11.7 | all stages | Pi action and tool need | `ToolCapabilitySpec`, department runtime registry | Pydantic I/O, role scope, idempotency, receipt obligation | tool registration receipt |
| 11.8 | adapter/export overlay | approved agent role spec | generated ADK/Agents CLI adapter | generated-only adapter and drift gate | adapter export receipt |

---

## 4. Detailed Epics and Stories

## Epic 1: Governed Workspace and Production Spine

**Epic Goal:** Create the governed product spine that lets the CMF team operate multiple brands, roles, commands, commercial entitlements, receipts, and PWA/Telegram surfaces over the same canonical state.

**Covers:** FR-CMF-01.01 through FR-CMF-01.07.

**User Value:** Owners, Admins, Operators, and commercial administrators can run production without cross-brand leakage, pricing drift, or separate state machines.

**Technical Context:** `contracts/tenancy.py`, `contracts/commercial.py`, `/api/v1/organizations`, `/api/v1/brands`, `/api/v1/auth`, Command Bus, `organizations`, `brand_workspaces`, `role_assignments`, `commercial_entitlements`, `command_log`, `domain_events`, `audit_receipts`.

**CBAR Failure Scenario:** If the system treats workspace setup as generic CRUD, then Telegram actions, provider jobs, memory, and publishing can mutate the wrong brand or expose the wrong offer. The story set therefore locks brand scope and command receipts before creative workflows begin.

### Story 1.1: Contract Kernel and Command Spine

As an Owner, I want every production action to enter through a typed command spine, so that CMF STUDIO can govern state consistently before creative workflows begin.

**Acceptance Criteria:**

- Given a state-changing request reaches FastAPI, when it is accepted, then it is wrapped in a Pydantic command with `command_id`, `command_type`, `organization_id`, `brand_id`, `actor_id`, `idempotency_key`, `payload`, and `requested_at`.
- Given a command is processed, when validation runs, then it follows schema version, authentication, role permission, organization and brand scope, object existence, state transition, consent policy, cost/quota policy, idempotency, provider policy when relevant, confirmation, and receipt-writer checks.
- Given a command succeeds, when persistence completes, then the system writes `command_log`, a domain event, and an audit receipt with correlation ID.
- Given the same idempotency key is submitted again, when the command is replayed, then the system returns the prior command result without duplicating side effects.
- Given a command lacks brand scope, when validation runs, then it fails with `BRAND_SCOPE_VIOLATION`.

**Technical Notes:** Implement base command contracts under `ccp_studio/contracts`, Command Bus handlers under `ccp_studio/api/commands`, repository enforcement for `organization_id` and `brand_id`, and generated TypeScript contract output for PWA and Telegram consumers.

**Legacy and Primitive Mapping:** Legacy receipt-chain references inform audit receipt fields. Active families: SAF, BUS, FBK.

**Prerequisites:** None.

### Story 1.2: Organization and Brand Workspace Lifecycle

As an Owner or Admin, I want to create, suspend, archive, restore, and inspect organizations and brand workspaces, so that each client brand has an isolated production context.

**Acceptance Criteria:**

- Given an Owner creates a brand workspace, when the command succeeds, then `organizations`, `brand_workspaces`, initial role assignment, default retention policy, and domain event are created in one transaction.
- Given an Admin suspends a brand workspace, when an Operator tries to start new production work in that brand, then mutating commands are blocked while read-only audit access remains available to permitted roles.
- Given a workspace is archived, when recovery is requested, then restoration requires an Owner/Admin command and writes an audit receipt.
- Given a workspace is inspected, when the UI renders, then the dashboard shows status, active roles, entitlement state, recent commands, open blockers, and production health.
- Given Brand A is active, when a user queries Brand B objects without permission, then no Brand B object ID, title, asset preview, memory, or provider job is returned.

**Technical Notes:** Use `/api/v1/organizations` and `/api/v1/brands`; enforce RLS or equivalent repository checks; expose lifecycle events `BrandWorkspaceCreated`, `BrandWorkspaceSuspended`, `BrandWorkspaceArchived`, `BrandWorkspaceRestored`.

**Legacy and Primitive Mapping:** Adapts legacy tenant isolation doctrine to Python-first repository enforcement. Active families: SAF, PER, BUS.

**Prerequisites:** Story 1.1.

### Story 1.3: Role-Based Production Permissions

As an Owner or Admin, I want role assignments for Operators, Reviewers, Migration Stewards, Production Stewards, Publishing Approvers, and commercial administrators, so that each actor can only perform the work they are trusted to perform.

**Acceptance Criteria:**

- Given a user receives a role assignment, when they authenticate, then their command permissions are derived from active role assignment, organization scope, and brand scope.
- Given an Operator attempts a Publishing Approval command without the required role, when validation runs, then the command is rejected with `PERMISSION_DENIED`.
- Given a Migration Steward accesses the migration ledger, when they approve a migrated registry entry, then the system records reviewer, source hash, target contract, fixture target, eval target, and receipt.
- Given a Reviewer acts through Telegram, when the quick action reaches FastAPI, then the same role checks apply as PWA.
- Given a role is revoked, when a user repeats a previously valid action, then the action is denied immediately.

**Technical Notes:** Model `RoleAssignment`, `PermissionPolicy`, and command permissions as Pydantic contracts; use repository joins against `role_assignments`; test every role against at least one allowed and one blocked command.

**Legacy and Primitive Mapping:** ERA3 spec discipline requires permission checks in downstream tech specs. Active families: SAF, PER.

**Prerequisites:** Stories 1.1 and 1.2.

### Story 1.4: Commercial Entitlements Without Offer Drift

As a commercial administrator, I want CMF STUDIO to expose only the two documented content charges while still enforcing internal usage and cost controls, so that customer-facing packaging stays simple and truthful.

**Acceptance Criteria:**

- Given a customer-facing price is rendered, when the billing or entitlement layer prepares copy, then the only public content offers are `$29/week` trial Guest Asset Pack and `$99/month` Monthly Asset Engine.
- Given an internal cost quota is applied, when an Operator queues renders, then the system enforces internal usage limits without exposing extra public content tiers.
- Given a trial Guest Asset Pack entitlement is active, when an Asset Package Spec is generated, then it follows the documented Guest Asset Pack format and does not silently reduce lineage, review, or consent requirements.
- Given a Monthly Asset Engine entitlement is active, when production work is requested, then the system still requires source lineage, evaluation receipts, human approval, and valid format registry entries.
- Given commercial entitlement is expired or suspended, when a new production job is requested, then the command is blocked with a receipt stating the commercial policy condition.

**Technical Notes:** Implement `CommercialEntitlement`, `CommercialPolicy`, cost receipts, and entitlement checks in Command Bus validation. Keep billing copy separate from internal provider-cost accounting.

**Legacy and Primitive Mapping:** Product Brief commercial scope and PRD commercial rules. Active families: BUS, SAF, PER.

**Prerequisites:** Stories 1.1 through 1.3.

### Story 1.5: PWA and Telegram State Parity

As an Operator, I want PWA Control Tower and Telegram actions to operate on the same governed object state, so that mobile approvals and notifications cannot fork production reality.

**Acceptance Criteria:**

- Given an object is visible in PWA, when a Telegram notification deep-links to it, then the Telegram payload references the same object ID, brand ID, state, and required command.
- Given a Telegram quick action is submitted, when FastAPI receives it, then it validates Telegram authentication, role, brand scope, idempotency, object state, and receipt writer availability.
- Given a PWA action and Telegram action target the same object, when one succeeds first, then the second sees the updated canonical state and cannot overwrite it blindly.
- Given Telegram cannot show enough evidence for a complex decision, when the user attempts approval, then the bot deep-links to the PWA review surface instead of allowing blind approval.
- Given a state change occurs in PWA, when Telegram renders a follow-up notification, then it reflects the latest canonical state.

**Technical Notes:** Use `/api/v1/webhooks/telegram`, generated TS contracts, command idempotency, and event-driven notifications. Telegram Bot and Mini App are leaf surfaces only.

**Legacy and Primitive Mapping:** Legacy Telegram/Mini App patterns are reference only; state belongs to Python backend. Active families: FRC, FBK, SAF.

**Prerequisites:** Stories 1.1 through 1.4.

### Story 1.6: Pipeline Stage Execution and Orchestration Records

As an Operator or agent supervisor, I want every autonomous or workflow-driven action to run inside a canonical pipeline stage with explicit orchestration records, so that Pi and specialist agents can operate without skipping consent, source truth, brand locks, routing, evaluation, approval, publishing, memory, or projection boundaries.

**Acceptance Criteria:**

- Given a state-changing pipeline action is requested, when orchestration begins, then the system opens or resumes an `OrchestrationRun` linked to organization, brand, actor, active object, and requested outcome.
- Given a stage is selected, when `StageExecutionPlan` is created, then it records canonical PRD pipeline stage, entry object, expected exit object, allowed actor/service, required inputs, blocked actions, and downstream proof obligation.
- Given execution is about to start, when the `ValidationContract` is recorded, then it defines success, failure, thresholds, forbidden skips, required evidence, and required receipts before any worker, DSPy program, provider adapter, renderer, or workflow acts.
- Given Pi dispatches work to a specialist agent, DSPy program, provider adapter, renderer, or workflow, when handoff occurs, then an `AgentHandoffPacket` carries active object, source evidence, upstream receipts, allowed actions, blocked actions, and required downstream receipt.
- Given a JIT Skill compiler is invoked inside the run, when it returns, then `SkillInvocationRecord` stores source context, registry snapshot, compiler fingerprint, contrastive prompt layer, critic result, synthesis result, and eval state.
- Given a stage succeeds, fails, partially completes, blocks, or needs human judgment, when execution closes, then the system records a success receipt, `FailureReceipt`, `FrictionReceipt`, or `HumanHandoffRequest` and only advances when the receipt satisfies the validation contract.
- Given Pi attempts to skip a pipeline stage, mutate canonical state directly, approve its own output, publish externally, or treat Neo4j as canonical truth, when validation runs, then execution is blocked.

**Technical Notes:** Implement `contracts/orchestration.py`, `/api/v1/orchestration`, `OrchestrationRunWorkflow`, `orchestration_runs`, `stage_execution_plans`, `validation_contracts`, `agent_handoff_packets`, `skill_invocation_records`, `failure_receipts`, `friction_receipts`, and `human_handoff_requests`. Command Bus remains the mutation boundary; durable workflows own retries, waits, and resumability.

**Legacy and Primitive Mapping:** Legacy Pi extension principles from `InteractComp`, `TillDone`, `DamageControl`, `ModelRouter`, `TeamOrchestrator`, `SystemSelect`, and `MemoryFolder`, updated for Python/Pydantic/DSPy/Pi. Active families: SAF, FBK, BUS, STR.

**Prerequisites:** Stories 1.1 through 1.5.

---

## Epic 2: Consent, Source, Likeness, and Voice Safety

**Epic Goal:** Make consent, source truth, likeness, file provenance, and voice eligibility product-level blockers before recording, extraction, rendering, review, memory, and publishing.

**Covers:** FR-CMF-02.01 through FR-CMF-02.07.

**User Value:** Guests and clients keep authority over permission boundaries; Operators and Reviewers know exactly when work is allowed, blocked, or requires repair.

**Technical Context:** `/api/v1/consent`, consent record versions, source artifact storage, recording configuration, voice eligibility policy, review gates, render manifests, error code `CONSENT_SCOPE_BLOCKED`.

**CBAR Failure Scenario:** If consent is a checkbox instead of a state machine, then a revoked likeness can still leak into a render, memory, or publishing job. Consent therefore becomes an execution gate across the whole chain.

### Story 2.1: Versioned Consent Records

As a guest or client, I want to provide, narrow, expire, and revoke consent, so that my source, likeness, voice, reuse, retention, and publication boundaries are enforceable.

**Acceptance Criteria:**

- Given a guest grants consent, when the record is saved, then it creates an immutable `consent_record_versions` row with scopes for recording, storage, likeness, derivative generation, provider processing, synthetic voice eligibility, reuse, retention, and publication.
- Given the guest narrows consent, when a new version is created, then the old version remains auditable and new commands evaluate against the current active version.
- Given consent expires, when a render or memory command runs after expiry, then the command is blocked and the receipt names the expired scope.
- Given consent is revoked, when a pending provider job is still queued, then the system blocks future processing and marks affected pending work for quarantine or review.
- Given a reviewer inspects an asset, when consent state is shown, then the UI displays active consent version, scope compatibility, source evidence, and revocation risk.

**Technical Notes:** Implement `ConsentRecordVersion`, `ConsentScope`, `ConsentPolicy`, and consent validation in the Command Bus. Store immutable consent receipts under `brands/{brand_id}/receipts/`.

**Legacy and Primitive Mapping:** Brand Genesis and V9.1 consent doctrine; legacy receipt chain. Active families: SAF, PER.

**Prerequisites:** Epic 1.

### Story 2.2: Recording Setup and Source Artifact Gate

As an Operator, I want to confirm recording setup, master source, backup source, upload route, and quality gates before starting a Complete Expression Session, so that downstream extraction never rests on ambiguous files.

**Acceptance Criteria:**

- Given an Operator starts session setup, when they submit recording configuration, then the system records expected master source, backup route, platform source, upload method, file safety expectations, and quality requirements.
- Given a master source is missing, when session start is requested, then the system blocks the session or requires an explicit approved exception receipt.
- Given a compressed meeting-platform file is uploaded as production source, when a master recording is required, then the system blocks the source from becoming canonical without review.
- Given a source artifact is accepted, when it is stored, then object storage records content hash, source hash, brand ID, session ID, retention policy, provenance, and immutable URI.
- Given upload quality fails, when the Operator reviews setup, then the system shows exact failure category and recovery action.

**Technical Notes:** Use `recording_artifacts`, object storage `brands/{brand_id}/source/`, `SourceArtifact`, `RecordingConfiguration`, and `CompleteExpressionSession` pre-start status.

**Legacy and Primitive Mapping:** V9.1 source doctrine; legacy audio engine references for source separation requirements. Active families: SAF, VOC, FBK.

**Prerequisites:** Stories 1.1 through 2.1.

### Story 2.3: Consent Blockers Across Workflows

As a Reviewer, I want incompatible consent to block processing, rendering, memory, review, and publishing, so that unsafe work cannot slip through another surface.

**Acceptance Criteria:**

- Given a consent scope does not allow provider processing, when a provider job command is submitted, then it fails with `CONSENT_SCOPE_BLOCKED`.
- Given likeness reuse is revoked, when an Operator attempts to re-render a scene using that likeness, then the command is blocked and all affected pending jobs are flagged.
- Given publication consent is missing, when Publishing Intent is drafted, then the draft is blocked before external scheduling.
- Given a memory admission candidate references sensitive source without compatible consent, when admission is reviewed, then approval is unavailable and quarantine is offered.
- Given consent changes after an asset was approved, when future reuse is requested, then the system reevaluates the current consent version rather than trusting historical approval.

**Technical Notes:** Consent policy must be called by provider jobs, render commands, memory admission, review commands, and publishing commands. Add tests for revoked consent in each boundary.

**Legacy and Primitive Mapping:** Consent doctrine, receipt chain, governance gates. Active families: SAF, FBK.

**Prerequisites:** Stories 2.1 and 2.2.

### Story 2.4: Voice-DNA Boost Eligibility and Audio Classification

As a Reviewer, I want Voice-DNA Boost to be allowed only as a documented structural repair exception, so that synthetic voice never becomes the primary voice of truth.

**Acceptance Criteria:**

- Given a SemanticCritic finds a structural gap, when Voice-DNA Boost is requested, then the system first checks recut, verbatim fragment search, prior approved quote, and human pickup request availability.
- Given synthetic bridge voice is eligible, when the command succeeds, then the receipt proves explicit consent, source evidence, visual covering, duration cap, repair hierarchy, and claim restrictions.
- Given synthetic bridge audio is included in a render, when the manifest is produced, then it distinguishes source voice, repaired source voice, synthetic bridge voice, interviewer voice, generated audio, SFX, and music.
- Given a requested synthetic bridge would carry a primary claim, decisive confession, or sensitive assertion, when eligibility runs, then the request is rejected.
- Given Voice DNA evaluation fails, when review opens, then the Reviewer sees the evidence and cannot approve the bridge.

**Technical Notes:** Implement `VoiceDnaBoostEligibility`, `AudioSourceType`, `AudioMixManifest`, `CalibrationReport`, and `AntiDraftCalibrationProgram` integration.

**Legacy and Primitive Mapping:** Legacy `voice_dna_models.py`, `anti_draft_calibrator.py`, SFL failure corpus. Active families: VOC, SAF, FBK.

**Prerequisites:** Stories 2.1 through 2.3.

### Story 2.5: Consent and Source Review Surface

As a Reviewer, I want to inspect consent lineage and source truth before approving assets, memory, publishing, or voice repair, so that approval is evidence-backed.

**Acceptance Criteria:**

- Given an asset is ready for review, when the Reviewer opens it, then the surface shows consent version, source artifact, transcript revision, timestamp references, claim references, voice classification, and file provenance.
- Given a claim lacks source reference, when the review gate runs, then approval is blocked until source truth is repaired or the claim is removed.
- Given source provenance has multiple revisions, when the Reviewer inspects history, then the system shows append-only transcript revisions and source hashes.
- Given the Reviewer approves, when the command is saved, then an `ApprovalEventRecorded` event and audit receipt include consent and source references.
- Given evidence is too complex for Telegram, when a quick approval is attempted, then the action deep-links to PWA.

**Technical Notes:** Implement PWA `Consent and Source Review` and API reads across `consent_record_versions`, `recording_artifacts`, `transcript_revisions`, `evaluation_receipts`, and `approval_events`.

**Legacy and Primitive Mapping:** V9.1 Evaluation Receipt doctrine; legacy receipt chain. Active families: SAF, FBK, PER.

**Prerequisites:** Stories 2.1 through 2.4.

---

## Epic 3: Legacy Intelligence and JIT Skill Governance

**Epic Goal:** Preserve the high-value legacy intelligence and its intentional orchestration logic as typed, evaluated, Python-first assets while blocking direct legacy runtime dependency and stale stack assumptions.

**Covers:** FR-CMF-03.01 through FR-CMF-03.09.

**User Value:** Migration Stewards and AI agents can recover the depth of CCP/CMF intelligence while production remains clean, typed, testable, and greenfield.

**Technical Context:** `/api/v1/legacy-migration`, `/api/v1/registries`, MigrationWorkflow, `legacy_inventory_items`, `migration_ledger_entries`, `legacy_orchestration_intent_records`, `migrated_registry_entries`, `fixture_sets`, `evaluation_targets`, DSPy programs, CI import gate.

**CBAR Failure Scenario:** If legacy intelligence is flattened into prompts, CMF loses its edge. If legacy runtime is imported directly, the greenfield architecture inherits fragmentation. The resolution is typed migration plus explicit compiler/eval targets.

### Story 3.1: Migration Ledger Inventory and Hashing

As a Migration Steward, I want to inventory, classify, hash, and map legacy assets, so that every reused idea has provenance and an approved migration destination.

**Acceptance Criteria:**

- Given a legacy asset is proposed, when it is added to the ledger, then the system records source path, legacy type, registry family/domain, canonicality confidence, owner, runtime language, valuable mechanics, defects, content hash, and status.
- Given an asset is mapped, when the Steward saves the record, then it includes target Python package, Pydantic contract target, DSPy program target when applicable, TypeScript leaf target if applicable, fixture target, eval target, and reviewer.
- Given a hash changes, when the ledger is refreshed, then the system flags the asset for review rather than silently updating the canonical source.
- Given an asset is blocked, when an agent references it, then the system returns the approved reason and replacement target if available.
- Given ledger changes are approved, when the command completes, then a migration receipt is written.

**Technical Notes:** Implement `LegacyAssetInventoryItem`, `MigrationLedgerEntry`, `/api/v1/legacy-migration`, and `MigrationWorkflow` steps through review.

**Legacy and Primitive Mapping:** Directly uses Legacy Inventory ledger fields and content hashes. Active families: STR, SAF, PER.

**Prerequisites:** Epic 1.

### Story 3.2: Registry Conversion, Fixtures, and Evals

As a Migration Steward, I want to convert archetypes, primitives, SDA/SFL assets, CBAR gates, TTT profiles, creative subsystem rules, Voice DNA logic, and CMF references into typed registries and test assets, so that production intelligence is reusable and verifiable.

**Acceptance Criteria:**

- Given a legacy archetype prompt is approved, when migration runs, then it produces a typed registry entry with examples, counterexamples, source hash, route constraints, and eval target.
- Given a cognitive primitive is migrated, when validation runs, then schema, source examples, failure cases, and registry family are required before activation.
- Given SDA/SFL assets are migrated, when fixtures are created, then downstream extraction, audio, compression, and evaluation tests can reference them.
- Given a CMF engine reference is migrated, when it is not approved as production code, then it is recorded as reference behavior or fixture only.
- Given a registry entry lacks eval coverage, when activation is requested, then it is blocked.

**Technical Notes:** Implement `RegistryEntry`, `FixtureSet`, `EvaluationTarget`, `tests/fixtures`, and `tests/evals` targets. Registry activation is a command with receipt.

**Legacy and Primitive Mapping:** 244 primitives, 44 SDA/SFL files, 96 archetype prompts, 34 creative subsystems, CBAR gates, TTT profiles, Voice DNA, CMF references. Active families: PSY, STR, VOC, VSG, FBK.

**Prerequisites:** Story 3.1.

### Story 3.3: JIT Skill Compiler Saturation and Contrast

As an Operator or agent, I want migrated JIT Skill compilers to use saturation context, drafting, contrast, calibration, and evaluation, so that extraction and routing exceed generic script prompting.

**Acceptance Criteria:**

- Given a JIT Skill compiler runs, when it receives input, then it must include source docs, transcript segments, guest dossier, audience reality, brand context, primitive candidates, prior evaluation history, and failure corpus where relevant.
- Given the compiler drafts candidate outputs, when it returns results, then it also returns contrast candidates, anti-draft calibration, evidence references, and confidence.
- Given a compiler output cannot cite saturation context, when it tries to influence routing or extraction, then it is rejected.
- Given a compiler identifies narrative induction material, when it emits guidance, then it distinguishes live guest extraction support from transcript/source extraction.
- Given a compiler output passes, when it is stored, then the receipt includes DSPy program version, input hashes, output schema, eval score, and reviewer state if required.

**Technical Notes:** Implement `JITSkillCompiler`, `DSPyProgramSpec`, `ccp_studio.dspy_programs.jit_skill_compilers`, eval tests, and receipt writing. DSPy owns reasoning, not canonical state.

**Legacy and Primitive Mapping:** Legacy skills modules, anti-draft calibrator, Narrative Intelligence, RSCS saturation/collision/compression/evaluation, CBAR. Active families: STR, PSY, TRG, VOC, FBK.

**Prerequisites:** Stories 3.1 and 3.2.

### Story 3.4: Legacy Import, Hidden Prompt, and Template Gates

As an Architect or reviewer, I want build and workflow gates to reject direct legacy imports, hidden prompt stacks, duplicate registries, and unapproved provider templates, so that the greenfield runtime stays clean.

**Acceptance Criteria:**

- Given production code imports a legacy runtime module directly, when CI runs, then the build fails with `LEGACY_IMPORT_BLOCKED` and points to the migration ledger target.
- Given an agent tries to use an unapproved prompt stack, when the workflow gate runs, then the action is blocked until the prompt is migrated into a typed compiler or registry.
- Given duplicate registry truths exist, when activation is requested, then the system requires conflict resolution before either entry can influence production.
- Given a ComfyUI template lacks approved hash or compatibility notes, when a worker job references it, then the provider route is blocked.
- Given a TypeScript-first assumption appears in a tech spec or story, when review runs, then it is flagged unless it is a permitted leaf runtime.

**Technical Notes:** Add static import checks, registry conflict checks, provider template hash checks, and spec-review checks. Store failures as evaluation receipts and migration review events.

**Legacy and Primitive Mapping:** Legacy Inventory greenfield rule; ERA3/PROMPT audit protocols. Active families: SAF, BUS.

**Prerequisites:** Stories 3.1 through 3.3.

### Story 3.5: Python/DSPy/Pi BMad Spec Workflow

As a PM, Architect, or Tech Writer agent, I want the legacy BMAD and ERA3 writing workflows adapted to Python, Pydantic, DSPy, Pi, CBAR, and CMF greenfield constraints, so that PRDs, epics, architecture, stories, and tech specs stay implementation-grounded.

**Acceptance Criteria:**

- Given a tech spec workflow starts, when the `TechSpecCompilerWorkflow` opens, then it must link to an approved epic/story and create a `TechSpecWorkflow` record.
- Given source context is gathered, when the compiler runs, then it records `FilesReadReceipt` entries for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, and feature-specific CMF/CCF source docs.
- Given traceability is compiled, when validation runs, then the spec includes `RequirementTrace` entries for FR-CMF IDs and `PipelineStageTrace` entries naming stage, entry object, exit object, validation contract, receipt, and allowed actor/service.
- Given implementation context is drafted, when the spec is produced, then the old "Existing Backend Integration" section is replaced with "Greenfield Integration and Legacy Migration Context" listing Pydantic contracts, commands, events, services, durable workflows, DSPy programs, JIT skills, legacy source paths, provider boundaries, renderer boundaries, projection boundaries, and tests.
- Given a spec references the old stack incorrectly, when audit runs, then it is blocked until updated for Python-first Harness, Pydantic contracts, DSPy programs, Pi orchestration, durable workflows, and TypeScript leaf boundaries.
- Given CBAR is applied, when audit runs, then the spec must include tension, failure scenario, resolution demand, and downstream proof tied to tests or receipts.
- Given RSCS is applied, when a recommendation or story detail is included, then it must require project-specific context to verify.
- Given audit completes, when the workflow closes, then it writes a `SpecAuditReceipt` with accepted, revision_requested, or blocked status.

**Technical Notes:** Model `SpecWritingProtocol`, `TechSpecWorkflow`, `TechSpecSourcePacket`, `FilesReadReceipt`, `RequirementTrace`, `PipelineStageTrace`, `CBARCheck`, `SpecAuditReceipt`, `EpicStoryCompiler`, `TechSpecCompiler`, `TechSpecAuditor`, `RequirementTraceCompiler`, and `CBARAuditor`. Tests live under `tests/spec_governance`.

**Legacy and Primitive Mapping:** ERA3 Epic and Story Writing Protocol, ERA3 Tech Spec Writing Protocol, PROMPT_Spec_Build, PROMPT_Spec_Audit, CBAR story adaptation. Active families: STR, SAF, FBK.

**Prerequisites:** Stories 3.1 through 3.4.

### Story 3.6: Intentional Orchestration Migration Contracts

As a Migration Steward, I want every orchestration-bearing legacy module to preserve why it exists and how it coordinates the system, so that CCF/CMF intelligence does not get flattened into disconnected prompts or feature labels.

**Acceptance Criteria:**

- Given a legacy CCF or CMF module is marked for migration, when the Steward creates its migration record, then the record must include product purpose, organism layer, upstream inputs, emitted packets, downstream consumers, required gates, failure modes, and proof obligations.
- Given a migrated module claims to support CRAL, Context Premise, Emotional DNA, Voice DNA, primitive coalitions, SVRE, scene containers, creative subsystems, or asset roles, when activation is requested, then it must cite the source document and expose a typed contract or registry target.
- Given a module is only summarized as style advice, vibes, or a prompt snippet, when activation is requested, then it is blocked until its orchestration role is made explicit.
- Given two legacy modules claim overlapping authority, when migration review runs, then the Steward must resolve whether each belongs to DNA/truth, RNA/transcription, force, delivery, variation, phenotype, evaluation, or outer learning.
- Given the orchestration intent passes review, when a downstream story or tech spec references the module, then it can cite the `LegacyOrchestrationIntentRecord` and inherit its gates.

**Technical Notes:** Add `LegacyOrchestrationIntentRecord` with organism layer enum, input/output packet references, gate references, downstream artifact references, failure modes, source links, and reviewer status. MigrationWorkflow activation requires this record for orchestration-bearing modules.

**Legacy and Primitive Mapping:** PRD-02 CCF, PRD-03 CMF, PRD-08 Conscious Primitives, CCP Biological Orchestration Model, CSIP v3, CRAL, SVRE, CMF Master Scene Intelligence. Active families: STR, PSY, VSG, VOC, SAF, FBK.

**Prerequisites:** Stories 3.1 through 3.5.

---

## Epic 4: Brand Genesis and Locked Creative Universe

**Epic Goal:** Let Operators manufacture, evaluate, repair, approve, and lock the brand creative universe before production depends on it.

**Covers:** FR-CMF-04.01 through FR-CMF-04.07.

**User Value:** Operators and Production Stewards can reuse approved identity, acting, visual, sonic, motion, prop, and publishing assets instead of reinventing the brand for each clip.

**Technical Context:** `/api/v1/brand-genesis`, BrandGenesisWorkflow, `brand_genesis_sessions`, `brand_context_versions`, `genesis_clearance_certificates`, `acting_references`, `rig_manifests`, `micro_semiotic_anchors`, `motion_recipes`, `sfx_assets`, `composition_preferences`.

**CBAR Failure Scenario:** If production starts before brand context is locked, every asset becomes a one-off taste decision. Brand Genesis must therefore produce immutable, reviewed creative truth before rendering begins.

### Story 4.1: Brand Genesis Intake and Session Creation

As an Operator, I want to run Brand Genesis from consent, source media, brand notes, audience, offer, forbidden tone, visual preferences, Voice DNA, visual constitution, and negative-space inputs, so that the creative universe starts from grounded brand evidence.

**Acceptance Criteria:**

- Given an Operator creates a Brand Genesis Session, when required intake is submitted, then the system records brand notes, audience, offer, forbidden tone, visual preferences, Voice DNA references, source media, negative-space inputs, and consent compatibility.
- Given source media lacks consent, when Brand Genesis starts, then the workflow is blocked with `CONSENT_SCOPE_BLOCKED`.
- Given intake is incomplete, when generation is requested, then the system shows missing evidence rather than fabricating a brand constitution.
- Given intake passes, when the workflow starts, then a `BrandGenesisSession` record and receipt are created.
- Given a session is brand-scoped, when another brand is active, then the session cannot be queried or reused across brand boundaries.

**Technical Notes:** Use BrandGenesisWorkflow first steps, `BrandGenesisSession`, `BrandSourceInput`, `VoiceDnaReference`, consent policy, and object storage under `brands/{brand_id}/brand-genesis/`.

**Legacy and Primitive Mapping:** Brand Genesis V3 and Legacy Inventory visual/sonic doctrine. Active families: VSG, VOC, SAF, PER.

**Prerequisites:** Epics 1 through 3.

### Story 4.2: 64-State Acting Library

As an Operator, I want to generate, evaluate, repair, reject, approve, and lock a 64-state acting library, so that future scenes can express emotion and gesture without identity drift.

**Acceptance Criteria:**

- Given acting references are generated, when the grid is shown, then each reference includes emotional family, gesture family, source inputs, provider receipt, and evaluation state.
- Given likeness, gesture clarity, hand quality, style adherence, or production usability fails, when the Operator reviews the reference, then they can reject, repair, or replace it.
- Given a reference is approved, when the acting library version is locked, then the reference is immutable except through a new version.
- Given production attempts to use an unapproved acting reference, when SceneSpec compilation runs, then the command is blocked.
- Given acting reference evaluation changes, when the library version is already locked, then historical outputs remain tied to their original locked version.

**Technical Notes:** Implement `ActingReference`, `ActingLibraryVersion`, evaluation receipts, provider job linkage, and lock command.

**Legacy and Primitive Mapping:** Brand Genesis V3 64-state acting library, Voice DNA doctrine, CMF visual constitution. Active families: ACT, VSG, SAF.

**Prerequisites:** Story 4.1.

### Story 4.3: Paper-Cut Rig and Creative Libraries

As an Operator, I want to create and validate the paper-cut avatar rig, props, micro-semiotic anchors, motion recipes, SFX libraries, composition preferences, platform profiles, and publishing profiles, so that rendering has reusable, approved brand parts.

**Acceptance Criteria:**

- Given a paper-cut rig is generated, when validation runs, then the rig manifest includes layer separation, pivot points, mouth shapes, eye/brow variants, gesture variants, body layers, and preview tests.
- Given a rig preview fails mouth, pivot, layer, or gesture validation, when review opens, then the Operator can repair or reject the rig before lock.
- Given props, anchors, motion recipes, or SFX assets are added, when saved, then each has source, version hash, use constraints, and evaluation state.
- Given a platform profile is configured, when render contracts are compiled, then platform variants inherit caption, negative-space, aspect, and publishing requirements.
- Given a creative library item is cross-brand, when selected, then brand scope validation blocks it.

**Technical Notes:** Implement `RigManifest`, `MicroSemioticAnchor`, `MotionRecipe`, `SfxAsset`, `CompositionPreference`, `PlatformProfile`, and object storage in `brand-genesis`, `rigs`, and `acting-library` paths.

**Legacy and Primitive Mapping:** Brand Genesis V3, Creative Pipeline V2, legacy CMF engine references. Active families: VSG, ACT, VOC, SAF.

**Prerequisites:** Stories 4.1 and 4.2.

### Story 4.4: Brand Context Version Locking and Forking

As an Operator, I want to lock approved Brand Context Versions and fork them for approved changes, so that production can rely on stable creative truth while future changes remain traceable.

**Acceptance Criteria:**

- Given all required Brand Genesis assets pass review, when the Operator locks a Brand Context Version, then the system writes a `GenesisClearanceCertificate`.
- Given a locked version exists, when a production job references it, then the job can only select assets approved within that version.
- Given an Operator changes a core visual identity rule, when future renders need the change, then the system creates a forked Brand Context Version rather than mutating the old version.
- Given an old render is audited, when its brand context is inspected, then it resolves to the exact locked version used at render time.
- Given a stale or cross-brand Brand Context Version is selected, when production starts, then SceneSpec compilation is blocked.

**Technical Notes:** Use immutable `BrandContextVersion`, `GenesisClearanceCertificate`, and version hash references in every downstream SceneSpec and RenderContract.

**Legacy and Primitive Mapping:** Brand Genesis V3 versioning doctrine. Active families: SAF, PER, VSG.

**Prerequisites:** Stories 4.1 through 4.3.

### Story 4.5: Production Gate to Locked Brand Context

As a Production Steward, I want production jobs to require an approved, locked, brand-scoped context, so that no scene can use unapproved or stale identity assets.

**Acceptance Criteria:**

- Given a Complete Editing Session is created, when Brand Context Version is missing or unlocked, then the command fails.
- Given a SceneSpec selects acting references, props, anchors, motion recipes, SFX assets, or caption rules, when validation runs, then each selection must belong to the locked brand context.
- Given a Brand Context Version is superseded, when an old scene is revised, then the Operator must choose whether to preserve original context or explicitly fork into the new approved context.
- Given provider jobs are queued, when they reference brand assets, then provider receipts include Brand Context Version ID and selected asset hashes.
- Given a Reviewer inspects a render, when context lineage is opened, then they can see the locked creative universe behind it.

**Technical Notes:** Enforce brand context gates in CompleteEditingSessionWorkflow, SceneSpec compilation, provider request construction, and review views.

**Legacy and Primitive Mapping:** CMF lineage doctrine, Brand Genesis V3, Creative Pipeline V2. Active families: VSG, SAF, FBK.

**Prerequisites:** Stories 4.1 through 4.4.

---

## Epic 5: Interview Intelligence and Narrative State Induction

**Epic Goal:** Help Operators prepare interviews that activate real expression before capture, then encode that preparation as typed Interview Asset Contracts.

**Covers:** FR-CMF-05.01 through FR-CMF-05.08.

**User Value:** Operators stop asking generic questions and start guiding guests into authentic, source-backed, routeable expression.

**Technical Context:** `/api/v1/research`, `/api/v1/interviews`, InterviewPreparationWorkflow, `research_fields`, `research_evidence`, `cral_findings`, `guest_dossiers`, `audience_reality_briefs`, `context_premises`, `audience_deep_trigger_maps`, `emotional_dna_profiles`, `voice_dna_profiles`, `interviewer_resonance_contexts`, `matrix_of_edging_briefs`, `interview_asset_contracts`, DSPy compilers.

**CBAR Failure Scenario:** If the interview plan is generated from a generic prompt, the guest gives centroid-safe answers and the backend can only clip mediocrity. Research saturation and narrative induction must precede extraction.

### Story 5.1: Research Fields and Evidence Capture

As an Operator, I want to create Research Fields with evidence, citations, claims, confidence, temporal sensitivity, provenance, and gaps, so that interview preparation has reality contact.

**Acceptance Criteria:**

- Given an Operator creates a Research Field, when evidence is added, then each item records claim, source, citation, confidence, temporal sensitivity, provenance, and research gap status.
- Given a claim is temporally sensitive, when it is reused in an interview plan, then the system marks it for freshness verification.
- Given evidence lacks provenance, when it is saved, then it remains draft and cannot support an Interview Asset Contract.
- Given a Research Field is brand-scoped, when another brand is active, then evidence cannot leak across brands.
- Given research is approved for use, when the workflow compiles downstream artifacts, then evidence IDs are retained.

**Technical Notes:** Implement `ResearchField`, `ResearchEvidence`, source provenance contracts, and `/api/v1/research` commands.

**Legacy and Primitive Mapping:** RSCS Law 1 saturation before compression, CRAL/Visual Research references. Active families: STR, SAF.

**Prerequisites:** Epics 1 through 4.

### Story 5.2: Guest Dossier, Audience Reality, Context Premise, and Resonance

As an Operator, I want the system to compile a Guest Dossier, Audience Reality Brief, Context Premise, and Interviewer Resonance Context, so that the session is prepared around the guest's truth and audience collision points.

**Acceptance Criteria:**

- Given approved Research Evidence exists, when compilation runs, then the system produces typed artifacts with source references and confidence.
- Given the Audience Reality Brief includes audience fears, desires, misconceptions, and language, when Context Premise is compiled, then it connects guest truth to audience reality.
- Given Interviewer Resonance Context is compiled, when the Operator reviews it, then it includes authentic curiosity, emotional bridges, questions to avoid, and opening state.
- Given a compilation output contains unsupported inference, when evaluation runs, then it is flagged for revision.
- Given artifacts are approved, when Interview Asset Contracts are compiled, then their IDs are included as saturation context.

**Technical Notes:** Implement DSPy compilers for `GuestDossierCompiler`, `AudienceRealityBriefCompiler`, `ContextPremiseCompiler`, and `InterviewerResonanceCompiler`.

**Legacy and Primitive Mapping:** V9 Interview-First Expression Engine, Matrix of Edging, Claude Interview Deck. Active families: PSY, STR, PRS, SAF.

**Prerequisites:** Story 5.1.

### Story 5.3: Matrix of Edging Brief

As an Operator, I want a Matrix of Edging brief that names primary signals, tension sites, primitive candidates, coalition signatures, edge products, and likely failure points, so that the interview plan is shaped by collisions rather than bland prompts.

**Acceptance Criteria:**

- Given Guest Dossier and Audience Reality Brief exist, when Matrix of Edging compilation runs, then it produces research pass, provocation pass, authentication pass, primitive pass, coalition pass, edge pass, routing pass, and benchmark pass outputs.
- Given a tension site is proposed, when it lacks source evidence, then it is marked speculative and cannot anchor a question.
- Given a likely failure point is detected, when the Operator reviews the plan, then the system shows how to avoid centroid-safe answers.
- Given primitive candidates are attached, when routing later runs, then they remain traceable to the brief.
- Given the Matrix output is too generic, when RSCS evaluation runs, then it fails specificity and must be regenerated.

**Technical Notes:** Implement `MatrixOfEdgingBrief` and DSPy program with RSCS evaluation. Preserve input artifact hashes and output receipt.

**Legacy and Primitive Mapping:** Matrix of Edging, RSCS Law 2 collision, cognitive primitives. Active families: TRG, PSY, HUM, PER.

**Prerequisites:** Stories 5.1 and 5.2.

### Story 5.4: Interviewer Pre-Induction

As an Operator, I want to run interviewer pre-induction before the session, so that I can guide the guest into authentic expression without scripting or manipulation.

**Acceptance Criteria:**

- Given a session plan exists, when pre-induction opens, then the Operator sees authentic curiosity prompts, emotional bridges, questions to avoid, guest-specific resonance, and opening state.
- Given a proposed question would produce a safe centroid answer, when the pre-session gate evaluates it, then the system flags the risk and recommends a collision-bearing route.
- Given the Operator edits a question, when it is saved, then the system preserves the source evidence and induction rationale.
- Given a prompt crosses into manipulation or scripted performance, when review runs, then it is blocked or marked for rewrite.
- Given pre-induction completes, when the session starts, then live guidance references the approved plan without replacing the Operator's judgment.

**Technical Notes:** Implement `InterviewerResonanceContext`, `PreInductionPlan`, and PWA Interview Intelligence Studio state. The output feeds Live Interview Mode.

**Legacy and Primitive Mapping:** V9 activation/articulation doctrine, TTT transition grammar, RSCS. Active families: PRS, PSY, SAF, HUM.

**Prerequisites:** Stories 5.1 through 5.3.

### Story 5.5: Interview Asset Contract and Quality Gate

As an Operator, I want Interview Asset Contracts with target expression state, archetype route, asset derivative, edge product, anchors, repair followups, CMF route, and evaluation logic, so that the session has routeable production intent without becoming a script.

**Acceptance Criteria:**

- Given approved interview preparation artifacts exist, when an Interview Asset Contract is compiled, then each content-intended question includes target expression state, target archetype, asset derivative, edge product, first-line anchor, depth anchor, repair followups, CMF route, and evaluation logic.
- Given an expression state is confused with an output archetype, when the quality gate runs, then the contract is rejected with a correction note.
- Given a contract lacks saturation context, collision strength, specificity, or routeability, when evaluation runs, then it cannot be approved for session use.
- Given the Operator approves a contract, when the Complete Expression Session is created, then the contract ID is bound to the session.
- Given a later extraction uses the contract, when Expression Moments are reviewed, then induction context is visible.

**Technical Notes:** Implement `InterviewAssetContract`, `InterviewDeck`, `InterviewPlanEvaluationReceipt`, and `InterviewAssetContractCompiled` event.

**Legacy and Primitive Mapping:** V9.1 Interview Asset Contract doctrine, Archetype Migration Proposition, RSCS 4 laws. Active families: STR, TRG, PSY, FBK.

**Prerequisites:** Stories 5.1 through 5.4.

### Story 5.6: CRAL, Context Premise, Emotional DNA, and Root-Down Induction

As an Operator, I want each planned interview move to expose the CRAL signal, Context Premise, Emotional DNA or Voice DNA rationale, and intended extraction outcome, so that Narrative State Induction is intentional rather than a polished question list.

**Acceptance Criteria:**

- Given CRAL/SCRE research is available, when a Research Field is promoted into interview preparation, then the system preserves the relevant, believable, undeniable, resonant, surprising, irrefutable, and relatable signal roles that support the planned session.
- Given audience evidence is sufficient, when Context Premise compilation runs, then it emits an Audience Deep Trigger Map with depth mode, hermeneutical gaps, moral-emotional vectors, coping trajectory, regulatory focus when available, confidence, and gaps.
- Given guest or coach source material is available, when Emotional DNA and Voice DNA extraction runs, then the output distinguishes belief content, construction mechanics, emotional path, negative space, suppression markers, escalation triggers, and normative expression targets.
- Given a proposed interview move is displayed, when the Operator inspects it, then the system shows CRAL evidence, Context Premise link, Emotional DNA or Voice DNA rationale when available, Matrix of Edging position, target expression state, and intended asset extraction outcome.
- Given the system lacks enough evidence for an Emotional DNA or full-depth Context Premise claim, when it compiles the plan, then it marks the rationale as partial, uses the appropriate shallow mode, and prevents unsupported psychological certainty.

**Technical Notes:** Implement or extend `CRALFinding`, `ContextPremise`, `AudienceDeepTriggerMap`, `EmotionalDNAProfile`, `VoiceDNAProfile`, `InductionRationale`, and DSPy programs for CRAL research, Context Premise, Emotional DNA extraction, Voice DNA compilation, and interview move explanation.

**Legacy and Primitive Mapping:** Sovereign CRAL, Context Premise Engine proposals, CSIP v3 Voice/Emotional DNA, Voice DNA Framework, Matrix of Edging, PRD-02 CCF, PRD-08 primitives. Active families: PSY, STR, TRG, VOC, PRS, SAF.

**Prerequisites:** Stories 5.1 through 5.5 and Story 3.6.

---

## Epic 6: Complete Expression Sessions and Guest Asset Packs

**Epic Goal:** Convert live narrative induction and grounded transcript/source extraction into approved Expression Moments, valid routes, and source-backed Guest Asset Pack specs.

**Covers:** FR-CMF-06.01 through FR-CMF-06.08.

**User Value:** Operators and Reviewers can transform an interview into routable assets without fabricating beyond source expression.

**Technical Context:** `/api/v1/expression-sessions`, `/api/v1/expression-moments`, `/api/v1/asset-packages`, CompleteExpressionSessionWorkflow, recording artifacts, transcript revisions, timestamped anchor hits, expression moments, archetype routes, asset package specs.

**CBAR Failure Scenario:** If the system only hunts clips after the transcript exists, it misses the human induction layer. If it routes by generic format, it fabricates. The resolution is dual-layer extraction plus valid route registries.

### Story 6.1: Complete Expression Session Creation

As an Operator, I want to create and manage a Complete Expression Session from approved interview contracts, recording configuration, source artifacts, quality gates, and consent state, so that capture begins from a governed plan.

**Acceptance Criteria:**

- Given an approved Interview Asset Contract exists, when the Operator creates a session, then the session binds brand ID, guest/client, consent state, recording configuration, source requirements, interview contract, and status.
- Given consent or recording setup is incomplete, when session start is requested, then the command is blocked.
- Given the Operator changes active brand context, when the session is queried, then only sessions from the active brand are returned.
- Given a session starts, when the command succeeds, then `CompleteExpressionSessionStarted` event and audit receipt are written.
- Given the session is paused or marked failed, when status changes, then state transitions use explicit statuses.

**Technical Notes:** Implement `CompleteExpressionSession`, `CreateCompleteExpressionSession`, session status machine, and workflow start command.

**Legacy and Primitive Mapping:** V9.1 Complete Expression Session schema. Active families: SAF, STR, FBK.

**Prerequisites:** Epics 1 through 5.

### Story 6.2: Source Ingestion, Transcript Alignment, and Provenance

As an Operator, I want to ingest, preserve, align, and version recordings, audio tracks, transcripts, timestamps, and upload provenance, so that every downstream moment has source lineage.

**Acceptance Criteria:**

- Given recording artifacts are uploaded, when ingestion succeeds, then each artifact records hash, source type, upload route, retention policy, brand ID, session ID, and immutable URI.
- Given a transcript is generated or uploaded, when alignment completes, then transcript revisions are append-only and timestamp aligned to source artifacts.
- Given a transcript revision supersedes another, when extraction runs, then it references the selected revision rather than mutating previous revisions.
- Given audio contains interviewer and guest tracks, when classification is available, then source voice and interviewer voice are represented distinctly.
- Given source artifact corruption is detected, when ingestion runs, then the workflow reaches terminal failure requiring re-upload.

**Technical Notes:** Use `recording_artifacts`, `transcript_revisions`, object storage `source` and `transcripts`, and transcript provider capability contract.

**Legacy and Primitive Mapping:** Legacy audio engine and source doctrine. Active families: VOC, SAF.

**Prerequisites:** Story 6.1.

### Story 6.3: Anchor Hit and Expression Moment Candidate Detection

As an Operator, I want the system to detect anchor hits, emotional shifts, transcript segments, timestamps, cues, and candidate Expression Moments, so that review starts from source-backed possibilities.

**Acceptance Criteria:**

- Given aligned transcript and source artifacts exist, when extraction runs, then each candidate includes timestamp range, transcript segment, source artifact reference, induction context, anchor hit, route rationale, and confidence.
- Given an emotional shift is detected, when candidate output is produced, then the system cites evidence rather than only labeling sentiment.
- Given a candidate lacks source support, when extraction completes, then it is marked rejected candidate or needs review, not approved.
- Given a JIT Skill compiler participates, when it emits candidates, then it returns saturation context, contrast output, and anti-draft calibration.
- Given extraction fails, when the workflow retries, then previous accepted artifacts and receipts remain intact.

**Technical Notes:** Implement `TimestampedAnchorHit`, `ExpressionMomentCandidate`, DSPy extraction programs, and JIT compiler receipts.

**Legacy and Primitive Mapping:** V9/V9.1 expression extraction, 96 archetype prompts, JIT skills, RSCS. Active families: STR, TRG, PSY, VOC.

**Prerequisites:** Stories 6.1 and 6.2.

### Story 6.4: Expression Moment Review and Boundary Control

As a Reviewer, I want to approve, reject, fix boundaries, split, merge, annotate, or place sensitivity holds on Expression Moments, so that only truthful, usable source fragments reach routing.

**Acceptance Criteria:**

- Given candidates exist, when the Reviewer opens the review surface, then each candidate shows source video/audio reference, transcript segment, timestamp range, induction context, route rationale, and sensitivity flags.
- Given a boundary is wrong, when the Reviewer fixes it, then the system writes a supersession record and preserves the original candidate.
- Given two candidates belong together, when merge is approved, then the merged Expression Moment records both source ranges.
- Given a sensitivity hold is placed, when routing is attempted, then routing is blocked until the hold is resolved.
- Given an Expression Moment is approved, when stored, then it becomes immutable except through supersession.

**Technical Notes:** Implement `ExpressionMoment`, review commands, status machine, and immutable approval events.

**Legacy and Primitive Mapping:** V9.1 review doctrine, CBAR, receipt chain. Active families: FBK, SAF, PER.

**Prerequisites:** Stories 6.1 through 6.3.

### Story 6.5: Archetype and Asset Derivative Routing

As a Production Steward, I want approved Expression Moments routed through Core Content Archetype, Asset Derivative, Meme Mechanism, Reaction Archetype, and CMF Render Mode registries, so that every output format is valid and source-supported.

**Acceptance Criteria:**

- Given an Expression Moment is approved, when routing runs, then it evaluates only active migrated registry entries.
- Given a route is selected, when the receipt is written, then it includes expression moment ID, route ID, registry versions, evidence, route rationale, and failure alternatives.
- Given an Expression Moment lacks evidence for a requested route, when routing runs, then the route is rejected rather than fabricated.
- Given a format is unsupported by the registries, when requested, then the system blocks it with a clear unsupported-format receipt.
- Given a route passes, when an Asset Package Spec is generated later, then route lineage remains attached.

**Technical Notes:** Implement `ArchetypeRoute`, registry query service, `RouteSelectionProgram`, and unsupported-format rejection.

**Legacy and Primitive Mapping:** Archetype System Migration Proposition, 96 archetype prompts, 34 creative subsystems. Active families: STR, HUM, TRG, PSY.

**Prerequisites:** Stories 3.2, 3.3, and 6.4.

### Story 6.6: Guest Asset Pack Spec Generation

As a Production Steward, I want to generate trial Guest Asset Pack specs from approved, routed Expression Moments, so that pack deliverables remain source-backed and commercially aligned.

**Acceptance Criteria:**

- Given enough approved source material exists, when a trial Guest Asset Pack spec is generated, then it targets 4 videos, 2 carousels, 2 meme visuals, 2 poll visuals, and 2-3 reaction seeds where source supports them.
- Given source material does not support one item, when the pack is generated, then the system marks the gap instead of inventing material.
- Given a package item is listed, when reviewed, then it maps to Expression Moment, route, registry entry, brand context requirement, evaluation state, and production readiness.
- Given the commercial entitlement is trial Guest Asset Pack, when pack scope is rendered, then it uses `$29/week` trial language only.
- Given a package is approved, when Complete Editing Sessions are created, then each item carries source lineage and route state.

**Technical Notes:** Implement `AssetPackageSpec`, `AssetPackageItem`, `/api/v1/asset-packages`, and package evaluation receipt.

**Legacy and Primitive Mapping:** V9.1 Guest Asset Pack standard. Active families: BUS, STR, FBK.

**Prerequisites:** Stories 6.1 through 6.5.

### Story 6.7: Rejected Candidate and Coalition-Fatality Memory

As an Operator, I want failed candidates, rejected routes, and coalition-fatality evidence preserved without becoming truth, so that future compilers learn from failures safely.

**Acceptance Criteria:**

- Given a candidate is rejected, when rejection is saved, then the system stores reason, evidence, reviewer, route attempt, and failure category.
- Given a route fails because source support is insufficient, when the failure is stored, then it is available as negative evidence for JIT compilers and future routing evals.
- Given rejected material contains sensitive or consent-incompatible content, when preservation is attempted, then it is blocked or quarantined according to consent policy.
- Given a future compiler references a rejected pattern, when it uses the evidence, then it must cite the rejection and cannot treat it as approved truth.
- Given memory admission is later proposed from rejected evidence, when reviewed, then it requires explicit evidence and cannot bypass memory gates.

**Technical Notes:** Store rejected candidates, route failures, and failure corpora with source references and consent checks. Do not admit as memory until Epic 10 gates.

**Legacy and Primitive Mapping:** SFL failure corpus, CBAR, RSCS evaluation. Active families: FBK, SAF, STR.

**Prerequisites:** Stories 6.3 through 6.6.

---

## Epic 7: Complete Editing Sessions and Reproducible Scenes

**Epic Goal:** Ensure every production output is created inside a Complete Editing Session with source lineage, Brand Context Version, SceneSpec, composition state, provider jobs, render contracts, evaluation receipts, revisions, and approvals.

**Covers:** FR-CMF-07.01 through FR-CMF-07.09.

**User Value:** Production Stewards and Reviewers can reconstruct why a scene exists and why it looks the way it does.

**Technical Context:** `/api/v1/editing-sessions`, `/api/v1/scenes`, CompleteEditingSessionWorkflow, `complete_editing_sessions`, `creative_states`, `scene_specs`, `scene_container_plans`, `scene_component_selections`, `creative_subsystem_decisions`, `asset_roll_plans`, `composition_jobs`, `asset_selections`, `layer_manifests`, `animation_plans`, `render_contracts`, `render_outputs`.

**CBAR Failure Scenario:** If scene lineage collapses into a final media URL, CMF cannot reproduce, repair, audit, or defend the output. Composition and rendering metadata must be first-class.

### Story 7.1: Complete Editing Session Creation From Approved Source

As a Production Steward, I want to create Complete Editing Sessions only from approved Expression Moments, route decisions, Asset Package items, and locked Brand Context Versions, so that editing never begins from unsupported material.

**Acceptance Criteria:**

- Given an approved Expression Moment and route exist, when a Complete Editing Session is created, then it binds source expression, route, asset package item if present, locked Brand Context Version, actor, brand, and status.
- Given Expression Moment approval is missing, when creation is attempted, then the command fails.
- Given Brand Context Version is unlocked or stale, when creation is attempted, then the command fails.
- Given the session is created, when persisted, then `CompleteEditingSessionCreated` event and audit receipt are written.
- Given the session is queried, when displayed, then source, route, brand context, and production readiness are visible.

**Technical Notes:** Implement `CompleteEditingSession`, `CreateCompleteEditingSession`, and workflow start after source/brand gates.

**Legacy and Primitive Mapping:** Creative Pipeline V2, V9.1 expression routing, Brand Genesis V3. Active families: SAF, STR, VSG.

**Prerequisites:** Epics 1 through 6.

### Story 7.2: SceneSpec, Creative State, and Render Contract Compilation

As a Production Steward, I want the system to compile SceneSpecs, Creative State, Render Contracts, asset selections, renderer routes, evaluation requirements, platform variants, and revision policies, so that each job is executable and reviewable.

**Acceptance Criteria:**

- Given a Complete Editing Session exists, when compilation runs, then it produces `SceneSpec`, `CreativeState`, `RenderContract`, `AssetSelection`, platform variants, evaluation requirements, and revision policy.
- Given selected assets are not approved in the locked Brand Context Version, when compilation validates, then it fails.
- Given platform variants require captions or negative space, when Render Contract is compiled, then those constraints are explicit.
- Given revision policy is missing, when provider jobs are queued, then the workflow blocks until the policy exists.
- Given compilation succeeds, when the receipt is written, then it references source expression, route, brand context, and input hashes.

**Technical Notes:** Use `SceneSpecCompiled` event, `scene_specs`, `creative_states`, `render_contracts`, and contract tests.

**Legacy and Primitive Mapping:** CMF engine manifest lineage, Creative Pipeline V2. Active families: VSG, STR, FBK.

**Prerequisites:** Story 7.1.

### Story 7.3: Ideogram 4 CompositionJob Lineage

As a Production Steward, I want Ideogram 4 `CompositionJob` JSON preserved as first-class composition lineage, so that composition plates can guide scenes without becoming final identity or text authority.

**Acceptance Criteria:**

- Given an Ideogram route is selected, when composition is submitted, then the system stores `CompositionJob` JSON, prompt hash, constraints, provider metadata, and correlation ID.
- Given Ideogram returns a composition plate, when saved, then composition plate URI, output hash, composition analysis, and provider receipt are linked to the Complete Editing Session.
- Given the plate contains final-looking text or identity drift, when evaluation runs, then the plate is restricted to background/composition use, rejected, or repaired.
- Given downstream edits occur, when they are recorded, then they reference the originating `CompositionJob` and plate.
- Given a scene is audited, when composition lineage is opened, then the `CompositionJob`, prompt hash, plate URI, analysis, downstream edits, and final text plan are visible.

**Technical Notes:** Implement `CompositionJob`, `CompositionPlan`, provider adapter `providers/ideogram.py`, and composition lineage storage under `brands/{brand_id}/composition-plates/`.

**Legacy and Primitive Mapping:** Product Brief Ideogram 4 doctrine, Creative Pipeline V2. Active families: VSG, SAF, FBK.

**Prerequisites:** Stories 7.1 and 7.2.

### Story 7.4: Layer Manifests, Animation Plans, EDL, Captions, and Sonic Plans

As a Production Steward, I want approved brand layers, manifests, animation plans, EDLs, caption manifests, and sonic plans created and evaluated, so that deterministic rendering can assemble assets transparently.

**Acceptance Criteria:**

- Given a SceneSpec is approved for deterministic rendering, when assembly planning runs, then it produces layer manifest, animation plan, edit decision list, timeline manifest, caption manifest, and sonic plan.
- Given audio components include source, interviewer, repaired source, synthetic bridge, SFX, and music, when the sonic plan is built, then each component is classified and traceable.
- Given caption timing conflicts with source timing, when evaluation runs, then the plan fails for repair.
- Given an animation plan selects rig layers, when validated, then those layers must belong to the locked Brand Context Version.
- Given a plan passes, when provider/render jobs run, then receipts include manifest hashes and selected asset IDs.

**Technical Notes:** Implement `LayerManifest`, `AnimationPlan`, `TimelineManifest`, `CaptionManifest`, `AudioMixManifest`, and EDL contracts.

**Legacy and Primitive Mapping:** Legacy audio engine, caption engine, timeline generator, rig manifests. Active families: VSG, VOC, SAF.

**Prerequisites:** Stories 7.1 through 7.3.

### Story 7.5: Revision and Reconstruction Audit

As a Reviewer or Operator, I want revisions to preserve source lineage, composition lineage, provider receipts, evaluation history, version history, and approval history, so that final scenes remain reconstructable.

**Acceptance Criteria:**

- Given a scene is revised, when the revision command is saved, then it records reason, changed fields, prior version, actor, source lineage, provider receipts, and evaluation state.
- Given a scene is revised multiple times, when final audit opens, then every revision can be traced to source expression, route, brand context, provider job, evaluation receipt, and human decision.
- Given a revision would drop source lineage, when validation runs, then it is blocked.
- Given a render is approved after revisions, when approval is saved, then approval references the final version and prior revision chain.
- Given a user asks why a scene looks the way it does, when reconstruction runs, then the system resolves source, route, brand context, composition JSON, provider jobs, render manifests, and approvals.

**Technical Notes:** Implement revision history for `complete_editing_sessions`, `scene_specs`, `render_outputs`, `evaluation_receipts`, and approval events.

**Legacy and Primitive Mapping:** CMF beat-fingerprint/manifest lineage doctrine. Active families: FBK, SAF, PER.

**Prerequisites:** Stories 7.1 through 7.4.

### Story 7.6: Scene Containers, Creative Subsystems, and Asset Roll Orchestration

As a Production Steward, I want SceneSpecs to preserve CMF scene-container, scene-component, creative-subsystem, and asset-roll decisions, so that every scene can explain what perceptual and narrative job it is performing.

**Acceptance Criteria:**

- Given a SceneSpec is compiled, when scene orchestration runs, then it selects a biological arc container such as HOOK, SETUP, CHALLENGE, TURNING_POINT, RESOLUTION, or VISION before choosing a cinematic component.
- Given a container is selected, when a component fills it, then the system records why that component is valid for the container and which constraints it satisfies or violates.
- Given creative subsystem gates are relevant, when the SceneSpec is saved, then it records decisions from first-frame imprint, recognition window, gaze transfer, excitation transfer, arousal-pacing, temporal binding, element count, silence container, or other migrated subsystem gates as applicable.
- Given assets are selected, when the Asset Roll Plan is generated, then each A-Roll, B-Roll, C-Roll, D-Roll, or E-Roll item carries its narrative/emotional/explanatory/authentic/cultural function and source or licensing status.
- Given a scene is reviewed or revised, when the Reviewer asks why the scene looks and feels this way, then the system can reconstruct source expression, route, container, component, subsystem gates, asset roll choices, sonic plan, CompositionJob when used, render manifests, and approvals.

**Technical Notes:** Add `SceneContainerPlan`, `SceneComponentSelection`, `CreativeSubsystemDecision`, and `AssetRollPlan` contracts. SceneSpec compilation consumes migrated CMF Master Scene Intelligence, Creative Subsystems, Scene Containers, Scene Components, and Conscious Asset Strategy Guide registry entries.

**Legacy and Primitive Mapping:** CMF Master Scene Intelligence, CMF Creative Subsystems, Scene Containers, Scene Components, Conscious Asset Strategy Guide, PRD-03 CMF. Active families: VSG, STR, VOC, ACT, FBK, SAF.

**Prerequisites:** Stories 7.1 through 7.5 and Story 3.6.

---

## Epic 8: Governed Rendering and Provider Operations

**Epic Goal:** Execute deterministic and generative rendering through explicit provider capability contracts, receipt-backed jobs, retryable workflows, and self-hosted GPU worker control.

**Covers:** FR-CMF-08.01 through FR-CMF-08.08.

**User Value:** Production Stewards can render assets without hidden scripts, provider drift, duplicate costs, or opaque final artifacts.

**Technical Context:** `/api/v1/provider-jobs`, `/api/v1/renders`, `/api/v1/visual-research`, `/api/v1/webhooks/providers`, provider adapters, `provider_jobs`, `visual_research_queries`, `visual_candidates`, `asset_research_manifests`, `image_resolution_maps`, `render_contracts`, `render_outputs`, ComfyUI worker assets, object storage provider paths.

**CBAR Failure Scenario:** If provider calls are hidden one-off scripts, costs and failures become unrecoverable. Provider operations must therefore be typed, receipt-backed, idempotent, and separable from canonical business decisions.

### Story 8.1: Provider Capability Registry and Job Receipts

As a Production Steward, I want provider jobs and receipts for approved providers and renderers, so that each external or rendering action is auditable, retryable, and cost-visible.

**Acceptance Criteria:**

- Given a provider is configured, when the capability record is activated, then it declares provider name, capability ID, model/workflow version, allowed input types, output contract, cost policy, retry policy, and evaluation requirements.
- Given a provider job is submitted, when it is accepted, then the provider request includes input artifact hashes, prompt hash if applicable, parameters, brand ID, scene ID, and correlation ID.
- Given a provider returns output, when normalized, then the receipt stores output artifact hashes, cost, retries, status, failure details if any, and created domain event.
- Given a provider capability is unavailable, when a job is requested, then the command fails with `PROVIDER_CAPABILITY_UNAVAILABLE`.
- Given a provider webhook arrives, when processed, then it updates provider job state through an approved command path.

**Technical Notes:** Implement `ProviderCapabilityRecord`, `ProviderRequest`, `ProviderResponse`, `ProviderReceipt`, provider adapter interface, and fake provider tests.

**Legacy and Primitive Mapping:** Legacy adapter registry models and receipt chain. Active families: SAF, FBK, BUS.

**Prerequisites:** Epics 1 through 7.

### Story 8.2: Deterministic Remotion and Motion Canvas Rendering

As a Production Steward, I want deterministic assets routed through Remotion or Motion Canvas using approved brand layers, final text rendering, captions, timing, motion recipes, and sonic plans, so that final assembly does not depend on flattened image output.

**Acceptance Criteria:**

- Given a Render Contract selects a deterministic route, when the renderer starts, then it consumes selected brand layers, rig manifest, final text plan, captions, motion recipes, SFX plan, scene timings, audio mix manifest, and platform variants.
- Given final text exists, when rendering occurs, then final text is rendered by the deterministic renderer, not delegated to a generative image provider.
- Given a selected layer is not in locked Brand Context Version, when rendering validates, then it fails.
- Given rendering succeeds, when output is saved, then preview/final URIs, manifest hashes, renderer version, and receipt are stored.
- Given rendering fails, when retry is requested, then previously completed artifacts remain intact.

**Technical Notes:** Implement Remotion and Motion Canvas worker boundaries as TypeScript leaf runtimes consuming generated contracts.

**Legacy and Primitive Mapping:** CMF engine references, caption engine, timeline generator. Active families: VSG, VOC, SAF.

**Prerequisites:** Story 8.1 and Epic 7.

### Story 8.3: Generative Provider Adapters

As a Production Steward, I want special or generative assets routed through approved provider adapters while preserving prompt hashes, metadata, inputs, outputs, costs, retries, and evaluation state, so that generative work remains reproducible enough for review.

**Acceptance Criteria:**

- Given GPT Image 2, Flux 2 Klein 9b, Qwen-Image-Layered, SAM3, LavaSR, or MOSS-TTS is used, when the job is submitted, then it passes through a provider adapter and capability record.
- Given a provider request uses source assets, when submitted, then input artifact hashes and consent compatibility are recorded.
- Given provider output is returned, when normalized, then it is stored under `brands/{brand_id}/provider-raw/` with output hashes and receipt.
- Given an output fails evaluation, when the job completes, then it is not promoted to approved render output without revision or rejection.
- Given model metadata is missing, when receipt is created, then the provider job fails receipt validation.

**Technical Notes:** Implement provider-specific adapters behind the common interface. Domain services cannot call provider SDKs directly unless they are provider adapter services.

**Legacy and Primitive Mapping:** Provider capability registry doctrine, visual research references. Active families: VSG, VOC, FBK.

**Prerequisites:** Stories 8.1 and 7.2.

### Story 8.4: Self-Hosted ComfyUI Docker GPU Worker

As a Production Steward, I want batch-first self-hosted ComfyUI Docker GPU workers on AWS or Google Cloud with 24GB or 32GB VRAM, so that approved workflow templates can render without relying on external hidden execution services.

**Acceptance Criteria:**

- Given a ComfyUI route is selected, when the worker starts, then it records GPU tier, cloud provider, Docker image, queue state, workflow hash, input assets, and job IDs.
- Given a queued job executes, when it completes an output checkpoint, then the output is uploaded, receipt is written, and progress is persisted.
- Given the queue drains, when no jobs remain, then the worker shuts down and reports cost.
- Given the worker is interrupted, when recovery runs, then completed outputs remain intact and incomplete jobs are requeued from checkpoint.
- Given an unapproved workflow template is referenced, when the job validates, then it is blocked.

**Technical Notes:** Implement `GpuWorkerJob`, worker queue, ComfyUI adapter, checkpointing, cloud metadata, cost reporting, and shutdown policy.

**Legacy and Primitive Mapping:** Legacy ComfyUI JSON templates such as `Wan 2.2 i2v.json` and `qwen-image-layered-image2image.json`. Active families: VSG, SAF, FBK.

**Prerequisites:** Stories 8.1 and 8.3.

### Story 8.5: ComfyUI Template Migration to Worker Assets

As a Migration Steward, I want approved ComfyUI JSON templates migrated into worker assets with hashes, compatibility notes, required inputs, output contracts, defects, and eval targets, so that GPU rendering uses governed templates.

**Acceptance Criteria:**

- Given a ComfyUI JSON template is selected, when migration is approved, then the worker asset stores source path, content hash, required inputs, output contract, compatibility notes, known defects, eval target, and reviewer.
- Given a template requires input assets, when validation runs, then the worker checks all typed inputs before queueing.
- Given a template output contract changes, when the worker uses an old template, then the system blocks or requires revalidation.
- Given a template fails eval, when activation is requested, then it remains inactive.
- Given a render uses a template, when receipt is written, then the template hash is included.

**Technical Notes:** Store worker assets under `worker-assets/comfyui-workflows`; connect to MigrationWorkflow and ProviderCapabilityRecord.

**Legacy and Primitive Mapping:** Legacy Inventory CMF engine and ComfyUI templates. Active families: VSG, SAF.

**Prerequisites:** Stories 3.1, 3.2, and 8.4.

### Story 8.6: Audio, Caption, Timeline, and Mix Assembly

As a Production Steward, I want source audio, interviewer audio, restored audio, synthetic bridge audio, SFX, music, captions, and final mix separated into auditable timeline components, so that sonic and caption quality can be reviewed and repaired.

**Acceptance Criteria:**

- Given a render uses audio, when the audio mix manifest is produced, then source, interviewer, restored, synthetic bridge, SFX, music, and final mix components are classified.
- Given captions are generated, when the caption manifest is built, then it includes timing, text source, style constraints, and platform variant.
- Given audio ducking is applied, when evaluated, then ducking math and affected segments are recorded.
- Given synthetic bridge voice exists, when rendered, then it follows Voice-DNA Boost restrictions from Epic 2.
- Given final assembly completes, when review opens, then the Reviewer can inspect timeline, audio, caption, and mix lineage.

**Technical Notes:** Implement `AudioMixManifest`, `CaptionManifest`, `TimelineManifest`, and tests against legacy audio/caption references.

**Legacy and Primitive Mapping:** Legacy audio engine, caption engine, timeline generator, SFL failure corpus. Active families: VOC, FBK, SAF.

**Prerequisites:** Stories 2.4, 7.4, and 8.2.

### Story 8.7: Provider Job Retry, Resume, Cancel, and Compensation

As an Operator, I want provider jobs to pause, retry, resume, cancel, or compensate idempotently, so that failures do not corrupt completed work or duplicate cost and publishing side effects.

**Acceptance Criteria:**

- Given a provider timeout occurs, when retry policy allows retry, then only incomplete work is retried and prior receipts remain immutable.
- Given partial output exists, when compensation runs, then completed artifacts are preserved and missing work is isolated.
- Given cancel is requested, when the job is cancellable, then provider state and canonical state are reconciled by receipt.
- Given a duplicate provider webhook arrives, when processed, then idempotency prevents duplicate provider job completion events.
- Given retry would duplicate billing or publishing, when validation runs, then the command is blocked or escalated for manual review.

**Technical Notes:** Durable workflows own provider retries, timeouts, checkpoints, compensation, and terminal failure. Use `provider_jobs`, `operational_incidents`, and `recovery_actions`.

**Legacy and Primitive Mapping:** Legacy circuit-breaker and receipt references. Active families: SAF, FBK, BUS.

**Prerequisites:** Stories 8.1 through 8.6.

### Story 8.8: SVRE, Aurore, and Asset Research Engine Routing

As a Production Steward, I want visual and found-asset research to run through governed SVRE/Aurore-style contracts, so that asset choices are emotionally precise, source-traced, licensed, and compatible with the scene's asset-roll intent.

**Acceptance Criteria:**

- Given a SceneSpec requires visual references or found assets, when visual research runs, then the system creates a `VisualResearchQuery` with scene ID, asset-roll intent, emotional state, symbolic role, contradiction value, brand alignment, source constraints, and licensing requirements.
- Given candidates are returned, when scoring runs, then each candidate is evaluated for emotional mode match, tribal/cultural proximity, symbolic role, visual congruence, authenticity, source quality, known-person validity when relevant, and direct-use versus composition-reference status.
- Given a candidate is not licensed for direct use, when selected, then it can only be routed as composition reference or blocked according to policy.
- Given SVRE/Aurore legacy logic references superseded execution services, when migrated, then provider execution is adapted to current CMF STUDIO routes and self-hosted ComfyUI worker policy.
- Given an asset is selected, when the Render Contract is compiled, then the `AssetResearchManifest` and `ImageResolutionMap` link selected candidate, alternatives, scoring receipt, license decision, source URL or reference, and downstream render route.

**Technical Notes:** Implement `VisualResearchQuery`, `VisualCandidate`, `AssetResearchManifest`, `ImageResolutionMap`, `LicensingDecision`, and `/api/v1/visual-research`. Use SVRE/Aurore as migration source for SearXNG categories, Pinterest/source search, T-Score-like scoring, known-person validity, and source win-rate logic while keeping provider execution behind current approved adapters.

**Legacy and Primitive Mapping:** Sovereign Visual Research Engine, Aurore v2, Conscious Asset Strategy Guide, CMF Manual asset hunt logic, PRD-03 CMF. Active families: VSG, SAF, TRB, SOC, FBK.

**Prerequisites:** Stories 7.6, 8.1, 8.3, and 8.5.

---

## Epic 9: Review, Approval, and Publishing Intent

**Epic Goal:** Make quality, truth, identity, consent, format, and publishing readiness reviewable before external scheduling.

**Covers:** FR-CMF-09.01 through FR-CMF-09.07.

**User Value:** Reviewers can approve only assets that are evidenced, truthful, identity-safe, platform-valid, and publication-ready.

**Technical Context:** `/api/v1/evaluations`, `/api/v1/reviews`, `/api/v1/publishing-intents`, `/api/v1/webhooks/publer`, `evaluation_receipts`, `review_decisions`, `revision_requests`, `approval_events`, `publishing_intents`, `publer_jobs`, `publishing_outcomes`.

**CBAR Failure Scenario:** If publishing follows provider completion, the system releases output before truth, consent, identity, and format checks survive human review. Publishing Intent must be internal authority; Publer is only an adapter.

### Story 9.1: Evaluation Receipt Generation

As a Reviewer, I want evaluation receipts for source truth, archetype fit, expression depth, identity, likeness, composition, style, motion, platform fit, negative space, micro-semiotic anchors, routeability, and publishing readiness, so that review starts with evidence.

**Acceptance Criteria:**

- Given a render or asset package reaches review readiness, when evaluation runs, then receipts are created for required evaluation categories.
- Given an evaluation category hard-fails, when approval is requested, then approval is blocked.
- Given a receipt references source truth, when opened, then it shows source artifact, transcript segment, timestamp, route, and evaluator version.
- Given evaluator output lacks evidence, when receipt validation runs, then the receipt is invalid.
- Given evaluation is rerun after revision, when saved, then the prior receipt remains immutable and the new receipt links to the revised object.

**Technical Notes:** Implement `EvaluationReceipt`, category-specific evaluators, `EvaluationReceiptCreated` event, and immutable storage.

**Legacy and Primitive Mapping:** ImageCritic, SemanticCritic, VoiceContinuityCritic, CBAR gate packs, anti-draft calibration, SDA/SFL failure corpora. Active families: FBK, SAF, VSG, VOC.

**Prerequisites:** Epics 1 through 8.

### Story 9.2: Evidence-Rich Review Surface

As a Reviewer, I want to review source quote, transcript segment, archetype route, Brand Context Version, selected assets, render output, evaluation receipt, revision history, and consent state, so that approval decisions are grounded.

**Acceptance Criteria:**

- Given an asset is in review, when the review page opens, then it shows preview, source quote, transcript segment, timestamps, route, brand context, selected assets, render output, evaluations, revisions, and consent state.
- Given a Reviewer selects an evaluation failure, when expanded, then the UI shows exact evidence and repair recommendation.
- Given revision history exists, when opened, then all prior versions and decision reasons are visible.
- Given consent state changed after render, when review opens, then the surface flags current consent compatibility.
- Given the asset is too complex for Telegram, when notification is sent, then Telegram links to this PWA review surface.

**Technical Notes:** Build PWA Render Review and Evaluation Receipt Viewer using generated contracts. Query must not cross brand boundaries.

**Legacy and Primitive Mapping:** V9.1 Evaluation Receipt doctrine, Brand Genesis review surfaces. Active families: FBK, SAF, PER.

**Prerequisites:** Story 9.1.

### Story 9.3: Review Commands and Voice-DNA Boost Requests

As a Reviewer, I want to approve, reject, request revisions, escalate for manual review, or request eligible Voice-DNA Boost through governed commands, so that every decision is auditable and reversible where allowed.

**Acceptance Criteria:**

- Given review evidence is visible, when the Reviewer approves, rejects, requests revision, escalates, or requests Voice-DNA Boost, then the action is a typed command with receipt.
- Given Voice-DNA Boost is requested, when eligibility fails, then the command is rejected with the violated rule.
- Given a revision request is saved, when the Production Steward opens the asset, then the request includes exact evidence, failure category, and expected repair.
- Given manual escalation is selected, when saved, then the asset enters `blocked` or `ready_for_review` according to state policy.
- Given approval succeeds, when event is recorded, then `ApprovalEventRecorded` includes actor, evidence, source references, and evaluation receipt IDs.

**Technical Notes:** Implement `ReviewDecision`, `RevisionRequest`, `ApprovalEvent`, `RequestVoiceDnaBoost`, and review command handlers.

**Legacy and Primitive Mapping:** Legacy receipt chain, Voice DNA doctrine, CBAR. Active families: FBK, SAF, VOC.

**Prerequisites:** Stories 2.4, 9.1, and 9.2.

### Story 9.4: Approval Blockers

As a Reviewer, I want final approval blocked when lineage, consent, source truth, identity, evaluation, platform format, or content-format requirements fail, so that no asset releases on incomplete evidence.

**Acceptance Criteria:**

- Given lineage is incomplete, when approval is attempted, then the command fails and names missing lineage.
- Given consent is incompatible, when approval is attempted, then it fails with `CONSENT_SCOPE_BLOCKED`.
- Given source truth is missing or disputed, when approval is attempted, then it fails.
- Given identity or likeness evaluation fails, when approval is attempted, then the asset must be revised or rejected.
- Given platform variant or valid format registry requirements fail, when approval is attempted, then approval is blocked.

**Technical Notes:** Approval policy checks `CompleteEditingSession`, `SceneSpec`, `ProviderReceipt`, `EvaluationReceipt`, `ConsentRecordVersion`, `ArchetypeRoute`, and `RenderOutput`.

**Legacy and Primitive Mapping:** CBAR failure scenario resolution, V9.1 approval doctrine. Active families: SAF, FBK, PER.

**Prerequisites:** Stories 9.1 through 9.3.

### Story 9.5: Publishing Intent and Publer Adapter

As a Publishing Approver, I want to create and confirm Publishing Intent only after approval, consent, lineage, platform variants, captions, and scheduling metadata are valid, so that external scheduling follows internal authority.

**Acceptance Criteria:**

- Given an asset is approved, when Publishing Intent is drafted, then it references approved asset, platform variant, captions, consent state, scheduling metadata, and approver.
- Given approval or consent is missing, when Publishing Intent is drafted or confirmed, then the command is blocked.
- Given Publishing Intent is confirmed, when submitted to Publer, then Publer job ID and request receipt are stored.
- Given Publer succeeds or fails, when webhook or polling result arrives, then `PublishingOutcome` is recorded without making Publer canonical.
- Given duplicate scheduling is attempted, when validation runs, then the command is blocked.

**Technical Notes:** Implement `PublishingIntent`, `PublerJob`, `PublishingOutcome`, `/api/v1/publishing-intents`, Publer adapter, and Publer webhook handler.

**Legacy and Primitive Mapping:** Product Brief Publer doctrine, Brand Genesis V3 adapter doctrine. Active families: SAF, BUS, FBK.

**Prerequisites:** Stories 9.1 through 9.4.

### Story 9.6: Telegram Quick Review With Evidence

As a Reviewer, I want Telegram quick approvals, rejections, or regeneration requests to show enough evidence and deep-link to PWA for complex cases, so that mobile decisions never become blind rubber-stamps.

**Acceptance Criteria:**

- Given a render is ready, when Telegram sends a notification, then it includes preview, route, source snippet, consent status, evaluation summary, and required action.
- Given evidence is sufficient for a quick decision, when the Reviewer approves or rejects, then the backend records the same command receipt as PWA.
- Given evidence is insufficient or conflicting, when the Reviewer attempts approval, then Telegram deep-links to PWA and approval is not available in-chat.
- Given the object state changes before the Reviewer acts, when the quick action is submitted, then idempotency and state transition checks prevent stale action.
- Given a quick regenerate action is submitted, when valid, then it creates a revision request rather than mutating provider output directly.

**Technical Notes:** Use Telegram Bot/Mini App as leaf surfaces; route all actions through `/api/v1/webhooks/telegram` and Command Bus.

**Legacy and Primitive Mapping:** PWA/Telegram parity doctrine, RIM feedback patterns. Active families: FBK, FRC, SAF.

**Prerequisites:** Story 1.5 and Stories 9.1 through 9.5.

---

## Epic 10: Evidence Memory, Neo4j Projection, and Recovery

**Epic Goal:** Let CMF STUDIO learn from approved evidence, expose relationship intelligence through Neo4j, and recover workflows without hidden scripts or manual database edits.

**Covers:** FR-CMF-10.01 through FR-CMF-10.07.

**User Value:** Operators can inspect memory, relationships, queues, failures, costs, blockers, and recovery actions while canonical state remains safe and rebuildable.

**Technical Context:** `/api/v1/memory`, `/api/v1/operations`, `/api/v1/projections`, `memory_admission_candidates`, `memory_events`, `projection_checkpoints`, `operational_incidents`, `recovery_actions`, Neo4j projection, domain event outbox.

**CBAR Failure Scenario:** If memory becomes lore, it will corrupt future interviews and routes. If Neo4j becomes canonical, production decisions become unrecoverable. Evidence memory and graph projection must remain governed and rebuildable.

### Story 10.1: Evidence-Backed Memory Admission

As an Operator, I want memory admissions proposed only from evidence-backed source, route, approval, publishing, or rejection events, so that the system learns without inventing brand lore.

**Acceptance Criteria:**

- Given an approved asset, route, rejection, or publishing outcome exists, when memory admission is proposed, then it includes source references, provenance, confidence, consent compatibility, originating route, and evidence.
- Given a memory candidate lacks evidence, when admission is requested, then it is rejected.
- Given consent is incompatible, when admission is proposed, then it is blocked or quarantined.
- Given a memory candidate is approved, when saved, then a `MemoryAdmissionApproved` event and memory receipt are written.
- Given a JIT compiler later uses memory, when it cites the memory, then it must reference evidence and memory event ID.

**Technical Notes:** Implement `MemoryAdmissionCandidate`, `MemoryEvent`, memory admission policy, and receipts.

**Legacy and Primitive Mapping:** Brand Memory, Interviewer Memory, Route Memory, rejected-pattern memory, RSCS reality-contact gate. Active families: FBK, SAF, PER.

**Prerequisites:** Epics 1 through 9.

### Story 10.2: Memory Review, Correction, Expiry, and Quarantine

As an Operator, I want to inspect, correct, reverse, expire, or quarantine memory admissions, so that wrong, stale, sensitive, or unsupported memory can be controlled.

**Acceptance Criteria:**

- Given memory exists, when the Memory Review surface opens, then it shows evidence, source references, route, confidence, consent compatibility, created event, and downstream usage.
- Given memory is wrong, when correction is approved, then the system writes a superseding memory event rather than mutating history.
- Given memory is stale, when expiry is approved, then future compilers cannot use it except as historical evidence.
- Given memory is sensitive, when quarantine is approved, then downstream use is blocked until resolved.
- Given memory is reversed, when future routes are compiled, then the reversal is respected.

**Technical Notes:** Memory events are append-only. Implement correction/reversal/expiry/quarantine commands and UI.

**Legacy and Primitive Mapping:** Product Brief memory doctrine and Legacy Inventory receipt chain. Active families: SAF, FBK, PER.

**Prerequisites:** Story 10.1.

### Story 10.3: Neo4j Relationship Projection

As an Operator, I want Neo4j to expose relationships among brand, guest, session, expression, archetype, asset, approval, publishing, provider, and memory entities, so that I can reason about production patterns without risking canonical state.

**Acceptance Criteria:**

- Given domain events are written, when projection runs, then Neo4j nodes and relationships are updated from canonical events.
- Given Neo4j is unavailable, when canonical workflows run, then production continues and projection lag is recorded.
- Given projection is rebuilt, when checkpoints are selected, then the graph is reconstructed from canonical events and validated against expected counts.
- Given a graph query informs an operator insight, when an action is taken, then the actual state change still goes through Command Bus and PostgreSQL canonical state.
- Given projection data conflicts with PostgreSQL, when detected, then projection is marked unhealthy and rebuild is required.

**Technical Notes:** Implement projection outbox, `ProjectionCheckpoint`, Neo4j driver integration, `/api/v1/projections`, and `ProjectionRebuildWorkflow`.

**Legacy and Primitive Mapping:** Product Brief Neo4j state retention updated by architecture boundary. Active families: BUS, FBK, SAF.

**Prerequisites:** Story 10.1 and domain events from prior epics.

### Story 10.4: Operations Board

As an Operator, I want an Operations Board showing queue depth, active workers, render tier, provider status, failures, retries, checkpoints, costs, consent blockers, approval blockers, publish readiness, and memory blockers, so that the full system is operable without hidden scripts.

**Acceptance Criteria:**

- Given jobs are running, when the Operations Board opens, then it shows queue depth, active workers, GPU tier, provider status, workflow checkpoints, retry state, costs, and blockers.
- Given a provider outage occurs, when the board refreshes, then affected jobs, completed artifacts, safe retries, costs, blockers, and recommended recovery actions are visible.
- Given consent or approval blocks work, when the board renders, then the blocker links to the exact object and required decision.
- Given a worker is draining, when no jobs remain, then shutdown status and final cost are visible.
- Given an incident is resolved, when recovery completes, then incident history and receipts remain available.

**Technical Notes:** Read from `provider_jobs`, `operational_incidents`, `recovery_actions`, workflow checkpoints, cost receipts, and projection health. No manual database edits.

**Legacy and Primitive Mapping:** Legacy operations and circuit-breaker references. Active families: FBK, BUS, FRC, SAF.

**Prerequisites:** Epics 1 through 9 and Story 10.3.

### Story 10.5: Workflow Recovery Actions

As an Operator, I want to retry, resume, cancel, compensate, or quarantine provider jobs and workflows idempotently, so that routine failures can be recovered safely.

**Acceptance Criteria:**

- Given a workflow is paused or failed, when the Operator opens recovery, then safe actions are derived from current state, completed artifacts, receipts, and consent compatibility.
- Given retry is safe, when submitted, then only incomplete work is retried.
- Given cancel is selected, when valid, then the workflow records terminal or compensated state with receipt.
- Given quarantine is required, when approved, then affected assets, memory, provider jobs, or publishing intents are blocked from future use.
- Given recovery would corrupt completed work or duplicate external action, when validation runs, then the command is blocked.

**Technical Notes:** Durable workflows own recovery semantics. Use `RecoveryAction`, `OperationalIncident`, workflow checkpoint IDs, and idempotency keys.

**Legacy and Primitive Mapping:** Receipt-chain and CBAR failure handling doctrine. Active families: SAF, FBK.

**Prerequisites:** Stories 8.7, 10.3, and 10.4.

### Story 10.6: Operational Readiness Checks

As an Owner or Operator, I want operational readiness checks for restore drills, provider outage handling, GPU worker shutdown, memory rebuild, Neo4j projection rebuild, and a complete brand cycle, so that the system proves readiness before real production pressure.

**Acceptance Criteria:**

- Given readiness checks run, when restore drill is executed, then the system verifies canonical state, object storage references, receipts, and projection rebuild ability.
- Given provider outage simulation runs, when jobs are interrupted, then recovery actions preserve completed artifacts and avoid duplicate external side effects.
- Given GPU worker shutdown check runs, when queue drains, then cost reporting and shutdown state are recorded.
- Given memory rebuild check runs, when memory events are replayed, then approved, expired, reversed, and quarantined states are preserved.
- Given full brand cycle check runs, when it completes, then it proves Brand Genesis, interview prep, expression session, package generation, editing, rendering, review, publishing intent, memory, operations, and projection health without manual database edits.

**Technical Notes:** Implement readiness commands, automated checks, fixtures, and reports under operations. These checks become release gates for production operation.

**Legacy and Primitive Mapping:** Product Brief final human acceptance, Greenfield Context release gates, Legacy Inventory spec/build protocols. Active families: SAF, BUS, FBK.

**Prerequisites:** Stories 10.1 through 10.5.

## Epic 11: Agent Factory Persona Runtime

**Epic Goal:** Create the traceable Agent Factory layer that names every agent, sub-agent, hook, extension, skill, registry, and eval with a compact persona code, binds each entity to a production responsibility, and prevents agents from becoming loose prompt personas.

**Covers:** PRD-CMF-10.00 through PRD-CMF-10.08, plus PRD-CMF-02.03 through PRD-CMF-02.05.

**User Value:** Operators and builders can tell exactly what each intelligence entity serves, which department owns it, what it can do, what it cannot do, which tools and skills it may use, and which receipt proves its work.

**Technical Context:** `docs/cmf-studio-agent-factory-registry.md`, `docs/cmf-studio-agent-intelligence-contract.md`, `src/ccp_studio/contracts/agent_gateway.py`, `src/ccp_studio/contracts/orchestration.py`, `src/ccp_studio/contracts/skills.py`, future `AgentFactorySpec`, `DepartmentSpec`, `AgentRoleSpec`, `SubAgentRoleSpec`, `HookSpec`, `ExtensionSpec`, `SkillBinding`, `ToolCapabilitySpec`, `AgentReadinessEval`, generated ADK/Agents CLI adapters.

**CBAR Failure Scenario:** If agents are named poetically but not operationally, the Factory becomes impossible to audit. If agents gain tools, memory, or skills without bounded contracts, they can bypass the pipeline. The resolution is a strict `DDD-XXXXXXX-TT` persona code, contract registry, readiness eval, and generated adapter boundary.

### Story 11.1: Persona Code Registry and Validation

As an Operator-builder, I want every Factory entity to use a compact persona code, so that logs, receipts, UI filters, specs, and agent configs reveal exactly what the entity serves.

**Acceptance Criteria:**

- Given an agent, sub-agent, hook, extension, skill, registry, or eval is registered, when its code is validated, then it must match `DDD-XXXXXXX-TT`.
- Given the middle segment is not exactly seven characters, when registration runs, then the entity is rejected.
- Given the type segment is not a known two-character entity type, when registration runs, then the entity is rejected.
- Given a code uses only a poetic persona name and not a service role, when review runs, then the reviewer must request a service-revealing code.
- Given `RES-VISRSCH-AG` is registered, when the registry renders it, then it resolves to Visual Research Agent / Aurore and its service scope.

**Technical Notes:** Implement persona code schema, department code enum, entity type enum, uniqueness check, and registry validation.

**Legacy and Primitive Mapping:** Preserves intentional orchestration traceability from old CCF/CMF modules. Active families: SAF, BUS, FBK.

**Prerequisites:** Stories 1.1, 1.6, 3.6.

### Story 11.2: Agent Role Spec Catalog

As a Builder, I want each Agent to have an `AgentRoleSpec`, so that the system knows its goal, responsibility, active objects, tools, memory, skills, evals, blocked actions, and receipts.

**Acceptance Criteria:**

- Given an Agent is added to the Factory, when saved, then it must include persona code, display name, department, goal, fit rationale, entry objects, exit objects, allowed tools, skills, sub-agent bindings, hooks, evals, memory policy, blocked actions, and receipt obligations.
- Given an AgentRoleSpec is activated, when runtime invocation is requested, then it must resolve through `OrchestrationRun`, `StageExecutionPlan`, `ValidationContract`, `AgentActionRequest`, and `PiAgentGateway`.
- Given an Agent implementation is a DSPy program, deterministic service, ADK adapter, workflow activity, provider worker, or human queue, when it runs, then it must still bind to the same `AgentRoleSpec` and receipt obligations.
- Given an Agent lacks active object scope, when activation is requested, then activation is blocked.
- Given an Agent has tool access without a permission and receipt obligation, when readiness eval runs, then it fails.
- Given an Agent tries to write canonical state outside the Command Bus or approved workflow command, when gateway or static guard runs, then the action is blocked.
- Given an Agent owns a pipeline stage, when inspected, then the UI and docs show the stage, entry object, exit object, validation contract, and required receipt.
- Given `ORC-PIORCHS-AG` is active, when it proposes work, then it acts only through the Agent Gateway and Command Bus.

**Technical Notes:** Add `AgentRoleSpec`, `DepartmentSpec`, activation state, readiness eval link, generated adapter hash, repository/service methods, validation gates, runtime invocation checks, and seed records from the persona registry.

**Legacy and Primitive Mapping:** Applies BMAD/ERA3 discipline to runtime agents instead of document-only personas. Active families: SAF, BUS.

**Prerequisites:** Story 11.1.

### Story 11.3: Sub-Agent Delegation and Bounded Authority

As an Agent owner, I want sub-agents to have bounded specialist contracts, so that narrow expertise can help without expanding authority beyond the parent stage.

**Acceptance Criteria:**

- Given a Sub-Agent is bound to an Agent, when saved, then it must include parent agent, invocation conditions, input contract, output contract, blocked actions, proof obligation, and receipt.
- Given a SubAgentRoleSpec is invoked, when execution starts, then it must cite parent `AgentRoleSpec`, parent orchestration run, parent stage plan, bounded input model, and expected output model.
- Given a Sub-Agent tries to mutate canonical state directly, when the gateway checks authority, then the action is blocked.
- Given a Sub-Agent needs a tool, when validation runs, then the tool must be listed in the sub-agent spec and compatible with the parent stage validation contract.
- Given a Sub-Agent output is used downstream, when the handoff packet is created, then it includes source evidence, parent stage, and sub-agent receipt.
- Given a Sub-Agent result should change production state, when the result is accepted, then the parent Agent must route it through the normal command, workflow, review, or evaluation path.
- Given `RES-EVDCRIT-SA` critiques evidence, when its output is consumed by `RES-CTXPRMS-AG`, then the Context Premise receipt cites the critique.
- Given `SCN-CMPDIRC-SA` analyzes an Ideogram plate, when render proceeds, then its output cannot override final text or identity authority.

**Technical Notes:** Add `SubAgentRoleSpec`, parent compatibility checks, bounded input/output models, sub-agent tool subset validation, sub-agent receipts, and handoff packet integration.

**Legacy and Primitive Mapping:** Protects specialized legacy lenses such as evidence critic, anti-centroid critic, visual candidate scorer, and composition inspector from becoming uncontrolled agents. Active families: SAF, FBK, VSG.

**Prerequisites:** Stories 1.6, 11.1, 11.2.

### Story 11.4: Hook and Extension Lifecycle Contracts

As an Architect, I want hooks and extensions to be explicitly registered, so that lifecycle checks and integrations enforce the pipeline without becoming hidden authority.

**Acceptance Criteria:**

- Given a Hook is registered, when activated, then it must declare lifecycle boundary, trigger condition, allowed checks, blocked mutations, emitted receipt, and failure behavior.
- Given an Extension is registered, when mounted, then it must declare tools, credentials boundary, provider or integration scope, canonical-state restrictions, and receipts.
- Given a Hook attempts creative reasoning instead of deterministic enforcement, when review runs, then activation is blocked.
- Given Publer is used, when `PUB-PUBLERX-EX` runs, then it schedules or reports status without owning approval, caption truth, or asset lineage.
- Given `REV-APPGATE-HK` fires, when an approval blocker exists, then publication cannot continue.

**Technical Notes:** Add `HookSpec`, `ExtensionSpec`, lifecycle enums, gateway mounting rules, and no-canonical-authority checks.

**Legacy and Primitive Mapping:** Preserves callback-like ideas from agent frameworks while enforcing CMF consent, review, provider, and memory gates. Active families: SAF, FRC, FBK.

**Prerequisites:** Stories 1.1, 2.3, 8.1, 9.4.

### Story 11.5: Skill Bindings and JIT Compiler Modes

As a Factory operator, I want stable skills and JIT skills bound differently, so that daily operational procedures and context-compiled intelligence are both governed correctly.

**Acceptance Criteria:**

- Given a stable operational skill is bound to an Agent, when used, then it references a versioned skill manifest and allowed procedure.
- Given a JIT skill compiler is bound to an Agent, when invoked, then it requires saturation context, registry snapshot, compiler fingerprint, contrastive prompt layer, critic result, synthesis result, and `SkillInvocationRecord`.
- Given a skill is needed for interview engineering, when compiled, then it supports Interview Briefs, induction moves, contrast questions, extraction lenses, route support, or eval support.
- Given a skill only contains generic few-shot examples, when activation is requested, then the activation is blocked.
- Given `EXT-JITCOMP-AG` emits extraction candidates, when routing consumes them, then source context and eval state remain attached.

**Technical Notes:** Extend skill binding contracts to distinguish stable `SK` and JIT `JS` entities, allowed use modes, invocation receipts, and readiness evals.

**Legacy and Primitive Mapping:** Adapts old JIT skill modules from scripts/visual prompts into interview brief, induction, extraction, and evaluation compilers. Active families: STR, PSY, TRG, VSG, VOC, FBK.

**Prerequisites:** Stories 3.3, 5.5, 6.3, 11.2.

### Story 11.6: Intelligence Contract and Agent Readiness Evals

As an Owner, I want every intelligence entity evaluated before activation, so that standards, primitives, rules, tools, memory, skills, and receipts govern its behavior.

**Acceptance Criteria:**

- Given an AgentRoleSpec is submitted, when readiness eval runs, then it checks constitutions, standards, primitives, deterministic rules, protocols, tools, memory access, skills, evals, receipts, and blocked actions.
- Given an Agent lacks primitive obligations for a quality-critical task, when readiness eval runs, then activation is blocked or revision-required.
- Given memory access is broader than the active object allows, when readiness eval runs, then activation is blocked.
- Given eval obligations are missing, when an Agent handles review, routing, extraction, or rendering, then readiness eval fails.
- Given readiness passes, when the Agent activates, then the versioned readiness receipt is linked to its role spec.

**Technical Notes:** Add `AgentReadinessEval`, readiness receipts, primitive obligation checks, memory policy checks, and review UI.

**Legacy and Primitive Mapping:** Makes primitives the production quality standard for agent behavior, not just output scoring. Active families: SAF, FBK, PER, BUS.

**Prerequisites:** Stories 3.2, 9.1, 10.1, 11.2.

### Story 11.7: Pi Harness Tool Registry and Department Runtime

As Pi Orchestrator, I need explicit tools registered per department, so that I can coordinate the Factory without relying on built-in or hidden capabilities.

**Acceptance Criteria:**

- Given a tool is registered, when Pi requests it, then the tool must expose Pydantic input/output, department scope, allowed stages, role policy, idempotency rule, receipt obligation, and failure behavior.
- Given Pi requests a tool outside the active stage or role, when the Agent Gateway evaluates the request, then it is blocked.
- Given a department has no registered tool for a required action, when Pi reaches that stage, then it creates a human handoff or blocker rather than inventing a tool.
- Given a tool mutates state, when executed, then the mutation goes through the Command Bus and writes a receipt.
- Given a provider or renderer tool is called, when it returns, then provider metadata, cost, retry state, and output hashes are preserved.

**Technical Notes:** Add `ToolCapabilitySpec`, department runtime registry, tool gateway checks, and Pi action validation.

**Legacy and Primitive Mapping:** Implements the correction that Pi has no built-in CMF production tools; every capability must be built, scoped, and receipt-backed. Active families: SAF, BUS, FRC.

**Prerequisites:** Stories 1.1, 1.6, 8.1, 11.2.

### Story 11.8: ADK and Agents CLI Adapter Export Drift Gate

As an Architect, I want Google ADK and Agents CLI adapters generated from CMF contracts, so that external agent runtimes help deployment without becoming the source of truth.

**Acceptance Criteria:**

- Given an AgentRoleSpec is approved, when ADK export runs, then the generated adapter includes name, description, tools, sub-agents, callbacks, and handoff hints derived from CMF contracts.
- Given a generated adapter is edited by hand, when drift check runs, then the adapter is marked non-canonical and export must be regenerated.
- Given an ADK callback maps to a CMF Hook, when exported, then the hook remains governed by CMF lifecycle and receipt rules.
- Given an ADK tool maps to a CMF ToolCapabilitySpec, when exported, then it cannot bypass Pydantic input/output or Command Bus mutation rules.
- Given Agents CLI deployment scaffolding is generated, when reviewed, then it cites the originating CMF role spec and readiness receipt.

**Technical Notes:** Add adapter export records, generated file hashes, drift checks, ADK/Agents CLI metadata, and read-only generated adapter folders.

**Legacy and Primitive Mapping:** Learns from Google agent config discipline without replacing BMAD, Pydantic contracts, Pi harness rules, or CMF receipt authority. Active families: SAF, BUS.

**Prerequisites:** Stories 11.1 through 11.7.

---

## 5. FR Coverage Matrix

| FR ID(s) | Covered By |
|---|---|
| FR-CMF-01.01 | Story 1.2 |
| FR-CMF-01.02 | Story 1.3 |
| FR-CMF-01.03 | Stories 1.1, 1.2, 1.5 |
| FR-CMF-01.04 | Story 1.4 |
| FR-CMF-01.05 | Story 1.4 |
| FR-CMF-01.06 | Stories 1.1, 1.6 |
| FR-CMF-01.07 | Story 1.5 |
| FR-CMF-02.01 | Story 2.1 |
| FR-CMF-02.02 | Story 2.2 |
| FR-CMF-02.03 | Story 2.3 |
| FR-CMF-02.04 | Stories 2.2, 2.5 |
| FR-CMF-02.05 | Story 2.4 |
| FR-CMF-02.06 | Story 2.4 |
| FR-CMF-02.07 | Story 2.5 |
| FR-CMF-03.01 | Story 3.1 |
| FR-CMF-03.02 | Story 3.2 |
| FR-CMF-03.03 | Story 3.2 |
| FR-CMF-03.04 | Story 3.3 |
| FR-CMF-03.05 | Story 3.3 |
| FR-CMF-03.06 | Story 3.4 |
| FR-CMF-03.07 | Stories 1.6, 3.5 |
| FR-CMF-03.08 | Stories 3.1, 3.2 |
| FR-CMF-03.09 | Story 3.6 |
| FR-CMF-04.01 | Story 4.1 |
| FR-CMF-04.02 | Story 4.2 |
| FR-CMF-04.03 | Story 4.3 |
| FR-CMF-04.04 | Story 4.3 |
| FR-CMF-04.05 | Stories 4.2, 4.3 |
| FR-CMF-04.06 | Story 4.4 |
| FR-CMF-04.07 | Stories 4.4, 4.5 |
| FR-CMF-05.01 | Story 5.1 |
| FR-CMF-05.02 | Story 5.2 |
| FR-CMF-05.03 | Story 5.3 |
| FR-CMF-05.04 | Story 5.4 |
| FR-CMF-05.05 | Story 5.5 |
| FR-CMF-05.06 | Story 5.5 |
| FR-CMF-05.07 | Stories 5.3, 5.5 |
| FR-CMF-05.08 | Story 5.6 |
| FR-CMF-06.01 | Story 6.1 |
| FR-CMF-06.02 | Story 6.2 |
| FR-CMF-06.03 | Story 6.3 |
| FR-CMF-06.04 | Story 6.4 |
| FR-CMF-06.05 | Story 6.5 |
| FR-CMF-06.06 | Story 6.6 |
| FR-CMF-06.07 | Story 6.5 |
| FR-CMF-06.08 | Story 6.7 |
| FR-CMF-07.01 | Story 7.1 |
| FR-CMF-07.02 | Story 7.2 |
| FR-CMF-07.03 | Story 7.3 |
| FR-CMF-07.04 | Story 7.3 |
| FR-CMF-07.05 | Story 7.4 |
| FR-CMF-07.06 | Story 7.4 |
| FR-CMF-07.07 | Story 7.5 |
| FR-CMF-07.08 | Story 7.5 |
| FR-CMF-07.09 | Story 7.6 |
| FR-CMF-08.01 | Story 8.1 |
| FR-CMF-08.02 | Story 8.2 |
| FR-CMF-08.03 | Story 8.3 |
| FR-CMF-08.04 | Story 8.4 |
| FR-CMF-08.05 | Story 8.5 |
| FR-CMF-08.06 | Story 8.6 |
| FR-CMF-08.07 | Story 8.7 |
| FR-CMF-08.08 | Story 8.8 |
| FR-CMF-09.01 | Story 9.1 |
| FR-CMF-09.02 | Story 9.2 |
| FR-CMF-09.03 | Story 9.3 |
| FR-CMF-09.04 | Story 9.4 |
| FR-CMF-09.05 | Story 9.5 |
| FR-CMF-09.06 | Story 9.5 |
| FR-CMF-09.07 | Story 9.6 |
| FR-CMF-10.01 | Story 10.1 |
| FR-CMF-10.02 | Story 10.2 |
| FR-CMF-10.03 | Story 10.3 |
| FR-CMF-10.04 | Story 10.3 |
| FR-CMF-10.05 | Story 10.4 |
| FR-CMF-10.06 | Stories 1.6, 10.5 |
| FR-CMF-10.07 | Story 10.6 |

### 5.1 PRD Module Requirement Coverage Matrix

| Module Requirement | Covered By |
|---|---|
| PRD-CMF-10.00 Persona Code Standard | Story 11.1 |
| PRD-CMF-10.01 Agent Definition | Story 11.2 |
| PRD-CMF-10.02 Sub-Agent Definition | Story 11.3 |
| PRD-CMF-10.03 Hooks | Story 11.4 |
| PRD-CMF-10.04 Extensions | Story 11.4 |
| PRD-CMF-10.05 Skills and JIT Skills | Story 11.5 |
| PRD-CMF-10.06 Intelligence Contract | Story 11.6 |
| PRD-CMF-10.07 Google Agents CLI and BMAD Compatibility | Story 11.8 |
| PRD-CMF-10.08 Harness and Department Runtime | Story 11.7 |
| PRD-CMF-02.03 Agent Team Topology | Stories 11.2, 11.3 |
| PRD-CMF-02.04 Pi Harness Rules | Stories 11.7, 11.8 |
| PRD-CMF-02.05 Agent Handoff Packets | Stories 11.2, 11.3, 11.7 |

---

## 6. Architecture Integration Validation

| Architecture Decision or Pattern | Story Coverage |
|---|---|
| Python-first Harness | Stories 1.1, 3.4, 3.5 |
| TypeScript as leaf runtime | Stories 1.5, 8.2, 9.6 |
| Pydantic as contract authority | Stories 1.1, 3.5, all command-driven stories |
| DSPy owns structured reasoning, not state | Stories 3.3, 5.2, 5.3, 5.5, 5.6, 6.3 |
| Pi orchestrates through commands | Stories 1.1, 1.6, 3.5, workflow stories across epics |
| AD-014 canonical pipeline stages govern agent autonomy | Story 1.6 and Story-to-Pipeline Trace Matrix |
| OrchestrationRun, StageExecutionPlan, ValidationContract, AgentHandoffPacket, SkillInvocationRecord, FailureReceipt, FrictionReceipt, HumanHandoffRequest | Story 1.6 |
| TechSpecCompilerWorkflow, FilesReadReceipt, RequirementTrace, PipelineStageTrace, SpecAuditReceipt | Story 3.5 |
| Command Bus as mutation boundary | Stories 1.1, 1.5, 2.3, 9.3, 10.5 |
| PostgreSQL canonical state | Stories 1.1, 10.3 |
| Neo4j rebuildable projection | Story 10.3 |
| Durable workflows | Stories 4.1, 5.5, 6.1, 7.1, 8.7, 10.5 |
| Provider capability registry | Stories 8.1, 8.3, 8.4 |
| SVRE/Aurore visual research contracts | Story 8.8 |
| Ideogram 4 `CompositionJob` lineage | Story 7.3 |
| CMF scene containers, components, subsystems, and asset rolls | Story 7.6 |
| CRAL, Context Premise, Emotional DNA, and Voice DNA induction rationale | Story 5.6 |
| Legacy read-only intelligence and orchestration intent | Stories 3.1 through 3.6 |
| Human review as product architecture | Stories 2.5, 6.4, 9.1 through 9.6 |
| Agent persona code standard | Story 11.1 |
| AgentRoleSpec, SubAgentRoleSpec, HookSpec, ExtensionSpec, SkillBinding, ToolCapabilitySpec | Stories 11.2 through 11.7 |
| ADK/Agents CLI generated adapters, not source of truth | Story 11.8 |

---

## 7. Story Quality Validation

- All 10 FR-CMF modules are represented by value-oriented epics.
- All 77 PRD sub-requirements are mapped to at least one story.
- All stories are mapped to canonical PRD pipeline stages, entry objects, exit objects, validation contracts, and required receipts.
- AD-014 orchestration objects are covered by Story 1.6.
- Each story includes a user story, BDD-style acceptance criteria, technical notes, legacy/primitive mapping, and prerequisites.
- Stories preserve the dependency chain without presenting scope as deferrable buckets.
- Acceptance criteria include critical failure examples for consent, brand scope, source truth, unsupported formats, provider receipts, projection lag, approval blockers, and recovery.
- JIT Skill compilers are modeled as saturation, drafting, contrast, calibration, and evaluation engines rather than generic prompts.
- Legacy CCF/CMF modules are modeled as intentional orchestration records rather than isolated prompts, vibes, or feature labels.
- CRAL/SCRE, Context Premise, Emotional DNA, Voice DNA, SVRE/Aurore, CMF scene intelligence, and legacy asset engines have explicit story coverage.
- Scene reproducibility preserves both legacy CMF lineage expectations and Ideogram 4 `CompositionJob` JSON.
- Neo4j is included now as a rebuildable relationship projection, not canonical state.
- Provider names and execution routes match CMF architecture: GPT Image 2, Flux 2 Klein 9b, Ideogram 4, Qwen-Image-Layered, SAM3, LavaSR, MOSS-TTS, Remotion, Motion Canvas, and self-hosted ComfyUI Docker GPU worker.
- Tech-spec generation is now explicitly governed by `TechSpecCompilerWorkflow`, `FilesReadReceipt`, `RequirementTrace`, `PipelineStageTrace`, CBAR checks, and `SpecAuditReceipt`.
- Agent Factory runtime requirements are now explicitly governed by persona codes, role specs, sub-agent specs, hooks, extensions, skills, readiness evals, tool capability specs, and generated adapter drift gates.

---

## 8. Handoff to Story Files and Tech Specs

The next BMad pass should use the SM `create-story` workflow to generate individual implementation story files from this artifact. Each story file must inherit:

1. The FR IDs listed in the coverage matrix.
2. The canonical pipeline stage listed in the story-to-pipeline trace matrix.
3. The entry object, exit object, validation contract, and required receipt listed in the trace matrix.
4. The architecture components listed in the story technical notes.
5. The legacy and primitive mappings listed in each story.
6. The failure examples and blockers listed in the acceptance criteria.
7. The AD-014 rule that Pi and specialist agents operate through `OrchestrationRun`, `StageExecutionPlan`, `ValidationContract`, `AgentHandoffPacket`, `SkillInvocationRecord`, and receipts where autonomous coordination is involved.
8. The tech-spec rule that "Existing Backend Integration" becomes "Greenfield Integration and Legacy Migration Context."

Tech specs should be generated only after these stories are expanded into dev-ready implementation story files. Each tech spec must then run through `TechSpecCompilerWorkflow` with `FilesReadReceipt`, `RequirementTrace`, `PipelineStageTrace`, CBAR checks, testing strategy, observability/recovery notes, and `SpecAuditReceipt`.

