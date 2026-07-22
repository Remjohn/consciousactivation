---
story_id: "9.5"
story_title: "Publishing Intent and Publer Adapter"
epic_id: 9
epic_title: "Review, Approval, and Publishing Intent"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-09.05"
  - "FR-CMF-09.06"
pipeline_stage: "14"
entry_object: "approved asset"
exit_object: "`PublishingIntent`, Publer outcome"
validation_contract: "approval/consent/platform validation"
required_receipt: "publishing receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 9.5: Publishing Intent and Publer Adapter

**Epic:** 9 - Review, Approval, and Publishing Intent
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-09.05, FR-CMF-09.06 |
| Canonical Pipeline Stage | 14 |
| Entry Object | approved asset |
| Exit Object | `PublishingIntent`, Publer outcome |
| Validation Contract | approval/consent/platform validation |
| Required Receipt | publishing receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Make quality, truth, identity, consent, format, and publishing readiness reviewable before external scheduling.

**Covers:** FR-CMF-09.01 through FR-CMF-09.07.

**User Value:** Reviewers can approve only assets that are evidenced, truthful, identity-safe, platform-valid, and publication-ready.

**Technical Context:** `/api/v1/evaluations`, `/api/v1/reviews`, `/api/v1/publishing-intents`, `/api/v1/webhooks/publer`, `evaluation_receipts`, `review_decisions`, `revision_requests`, `approval_events`, `publishing_intents`, `publer_jobs`, `publishing_outcomes`.

**CBAR Failure Scenario:** If publishing follows provider completion, the system releases output before truth, consent, identity, and format checks survive human review. Publishing Intent must be internal authority; Publer is only an adapter.

## Story Definition

As a Publishing Approver, I want to create and confirm Publishing Intent only after approval, consent, lineage, platform variants, captions, and scheduling metadata are valid, so that external scheduling follows internal authority.

**Acceptance Criteria:**

- Given an asset is approved, when Publishing Intent is drafted, then it references approved asset, platform variant, captions, consent state, scheduling metadata, and approver.
- Given approval or consent is missing, when Publishing Intent is drafted or confirmed, then the command is blocked.
- Given Publishing Intent is confirmed, when submitted to Publer, then Publer job ID and request receipt are stored.
- Given Publer succeeds or fails, when webhook or polling result arrives, then `PublishingOutcome` is recorded without making Publer canonical.
- Given duplicate scheduling is attempted, when validation runs, then the command is blocked.

**Technical Notes:** Implement `PublishingIntent`, `PublerJob`, `PublishingOutcome`, `/api/v1/publishing-intents`, Publer adapter, and Publer webhook handler.

**Legacy and Primitive Mapping:** Product Brief Publer doctrine, Brand Genesis V3 adapter doctrine. Active families: SAF, BUS, FBK.

**Prerequisites:** Stories 9.1 through 9.4.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
