---
tech_spec_id: "TS-CMF-002"
title: "Pipeline Stage Execution and Orchestration Records"
story_id: "1.6"
story_title: "Pipeline Stage Execution and Orchestration Records"
epic_id: 1
epic_title: "Governed Workspace and Production Spine"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-1-6-pipeline-stage-execution-and-orchestration-records.md"
fr_ids:
  - "FR-CMF-01.06"
  - "FR-CMF-03.07"
  - "FR-CMF-10.06"
pipeline_stage: "all stages"
entry_object: "active object and requested action"
exit_object: "OrchestrationRun, StageExecutionPlan, receipt"
validation_contract: "stage/object/actor validation"
required_receipt: "stage execution receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / durable workflows / DSPy / Pi"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-002: Pipeline Stage Execution and Orchestration Records

**Status:** Ready for Development  
**Story:** `1.6 - Pipeline Stage Execution and Orchestration Records`  
**Implementation Boundary:** Canonical orchestration records, Pi handoff contracts, validation contracts, JIT skill invocation records, failure/friction/human handoff receipts.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for autonomous team orchestration, Pi harness rules, full pipeline, and no partial-scope posture. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-01.06, FR-CMF-03.07, FR-CMF-10.06 and canonical pipeline source. |
| `docs/architecture.md` | Architecture source for `OrchestrationRun`, `StageExecutionPlan`, `ValidationContract`, `AgentHandoffPacket`, and `SkillInvocationRecord`. |
| `docs/cmf-studio-pipeline-map.md` | Stage-by-stage trace source and agent/sub-agent map. |
| `docs/migration/legacy-inventory.md` | Legacy Pi extension intent, JIT skill compiler sources, and greenfield migration boundary. |
| `docs/stories/story-1-6-pipeline-stage-execution-and-orchestration-records.md` | Story acceptance criteria and handoff requirements. |
| `docs/architecture/FR39_Core_Orchestration_11_Pi_Extensions.md` | Legacy Pi extension concepts used as reference, not runtime dependency. |
| `docs/architecture/spec updates/CBAR_Constraint_Based_Adversarial_Reasoning_Epics_Stories.md` | CBAR tension structure for autonomy versus pipeline safety. |

## 2. Overview

### Problem Statement

CMF STUDIO uses agents, DSPy programs, deterministic services, provider adapters, renderers, JIT skill compilers, and human reviewers across a long creative production pipeline. If these participants operate from local prompts or implicit memory, they can skip consent, source truth, Brand Context locking, extraction evidence, evaluation, approval, publishing, memory admission, or projection boundaries.

### Solution

Implement canonical orchestration records that make every autonomous or workflow-driven action stage-aware. Pi opens or resumes an `OrchestrationRun`, creates a `StageExecutionPlan`, records a `ValidationContract`, dispatches allowed work through an `AgentHandoffPacket`, records any `SkillInvocationRecord`, and closes the stage with a success, failure, friction, human handoff, or quarantine receipt.

### Scope

In scope:

- Pydantic contracts for orchestration runs, stage plans, validation contracts, agent handoffs, skill invocations, failure receipts, friction receipts, and human handoff requests.
- Persistence and repositories for orchestration records.
- Durable workflow wrapper for retries, waits, resume, cancellation, compensation, and quarantine.
- Pi Agent Gateway contract enforcing allowed actions and blocked actions.
- Integration with the Command Bus from TS-CMF-001.
- Tests proving stages cannot be skipped and agents cannot self-approve, self-publish, or mutate canonical state directly.

Out of scope:

