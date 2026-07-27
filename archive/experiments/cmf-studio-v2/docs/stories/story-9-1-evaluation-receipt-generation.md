---
story_id: "9.1"
story_title: "Evaluation Receipt Generation"
epic_id: 9
epic_title: "Review, Approval, and Publishing Intent"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-09.01"
pipeline_stage: "13"
entry_object: "render/package ready for review"
exit_object: "`EvaluationReceipt`"
validation_contract: "category thresholds and evidence"
required_receipt: "evaluation receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 9.1: Evaluation Receipt Generation

**Epic:** 9 - Review, Approval, and Publishing Intent
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-09.01 |
| Canonical Pipeline Stage | 13 |
| Entry Object | render/package ready for review |
| Exit Object | `EvaluationReceipt` |
| Validation Contract | category thresholds and evidence |
| Required Receipt | evaluation receipt |
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

As a Reviewer, I want evaluation receipts for source truth, archetype fit, expression depth, identity, likeness, composition, style, motion, platform fit, negative space, micro-semiotic anchors, routeability, and publishing readiness, so that review starts with evidence.

**Acceptance Criteria:**

- Given a render or asset package reaches review readiness, when evaluation runs, then receipts are created for required evaluation categories.
- Given an evaluation category hard-fails, when approval is requested, then approval is blocked.
- Given a receipt references source truth, when opened, then it shows source artifact, transcript segment, timestamp, route, and evaluator version.
- Given evaluator output lacks evidence, when receipt validation runs, then the receipt is invalid.
- Given evaluation is rerun after revision, when saved, then the prior receipt remains immutable and the new receipt links to the revised object.

**Technical Notes:** Implement `EvaluationReceipt`, category-specific evaluators, `EvaluationReceiptCreated` event, and immutable storage.

**Legacy and Primitive Mapping:** ImageCritic, SemanticCritic, VoiceContinuityCritic, CBAR gate packs, anti-draft calibration, SDA/SFL failure corpora. Active families: FBK, SAF, VSG, VOC.

**Prerequisites:** Epics 1 through 8.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
