---
type: prd-module
project: CMF STUDIO
module_id: PRD-CMF-10
status: canonical
source_prd: 05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
source_sections:
  - Canonical Product Pipeline and Agent Orchestration Map
  - Functional Requirement Governance Rules
related_docs:
  - docs/cmf-studio-agent-factory-architecture.md
  - docs/cmf-studio-agent-factory-registry.md
  - docs/cmf-studio-agent-intelligence-contract.md
  - docs/cmf-studio-intelligence-operating-model.md
last_updated: 2026-06-22
---

# PRD-CMF-10 - Agent Factory Runtime

## Module Purpose

This module defines how CMF STUDIO thinks about agents, sub-agents, hooks, extensions, skills, tools, teams, and runtime orchestration. The factory metaphor is intentional: the primitives and pipeline define departments, departments define responsibilities, responsibilities define agent architecture, and agent architecture defines which intelligence, tools, memory, standards, and receipts each entity can use.

## Product Requirements

### PR-CMF-10.00 Persona Code Standard

Every agent, sub-agent, hook, extension, skill, registry, and eval must be represented by a stable persona code in the form `DDD-XXXXXXX-TT`. The department code is three characters, the service code is exactly seven characters, and the type code is exactly two characters.

The code must reveal the entity's production service. Example: `RES-VISRSCH-AG` represents the Visual Research Agent. Display persona names may be expressive, but operational identity must remain short, traceable, and stable across registries, UI, receipts, stories, specs, and generated adapter configs.

### PR-CMF-10.01 Agent Definition

An Agent is an accountable runtime actor with a production goal, bounded authority, active object scope, allowed tools, memory access, standards, protocols, evaluation obligations, and receipt outputs. Agents are not just prompts. They carry responsibility and must be fit for the pipeline stage they serve.

Technically, an Agent is represented by an `AgentRoleSpec` stored in the Agent Factory registry. The spec is the canonical product/runtime contract; the model prompt, DSPy program, ADK adapter, workflow activity, or deterministic service is only an implementation of that contract.

An `AgentRoleSpec` must include:

- `entity_code` using `DDD-XXXXXXX-TT`;
- `department_key`, `service_code`, `display_name`, and optional `persona_name`;
- production goal and fit rationale;
- owned pipeline stage or overlay;
- active object types it may read or act on;
- entry object contracts and exit object contracts;
- allowed `ToolCapabilitySpec` references;
- allowed stable skills and JIT skill modes;
- sub-agent bindings it may invoke;
- hook bindings that fire before or after its work;
- memory access policy and permitted memory scopes;
- eval bindings, readiness eval, and activation status;
- blocked actions;
- required receipts and handoff packet obligations;
- adapter export metadata and generated adapter hash when applicable.

Agent invocation must flow through the CMF runtime spine:

`OrchestrationRun` -> `StageExecutionPlan` -> `ValidationContract` -> `AgentActionRequest` -> `PiAgentGateway` -> allowed tool, workflow, DSPy program, deterministic service, provider adapter, or human review queue -> typed output -> receipt -> `AgentHandoffPacket`.

Agents cannot directly mutate canonical state. Mutations must go through the Command Bus or an approved durable workflow command. Read access must go through scoped repositories, read models, registry snapshots, or explicit context bundles. Memory access is never global; it is granted by memory policy and source evidence. Every output that can influence production must be typed, evidence-linked, receipt-backed, and eligible for evaluation.

An Agent may compile to multiple technical shapes:

- a Python role class behind the Agent Gateway;
- a DSPy program or evaluator;
- a durable workflow activity;
- a deterministic domain service;
- an ADK `LlmAgent` adapter generated from the spec;
- a provider/renderer worker adapter;
- a human review queue with the same receipt obligations.

The spec remains canonical across all implementations.

### PR-CMF-10.02 Sub-Agent Definition

A Sub-Agent is a specialized actor invoked by an Agent for a narrower responsibility, such as Context Premise synthesis, Matrix of Edging scoring, transcription alignment, visual candidate scoring, Voice DNA eligibility, or composition analysis. Sub-agents cannot expand their own authority beyond the parent stage contract.

