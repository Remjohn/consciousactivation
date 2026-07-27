---
tech_spec_id: "TS-CMF-007"
title: "PWA and Telegram State Parity"
story_id: "1.5"
story_title: "PWA and Telegram State Parity"
epic_id: 1
epic_title: "Governed Workspace and Production Spine"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-1-5-pwa-and-telegram-state-parity.md"
fr_ids:
  - "FR-CMF-01.03"
  - "FR-CMF-01.07"
pipeline_stage: "1 / 13"
entry_object: "PWA or Telegram action"
exit_object: "canonical command result"
validation_contract: "same state and role validation"
required_receipt: "command receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / generated TypeScript / Telegram Bot and Mini App"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-007: PWA and Telegram State Parity

**Status:** Ready for Development  
**Story:** `1.5 - PWA and Telegram State Parity`  
**Implementation Boundary:** Surface action envelopes, Telegram webhook authentication, generated PWA/Telegram contracts, deep links, canonical command results, notification intents, and stale-state protection.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Product authority for PWA Control Tower and Telegram Operator Cockpit. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-01.03 and FR-CMF-01.07 source authority plus Telegram quick action parity. |
| `docs/architecture.md` | Architecture source for PWA/Telegram surface boundaries, Telegram initData verification, generated contracts, and Command Bus. |
| `docs/cmf-studio-pipeline-map.md` | Stage 1 and Stage 13 trace for actions, review, approval, and publication readiness. |
| `docs/migration/legacy-inventory.md` | Legacy Telegram/Mini App patterns as reference only. |
| `docs/stories/story-1-5-pwa-and-telegram-state-parity.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-001-contract-kernel-command-spine.md` | Canonical command result dependency. |
| `docs/tech-specs/TS-CMF-004-organization-and-brand-workspace-lifecycle.md` | Brand scope dependency. |
| `docs/tech-specs/TS-CMF-005-role-based-production-permissions.md` | Same role validation dependency. |

## 2. Overview

### Problem Statement

PWA and Telegram serve different operator moments. PWA is the deep-work control tower. Telegram is the mobile cockpit for notifications, previews, quick approvals, rejections, and status commands. If Telegram owns separate business state or a weaker permission path, mobile decisions can fork production reality.

### Solution

Implement a surface parity layer where PWA and Telegram submit the same typed commands to the same FastAPI backend. Telegram webhook and Mini App actions are authenticated server-side, converted into `SurfaceActionEnvelope`, validated through Command Bus, checked against current object version, and closed with the same canonical command result and receipt as PWA.

### Scope

In scope:

- `SurfaceActionEnvelope`, `TelegramActionPayload`, `PWAActionPayload`, `DeepLinkTarget`, `ObjectStateSnapshot`, `NotificationIntent`, and `SurfaceCommandResult` contracts.
- Telegram webhook endpoint and server-side Telegram authentication.
- Generated TypeScript contracts for PWA and Telegram.
- Stale-state protection with object version or state hash.
- Deep-link rules for complex decisions that require PWA review.
- Event-driven notifications reflecting latest canonical state.

Out of scope:

- Visual design of PWA review screens.
- Telegram bot copy finalization.
- Publishing adapter implementation.
- Separate Telegram business state.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-01.03 | Every command and query binds to active brand context. | Surface action envelope includes organization, brand, object, state version, command, and actor context. |
| FR-CMF-01.07 | PWA Control Tower and Telegram Operator Cockpit expose same governed object state through different surfaces. | Generated contracts, shared Command Bus, Telegram webhook auth, stale-state checks, and event-driven notification read model. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `1 - Workspace and commercial setup`; `13 - Review, approval, revision, and publishing intent` |
| Entry Object | PWA or Telegram action |
| Exit Object | Canonical command result |
| Allowed Actors / Services | Operator, Reviewer, Publishing Approver, PWA, Telegram Bot, Telegram Mini App, SurfaceActionService, Command Bus |
| Validation Contract | Same authentication, role, brand scope, object state, idempotency, evidence, and receipt validation |
| Required Receipt | Command receipt |
| Forbidden Shortcut | Telegram-only business state, blind approval without evidence, stale overwrite, PWA-only role logic |

