---
tech_spec_id: "TS-CMF-032"
title: "Expression Moment Review and Boundary Control"
story_id: "6.4"
story_title: "Expression Moment Review and Boundary Control"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-6-4-expression-moment-review-and-boundary-control.md"
fr_ids:
  - "FR-CMF-06.04"
pipeline_stage: "6"
entry_object: "moment candidates"
exit_object: "approved/superseded Expression Moments"
validation_contract: "reviewer boundary gate"
required_receipt: "expression review receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / PWA review surface"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-032: Expression Moment Review and Boundary Control

**Status:** Ready for Development  
**Story:** `6.4 - Expression Moment Review and Boundary Control`  
**Implementation Boundary:** Reviewer approval/rejection, boundary fixing, split/merge, annotations, sensitivity holds, immutable approved moments, and expression review receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-6-4-expression-moment-review-and-boundary-control.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-06.04 authority and source truth review constraints. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Complete Expression Session, source-truth review, and evaluation receipt doctrine. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Expression session evaluation and route handoff rules. |
| `docs/architecture.md` | Approved Expression Moments immutability and reviewer queue. |
| `docs/cmf-studio-pipeline-map.md` | Stage 6 review boundary and evaluation context. |
| `docs/migration/legacy-inventory.md` | CBAR, receipt chain, and failure corpus references. |
| `docs/stories/story-6-4-expression-moment-review-and-boundary-control.md` | Pipeline trace and story handoff. |

## 2. Overview

Implement `ExpressionMoment` review as the human gate that turns candidates into source-truth production inputs. Reviewers can approve, reject, fix boundaries, split, merge, annotate, or place sensitivity holds. Approved moments are immutable except through supersession records.

This layer prevents the system from forcing source fragments into routes. If a moment is not truthful, bounded, dignified, and source-supported, it cannot enter routing.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-06.04 | Reviewers can approve, reject, fix boundaries, split, merge, annotate, or place sensitivity holds on Expression Moments. | Review command set, status machine, immutable approval, supersession records, sensitivity holds, and expression review receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 6 - Post-session extraction |
| Entry Object | moment candidates |
| Exit Object | approved/superseded Expression Moments |
| Validation Contract | reviewer boundary gate |
| Required Receipt | expression review receipt |

### Legacy Intelligence Mapping

- CBAR and receipt chain inform rejection reasons, sensitivity holds, and immutable review audit.
- V9.1 evaluation requires source truth, clipability, narrative density, and route readiness.
- Failure corpus patterns inform reviewer guidance but cannot approve moments automatically.

## 4. Implementation Plan

1. Add contracts for `ExpressionMoment`, `ExpressionMomentBoundary`, `ExpressionMomentReviewDecision`, `SensitivityHold`, and `ExpressionReviewReceipt`.
2. Implement review commands for approve, reject, adjust boundary, split, merge, annotate, hold, release hold, and supersede.
3. Add immutable approved moment storage; edits create supersession records.
4. Add review surface read model showing source playback refs, transcript segment, timestamp range, induction context, route rationale, and sensitivity flags.
5. Block routing for held, rejected, draft, or superseded-without-successor moments.
6. Write review receipts for every decision.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ExpressionMomentStatus(str, Enum):
    CANDIDATE = "candidate"
    APPROVED = "approved"
    REJECTED = "rejected"
    SENSITIVITY_HOLD = "sensitivity_hold"
    SUPERSEDED = "superseded"


class ExpressionMomentBoundary(BaseModel):
    source_artifact_id: str
    transcript_revision_id: str
    start_ms: int
    end_ms: int
    transcript_segment_ids: list[str] = Field(min_length=1)


class SensitivityHold(BaseModel):
    sensitivity_hold_id: str
    reason: str
    consent_record_version_id: str | None = None
    placed_by_user_id: str
    placed_at: datetime
    released_at: datetime | None = None


