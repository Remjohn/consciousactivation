---
tech_spec_id: "TS-CMF-020"
title: "Paper-Cut Rig and Creative Libraries"
story_id: "4.3"
story_title: "Paper-Cut Rig and Creative Libraries"
epic_id: 4
epic_title: "Brand Genesis and Locked Creative Universe"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-4-3-paper-cut-rig-and-creative-libraries.md"
fr_ids:
  - "FR-CMF-04.03"
  - "FR-CMF-04.04"
  - "FR-CMF-04.05"
pipeline_stage: "2"
entry_object: "creative generation request"
exit_object: "rig and creative libraries"
validation_contract: "layer/anchor/preview validation"
required_receipt: "creative library receipt"
runtime_target: "Python / Pydantic v2 / object storage / renderer preview contracts"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-020: Paper-Cut Rig and Creative Libraries

**Status:** Ready for Development  
**Story:** `4.3 - Paper-Cut Rig and Creative Libraries`  
**Implementation Boundary:** Rig manifest, layer validation, preview tests, props, micro-semiotic anchors, motion recipes, SFX, composition preferences, platform profiles, and creative library receipts.

## 1. Files Read

| File | Use in This Spec |
|---|---|
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Paper-cut rig, micro-semiotic anchors, ImageCritic, and creative substrate rules. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-04.03, FR-CMF-04.04, and FR-CMF-04.05 source authority. |
| `THE CMF STUDIO/CCP_CMF_Brand_Genesis_and_Micro_Semiotic_Pipeline_V3.md` | Paper-cut avatar system, rig manifest, preview tests, props, micro-semiotic doctrine, motion, SFX, and platform profile details. |
| `docs/architecture.md` | Architecture authority for rig manifests, creative libraries, object storage, and renderer boundaries. |
| `docs/cmf-studio-pipeline-map.md` | Stage 2 Brand Genesis trace. |
| `docs/migration/legacy-inventory.md` | Creative subsystem and CMF engine references as migration context. |
| `docs/stories/story-4-3-paper-cut-rig-and-creative-libraries.md` | Story acceptance criteria and handoff requirements. |
| `docs/tech-specs/TS-CMF-019-64-state-acting-library.md` | Acting library dependency. |

## 2. Overview

### Problem Statement

A paper-cut avatar cannot remain a flat image if it must animate deterministically. It needs layer separation, pivot points, mouth shapes, eye/brow variants, gesture variants, body layers, and preview validation. The same Brand Context must also carry props, micro-semiotic anchors, motion recipes, SFX, composition preferences, platform profiles, and publishing profiles.

### Solution

Implement rig and creative library contracts with evaluation and preview gates. Creative library items are brand-scoped, version-hashed, source-linked, constrained, and evaluated. Platform profiles provide downstream render contracts with caption, negative-space, aspect, and publishing requirements.

### Scope

In scope:

- `RigManifest`, `RigLayer`, `RigPreviewTest`, `MicroSemioticAnchor`, `MotionRecipe`, `SfxAsset`, `CompositionPreference`, `PlatformProfile`, and `CreativeLibraryReceipt`.
- Rig validation for mouth, pivot, layer, and gesture failures.
- Source, version hash, use constraints, and evaluation state for each creative item.
- Brand-scope validation for creative library selection.

Out of scope:

- Full renderer implementation.
- Provider-specific asset generation internals.
- Publishing adapter execution.

## 3. Context for Development

### Requirement Trace

| FR ID | Requirement | Enforcement Mechanism |
|---|---|---|
| FR-CMF-04.03 | Operators generate, evaluate, repair, approve, and lock a paper-cut avatar rig with layer separation, pivot points, mouth shapes, eye/brow variants, gesture variants, body layers, preview tests, and rig manifest. | `RigManifest`, preview tests, repair/reject/approve commands, and rig lock receipt. |
| FR-CMF-04.04 | Operators govern props, micro-semiotic anchors, motion recipes, SFX, composition, platform, and publishing profiles. | Creative library contracts, version hashes, use constraints, and platform profile inheritance. |
| FR-CMF-04.05 | System scores generated references for likeness, gesture clarity, hand quality, paper texture, style adherence, negative space, and usability. | Evaluation receipts and preview gate outcomes attached to rig and library items. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | `2 - Brand Genesis` |
| Entry Object | Creative generation request |
| Exit Object | Rig and creative libraries |
| Allowed Actors / Services | Operator, BrandGenesisWorkflow, RigValidationService, EvaluationService, RendererPreviewService |
| Validation Contract | Layer, anchor, and preview validation |
| Required Receipt | Creative library receipt |
| Forbidden Shortcut | Flat avatar asset without rig manifest, creative item without source/version/eval state, cross-brand library reuse |

