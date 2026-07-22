---
tech_spec_id: "TS-CMF-141"
title: "Telegram Bot, Mini App, and PWA Handoff Integration"
story_id: "15.6"
story_title: "Complete the Telegram Operations Surface"
epic_id: 15
epic_title: "Operator Operations Runtime and Agentic Control"
status: "ready-for-development"
created_at: "2026-06-26"
fr_ids:
  - "FR-CMF-01"
  - "FR-CMF-09"
  - "FR-CMF-10"
pipeline_stage: "mobile notification, quick review, quick command, and PWA handoff"
entry_object: "TelegramReviewNotification, SurfaceActionEnvelope, QuickActionToken"
exit_object: "QuickReviewReceipt, SurfaceCommandResult, PwaHandoffReceipt"
validation_contract: "Telegram initData verification, quick action token, evidence sufficiency, PWA deep link, Command Bus submission"
required_receipt: "QuickReviewReceipt"
runtime_target: "Telegram Bot / Telegram Mini App / FastAPI webhook / PWA deep link / Command Bus"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-141: Telegram Bot, Mini App, and PWA Handoff Integration

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture.md` | Defines Telegram Bot and Telegram Mini App as surfaces over the same command/object model. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-007-pwa-and-telegram-state-parity.md` | PWA and Telegram parity requirement. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-055-telegram-quick-review-with-evidence.md` | Existing Telegram quick review spec. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/telegram_review.py` | Existing quick review route requires configured service. |
| `THE CMF STUDIO/src/ccp_studio/api/v1/webhooks/telegram.py` | Existing webhook validates Telegram init data and submits surface actions. |
| `THE CMF STUDIO/src/ccp_studio/contracts/telegram_review.py` | Existing notification, quick action, token, and receipt contracts. |
| `THE CMF STUDIO/src/ccp_studio/contracts/surfaces.py` | Surface action command result contracts. |
| `THE CMF STUDIO/src/ccp_studio/services/telegram_review_service.py` | Telegram review service and command handler owner. |
| `THE CMF STUDIO/src/ccp_studio/services/surface_action_service.py` | Surface action to Command Bus adapter owner. |

## 2. Overview

Telegram is not an optional notification toy. For CMF Studio it is the lightweight mobile cockpit for quick review, render alerts, approval blockers, provider failures, and handoff back to the PWA. The backend already has important pieces: quick review contracts, notification APIs, surface action service, and webhook verification. This spec completes the production integration.

Telegram must support three modes. First, Bot notifications send compact evidence-rich cards when work needs attention. Second, quick actions allow low-risk approve, reject, or request revision only when evidence sufficiency permits. Third, Telegram Mini App/PWA handoff opens the full review workbench when the object is complex, blocked, stale, identity-sensitive, or missing required evidence.

Telegram never owns separate business state. It submits `SurfaceActionEnvelope` objects to the same Command Bus used by PWA and Pi. The same review read model and approval blockers must decide what is available in Telegram.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-141-001 | `TelegramBotAdapter` | Sends notifications, command buttons, and render/review alerts. |
| DEP-CMF-141-002 | `TelegramMiniAppShell` | Authenticated lightweight preview and PWA handoff surface. |
| DEP-CMF-141-003 | `EvidenceSufficiencyDecision` | Determines whether quick action is allowed. |
| DEP-CMF-141-004 | `QuickActionToken` | Short-lived token for Telegram actions. |
| DEP-CMF-141-005 | `SurfaceActionEnvelope` | Surface-neutral command request. |
| DEP-CMF-141-006 | `PwaHandoffReceipt` | Receipt proving Telegram linked to exact PWA route/object/version. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `api/v1/telegram_review.py` | Configure service from production app root and add handoff endpoint. |
| `api/v1/webhooks/telegram.py` | Replace default token and in-memory service with production injected dependencies. |
| `services/telegram_review_service.py` | Build evidence cards and quick action tokens for all review objects. |
| `services/surface_action_service.py` | Enforce evidence sufficiency and submit through Command Bus. |
| `operator-web` | Provide deep-linkable PWA routes for review objects. |

### ADR-05 Primitive Implementation

Telegram cards must show primitive status summaries for composition-bearing, script, interview brief, or extraction review objects. If primitive evidence cannot fit in the card, Telegram approval is disabled and `Open PWA Review` is the primary action.

### CBAR Mandate Enforcement

| CBAR Mandate | Implementation Rule |
|---|---|
| Phase4-M04 Frictionless Block | Telegram shows why action is blocked and provides PWA handoff. |
| Phase4-M05 Actionable Rejection | Request revision includes structured reason or opens PWA for detail. |
| Phase5-M01 Verifiable Artifact | Quick actions produce `QuickReviewReceipt` and linked command receipt. |

## 4. PRD and FR-CMF Requirement Trace

| Requirement | Implementation Meaning |
|---|---|
| FR-CMF-01 | Telegram actions validate actor, role, brand workspace, guest, and object scope. |
| FR-CMF-09 | Telegram supports evidence-rich review, approval, rejection, revision, and blocker display. |
| FR-CMF-10 | Telegram shows operations alerts, recovery prompts, and PWA handoff. |

## 5. Canonical Pipeline Stage Trace

Telegram participates in review, approval, provider alert, render alert, publishing confirmation, and recovery prompt stages. It does not perform heavy authoring, deep editing, or hidden production mutation.

## 6. Greenfield Integration and Legacy Migration Context

Legacy Telegram bots may be referenced for interaction patterns only. The production Telegram integration belongs inside CMF project services and contracts.