class ExpressionMoment(BaseModel):
    expression_moment_id: str
    source_candidate_ids: list[str]
    expression_session_id: str
    brand_id: str
    boundary: ExpressionMomentBoundary
    source_quote: str
    induction_context_ids: list[str]
    route_rationale: str
    annotations: list[str] = []
    status: ExpressionMomentStatus
    supersedes_expression_moment_ids: list[str] = []
    sensitivity_hold_id: str | None = None
    approved_at: datetime | None = None
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `ApproveExpressionMomentCommand`, `RejectExpressionMomentCommand`, `AdjustExpressionMomentBoundaryCommand`, `SplitExpressionMomentCommand`, `MergeExpressionMomentsCommand`, `PlaceSensitivityHoldCommand`, `ReleaseSensitivityHoldCommand`, `SupersedeExpressionMomentCommand` |
| Events | `ExpressionMomentApproved`, `ExpressionMomentRejected`, `ExpressionMomentBoundaryAdjusted`, `ExpressionMomentsSplit`, `ExpressionMomentsMerged`, `ExpressionMomentSensitivityHeld`, `ExpressionMomentSuperseded` |
| Workflow | `CompleteExpressionSessionWorkflow.stage6_review_expression_moments` |
| Receipt | `ExpressionReviewReceipt` with reviewer, decision, source ranges, prior/new IDs, hold state, and rationale |

## 7. Backward Compatibility and Migration Fallback

Legacy review doctrine and failure corpus inform evaluator prompts and reviewer hints. Approved moment state is greenfield canonical state. If a reviewer imports a legacy failure category, it must map to a typed rejection code before persistence.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Automation speed vs. reviewer truth | Candidates require human approval before routing. | Routing command rejects non-approved status. |
| Boundary repair vs. auditability | Boundary changes create supersession records. | Original candidate and moment remain traceable. |
| Sensitivity vs. output pressure | Holds block routing until released. | Route receipt cannot exist for held moment. |

## 9. Tasks

- Add review contracts and persistence.
- Implement command handlers and status guards.
- Add review surface read model.
- Add routing blocker for non-approved/held/superseded moments.
- Add receipt writer.
- Add tests for approve, reject, boundary, split, merge, hold, and supersession.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Review surface shows source, transcript, timestamp, context, route rationale, sensitivity. | Reviewer sees quote without source playback reference. |
| AC2 | Boundary fix preserves original candidate. | Adjusted boundary overwrites original record. |
| AC3 | Merge records both source ranges. | Merged moment loses one timestamp range. |
| AC4 | Sensitivity hold blocks routing. | Held moment receives route receipt. |
| AC5 | Approved moment immutable except supersession. | Approved source quote is edited in place. |

## 11. Dependencies

- TS-CMF-030 source ingestion/alignment.
- TS-CMF-031 candidate detection.
- TS-CMF-008 consent records.
- TS-CMF-010 consent blockers.
- TS-CMF-002 orchestration records.

## 12. Testing Strategy


Unit tests:

- Unit tests for moment status machine and boundary constraints.
- Command tests for each review action.
- Routing blocker tests for held/rejected/non-approved moments.
- Supersession tests proving old IDs remain traceable.
- UI contract tests for source playback/transcript/timestamp context.

Integration tests:

- Workflow test from `moment candidates` to `approved/superseded Expression Moments` through pipeline stage `6`.
- Command Bus test proving `expression review receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for approval rate, rejection reasons, boundary adjustments, sensitivity holds, split/merge counts, and review latency.
- Logs include reviewer ID, moment ID, session ID, receipt ID, and source range.
- Recovery: create superseding moment after boundary correction or hold release.
- Rollback: supersede erroneous approved moment and block dependent draft routes.

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
| Tech Spec ID | TS-CMF-032 |
| Story | 6.4 |
| Requirement Trace | FR-CMF-06.04 |
| Pipeline Trace | Stage 6, moment candidates to approved/superseded Expression Moments |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No routing without approval, no mutable approved moments, no sensitivity bypass |
