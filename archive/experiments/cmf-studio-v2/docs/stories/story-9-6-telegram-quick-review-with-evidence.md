---
story_id: "9.6"
story_title: "Telegram Quick Review With Evidence"
epic_id: 9
epic_title: "Review, Approval, and Publishing Intent"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-09.07"
pipeline_stage: "13 / 14"
entry_object: "Telegram quick action"
exit_object: "command result or PWA handoff"
validation_contract: "evidence sufficiency and idempotency"
required_receipt: "quick review receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 9.6: Telegram Quick Review With Evidence

**Epic:** 9 - Review, Approval, and Publishing Intent
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-09.07 |
| Canonical Pipeline Stage | 13 / 14 |
| Entry Object | Telegram quick action |
| Exit Object | command result or PWA handoff |
| Validation Contract | evidence sufficiency and idempotency |
| Required Receipt | quick review receipt |
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

As a Reviewer, I want Telegram quick approvals, rejections, or regeneration requests to show enough evidence and deep-link to PWA for complex cases, so that mobile decisions never become blind rubber-stamps.

**Acceptance Criteria:**

- Given a render is ready, when Telegram sends a notification, then it includes preview, route, source snippet, consent status, evaluation summary, and required action.
- Given evidence is sufficient for a quick decision, when the Reviewer approves or rejects, then the backend records the same command receipt as PWA.
- Given evidence is insufficient or conflicting, when the Reviewer attempts approval, then Telegram deep-links to PWA and approval is not available in-chat.
- Given the object state changes before the Reviewer acts, when the quick action is submitted, then idempotency and state transition checks prevent stale action.
- Given a quick regenerate action is submitted, when valid, then it creates a revision request rather than mutating provider output directly.

**Technical Notes:** Use Telegram Bot/Mini App as leaf surfaces; route all actions through `/api/v1/webhooks/telegram` and Command Bus.

**Legacy and Primitive Mapping:** PWA/Telegram parity doctrine, RIM feedback patterns. Active families: FBK, FRC, SAF.

**Prerequisites:** Story 1.5 and Stories 9.1 through 9.5.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