### Legacy Intelligence Mapping

Legacy Telegram and Mini App patterns are reference only. State belongs to the Python backend. TypeScript is restricted to PWA, Telegram Mini App, Telegram Bot client where needed, and generated contract consumers. Telegram cannot decide domain semantics, approve without sufficient evidence, or write directly to production tables.

Target modules:

- `ccp_studio.contracts.surfaces`
- `ccp_studio.services.surface_action_service`
- `ccp_studio.services.telegram_auth_service`
- `ccp_studio.services.notification_intent_service`
- `ccp_studio.api.v1.webhooks.telegram`
- `ccp_studio.api.v1.surface_actions`
- `ccp_studio.contract_generation.typescript`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `SurfaceActionEnvelope` | Normalizes PWA and Telegram actions before Command Bus. |
| `TelegramActionPayload` | Telegram-specific signed payload, message context, and callback data. |
| `DeepLinkTarget` | Stable PWA object route for complex review or evidence expansion. |
| `ObjectStateSnapshot` | Object ID, brand ID, state, version, and evidence sufficiency. |
| `NotificationIntent` | Backend-generated notification over latest canonical state. |
| `SurfaceCommandResult` | Shared action result returned to PWA or Telegram. |

## 4. Implementation Plan

### Workstream A: Surface Contracts

Define shared surface action and result contracts. Include object ID, brand ID, state version, command type, idempotency key, evidence summary, and source surface.

### Workstream B: Telegram Authentication

Implement server-side Telegram `initData` verification for Mini App and webhook/callback verification for Bot interactions. Reject unsigned or stale payloads before Command Bus.

### Workstream C: Surface Action Service

Convert PWA and Telegram actions into `CommandEnvelope`. The surface layer cannot bypass TS-CMF-001 validation.

### Workstream D: Stale State Protection

Require `object_state_version` or state hash on quick actions. If another surface changes the object first, reject stale action with a clear command result.

### Workstream E: Evidence and Deep Link Policy

Define evidence sufficiency rules. If Telegram cannot show enough evidence for approval, return deep link to PWA rather than allowing blind approval.

### Workstream F: Notification Intents

Generate notifications from domain events and read latest canonical state before delivery.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field


class SurfaceKey(str, Enum):
    pwa = "pwa"
    telegram_bot = "telegram_bot"
    telegram_mini_app = "telegram_mini_app"


class ObjectStateSnapshot(BaseModel):
    schema_version: Literal["cmf.object_state_snapshot.v1"]
    object_type: str
    object_id: UUID
    organization_id: UUID
    brand_id: UUID
    state: str
    state_version: str
    evidence_sufficient_for_surface: bool
    evidence_refs: list[str] = Field(default_factory=list)


class SurfaceActionEnvelope(BaseModel):
    schema_version: Literal["cmf.surface_action.v1"]
    surface_action_id: UUID
    source_surface: SurfaceKey
    actor_id: UUID
    organization_id: UUID
    brand_id: UUID
    command_type: str
    idempotency_key: str
    object_snapshot: ObjectStateSnapshot
    payload: dict[str, Any]
    requested_at: datetime


class DeepLinkTarget(BaseModel):
    schema_version: Literal["cmf.deep_link_target.v1"]
    target_surface: Literal["pwa"]
    route: str
    object_type: str
    object_id: UUID
    brand_id: UUID
    required_reason: str


class SurfaceCommandResult(BaseModel):
    schema_version: Literal["cmf.surface_command_result.v1"]
    surface_action_id: UUID
    command_id: UUID | None = None
    accepted: bool
    result_code: str
    message: str
    deep_link: DeepLinkTarget | None = None
    latest_state: ObjectStateSnapshot | None = None
    receipt_id: UUID | None = None
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `SubmitSurfaceActionCommand`, `SubmitTelegramQuickActionCommand`, `SubmitPWAActionCommand`, `GenerateNotificationIntentCommand` |
| Events | `SurfaceActionReceived`, `TelegramActionAuthenticated`, `SurfaceActionRejected`, `NotificationIntentCreated`, `SurfaceCommandResultReturned` |
| Workflows | Surface action workflow, Telegram notification workflow, stale action resolution workflow |
| Receipts | Command receipt, surface action receipt, Telegram authentication receipt where required |

