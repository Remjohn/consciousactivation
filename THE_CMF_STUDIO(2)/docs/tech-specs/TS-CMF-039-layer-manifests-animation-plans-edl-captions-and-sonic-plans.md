---
tech_spec_id: "TS-CMF-039"
title: "Layer Manifests, Animation Plans, EDL, Captions, and Sonic Plans"
story_id: "7.4"
story_title: "Layer Manifests, Animation Plans, EDL, Captions, and Sonic Plans"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-7-4-layer-manifests-animation-plans-edl-captions-and-sonic-plans.md"
fr_ids:
  - "FR-CMF-07.05"
  - "FR-CMF-07.06"
pipeline_stage: "12"
entry_object: "approved SceneSpec"
exit_object: "layer, animation, timeline, caption, sonic manifests"
validation_contract: "brand layer and timing validation"
required_receipt: "assembly-plan receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / SQLAlchemy v2 / Remotion / Motion Canvas / audio services"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-039: Layer Manifests, Animation Plans, EDL, Captions, and Sonic Plans

**Status:** Ready for Development  
**Story:** `7.4 - Layer Manifests, Animation Plans, EDL, Captions, and Sonic Plans`  
**Implementation Boundary:** Layer manifests, animation plans, edit decision lists, timeline manifests, caption manifests, sonic plans, brand-layer validation, timing validation, and assembly-plan receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-7-4-layer-manifests-animation-plans-edl-captions-and-sonic-plans.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-07.05 and FR-CMF-07.06 authority. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | LayerManifest, AnimationPlan, deterministic render branches, and receipt doctrine. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Render reproducibility and CMF manifest lineage. |
| `docs/architecture.md` | Stage 12 rendering/assembly objects and asset roll rule. |
| `docs/cmf-studio-pipeline-map.md` | Rendering sub-workflow. |
| `docs/migration/legacy-inventory.md` | Legacy audio engine, caption engine, timeline generator, rig manifests, and SFL failure corpus. |

## 2. Overview

Implement deterministic assembly planning after SceneSpec approval. The system must produce and evaluate `LayerManifest`, `AnimationPlan`, EDL, `TimelineManifest`, `CaptionManifest`, and `AudioMixManifest` before renderer/provider execution. Brand layers, acting references, rig layers, props, micro-semiotic anchors, motion recipes, SFX, captions, and negative-space constraints must come from the locked Brand Context Version or approved source/provider outputs.

No final artifact can be treated as reproducible without these manifests and hashes.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-07.05 | Select approved acting references, identity assets, props, anchors, motion recipes, SFX assets, caption rules, and visual negative-space constraints from locked brand context. | Brand layer validation, manifest source refs, and locked-context guards. |
| FR-CMF-07.06 | Create/evaluate Layer Manifests, Animation Plans, Renderer Routes, EDLs, timeline manifests, caption manifests, sonic plans, and Render Outputs. | Assembly-plan contracts, validation, receipt, and renderer handoff. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 12 - Rendering and assembly |
| Entry Object | approved SceneSpec |
| Exit Object | layer, animation, timeline, caption, sonic manifests |
| Validation Contract | brand layer and timing validation |
| Required Receipt | assembly-plan receipt |

### Legacy Intelligence Mapping

- Legacy audio engine, caption engine, and timeline generator inform migrated Python services and golden fixtures.
- Rig manifests and Brand Genesis libraries define approved layers and motion affordances.
- SFL failure corpus informs audio/caption continuity tests.

## 4. Implementation Plan

1. Add contracts for `LayerManifest`, `LayerEntry`, `AnimationPlan`, `EditDecisionList`, `TimelineManifest`, `CaptionManifest`, `AudioMixManifest`, and `AssemblyPlanReceipt`.
2. Implement assembly planner that reads SceneSpec, RenderContract, Brand Context Version, CompositionJob/plate when present, and asset selections.
3. Validate all brand layers and rig layers against locked context.
4. Validate caption timing, source timing, audio component classification, and negative-space constraints.
5. Emit manifest hashes into provider/render receipts.
6. Block rendering when assembly plan is missing or invalid.

## 5. Primary Output Schema

