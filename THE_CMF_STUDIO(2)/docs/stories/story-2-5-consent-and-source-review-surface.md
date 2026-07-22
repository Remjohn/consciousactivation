---
story_id: "2.5"
story_title: "Consent and Source Review Surface"
epic_id: 2
epic_title: "Consent, Source, Likeness, and Voice Safety"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-02.04"
  - "FR-CMF-02.07"
pipeline_stage: "13"
entry_object: "asset under review"
exit_object: "approval-ready evidence view"
validation_contract: "source and consent completeness"
required_receipt: "review evidence receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 2.5: Consent and Source Review Surface

**Epic:** 2 - Consent, Source, Likeness, and Voice Safety
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-02.04, FR-CMF-02.07 |
| Canonical Pipeline Stage | 13 |
| Entry Object | asset under review |
| Exit Object | approval-ready evidence view |
| Validation Contract | source and consent completeness |
| Required Receipt | review evidence receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Make consent, source truth, likeness, file provenance, and voice eligibility product-level blockers before recording, extraction, rendering, review, memory, and publishing.

**Covers:** FR-CMF-02.01 through FR-CMF-02.07.

**User Value:** Guests and clients keep authority over permission boundaries; Operators and Reviewers know exactly when work is allowed, blocked, or requires repair.

**Technical Context:** `/api/v1/consent`, consent record versions, source artifact storage, recording configuration, voice eligibility policy, review gates, render manifests, error code `CONSENT_SCOPE_BLOCKED`.

**CBAR Failure Scenario:** If consent is a checkbox instead of a state machine, then a revoked likeness can still leak into a render, memory, or publishing job. Consent therefore becomes an execution gate across the whole chain.

## Story Definition

As a Reviewer, I want to inspect consent lineage and source truth before approving assets, memory, publishing, or voice repair, so that approval is evidence-backed.

**Acceptance Criteria:**

- Given an asset is ready for review, when the Reviewer opens it, then the surface shows consent version, source artifact, transcript revision, timestamp references, claim references, voice classification, and file provenance.
- Given a claim lacks source reference, when the review gate runs, then approval is blocked until source truth is repaired or the claim is removed.
- Given source provenance has multiple revisions, when the Reviewer inspects history, then the system shows append-only transcript revisions and source hashes.
- Given the Reviewer approves, when the command is saved, then an `ApprovalEventRecorded` event and audit receipt include consent and source references.
- Given evidence is too complex for Telegram, when a quick approval is attempted, then the action deep-links to PWA.

**Technical Notes:** Implement PWA `Consent and Source Review` and API reads across `consent_record_versions`, `recording_artifacts`, `transcript_revisions`, `evaluation_receipts`, and `approval_events`.

**Legacy and Primitive Mapping:** V9.1 Evaluation Receipt doctrine; legacy receipt chain. Active families: SAF, FBK, PER.

**Prerequisites:** Stories 2.1 through 2.4.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
