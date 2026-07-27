---
tech_spec_id: "TS-CMF-053"
title: "Approval Blockers"
story_id: "9.4"
story_title: "Approval Blockers"
epic_id: 9
epic_title: "Review, Approval, and Publishing Intent"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-9-4-approval-blockers.md"
fr_ids:
  - "FR-CMF-09.04"
pipeline_stage: "13"
entry_object: "approval request"
exit_object: "blocked or approved state"
validation_contract: "lineage/consent/format/evaluation gate"
required_receipt: "approval blocker receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / Command Bus / approval policy"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-053: Approval Blockers

**Status:** Ready for Development  
**Story:** `9.4 - Approval Blockers`  
**Implementation Boundary:** ApprovalGateInput, ApprovalPolicyReport, ApprovalBlocker, content-format validation, lineage completeness checks, consent compatibility, source-truth gate, and approval blocker receipt.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-9-4-approval-blockers.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-09.04 authority and blocker classes. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Full-system approval and publishing safety doctrine. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Hard-fail conditions and approval append-only rules. |
| `docs/architecture.md` | Evaluation, approval, publishing core objects and state rules. |
| `docs/cmf-studio-pipeline-map.md` | Stage 13 review and approval trace. |
| `docs/migration/legacy-inventory.md` | CBAR failure scenario resolution and V9.1 approval doctrine references. |
| `docs/tech-specs/TS-CMF-050-evaluation-receipt-generation.md` | Evaluation hard-failure dependency. |

## 2. Overview

Approval blockers prevent final approval when evidence is incomplete or unsafe. The policy checks lineage, consent, source truth, identity, evaluation, platform format, and valid content-format requirements before an approval command can succeed.

Approval blockers are explicit objects with codes, evidence refs, repair hints, and severity. They do not silently hide a button. The reviewer must see what is blocked, why it is blocked, and what command or revision can repair it.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-09.04 | Block final approval when lineage, consent, source truth, identity, evaluation, platform format, or content-format requirements fail. | ApprovalGateInput, blocker policy, content-format registry check, evaluation hard-fail enforcement, approval blocker receipt, and repair hints. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 13 - Evaluation, review, revision, approval |
| Entry Object | approval request |
| Exit Object | blocked or approved state |
| Validation Contract | lineage/consent/format/evaluation gate |
| Required Receipt | approval blocker receipt |

### Legacy Intelligence Mapping

- CBAR failure scenario resolution becomes a mandatory blocker pass before approval.
- V9.1 approval doctrine becomes a policy object rather than a reviewer memory burden.
- Active primitive families SAF, FBK, and PER shape safety priority, blocker clarity, and review pacing.

## 4. Implementation Plan

1. Define `ApprovalGateInput`, `ApprovalBlocker`, `ApprovalPolicyReport`, `ContentFormatValidation`, and `ApprovalBlockerReceipt`.
2. Implement policy checks against CompleteEditingSession, SceneSpec, ProviderReceipt, EvaluationReceipt, ConsentRecordVersion, ArchetypeRoute, RenderOutput, CaptionManifest, and platform variant.
3. Validate valid content formats from the archetype/content-format registry and reject unsupported output classes.
4. Convert missing or failing checks into named blockers with repair hints.
5. Prevent ApprovalEvent creation while any hard blocker remains active.
6. Persist blocker receipt and expose it to the evidence-rich review surface.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from pydantic import BaseModel


class ApprovalBlockerSeverity(str, Enum):
    HARD = "hard"
    SOFT = "soft"
    ESCALATE = "escalate"


class ApprovalBlocker(BaseModel):
    blocker_id: str
    code: str
    severity: ApprovalBlockerSeverity
    source_object_ref: str
    evidence_refs: list[str]
    message: str
    repair_hint: str


class ContentFormatValidation(BaseModel):
    platform_variant_id: str
    format_key: str
    valid_content_format: bool
    registry_version_id: str
    blocker_code: str | None = None