```python
from pydantic import BaseModel, Field


class LayerEntry(BaseModel):
    layer_id: str
    semantic_type: str
    file_uri: str
    asset_hash: str
    z_index: int
    bbox: tuple[int, int, int, int]
    anchor_point: tuple[float, float]
    motion_affordances: list[str] = []
    brand_context_asset_id: str | None = None


class LayerManifest(BaseModel):
    layer_manifest_id: str
    scene_spec_id: str
    canvas_width: int
    canvas_height: int
    aspect_ratio: str
    layers: list[LayerEntry] = Field(min_length=1)
    manifest_hash: str


class AnimationPlan(BaseModel):
    animation_plan_id: str
    layer_manifest_id: str
    fps: int
    duration_frames: int
    motion_style: str
    layer_animations: list[dict]
    plan_hash: str


class AudioMixManifest(BaseModel):
    audio_mix_manifest_id: str
    source_voice_refs: list[str]
    interviewer_voice_refs: list[str] = []
    repaired_source_refs: list[str] = []
    synthetic_bridge_refs: list[str] = []
    sfx_refs: list[str] = []
    music_refs: list[str] = []
    mix_hash: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CompileLayerManifestCommand`, `CompileAnimationPlanCommand`, `CompileEditDecisionListCommand`, `CompileCaptionManifestCommand`, `CompileAudioMixManifestCommand`, `ValidateAssemblyPlanCommand`, `BlockRenderWithoutAssemblyPlanCommand` |
| Events | `LayerManifestCompiled`, `AnimationPlanCompiled`, `EditDecisionListCompiled`, `CaptionManifestCompiled`, `AudioMixManifestCompiled`, `AssemblyPlanValidated`, `RenderBlockedMissingAssemblyPlan` |
| Workflow | `RenderWorkflow.stage12_compile_assembly_plan` |
| Receipt | `AssemblyPlanReceipt` with manifest IDs, hashes, brand context refs, timing validation, caption validation, sonic validation, and renderer route |

## 7. Backward Compatibility and Migration Fallback

Legacy engines are reference implementations and fixtures. The new Python services own contracts and persistence. If a legacy behavior cannot be expressed as a manifest, it cannot be used in production render.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Visual richness vs. reproducibility | Every layer has URI/hash/z-order/bbox/affordance. | Render receipt includes manifest hashes. |
| Sonic repair vs. source truth | Audio components are classified by role and source. | AudioMixManifest distinguishes source, repaired, synthetic, SFX, music. |
| Caption polish vs. timing truth | Caption timing validates against source/timeline. | Timing conflict blocks render. |

## 9. Tasks

- Add manifest contracts and tables.
- Implement assembly planner.
- Add brand layer and timing validators.
- Add audio/caption continuity checks.
- Add renderer handoff fields.
- Add golden fixture tests from legacy audio/caption/timeline behavior.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Assembly emits layer, animation, EDL, timeline, caption, sonic manifests. | Renderer starts with only a flattened image. |
| AC2 | Audio components are classified and traceable. | Synthetic bridge is mixed as source voice. |
| AC3 | Caption/source timing conflict fails. | Caption appears before source phrase. |
| AC4 | Rig layers belong to locked Brand Context. | Draft rig layer enters animation plan. |
| AC5 | Render receipts include manifest hashes and assets. | Final render has no manifest hash. |

## 11. Dependencies

- TS-CMF-020 paper-cut rig and creative libraries.
- TS-CMF-021 locked Brand Context.
- TS-CMF-037 SceneSpec/RenderContract.
- TS-CMF-038 CompositionJob when used.
- TS-CMF-011 audio classification and Voice-DNA Boost eligibility when applicable.

## 12. Testing Strategy


Unit tests:

- Unit tests for manifest schemas and hashes.
- Brand layer validation tests.
- Caption timing conflict tests.
- Audio component classification tests.
- Renderer handoff tests for Remotion and Motion Canvas props.
- Golden tests from legacy audio/caption/timeline fixtures.

Integration tests:

- Workflow test from `approved SceneSpec` to `layer, animation, timeline, caption, sonic manifests` through pipeline stage `12`.
- Command Bus test proving `assembly-plan receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for manifest compile failures, brand layer rejects, caption conflicts, audio role conflicts, and render blocks.
- Logs include SceneSpec ID, render contract ID, manifest hashes, and brand context hash.
- Recovery: rebuild assembly plan with corrected assets/timing.
- Rollback: supersede invalid manifests and block dependent render outputs.

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
| Tech Spec ID | TS-CMF-039 |
| Story | 7.4 |
| Requirement Trace | FR-CMF-07.05, FR-CMF-07.06 |
| Pipeline Trace | Stage 12, approved SceneSpec to layer/animation/timeline/caption/sonic manifests |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No opaque final artifact, no unapproved brand layer, no synthetic/source audio confusion |

