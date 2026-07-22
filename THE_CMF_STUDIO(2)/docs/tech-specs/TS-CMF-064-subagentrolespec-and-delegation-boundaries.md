---
tech_spec_id: "TS-CMF-064"
title: "SubAgentRoleSpec and Delegation Boundaries"
story_id: "11.3"
story_title: "Sub-Agent Delegation and Bounded Authority"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-development"
created_at: "2026-06-22"
source_story: "docs/stories/story-11-3-sub-agent-delegation-and-bounded-authority.md"
fr_ids:
  - "PRD-CMF-10.02"
  - "PRD-CMF-02.03"
  - "PRD-CMF-02.05"
module_requirement_ids:
  - "PRD-CMF-10.02"
  - "PRD-CMF-02.03"
  - "PRD-CMF-02.05"
pipeline_stage: "agent-factory overlay"
entry_object: "parent agent and specialist task"
exit_object: "`SubAgentRoleSpec` binding"
validation_contract: "bounded authority and parent-stage compatibility"
required_receipt: "sub-agent binding receipt"
runtime_target: "Python / Pydantic v2 / Agent Gateway / Handoff Packets"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-064: SubAgentRoleSpec and Delegation Boundaries

**Status:** Ready for Development  
**Story:** `11.3 - Sub-Agent Delegation and Bounded Authority`  
**Implementation Boundary:** SubAgentRoleSpec, parent-agent binding, bounded I/O, tool subset validation, sub-agent receipts, parent synthesis contract, and gateway enforcement.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-11-3-sub-agent-delegation-and-bounded-authority.md` | Story source and acceptance criteria. |
| `docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md` | Technical Sub-Agent definition. |
| `docs/prd/modules/PRD_CMF_02_Pipeline_Agent_Orchestration.md` | Agent team topology and handoff obligations. |
| `docs/cmf-studio-agent-factory-architecture.md` | Sub-agent runtime architecture. |
| `docs/cmf-studio-agent-intelligence-contract.md` | SubAgentRoleSpec invocation shape. |
| `docs/cmf-studio-agent-factory-registry.md` | Initial sub-agent persona codes. |
| `src/ccp_studio/contracts/orchestration.py` | Handoff packet and stage plan contracts. |
| `docs/migration/legacy-inventory.md` | Legacy specialist lenses and orchestration intent. |

## 2. Overview

Sub-agents are narrow specialists under parent agents. They perform analysis, scoring, critique, synthesis, search, inspection, or validation. They do not own a whole pipeline stage and cannot expand authority beyond the parent `AgentRoleSpec` and current `ValidationContract`.

`SubAgentRoleSpec` protects specialized intelligence from becoming uncontrolled autonomy. It requires parent binding, bounded input/output models, limited context, tool subset validation, evidence refs, receipt linkage, and parent synthesis.

## 3. Context for Development

### Requirement Trace

| Requirement | Required Behavior | Spec Coverage |
|---|---|---|
| PRD-CMF-10.02 | Define Sub-Agent as bounded specialist under Agent. | SubAgentRoleSpec, parent binding, bounded I/O, receipts, authority checks. |
| PRD-CMF-02.03 | Preserve agent/sub-agent topology. | Parent-agent compatibility and department codes. |
| PRD-CMF-02.05 | Handoffs carry evidence and proof. | Sub-agent receipt links to parent handoff and stage. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | agent-factory overlay |
| Entry Object | parent agent and specialist task |
| Exit Object | `SubAgentRoleSpec` binding |
| Validation Contract | bounded authority and parent-stage compatibility |
| Required Receipt | sub-agent binding receipt |

## 4. Implementation Plan

1. Define `SubAgentRoleSpec`, `SubAgentInvocationRequest`, `SubAgentOutputEnvelope`, and `SubAgentReceipt`.
2. Link sub-agent `entity_code` to persona registry and parent `AgentRoleSpec`.
3. Validate parent-stage compatibility and invocation conditions.
4. Enforce bounded input and output schemas.
5. Enforce sub-agent tool list as subset of parent allowed tools or explicitly delegated tools.
6. Block direct canonical mutation by default.
7. Add parent synthesis path and handoff packet links.
8. Add tests for examples such as `RES-EVDCRIT-SA` and `SCN-CMPDIRC-SA`.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class SubAgentRoleSpec(BaseModel):
    schema_version: Literal["cmf.sub_agent_role_spec.v1"]
    sub_agent_role_spec_id: UUID
    entity_code: str
    parent_agent_refs: list[str] = Field(min_length=1)
    invocation_conditions: list[str] = Field(min_length=1)
    input_model_ref: str
    output_model_ref: str
    allowed_context_fields: list[str]
    allowed_tool_refs: list[str] = []
    mutation_policy: Literal["read_only", "parent_delegated_command_only"]
    required_evidence_refs: list[str]
    blocked_actions: list[str]
    receipt_type: str


class SubAgentReceipt(BaseModel):
    schema_version: Literal["cmf.sub_agent_receipt.v1"]
    receipt_id: UUID
    sub_agent_code: str
    parent_agent_code: str
    orchestration_run_id: UUID
    stage_execution_plan_id: UUID
    input_hash: str
    output_hash: str
    evidence_refs: list[str]
    downstream_parent_decision: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `RegisterSubAgentRoleSpecCommand`, `BindSubAgentToAgentCommand`, `InvokeSubAgentCommand`, `RecordSubAgentReceiptCommand` |
| Events | `SubAgentRoleSpecRegistered`, `SubAgentBoundToAgent`, `SubAgentInvocationCompleted`, `SubAgentInvocationBlocked` |
| Workflow | `AgentFactoryWorkflow.sub_agent_delegation` |
| Receipt | `SubAgentReceipt` linked to parent agent, stage plan, evidence refs, and parent decision |

## 7. Backward Compatibility and Migration Fallback

Legacy specialist modules can become sub-agents only after intentional orchestration mapping. If a specialist needs full stage authority, it should become an AgentRoleSpec instead. If it lacks bounded I/O, it remains a reference or skill, not a sub-agent.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Specialist intelligence vs. unchecked autonomy | Sub-agent must bind to parent and narrower task. | Parent compatibility gate and sub-agent receipt. |
| Narrow critique vs. canonical truth | Sub-agent output cannot become state directly. | Parent synthesis and Command Bus path required. |
| Tool usefulness vs. tool sprawl | Tool access is subset of parent or explicit delegation. | Gateway blocks non-listed tools. |

## 9. Tasks

- Add SubAgentRoleSpec contracts.
- Add parent binding service.
- Add invocation request and receipt.
- Add tool subset validation.
- Add gateway checks.
- Seed initial sub-agent records.
- Add tests.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Sub-agent binding includes parent, invocation conditions, I/O, blockers, proof, receipt. | Sub-agent activates with only display name. |
| AC2 | Invocation cites parent spec, run, stage, input, output. | Sub-agent runs outside any parent stage. |
| AC3 | Direct canonical mutation is blocked. | Sub-agent writes memory directly. |
| AC4 | Tool use is explicitly allowed. | Sub-agent calls provider adapter outside parent validation. |
| AC5 | Parent routes accepted result through normal path. | Sub-agent critique auto-approves publication. |

## 11. Dependencies

- TS-CMF-002, TS-CMF-062, TS-CMF-063.
- Existing handoff packet contracts.

## 12. Testing Strategy

Unit tests:

- Contract validation for parent refs, I/O model refs, mutation policy.
- Tool subset validation.
- Direct mutation blocker.

Integration tests:

- Evidence critic invoked by Context Premise Agent and receipt linked.
- Composition Director Adapter cannot override final text or identity.
- Parent handoff includes sub-agent output and receipt.

Eval and recovery tests:

- Missing parent receipt blocks downstream use.
- Re-run sub-agent with same input is idempotent and linked.

## 13. Observability, Recovery, and Rollback

- Metrics: sub-agent invocations, blocked invocations, parent compatibility failures.
- Logs include parent code, sub-agent code, stage plan ID, input/output hashes.
- Rollback deactivates binding and preserves prior receipts.

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
| Tech Spec ID | TS-CMF-064 |
| Story | 11.3 |
| Requirement Trace | PRD-CMF-10.02, PRD-CMF-02.03, PRD-CMF-02.05 |
| Pipeline Trace | agent-factory overlay, parent agent task to SubAgentRoleSpec binding |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No independent sub-agent stage authority, no direct mutation, no tool access outside parent contract |
