---
story_id: "8.4"
story_title: "Self-Hosted ComfyUI Docker GPU Worker"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-08.04"
pipeline_stage: "11"
entry_object: "ComfyUI queued job"
exit_object: "worker output and cost report"
validation_contract: "approved template and GPU policy"
required_receipt: "GPU worker receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 8.4: Self-Hosted ComfyUI Docker GPU Worker

**Epic:** 8 - Governed Rendering and Provider Operations
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-08.04 |
| Canonical Pipeline Stage | 11 |
| Entry Object | ComfyUI queued job |
| Exit Object | worker output and cost report |
| Validation Contract | approved template and GPU policy |
| Required Receipt | GPU worker receipt |
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

As a Production Steward, I want batch-first self-hosted ComfyUI Docker GPU workers on AWS or Google Cloud with 24GB or 32GB VRAM, so that approved workflow templates can render without relying on external hidden execution services.

**Acceptance Criteria:**

- Given a ComfyUI route is selected, when the worker starts, then it records GPU tier, cloud provider, Docker image, queue state, workflow hash, input assets, and job IDs.
- Given a queued job executes, when it completes an output checkpoint, then the output is uploaded, receipt is written, and progress is persisted.
- Given the queue drains, when no jobs remain, then the worker shuts down and reports cost.
- Given the worker is interrupted, when recovery runs, then completed outputs remain intact and incomplete jobs are requeued from checkpoint.
- Given an unapproved workflow template is referenced, when the job validates, then it is blocked.

**Technical Notes:** Implement `GpuWorkerJob`, worker queue, ComfyUI adapter, checkpointing, cloud metadata, cost reporting, and shutdown policy.

**Legacy and Primitive Mapping:** Legacy ComfyUI JSON templates such as `Wan 2.2 i2v.json` and `qwen-image-layered-image2image.json`. Active families: VSG, SAF, FBK.

**Prerequisites:** Stories 8.1 and 8.3.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
