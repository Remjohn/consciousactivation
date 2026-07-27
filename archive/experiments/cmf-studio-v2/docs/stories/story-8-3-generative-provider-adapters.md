---
story_id: "8.3"
story_title: "Generative Provider Adapters"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-08.03"
pipeline_stage: "11"
entry_object: "generative provider request"
exit_object: "generated/edited asset"
validation_contract: "provider metadata and consent compatibility"
required_receipt: "provider receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 8.3: Generative Provider Adapters

**Epic:** 8 - Governed Rendering and Provider Operations
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-08.03 |
| Canonical Pipeline Stage | 11 |
| Entry Object | generative provider request |
| Exit Object | generated/edited asset |
| Validation Contract | provider metadata and consent compatibility |
| Required Receipt | provider receipt |
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

As a Production Steward, I want special or generative assets routed through approved provider adapters while preserving prompt hashes, metadata, inputs, outputs, costs, retries, and evaluation state, so that generative work remains reproducible enough for review.

**Acceptance Criteria:**

- Given GPT Image 2, Flux 2 Klein 9b, Qwen-Image-Layered, SAM3, LavaSR, or MOSS-TTS is used, when the job is submitted, then it passes through a provider adapter and capability record.
- Given a provider request uses source assets, when submitted, then input artifact hashes and consent compatibility are recorded.
- Given provider output is returned, when normalized, then it is stored under `brands/{brand_id}/provider-raw/` with output hashes and receipt.
- Given an output fails evaluation, when the job completes, then it is not promoted to approved render output without revision or rejection.
- Given model metadata is missing, when receipt is created, then the provider job fails receipt validation.

**Technical Notes:** Implement provider-specific adapters behind the common interface. Domain services cannot call provider SDKs directly unless they are provider adapter services.

**Legacy and Primitive Mapping:** Provider capability registry doctrine, visual research references. Active families: VSG, VOC, FBK.

**Prerequisites:** Stories 8.1 and 7.2.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
