---
tech_spec_id: "TS-CMF-063"
title: "AgentRoleSpec and DepartmentSpec Runtime"
story_id: "11.2"
story_title: "Agent Role Spec Catalog"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-development"
created_at: "2026-06-22"
source_story: "docs/stories/story-11-2-agent-role-spec-catalog.md"
fr_ids:
  - "PRD-CMF-10.01"
  - "PRD-CMF-02.03"
  - "PRD-CMF-02.05"
module_requirement_ids:
  - "PRD-CMF-10.01"
  - "PRD-CMF-02.03"
  - "PRD-CMF-02.05"
pipeline_stage: "agent-factory overlay"
entry_object: "department and production responsibility"
exit_object: "`AgentRoleSpec` catalog"
validation_contract: "goal, active object, tool, memory, eval, receipt completeness"
required_receipt: "agent role spec receipt"
runtime_target: "Python / Pydantic v2 / Agent Gateway / Command Bus / generated adapters"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-063: AgentRoleSpec and DepartmentSpec Runtime

**Status:** Ready for Development  
**Story:** `11.2 - Agent Role Spec Catalog`  
**Implementation Boundary:** DepartmentSpec, AgentRoleSpec, role catalog, activation checks, runtime invocation path, gateway binding, adapter binding fields, and agent role receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-11-2-agent-role-spec-catalog.md` | Story source and acceptance criteria. |
| `docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md` | Technical Agent definition and AgentRoleSpec authority. |
| `docs/prd/modules/PRD_CMF_02_Pipeline_Agent_Orchestration.md` | Agent topology and handoff packet obligations. |
| `docs/cmf-studio-agent-factory-architecture.md` | Runtime architecture and invocation spine. |
| `docs/cmf-studio-agent-intelligence-contract.md` | AgentRoleSpec shape and intelligence profile. |
| `docs/cmf-studio-agent-factory-registry.md` | Persona code seed registry. |
| `src/ccp_studio/contracts/agent_gateway.py` | Existing `AgentActionRequest` and gateway decision contracts. |
| `src/ccp_studio/contracts/orchestration.py` | Existing `OrchestrationRun`, `StageExecutionPlan`, `ValidationContract`, `AgentHandoffPacket`. |
| `docs/migration/legacy-inventory.md` | Legacy role/persona lineage and orchestration intent source. |

## 2. Overview

`AgentRoleSpec` is the canonical runtime contract for every CMF Agent. It prevents agents from becoming prompt-only personas by requiring goal, fit rationale, active object scope, entry/exit contracts, allowed tools, skill bindings, sub-agent bindings, hook bindings, memory policy, eval obligations, blocked actions, receipts, activation state, readiness eval link, and generated adapter hash.

An Agent may compile to Python role class, DSPy program, deterministic service, durable workflow activity, ADK adapter, provider worker, or human review queue. The implementation varies; `AgentRoleSpec` remains canonical.

## 3. Context for Development

### Requirement Trace

| Requirement | Required Behavior | Spec Coverage |
|---|---|---|
| PRD-CMF-10.01 | Define Agent as accountable runtime role represented by `AgentRoleSpec`. | Contracts, registry, activation, runtime invocation, gateway checks. |
| PRD-CMF-02.03 | Preserve agent team topology by department and responsibility. | DepartmentSpec and role catalog. |
| PRD-CMF-02.05 | Handoffs carry active object, evidence, actions, blockers, and proof obligations. | Handoff fields and receipt obligations in AgentRoleSpec. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | agent-factory overlay |
| Entry Object | department and production responsibility |
| Exit Object | `AgentRoleSpec` catalog |
| Validation Contract | goal, active object, tool, memory, eval, receipt completeness |
| Required Receipt | agent role spec receipt |

### Runtime Invocation Trace

`OrchestrationRun` -> `StageExecutionPlan` -> `ValidationContract` -> `AgentActionRequest` -> `PiAgentGateway` -> allowed tool/workflow/DSPy/service/adapter/human queue -> typed output -> required receipt -> `AgentHandoffPacket`.

## 4. Implementation Plan

1. Define `DepartmentSpec`, `AgentRoleSpec`, `AgentActivationState`, `MemoryAccessPolicy`, and `AgentRoleSpecReceipt`.
2. Link `AgentRoleSpec.entity_code` to TS-CMF-062 persona registry.
3. Add repository/service for agent role registration, inspection, activation, and deactivation.
4. Add readiness precondition: no activation without active object scope, allowed tools, memory policy, eval obligations, blocked actions, and receipts.
5. Extend `PiAgentGateway` to resolve the active `AgentRoleSpec` before authorizing `AgentActionRequest`.
6. Add generated adapter hash fields for ADK/Agents CLI exports.
7. Add read models for Agent Factory UI and spec workflow lookup.
8. Emit `AgentRoleSpecReceipt`.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class AgentActivationState(str, Enum):
    draft = "draft"
    ready_for_eval = "ready_for_eval"
    active = "active"
    blocked = "blocked"
    deprecated = "deprecated"


class DepartmentSpec(BaseModel):
    schema_version: Literal["cmf.department_spec.v1"]
    department_key: str = Field(min_length=3, max_length=3)
    display_name: str
    pipeline_stage_refs: list[str]
    owned_object_types: list[str]
    proof_obligations: list[str]


class AgentRoleSpec(BaseModel):
    schema_version: Literal["cmf.agent_role_spec.v1"]
    agent_role_spec_id: UUID
    entity_code: str
    department_key: str
    service_code: str
    display_name: str
    persona_name: str | None = None
    goal: str
    fit_rationale: str
    pipeline_stage_refs: list[str]
    active_object_types: list[str]
    entry_object_contracts: list[str]
    exit_object_contracts: list[str]
    allowed_tool_refs: list[str]
    stable_skill_refs: list[str] = []
    jit_skill_mode_refs: list[str] = []
    sub_agent_refs: list[str] = []
    hook_refs: list[str] = []
    eval_refs: list[str]
    memory_access_policy_ref: str
    blocked_actions: list[str]
    required_receipt_types: list[str]
    readiness_eval_id: UUID | None = None
    activation_state: AgentActivationState
    generated_adapter_hash: str | None = None
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `RegisterAgentRoleSpecCommand`, `ActivateAgentRoleSpecCommand`, `DeactivateAgentRoleSpecCommand`, `InspectAgentRoleSpecCommand` |
| Events | `AgentRoleSpecRegistered`, `AgentRoleSpecActivated`, `AgentRoleSpecBlocked`, `AgentRoleSpecDeactivated` |
| Workflow | `AgentFactoryWorkflow.agent_role_spec_activation` |
| Receipt | `AgentRoleSpecReceipt` with validation results, readiness eval ref, and active object proof |

## 7. Backward Compatibility and Migration Fallback

Earlier BMad agent personas and legacy role names may become display names or source refs, but runtime activation requires `AgentRoleSpec`. Any runtime actor without a role spec remains unavailable to Pi and generated adapters.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Agent persona vs. accountable runtime actor | Agent requires `AgentRoleSpec`, active object scope, tools, memory, evals, and receipts. | Activation fails when required fields are missing. |
| Multiple implementation shapes vs. one authority | Python, DSPy, ADK, workflow, service, provider, or human queue all bind to the same spec. | Runtime invocation stores `agent_role_spec_id`. |
| Autonomy vs. mutation safety | Agents cannot mutate outside Command Bus or durable workflow commands. | Gateway and static guard block direct writes. |

## 9. Tasks

- Add AgentRoleSpec and DepartmentSpec contracts.
- Add repository and service.
- Add activation validation.
- Extend PiAgentGateway lookup.
- Add read models and API endpoints.
- Seed role specs for initial persona registry agents.
- Add tests and receipts.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | AgentRoleSpec includes persona, department, goal, objects, tools, skills, hooks, evals, memory, blocked actions, receipts. | Agent with name and prompt only activates. |
| AC2 | Runtime invocation resolves through orchestration and gateway. | Agent executes directly from chat request. |
| AC3 | Different implementation shapes bind to same spec. | ADK adapter uses hand-authored authority not in spec. |
| AC4 | Missing active object blocks activation. | Agent acts on arbitrary objects. |
| AC5 | Direct canonical writes are blocked. | Agent writes repository state outside Command Bus. |

## 11. Dependencies

- TS-CMF-001, TS-CMF-002, TS-CMF-003, TS-CMF-062.
- Existing Agent Gateway and orchestration contracts.

## 12. Testing Strategy

Unit tests:

- Contract validation for required fields.
- Activation failure for missing active objects, tools, memory policy, evals, or receipts.
- Persona code lookup from TS-CMF-062 registry.

Integration tests:

- Gateway refuses unregistered or inactive `AgentRoleSpec`.
- Gateway permits active spec with valid stage and action.
- Agent handoff packet includes role spec and receipt obligations.

Eval and recovery tests:

- Readiness eval fixture for complete and incomplete specs.
- Deactivation prevents future invocation while preserving receipts.

## 13. Observability, Recovery, and Rollback

- Metrics: role specs by activation state, gateway denials, activation failures.
- Logs include `entity_code`, `agent_role_spec_id`, stage plan ID, requested action, and receipt ID.
- Rollback deactivates the role spec and generated adapters; no deletion of history.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 14. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-063 |
| Story | 11.2 |
| Requirement Trace | PRD-CMF-10.01, PRD-CMF-02.03, PRD-CMF-02.05 |
| Pipeline Trace | agent-factory overlay, department responsibility to AgentRoleSpec catalog |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No prompt-only agents, no direct canonical writes, no generated adapter as source of truth |
