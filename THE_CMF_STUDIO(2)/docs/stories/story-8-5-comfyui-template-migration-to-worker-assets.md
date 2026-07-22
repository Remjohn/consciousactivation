---
story_id: "8.5"
story_title: "ComfyUI Template Migration to Worker Assets"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-08.05"
pipeline_stage: "0 / 11"
entry_object: "ComfyUI template"
exit_object: "worker asset"
validation_contract: "hash, compatibility, eval target"
required_receipt: "template migration receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 8.5: ComfyUI Template Migration to Worker Assets

**Epic:** 8 - Governed Rendering and Provider Operations
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-08.05 |
| Canonical Pipeline Stage | 0 / 11 |
| Entry Object | ComfyUI template |
| Exit Object | worker asset |
| Validation Contract | hash, compatibility, eval target |
| Required Receipt | template migration receipt |
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

As a Migration Steward, I want approved ComfyUI JSON templates migrated into worker assets with hashes, compatibility notes, required inputs, output contracts, defects, and eval targets, so that GPU rendering uses governed templates.

**Acceptance Criteria:**

- Given a ComfyUI JSON template is selected, when migration is approved, then the worker asset stores source path, content hash, required inputs, output contract, compatibility notes, known defects, eval target, and reviewer.
- Given a template requires input assets, when validation runs, then the worker checks all typed inputs before queueing.
- Given a template output contract changes, when the worker uses an old template, then the system blocks or requires revalidation.
- Given a template fails eval, when activation is requested, then it remains inactive.
- Given a render uses a template, when receipt is written, then the template hash is included.

**Technical Notes:** Store worker assets under `worker-assets/comfyui-workflows`; connect to MigrationWorkflow and ProviderCapabilityRecord.

**Legacy and Primitive Mapping:** Legacy Inventory CMF engine and ComfyUI templates. Active families: VSG, SAF.

**Prerequisites:** Stories 3.1, 3.2, and 8.4.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
