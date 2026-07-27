---
tech_spec_id: "TS-CMF-054"
title: "Publishing Intent and Publer Adapter"
story_id: "9.5"
story_title: "Publishing Intent and Publer Adapter"
epic_id: 9
epic_title: "Review, Approval, and Publishing Intent"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-9-5-publishing-intent-and-publer-adapter.md"
fr_ids:
  - "FR-CMF-09.05"
  - "FR-CMF-09.06"
pipeline_stage: "14"
entry_object: "approved asset"
exit_object: "PublishingIntent, Publer outcome"
validation_contract: "approval/consent/platform validation"
required_receipt: "publishing receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / Publer adapter / durable workflow"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-054: Publishing Intent and Publer Adapter

**Status:** Ready for Development  
**Story:** `9.5 - Publishing Intent and Publer Adapter`  
**Implementation Boundary:** PublishingIntent, PublishingPlatformVariant, PublerJob, PublishingOutcome, duplicate scheduling guard, Publer adapter, webhook/poll reconciliation, and publishing receipt.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-9-5-publishing-intent-and-publer-adapter.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-09.05 and FR-CMF-09.06 authority. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Publer adapter and human-approved publishing doctrine. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | PublishingIntent, Publer safety, and adapter boundary source. |
| `docs/architecture.md` | PublishingWorkflow and Publer adapter rule. |
| `docs/cmf-studio-pipeline-map.md` | Stage 14 publishing trace. |
| `docs/migration/legacy-inventory.md` | Brand Genesis V3 adapter doctrine and receipt-chain references. |
| `docs/tech-specs/TS-CMF-053-approval-blockers.md` | Approval gate dependency. |

## 2. Overview

Publishing Intent is the internal authority that exists before Publer. It references approved asset, platform variant, captions, consent state, schedule metadata, account mapping, approver, and compliance notes. Publer receives only confirmed Publishing Intents.

Publer is an adapter. It owns external delivery status only. CMF STUDIO owns asset state, approval state, caption truth, schedule intent, source lineage, platform strategy, duplicate scheduling policy, and publishing receipt.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-09.05 | Operators create and confirm Publishing Intent only after approval, consent, lineage, platform variants, captions, and scheduling metadata are valid. | Draft/confirm commands, validation policy, platform variant and caption references, human confirmation, and duplicate scheduling guard. |
| FR-CMF-09.06 | Submit approved Publishing Intents to Publer, track status, prevent duplicate scheduling, and attach outcomes to asset record. | Publer job, adapter request receipt, webhook/poll reconciliation, outcome recording, idempotency, and publishing receipt. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 14 - Publishing, memory, and projection |
| Entry Object | approved asset |
| Exit Object | `PublishingIntent`, Publer outcome |
| Validation Contract | approval/consent/platform validation |
| Required Receipt | publishing receipt |

### Legacy Intelligence Mapping

- Product Brief Publer doctrine maps to adapter-only boundary and confirmation rule.
- Brand Genesis V3 adapter doctrine maps to explicit account, platform, caption, and schedule display.
- Active primitive families SAF, BUS, and FBK govern safety, commercial scheduling clarity, and feedback outcomes.

## 4. Implementation Plan

1. Define `PublishingIntent`, `PublishingPlatformVariant`, `PublishingSchedule`, `PublerJob`, `PublishingOutcome`, `PublerWebhookEnvelope`, and `PublishingReceipt`.
2. Implement draft and confirm commands with approval, consent, lineage, captions, platform, and schedule validation.
3. Require explicit human confirmation before Publer submission.
4. Submit confirmed intents through Publer adapter with idempotency key and duplicate scheduling guard.
5. Reconcile Publer webhook or polling status into `PublishingOutcome`.
6. Attach outcome to asset record without making Publer canonical.
7. Propose memory admission only after outcome receipt is written.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from pydantic import BaseModel


class PublishingIntentStatus(str, Enum):
    DRAFT = "draft"
    VALIDATED = "validated"
    CONFIRMED = "confirmed"
    SUBMITTED = "submitted"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class PublishingPlatformVariant(BaseModel):
    platform_variant_id: str
    platform: str
    asset_uri: str
    caption_manifest_id: str
    platform_format_key: str
    account_mapping_id: str


class PublishingIntent(BaseModel):
    schema_version: Literal["cmf.publishing_intent.v1"]
    publishing_intent_id: str
    approved_asset_id: str
    approval_event_id: str
    consent_record_version_id: str
    platform_variants: list[PublishingPlatformVariant]
    schedule_at: str
    time_zone: str
    confirmed_by_user_id: str | None = None
    status: PublishingIntentStatus
    idempotency_key: str


