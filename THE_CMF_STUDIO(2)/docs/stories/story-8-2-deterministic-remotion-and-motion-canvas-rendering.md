---
story_id: "8.2"
story_title: "Deterministic Remotion and Motion Canvas Rendering"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-08.02"
pipeline_stage: "12"
entry_object: "RenderContract"
exit_object: "deterministic render output"
validation_contract: "renderer props and brand layer validation"
required_receipt: "render receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 8.2: Deterministic Remotion and Motion Canvas Rendering

**Epic:** 8 - Governed Rendering and Provider Operations
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-08.02 |
| Canonical Pipeline Stage | 12 |
| Entry Object | RenderContract |
| Exit Object | deterministic render output |
| Validation Contract | renderer props and brand layer validation |
| Required Receipt | render receipt |
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

As a Production Steward, I want deterministic assets routed through Remotion or Motion Canvas using approved brand layers, final text rendering, captions, timing, motion recipes, and sonic plans, so that final assembly does not depend on flattened image output.

**Acceptance Criteria:**

- Given a Render Contract selects a deterministic route, when the renderer starts, then it consumes selected brand layers, rig manifest, final text plan, captions, motion recipes, SFX plan, scene timings, audio mix manifest, and platform variants.
- Given final text exists, when rendering occurs, then final text is rendered by the deterministic renderer, not delegated to a generative image provider.
- Given a selected layer is not in locked Brand Context Version, when rendering validates, then it fails.
- Given rendering succeeds, when output is saved, then preview/final URIs, manifest hashes, renderer version, and receipt are stored.
- Given rendering fails, when retry is requested, then previously completed artifacts remain intact.

**Technical Notes:** Implement Remotion and Motion Canvas worker boundaries as TypeScript leaf runtimes consuming generated contracts.

**Legacy and Primitive Mapping:** CMF engine references, caption engine, timeline generator. Active families: VSG, VOC, SAF.

**Prerequisites:** Story 8.1 and Epic 7.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
