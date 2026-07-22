---
type: prd-module
project: CMF STUDIO
module_id: PRD-CMF-02
status: canonical
source_prd: 05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
source_sections:
  - Canonical Product Pipeline and Agent Orchestration Map
last_updated: 2026-06-22
---

# PRD-CMF-02 - Pipeline and Agent Orchestration

## Module Purpose

This module turns the CMF STUDIO pipeline into the operating map used by agents, services, stories, specs, evals, and UI surfaces. Agents may operate autonomously only inside a shared production chain. The chain defines active object, allowed role, required validation, emitted receipt, blocked actions, and human gate.

## Canonical Pipeline

`Legacy Inventory and Migration`
-> `Workspace, Commercial Scope, Consent, and Source Intake`
-> `Brand Genesis`
-> `Research and Context Engineering`
-> `Interview Intelligence and Narrative State Induction`
-> `Complete Expression Session`
-> `Post-Session Extraction`
-> `Archetype and Asset Routing`
-> `Asset Package Spec`
-> `Complete Editing Session`
-> `Scene Planning and Composition Control`
-> `Asset Research and Provider Jobs`
-> `Rendering and Assembly`
-> `Evaluation, Review, Revision, and Approval`
-> `Publishing Intent and Publer Scheduling`
-> `Memory Admission and Neo4j Projection`

## Product Requirements

### PR-CMF-02.01 Stage-Gated Production

Every production stage must declare:

- entry objects;
- exit objects;
- primary agent, sub-agent, deterministic service, or workflow;
- required validation contract;
- required receipt;
- downstream proof obligation;
- blocked actions.

No agent or workflow may reorder consent, source truth, Brand Context locking, extraction, routing, evaluation, approval, publishing, memory admission, or projection boundaries.

### PR-CMF-02.02 Object Spine

Architecture, epics, stories, specs, runtime code, and UI state must preserve this object spine:

`MigrationLedgerEntry`
-> `LegacyOrchestrationIntentRecord`
-> `BrandWorkspace`
-> `ConsentRecord`
-> `SourceArtifactManifest`
-> `BrandContextVersion`
-> `ResearchSnapshot`
-> `ContextPremise`
-> `EmotionalDNAProfile` / `VoiceDNAProfile`
-> `MatrixBrief`
-> `InterviewAssetContract`
-> `CompleteExpressionSession`
-> `ExpressionMoment`
-> `AssetRouteReceipt`
-> `AssetPackageSpec`
-> `CompleteEditingSession`
-> `SceneSpec`
-> `CompositionJob`
-> `AssetResearchManifest`
-> `ProviderJobReceipt`
-> `RenderOutput`
-> `EvaluationReceipt`
-> `ApprovalEvent`
-> `PublishingIntent`
-> `MemoryAdmission`
-> `Neo4jProjectionEvent`

### PR-CMF-02.03 Agent Team Topology

The agent team is organized around product responsibility, not model personality. Pi orchestrates through the Python Agent Gateway. DSPy programs perform typed reasoning and calibrated evaluations. Deterministic services perform commands, workflows, storage, rendering, and projection. Provider adapters perform external work through capability contracts only.

Core departments:

- Orchestration Department: Pi Orchestrator, Validation Contract Agent, Handoff Agent.
- Migration Department: Migration Steward, Legacy Orchestration Intent Analyst, Spec Governance Agent.
- Brand Department: Brand Genesis Agent, Acting Library Agent, Paper-Cut Rig Agent, Micro-Semiotic Agent, Voice/Emotional DNA Agent.
- Research Department: CRAL/SCRE Research Agent, Context Premise Agent, Audience Reality Agent, Evidence Critic.
- Induction Department: Matrix of Edging Agent, Narrative State Induction Agent, Interview Asset Contract Agent.
- Session Department: Live Interview Assistant, Consent Monitor, Recording Steward, Session Quality Agent.
- Extraction and Routing Department: JIT Skill Compiler modules, Expression Moment Agent, Archetype Router, Asset Derivative Router.
- Production Department: Complete Editing Session Agent, SceneSpec Compiler, Composition Director Adapter, SVRE/Aurore Agent, Renderer Router.
- Evaluation Department: SemanticCritic, ImageCritic, VoiceContinuityCritic, CBAR Auditor, Human Review Coordinator.
- Memory and Operations Department: Memory Admission Agent, Projection Builder, Operations Board Agent, Recovery Agent.

### PR-CMF-02.04 Pi Harness Rules

Pi orchestrates the pipeline; it does not replace the pipeline. For each stage, Pi must:

- read the active production object;
- identify the next valid transition;
- select the allowed role contract, JIT skill, DSPy program, provider adapter, deterministic service, or durable workflow;
- write a pre-execution `ValidationContract`;
- propose a typed `AgentCommand`;
- wait for an honest receipt before continuing.

Pi cannot directly mutate production tables, bypass consent, approve its own output, publish publicly, change locked Brand Context Versions, skip evaluation, or treat Neo4j as canonical state.

### PR-CMF-02.05 Agent Handoff Packets

Every handoff between agents must carry an `AgentHandoffPacket` with active object, source evidence, upstream receipts, required downstream object, allowed actions, blocked actions, validation contract, and proof obligations.

## Acceptance Gates

- A stage cannot execute without a validation contract.
- A downstream stage cannot start until the previous stage emits an accepted receipt or explicit human handoff.
- Human approval is mandatory before public publishing.
- Agent output must be inspectable from active object to final receipt.