### Legacy Intelligence Mapping

Brand Genesis V3, Creative Pipeline V2, and legacy CMF references provide orchestration logic and fixture targets. Runtime implementation remains Python/Pydantic. Renderer preview contracts are generated from Python contracts; Remotion or Motion Canvas do not define brand truth.

Target modules:

- `ccp_studio.contracts.rig_manifest`
- `ccp_studio.contracts.creative_libraries`
- `ccp_studio.services.rig_validation_service`
- `ccp_studio.services.creative_library_service`
- `ccp_studio.workflows.brand_genesis`
- `ccp_studio.repositories.rig_manifests`
- `ccp_studio.repositories.creative_library_items`

### Architecture Component Map

| Component | Responsibility |
|---|---|
| `RigManifest` | Layer, pivot, mouth, eye/brow, gesture, body, and preview metadata. |
| `RigPreviewTest` | Validation for mouth, pivot, layer, gesture, and renderer preview behavior. |
| `MicroSemioticAnchor` | Culturally specific cue with risk, subtlety, comment potential, and use constraints. |
| `MotionRecipe` | Approved motion pattern for paper-cut animation. |
| `SfxAsset` | Approved sonic cue with use context and provenance. |
| `PlatformProfile` | Caption, negative-space, aspect, and publishing requirements inherited by render contracts. |

## 4. Implementation Plan

### Workstream A: Contracts

Define rig, creative library, anchor, motion, SFX, composition, platform, and receipt contracts.

### Workstream B: Rig Preview Validation

Implement preview validation and failure categories for mouth, pivot, layer, gesture, body, and renderer route readiness.

### Workstream C: Creative Libraries

Store props, anchors, motion recipes, SFX, composition preferences, platform profiles, and publishing profiles with source refs, version hashes, constraints, and evaluation state.

### Workstream D: Brand Scope Enforcement

Prevent cross-brand creative library selection.

### Workstream E: Renderer Contract Hooks

Expose platform profile and creative library data to downstream SceneSpec/RenderContract compilers.

## 5. Primary Output Schema

