---
tech_spec_id: "TS-CMF-048"
title: "Provider Job Retry, Resume, Cancel, and Compensation"
story_id: "8.7"
story_title: "Provider Job Retry, Resume, Cancel, and Compensation"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-8-7-provider-job-retry-resume-cancel-and-compensation.md"
fr_ids:
  - "FR-CMF-08.07"
pipeline_stage: "11 / 12"
entry_object: "failed or active provider job"
exit_object: "retry/resume/cancel/compensation state"
validation_contract: "idempotency and duplicate-cost gate"
required_receipt: "recovery receipt"
runtime_target: "Python / durable workflows / Pydantic v2 / provider adapters"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-048: Provider Job Retry, Resume, Cancel, and Compensation

**Status:** Ready for Development  
**Story:** `8.7 - Provider Job Retry, Resume, Cancel, and Compensation`  
**Implementation Boundary:** Durable provider retry/resume/cancel/compensation commands, idempotency keys, duplicate-cost guard, partial-output preservation, operational incidents, recovery actions, and recovery receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-8-7-provider-job-retry-resume-cancel-and-compensation.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-08.07 authority and durable workflow requirements. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | GPU and provider risk/cost doctrine. |
| `docs/architecture.md` | Durable workflow retry, timeout, compensation, and terminal failure state. |
| `docs/cmf-studio-pipeline-map.md` | Provider execution and learning loop boundaries. |
| `docs/migration/legacy-inventory.md` | Legacy circuit-breaker and receipt references. |

## 2. Overview

Provider failures must not corrupt completed work, duplicate cost, or create duplicate completion events. Durable workflows own provider retries, timeouts, checkpoints, cancellation, compensation, and terminal failure. Recovery commands must be idempotent and receipt-backed.

This spec applies to provider jobs, deterministic renders, GPU worker jobs, webhooks, and partial output handling.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-08.07 | Pause, retry, resume, cancel, or compensate provider jobs idempotently without corrupting completed work or losing receipts. | Recovery command set, idempotency key, duplicate-cost gate, partial-output preservation, operational incident, recovery receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 11 / 12 - Provider jobs and rendering |
| Entry Object | failed or active provider job |
| Exit Object | retry/resume/cancel/compensation state |
| Validation Contract | idempotency and duplicate-cost gate |
| Required Receipt | recovery receipt |

### Legacy Intelligence Mapping

- Legacy circuit-breaker concepts inform retry/compensation tests.
- Receipt chain remains the source of recovery truth.
- Provider webhooks and worker checkpoints are normalized into command events.

## 4. Implementation Plan

1. Add contracts for `ProviderRecoveryAction`, `ProviderJobCheckpoint`, `OperationalIncident`, `DuplicateCostRisk`, and `RecoveryReceipt`.
2. Implement pause/retry/resume/cancel/compensate commands through durable workflows.
3. Enforce idempotency keys and duplicate webhook handling.
4. Preserve completed artifacts and isolate missing work.
5. Block or escalate recovery that may duplicate billing, public publishing, or final approval side effects.
6. Attach recovery receipt to provider job and downstream artifacts.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel


class RecoveryActionType(str, Enum):
    PAUSE = "pause"
    RETRY = "retry"
    RESUME = "resume"
    CANCEL = "cancel"
    COMPENSATE = "compensate"
    ESCALATE = "escalate"


class ProviderRecoveryAction(BaseModel):
    provider_recovery_action_id: str
    provider_job_id: str
    action_type: RecoveryActionType
    idempotency_key: str
    reason: str
    duplicate_cost_risk: bool
    manual_review_required: bool = False


class RecoveryReceipt(BaseModel):
    recovery_receipt_id: str
    provider_job_id: str
    action_id: str
    preserved_output_hashes: list[str]
    requeued_work_ids: list[str]
    terminal_state: str | None = None
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `PauseProviderJobCommand`, `RetryProviderJobCommand`, `ResumeProviderJobCommand`, `CancelProviderJobCommand`, `CompensateProviderJobCommand`, `BlockDuplicateCostRecoveryCommand`, `RecordOperationalIncidentCommand` |
| Events | `ProviderJobPaused`, `ProviderJobRetried`, `ProviderJobResumed`, `ProviderJobCancelled`, `ProviderJobCompensated`, `DuplicateCostRecoveryBlocked`, `OperationalIncidentRecorded` |
| Workflow | `ProviderJobWorkflow.stage11_12_recovery` |
| Receipt | `RecoveryReceipt` with action, idempotency key, preserved outputs, requeued work, cost risk, and final state |

## 7. Backward Compatibility and Migration Fallback

Legacy retry/circuit-breaker behavior can seed recovery fixtures. New provider jobs must use durable workflow state and idempotency keys.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Fast retry vs. duplicate cost | Duplicate-cost gate blocks or escalates risky retries. | Recovery receipt records risk decision. |
| Partial output vs. corruption | Completed artifacts are preserved by hash. | Requeued work IDs exclude completed outputs. |
| Webhook duplication vs. state safety | Idempotency prevents duplicate completion events. | Duplicate webhook metric increments with no state duplicate. |

## 9. Tasks

- Add recovery contracts and persistence.
- Implement recovery command handlers.
- Add idempotency and duplicate webhook handling.
- Add duplicate-cost/public-side-effect guard.
- Add operational incident and recovery action logs.
- Add tests for retry, cancel, compensation, and duplicate events.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Timeout retries only incomplete work. | Retry reruns completed paid job. |
| AC2 | Partial output compensation preserves completed artifacts. | Compensation deletes uploaded asset. |
| AC3 | Cancel reconciles provider and canonical state by receipt. | Provider cancelled but local state remains running. |
| AC4 | Duplicate webhook creates no duplicate completion. | Two completion events emitted. |
| AC5 | Duplicate billing/publishing risk blocks or escalates. | Retry posts or bills twice. |

## 11. Dependencies

- TS-CMF-042 provider jobs.
- TS-CMF-043 deterministic rendering.
- TS-CMF-044 generative adapters.
- TS-CMF-045 GPU worker.

## 12. Testing Strategy


Unit tests:

- Unit tests for recovery actions and receipts.
- Workflow tests for retry/resume/cancel/compensate.
- Duplicate webhook/idempotency tests.
- Duplicate-cost escalation tests.
- Partial output preservation tests.

Integration tests:

- Workflow test from `failed or active provider job` to `retry/resume/cancel/compensation state` through pipeline stage `11 / 12`.
- Command Bus test proving `recovery receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for recovery actions, duplicate webhook blocks, duplicate-cost escalations, cancellations, and compensation outcomes.
- Logs include provider job ID, action ID, idempotency key, preserved outputs, and terminal state.
- Recovery is the feature: all actions create receipts.
- Rollback: issue compensating action and retain prior receipts.

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
| Tech Spec ID | TS-CMF-048 |
| Story | 8.7 |
| Requirement Trace | FR-CMF-08.07 |
| Pipeline Trace | Stages 11 / 12, failed/active provider job to recovery state |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No duplicate cost, no receipt loss, no direct webhook mutation |

