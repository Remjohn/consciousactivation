---
tech_spec_id: "TS-CMF-060"
title: "Workflow Recovery Actions"
story_id: "10.5"
story_title: "Workflow Recovery Actions"
epic_id: 10
epic_title: "Evidence Memory, Neo4j Projection, and Recovery"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-10-5-workflow-recovery-actions.md"
fr_ids:
  - "FR-CMF-10.06"
pipeline_stage: "operations overlay"
entry_object: "failed workflow/job"
exit_object: "RecoveryAction"
validation_contract: "idempotent safe-action validation"
required_receipt: "recovery receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / durable workflows / operations service"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-060: Workflow Recovery Actions

**Status:** Ready for Development  
**Story:** `10.5 - Workflow Recovery Actions`  
**Implementation Boundary:** RecoveryAction, OperationalIncident, workflow checkpoint analysis, safe retry/resume/cancel/compensate/quarantine commands, idempotency guard, and recovery receipt.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-10-5-workflow-recovery-actions.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-10.06 authority and recovery action list. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Pi orchestration, provider outage, and readiness doctrine. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Recovery, durable workflow, and failure handling source. |
| `docs/architecture.md` | Failure taxonomy, RecoveryAction, OperationalIncident, and workflow rules. |
| `docs/cmf-studio-pipeline-map.md` | DamageControl interpretation and recovery loop. |
| `docs/migration/legacy-inventory.md` | Receipt chain and CBAR failure handling doctrine. |
| `docs/tech-specs/TS-CMF-048-provider-job-retry-resume-cancel-and-compensation.md` | Provider job recovery dependency. |
| `docs/tech-specs/TS-CMF-059-operations-board.md` | Operations board recovery recommendation source. |

## 2. Overview

Workflow recovery lets Operators retry, resume, cancel, compensate, or quarantine failed provider jobs and workflows without corrupting completed work, duplicating external side effects, or losing receipts. Durable workflows own recovery semantics; the Operations Board exposes safe actions.

Every recovery action must be idempotent, state-derived, receipt-backed, and aware of completed artifacts, workflow checkpoints, consent compatibility, publishing side effects, memory side effects, and provider costs.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-10.06 | Retry, resume, cancel, compensate, or quarantine provider jobs and workflows idempotently without losing completed work or corrupting receipts. | RecoveryAction contracts, safe-action validator, checkpoint analysis, completed artifact preservation, duplicate side-effect blocker, quarantine command, and recovery receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | operations overlay |
| Entry Object | failed workflow/job |
| Exit Object | `RecoveryAction` |
| Validation Contract | idempotent safe-action validation |
| Required Receipt | recovery receipt |

### Legacy Intelligence Mapping

- Receipt-chain doctrine becomes required pre/post recovery evidence.
- CBAR failure handling maps to state-derived safe actions and downstream proof.
- Active primitive families SAF and FBK govern safety-first recovery and clear operator feedback.

## 4. Implementation Plan

1. Define `RecoveryAction`, `RecoveryActionType`, `RecoveryValidationReport`, `OperationalIncident`, `RecoveryReceipt`, and `QuarantineScope`.
2. Analyze workflow checkpoints, completed artifacts, receipts, provider state, consent compatibility, publishing state, and memory state before offering actions.
3. Implement retry, resume, cancel, compensate, and quarantine commands.
4. Block actions that duplicate external calls, public scheduling, billing, approval, or memory effects.
5. Preserve completed artifacts and receipts during retry/resume.
6. Record incident and recovery receipt for every action.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from pydantic import BaseModel


class RecoveryActionType(str, Enum):
    RETRY = "retry"
    RESUME = "resume"
    CANCEL = "cancel"
    COMPENSATE = "compensate"
    QUARANTINE = "quarantine"


class RecoveryValidationReport(BaseModel):
    report_id: str
    workflow_id: str
    failed_object_ref: str
    safe_actions: list[RecoveryActionType]
    blocked_actions: list[str]
    completed_artifact_refs: list[str]
    duplicate_side_effect_risks: list[str]
    consent_compatible: bool


class RecoveryAction(BaseModel):
    schema_version: Literal["cmf.recovery_action.v1"]
    recovery_action_id: str
    incident_id: str
    action_type: RecoveryActionType
    idempotency_key: str
    validation_report_id: str
    requested_by_user_id: str
    reason: str


