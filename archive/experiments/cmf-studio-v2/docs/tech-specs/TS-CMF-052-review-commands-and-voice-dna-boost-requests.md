---
tech_spec_id: "TS-CMF-052"
title: "Review Commands and Voice-DNA Boost Requests"
story_id: "9.3"
story_title: "Review Commands and Voice-DNA Boost Requests"
epic_id: 9
epic_title: "Review, Approval, and Publishing Intent"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-9-3-review-commands-and-voice-dna-boost-requests.md"
fr_ids:
  - "FR-CMF-09.03"
pipeline_stage: "13"
entry_object: "reviewer decision"
exit_object: "review command or approval event"
validation_contract: "role/evidence/voice eligibility"
required_receipt: "review decision receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / Command Bus / ReviewWorkflow"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-052: Review Commands and Voice-DNA Boost Requests

**Status:** Ready for Development  
**Story:** `9.3 - Review Commands and Voice-DNA Boost Requests`  
**Implementation Boundary:** ReviewDecision, RevisionRequest, ApprovalEvent, ManualEscalation, RequestVoiceDnaBoost, command policy, evidence binding, and append-only review decision receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-9-3-review-commands-and-voice-dna-boost-requests.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-09.03 authority and review command requirements. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Voice DNA, human approval, and no direct publishing doctrine. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Approval event, revision, and hard-fail source. |
| `docs/architecture.md` | ReviewDecision, RevisionRequest, ApprovalEvent, and command bus patterns. |
| `docs/cmf-studio-pipeline-map.md` | Stage 13 review and approval flow. |
| `docs/migration/legacy-inventory.md` | Legacy receipt chain, Voice DNA doctrine, and CBAR. |
| `docs/tech-specs/TS-CMF-011-voice-dna-boost-eligibility-and-audio-classification.md` | Voice-DNA Boost eligibility dependency. |

## 2. Overview

Review decisions are state transitions, not UI clicks. Approve, reject, request revision, escalate, and request Voice-DNA Boost must all enter the Command Bus with actor, role, evidence state, object version, evaluation receipt IDs, source references, and idempotency key.

Voice-DNA Boost remains a narrow structural repair exception. A reviewer can request it only when eligibility, consent, duration, claim, visual-covering, and evidence rules pass. Approval events are append-only and cannot erase prior review decisions.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-09.03 | Reviewers can approve, reject, request revisions, escalate for manual review, or request eligible Voice-DNA Boost through governed commands. | Typed review commands, role checks, evidence binding, voice eligibility gate, revision request schema, approval event, and review decision receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 13 - Evaluation, review, revision, approval |
| Entry Object | reviewer decision |
| Exit Object | review command or approval event |
| Validation Contract | role/evidence/voice eligibility |
| Required Receipt | review decision receipt |

### Legacy Intelligence Mapping

- Legacy receipt-chain doctrine maps to append-only review decision receipts.
- Voice DNA doctrine maps to `RequestVoiceDnaBoostCommand` guardrails.
- CBAR maps to explicit review tension and downstream proof in every decision.
- Active primitive families FBK, SAF, and VOC govern repair clarity, safety, and voice continuity.

## 4. Implementation Plan

1. Define `ReviewDecision`, `RevisionRequest`, `ManualEscalation`, `ApprovalEvent`, `VoiceDnaBoostRequest`, and `ReviewDecisionReceipt`.
2. Implement command handlers for approve, reject, request revision, escalate, and request Voice-DNA Boost.
3. Validate role, object version, evidence state, evaluation receipt IDs, consent state, and lineage before state transition.
4. Route Voice-DNA Boost requests through existing eligibility policy and audio classification contracts.
5. Persist append-only events and receipts.
6. Notify Production Steward of revision or escalation with exact evidence and repair target.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from pydantic import BaseModel