## 7. Backward Compatibility and Migration Fallback

Telegram legacy patterns can inform interaction design, but not persistence. If a Telegram action cannot be authenticated or cannot show enough evidence, it must fail or deep-link to PWA.

Fallback behavior:

- Invalid Telegram auth returns `TELEGRAM_AUTH_INVALID`.
- Stale object version returns `STALE_OBJECT_STATE`.
- Insufficient evidence returns `PWA_REVIEW_REQUIRED`.
- Missing brand scope returns `BRAND_SCOPE_VIOLATION`.
- Separate Telegram state writes are blocked by architecture and tests.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Telegram must be fast and low-friction; production authority requires the same evidence, role, brand, and state validation as PWA. |
| UX / Ops Failure Scenario | A Telegram quick approval overwrites a newer PWA rejection or approves an asset without enough evidence. |
| Resolution Demand | Canonical state parity takes precedence. Telegram can accelerate valid actions but cannot weaken validation or fork state. |
| Downstream Proof | Tests must prove Telegram and PWA actions use the same Command Bus, stale actions fail, blind approvals deep-link to PWA, and notifications reflect latest canonical state. |

## 9. Tasks

- Define surface contracts.
- Implement Telegram auth service.
- Implement surface action service.
- Add Telegram webhook route and PWA surface action route.
- Generate TypeScript contracts.
- Add stale-state protection.
- Add evidence sufficiency and deep-link policy.
- Add notification intent generation from domain events.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Telegram deep link references the same object ID, brand ID, state, and required command as PWA. | Telegram payload points to stale asset ID. |
| AC2 | Telegram quick action validates auth, role, brand scope, idempotency, object state, and receipt writer availability. | Telegram callback bypasses role check. |
| AC3 | Competing PWA and Telegram actions respect latest canonical state. | Telegram approval overwrites earlier PWA rejection. |
| AC4 | Complex decision requiring more evidence deep-links to PWA instead of allowing blind approval. | Bot approves a sensitive render from a thumbnail only. |
| AC5 | Telegram follow-up notification reflects latest canonical state after PWA changes. | Bot says render is pending after PWA rejection. |

## 11. Dependencies

Internal:

- TS-CMF-001 Command Bus
- TS-CMF-004 Workspace lifecycle
- TS-CMF-005 Role permissions
- Event outbox
- Generated TypeScript contract pipeline

External:

- FastAPI
- Pydantic v2
- Telegram Bot API and Mini App auth
- Next.js PWA consumer

## 12. Testing Strategy

Unit tests:

- Surface action schema.
- Telegram initData verification.
- Object state version stale check.
- Evidence sufficiency decision.
- Deep link target validation.

Integration tests:

- PWA action submits command and returns receipt.
- Telegram action submits same command path and returns receipt.
- PWA first action updates state, Telegram stale action fails.
- Telegram insufficient evidence returns PWA deep link.
- Domain event creates notification from latest state.

Safety tests:

- Telegram route cannot write to canonical tables directly.
- PWA and Telegram permission checks are identical.
- Generated TypeScript contract matches Pydantic schema.

## 13. Observability, Recovery, and Rollback

- Logs include `surface_action_id`, `source_surface`, `command_id`, `object_id`, `state_version`, `organization_id`, and `brand_id`.
- Metrics track Telegram auth failures, stale actions, PWA review redirects, command receipts, and notification latency.
- Recovery regenerates notification intents from domain events.
- Rollback uses compensating commands, not surface-specific state edits.

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
| Requirement Trace | FR-CMF-01.03, FR-CMF-01.07 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Telegram patterns are reference only; Python backend owns state |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | PWA/Telegram submit typed commands to Python Command Bus |
| TypeScript Boundary | Generated consumer contracts only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

