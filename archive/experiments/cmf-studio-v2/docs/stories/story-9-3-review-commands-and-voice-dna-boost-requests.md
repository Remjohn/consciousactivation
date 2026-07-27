---
story_id: "9.3"
story_title: "Review Commands and Voice-DNA Boost Requests"
epic_id: 9
epic_title: "Review, Approval, and Publishing Intent"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-09.03"
pipeline_stage: "13"
entry_object: "reviewer decision"
exit_object: "review command or approval event"
validation_contract: "role/evidence/voice eligibility"
required_receipt: "review decision receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 9.3: Review Commands and Voice-DNA Boost Requests

**Epic:** 9 - Review, Approval, and Publishing Intent
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-09.03 |
| Canonical Pipeline Stage | 13 |
| Entry Object | reviewer decision |
| Exit Object | review command or approval event |
| Validation Contract | role/evidence/voice eligibility |
| Required Receipt | review decision receipt |
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

As a Reviewer, I want to approve, reject, request revisions, escalate for manual review, or request eligible Voice-DNA Boost through governed commands, so that every decision is auditable and reversible where allowed.

**Acceptance Criteria:**

- Given review evidence is visible, when the Reviewer approves, rejects, requests revision, escalates, or requests Voice-DNA Boost, then the action is a typed command with receipt.
- Given Voice-DNA Boost is requested, when eligibility fails, then the command is rejected with the violated rule.
- Given a revision request is saved, when the Production Steward opens the asset, then the request includes exact evidence, failure category, and expected repair.
- Given manual escalation is selected, when saved, then the asset enters `blocked` or `ready_for_review` according to state policy.
- Given approval succeeds, when event is recorded, then `ApprovalEventRecorded` includes actor, evidence, source references, and evaluation receipt IDs.

**Technical Notes:** Implement `ReviewDecision`, `RevisionRequest`, `ApprovalEvent`, `RequestVoiceDnaBoost`, and review command handlers.

**Legacy and Primitive Mapping:** Legacy receipt chain, Voice DNA doctrine, CBAR. Active families: FBK, SAF, VOC.

**Prerequisites:** Stories 2.4, 9.1, and 9.2.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