Technically, a Sub-Agent is represented by a `SubAgentRoleSpec` bound to one or more parent `AgentRoleSpec` records. It does not own the whole stage. It performs a bounded analysis, critique, score, synthesis, search, inspection, or validation task for the parent agent.

A `SubAgentRoleSpec` must include:

- `entity_code` using `DDD-XXXXXXX-TT`;
- parent agent bindings and allowed invocation conditions;
- narrow input model and output model;
- allowed context bundle fields;
- allowed tools, normally a strict subset of the parent tools;
- default mutation policy, which should be read-only unless an explicit parent-delegated tool is approved;
- required evidence references;
- blocked actions;
- output confidence, critique, score, or synthesis schema;
- receipt type linked to parent orchestration run and stage plan;
- handoff behavior back to the parent agent.

Sub-agent invocation must be traceable:

`Parent AgentRoleSpec` -> `AgentHandoffPacket` or internal delegation request -> `SubAgentRoleSpec` -> bounded task execution -> typed sub-agent output -> sub-agent receipt -> parent agent synthesis or blocker.

Sub-agents cannot publish, approve, mutate locked Brand Context Versions, bypass consent, call provider adapters independently, change memory, or promote their own output to canonical truth. If a sub-agent result should affect state, the parent agent must route that result through the normal validation, command, workflow, review, and receipt chain.

### PR-CMF-10.03 Hooks

Hooks are event-bound enforcement or enrichment mechanisms. They run before or after commands, stage transitions, provider calls, evaluations, approvals, memory admissions, or publishing actions. Hooks are used for consent, brand-scope checks, registry validation, evaluation blockers, migration gates, observability, and recovery.

### PR-CMF-10.04 Extensions

Extensions are bounded integrations or optional runtime capabilities behind contracts. Examples include Publer, Telegram, Remotion, Motion Canvas, ComfyUI worker, provider adapters, search/research connectors, and graph projection. Extensions cannot own canonical domain truth.

### PR-CMF-10.05 Skills and JIT Skills

Skills are reusable capability modules available to agents. Some are stable operational skills. JIT Skills are context-compiled modules, especially for interview briefs, narrative induction, expression extraction, contrastive prompt layers, route reasoning, creative writing, visual prompts, and evaluation lenses.

JIT Skills are part of intelligence execution. They must produce invocation records, not invisible prompt text.

### PR-CMF-10.06 Intelligence Contract

Each agent, sub-agent, hook, extension, and skill must state:

- goal;
- responsibility;
- active object;
- allowed inputs;
- allowed outputs;
- standards and primitives used;
- memory access;
- tool access;
- blocked actions;
- evaluation obligations;
- receipt type;
- human handoff condition.

### PR-CMF-10.07 Google Agents CLI and BMAD Compatibility

Google-style agent descriptions can help specify agent identity, goals, tools, instructions, and handoffs. BMAD remains the workflow shell for disciplined PRD, story, architecture, and tech-spec generation. CMF STUDIO should embrace the clarity of agent specifications while preserving BMAD/ERA3 governance, files-read discipline, approval menus where required, and traceable artifacts.

BMAD agents are not enough by themselves for runtime intelligence. They are closer to workflow personas and procedural shells. CMF runtime agents need contracts, tools, memory, gates, receipts, and production responsibilities.

### PR-CMF-10.08 Harness and Department Runtime

The Pi Coding Harness orchestrates departments through the Agent Gateway and Command Bus. It must not depend on built-in magic tools. Tools, adapters, registries, and allowed commands must be explicitly built, registered, validated, and tested.

## Factory Departments

- Strategy and Governance.
- Migration and Registry.
- Brand Genesis.
- Research and Context.
- Interview and Induction.
- Session and Extraction.
- Routing and Packaging.
- Scene and Production.
- Assets and Providers.
- Evaluation and Review.
- Publishing and Memory.
- Operations and Recovery.

## Acceptance Gates

- No agent can execute without a declared active object and validation contract.
- No sub-agent can bypass parent stage authority.
- No hook can mutate canonical state without command authorization.
- No extension can become canonical truth.
- No skill or JIT compiler can influence production without invocation record and eval path.
