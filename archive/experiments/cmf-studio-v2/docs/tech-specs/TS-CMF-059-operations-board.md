---
tech_spec_id: "TS-CMF-059"
title: "Operations Board"
story_id: "10.4"
story_title: "Operations Board"
epic_id: 10
epic_title: "Evidence Memory, Neo4j Projection, and Recovery"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-10-4-operations-board.md"
fr_ids:
  - "FR-CMF-10.05"
pipeline_stage: "operations overlay"
entry_object: "queues/incidents/jobs"
exit_object: "operations board state"
validation_contract: "canonical-state-only reads"
required_receipt: "operations receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / generated TypeScript / PWA operations board"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-059: Operations Board

**Status:** Ready for Development  
**Story:** `10.4 - Operations Board`  
**Implementation Boundary:** OperationsBoardState, queue depth, worker status, provider status, workflow checkpoints, retry state, costs, blockers, projection health, recovery recommendations, and operations receipt.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-10-4-operations-board.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-10.05 authority and operations visibility requirements. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Operational readiness and high-velocity operator doctrine. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Provider cost/performance and operational tasks. |
| `docs/architecture.md` | memory_ops tables, failure taxonomy, and operations service target. |
| `docs/cmf-studio-pipeline-map.md` | Operations overlay and Pi recovery context. |
| `docs/migration/legacy-inventory.md` | Circuit-breaker and operations references. |
| `docs/tech-specs/TS-CMF-048-provider-job-retry-resume-cancel-and-compensation.md` | Provider recovery dependency. |

## 2. Overview

The Operations Board lets Operators run CMF STUDIO without hidden scripts or manual database edits. It shows queue depth, active workers, GPU tier, provider status, workflow checkpoints, retry state, costs, consent blockers, approval blockers, publish readiness, memory blockers, projection health, and recommended recovery actions.

The board is read-only for state inspection. Any action it exposes must call typed backend commands and produce receipts. TypeScript renders generated contracts; Python owns the read model, policy, and command routing.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-10.05 | Operators can inspect queue depth, active workers, render tier, provider status, failed jobs, retry state, workflow checkpoints, cost receipts, consent blockers, approval blockers, publish readiness, and memory blockers. | Operations read model, board state, blocker links, provider/worker/cost snapshots, incident summaries, recovery recommendations, and operations receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | operations overlay |
| Entry Object | queues/incidents/jobs |
| Exit Object | operations board state |
| Validation Contract | canonical-state-only reads |
| Required Receipt | operations receipt |

### Legacy Intelligence Mapping

- Legacy circuit-breaker references become visible incident and recovery recommendations.
- Receipt-chain doctrine becomes board-level links back to receipts and blockers.
- Active primitive families FBK, BUS, FRC, and SAF govern feedback visibility, business cost awareness, low-friction operation, and safety.

## 4. Implementation Plan

1. Define `OperationsBoardState`, `QueueSnapshot`, `WorkerStatusSnapshot`, `ProviderStatusSnapshot`, `CostSnapshot`, `BlockerSummary`, `IncidentSummary`, and `OperationsReceipt`.
2. Implement read model from provider jobs, operational incidents, recovery actions, workflow checkpoints, cost receipts, consent blockers, approval blockers, publishing intents, memory events, and projection health.
3. Link each blocker or failure to exact object, receipt, and allowed recovery command.
4. Add worker drain and GPU cost visibility.
5. Add provider outage view with affected jobs, completed artifacts, safe retries, costs, blockers, and recommendations.
6. Prevent manual database-edit actions; all actions route to command endpoints.

## 5. Primary Output Schema

