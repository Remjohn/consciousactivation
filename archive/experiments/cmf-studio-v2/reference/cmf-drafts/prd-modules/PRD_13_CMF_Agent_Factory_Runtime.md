---
type: modular-prd
module: PRD-13
title: CMF Agent Factory Runtime - Departments, Agents, Sub-Agents, Hooks, Skills, and Tools
author: John (Product Manager)
date: 2026-06-22
status: Draft Source of Truth
version: 1.0
dependencies:
  - docs/prd/modules/PRD_INDEX.md
  - docs/prd/modules/PRD_10_CMF_Interview_Intelligence.md
  - docs/prd/modules/PRD_11_CMF_JIT_Interview_Brief_Compiler.md
  - docs/prd/modules/PRD_12_CMF_Primitive_Eval_Review_Workbench.md
  - docs/cmf-studio-agent-factory-architecture.md
  - docs/cmf-studio-intelligence-operating-model.md
source_documents:
  - THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md
  - docs/cmf-studio-agent-factory-architecture.md
  - docs/cmf-studio-intelligence-operating-model.md
  - docs/cmf-studio-agent-intelligence-contract.md
  - docs/cmf-studio-skill-system-contract.md
  - docs/cmf-studio-agent-factory-registry.md
active_primitives:
  meaning_plane: [STR, PRS, CON, PSY, VOC, VSG, ACT, BUS]
  experience_plane: [TRG, FRC, FBK, SAF, PER]
capability_areas: [CMF-AGENTS, CMF-FACTORY, CMF-PI-HARNESS]
---

# PRD-13: CMF Agent Factory Runtime - Departments, Agents, Sub-Agents, Hooks, Skills, and Tools

**Version:** 1.0 | **Status:** Draft Source of Truth | **Date:** 2026-06-22

## 1. Purpose and Architectural Claim

CMF agents should be derived from the Factory. The Factory is the department-based production organization that owns pipeline stages, objects, proof obligations, tools, skills, hooks, evals, and receipts.

An agent is not a prompt personality. It is a named accountable role contract with a goal, fit rationale, inputs, outputs, allowed tools, skill bindings, memory policy, eval obligations, and receipt obligations.

Pi orchestrates the Factory through the Python Agent Gateway, Pydantic contracts, DSPy programs, Command Bus, durable workflows, and human review. Google ADK and Agents CLI can be useful adapter or deployment references, but CMF source of truth remains Python/Pydantic/DSPy/Pi.

## 2. Entity Vocabulary

| Entity | Definition |
|---|---|
| Factory | Department-based production operating system for CMF |
| Department | Bounded production capability that owns stage objects and proof obligations |
| Agent | Named accountable role contract |
| Sub-agent | Specialist role with narrower scope and permissions |
| Tool | Executable capability exposed as a command, query, workflow, adapter, or provider action |
| Hook | Lifecycle check before or after model, tool, workflow, command, or receipt creation |
| Extension | Adapter package that exposes tools, deployment surfaces, provider actions, or integrations |
| Stable skill | Reusable operational procedure |
| JIT skill compiler | Saturation-bound compiler for specialized execution |

## 3. First Executable Factory Slice

The first agentic slice follows the interview-first chain:

```text
SCRE/CRAL Research Agent
-> Evidence Critic
-> Context Premise Agent
-> Matrix of Edging Agent
-> JIT Skill Compiler Agent
-> Interview Brief Agent
-> Expression Extraction Agent
-> Route Candidate Agent
-> Eval Registry Agent
-> Evaluation Agent
-> Review Workbench Agent
-> Pi Orchestrator
```

This slice exists because it exercises the actual CMF moat: better interview preparation, better source expression, governed extraction, primitive-aware evaluation, and reviewable approval evidence.

## 4. Functional Requirements

### FR-CMF-AGENT-01 Factory Registry

The system shall maintain a Factory registry of departments, agents, sub-agents, tools, skills, hooks, eval bindings, memory policies, and receipt obligations.

### FR-CMF-AGENT-02 Agent Role Spec

Every agent shall have a role spec containing goal, department, fit rationale, entry objects, exit objects, allowed tools, stable skills, JIT skill modes, hooks, evals, memory access policy, and receipts.

### FR-CMF-AGENT-03 Sub-Agent Boundaries

Sub-agents shall be scoped to bounded specialist work and shall inherit permission, evidence, registry, and receipt constraints from their owning agent or department.

### FR-CMF-AGENT-04 Tool Construction

Because Pi does not include CMF production tools by default, every tool must be built as a typed command, query, workflow signal, provider adapter, renderer action, research action, or review action.

### FR-CMF-AGENT-05 Hook Governance

Hooks shall enforce source evidence, consent, cost, role, registry, primitive, eval, memory, and receipt checks before and after consequential execution.

### FR-CMF-AGENT-06 Intelligence Profile

Every agent shall declare how it uses constitutions, standards, primitives, rules, protocols, memory, skills, tools, evals, and receipts.

### FR-CMF-AGENT-07 Pi Orchestration

Pi shall coordinate agents through StageExecutionPlans, AgentHandoffPackets, ValidationContracts, Command Bus submissions, workflow signals, and receipts.

### FR-CMF-AGENT-08 ADK/Agents CLI Adapter

The system may export ADK/Agents CLI-compatible configs from CMF AgentRoleSpecs after Python contracts exist. Hand-authored ADK configs are not the canonical source.

## 5. Epics and Stories

### Epic AGENT-1: Factory Registry and Intelligence Contracts

**Outcome:** CMF can describe its agent team before executing it.

- Story AGENT-1.1: Define DepartmentSpec and Factory registry.
- Story AGENT-1.2: Define AgentRoleSpec and SubAgentRoleSpec.
- Story AGENT-1.3: Define IntelligenceProfile.
- Story AGENT-1.4: Bind tools, stable skills, JIT modes, hooks, evals, memory policies, and receipts.
- Story AGENT-1.5: Validate incomplete agent specs as blocked.

### Epic AGENT-2: First Interview-to-Review Agent Team

**Outcome:** The first Factory team can execute the research-to-review slice.

- Story AGENT-2.1: Register SCRE/CRAL Research Agent and Evidence Critic.
- Story AGENT-2.2: Register Context Premise and Matrix Agents.
- Story AGENT-2.3: Register JIT Skill Compiler and Interview Brief Agents.
- Story AGENT-2.4: Register Extraction and Route Candidate Agents.
- Story AGENT-2.5: Register Eval Registry, Evaluation, and Review Workbench Agents.

### Epic AGENT-3: Runtime Orchestration and Adapters

**Outcome:** Pi can orchestrate the Factory safely, and adapter exports remain projections.

- Story AGENT-3.1: Create StageExecutionPlan for interview-to-review slice.
- Story AGENT-3.2: Create AgentHandoffPacket between agents.
- Story AGENT-3.3: Enforce ValidationContracts and hooks.
- Story AGENT-3.4: Submit approved commands through Command Bus.
- Story AGENT-3.5: Generate ADK/Agents CLI adapter configs from typed specs.

## 6. Non-Goals and Forbidden Drift

- No agent as untyped persona prompt.
- No hidden tool execution.
- No direct state mutation by Pi or agents.
- No generated ADK config as source of truth.
- No agent memory without evidence admission.
- No agent can approve final publication.
- No agent can invent content formats, primitives, routes, or eval standards outside active registries.

