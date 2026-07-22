---
tech_spec_id: "TS-CMF-042"
title: "Provider Capability Registry and Job Receipts"
story_id: "8.1"
story_title: "Provider Capability Registry and Job Receipts"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-8-1-provider-capability-registry-and-job-receipts.md"
fr_ids:
  - "FR-CMF-08.01"
pipeline_stage: "11"
entry_object: "provider request"
exit_object: "provider job and receipt"
validation_contract: "capability and cost policy"
required_receipt: "provider receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / durable workflows / provider adapters"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-042: Provider Capability Registry and Job Receipts

**Status:** Ready for Development  
**Story:** `8.1 - Provider Capability Registry and Job Receipts`  
**Implementation Boundary:** Provider capability records, provider requests/responses/jobs/receipts, adapter interface, cost/retry/evaluation policy, webhook normalization, and provider-job domain events.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-8-1-provider-capability-registry-and-job-receipts.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-08.01 authority and provider receipt requirements. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Provider stack, Python-first contract doctrine, and GPU/receipt requirements. |
| `docs/architecture.md` | AD-010 Provider Capability Registry and provider replaceability rule. |
| `docs/cmf-studio-pipeline-map.md` | Stage 11 asset research/provider jobs and stage 12 rendering trace. |
| `docs/migration/legacy-inventory.md` | Legacy adapter registry models and receipt chain references. |

## 2. Overview

Implement a Provider Capability Registry so every external model, renderer, transcript provider, publishing adapter, or GPU route is represented by a typed capability record. Domain services cannot call providers directly. They issue `ProviderRequest` objects through provider adapters; adapters normalize responses into `ProviderReceipt` records.

Provider operations must be typed, receipt-backed, idempotent, cost-visible, retryable, and separate from final business decisions. A provider may generate an artifact, but it cannot approve, publish, mutate canonical state, or decide brand truth.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-08.01 | Create provider jobs and receipts for Ideogram 4, GPT Image 2, Flux 2 Klein 9b, Qwen-Image-Layered, SAM3, self-hosted ComfyUI Docker GPU workers, LavaSR, MOSS-TTS, Remotion, and Motion Canvas where applicable. | Capability records, requests, jobs, responses, receipts, adapter interface, webhook command path, cost/retry policy. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 11 - Asset research and provider jobs |
| Entry Object | provider request |
| Exit Object | provider job and receipt |
| Validation Contract | capability and cost policy |
| Required Receipt | provider receipt |

### Legacy Intelligence Mapping

- Legacy `adapter_registry_models.py` and receipt chain inform contracts and fixtures.
- Provider-specific behavior is captured behind adapter interfaces and capability records.
- Superseded execution services are migration context only; production uses approved current provider records.

## 4. Implementation Plan

1. Add contracts for `ProviderCapabilityRecord`, `ProviderRequest`, `ProviderJob`, `ProviderResponse`, `ProviderReceipt`, and `ProviderWebhookEnvelope`.
2. Add SQLAlchemy tables for provider capabilities, jobs, receipts, webhooks, costs, and retry state.
3. Implement adapter interface with validation hooks for input artifact hashes, prompt hashes, model/workflow version, parameters, brand ID, scene ID, and correlation ID.
4. Enforce capability availability, cost policy, retry policy, and evaluation requirement before job submission.
5. Normalize provider webhooks through Command Bus commands only.
6. Emit domain events only after receipt validation succeeds.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ProviderJobStatus(str, Enum):
    REQUESTED = "requested"
    SUBMITTED = "submitted"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProviderCapabilityRecord(BaseModel):
    provider_capability_id: str
    provider_name: str
    capability_name: str
    model_or_workflow_version: str
    allowed_input_types: list[str]
    output_contract: str
    cost_policy_id: str
    retry_policy_id: str
    evaluation_requirement_ids: list[str]
    active: bool


