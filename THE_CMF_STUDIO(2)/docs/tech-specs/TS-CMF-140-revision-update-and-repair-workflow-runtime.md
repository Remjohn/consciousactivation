---
tech_spec_id: "TS-CMF-140"
title: "Revision, Update, and Repair Workflow Runtime"
story_id: "15.5"
story_title: "Make Revisions First-Class Factory Work"
epic_id: 15
epic_title: "Operator Operations Runtime and Agentic Control"
status: "ready-for-development"
created_at: "2026-06-26"
fr_ids:
  - "FR-CMF-06"
  - "FR-CMF-07"
  - "FR-CMF-09"
  - "FR-CMF-10"
pipeline_stage: "review, revision request, repair planning, rerun, and approval recovery"
entry_object: "RevisionRequestCommand, ReviewEvidenceState, EvaluationReceipt"
exit_object: "RepairPlan, RepairExecutionReceipt, RevisionClosureReceipt"
validation_contract: "structured target, evidence gap, primitive/doctrine blocker, rerun plan, post-repair eval, operator closure"
required_receipt: "RevisionClosureReceipt"
runtime_target: "Python / FastAPI / Pydantic v2 / Command Bus / workflows / eval harness / operator UI"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-140: Revision, Update, and Repair Workflow Runtime

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture.md` | Defines review, revision, approval, recovery, and receipt rules. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-040-revision-and-reconstruction-audit.md` | Earlier revision/reconstruction audit dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-050-evaluation-receipt-generation.md` | Eval receipt dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-052-review-commands-and-voice-dna-boost-requests.md` | Review command dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md` | Composition eval and approval blocker workflow. |
| `THE CMF STUDIO/src/ccp_studio/services/revision_service.py` | Existing revision service and command handler owner. |
| `THE CMF STUDIO/src/ccp_studio/services/review_state_service.py` | Review state owner. |
| `THE CMF STUDIO/src/ccp_studio/services/evaluation_receipt_service.py` | Eval receipt owner. |
| `THE CMF STUDIO/src/ccp_studio/services/rejection_memory_service.py` | Rejection memory owner. |
| `THE CMF STUDIO/src/ccp_studio/services/workflow_recovery_service.py` | Recovery action owner. |

## 2. Overview

Revisions are not a side conversation. In CMF Studio, revisions are production objects. The operator, Telegram quick review, Pi harness, eval harness, or provider QA can all request changes, but every revision must name what failed, what object it targets, what evidence supports the failure, which primitive/doctrine/provider/timing/source rule was violated, and what repair workflow should happen next.

This spec builds the runtime that turns "fix this" into a structured repair loop. A revision request becomes a `RepairPlan`; the plan selects owner service, affected stage, rerun requirements, provider limits, eval gates, and operator approval path. Repair execution emits receipts and must rerun the relevant evals before the object can return to review. Rejection memory records repeated failure patterns without allowing stale failures to poison unrelated guests.

This is the answer to "what if there are edits or updates or revisions": the system does not patch artifacts casually; it runs a governed repair workflow.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-140-001 | `RevisionRequestCommand` | Structured command from UI, Telegram, eval, agent, or workflow. |
| DEP-CMF-140-002 | `RepairPlan` | Stage-specific plan with owner, target, steps, blockers, and rerun requirements. |
| DEP-CMF-140-003 | `RepairExecutionReceipt` | Receipt for each repair attempt. |
| DEP-CMF-140-004 | `RevisionClosureReceipt` | Final accepted, blocked, rejected, or superseded closure receipt. |
| DEP-CMF-140-005 | `RejectionMemoryEntry` | Scoped learning from repeated failures. |
| DEP-CMF-140-006 | `RevisionReadModel` | Operator-visible repair state. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `services/revision_service.py` | Build repair plans and manage revision lifecycle. |
| `services/workflow_recovery_service.py` | Execute recoverable stage repairs. |
| `services/rejection_memory_service.py` | Store repeated failure patterns. |
| `services/evaluation_receipt_service.py` | Trigger rerun evals after repair. |
| `api/v1/operator_ui.py` | Submit revision commands and load revision read model. |
| `api/v1/telegram_review.py` | Convert quick-review revision to structured request. |

### ADR-05 Primitive Implementation

If a revision is caused by primitive failure, the repair target must reference the primitive role and expected expression repair. A revision cannot say only "bad composition." It must say, for example, `delivery_shape primitive missing: route SV-EDU lacks teaching diagram layer`.

### CBAR Mandate Enforcement

| CBAR Mandate | Implementation Rule |
|---|---|
| Phase4-M05 Actionable Rejection | Revision request requires failure category, repair target, and next action. |
| Phase4-M04 Frictionless Block | Hard blockers route to repair plan instead of disabled approval only. |
| Phase5-M01 Verifiable Artifact | Repair execution and closure receipts prove what changed. |

## 4. PRD and FR-CMF Requirement Trace

| Requirement | Implementation Meaning |
|---|---|
| FR-CMF-06 | Expression and asset routing revisions preserve source lineage. |
| FR-CMF-07 | Scene, composition, timing, and render revisions are reconstructable. |
| FR-CMF-09 | Eval, review, approval, and publishing revisions require receipts and blockers. |
| FR-CMF-10 | Recovery and rejection memory close the loop. |

## 5. Canonical Pipeline Stage Trace

| Stage | Repair Examples |
|---|---|
| Research | Missing Context Premise evidence or weak CRAL source. |
| Interview Brief | Question not grounded in guest DNA or audience premise. |
| Extraction | Candidate moment lacks transcript evidence or Emotional DNA fit. |
| Routing | Wrong asset format or archetype route. |
| Composition | Wrong visual feel, missing primitive triad, timing mismatch. |
| Render | Caption overflow, render hash mismatch, provider artifact issue. |
| Review | Missing eval receipt, approval blocker, stale evidence. |

## 6. Greenfield Integration and Legacy Migration Context

Legacy revision prompts and audit protocols can become repair templates, but production repair plans must use CMF contracts and current project paths only.

## 7. Architecture Component Map

| Component | Owner | Responsibility |
|---|---|---|
| `RevisionService` | Backend | Own revision lifecycle. |
| `RepairPlanner` | Backend | Map failure categories to repair steps. |
| `RepairExecutor` | Workflow | Invoke stage service, provider rerun, or eval rerun. |
| `RevisionReadModelProjector` | Projection | Feed UI and Telegram state. |
| `RejectionMemoryService` | Backend | Record scoped learning. |

## 8. Implementation Plan

1. Extend revision contracts with target type, failure category, evidence refs, primitive refs, doctrine refs, expected repair, and severity.
2. Add repair plan compiler in `RevisionService`.
3. Add repair target enum: `source`, `research`, `interview_brief`, `extraction`, `route`, `composition_json`, `layer_asset`, `timing`, `caption`, `audio`, `render`, `eval`, and `approval`.
4. Add workflow activity to execute repair plan and record receipts.
5. Rerun required evals before returning object to review.
6. Update operator UI with revision lane: requested, planned, repairing, reevaluating, ready for review, closed, blocked.
7. Update Telegram quick review to request revisions but require PWA for complex repair detail.

## 9. Primary Pydantic Output Schema

```python
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field

