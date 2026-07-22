---
tech_spec_id: "TS-CMF-138"
title: "Pi Harness Agent Command Routing and Delegation Runtime"
story_id: "15.3"
story_title: "Make Agent Operations Accountable Through the Harness"
epic_id: 15
epic_title: "Operator Operations Runtime and Agentic Control"
status: "ready-for-development"
created_at: "2026-06-26"
fr_ids:
  - "FR-CMF-03"
  - "FR-CMF-05"
  - "FR-CMF-06"
  - "FR-CMF-07"
  - "FR-CMF-10"
pipeline_stage: "agentic orchestration, delegation, stage execution, and command proposal"
entry_object: "AgentActionRequest, StageExecutionPlan, AgentRoleSpec"
exit_object: "AgentGatewayDecision, AgentHandoffPacket, AgentCommandProposalReceipt"
validation_contract: "agent authority, sub-agent delegation, allowed tools, stage scope, command proposal, no direct mutation"
required_receipt: "AgentCommandProposalReceipt"
runtime_target: "Python / PiAgentGateway / AgentFactoryService / OrchestrationService / Command Bus"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-138: Pi Harness Agent Command Routing and Delegation Runtime

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/cmf-studio-agent-factory-architecture.md` | Defines departments, agents, sub-agents, hooks, extensions, skills, persona codes, and authority boundaries. |
| `THE CMF STUDIO/docs/cmf-studio-intelligence-operating-model.md` | Defines intelligence as governed capability, expertise, standards, protocols, memory, tools, and constitutions. |
| `THE CMF STUDIO/docs/architecture.md` | Defines Pi as orchestrator that cannot mutate state directly. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-063-agentrolespec-and-departmentspec-runtime.md` | Agent role and department contracts. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-064-subagentrolespec-and-delegation-boundaries.md` | Sub-agent delegation rules. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-066-skillbinding-and-jit-skill-mode-binding.md` | Skill binding and JIT skill mode rules. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-068-pi-harness-tool-registry.md` | Pi harness tool registry dependency. |
| `THE CMF STUDIO/src/ccp_studio/services/agent_gateway.py` | Existing `PiAgentGateway.request_action` implementation. |
| `THE CMF STUDIO/src/ccp_studio/contracts/agent_gateway.py` | Existing `AgentActionRequest` and `AgentGatewayDecision` contracts. |
| `THE CMF STUDIO/src/ccp_studio/services/agent_factory_service.py` | Existing Agent Factory service. |
| `THE CMF STUDIO/src/ccp_studio/services/command_bus.py` | Mutation boundary for agent-proposed commands. |

## 2. Overview

CMF agents are not prompts. They are accountable runtime actors with production goals, bounded authority, object scope, allowed tools, memory access, standards, protocols, eval obligations, and receipt outputs. The Pi harness is the orchestrator that activates those actors. This spec turns agent activity into a governed runtime path: Agent Factory resolves the appropriate agent, Pi creates an action request, Agent Gateway verifies authority and stage scope, the agent or sub-agent performs bounded work, and any mutation becomes a command proposal or Command Bus submission.

The user asked whether operations are agentically managed and what happens when edits, updates, or revisions are needed. The answer after this spec is: yes, but not as free-form autonomy. Agents propose, execute bounded deterministic or intelligence tasks, and write receipts. They may not self-approve, skip eval gates, or mutate state outside the Command Bus.

Persona codes such as `RES-VISRSCH-AG` are not decorative. They must map to `AgentRoleSpec`, department, authority scope, tool menu, skills, memory policy, eval obligations, and operator-visible activity.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-138-001 | `AgentRoleSpec` | Defines goal, authority, tools, memory, standards, protocols, and receipts. |
| DEP-CMF-138-002 | `SubAgentRoleSpec` | Defines parent-bound narrow delegation. |
| DEP-CMF-138-003 | `AgentActionRequest` | Pi request to invoke an agent for a stage/object. |
| DEP-CMF-138-004 | `AgentGatewayDecision` | Allow, block, delegate, or require human approval. |
| DEP-CMF-138-005 | `AgentHandoffPacket` | Stage-specific packet sent to agent/sub-agent. |
| DEP-CMF-138-006 | `AgentCommandProposalReceipt` | Receipt proving proposed command, evidence, and validation status. |
| DEP-CMF-138-007 | `AgentActivityReadModel` | UI-visible current and historical agent work. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `services/agent_gateway.py` | Resolve `AgentRoleSpec`, verify authority, build action receipts, and create command proposals. |
| `services/agent_factory_service.py` | Provide persona code lookup, department membership, and readiness state. |
| `services/orchestration_service.py` | Create handoff packets and stage execution records. |
| `services/command_bus.py` | Accept agent-originated commands only after policy validation. |
| `contracts/agent_gateway.py` | Add proposal receipt, delegation result, and authority blocker schemas. |
| `api/v1/agent_factory.py` | Expose agent readiness and activity read model. |

### ADR-05 Primitive Implementation

Agents performing creative or evaluative work must declare primitive obligations before execution. The gateway blocks agent actions that target composition, script, interview question, extraction, or review stages without the required primitive/eval registry references.

### CBAR Mandate Enforcement

| CBAR Mandate | Implementation Rule |
|---|---|
| Phase1-M05 Deterministic Override | Agent output is not canonical until validated and receipted. |
| Phase3-M04 Telemetry Surfacing | Agent decisions and blockers appear in the operator UI. |
| Phase4-M03 Inline Routing SLA | Gateway returns route/delegation decision quickly before long work starts. |
| Phase4-M04 Frictionless Block | Blocked agent actions include exact authority or evidence gap. |
| Phase5-M01 Verifiable Artifact | Every agent action emits a handoff, proposal, or execution receipt. |

## 4. PRD and FR-CMF Requirement Trace

| Requirement | Implementation Meaning |
|---|---|
| FR-CMF-03 | Agents use migrated intelligence, JIT skills, and spec governance through CMF contracts. |
| FR-CMF-05 | Research, interview intelligence, Context Premise, and Narrative Induction agents run with source evidence. |
| FR-CMF-06 | Extraction and routing agents work only on source-backed expression objects. |
| FR-CMF-07 | Composition agents cannot bypass SceneSpec, timing, and render contracts. |
| FR-CMF-10 | Operations, recovery, memory, and projection agents write receipts and read models. |

## 5. Canonical Pipeline Stage Trace

| Stage | Agent Runtime Rule |
|---|---|
| Research | Research agents gather and synthesize evidence but cannot approve interview briefs. |
| Interview Brief | Brief agents compile questions; operator approves. |
| Recording | Capture agents track live coverage and blockers; no content fabrication. |
| Extraction | Extraction agents propose expression candidates; review service approves. |
| Routing | Routing agents propose asset routes; eval and operator approve where required. |
| Composition | Composition agents compile JSON/programs; render/eval services validate. |
| Review | Review agents prepare evidence; human operator remains final arbiter. |
| Recovery | Recovery agents propose repairs; commands execute through Command Bus. |

## 6. Greenfield Integration and Legacy Migration Context

Legacy BMAD/Google Agents CLI patterns may inform exported adapter formats, but CMF-native `AgentRoleSpec` remains the source of truth. Legacy skills become skill bindings or JIT compiler inputs only after registry conversion and eval.

## 7. Architecture Component Map

| Component | Owner | Responsibility |
|---|---|---|
| `AgentRuntimeResolver` | Agent Gateway | Resolve persona code to role spec and runtime adapter. |
| `AgentAuthorityPolicy` | Agent Gateway | Validate stage, object scope, allowed tools, memory, and command types. |
| `DelegationPolicy` | Agent Gateway | Ensure sub-agents cannot expand authority beyond parent stage contract. |
| `AgentCommandProposalService` | Agent Gateway | Convert agent intent into command draft/proposal. |
| `AgentActivityProjector` | Projection service | Feed agent activity into UI read model. |

## 8. Implementation Plan

1. Extend `AgentActionRequest` with persona code, stage id, active object, desired command type, expected receipt type, and evidence refs.
2. Add `AgentAuthorityPolicy.validate(request, role_spec, stage_plan)`.
3. Add `AgentCommandProposalReceipt` and `AgentActivityReadModel` contracts.
4. Extend `PiAgentGateway.request_action()` to resolve role spec, validate readiness, validate stage scope, validate tool/menu access, create handoff packet, return allow/block/delegate decision, and create command proposal when mutation is requested.
5. Add a command submission path that marks `actor_kind="agent"` and `actor_ref=persona_code`.
6. Add UI read model endpoint for current agent activity by workspace, stage, and object.
7. Add tests proving agents cannot self-approve, mutate directly, call providers outside tool registry, access other guest workspaces, or delegate broader authority to sub-agents.

## 9. Primary Pydantic Output Schema

```python
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field

