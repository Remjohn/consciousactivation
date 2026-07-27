---
story_id: "2.2"
story_title: "Recording Setup and Source Artifact Gate"
epic_id: 2
epic_title: "Consent, Source, Likeness, and Voice Safety"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-02.02"
  - "FR-CMF-02.04"
pipeline_stage: "1 / 5"
entry_object: "recording setup"
exit_object: "`SourceArtifactManifest`"
validation_contract: "source quality and provenance"
required_receipt: "source intake receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 2.2: Recording Setup and Source Artifact Gate

**Epic:** 2 - Consent, Source, Likeness, and Voice Safety
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-02.02, FR-CMF-02.04 |
| Canonical Pipeline Stage | 1 / 5 |
| Entry Object | recording setup |
| Exit Object | `SourceArtifactManifest` |
| Validation Contract | source quality and provenance |
| Required Receipt | source intake receipt |
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

As an Operator, I want to confirm recording setup, master source, backup source, upload route, and quality gates before starting a Complete Expression Session, so that downstream extraction never rests on ambiguous files.

**Acceptance Criteria:**

- Given an Operator starts session setup, when they submit recording configuration, then the system records expected master source, backup route, platform source, upload method, file safety expectations, and quality requirements.
- Given a master source is missing, when session start is requested, then the system blocks the session or requires an explicit approved exception receipt.
- Given a compressed meeting-platform file is uploaded as production source, when a master recording is required, then the system blocks the source from becoming canonical without review.
- Given a source artifact is accepted, when it is stored, then object storage records content hash, source hash, brand ID, session ID, retention policy, provenance, and immutable URI.
- Given upload quality fails, when the Operator reviews setup, then the system shows exact failure category and recovery action.

**Technical Notes:** Use `recording_artifacts`, object storage `brands/{brand_id}/source/`, `SourceArtifact`, `RecordingConfiguration`, and `CompleteExpressionSession` pre-start status.

**Legacy and Primitive Mapping:** V9.1 source doctrine; legacy audio engine references for source separation requirements. Active families: SAF, VOC, FBK.

**Prerequisites:** Stories 1.1 through 2.1.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