class ReviewDecisionType(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_REVISION = "request_revision"
    ESCALATE = "escalate"
    REQUEST_VOICE_DNA_BOOST = "request_voice_dna_boost"


class RevisionRequest(BaseModel):
    revision_request_id: str
    object_id: str
    failure_category: str
    evidence_refs: list[str]
    expected_repair: str
    requested_by_user_id: str


class ApprovalEvent(BaseModel):
    schema_version: Literal["cmf.approval_event.v1"]
    approval_event_id: str
    object_type: str
    object_id: str
    reviewer_user_id: str
    evidence_state_id: str
    evaluation_receipt_ids: list[str]
    source_refs: list[str]
    created_at: str


class VoiceDnaBoostRequest(BaseModel):
    request_id: str
    object_id: str
    source_gap_ref: str
    eligibility_report_id: str
    requested_by_user_id: str
    evidence_refs: list[str]
    structural_repair_reason: str


class ReviewDecisionReceipt(BaseModel):
    receipt_id: str
    decision_type: ReviewDecisionType
    command_id: str
    object_version_hash: str
    result_state: str
    blocker_codes: list[str]
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `ApproveAssetCommand`, `RejectAssetCommand`, `RequestRevisionCommand`, `EscalateManualReviewCommand`, `RequestVoiceDnaBoostCommand`, `RecordReviewDecisionReceiptCommand` |
| Events | `AssetApproved`, `AssetRejected`, `RevisionRequested`, `ManualReviewEscalated`, `VoiceDnaBoostRequested`, `ReviewDecisionReceiptRecorded` |
| Workflow | `ReviewWorkflow.stage13_apply_review_decision` |
| Receipt | `ReviewDecisionReceipt` with actor, role, object version, evidence state, evaluation receipts, blocker outcome, and resulting state |

## 7. Backward Compatibility and Migration Fallback

Legacy review commands and voice repair conventions are migrated as policy fixtures and evals. Any old shortcut that edits audio or render output directly must be replaced with a revision request or governed Voice-DNA Boost command.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Reviewer speed vs. auditability | Every decision is a typed command with receipt. | ApprovalEvent includes actor, source refs, and evaluation IDs. |
| Voice repair vs. source truth | Voice-DNA Boost requires eligibility and cannot carry primary claims. | Failed eligibility returns violated rule and blocks command. |
| Reversibility vs. approval authority | Approvals are append-only; revisions supersede outputs, not history. | Review history remains visible in TS-CMF-051. |

## 9. Tasks

- Add review decision contracts.
- Implement approve, reject, revision, escalation, and voice boost command handlers.
- Add role and evidence policy checks.
- Integrate Voice-DNA Boost eligibility.
- Write append-only decision receipts.
- Add Production Steward notification for revisions.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Every review action writes typed command and receipt. | PWA button flips status directly. |
| AC2 | Voice-DNA Boost request fails with violated rule when ineligible. | Synthetic bridge is requested as convenience rewrite. |
| AC3 | Revision request includes evidence, failure category, and repair target. | Production Steward receives "make it better." |
| AC4 | Escalation follows state policy and records blocked or ready state. | Escalated asset remains silently approval-ready. |
| AC5 | ApprovalEvent includes actor, evidence, source refs, and evaluation IDs. | Approval event stores only reviewer name and timestamp. |

## 11. Dependencies

- TS-CMF-005 role-based permissions.
- TS-CMF-011 Voice-DNA Boost eligibility.
- TS-CMF-012 consent and source review.
- TS-CMF-047 audio, caption, timeline, and mix assembly.
- TS-CMF-050 evaluation receipt generation.
- TS-CMF-051 evidence-rich review state.

## 12. Testing Strategy


Unit tests:

- Unit tests for review command schemas and state transitions.
- Policy tests for role, object version, evidence, consent, and evaluation receipt requirements.
- Voice-DNA Boost eligibility rejection tests.
- Integration tests from review evidence state to approval event.
- Idempotency tests for duplicate review command submission.

Integration tests:

- Workflow test from `reviewer decision` to `review command or approval event` through pipeline stage `13`.
- Command Bus test proving `review decision receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for approvals, rejections, revision requests, escalations, voice boost requests, and blocked commands.
- Logs include command ID, actor ID, object ID, evidence state ID, decision type, and blocker codes.
- Recovery replays command receipts to rebuild review state.
- Rollback creates corrective review events or revision requests; approval history is never deleted.

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
| Tech Spec ID | TS-CMF-052 |
| Story | 9.3 |
| Requirement Trace | FR-CMF-09.03 |
| Pipeline Trace | Stage 13, reviewer decision to review command or approval event |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No direct status flip, no voice convenience rewrite, no mutable approval history |
