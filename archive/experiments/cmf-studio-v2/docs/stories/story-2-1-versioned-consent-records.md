---
story_id: "2.1"
story_title: "Versioned Consent Records"
epic_id: 2
epic_title: "Consent, Source, Likeness, and Voice Safety"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-02.01"
pipeline_stage: "1 / 13 / 14"
entry_object: "consent request"
exit_object: "`ConsentRecordVersion`"
validation_contract: "consent scope model"
required_receipt: "consent receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 2.1: Versioned Consent Records

**Epic:** 2 - Consent, Source, Likeness, and Voice Safety
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-02.01 |
| Canonical Pipeline Stage | 1 / 13 / 14 |
| Entry Object | consent request |
| Exit Object | `ConsentRecordVersion` |
| Validation Contract | consent scope model |
| Required Receipt | consent receipt |
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

As a guest or client, I want to provide, narrow, expire, and revoke consent, so that my source, likeness, voice, reuse, retention, and publication boundaries are enforceable.

**Acceptance Criteria:**

- Given a guest grants consent, when the record is saved, then it creates an immutable `consent_record_versions` row with scopes for recording, storage, likeness, derivative generation, provider processing, synthetic voice eligibility, reuse, retention, and publication.
- Given the guest narrows consent, when a new version is created, then the old version remains auditable and new commands evaluate against the current active version.
- Given consent expires, when a render or memory command runs after expiry, then the command is blocked and the receipt names the expired scope.
- Given consent is revoked, when a pending provider job is still queued, then the system blocks future processing and marks affected pending work for quarantine or review.
- Given a reviewer inspects an asset, when consent state is shown, then the UI displays active consent version, scope compatibility, source evidence, and revocation risk.

**Technical Notes:** Implement `ConsentRecordVersion`, `ConsentScope`, `ConsentPolicy`, and consent validation in the Command Bus. Store immutable consent receipts under `brands/{brand_id}/receipts/`.

**Legacy and Primitive Mapping:** Brand Genesis and V9.1 consent doctrine; legacy receipt chain. Active families: SAF, PER.

**Prerequisites:** Epic 1.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