RepairTarget = Literal["source", "research", "interview_brief", "extraction", "route", "composition_json", "layer_asset", "timing", "caption", "audio", "render", "eval", "approval"]

class RevisionRequestCommand(BaseModel):
    schema_version: Literal["cmf.revision_request_command.v1"] = "cmf.revision_request_command.v1"
    command_id: UUID
    brand_workspace_id: UUID
    guest_id: UUID | None = None
    target_object_type: str
    target_object_id: UUID
    repair_target: RepairTarget
    failure_category: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    primitive_refs: list[str] = Field(default_factory=list)
    doctrine_refs: list[str] = Field(default_factory=list)
    expected_repair: str = Field(min_length=1)

class RepairPlan(BaseModel):
    schema_version: Literal["cmf.repair_plan.v1"] = "cmf.repair_plan.v1"
    repair_plan_id: UUID
    revision_command_id: UUID
    owner_service: str
    steps: list[dict]
    required_eval_reruns: list[str] = Field(default_factory=list)
    approval_required: bool = True
    blocker_codes: list[str] = Field(default_factory=list)

class RevisionClosureReceipt(BaseModel):
    schema_version: Literal["cmf.revision_closure_receipt.v1"] = "cmf.revision_closure_receipt.v1"
    receipt_id: UUID
    repair_plan_id: UUID
    status: Literal["accepted", "blocked", "rejected", "superseded"]
    repair_receipt_ids: list[UUID] = Field(default_factory=list)
    eval_receipt_ids: list[UUID] = Field(default_factory=list)
    closed_at: datetime
