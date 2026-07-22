---
tech_spec_id: "TS-CMF-111"
title: "2D Character Provider Adapters, Rig Authoring, and Asset Promotion"
story_id: "7.27"
story_title: "2D Character Provider Adapters"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-25"
source_story: "CCP 2D Character Animation Engine V1 bundle provider and rigging integration"
pipeline_stage: "4 / 8 / 10 / 11"
entry_object: "CharacterGenesisRequest, CharacterIdentityPack, CharacterArtVersion, ProviderCapabilityRegistry"
exit_object: "CharacterProviderJobPlan, LayeredCharacterAssetCandidate, RigAuthoringProject, RigExportBundle, ProviderAdapterReceipt"
validation_contract: "provider boundary, license readiness, reproducibility, asset hashes, semantic layer integrity, rig authoring parity, promotion gate"
required_receipt: "ProviderAdapterReceipt"
runtime_target: "Python / Pydantic v2 / provider adapters / object storage / Stretchy Studio adapter / Spine-compatible export"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-111: 2D Character Provider Adapters, Rig Authoring, and Asset Promotion

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Mandatory CMF/ERA3 format and backend integration protocol. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/02_PIPELINE_AND_PROVIDER_ROLES.md` | Defines provider boundaries for See-Through, Qwen-Image-Layered, SAM3, GPT Image/Flux, Stretchy Studio, Spine, Motion Canvas, Remotion, and FFmpeg. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/03_RIGGING_AND_ASSET_CONTRACTS.md` | Defines PSD normalization, layer graph, bone graph, mesh bundle, masks, shape keys, hand/mouth/gaze libraries, skins, and rig release gates. |
| `THE CMF STUDIO/CCP_2D_CHARACTER_ANIMATION_ENGINE_V1_BUNDLE/ccp_2d_character_engine_v1/registries/provider_responsibilities.json` | Machine-readable provider responsibility boundaries. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-042-provider-capability-registry-and-job-receipts.md` | Provider capability and job receipt dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-044-generative-provider-adapters.md` | Existing generative provider adapter boundary. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-076-open-source-integration-adapter-evaluation-and-import-plan.md` | Requires license, security, reproducibility, and doctrine fit checks before open-source-inspired adapter use. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-089-generative-asset-factory-layer-extraction-and-repair-queue.md` | Existing Qwen/SAM3/layer extraction and repair dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-093-animation-studio-migration-and-operator-rig-editor.md` | Operator rig editor dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-110-two-d-character-engine-object-model-and-character-genesis.md` | Upstream object model and Character Genesis dependency. |

## 2. Overview

This spec defines the provider adapter and asset promotion layer for the 2D Character Engine. It turns external or open-source-inspired tools into bounded CMF workers. Providers execute transformations; they do not own character truth, identity approval, rig approval, semantic interpretation, or final production release.

The provider map is:

| Provider | CMF Role |
|---|---|
| See-Through-style decomposition | Candidate layered PSD, masks, depth, hidden-region proposal for supported illustration/anime-like assets. |
| Qwen-Image-Layered | Mixed-media and semantic RGBA layer decomposition for photo-paper-cut and generated scenes. |
| SAM3 | Precise segmentation, alpha cleanup, hand/prop isolation, mask generation, background removal, and tracking. |
| GPT Image 2 / Flux 2 Klein | Rig-aware master art candidates, identity-preserving edits, hidden-region repair, costume/hand variants, paper texture harmonization. |
| Stretchy Studio adapter | Authoring import/export, hierarchy normalization, pivot editing, rigging, mesh generation, shape-key authoring, audio-synced preview, runtime export. |
| Spine-compatible compiler/runtime | Production-grade bone, slot, skin, mesh, deform, clipping, IK, and layered playback export. |