class ApprovalPolicyReport(BaseModel):
    schema_version: Literal["cmf.approval_policy_report.v1"]
    approval_request_id: str
    object_id: str
    lineage_complete: bool
    consent_compatible: bool
    source_truth_passed: bool
    identity_passed: bool
    evaluation_passed: bool
    platform_format_passed: bool
    content_format_passed: bool
    blockers: list[ApprovalBlocker]
    decision: Literal["approved_allowed", "blocked", "escalate"]
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `EvaluateApprovalGateCommand`, `BlockApprovalCommand`, `ClearApprovalBlockerCommand`, `ValidateContentFormatCommand`, `RecordApprovalBlockerReceiptCommand` |
| Events | `ApprovalGateEvaluated`, `ApprovalBlocked`, `ApprovalBlockerCleared`, `ContentFormatValidated`, `ApprovalBlockerReceiptRecorded` |
| Workflow | `ReviewWorkflow.stage13_approval_gate` |
| Receipt | `ApprovalBlockerReceipt` with request ID, blocker list, evidence refs, policy version, content-format validation, and repair hints |

## 7. Backward Compatibility and Migration Fallback

Legacy export gates and approval doctrines become blocker policies and fixtures. Old auto-export assumptions are invalid unless they can pass the new approval gate. Unsupported content formats are blocked until represented in the valid content-format registry and connected to source evidence.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Production velocity vs. release safety | Any hard blocker stops approval. | ApprovalEvent handler requires `approved_allowed` report. |
| Reviewer clarity vs. policy density | Blockers must name missing evidence and repair path. | Review surface displays blocker code, evidence, and repair hint. |
| Format ambition vs. documented formats | Only documented archetype/content formats can approve. | ContentFormatValidation cites registry version. |

## 9. Tasks

- Add approval blocker contracts.
- Implement approval gate policy.
- Add content-format registry validation.
- Integrate evaluation hard-fail blockers.
- Integrate consent and lineage checks.
- Expose blockers to review surface.
- Add receipt writer and command bus enforcement.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Incomplete lineage blocks approval and names missing lineage. | Approval succeeds without ProviderReceipt. |
| AC2 | Incompatible consent blocks approval with `CONSENT_SCOPE_BLOCKED`. | Revoked publication consent still allows approval. |
| AC3 | Missing or disputed source truth blocks approval. | Unsupported claim enters approved asset. |
| AC4 | Identity or likeness failure requires revision or rejection. | Wrong identity passes because composition looks strong. |
| AC5 | Platform or content-format failure blocks approval. | Invalid format is approved for public scheduling. |

## 11. Dependencies

- TS-CMF-008 versioned consent records.
- TS-CMF-010 consent blockers.
- TS-CMF-033 archetype and asset derivative routing.
- TS-CMF-037 SceneSpec and RenderContract.
- TS-CMF-042 provider receipts.
- TS-CMF-047 caption and platform manifests.
- TS-CMF-050 evaluation receipt generation.
- TS-CMF-052 review commands.

## 12. Testing Strategy


Unit tests:

- Unit tests for blocker severity and policy report schema.
- Integration tests for each blocker class.
- Consent compatibility tests with revoked or mismatched scope.
- Content-format registry tests with valid and invalid formats.
- ApprovalEvent negative tests proving hard blockers stop approval.

Integration tests:

- Workflow test from `approval request` to `blocked or approved state` through pipeline stage `13`.
- Command Bus test proving `approval blocker receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for approval gate evaluations, blocker codes, cleared blockers, escalations, and content-format failures.
- Logs include approval request ID, object ID, blocker codes, policy version, registry version, and reviewer ID.
- Recovery reruns approval gate after revision, consent repair, evaluation rerun, or format correction.
- Rollback cannot clear blockers silently; it writes a cleared or superseded blocker event.

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
| Tech Spec ID | TS-CMF-053 |
| Story | 9.4 |
| Requirement Trace | FR-CMF-09.04 |
| Pipeline Trace | Stage 13, approval request to blocked or approved state |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No hidden approval gate, no unsupported content format, no approval with hard blockers |