- Feature-specific extraction, rendering, publishing, or memory algorithms.
- UI presentation of orchestration boards.
- Provider-specific worker implementation.
- Neo4j authorization. Neo4j is derived projection only.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-01.06 | Every mutating command is idempotent, permission-checked, tenant-scoped, and receipt-writing. | Orchestration actions create typed commands through TS-CMF-001 and require receipts before advancement. |
| FR-CMF-03.07 | PRD, epic/story, architecture, and tech-spec workflows run with BMAD/ERA3 discipline updated for Python/Pydantic/DSPy/Pi. | Spec-governance runs are represented as orchestration runs and use the same stage/receipt model. |
| FR-CMF-10.06 | Provider jobs and workflows can retry, resume, cancel, compensate, or quarantine idempotently. | Durable orchestration records store state, retry policies, blocked actions, and recovery receipts. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | All CMF stages, including spec-governance overlay |
| Entry Object | Active production object and requested action |
| Exit Object | `OrchestrationRun`, `StageExecutionPlan`, receipt |
| Allowed Actors / Services | Pi Orchestrator, DSPy program, deterministic service, durable workflow, provider adapter, renderer, reviewer, recovery job |
| Validation Contract | Stage, object, actor, evidence, threshold, and receipt validation |
| Required Receipt | Stage execution receipt |
| Forbidden Shortcut | Stage skipping, direct canonical mutation, self-approval, public publishing, Neo4j as canonical state |

### Legacy Intelligence Mapping

Legacy orchestration assets are treated as design intelligence. The old Pi extension ideas such as InteractComp, TillDone, DamageControl, ModelRouter, TeamOrchestrator, SystemSelect, and MemoryFolder map into explicit Python contracts and workflows, not inherited runtime code. JIT Skill Compiler modules are invoked only through registered compiler contracts that record source context, registry snapshot, prompt layers, critic outputs, synthesis outputs, and eval state.

Target modules:

- `ccp_studio.contracts.orchestration`
- `ccp_studio.contracts.agent_gateway`
- `ccp_studio.contracts.skills`
- `ccp_studio.services.orchestration`
- `ccp_studio.services.agent_gateway`
- `ccp_studio.workflows.orchestration_run`
- `ccp_studio.repositories.orchestration`
- `ccp_studio.api.v1.orchestration`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `OrchestrationRun` | Top-level execution record for a brand cycle, interview session, extraction run, asset package, render job, migration run, or spec-writing run. |
| `StageExecutionPlan` | Stage choice, active object, owner, required input, allowed actions, blocked actions, and expected exit object. |
| `ValidationContract` | Pre-execution success/failure definition, thresholds, forbidden patterns, evidence requirements, and required receipts. |
| `AgentHandoffPacket` | Structured context passed to Pi, DSPy, deterministic services, workers, renderers, reviewers, or projection builders. |
| `SkillInvocationRecord` | Evidence record for migrated JIT skills, prompt layers, compiler fingerprint, critic result, synthesis result, and eval state. |
| `FailureReceipt` | Honest failure record that prevents silent advancement. |
| `FrictionReceipt` | Captures operational or UX friction introduced by an action. |
| `HumanHandoffRequest` | Typed request when taste, consent, approval, or ambiguity requires a human. |

### Technical Decisions

- Durable workflow state is operational truth for long-running orchestration, but canonical business mutation still flows through the Command Bus.
- Pi proposes and dispatches allowed actions; it does not mutate canonical state.
- Each stage must have a `ValidationContract` before a worker or agent acts.
- Every handoff must include upstream receipts and downstream proof obligations.
- Neo4j projection can support relationship inspection but cannot authorize transitions.

## 4. Implementation Plan

### Workstream A: Orchestration Contracts

Define Pydantic contracts with explicit `organization_id`, `brand_id`, `active_object_ref`, `pipeline_stage`, `allowed_actions`, `blocked_actions`, `required_receipts`, and `correlation_id`.

### Workstream B: Persistence

Add tables:

- `orchestration_runs`
- `stage_execution_plans`
- `validation_contracts`
- `agent_handoff_packets`
- `skill_invocation_records`
- `failure_receipts`
- `friction_receipts`
- `human_handoff_requests`

### Workstream C: OrchestrationRunWorkflow

Implement the durable flow:

1. Open or resume orchestration run.
2. Resolve current canonical stage from the active object and requested action.
3. Create `StageExecutionPlan`.
4. Create `ValidationContract`.
5. Dispatch through Command Bus, deterministic service, DSPy program, provider adapter, renderer, reviewer queue, or JIT skill compiler.
6. Validate returned receipt against the validation contract.
7. Advance, block, retry, compensate, quarantine, or request human handoff.

### Workstream D: Pi Agent Gateway

Expose a constrained gateway where Pi can read active objects, request valid actions, receive allowed handoff packets, submit typed commands, and return receipts. Pi cannot receive raw database credentials or bypass validation.