This spec makes provider outputs auditable, promotable, and reversible.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-107-001 | `ProviderCapabilityRegistry` | Declares which provider roles are available, licensed, enabled, and allowed in production. |
| DEP-CMF-107-002 | `CharacterProviderJobPlan` | Specifies provider role, input refs, output contract, deterministic settings, expected artifacts, and approval target. |
| DEP-CMF-107-003 | `ProviderJobReceipt` | Records provider version, model/version ID, input hashes, output hashes, runtime config, errors, and cost. |
| DEP-CMF-107-004 | `LayeredCharacterAssetCandidate` | Candidate layers, masks, depth, hidden regions, draw order, alpha quality, and semantic grouping. |
| DEP-CMF-107-005 | `RigAuthoringProject` | Authoring artifact that may exist as `.stretch`, Spine project, or CMF-native rig workspace. |
| DEP-CMF-107-006 | `RigExportBundle` | Runtime export sidecars, atlas/textures, skeleton, mesh, constraints, and version metadata. |
| DEP-CMF-107-007 | `AssetPromotionDecision` | Operator and automated gate result deciding whether a candidate becomes a locked CMF version. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/provider_operations.py` | Add character-provider job role enums and receipts. |
| `src/ccp_studio/services/provider_operations_service.py` | Register and validate character provider capabilities. |
| `src/ccp_studio/services/character_provider_router.py` | New router that selects See-Through, Qwen, SAM3, GPT Image 2, Flux 2 Klein, Stretchy, or Spine-compatible jobs. |
| `src/ccp_studio/services/character_asset_promotion_service.py` | New service that promotes candidates into locked CMF versions only after gates pass. |
| `src/ccp_studio/services/rig_validation_service.py` | Runs rig parity and release checks after authoring/export. |
| `src/ccp_studio/services/open_source_adapter_evaluation_service.py` | Applies `TS-CMF-076` license, security, sandbox, and doctrine-fit checks. |
| Object storage | Stores provider inputs, outputs, candidate layers, masks, `.stretch` projects, Spine bundles, previews, and hashes. |

### ADR-05 Primitives

Provider routing must preserve primitive intent:

| Role | Required Proof |
|---|---|
| Meaning transform | Provider output must support the intended teaching, witnessing, contrast, or reaction operation. |
| Delivery shape | Provider output must improve layer, rig, gaze, gesture, prop, or readable motion capability. |
| Format material | Provider output must preserve PaperCut, avatar, or mixed-media materiality required by the route. |

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase4-M01 Intelligence-Gated Intercept | Provider jobs cannot run without declared role, input refs, output contract, capability, and promotion target. |
| Phase4-M04 Frictionless Block | Missing provider capability, license uncertainty, missing input hashes, or unsupported asset type blocks before job execution. |
| Phase4-M05 Actionable Rejection | Provider failure names provider role, artifact, gate, and repair path. |
| Phase5-M01 Verifiable Artifact | Every provider output must be reconstructable from job plan, receipt, input hash, output hash, and runtime config. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Providers have narrow roles. | Prevents a single model/tool from silently replacing CMF orchestration and approval. |
| Stretchy projects are authoring artifacts. | `.stretch` files can aid rigging but cannot become semantic source of truth. |
| See-Through is not universal. | It is useful for supported illustration/anime-like assets but risky for photo-paper-cut or mixed media. |
| Qwen and SAM3 are complementary. | Qwen proposes semantic layers; SAM3 refines masks and segmentation. |
| Spine-compatible export is a runtime target, not a doctrine. | Runtime performance matters, but CMF contracts own meaning, identity, and approval. |
| Asset promotion is explicit. | Candidate outputs can be repaired, rejected, or promoted with receipts. |

### Gate Thresholds and Verdicts

Provider adapter gates must produce numeric verdicts before promotion. Where a provider output feeds Character Genesis, the source bundle gates from `registries/eval_gates.json` remain authoritative.

| Gate ID | Threshold | Hard Fail | Downstream Consequence |
|---|---:|---|---|
| `provider_capability_ready` | 1.00 | Yes | Blocks provider job planning. |
| `provider_license_security_ready` | 1.00 | Yes | Blocks adapter execution. |
| `provider_input_hash_completeness` | 1.00 | Yes | Blocks provider execution. |
| `provider_output_hash_completeness` | 1.00 | Yes | Blocks candidate registration. |
| `semantic_layer_correctness` | 0.92 | Yes | Blocks layered asset promotion. |
| `hidden_region_completeness` | 0.88 | Yes | Blocks rig authoring. |
| `alpha_quality_score` | 0.90 | Yes | Blocks mask-dependent promotion. |
| `runtime_export_parity` | 0.94 | Yes | Blocks runtime export promotion. |

All provider gates are hard-fail unless explicitly reclassified by a future adapter audit. No provider result may enter production through a provisional provider verdict; provisional status is allowed only after the candidate has been registered for operator inspection.

## 4. Implementation Plan

1. Add provider role enums for `character_master_art`, `character_layer_decomposition`, `character_mask_refinement`, `character_hidden_region_repair`, `character_rig_authoring`, and `character_runtime_export`.
2. Add `CharacterProviderJobPlan`, `LayeredCharacterAssetCandidate`, `RigAuthoringProject`, `RigExportBundle`, `AssetPromotionDecision`, and `ProviderAdapterReceipt`.
3. Add `character_provider_router.py` with routing rules by source asset type, target style, materiality, provider capability, and doctrine requirements.
4. Add See-Through adapter contract for supported illustration decomposition only.
5. Add Qwen-Image-Layered adapter contract for mixed-media layered extraction.
6. Add SAM3 adapter contract for mask refinement, background removal, alpha cleanup, and tracked cutouts.
7. Add GPT Image 2 / Flux 2 Klein repair and variant job contracts.
8. Add Stretchy Studio import/export adapter contract, including `.stretch` artifact retention and CMF contract translation.
9. Add Spine-compatible export validation for skeleton, atlas, meshes, constraints, and runtime parity.
10. Add promotion workflow that creates a locked CMF object only after automated gates and operator approval.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


ProviderRole = Literal[
    "character_master_art",
    "character_layer_decomposition",
    "character_mask_refinement",
    "character_hidden_region_repair",
    "character_rig_authoring",
    "character_runtime_export",
]


class CharacterProviderJobPlan(BaseModel):
    schema_version: Literal["cmf.character_provider_job_plan.v1"]
    job_plan_id: UUID
    workspace_id: UUID
    provider_role: ProviderRole
    provider_capability_id: str
    input_asset_refs: list[str]
    input_hashes: dict[str, str]
    output_contract: str
    deterministic_config: dict
    promotion_target: Literal[
        "character_art_version",
        "layered_character_asset_version",
        "character_rig_version",
        "performance_library_version",
        "candidate_only",
    ]


class LayeredCharacterAssetCandidate(BaseModel):
    schema_version: Literal["cmf.layered_character_asset_candidate.v1"]
    candidate_id: UUID
    job_plan_id: UUID
    psd_ref: str | None = None
    layer_manifest_ref: str
    mask_bundle_ref: str
    depth_map_ref: str | None = None
    hidden_region_report_ref: str | None = None
    alpha_quality_score: float = Field(ge=0.0, le=1.0)
    semantic_layer_coverage_score: float = Field(ge=0.0, le=1.0)
    blocker_codes: list[str]


class RigAuthoringProject(BaseModel):
    schema_version: Literal["cmf.rig_authoring_project.v1"]
    rig_authoring_project_id: UUID
    layered_asset_candidate_id: UUID
    authoring_tool: Literal["stretchy_studio", "spine", "cmf_native", "manual_import"]
    authoring_artifact_ref: str
    translated_contract_ref: str
    project_hash: str


class RigExportBundle(BaseModel):
    schema_version: Literal["cmf.rig_export_bundle.v1"]
    rig_export_bundle_id: UUID
    rig_authoring_project_id: UUID
    skeleton_ref: str
    atlas_ref: str | None = None
    texture_refs: list[str]
    mesh_bundle_ref: str
    constraint_bundle_ref: str
    runtime_version: str
    export_hashes: dict[str, str]
    parity_preview_refs: list[str]


class ProviderAdapterReceipt(BaseModel):
    schema_version: Literal["cmf.character_provider_adapter_receipt.v1"]
    receipt_id: UUID
    job_plan_id: UUID
    provider_job_receipt_ref: str
    output_refs: list[str]
    output_hashes: dict[str, str]
    promotion_decision_ref: str | None = None
    blocker_codes: list[str]
```

