---
tech_spec_id: "TS-CMF-055"
title: "Telegram Quick Review With Evidence"
story_id: "9.6"
story_title: "Telegram Quick Review With Evidence"
epic_id: 9
epic_title: "Review, Approval, and Publishing Intent"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-9-6-telegram-quick-review-with-evidence.md"
fr_ids:
  - "FR-CMF-09.07"
pipeline_stage: "13 / 14"
entry_object: "Telegram quick action"
exit_object: "command result or PWA handoff"
validation_contract: "evidence sufficiency and idempotency"
required_receipt: "quick review receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / Telegram bot / Telegram Mini App / generated TypeScript"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-055: Telegram Quick Review With Evidence

**Status:** Ready for Development  
**Story:** `9.6 - Telegram Quick Review With Evidence`  
**Implementation Boundary:** TelegramReviewNotification, QuickActionToken, EvidenceSufficiencyDecision, Telegram webhook command routing, stale-action protection, PWA handoff, and quick review receipt.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-9-6-telegram-quick-review-with-evidence.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-09.07 authority and Telegram evidence requirements. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | PWA/Telegram operator-surface doctrine. |
| `THE CMF STUDIO/CCP V9 — Interview-First Expression Engine.md` | Telegram comes after expression and asset creation doctrine. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Telegram as operator cockpit and shared backend state source. |
| `docs/architecture.md` | Telegram Bot/Mini App, permissions, and PWA state parity. |
| `docs/cmf-studio-pipeline-map.md` | Stage 13/14 quick-review and publishing trace. |
| `docs/migration/legacy-inventory.md` | RIM feedback patterns and CBAR/receipt references. |
| `docs/tech-specs/TS-CMF-007-pwa-and-telegram-state-parity.md` | Shared state and webhook dependency. |

## 2. Overview

Telegram quick review accelerates low-risk decisions but cannot become blind rubber-stamping. Notifications must show preview, route, source snippet, consent status, evaluation summary, required action, object version, and PWA link.

When evidence is sufficient, Telegram submits the same backend command as PWA. When evidence is insufficient or conflicting, Telegram removes approval from chat and deep-links to PWA. Quick regenerate creates a revision request; it never mutates provider output directly.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-09.07 | Telegram quick approvals show enough evidence and deep-link to PWA for complex review. | Notification evidence packet, sufficiency policy, quick action token, webhook command routing, stale-action guard, PWA handoff, and quick review receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 13 - Evaluation/review and 14 - Publishing intent handoff |
| Entry Object | Telegram quick action |
| Exit Object | command result or PWA handoff |
| Validation Contract | evidence sufficiency and idempotency |
| Required Receipt | quick review receipt |

### Legacy Intelligence Mapping

- PWA/Telegram parity doctrine maps to shared backend command handling and generated contracts.
- RIM feedback patterns map to concise, evidence-bearing mobile review messages.
- V9 Telegram doctrine maps to operator utility after expression and asset creation, not client-first onboarding.
- Active primitive families FBK, FRC, and SAF shape compact feedback, low friction, and safety gates.

## 4. Implementation Plan

1. Define `TelegramReviewNotification`, `QuickActionToken`, `EvidenceSufficiencyDecision`, `TelegramQuickAction`, and `QuickReviewReceipt`.
2. Build notification summaries from `ReviewEvidenceState` and `ApprovalPolicyReport`.
3. Evaluate evidence sufficiency before exposing approve/reject/regenerate actions.
4. Route Telegram webhook submissions through the Command Bus with the same handlers as PWA.
5. Reject stale or tampered quick actions through object version, actor, role, token, and idempotency checks.
6. Convert quick regenerate into `RequestRevisionCommand`.
7. Deep-link to PWA when evidence is complex, conflicting, or incomplete.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from pydantic import BaseModel