### Workstream E: JIT Skill Invocation Recording

Add a skill invocation recorder that stores registry snapshot, compiler fingerprint, contrastive prompt layer, critic result, synthesis result, eval state, and evidence references.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field


class StageRunStatus(str, Enum):
    opened = "opened"
    planned = "planned"
    executing = "executing"
    succeeded = "succeeded"
    failed = "failed"
    blocked = "blocked"
    waiting_for_human = "waiting_for_human"
    quarantined = "quarantined"
    compensated = "compensated"


class ActiveObjectRef(BaseModel):
    object_type: str
    object_id: UUID
    version_id: UUID | None = None


class OrchestrationRun(BaseModel):
    schema_version: Literal["cmf.orchestration_run.v1"]
    orchestration_run_id: UUID
    organization_id: UUID
    brand_id: UUID
    actor_id: UUID
    active_object: ActiveObjectRef
    requested_outcome: str
    status: StageRunStatus
    correlation_id: UUID
    opened_at: datetime
    updated_at: datetime


class StageExecutionPlan(BaseModel):
    schema_version: Literal["cmf.stage_execution_plan.v1"]
    stage_execution_plan_id: UUID
    orchestration_run_id: UUID
    pipeline_stage: str
    entry_object: ActiveObjectRef
    expected_exit_object_type: str
    allowed_actor_or_service: str
    required_inputs: list[str]
    allowed_actions: list[str]
    blocked_actions: list[str]
    downstream_proof_obligation: str
    created_at: datetime


class ValidationContract(BaseModel):
    schema_version: Literal["cmf.validation_contract.v1"]
    validation_contract_id: UUID
    stage_execution_plan_id: UUID
    success_criteria: list[str]
    failure_criteria: list[str]
    thresholds: dict[str, float] = Field(default_factory=dict)
    forbidden_skips: list[str]
    required_evidence_refs: list[str]
    required_receipt_types: list[str]


class AgentHandoffPacket(BaseModel):
    schema_version: Literal["cmf.agent_handoff_packet.v1"]
    handoff_packet_id: UUID
    orchestration_run_id: UUID
    stage_execution_plan_id: UUID
    recipient_type: str
    recipient_name: str
    active_object: ActiveObjectRef
    source_evidence_refs: list[str]
    upstream_receipt_ids: list[UUID]
    allowed_actions: list[str]
    blocked_actions: list[str]
    required_downstream_receipt: str


class SkillInvocationRecord(BaseModel):
    schema_version: Literal["cmf.skill_invocation_record.v1"]
    skill_invocation_id: UUID
    orchestration_run_id: UUID
    skill_key: str
    registry_snapshot_id: UUID
    compiler_fingerprint: str
    source_context_refs: list[str]
    contrastive_prompt_layer_refs: list[str]
    critic_result_ref: str
    synthesis_result_ref: str
    eval_state: str
    created_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `OpenOrchestrationRunCommand`, `CreateStageExecutionPlanCommand`, `RecordValidationContractCommand`, `CreateAgentHandoffPacketCommand`, `RecordSkillInvocationCommand`, `CloseStageExecutionCommand` |
| Events | `OrchestrationRunStarted`, `StageExecutionPlanCreated`, `ValidationContractRecorded`, `AgentHandoffPacketCreated`, `SkillInvocationRecorded`, `StageExecutionClosed` |
| Workflows | `OrchestrationRunWorkflow`, `ProviderJobRecoveryWorkflow`, `HumanHandoffWorkflow` |
| Receipts | `StageExecutionReceipt`, `FailureReceipt`, `FrictionReceipt`, `HumanHandoffRequest`, `QuarantineReceipt` |

## 7. Backward Compatibility and Migration Fallback

There is no untracked agent execution mode. Legacy orchestration concepts must be migrated into contracts and tests before use. If an old module can only operate by implicit prompt memory or legacy runtime coupling, it is blocked until wrapped by a JIT skill compiler or deterministic service.

Fallback behavior:

- Missing `ValidationContract` blocks execution with `VALIDATION_CONTRACT_REQUIRED`.
- Stage mismatch blocks execution with `PIPELINE_STAGE_MISMATCH`.
- Attempted self-approval blocks execution with `SELF_APPROVAL_FORBIDDEN`.
- Attempted public publishing without approval blocks execution with `PUBLICATION_APPROVAL_REQUIRED`.
- Attempted Neo4j canonical decision blocks execution with `PROJECTION_NOT_CANONICAL`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Agent autonomy wants fast local action; CMF pipeline integrity requires every action to carry stage, evidence, allowed actions, and receipt obligations. |
| UX / Ops Failure Scenario | Pi or a specialist agent jumps from extraction to rendering without source-truth receipts, causing generic assets that cannot be audited or repaired. |
| Resolution Demand | Pipeline stage authority takes precedence. Pi orchestrates the team through contracts, handoffs, and receipts instead of operating as an unconstrained executor. |
| Downstream Proof | Tests must prove missing validation blocks execution, stage skipping fails, JIT skill invocations are recorded, and successful stages cannot advance without the required receipt. |

## 9. Tasks

- Define orchestration, handoff, skill invocation, failure, friction, and human handoff Pydantic contracts.
- Add database migrations and repositories for orchestration records.
- Implement `OrchestrationRunWorkflow`.
- Implement Pi Agent Gateway allowed-action protocol.
- Integrate orchestration commands with TS-CMF-001 Command Bus.
- Implement validation of stage, object, actor, evidence, and required receipts.
- Add JIT skill invocation recorder.
- Add recovery and quarantine handlers.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | State-changing pipeline action opens or resumes `OrchestrationRun`. | Provider job starts with no orchestration record. |
| AC2 | `StageExecutionPlan` records stage, entry object, exit object, allowed actor/service, blocked actions, and downstream proof. | A renderer receives only a prompt and asset ID. |
| AC3 | `ValidationContract` exists before any worker, DSPy program, provider adapter, renderer, or workflow acts. | DSPy extraction runs before success criteria are recorded. |
| AC4 | `AgentHandoffPacket` carries active object, source evidence, upstream receipts, allowed actions, blocked actions, and required downstream receipt. | Pi hands off to a provider with no upstream evidence. |
| AC5 | JIT Skill compiler invocation stores registry snapshot, compiler fingerprint, prompt layers, critic result, synthesis result, and eval state. | Extraction skill emits candidates with no compiler record. |
| AC6 | Stage closure writes success, failure, friction, human handoff, or quarantine receipt. | Failed render disappears from dashboard with no receipt. |
| AC7 | Pi cannot skip stage, mutate canonical state directly, self-approve, publish externally, or treat Neo4j as canonical truth. | Pi approves its own generated brand context and publishes it. |

## 11. Dependencies

Internal:

- TS-CMF-001 Command Bus
- Canonical pipeline map
- Pydantic contract package
- Durable workflow runtime
- JIT skill registry
- Audit receipt writer

External:

- FastAPI
- Pydantic v2
- PostgreSQL
- Durable workflow engine selected by architecture
- DSPy
- Pi orchestration tools

## 12. Testing Strategy

Unit tests:

- Stage plan schema validation.
- Validation contract required fields.
- Agent handoff packet allowed/blocked action enforcement.
- Skill invocation record completeness.

Integration tests:

- Open run, create plan, create validation contract, hand off work, close with receipt.
- Resume run after process restart.
- Block execution when validation contract is missing.
- Quarantine provider job after repeated failure.

Safety tests:

- Pi cannot call repository write methods directly.
- Stage skipping is rejected.
- Self-approval is rejected.
- Neo4j projection result cannot authorize stage transition.

## 13. Observability, Recovery, and Rollback

- Logs must include `orchestration_run_id`, `stage_execution_plan_id`, `validation_contract_id`, `correlation_id`, `organization_id`, and `brand_id`.
- Metrics must track stage duration, blocked actions, failures, retries, human handoffs, and receipt latency.
- Recovery can resume from the last valid receipt.
- Compensation uses typed compensating commands.
- Quarantine stores ambiguous results without advancing the pipeline.

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
| Files Read Receipt | Complete |
| Requirement Trace | FR-CMF-01.06, FR-CMF-03.07, FR-CMF-10.06 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Pi extension intent and JIT skill governance mapped to Python contracts |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Pi orchestration through typed stage records and receipts |
| TypeScript Boundary | No TypeScript orchestration authority |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