```python
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class CreativeItemStatus(str, Enum):
    draft = "draft"
    evaluation_failed = "evaluation_failed"
    approved = "approved"
    locked = "locked"
    rejected = "rejected"


class RigLayer(BaseModel):
    schema_version: Literal["cmf.rig_layer.v1"]
    layer_name: str
    asset_uri: str
    pivot_points: dict[str, tuple[float, float]] = Field(default_factory=dict)
    layer_hash: str


class RigPreviewTest(BaseModel):
    schema_version: Literal["cmf.rig_preview_test.v1"]
    test_name: str
    passed: bool
    failure_category: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)


class RigManifest(BaseModel):
    schema_version: Literal["cmf.rig_manifest.v1"]
    rig_manifest_id: UUID
    brand_id: UUID
    acting_library_version_id: UUID
    layers: list[RigLayer]
    mouth_shape_refs: list[str]
    eye_brow_variant_refs: list[str]
    gesture_variant_refs: list[str]
    body_layer_refs: list[str]
    preview_tests: list[RigPreviewTest]
    version_hash: str
    status: CreativeItemStatus


class MicroSemioticAnchor(BaseModel):
    schema_version: Literal["cmf.micro_semiotic_anchor.v1"]
    micro_semiotic_anchor_id: UUID
    brand_id: UUID
    name: str
    category: str
    cultural_context: str
    subtlety_score: float
    comment_potential_score: float
    legal_risk_score: float
    use_constraints: list[str] = Field(default_factory=list)
    version_hash: str
    status: CreativeItemStatus
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Required Items |
|---|---|
| Commands | `GenerateRigManifestCommand`, `RunRigPreviewTestsCommand`, `RepairRigCommand`, `ApproveRigCommand`, `CreateCreativeLibraryItemCommand`, `ApproveCreativeLibraryItemCommand`, `ConfigurePlatformProfileCommand` |
| Events | `RigManifestCreated`, `RigPreviewFailed`, `RigApproved`, `CreativeLibraryItemApproved`, `PlatformProfileConfigured` |
| Workflows | Rig generation workflow, creative library approval workflow, platform profile workflow |
| Receipts | `CreativeLibraryReceipt`, `RigPreviewReceipt`, `EvaluationReceipt`, `ApprovalReceipt` |

## 7. Backward Compatibility and Migration Fallback

Legacy CMF rigging and creative subsystem references become contracts, fixtures, and eval targets. Flat images are not accepted as rigs unless converted into a valid manifest and preview-tested.

Fallback behavior:

- Missing rig layers returns `RIG_LAYER_MANIFEST_REQUIRED`.
- Failed preview returns `RIG_PREVIEW_FAILED`.
- Missing creative item source returns `CREATIVE_ITEM_SOURCE_REQUIRED`.
- Cross-brand selection returns `BRAND_SCOPE_VIOLATION`.
- Missing evaluation state returns `CREATIVE_ITEM_EVALUATION_REQUIRED`.

## 8. CBAR Constraint Pass

| CBAR Part | Resolution |
|---|---|
| Primitive Tension | Visual speed wants flat generated assets; deterministic animation requires rigged, tested, versioned components. |
| UX / Ops Failure Scenario | A paper-cut avatar looks fine as a still image but fails mouth or pivot animation during render. |
| Resolution Demand | Rig and creative library validation take precedence. Assets cannot enter Brand Context without layer, anchor, preview, source, hash, and eval proof. |
| Downstream Proof | Tests must block flat rigs, failed previews, missing version hashes, cross-brand creative items, and platform profiles missing negative-space/aspect rules. |

## 9. Tasks

- Define rig and creative library contracts.
- Add persistence for rig manifests and creative library items.
- Implement preview validation.
- Implement creative item approval state machine.
- Add brand-scope selection guard.
- Add platform profile inheritance hooks.
- Add tests for rig/anchor/profile validation.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Rig manifest includes layers, pivots, mouth shapes, eye/brow variants, gestures, body layers, and preview tests. | Avatar pack is stored as one flat PNG. |
| AC2 | Failed mouth, pivot, layer, or gesture preview can be repaired or rejected before lock. | Rig with failed mouth preview is approved. |
| AC3 | Props, anchors, motion recipes, and SFX store source, version hash, constraints, and eval state. | Anchor has no cultural context or risk score. |
| AC4 | Platform profile drives caption, negative-space, aspect, and publishing requirements. | Render contract ignores platform negative space. |
| AC5 | Cross-brand creative item selection is blocked. | Brand A selects Brand B's anchor. |

## 11. Dependencies

Internal:

- TS-CMF-018 Brand Genesis session
- TS-CMF-019 Acting library
- TS-CMF-014 Registry/eval targets
- TS-CMF-016 Greenfield gates

External:

- Pydantic v2
- Object storage
- Renderer preview tooling
- Evaluation service

## 12. Testing Strategy

Unit tests:

- Rig manifest required fields.
- Preview test failures.
- Anchor scoring schema.
- Platform profile constraints.

Integration tests:

- Generate rig manifest and run previews.
- Reject failed preview.
- Approve creative library item.
- Configure platform profile.
- Block cross-brand selection.

Safety tests:

- Flat avatar cannot lock.
- Missing version hash blocks approval.
- Renderer preview cannot define brand truth.

## 13. Observability, Recovery, and Rollback

- Logs include `rig_manifest_id`, `creative_item_id`, `brand_id`, `version_hash`, preview status, and blocker code.
- Metrics track preview failures, repairs, approved items, rejected items, and cross-brand blocks.
- Recovery reruns preview tests from stored artifacts.
- Rollback forks a new rig/library version; it never mutates locked items.

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
| Files Read Receipt | Complete |
| Requirement Trace | FR-CMF-04.03, FR-CMF-04.04, FR-CMF-04.05 |
| Pipeline Trace | Complete |
| Legacy Inventory Referenced | Yes - Brand Genesis V3 and CMF creative subsystem doctrine as source |
| CBAR Check | Complete |
| Python/DSPy/Pi Alignment | Python contracts with renderer previews as downstream consumers |
| TypeScript Boundary | Renderer/UI consumes generated contracts only |
| Legacy Runtime Coupling | Forbidden |
| Verdict | Accepted for implementation |