## 7. Architecture Component Map

| Component | Owner | Responsibility |
|---|---|---|
| `TelegramBotAdapter` | Backend adapter | Send messages/buttons and receive webhook updates. |
| `TelegramAuthService` | Backend | Verify initData and action tokens. |
| `TelegramReviewService` | Backend | Create review cards and quick action receipts. |
| `SurfaceActionService` | Backend | Convert surface action to Command Bus submission. |
| `PwaDeepLinkBuilder` | Backend/PWA | Generate exact PWA route with object id/version. |
| `TelegramMiniAppShell` | Frontend | Render compact review and handoff. |

## 8. Implementation Plan

1. Add production Telegram settings in `ApplicationSettings`.
2. Configure `TelegramReviewService` and `SurfaceActionService` through TS-CMF-137 composition root.
3. Add `PwaHandoffReceipt` contract.
4. Add `POST /api/v1/webhooks/telegram/pwa-handoff`, validating token/initData, returning a deep link, and recording receipt.
5. Extend quick review card builders for video, still visual, carousel, interview brief, eval blocker, and publishing intent objects.
6. Enforce evidence sufficiency: approve only if hard blockers are absent and evidence summary is complete; revision allowed with short reason or PWA requirement; complex revisions force PWA.
7. Add Mini App route in `operator-web` or a sibling app that reads the same API client.
8. Add tests for token expiry, stale object, insufficient evidence, and PWA handoff.

## 9. Primary Pydantic Output Schema

```python
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field

class PwaHandoffRequest(BaseModel):
    schema_version: Literal["cmf.pwa_handoff_request.v1"] = "cmf.pwa_handoff_request.v1"
    telegram_user_id: str = Field(min_length=1)
    review_object_type: str = Field(min_length=1)
    review_object_id: UUID
    expected_object_version: str | None = None
    requested_action: Literal["open_review", "complete_revision", "inspect_blockers", "approve_after_evidence"]

class PwaHandoffReceipt(BaseModel):
    schema_version: Literal["cmf.pwa_handoff_receipt.v1"] = "cmf.pwa_handoff_receipt.v1"
    receipt_id: UUID
    telegram_user_id: str
    review_object_type: str
    review_object_id: UUID
    pwa_route: str
    token_expires_at: datetime
    created_at: datetime
```

## 10. Commands, Events, Workflows, and Receipts

| Object | Requirement |
|---|---|
| `TelegramReviewNotification` | Sent when object needs attention. |
| `QuickActionToken` | Required for quick action. |
| `SurfaceActionEnvelope` | Submitted by Telegram/Mini App. |
| `QuickReviewReceipt` | Required for quick review outcome. |
| `PwaHandoffReceipt` | Required for deep link handoff. |
| `telegram.quick_action.blocked` | Event when evidence insufficiency blocks action. |

## 11. DSPy Programs, JIT Skills, or Deterministic Services

Telegram does not run intelligence programs. It can request agent work through command proposals, but the agent work runs server-side.

## 12. Provider, Renderer, Projection, or Worker Boundaries

Telegram receives provider/render status summaries only from CMF read models. It never calls workers or provider APIs.

## 13. CBAR Constraint Pass

| Constraint | Pass Condition |
|---|---|
| Tension | Mobile review must be fast but not under-evidenced. |
| Failure Scenario | Telegram approves a composition without primitive details. |
| Resolution Demand | Evidence sufficiency disables approval and opens PWA. |
| Downstream Proof | Quick review receipt or PWA handoff receipt is written. |

## 14. Acceptance Criteria with Failure Examples

| AC | Acceptance Criteria | Failure Example | CBAR |
|---|---|---|---|
| AC141-01 | Telegram initData/action token verified for every action. | Webhook accepts unsigned payload. | Phase1-M05 |
| AC141-02 | Telegram service is configured by app root. | Route raises "must be configured" in production. | Phase4-M04 |
| AC141-03 | Approval is disabled when evidence is insufficient. | Telegram approves object with hard blocker. | Phase4-M04 |
| AC141-04 | Complex revision opens PWA handoff. | Telegram collects vague free text and submits repair. | Phase4-M05 |
| AC141-05 | Quick actions produce receipts linked to command ids. | Button response changes state without receipt. | Phase5-M01 |

## 15. Dependencies

| Dependency | Required Before Build |
|---|---|
| TS-CMF-007 | PWA/Telegram parity. |
| TS-CMF-055 | Telegram quick review. |
| TS-CMF-136 | PWA API client and deep-link routes. |
| TS-CMF-137 | Production app composition. |
| TS-CMF-140 | Revision workflow for request revision actions. |

## 16. Testing Strategy

| Test Type | Required Tests |
|---|---|
| Unit | Token verification rejects invalid/expired token. |
| Unit | Evidence insufficiency disables approval. |
| Integration | Notification to quick action to surface command to receipt. |
| Integration | Complex review creates PWA handoff receipt. |
| Negative | Telegram cannot approve stale object version. |

## 17. Observability, Recovery, and Rollback

1. Log Telegram correlation ids and action token ids.
2. Show failed webhook delivery in operations board.
3. Retry notification sends with idempotency.
4. Roll back by disabling quick actions while keeping notifications and PWA links.

## 18. Spec Audit Receipt

| Field | Value |
|---|---|
| Spec id | TS-CMF-141 |
| Protocol | CMF/ERA3 18-section spec |
| Telegram state ownership | Not allowed |
| Evidence sufficiency | Required |
| PWA handoff | Required |
| Status | ready-for-development |