## 6. Backward Compatibility Fallback

| Condition | Fallback |
|---|---|
| See-Through unsupported asset type | Route to Qwen/SAM3 or block with `SEE_THROUGH_UNSUPPORTED_ASSET_TYPE`. |
| Qwen unavailable for mixed-media layer extraction | Block layer-dependent route with `QWEN_LAYERED_CHARACTER_REQUIRED`. |
| SAM3 mask refinement unavailable | Permit draft concept only; block lock with `SAM3_MASK_REQUIRED`. |
| Stretchy adapter unavailable | Allow manual rig import if it produces CMF contract parity and passes gates. |
| Spine export license/runtime is not approved | Use precomposed RGBA plate path or block production with `SPINE_RUNTIME_NOT_APPROVED`. |
| Provider output lacks hashes | Reject output with `PROVIDER_OUTPUT_HASH_MISSING`. |

## 7. Tasks

| Task | Implementation Requirement |
|---|---|
| T107-01 | Add character provider role enums and provider job plan contracts. |
| T107-02 | Register provider capabilities and license/security status. |
| T107-03 | Implement character provider router with source-type and doctrine-aware routing. |
| T107-04 | Add See-Through, Qwen, SAM3, GPT Image 2, Flux 2 Klein, Stretchy, and Spine-compatible adapter contracts. |
| T107-05 | Add candidate asset promotion workflow and receipt chain. |
| T107-06 | Add provider output hash and schema validation. |
| T107-07 | Add rig export parity validation. |
| T107-08 | Add negative fixtures for unsupported provider misuse. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | Mandate |
|---|---|---|---|
| AC107-01 | Every provider job has role, capability, input refs, output contract, config, and promotion target. | A model call returns layers with no typed job plan. | Phase4-M01 |
| AC107-02 | Providers cannot approve identity, rig, or production release. | See-Through output becomes final rig without operator approval. | Phase5-M01 |
| AC107-03 | See-Through route is blocked for unsupported photo-paper-cut assets. | A realistic portrait is forced through illustration decomposition and loses facial structure. | Phase4-M04 |
| AC107-04 | Qwen/SAM3 outputs are validated separately. | A semantic layer result with poor alpha masks is promoted without mask QC. | Phase4-M05 |
| AC107-05 | Stretchy and Spine artifacts translate into CMF contracts. | A `.stretch` file is stored but no CMF rig contract exists. | Phase5-M01 |
| AC107-06 | Asset promotion requires provider receipt, output hashes, eval status, and approval status. | A repair image is silently used as a costume skin. | Phase5-M01 |

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| `TS-CMF-042` | Internal | Provider registry and receipts. |
| `TS-CMF-044` | Internal | Generative provider adapters. |
| `TS-CMF-076` | Internal | Open-source adapter evaluation and import plan. |
| `TS-CMF-089` | Internal | Layer extraction and repair queue. |
| `TS-CMF-093` | Internal | Operator rig editor. |
| `TS-CMF-110` | Internal | Character object model and genesis lifecycle. |
| See-Through | External/reference | Layered illustration decomposition. |
| Qwen-Image-Layered | External/provider | Semantic RGBA layer extraction. |
| SAM3 | External/provider | Precise masks, tracking, alpha cleanup. |
| GPT Image 2 / Flux 2 Klein | External/provider | Candidate creation and repair. |
| Stretchy Studio | External/reference | Rig authoring adapter. |
| Spine-compatible runtime | External/runtime | Production rig playback/export target. |

## 10. Testing Strategy

- Unit test provider role validation and output contract validation.
- Test unsupported provider routing decisions for See-Through, Qwen, SAM3, Stretchy, and Spine-compatible paths.
- Run hash integrity tests for every provider input and output.
- Run license/security readiness tests through `TS-CMF-076` rules.
- Run layer candidate tests for semantic coverage, alpha quality, draw order, hidden regions, and mask readiness.
- Run rig authoring translation tests from sample Stretchy/Spine-like artifacts into CMF contracts.
- Run promotion tests proving candidate artifacts cannot become locked versions without receipts, gates, and approval.
- Run workflow resume tests after failed provider jobs and repaired provider jobs.
