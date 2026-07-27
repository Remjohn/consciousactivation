---
tech_spec_id: "TS-CMF-068"
title: "Pi Harness Tool Registry"
story_id: "11.7"
story_title: "Pi Harness Tool Registry and Department Runtime"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-development"
created_at: "2026-06-22"
source_story: "docs/stories/story-11-7-pi-harness-tool-registry-and-department-runtime.md"
fr_ids:
  - "PRD-CMF-10.08"
  - "PRD-CMF-02.04"
  - "PRD-CMF-02.05"
module_requirement_ids:
  - "PRD-CMF-10.08"
  - "PRD-CMF-02.04"
  - "PRD-CMF-02.05"
pipeline_stage: "all stages"
entry_object: "Pi action and tool need"
exit_object: "`ToolCapabilitySpec`, department runtime registry"
validation_contract: "Pydantic I/O, role scope, idempotency, receipt obligation"
required_receipt: "tool registration receipt"
runtime_target: "Python / Pydantic v2 / Pi Agent Gateway / Command Bus / durable workflows"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-068: Pi Harness Tool Registry

**Status:** Ready for Development  
**Story:** `11.7 - Pi Harness Tool Registry and Department Runtime`  
**Implementation Boundary:** ToolCapabilitySpec, department runtime registry, Pi gateway tool resolution, Pydantic I/O contracts, role/stage scope, idempotency, receipt obligations, and missing-tool handoff behavior.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-11-7-pi-harness-tool-registry-and-department-runtime.md` | Story source and acceptance criteria. |
| `docs/prd/modules/PRD_CMF_10_Agent_Factory_Runtime.md` | Harness and Department Runtime authority. |
| `docs/prd/modules/PRD_CMF_02_Pipeline_Agent_Orchestration.md` | Pi harness rules and handoff packet obligations. |
| `docs/cmf-studio-agent-factory-architecture.md` | Tool vocabulary and Factory runtime. |
| `src/ccp_studio/contracts/agent_gateway.py` | Existing gateway request/decision. |
| `src/ccp_studio/services/agent_gateway.py` | Current constrained Pi Agent Gateway. |
| `docs/architecture.md` | Command Bus, workflows, provider adapters, and generated contracts. |
| `docs/migration/legacy-inventory.md` | Legacy tool behavior and adapter sources. |

## 2. Overview

Pi has no built-in CMF production tools. Every executable capability must be registered as a `ToolCapabilitySpec` and scoped by department, stage, role, Pydantic input/output, idempotency, receipt obligation, failure behavior, and mutation boundary.

The registry lets Pi coordinate the Factory without inventing tools or bypassing the backend. If a required tool is missing, Pi creates a human handoff or blocker.

## 3. Context for Development

### Requirement Trace

| Requirement | Required Behavior | Spec Coverage |
|---|---|---|
| PRD-CMF-10.08 | Pi orchestrates through Agent Gateway and explicitly built tools/adapters/registries. | ToolCapabilitySpec and department runtime registry. |
| PRD-CMF-02.04 | Pi reads active object, validates transition, selects allowed tool/service, writes receipt. | Gateway tool resolution and validation. |
| PRD-CMF-02.05 | Handoffs carry active object, evidence, allowed actions, blocked actions, proof obligations. | Missing-tool handoff and receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | all stages |
| Entry Object | Pi action and tool need |
| Exit Object | `ToolCapabilitySpec`, department runtime registry |
| Validation Contract | Pydantic I/O, role scope, idempotency, receipt obligation |
| Required Receipt | tool registration receipt |

## 4. Implementation Plan

1. Define `ToolCapabilitySpec`, `ToolInvocationRequest`, `ToolInvocationReceipt`, and `DepartmentRuntimeRegistry`.
2. Register command tools, query tools, workflow signal tools, DSPy tools, provider tools, renderer tools, review tools, and projection tools.
3. Add Pydantic input/output model refs and schema validation.
4. Add role, department, and stage scope validation.
5. Add idempotency policy and receipt obligation.
6. Extend `PiAgentGateway` to resolve requested tools and reject unregistered/mis-scoped tools.
7. Add missing-tool blocker/human handoff behavior.
8. Add tests across Command Bus, provider, renderer, and review tools.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class ToolCapabilityKind(str, Enum):
    command = "command"
    query = "query"
    workflow_signal = "workflow_signal"
    dspy_program = "dspy_program"
    provider_adapter = "provider_adapter"
    renderer = "renderer"
    review_action = "review_action"


class ToolCapabilitySpec(BaseModel):
    schema_version: Literal["cmf.tool_capability_spec.v1"]
    tool_capability_spec_id: UUID
    tool_key: str
    kind: ToolCapabilityKind
    department_code: str
    allowed_agent_refs: list[str]
    allowed_stage_refs: list[str]
    input_model_ref: str
    output_model_ref: str
    idempotency_required: bool
    required_receipt_type: str
    mutation_boundary: Literal["none", "command_bus", "workflow_command"]
    failure_behavior: Literal["block", "retry", "handoff", "terminal_failure"]
    active: bool
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `RegisterToolCapabilityCommand`, `ActivateToolCapabilityCommand`, `InvokeToolCapabilityCommand`, `RecordToolInvocationReceiptCommand` |
| Events | `ToolCapabilityRegistered`, `ToolCapabilityActivated`, `ToolInvocationAllowed`, `ToolInvocationBlocked`, `ToolInvocationCompleted` |
| Workflow | `AgentFactoryWorkflow.department_tool_runtime` |
| Receipt | `ToolRegistrationReceipt`, `ToolInvocationReceipt`, `MissingToolHandoffReceipt` |

## 7. Backward Compatibility and Migration Fallback

Legacy scripts, provider snippets, and manual operations become ToolCapabilitySpec records only after Pydantic I/O, role/stage scope, idempotency, and receipts are defined. Otherwise they remain reference-only.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Pi autonomy vs. no built-in tools | Pi can only use registered ToolCapabilitySpec. | Gateway rejects missing tools. |
| Execution power vs. mutation safety | Mutating tools require Command Bus or workflow command boundary. | Tool spec and invocation receipt. |
| Provider convenience vs. lineage | Provider/renderer tools store metadata, cost, retries, hashes. | Provider tool receipts. |

## 9. Tasks

- Add tool capability contracts.
- Add department runtime registry.
- Extend Agent Gateway.
- Add missing-tool handoff.
- Seed initial tools.
- Add API/read model.
- Add tests.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Tool exposes Pydantic I/O, department, stage, role, idempotency, receipt, failure behavior. | Tool is arbitrary Python function with no schema. |
| AC2 | Pi tool request outside stage/role is blocked. | Pi calls provider during consent-blocked stage. |
| AC3 | Missing tool creates handoff/blocker. | Pi invents unregistered tool. |
| AC4 | Mutating tool goes through Command Bus or workflow command. | Tool writes repository directly. |
| AC5 | Provider/renderer tool preserves metadata, cost, retry, hashes. | Render output has no provider receipt. |

## 11. Dependencies

- TS-CMF-001, TS-CMF-002, TS-CMF-042 through TS-CMF-049, TS-CMF-063, TS-CMF-065.

## 12. Testing Strategy

Unit tests:

- ToolCapabilitySpec validation.
- Stage/role scope checks.
- Mutation boundary checks.

Integration tests:

- Pi gateway permits valid command tool and blocks invalid stage request.
- Missing tool emits handoff receipt.
- Provider/renderer tool stores metadata and hashes.

Eval and recovery tests:

- Duplicate idempotent invocation does not duplicate side effect.
- Failed provider tool invocation supports retry/handoff according to spec.

## 13. Observability, Recovery, and Rollback

- Metrics: tool registrations, invocations, denials, missing tools, duplicate idempotency hits.
- Logs include tool key, agent code, stage plan, input hash, output hash, receipt ID.
- Rollback deactivates tool capability; prior invocation receipts remain.

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
| Tech Spec ID | TS-CMF-068 |
| Story | 11.7 |
| Requirement Trace | PRD-CMF-10.08, PRD-CMF-02.04, PRD-CMF-02.05 |
| Pipeline Trace | all stages, Pi action/tool need to ToolCapabilitySpec |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No invented Pi tools, no direct repository writes, no provider output without receipt |