class PublerJob(BaseModel):
    publer_job_id: str
    publishing_intent_id: str
    external_job_id: str | None = None
    request_receipt_id: str
    status: str


class PublishingOutcome(BaseModel):
    publishing_outcome_id: str
    publishing_intent_id: str
    external_status: str
    external_url: str | None = None
    failure_reason: str | None = None
    received_at: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `DraftPublishingIntentCommand`, `ValidatePublishingIntentCommand`, `ConfirmPublishingIntentCommand`, `SubmitPublishingIntentToPublerCommand`, `ReconcilePublerStatusCommand`, `BlockDuplicatePublishingCommand`, `CancelPublishingIntentCommand` |
| Events | `PublishingIntentDrafted`, `PublishingIntentValidated`, `PublishingIntentConfirmed`, `PublishingIntentSubmittedToPubler`, `PublerStatusReconciled`, `DuplicatePublishingBlocked`, `PublishingIntentCancelled` |
| Workflow | `PublishingWorkflow.stage14_publish_intent` |
| Receipt | `PublishingReceipt` with approval event, consent version, platform variants, captions, schedule, Publer request/status, idempotency key, and outcome |

## 7. Backward Compatibility and Migration Fallback

Legacy publishing/export scripts are adapter references only. If an old path conflated export, approval, and scheduling, split it into approval event, Publishing Intent, adapter request, and outcome receipt. If Publer is unavailable, the internal Publishing Intent remains authoritative with external status `failed` or `pending_retry`.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Scheduling speed vs. human authority | Confirmed Publishing Intent is required before Publer submission. | Publer adapter rejects unconfirmed intents. |
| External delivery vs. internal truth | Publer status cannot mutate canonical approval, caption, or lineage. | Outcome attaches to intent; source state stays internal. |
| Convenience vs. duplicate posting | Idempotency and duplicate scheduling checks must run before submission. | Duplicate attempt writes blocked receipt. |

## 9. Tasks

- Add publishing contracts and persistence.
- Implement draft, validate, confirm, submit, reconcile, cancel, and duplicate-block commands.
- Implement Publer adapter with webhook and polling reconciliation.
- Add platform variant and caption validation.
- Add explicit time zone and account display requirements.
- Add publishing receipt writer.
- Add memory admission proposal hook after outcome.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Draft intent references approved asset, platform variant, captions, consent, schedule, and approver. | Intent references only a media URL. |
| AC2 | Missing approval or consent blocks draft or confirmation. | Unapproved asset is sent to Publer. |
| AC3 | Confirmed intent submitted to Publer stores job ID and request receipt. | Publer upload happens with no internal receipt. |
| AC4 | Publer webhook or poll records outcome without making Publer canonical. | Publer status overwrites approval or caption state. |
| AC5 | Duplicate scheduling attempt is blocked. | Same asset and platform are scheduled twice. |

## 11. Dependencies

- TS-CMF-006 commercial entitlements.
- TS-CMF-007 PWA and Telegram state parity.
- TS-CMF-008 consent records.
- TS-CMF-047 caption and platform manifests.
- TS-CMF-052 review commands.
- TS-CMF-053 approval blockers.

## 12. Testing Strategy


Unit tests:

- Unit tests for PublishingIntent and PublerJob schemas.
- Policy tests for approval, consent, lineage, captions, platform, and schedule validation.
- Adapter tests with Publer sandbox/draft responses.
- Webhook idempotency and polling reconciliation tests.
- Duplicate scheduling tests.
- Failure tests for revoked token and external delivery failure.

Integration tests:

- Workflow test from `approved asset` to `PublishingIntent, Publer outcome` through pipeline stage `14`.
- Command Bus test proving `publishing receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for intents drafted, confirmed, submitted, succeeded, failed, cancelled, and duplicate-blocked.
- Logs include publishing intent ID, approval event ID, account mapping, platform, schedule, time zone, Publer job ID, and idempotency key.
- Recovery retries Publer submission or status reconciliation without creating duplicate jobs.
- Rollback cancels pending external jobs where possible and writes a cancelled or failed outcome; internal approvals remain append-only.

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
| Tech Spec ID | TS-CMF-054 |
| Story | 9.5 |
| Requirement Trace | FR-CMF-09.05, FR-CMF-09.06 |
| Pipeline Trace | Stage 14, approved asset to PublishingIntent/Publer outcome |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No direct Publer publishing, no one-step public scheduling, no Publer canonical state |
