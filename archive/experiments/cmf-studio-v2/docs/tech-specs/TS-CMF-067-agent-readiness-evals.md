---
tech_spec_id: "TS-CMF-067"
title: "Agent Readiness Evals"
story_id: "11.6"
story_title: "Intelligence Contract and Agent Readiness Evals"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-development"
created_at: "2026-06-22"
source_story: "docs/stories/story-11-6-intelligence-contract-and-agent-readiness-evals.md"
fr_ids:
  - "PRD-CMF-10.06"
module_requirement_ids:
  - "PRD-CMF-10.06"
pipeline_stage: "agent-factory overlay"
entry_object: "agent intelligence profile"
exit_object: "`AgentReadinessEval`"
validation_contract: "standards, primitives, tools, memory, evals, receipts, blocked actions"
required_receipt: "readiness eval receipt"
runtime_target: "Python / Pydantic v2 / eval registry / primitive obligations"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-067: Agent Readiness Evals

**Status:** Ready for Development  
**Story:** `11.6 - Intelligence Contract and Agent Readiness Evals`  
**Implementation Boundary:** AgentReadinessEval, intelligence profile validation, primitive obligation checks, memory access checks, tool scope checks, blocked-action checks, eval binding checks, and readiness receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-11-6-intelligence-contract-and-agent-readiness-evals.md` | Story source and acceptance criteria. |
| `docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md` | Intelligence Contract authority. |
| `docs/cmf-studio-agent-intelligence-contract.md` | IntelligenceProfile structure. |
| `docs/cmf-studio-agent-factory-registry.md` | Agent and sub-agent persona registry. |
| `docs/evals/07-eval-registry-and-workbench-architecture.md` | Eval registry and workbench requirements. |
| `registries/primitives/` | Primitive quality standard source. |
| `docs/migration/legacy-inventory.md` | Legacy eval and primitive lineage. |

## 2. Overview

Agent activation requires proof that the role has the right intelligence architecture. `AgentReadinessEval` checks constitutions, standards, primitives, deterministic rules, protocols, tools, memory access, stable skills, JIT skill modes, eval bindings, receipts, blocked actions, and adapter boundaries.

This makes primitives part of agent behavior, not just output review. An extraction agent, routing agent, render agent, review agent, or memory agent cannot activate unless its primitive obligations and proof obligations are explicit.

## 3. Context for Development

### Requirement Trace

| Requirement | Required Behavior | Spec Coverage |
|---|---|---|
| PRD-CMF-10.06 | Each entity states goal, responsibility, active object, I/O, standards, primitives, memory, tools, blocked actions, evals, receipts, human handoff. | AgentReadinessEval and readiness receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | agent-factory overlay |
| Entry Object | agent intelligence profile |
| Exit Object | `AgentReadinessEval` |
| Validation Contract | standards, primitives, tools, memory, evals, receipts, blocked actions |
| Required Receipt | readiness eval receipt |

## 4. Implementation Plan

1. Define `IntelligenceProfile`, `PrimitiveObligation`, `AgentReadinessEval`, and `AgentReadinessReceipt`.
2. Validate required intelligence profile fields for AgentRoleSpec and SubAgentRoleSpec.
3. Add primitive obligation resolver against active primitive registry.
4. Add memory access policy checks.
5. Add tool scope and blocked-action checks.
6. Add eval binding checks for extraction, routing, rendering, review, memory, and publishing agents.
7. Add activation gate: AgentRoleSpec cannot become active without accepted readiness eval.
8. Add UI/read model for readiness findings.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class PrimitiveObligation(BaseModel):
    primitive_family: str
    obligation: str
    evidence_ref: str
    required: bool = True


class AgentReadinessEval(BaseModel):
    schema_version: Literal["cmf.agent_readiness_eval.v1"]
    agent_readiness_eval_id: UUID
    entity_code: str
    target_spec_ref: str
    primitive_obligations: list[PrimitiveObligation]
    tool_scope_passed: bool
    memory_policy_passed: bool
    eval_bindings_passed: bool
    receipt_obligations_passed: bool
    blocked_actions_passed: bool
    adapter_boundary_passed: bool
    status: Literal["accepted", "revision_required", "blocked"]
    findings: list[str]
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `RunAgentReadinessEvalCommand`, `ApproveAgentReadinessCommand`, `BlockAgentActivationCommand` |
| Events | `AgentReadinessEvalStarted`, `AgentReadinessEvalAccepted`, `AgentReadinessEvalBlocked`, `AgentActivationRevisionRequested` |
| Workflow | `AgentFactoryWorkflow.readiness_eval` |
| Receipt | `AgentReadinessReceipt` linked to role spec and activation state |

## 7. Backward Compatibility and Migration Fallback

Existing agents without readiness eval remain draft. Legacy agents or BMad personas can be mapped into AgentRoleSpec, but cannot activate until readiness eval passes.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Intelligence breadth vs. bounded action | Readiness checks tools, memory, evals, receipts, blocked actions. | AgentReadinessReceipt blocks activation. |
| Primitives as theory vs. production standard | Primitive obligations are required for quality-critical roles. | Eval records active primitive families and obligations. |
| Adapter convenience vs. runtime authority | Adapter boundary check prevents ADK drift. | Adapter boundary pass/fail in readiness eval. |

## 9. Tasks

- Add readiness eval contracts.
- Add primitive obligation resolver.
- Add readiness service and repository.
- Integrate activation gate.
- Add read model.
- Add tests and fixtures.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Eval checks constitutions, standards, primitives, rules, protocols, tools, memory, skills, evals, receipts, blockers. | Agent activates with goal and prompt only. |
| AC2 | Missing primitive obligations block/revision quality-critical roles. | Routing agent has no primitive obligations. |
| AC3 | Overbroad memory access blocks activation. | Agent can read all brand memory globally. |
| AC4 | Missing eval obligations block review/routing/extraction/rendering. | ImageCritic has no eval target. |
| AC5 | Accepted readiness receipt links to role spec. | Active agent has no readiness evidence. |

## 11. Dependencies

- TS-CMF-014, TS-CMF-050, TS-CMF-056, TS-CMF-062, TS-CMF-063, TS-CMF-064, TS-CMF-066.

## 12. Testing Strategy

Unit tests:

- Readiness pass/fail for complete and incomplete specs.
- Primitive obligation resolution.
- Memory and tool scope validation.

Integration tests:

- Agent activation requires accepted readiness eval.
- Readiness finding appears in review UI/read model.
- Adapter boundary failure blocks activation.

Eval and recovery tests:

- Fixtures for missing primitives, missing evals, overbroad memory, and direct mutation attempts.
- Re-run readiness after repair supersedes prior receipt.

## 13. Observability, Recovery, and Rollback

- Metrics: readiness evals run, blocked activations, common finding codes.
- Logs include entity code, target spec, findings, status, receipt ID.
- Rollback marks readiness eval superseded and deactivates affected role.

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
| Tech Spec ID | TS-CMF-067 |
| Story | 11.6 |
| Requirement Trace | PRD-CMF-10.06 |
| Pipeline Trace | agent-factory overlay, intelligence profile to AgentReadinessEval |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No active agent without readiness eval, no missing primitive obligations, no global memory access |
