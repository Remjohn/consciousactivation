---
story_id: "9.4"
story_title: "Approval Blockers"
epic_id: 9
epic_title: "Review, Approval, and Publishing Intent"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-09.04"
pipeline_stage: "13"
entry_object: "approval request"
exit_object: "blocked or approved state"
validation_contract: "lineage/consent/format/evaluation gate"
required_receipt: "approval blocker receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 9.4: Approval Blockers

**Epic:** 9 - Review, Approval, and Publishing Intent
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-09.04 |
| Canonical Pipeline Stage | 13 |
| Entry Object | approval request |
| Exit Object | blocked or approved state |
| Validation Contract | lineage/consent/format/evaluation gate |
| Required Receipt | approval blocker receipt |
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

As a Reviewer, I want final approval blocked when lineage, consent, source truth, identity, evaluation, platform format, or content-format requirements fail, so that no asset releases on incomplete evidence.

**Acceptance Criteria:**

- Given lineage is incomplete, when approval is attempted, then the command fails and names missing lineage.
- Given consent is incompatible, when approval is attempted, then it fails with `CONSENT_SCOPE_BLOCKED`.
- Given source truth is missing or disputed, when approval is attempted, then it fails.
- Given identity or likeness evaluation fails, when approval is attempted, then the asset must be revised or rejected.
- Given platform variant or valid format registry requirements fail, when approval is attempted, then approval is blocked.

**Technical Notes:** Approval policy checks `CompleteEditingSession`, `SceneSpec`, `ProviderReceipt`, `EvaluationReceipt`, `ConsentRecordVersion`, `ArchetypeRoute`, and `RenderOutput`.

**Legacy and Primitive Mapping:** CBAR failure scenario resolution, V9.1 approval doctrine. Active families: SAF, FBK, PER.

**Prerequisites:** Stories 9.1 through 9.3.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
