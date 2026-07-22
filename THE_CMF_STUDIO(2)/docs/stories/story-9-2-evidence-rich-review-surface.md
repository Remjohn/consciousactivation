---
story_id: "9.2"
story_title: "Evidence-Rich Review Surface"
epic_id: 9
epic_title: "Review, Approval, and Publishing Intent"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-09.02"
pipeline_stage: "13"
entry_object: "asset under review"
exit_object: "evidence-rich review state"
validation_contract: "consent/source/eval completeness"
required_receipt: "review state receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 9.2: Evidence-Rich Review Surface

**Epic:** 9 - Review, Approval, and Publishing Intent
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-09.02 |
| Canonical Pipeline Stage | 13 |
| Entry Object | asset under review |
| Exit Object | evidence-rich review state |
| Validation Contract | consent/source/eval completeness |
| Required Receipt | review state receipt |
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

As a Reviewer, I want to review source quote, transcript segment, archetype route, Brand Context Version, selected assets, render output, evaluation receipt, revision history, and consent state, so that approval decisions are grounded.

**Acceptance Criteria:**

- Given an asset is in review, when the review page opens, then it shows preview, source quote, transcript segment, timestamps, route, brand context, selected assets, render output, evaluations, revisions, and consent state.
- Given a Reviewer selects an evaluation failure, when expanded, then the UI shows exact evidence and repair recommendation.
- Given revision history exists, when opened, then all prior versions and decision reasons are visible.
- Given consent state changed after render, when review opens, then the surface flags current consent compatibility.
- Given the asset is too complex for Telegram, when notification is sent, then Telegram links to this PWA review surface.

**Technical Notes:** Build PWA Render Review and Evaluation Receipt Viewer using generated contracts. Query must not cross brand boundaries.

**Legacy and Primitive Mapping:** V9.1 Evaluation Receipt doctrine, Brand Genesis review surfaces. Active families: FBK, SAF, PER.

**Prerequisites:** Story 9.1.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