class AgentAuthorityBlocker(BaseModel):
    blocker_code: str
    severity: Literal["soft", "hard"]
    message: str
    required_action: str

class AgentCommandProposalReceipt(BaseModel):
    schema_version: Literal["cmf.agent_command_proposal_receipt.v1"] = "cmf.agent_command_proposal_receipt.v1"
    receipt_id: UUID
    persona_code: str = Field(min_length=1)
    department_code: str = Field(min_length=1)
    stage_id: str = Field(min_length=1)
    active_object_type: str = Field(min_length=1)
    active_object_id: UUID
    proposed_command_type: str | None = None
    proposed_command_payload: dict = Field(default_factory=dict)
    evidence_refs: list[str] = Field(default_factory=list)
    authority_blockers: list[AgentAuthorityBlocker] = Field(default_factory=list)
    decision: Literal["allowed", "blocked", "delegated", "requires_human_approval"]
    created_at: datetime
```

## 10. Commands, Events, Workflows, and Receipts

| Object | Requirement |
|---|---|
| `AgentActionRequest` | Entry for every Pi-triggered agent operation. |
| `AgentGatewayDecision` | Returned before work begins. |
| `AgentHandoffPacket` | Created for allowed/delegated work. |
| `AgentCommandProposalReceipt` | Required when an agent wants to mutate state. |
| `agent.action.blocked` | Event with blocker code and required action. |
| `agent.command.proposed` | Event linked to command draft. |

## 11. DSPy Programs, JIT Skills, or Deterministic Services

Agents may use DSPy programs, deterministic services, or skills only through `SkillBinding` and tool registry policy. JIT skills are especially relevant for extraction, narrative induction, interview engineering, and creative output generation, but their output remains draft intelligence until converted to validated contracts.

## 12. Provider, Renderer, Projection, or Worker Boundaries

Agents call providers through registered tool adapters. They do not hold provider secrets in prompts, launch renderers directly, or write to object storage without provider/job receipts.

## 13. CBAR Constraint Pass

| Constraint | Pass Condition |
|---|---|
| Tension | Autonomous team behavior is useful, but hidden autonomy is unsafe. |
| Failure Scenario | Composition agent regenerates an asset without operator scope or command receipt. |
| Resolution Demand | Agent Gateway blocks or converts intent to command proposal. |
| Downstream Proof | UI shows agent, stage, proposed command, evidence, and receipt. |

## 14. Acceptance Criteria with Failure Examples

| AC | Acceptance Criteria | Failure Example | CBAR |
|---|---|---|---|
| AC138-01 | Every Pi agent action enters through `PiAgentGateway.request_action`. | Pi calls provider adapter directly. | Phase1-M05 |
| AC138-02 | Gateway validates persona code against Agent Factory registry. | Unknown agent performs extraction. | Phase4-M04 |
| AC138-03 | Sub-agent delegation cannot expand parent authority. | Context Premise sub-agent submits render approval. | Phase4-M04 |
| AC138-04 | Agent mutation intent becomes command proposal or Command Bus envelope. | Agent writes review status directly. | Phase5-M01 |
| AC138-05 | Agent activity appears in Operator UI read model. | Operator cannot tell which agent changed route proposal. | Phase3-M04 |
| AC138-06 | JIT skill use records skill binding and eval refs. | Interview questions appear with no skill/compiler trace. | Phase5-M01 |

## 15. Dependencies

| Dependency | Required Before Build |
|---|---|
| TS-CMF-063 | Agent and department runtime. |
| TS-CMF-064 | Sub-agent boundaries. |
| TS-CMF-066 | Skill binding and JIT modes. |
| TS-CMF-067 | Agent readiness evals. |
| TS-CMF-068 | Pi harness tool registry. |
| TS-CMF-137 | Production app composition root. |

## 16. Testing Strategy

| Test Type | Required Tests |
|---|---|
| Unit | Unknown persona code is blocked. |
| Unit | Agent with missing tool permission is blocked. |
| Unit | Sub-agent authority cannot exceed parent. |
| Integration | Pi request creates handoff packet and proposal receipt. |
| Negative | Agent cannot approve its own output. |
| UI | Agent activity read model shows current and recent work. |

## 17. Observability, Recovery, and Rollback

1. Log every gateway decision with correlation id and persona code.
2. Store blocked decisions for audit and agent readiness improvement.
3. Roll back a problematic agent by disabling its registry readiness flag.
4. Keep human operator override through command review, not direct state edit.

## 18. Spec Audit Receipt

| Field | Value |
|---|---|
| Spec id | TS-CMF-138 |
| Protocol | CMF/ERA3 18-section spec |
| Agent definitions technicalized | Yes |
| Command Bus boundary | Preserved |
| JIT skill boundary | Preserved |
| Human approval | Required for sensitive/final decisions |
| Status | ready-for-development |
