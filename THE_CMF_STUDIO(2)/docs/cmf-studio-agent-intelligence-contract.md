---
title: "CMF Studio Agent Intelligence Contract"
status: "draft-canonical"
created_at: "2026-06-22"
source_files:
  - "docs/cmf-studio-agent-factory-architecture.md"
  - "docs/cmf-studio-intelligence-operating-model.md"
  - "docs/cmf-studio-pipeline-map.md"
  - "docs/tech-specs/TS-CMF-002-pipeline-stage-orchestration-records.md"
  - "src/ccp_studio/contracts/agent_gateway.py"
  - "src/ccp_studio/contracts/orchestration.py"
---

# CMF Studio Agent Intelligence Contract

## 1. Purpose

An agent is a named accountable role contract. It is not a prompt persona. It uses intelligence through standards, primitives, rules, tools, protocols, memory, skills, constitutions, and evals.

## 2. Entity Definitions

| Entity | Definition |
|---|---|
| Agent | Accountable runtime role represented by `AgentRoleSpec`; invoked through `OrchestrationRun`, `StageExecutionPlan`, `ValidationContract`, and `PiAgentGateway`; executes through allowed tools, workflows, DSPy programs, deterministic services, adapters, or human queues; emits typed outputs, receipts, and handoff packets |
| Sub-agent | Specialist runtime role represented by `SubAgentRoleSpec`; bound to a parent `AgentRoleSpec`; uses narrower input/output models, narrower context, stricter tool scope, linked receipts, and no independent stage authority |
| Tool | Executable capability exposed through Python contracts, commands, queries, workflows, adapters, or provider actions |
| Hook | Lifecycle check before or after model, tool, workflow, command, or receipt creation |
| Extension | Adapter package that exposes tools, deployment surfaces, provider actions, or runtime integrations |
| Stable operational skill | Reusable procedure for regular operations such as source review, registry lookup, blocker inspection, or command proposal |
| JIT skill compiler | Saturation-bound specialist compiler for extraction, narrative induction, interview engineering, contrast, routing, or evaluation support |

## 3. Contract Shape

```text
AgentRoleSpec
  entity_code
  agent_key
  display_name
  persona_name
  department_key
  service_code
  entity_type
  goal
  fit_rationale
  entry_objects
  exit_objects
  intelligence_profile
  allowed_tools
  stable_skill_bindings
  jit_skill_modes
  sub_agent_bindings
  hook_bindings
  eval_bindings
  memory_access_policy
  receipt_obligations
  activation_state
  readiness_eval_id
  generated_adapter_hash
  adk_export_hint
```

`entity_code` must follow `DDD-XXXXXXX-TT`, where the middle segment is exactly seven characters and the type segment is exactly two characters. `agent_key` should equal `entity_code` unless a generated adapter requires a separate slug. `persona_name` is the human-readable display identity, not the operational key.

## 3A. Runtime Invocation Architecture

An agent cannot execute by receiving an unstructured prompt. It must be invoked through the runtime spine:

```text
OrchestrationRun
-> StageExecutionPlan
-> ValidationContract
-> AgentActionRequest
-> PiAgentGateway
-> ToolCapabilitySpec / workflow / DSPy program / deterministic service / adapter / human queue
-> typed output
-> required receipt
-> AgentHandoffPacket
```

Sub-agents are invoked only through a parent agent:

```text
Parent AgentRoleSpec
-> SubAgentRoleSpec binding
-> bounded input model
-> bounded execution
-> typed output
-> sub-agent receipt
-> parent synthesis or blocker
```

Runtime constraints:

- Agents and sub-agents cannot directly mutate canonical state.
- Mutations go through Command Bus or approved durable workflow commands.
- Tool use requires `ToolCapabilitySpec` and gateway validation.
- Memory access is granted by `memory_access_policy`, never by global context.
- JIT skills require `SkillInvocationRecord`.
- Outputs that influence production require receipts and eval eligibility.
- Generated ADK/Agents CLI adapters are deployment artifacts, not source of truth.

## 4. Intelligence Profile

An `IntelligenceProfile` defines how the agent thinks and acts:

- constitutions: what the agent must protect;
- standards: production standards and forbidden drift;
- primitives: quality operators the agent must preserve;
- rules: deterministic policies;
- protocols: stage and handoff procedure;
- tools: executable capability;
- memory: admitted evidence only;
- skills: stable and JIT execution knowledge;
- evals: how outcomes are inspected;
- receipts: what proves the action happened correctly.

## 5. Google ADK and Agents CLI Relationship

CMF source of truth is Python/Pydantic/DSPy/Pi. Google ADK and Agents CLI can be useful for generated adapters, deployment scaffolds, root-agent/sub-agent layout, tool declarations, callbacks, and graph workflows.

They do not replace:

- `AgentRoleSpec`;
- `StageExecutionPlan`;
- `ValidationContract`;
- `AgentHandoffPacket`;
- Command Bus;
- EvaluationReceipt;
- human approval.

## 6. First Required Agent Bindings

The first executable research-to-review slice requires:

- SCRE/CRAL Research Agent;
- Evidence Critic;
- Context Premise Agent;
- Matrix of Edging Agent;
- JIT Skill Compiler Agent;
- Expression Extraction Agent;
- Route Candidate Agent;
- Eval Registry Agent;
- Evaluation Agent;
- Review Workbench Agent;
- Pi Orchestrator.