class TelegramQuickActionType(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_REVISION = "request_revision"
    OPEN_PWA_REVIEW = "open_pwa_review"


class EvidenceSufficiencyDecision(BaseModel):
    decision_id: str
    object_id: str
    quick_actions_allowed: bool
    required_pwa_review: bool
    reasons: list[str]
    review_state_id: str
    approval_policy_report_id: str | None = None


class QuickActionToken(BaseModel):
    token_id: str
    user_id: str
    object_id: str
    object_version_hash: str
    allowed_actions: list[TelegramQuickActionType]
    expires_at: str
    idempotency_key: str


class TelegramReviewNotification(BaseModel):
    schema_version: Literal["cmf.telegram_review_notification.v1"]
    notification_id: str
    object_id: str
    preview_uri: str
    route_summary: str
    source_snippet: str
    consent_status: str
    evaluation_summary: str
    required_action: str
    pwa_review_url: str
    quick_action_token_id: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `SendTelegramReviewNotificationCommand`, `EvaluateTelegramEvidenceSufficiencyCommand`, `SubmitTelegramQuickActionCommand`, `DeepLinkToPwaReviewCommand`, `RejectStaleTelegramActionCommand`, `CreateRevisionFromTelegramRegenerateCommand` |
| Events | `TelegramReviewNotificationSent`, `TelegramEvidenceSufficiencyEvaluated`, `TelegramQuickActionSubmitted`, `PwaReviewDeepLinkIssued`, `StaleTelegramActionRejected`, `TelegramRevisionRequested` |
| Workflow | `ReviewWorkflow.stage13_telegram_quick_review` and `PublishingWorkflow.stage14_telegram_confirmation_handoff` |
| Receipt | `QuickReviewReceipt` with notification ID, token ID, actor, object version, evidence sufficiency, command result, and PWA handoff state |

## 7. Backward Compatibility and Migration Fallback

Telegram-first doctrine is not reintroduced. Telegram is an operator surface after evidence exists. If a legacy Telegram flow made hidden state changes, it must be converted to backend commands or removed. Telegram Mini App TypeScript consumes generated contracts only.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Mobile speed vs. blind approval | Quick actions require evidence sufficiency and version-bound token. | Insufficient evidence returns PWA handoff. |
| Telegram convenience vs. canonical state | Telegram calls the same backend command handlers as PWA. | QuickReviewReceipt links to command receipt. |
| Regeneration request vs. provider mutation | Quick regenerate creates revision request only. | Provider output remains immutable until workflow acts. |

## 9. Tasks

- Add Telegram review contracts.
- Implement notification builder from review evidence state.
- Implement evidence sufficiency policy.
- Add quick action token issuance and validation.
- Route webhook actions through Command Bus.
- Add stale/tamper/idempotency protection.
- Add PWA deep-link generation.
- Add quick review receipt writer.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Notification includes preview, route, source snippet, consent, evaluation summary, and required action. | Telegram message shows only thumbnail and approve button. |
| AC2 | Sufficient quick approve/reject records same backend receipt as PWA. | Telegram writes a local approval flag. |
| AC3 | Insufficient or conflicting evidence deep-links to PWA and disables approval in chat. | Telegram approves despite missing source truth. |
| AC4 | Stale object version blocks quick action. | Reviewer approves an old render after a newer revision exists. |
| AC5 | Quick regenerate creates revision request. | Telegram directly reruns provider job. |

## 11. Dependencies

- TS-CMF-005 role-based permissions.
- TS-CMF-007 PWA and Telegram state parity.
- TS-CMF-051 evidence-rich review surface.
- TS-CMF-052 review commands.
- TS-CMF-053 approval blockers.
- TS-CMF-054 Publishing Intent and Publer adapter.

## 12. Testing Strategy


Unit tests:

- Unit tests for notification and token schemas.
- Evidence sufficiency tests for quick-allowed and PWA-required cases.
- Telegram webhook auth and tamper tests.
- Idempotency and stale object version tests.
- Integration tests proving Telegram actions call the same command handlers as PWA.
- Quick regenerate tests proving revision request creation only.

Integration tests:

- Workflow test from `Telegram quick action` to `command result or PWA handoff` through pipeline stage `13 / 14`.
- Command Bus test proving `quick review receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for notifications sent, quick actions submitted, PWA handoffs, stale actions rejected, and tamper failures.
- Logs include notification ID, token ID, user ID, object ID, object version, action, and command receipt ID.
- Recovery resends notifications when object version changes and previous quick action expires.
- Rollback revokes quick action tokens and routes reviewer to PWA for current evidence state.

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
| Tech Spec ID | TS-CMF-055 |
| Story | 9.6 |
| Requirement Trace | FR-CMF-09.07 |
| Pipeline Trace | Stage 13/14, Telegram quick action to command result or PWA handoff |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No Telegram canonical state, no blind approval, no direct provider mutation from quick regenerate |
