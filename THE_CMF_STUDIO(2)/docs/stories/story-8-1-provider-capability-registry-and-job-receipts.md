---
story_id: "8.1"
story_title: "Provider Capability Registry and Job Receipts"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-08.01"
pipeline_stage: "11"
entry_object: "provider request"
exit_object: "provider job and receipt"
validation_contract: "capability and cost policy"
required_receipt: "provider receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 8.1: Provider Capability Registry and Job Receipts

**Epic:** 8 - Governed Rendering and Provider Operations
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-08.01 |
| Canonical Pipeline Stage | 11 |
| Entry Object | provider request |
| Exit Object | provider job and receipt |
| Validation Contract | capability and cost policy |
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

As a Production Steward, I want provider jobs and receipts for approved providers and renderers, so that each external or rendering action is auditable, retryable, and cost-visible.

**Acceptance Criteria:**

- Given a provider is configured, when the capability record is activated, then it declares provider name, capability ID, model/workflow version, allowed input types, output contract, cost policy, retry policy, and evaluation requirements.
- Given a provider job is submitted, when it is accepted, then the provider request includes input artifact hashes, prompt hash if applicable, parameters, brand ID, scene ID, and correlation ID.
- Given a provider returns output, when normalized, then the receipt stores output artifact hashes, cost, retries, status, failure details if any, and created domain event.
- Given a provider capability is unavailable, when a job is requested, then the command fails with `PROVIDER_CAPABILITY_UNAVAILABLE`.
- Given a provider webhook arrives, when processed, then it updates provider job state through an approved command path.

**Technical Notes:** Implement `ProviderCapabilityRecord`, `ProviderRequest`, `ProviderResponse`, `ProviderReceipt`, provider adapter interface, and fake provider tests.

**Legacy and Primitive Mapping:** Legacy adapter registry models and receipt chain. Active families: SAF, FBK, BUS.

**Prerequisites:** Epics 1 through 7.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
