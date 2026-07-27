---
tech_spec_id: "TS-CMF-044"
title: "Generative Provider Adapters"
story_id: "8.3"
story_title: "Generative Provider Adapters"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-8-3-generative-provider-adapters.md"
fr_ids:
  - "FR-CMF-08.03"
pipeline_stage: "11"
entry_object: "generative provider request"
exit_object: "generated/edited asset"
validation_contract: "provider metadata and consent compatibility"
required_receipt: "provider receipt"
runtime_target: "Python / provider adapters / Pydantic v2 / object storage / durable workflows"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-044: Generative Provider Adapters

**Status:** Ready for Development  
**Story:** `8.3 - Generative Provider Adapters`  
**Implementation Boundary:** GPT Image 2, Flux 2 Klein 9b, Qwen-Image-Layered, SAM3, LavaSR, and MOSS-TTS adapter contracts, metadata capture, consent compatibility, raw output storage, and receipt validation.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-8-3-generative-provider-adapters.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-08.03 authority and current provider names. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Provider stack and ImageCritic repair pipeline. |
| `docs/architecture.md` | Provider replaceability and capability records. |
| `docs/cmf-studio-pipeline-map.md` | Stage 11 provider jobs and stage 12 rendering. |
| `docs/migration/legacy-inventory.md` | Visual research references, Voice DNA, and adapter registry guidance. |

## 2. Overview

Implement generative provider adapters behind the common Provider Capability Registry. GPT Image 2 and Flux 2 Klein 9b support asset generation, identity-preserving edits, local repair, and production refinement. Qwen-Image-Layered and SAM3 support layer decomposition, segmentation, and tracking. LavaSR restores audio, and MOSS-TTS may create governed Voice-DNA Boost bridges under strict eligibility gates.

Each adapter must preserve input artifact hashes, prompt hash, provider/model metadata, parameters, seed/config values when available, output hashes, costs, retries, evaluation state, and consent compatibility.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-08.03 | Route special or generative assets through approved provider adapters while preserving prompt hashes, model/provider metadata, seed/config values when available, input assets, outputs, costs, retries, and evaluation state. | Adapter contracts, metadata capture, consent compatibility gate, raw output storage, provider receipt validation, evaluation promotion guard. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 11 - Asset research and provider jobs |
| Entry Object | generative provider request |
| Exit Object | generated/edited asset |
| Validation Contract | provider metadata and consent compatibility |
| Required Receipt | provider receipt |

### Legacy Intelligence Mapping

- Provider adapters replace hidden scripts and direct model calls.
- Legacy visual research and Voice DNA assets inform evals and compatibility fixtures.
- Voice-DNA Boost remains governed by consent and semantic limits from Epic 2.

## 4. Implementation Plan

1. Add `GenerativeProviderRequest`, `GenerativeProviderOutput`, `ProviderMetadata`, and adapter-specific parameter contracts.
2. Implement adapters behind `ProviderAdapter` interface.
3. Enforce input artifact hash, consent compatibility, provider capability, cost policy, and evaluation target before submission.
4. Store raw outputs under `brands/{brand_id}/provider-raw/` with output hashes and provider receipt.
5. Prevent failed evaluation outputs from promotion to approved render output.
6. Fail receipt validation when model/provider metadata is missing.

## 5. Primary Output Schema

```python
from pydantic import BaseModel


class ProviderMetadata(BaseModel):
    provider_name: str
    model_or_workflow_version: str
    seed: str | None = None
    config_values: dict = {}
    provider_response_id: str | None = None


class GenerativeProviderRequest(BaseModel):
    provider_request_id: str
    provider_capability_id: str
    brand_id: str
    purpose: str
    input_artifact_hashes: list[str]
    prompt_hash: str | None = None
    parameters: dict
    consent_record_version_ids: list[str] = []


class GenerativeProviderOutput(BaseModel):
    provider_output_id: str
    provider_job_id: str
    raw_output_uri: str
    output_hash: str
    metadata: ProviderMetadata
    evaluation_state: str
    promoted_asset_id: str | None = None
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `SubmitGenerativeProviderJobCommand`, `ValidateGenerativeProviderConsentCommand`, `NormalizeGenerativeProviderOutputCommand`, `EvaluateGeneratedAssetCommand`, `BlockGeneratedAssetPromotionCommand` |
| Events | `GenerativeProviderJobSubmitted`, `GenerativeProviderConsentValidated`, `GenerativeProviderOutputNormalized`, `GeneratedAssetEvaluated`, `GeneratedAssetPromotionBlocked` |
| Workflow | `ProviderJobWorkflow.stage11_generative_provider_adapter` |
| Receipt | `ProviderReceipt` plus adapter metadata, input/output hashes, consent refs, evaluation state, and promotion state |

## 7. Backward Compatibility and Migration Fallback

Legacy provider scripts and visual research logic can become adapter fixtures. Domain code never calls provider SDKs directly. Unsupported provider metadata or missing output contract blocks receipt creation.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Generative speed vs. consent | Source assets require consent compatibility before submission. | Provider receipt stores consent refs. |
| Provider output vs. approved asset | Output must pass evaluation before promotion. | Evaluation state gates promoted asset ID. |
| Model drift vs. reproducibility | Metadata and prompt/config hashes are required. | Receipt validation fails without model metadata. |

## 9. Tasks

- Add generative adapter contracts.
- Implement adapters for approved providers.
- Add consent and cost policy guards.
- Add raw output storage and hash validation.
- Add evaluation promotion guard.
- Add tests for metadata, consent, and missing receipt fields.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Approved providers pass through adapter/capability record. | Domain service calls provider directly. |
| AC2 | Source inputs store artifact hashes and consent compatibility. | Likeness source used without consent ref. |
| AC3 | Output stored under provider-raw with hash/receipt. | Output is copied directly into final asset path. |
| AC4 | Failed evaluation output is not promoted. | Drifted image becomes approved render output. |
| AC5 | Missing model metadata fails receipt validation. | Receipt has no provider/model version. |

## 11. Dependencies

- TS-CMF-042 Provider Capability Registry.
- TS-CMF-008 and TS-CMF-010 consent governance.
- TS-CMF-011 Voice-DNA Boost eligibility.
- TS-CMF-038 CompositionJob lineage.
- TS-CMF-039 assembly manifests.

## 12. Testing Strategy

Unit tests:

- Adapter request and response contract validation with fake provider responses.
- Consent compatibility validation for input source assets.
- Provider metadata validation.
- Object storage hash validation.

Integration tests:

- Provider job submission through capability registry and typed adapter boundary.
- Provider receipt persistence with raw output, transformed output, metadata, and object hash.
- Evaluation promotion guard blocking unapproved provider outputs.

Eval tests:

- Fixture comparisons for GPT Image 2, Flux 2 Klein 9b, Qwen-Image-Layered, SAM3, and ComfyUI Docker GPU worker response normalization.

## 13. Observability, Recovery, and Rollback

- Metrics for provider submissions, output failures, consent blocks, evaluation failures, and promotion blocks.
- Logs include provider capability ID, provider job ID, input hashes, output hash, and metadata.
- Recovery: retry provider job or route output to repair.
- Rollback: revoke promotion and retain raw output receipt for audit.

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
| Tech Spec ID | TS-CMF-044 |
| Story | 8.3 |
| Requirement Trace | FR-CMF-08.03 |
| Pipeline Trace | Stage 11, generative provider request to generated/edited asset |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No hidden scripts, no missing provider metadata, no evaluation-bypassing promotion |