```

## 10. Commands, Events, Workflows, and Receipts

| Object | Requirement |
|---|---|
| `RevisionRequestCommand` | Entry for every edit, update, or revision. |
| `RepairPlan` | Required before repair execution. |
| `RepairExecutionReceipt` | Required per executed step. |
| `RevisionClosureReceipt` | Required before returning to approved/exportable state. |
| `revision.requested` | Event from UI, Telegram, eval, or agent. |
| `revision.closed` | Event after accepted or blocked outcome. |

## 11. DSPy Programs, JIT Skills, or Deterministic Services

Repair plans may invoke JIT skills for interview brief repair, extraction repair, narrative induction repair, or composition prompt repair, but all outputs must be validated and receipted. Deterministic repairs are preferred for timing, captions, object references, and render prop corrections.

## 12. Provider, Renderer, Projection, or Worker Boundaries

Provider reruns must use provider job receipts and must not overwrite old artifacts in place. Render repairs create new render outputs with lineage to the failed output.

## 13. CBAR Constraint Pass

| Constraint | Pass Condition |
|---|---|
| Tension | Operators need fast fixes; production needs reconstructable repairs. |
| Failure Scenario | Operator says "remove this part" and the render changes with no lineage. |
| Resolution Demand | Structured revision command and repair plan create receipts. |
| Downstream Proof | Review read model shows before/after, eval reruns, and closure receipt. |

## 14. Acceptance Criteria with Failure Examples

| AC | Acceptance Criteria | Failure Example | CBAR |
|---|---|---|---|
| AC140-01 | Every revision names target object and repair target. | Generic `fix asset` command accepted. | Phase4-M05 |
| AC140-02 | Repair plan is created before repair execution. | Service reruns provider immediately from UI button. | Phase5-M01 |
| AC140-03 | Eval reruns are required for eval-caused revisions. | Primitive failure repaired without primitive rerun. | Phase4-M04 |
| AC140-04 | Repaired artifacts preserve failed artifact lineage. | Old preview overwritten. | Phase5-M01 |
| AC140-05 | Rejection memory is scoped by guest/workspace/failure class. | Claude failure poisons Adele routes. | Phase1-M05 |

## 15. Dependencies

| Dependency | Required Before Build |
|---|---|
| TS-CMF-040 | Revision and reconstruction audit. |
| TS-CMF-050 | Evaluation receipts. |
| TS-CMF-052 | Review commands. |
| TS-CMF-060 | Workflow recovery. |
| TS-CMF-136 | UI command binding. |
| TS-CMF-137 | Production command handler wiring. |

## 16. Testing Strategy

| Test Type | Required Tests |
|---|---|
| Unit | Revision command validation rejects missing target/evidence. |
| Unit | Repair planner maps failure category to owner service. |
| Integration | Revision command to repair plan to repair receipt to eval rerun to closure receipt. |
| Negative | Approval blocked until revision closure. |
| UI | Revision lane shows status and next action. |

## 17. Observability, Recovery, and Rollback

1. Store before/after artifact refs for each repair.
2. Allow repair plan cancellation with receipt.
3. If repair fails, route to recovery service with blockers.
4. Rollback by restoring previous approved version, not by deleting failed artifacts.

## 18. Spec Audit Receipt

| Field | Value |
|---|---|
| Spec id | TS-CMF-140 |
| Protocol | CMF/ERA3 18-section spec |
| Revision as first-class object | Yes |
| Repair receipts | Required |
| Eval rerun | Required where relevant |
| Status | ready-for-development |
