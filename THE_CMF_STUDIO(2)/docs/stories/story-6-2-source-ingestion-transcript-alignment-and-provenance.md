---
story_id: "6.2"
story_title: "Source Ingestion, Transcript Alignment, and Provenance"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-06.02"
pipeline_stage: "5"
entry_object: "recordings/transcripts"
exit_object: "aligned source/transcript artifacts"
validation_contract: "source integrity and transcript alignment"
required_receipt: "ingestion receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 6.2: Source Ingestion, Transcript Alignment, and Provenance

**Epic:** 6 - Complete Expression Sessions and Guest Asset Packs
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-06.02 |
| Canonical Pipeline Stage | 5 |
| Entry Object | recordings/transcripts |
| Exit Object | aligned source/transcript artifacts |
| Validation Contract | source integrity and transcript alignment |
| Required Receipt | ingestion receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Convert live narrative induction and grounded transcript/source extraction into approved Expression Moments, valid routes, and source-backed Guest Asset Pack specs.

**Covers:** FR-CMF-06.01 through FR-CMF-06.08.

**User Value:** Operators and Reviewers can transform an interview into routable assets without fabricating beyond source expression.

**Technical Context:** `/api/v1/expression-sessions`, `/api/v1/expression-moments`, `/api/v1/asset-packages`, CompleteExpressionSessionWorkflow, recording artifacts, transcript revisions, timestamped anchor hits, expression moments, archetype routes, asset package specs.

**CBAR Failure Scenario:** If the system only hunts clips after the transcript exists, it misses the human induction layer. If it routes by generic format, it fabricates. The resolution is dual-layer extraction plus valid route registries.

## Story Definition

As an Operator, I want to ingest, preserve, align, and version recordings, audio tracks, transcripts, timestamps, and upload provenance, so that every downstream moment has source lineage.

**Acceptance Criteria:**

- Given recording artifacts are uploaded, when ingestion succeeds, then each artifact records hash, source type, upload route, retention policy, brand ID, session ID, and immutable URI.
- Given a transcript is generated or uploaded, when alignment completes, then transcript revisions are append-only and timestamp aligned to source artifacts.
- Given a transcript revision supersedes another, when extraction runs, then it references the selected revision rather than mutating previous revisions.
- Given audio contains interviewer and guest tracks, when classification is available, then source voice and interviewer voice are represented distinctly.
- Given source artifact corruption is detected, when ingestion runs, then the workflow reaches terminal failure requiring re-upload.

**Technical Notes:** Use `recording_artifacts`, `transcript_revisions`, object storage `source` and `transcripts`, and transcript provider capability contract.

**Legacy and Primitive Mapping:** Legacy audio engine and source doctrine. Active families: VOC, SAF.

**Prerequisites:** Story 6.1.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