class RecoveryReceipt(BaseModel):
    receipt_id: str
    recovery_action_id: str
    preserved_artifact_refs: list[str]
    requeued_work_refs: list[str]
    quarantined_refs: list[str]
    terminal_state: str | None = None
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `BuildRecoveryValidationReportCommand`, `RetryWorkflowCommand`, `ResumeWorkflowCommand`, `CancelWorkflowCommand`, `CompensateWorkflowCommand`, `QuarantineWorkflowArtifactsCommand`, `RecordRecoveryReceiptCommand` |
| Events | `RecoveryValidationReportBuilt`, `WorkflowRetried`, `WorkflowResumed`, `WorkflowCancelled`, `WorkflowCompensated`, `WorkflowArtifactsQuarantined`, `RecoveryReceiptRecorded` |
| Workflow | `OperationsWorkflow.recover_failed_workflow` |
| Receipt | `RecoveryReceipt` with action, idempotency key, preserved artifacts, requeued work, quarantined refs, terminal state, and duplicate-side-effect assessment |

## 7. Backward Compatibility and Migration Fallback

Legacy manual recovery runbooks are not executed directly. Useful recovery logic must be converted into safe-action validators and typed commands. If a failure has no safe command, it creates a human handoff request and quarantine state rather than a manual database edit.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Fast recovery vs. duplicate external effects | Safe-action validation blocks duplicate provider, billing, publishing, approval, or memory effects. | Recovery receipt records duplicate-risk assessment. |
| Retry completion vs. artifact preservation | Retry only incomplete work and preserve completed artifacts. | Receipt lists preserved and requeued refs. |
| Routine failure vs. hidden manual repair | All recovery actions are typed commands. | Operations Board exposes command links, not scripts. |

## 9. Tasks

- Add recovery contracts and persistence.
- Implement recovery validation report builder.
- Implement retry, resume, cancel, compensate, and quarantine commands.
- Integrate provider job recovery from TS-CMF-048.
- Add duplicate side-effect blocker.
- Add operational incident linking.
- Add recovery receipt writer.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Recovery view derives safe actions from state, completed artifacts, receipts, and consent. | Operator sees generic retry button only. |
| AC2 | Safe retry retries incomplete work only. | Retry deletes completed artifact and regenerates it. |
| AC3 | Cancel records terminal or compensated state with receipt. | Workflow is stopped with no terminal event. |
| AC4 | Quarantine blocks affected assets, memory, provider jobs, or publishing intents. | Quarantined artifact remains selectable. |
| AC5 | Corrupting or duplicate action is blocked. | Recovery resubmits a public schedule or bills twice. |

## 11. Dependencies

- TS-CMF-002 pipeline stage records.
- TS-CMF-042 provider capability registry.
- TS-CMF-048 provider job recovery.
- TS-CMF-054 Publishing Intent.
- TS-CMF-056 memory admission.
- TS-CMF-057 memory governance.
- TS-CMF-059 operations board.

## 12. Testing Strategy


Unit tests:

- Unit tests for recovery action and validation report schemas.
- Safe-action tests for retry, resume, cancel, compensate, and quarantine.
- Duplicate side-effect tests across provider, publishing, approval, and memory actions.
- Artifact preservation integration tests.
- Incident linking and receipt tests.
- Idempotency tests for repeated recovery submissions.

Integration tests:

- Workflow test from `failed workflow/job` to `RecoveryAction` through pipeline stage `operations overlay`.
- Command Bus test proving `recovery receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for incidents, safe actions offered, actions submitted, blocked actions, quarantines, compensation, and repeated idempotency keys.
- Logs include incident ID, recovery action ID, workflow ID, checkpoint ID, idempotency key, action type, and duplicate-risk list.
- Recovery recovers itself by replaying idempotent recovery receipts.
- Rollback uses compensation or quarantine; it never deletes recovery history.

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
| Tech Spec ID | TS-CMF-060 |
| Story | 10.5 |
| Requirement Trace | FR-CMF-10.06 |
| Pipeline Trace | Operations overlay, failed workflow/job to RecoveryAction |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No unsafe retry, no duplicate external side effect, no manual recovery script |
