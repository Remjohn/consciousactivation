---
story_id: "8.7"
story_title: "Provider Job Retry, Resume, Cancel, and Compensation"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-08.07"
pipeline_stage: "11 / 12"
entry_object: "failed or active provider job"
exit_object: "retry/resume/cancel/compensation state"
validation_contract: "idempotency and duplicate-cost gate"
required_receipt: "recovery receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 8.7: Provider Job Retry, Resume, Cancel, and Compensation

**Epic:** 8 - Governed Rendering and Provider Operations
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-08.07 |
| Canonical Pipeline Stage | 11 / 12 |
| Entry Object | failed or active provider job |
| Exit Object | retry/resume/cancel/compensation state |
| Validation Contract | idempotency and duplicate-cost gate |
| Required Receipt | recovery receipt |
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

As an Operator, I want provider jobs to pause, retry, resume, cancel, or compensate idempotently, so that failures do not corrupt completed work or duplicate cost and publishing side effects.

**Acceptance Criteria:**

- Given a provider timeout occurs, when retry policy allows retry, then only incomplete work is retried and prior receipts remain immutable.
- Given partial output exists, when compensation runs, then completed artifacts are preserved and missing work is isolated.
- Given cancel is requested, when the job is cancellable, then provider state and canonical state are reconciled by receipt.
- Given a duplicate provider webhook arrives, when processed, then idempotency prevents duplicate provider job completion events.
- Given retry would duplicate billing or publishing, when validation runs, then the command is blocked or escalated for manual review.

**Technical Notes:** Durable workflows own provider retries, timeouts, checkpoints, compensation, and terminal failure. Use `provider_jobs`, `operational_incidents`, and `recovery_actions`.

**Legacy and Primitive Mapping:** Legacy circuit-breaker and receipt references. Active families: SAF, FBK, BUS.

**Prerequisites:** Stories 8.1 through 8.6.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