```python
from typing import Literal
from pydantic import BaseModel


class QueueSnapshot(BaseModel):
    queue_name: str
    depth: int
    active_count: int
    failed_count: int
    oldest_job_age_seconds: int | None = None


class WorkerStatusSnapshot(BaseModel):
    worker_id: str
    worker_type: str
    status: Literal["idle", "running", "draining", "failed", "offline"]
    gpu_tier: str | None = None
    active_job_ids: list[str]
    current_cost_estimate_usd: float | None = None


class BlockerSummary(BaseModel):
    blocker_type: Literal["consent", "approval", "publishing", "memory", "projection"]
    blocker_code: str
    object_ref: str
    receipt_id: str
    required_action: str


class OperationsBoardState(BaseModel):
    schema_version: Literal["cmf.operations_board_state.v1"]
    board_state_id: str
    organization_id: str
    brand_id: str | None = None
    queues: list[QueueSnapshot]
    workers: list[WorkerStatusSnapshot]
    blockers: list[BlockerSummary]
    provider_statuses: list[str]
    incident_ids: list[str]
    projection_health: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `BuildOperationsBoardStateCommand`, `RefreshOperationsBoardCommand`, `LinkBlockerToObjectCommand`, `RecommendRecoveryActionCommand`, `RecordOperationsReceiptCommand` |
| Events | `OperationsBoardStateBuilt`, `OperationsBoardRefreshed`, `BlockerLinkedToObject`, `RecoveryActionRecommended`, `OperationsReceiptRecorded` |
| Workflow | `OperationsWorkflow.overlay_board_state` |
| Receipt | `OperationsReceipt` with board state ID, source query snapshot, blocker count, incident count, cost summary, projection health, and recommended recovery actions |

## 7. Backward Compatibility and Migration Fallback

Legacy operations scripts are not invoked by the board. If a legacy runbook is still useful, convert it into a typed recovery command or readiness check. Unsupported manual operations remain documentation only until converted.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Operator speed vs. state safety | Board is read model plus command links only. | No manual database edit action exists. |
| Incident visibility vs. overwhelm | Board groups queues, blockers, incidents, costs, and recovery recommendations. | OperationsReceipt captures summary counts and links. |
| Provider outage vs. duplicate work | Completed artifacts and safe retries are visible before action. | Recovery command requires state and receipt validation. |

## 9. Tasks

- Add operations board contracts.
- Implement operations read model service.
- Add blocker and incident linking.
- Add provider/worker/cost snapshots.
- Add projection health summary.
- Add recovery recommendations.
- Add PWA operations board contract and view.
- Add operations receipt writer.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Board shows queues, workers, GPU tier, provider status, checkpoints, retries, costs, blockers. | Operator must inspect logs manually. |
| AC2 | Provider outage shows affected jobs, completed artifacts, safe retries, costs, blockers, and actions. | Board only says provider down. |
| AC3 | Consent or approval blocker links to object and decision required. | Blocker appears with no repair path. |
| AC4 | Draining worker shows shutdown status and final cost. | GPU worker disappears after queue drains. |
| AC5 | Resolved incident history and receipts remain visible. | Incident vanishes after recovery. |

## 11. Dependencies

- TS-CMF-010 consent blockers.
- TS-CMF-042 provider capability registry.
- TS-CMF-045 ComfyUI GPU worker.
- TS-CMF-048 provider recovery.
- TS-CMF-053 approval blockers.
- TS-CMF-054 Publishing Intent.
- TS-CMF-058 Neo4j projection.

## 12. Testing Strategy


Unit tests:

- Unit tests for operations board schemas.
- Read model integration tests across queues, workers, provider jobs, incidents, costs, blockers, and projection health.
- Authorization tests for organization/brand scoping.
- Provider outage fixture tests.
- Worker draining and cost reporting tests.
- Negative tests proving board actions route to command handlers only.

Integration tests:

- Workflow test from `queues/incidents/jobs` to `operations board state` through pipeline stage `operations overlay`.
- Command Bus test proving `operations receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for board refresh latency, queue depths, active workers, provider failures, blocker counts, incident counts, and projected spend.
- Logs include board state ID, organization ID, brand ID, incident IDs, blocker codes, and recovery recommendations.
- Recovery rebuilds board state from canonical tables and receipts.
- Rollback clears cached board state only; canonical events and receipts remain unchanged.

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
| Tech Spec ID | TS-CMF-059 |
| Story | 10.4 |
| Requirement Trace | FR-CMF-10.05 |
| Pipeline Trace | Operations overlay, queues/incidents/jobs to operations board state |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No hidden scripts, no manual database edits, no state mutation from read model |
