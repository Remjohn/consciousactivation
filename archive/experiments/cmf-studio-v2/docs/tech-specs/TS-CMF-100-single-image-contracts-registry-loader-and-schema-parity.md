---
tech_spec_id: "TS-CMF-100"
title: "Single Image Contracts, Registry Loader, and Schema Parity"
story_id: "7.27A"
story_title: "Single Image Registry Foundation"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-24"
source_story: "TS-CMF-099 decomposition after audit"
pipeline_stage: "8 / 9 / 10"
entry_object: "AssetPackageItem, BrandContextVersion, SingleImageRegistryBundleSource"
exit_object: "SingleImageRegistryBundle, SingleImageRegistryLoadReceipt, GeneratedSingleImageContracts"
validation_contract: "canonical registry paths, schema parity, registry hash, format compatibility, primitive defaults, provider policy references, generated TypeScript parity"
required_receipt: "SingleImageRegistryLoadReceipt"
runtime_target: "Python / Pydantic v2 / JSON registry loader / TypeScript codegen"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-100: Single Image Contracts, Registry Loader, and Schema Parity

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | Governs 10-section spec shape, backend mapping, primitives, CBAR, acceptance, and tests. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` | Umbrella Single Image/SuperVisual spec being decomposed. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/single_image_composition_models_v2.py` | Source model sketch that must be adapted, not blindly copied. |
| `THE CMF STUDIO/CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE/single_image_render_contracts_v2.ts` | Proof that TypeScript must be generated from Python authority. |
| `THE CMF STUDIO/registries/composition/single_image_composition_registry.v2.json` | Canonical registry of 28 single-image composition contracts. |
| `THE CMF STUDIO/registries/composition/single_image_router_policy.v2.json` | Canonical router policy dependency. |
| `THE CMF STUDIO/registries/composition/single_image_provider_responsibilities.v2.json` | Canonical provider boundary dependency. |
| `THE CMF STUDIO/registries/composition/single_image_skia_component_catalog.v2.json` | Canonical Skia component catalog dependency. |
| `THE CMF STUDIO/registries/composition/single_image_ideogram_prompt_contracts.v2.json` | Canonical Ideogram prompt contract dependency. |
| `THE CMF STUDIO/registries/evals/composition/single_image_eval_rubrics.v2.json` | Canonical eval rubric dependency. |
| `THE CMF STUDIO/docs/content-asset-code-and-format-registry.md` | Defines `SPV-*`, `VPL-*`, `TWQ-*`, `MEM-*`, and `RCT-SEED` subtypes. |

## 2. Overview

This spec owns the foundational contracts and registry loader for all single-image outputs. It does not choose a composition, call providers, render Skia, or approve assets. Its job is to make the engine impossible to start from loose prompts or incomplete registry data.

The loader must treat the migrated bundle files as runtime dependencies only after validation:

```text
canonical registry paths
-> schema validation
-> hash generation
-> cross-file reference validation
-> format compatibility validation
-> primitive default validation
-> generated Python JSON Schema
-> generated TypeScript consumer contracts
-> SingleImageRegistryLoadReceipt
```

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-100-001 | `single_image_composition_registry.v2.json` | Loads 28 composition contracts and validates zones, text budgets, format support, eval profile IDs, provider modes, and primitive defaults. |
| DEP-CMF-100-002 | `single_image_router_policy.v2.json` | Validates hard constraints, weights, penalties, fallback policy, and candidate count rules. |
| DEP-CMF-100-003 | `single_image_provider_responsibilities.v2.json` | Validates allowed/prohibited provider ownership boundaries. |
| DEP-CMF-100-004 | `single_image_skia_component_catalog.v2.json` | Validates that scene specs can reference only registered Skia components. |
| DEP-CMF-100-005 | `single_image_ideogram_prompt_contracts.v2.json` | Validates no final text, handles, stats, dates, or logos are delegated to Ideogram. |
| DEP-CMF-100-006 | `single_image_eval_rubrics.v2.json` | Validates eval profiles, thresholds, hard-fail codes, and repair dimensions. |
| DEP-CMF-100-007 | `GeneratedSingleImageContracts` | Python-generated JSON Schema and TypeScript types. |
| DEP-CMF-100-008 | `SingleImageRegistryLoadReceipt` | Immutable receipt proving the registry bundle is loadable and hashable. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `src/ccp_studio/contracts/single_image.py` | New Pydantic contract module for enums, bounds, zones, text budgets, composition contracts, provider policy refs, registry bundle, and load receipts. |
| `src/ccp_studio/services/single_image_registry_service.py` | New loader that validates all single-image registries and emits `SingleImageRegistryLoadReceipt`. |
| `src/ccp_studio/generated/typescript/` | Generated consumer contracts from Python. Hand-maintained TS semantic authority is disallowed. |
| `src/ccp_studio/services/provider_operations_service.py` | Reads provider policy refs but does not execute provider jobs in this spec. |

### ADR-05 Primitives

The registry loader must validate exact primitive IDs where a composition declares defaults. It must reject fuzzy primitives such as `premium`, `viral`, `clean`, or `smart`.