class ProviderRequest(BaseModel):
    provider_request_id: str
    provider_capability_id: str
    brand_id: str
    complete_editing_session_id: str | None = None
    scene_spec_id: str | None = None
    input_artifact_hashes: list[str]
    prompt_hash: str | None = None
    parameters: dict
    idempotency_key: str


class ProviderReceipt(BaseModel):
    provider_receipt_id: str
    provider_job_id: str
    status: ProviderJobStatus
    output_artifact_hashes: list[str] = []
    cost_amount: float | None = None
    retry_count: int = 0
    failure_code: str | None = None
    created_at: datetime
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `ActivateProviderCapabilityCommand`, `SubmitProviderJobCommand`, `NormalizeProviderResponseCommand`, `ProcessProviderWebhookCommand`, `FailProviderCapabilityUnavailableCommand`, `ValidateProviderReceiptCommand` |
| Events | `ProviderCapabilityActivated`, `ProviderJobSubmitted`, `ProviderResponseNormalized`, `ProviderWebhookProcessed`, `ProviderReceiptValidated`, `ProviderJobCompleted` |
| Workflow | `ProviderJobWorkflow.stage11_provider_execution` |
| Receipt | `ProviderReceipt` with capability, request, response, output hashes, cost, retry, status, and failure details |

## 7. Backward Compatibility and Migration Fallback

Legacy adapter records may seed capability records and fake-provider fixtures. Direct SDK calls from domain services are not allowed. If no active capability exists, the job is blocked with `PROVIDER_CAPABILITY_UNAVAILABLE`.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Provider power vs. business authority | Providers produce artifacts and receipts only. | Approval/publishing commands require human/domain gates. |
| Cost speed vs. duplicate spend | Idempotency key and cost policy required before submission. | Duplicate webhook does not create duplicate completion. |
| Multi-provider flexibility vs. drift | Capability record pins provider/model/workflow/output contract. | Receipt stores capability and output hashes. |

## 9. Tasks

- Add provider contracts and persistence.
- Implement adapter interface and fake provider.
- Add capability/cost/retry/evaluation validation.
- Add webhook normalization.
- Add receipt validator and event outbox integration.
- Add API endpoints under `/api/v1/provider-jobs`.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Active capability declares provider, version, inputs, output, cost, retry, evaluation. | Provider record lacks output contract. |
| AC2 | Submitted request includes hashes, prompt hash when applicable, params, brand, scene, correlation. | Provider called with raw prompt only. |
| AC3 | Receipt stores outputs, cost, retries, status, failures, event. | Output URL stored without hash/cost. |
| AC4 | Unavailable capability fails. | Inactive provider accepts job. |
| AC5 | Webhook updates state via command path. | Webhook mutates DB directly. |

## 11. Dependencies

- TS-CMF-001 Command Bus.
- TS-CMF-002 orchestration records.
- TS-CMF-037 RenderContract.
- TS-CMF-038 CompositionJob lineage.
- TS-CMF-039 assembly plan receipts.

## 12. Testing Strategy


Unit tests:

- Unit tests for capability/request/receipt models.
- Adapter contract tests with fake provider.
- Command tests for unavailable capability and cost policy blocks.
- Webhook idempotency tests.
- Receipt validation tests for missing metadata and missing output hashes.

Integration tests:

- Workflow test from `provider request` to `provider job and receipt` through pipeline stage `11`.
- Command Bus test proving `provider receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for provider jobs by status, provider cost, retries, failures, webhook duplicates, and capability blocks.
- Logs include provider capability ID, provider job ID, correlation ID, idempotency key, and receipt ID.
- Recovery: retry or compensate through ProviderJobWorkflow; receipts stay immutable.
- Rollback: mark job failed/cancelled and supersede dependent draft artifacts.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 14. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-042 |
| Story | 8.1 |
| Requirement Trace | FR-CMF-08.01 |
| Pipeline Trace | Stage 11, provider request to provider job and receipt |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No hidden provider scripts, no direct SDK domain calls, no receipt-free outputs |

