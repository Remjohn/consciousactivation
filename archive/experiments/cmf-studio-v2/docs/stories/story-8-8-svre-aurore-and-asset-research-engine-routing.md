---
story_id: "8.8"
story_title: "SVRE, Aurore, and Asset Research Engine Routing"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-08.08"
pipeline_stage: "11"
entry_object: "`VisualResearchQuery`"
exit_object: "`AssetResearchManifest`, `ImageResolutionMap`"
validation_contract: "license/provenance/asset-roll gate"
required_receipt: "asset research receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 8.8: SVRE, Aurore, and Asset Research Engine Routing

**Epic:** 8 - Governed Rendering and Provider Operations
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-08.08 |
| Canonical Pipeline Stage | 11 |
| Entry Object | `VisualResearchQuery` |
| Exit Object | `AssetResearchManifest`, `ImageResolutionMap` |
| Validation Contract | license/provenance/asset-roll gate |
| Required Receipt | asset research receipt |
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

As a Production Steward, I want visual and found-asset research to run through governed SVRE/Aurore-style contracts, so that asset choices are emotionally precise, source-traced, licensed, and compatible with the scene's asset-roll intent.

**Acceptance Criteria:**

- Given a SceneSpec requires visual references or found assets, when visual research runs, then the system creates a `VisualResearchQuery` with scene ID, asset-roll intent, emotional state, symbolic role, contradiction value, brand alignment, source constraints, and licensing requirements.
- Given candidates are returned, when scoring runs, then each candidate is evaluated for emotional mode match, tribal/cultural proximity, symbolic role, visual congruence, authenticity, source quality, known-person validity when relevant, and direct-use versus composition-reference status.
- Given a candidate is not licensed for direct use, when selected, then it can only be routed as composition reference or blocked according to policy.
- Given SVRE/Aurore legacy logic references superseded execution services, when migrated, then provider execution is adapted to current CMF STUDIO routes and self-hosted ComfyUI worker policy.
- Given an asset is selected, when the Render Contract is compiled, then the `AssetResearchManifest` and `ImageResolutionMap` link selected candidate, alternatives, scoring receipt, license decision, source URL or reference, and downstream render route.

**Technical Notes:** Implement `VisualResearchQuery`, `VisualCandidate`, `AssetResearchManifest`, `ImageResolutionMap`, `LicensingDecision`, and `/api/v1/visual-research`. Use SVRE/Aurore as migration source for SearXNG categories, Pinterest/source search, T-Score-like scoring, known-person validity, and source win-rate logic while keeping provider execution behind current approved adapters.

**Legacy and Primitive Mapping:** Sovereign Visual Research Engine, Aurore v2, Conscious Asset Strategy Guide, CMF Manual asset hunt logic, PRD-03 CMF. Active families: VSG, SAF, TRB, SOC, FBK.

**Prerequisites:** Stories 7.6, 8.1, 8.3, and 8.5.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