| Requirement | Primitive Handling |
|---|---|
| Composition defaults | Must be exact registry IDs or registered primitive bundle refs. |
| Format compatibility | Must require later role coverage across meaning, delivery, and format/material. |
| Missing primitive default | Allowed only if router/runtime requires a later primitive triad receipt before render. |

### CBAR Mandate Enforcement

| Mandate | Enforcement |
|---|---|
| Phase1-M05 Deterministic Override | Registry validates provider boundaries so generated tools cannot own final text or geometry. |
| Phase4-M01 Intelligence-Gated Intercept | Engine cannot start without a valid registry bundle and format subtype map. |
| Phase4-M04 Frictionless Block | Invalid registry, zone, text budget, provider role, or eval profile blocks before provider calls. |
| Phase5-M01 Verifiable Artifact | Every registry load emits hashes and source file refs. |

### Technical Decisions

| Decision | Rationale |
|---|---|
| Python/Pydantic is semantic authority. | Runtime contracts and frontend types must not drift. |
| Registries are loaded as a bundle. | Composition, router, provider, Skia, prompt, and eval files must agree. |
| Loader emits receipts. | A rendered SuperVisual must prove which registry bundle was used. |

## 4. Implementation Plan

1. Add `contracts/single_image.py` with registry, policy, and receipt models.
2. Add `SingleImageRegistryService.load_bundle()`.
3. Validate all canonical paths exist.
4. Validate 28 composition IDs are unique.
5. Validate zone bounds are normalized and text budgets are non-negative.
6. Validate eval profile IDs exist in `single_image_eval_rubrics.v2.json`.
7. Validate provider modes map to `single_image_provider_responsibilities.v2.json`.
8. Validate Skia component refs map to `single_image_skia_component_catalog.v2.json`.
9. Generate JSON Schema and TypeScript contracts from Python.
10. Emit `SingleImageRegistryLoadReceipt`.

## 5. Primary Output Schema

```python
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field


class SingleImageRegistryBundle(BaseModel):
    schema_version: Literal["cmf.single_image_registry_bundle.v1"]
    bundle_id: UUID
    composition_registry_hash: str
    router_policy_hash: str
    provider_policy_hash: str
    skia_catalog_hash: str
    ideogram_contract_hash: str
    eval_rubric_hash: str
    composition_count: int = 28
    supported_format_codes: list[str]
    loaded_at_iso: str


class SingleImageRegistryLoadReceipt(BaseModel):
    schema_version: Literal["cmf.single_image_registry_load_receipt.v1"]
    receipt_id: UUID
    bundle: SingleImageRegistryBundle
    source_paths: list[str]
    validation_passed: bool
    generated_schema_refs: list[str]
    generated_typescript_refs: list[str]
    blocker_codes: list[str] = Field(default_factory=list)
```

## 6. Backward Compatibility Fallback

| Condition | Required Fallback |
|---|---|
| Registry path missing | Block with `SINGLE_IMAGE_REGISTRY_BUNDLE_MISSING`. |
| Source bundle path used in production | Block with `SINGLE_IMAGE_SOURCE_BUNDLE_NOT_RUNTIME_TRUTH`. |
| TypeScript contract hand-edited | Block CI with `SINGLE_IMAGE_TYPESCRIPT_PARITY_FAILED`. |
| Eval profile missing | Block with `SINGLE_IMAGE_EVAL_PROFILE_UNKNOWN`. |

## 7. Tasks

| Task | Requirement |
|---|---|
| T100-01 | Add `contracts/single_image.py`. |
| T100-02 | Add registry loader service. |
| T100-03 | Add cross-file registry validator. |
| T100-04 | Add generated JSON Schema and TypeScript parity tests. |
| T100-05 | Add registry load receipt persistence. |

## 8. Acceptance Criteria

| AC | Requirement | Failure Example | CBAR |
|---|---|---|---|
| AC100-01 | All canonical single-image registry files load as one bundle. | Composition registry loads but eval rubrics are missing. | Phase4-M04 |
| AC100-02 | Runtime refuses direct source-bundle reads. | Production service reads from `CCP_SINGLE_IMAGE_POST_ENGINE_V2_BUNDLE`. | Phase5-M01 |
| AC100-03 | Generated TS contracts match Python schemas. | Frontend accepts a field Python rejects. | Phase5-M01 |
| AC100-04 | Provider responsibility policy validates prohibited ownership. | Ideogram is allowed to own final text. | Phase1-M05 |

## 9. Dependencies

| Dependency | Owner |
|---|---|
| Umbrella Single Image spec | `TS-CMF-099` |
| Content asset code registry | `docs/content-asset-code-and-format-registry.md` |
| Single-image registries | `registries/composition/single_image_*`, `registries/evals/composition/single_image_eval_rubrics.v2.json` |
| Generated contract pipeline | Existing CMF Python-to-TypeScript generation pattern |

## 10. Testing Strategy

- Unit tests for every registry file.
- Hash stability snapshot tests.
- Cross-file reference tests.
- Provider responsibility negative tests.
- Generated TypeScript parity tests.
- CI blocker test for source-bundle production reads.
