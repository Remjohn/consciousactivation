---
story_id: "8.6"
story_title: "Audio, Caption, Timeline, and Mix Assembly"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-08.06"
pipeline_stage: "12"
entry_object: "audio/caption/timeline plan"
exit_object: "manifests and final mix"
validation_contract: "voice/caption/timing validation"
required_receipt: "sonic/timeline receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 8.6: Audio, Caption, Timeline, and Mix Assembly

**Epic:** 8 - Governed Rendering and Provider Operations
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-08.06 |
| Canonical Pipeline Stage | 12 |
| Entry Object | audio/caption/timeline plan |
| Exit Object | manifests and final mix |
| Validation Contract | voice/caption/timing validation |
| Required Receipt | sonic/timeline receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Execute deterministic and generative rendering through explicit provider capability contracts, receipt-backed jobs, retryable workflows, and self-hosted GPU worker control.

**Covers:** FR-CMF-08.01 through FR-CMF-08.08.

**User Value:** Production Stewards can render assets without hidden scripts, provider drift, duplicate costs, or opaque final artifacts.

**Technical Context:** `/api/v1/provider-jobs`, `/api/v1/renders`, `/api/v1/visual-research`, `/api/v1/webhooks/providers`, provider adapters, `provider_jobs`, `visual_research_queries`, `visual_candidates`, `asset_research_manifests`, `image_resolution_maps`, `render_contracts`, `render_outputs`, ComfyUI worker assets, object storage provider paths.

**CBAR Failure Scenario:** If provider calls are hidden one-off scripts, costs and failures become unrecoverable. Provider operations must therefore be typed, receipt-backed, idempotent, and separable from canonical business decisions.

## Story Definition

As a Production Steward, I want source audio, interviewer audio, restored audio, synthetic bridge audio, SFX, music, captions, and final mix separated into auditable timeline components, so that sonic and caption quality can be reviewed and repaired.

**Acceptance Criteria:**

- Given a render uses audio, when the audio mix manifest is produced, then source, interviewer, restored, synthetic bridge, SFX, music, and final mix components are classified.
- Given captions are generated, when the caption manifest is built, then it includes timing, text source, style constraints, and platform variant.
- Given audio ducking is applied, when evaluated, then ducking math and affected segments are recorded.
- Given synthetic bridge voice exists, when rendered, then it follows Voice-DNA Boost restrictions from Epic 2.
- Given final assembly completes, when review opens, then the Reviewer can inspect timeline, audio, caption, and mix lineage.

**Technical Notes:** Implement `AudioMixManifest`, `CaptionManifest`, `TimelineManifest`, and tests against legacy audio/caption references.

**Legacy and Primitive Mapping:** Legacy audio engine, caption engine, timeline generator, SFL failure corpus. Active families: VOC, FBK, SAF.

**Prerequisites:** Stories 2.4, 7.4, and 8.2.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
