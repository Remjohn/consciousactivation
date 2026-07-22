---
tech_spec_id: "TS-CMF-043"
title: "Deterministic Remotion and Motion Canvas Rendering"
story_id: "8.2"
story_title: "Deterministic Remotion and Motion Canvas Rendering"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-8-2-deterministic-remotion-and-motion-canvas-rendering.md"
fr_ids:
  - "FR-CMF-08.02"
pipeline_stage: "12"
entry_object: "RenderContract"
exit_object: "deterministic render output"
validation_contract: "renderer props and brand layer validation"
required_receipt: "render receipt"
runtime_target: "Python contracts / Remotion / Motion Canvas / generated TypeScript consumers"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-043: Deterministic Remotion and Motion Canvas Rendering

**Status:** Ready for Development  
**Story:** `8.2 - Deterministic Remotion and Motion Canvas Rendering`  
**Implementation Boundary:** Remotion/Motion Canvas renderer routing, generated renderer props, brand layer validation, final text rendering, captions/timing/motion/sonic inputs, deterministic render receipt, and output storage.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-8-2-deterministic-remotion-and-motion-canvas-rendering.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-08.02 authority and TypeScript leaf-runtime rule. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | Remotion/Motion Canvas deterministic route requirements. |
| `THE CMF STUDIO/CCP_Creative_Pipeline_Architecture_V2.md` | Deterministic branch, renderer routing, layer and animation contracts. |
| `docs/architecture.md` | Renderer props rule and TypeScript boundary. |
| `docs/cmf-studio-pipeline-map.md` | Rendering sub-workflow and final text outside Ideogram. |
| `docs/migration/legacy-inventory.md` | Caption engine, timeline generator, CMF engine references. |

## 2. Overview

Implement deterministic rendering through Remotion or Motion Canvas as downstream execution targets. They consume Python-issued `RenderContract`, `LayerManifest`, `AnimationPlan`, `TimelineManifest`, `CaptionManifest`, `AudioMixManifest`, final text plan, and platform variants. They do not decide brand truth, archetype routing, source state, approval, or publishing policy.

Final text is rendered by deterministic renderers from the approved text plan, not delegated to a flattened image provider output.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-08.02 | Route deterministic assets through Remotion or Motion Canvas using approved brand layers, manifests, final text rendering, captions, timing, motion recipes, and sonic plans. | Renderer route decision, generated props, brand-layer validation, final text rule, render receipt, and retry-safe output storage. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 12 - Rendering and assembly |
| Entry Object | RenderContract |
| Exit Object | deterministic render output |
| Validation Contract | renderer props and brand layer validation |
| Required Receipt | render receipt |

### Legacy Intelligence Mapping

- Legacy caption/timeline engine behavior informs fixtures and tests.
- Remotion/Motion Canvas are TypeScript leaf runtimes consuming generated contracts.
- Paper-cut rig and motion recipes come from locked Brand Context Version.

## 4. Implementation Plan

1. Add contracts for `RendererRouteDecision`, `RendererPropsBundle`, `DeterministicRenderJob`, `RenderOutput`, and `RenderReceipt`.
2. Generate TypeScript props from Pydantic schemas for Remotion/Motion Canvas consumers.
3. Validate brand layers, rig references, motion recipes, text plan, captions, timing, audio mix, and platform variants before render.
4. Store preview/final artifacts with hashes and renderer version.
5. Write render receipt linked to provider/job receipts and assembly manifests.
6. Preserve completed artifacts across retry.

## 5. Primary Output Schema

```python
from enum import Enum
from pydantic import BaseModel


class DeterministicRenderer(str, Enum):
    REMOTION = "remotion"
    MOTION_CANVAS = "motion_canvas"


class RendererPropsBundle(BaseModel):
    renderer_props_bundle_id: str
    render_contract_id: str
    renderer: DeterministicRenderer
    layer_manifest_id: str
    animation_plan_id: str
    timeline_manifest_id: str
    caption_manifest_id: str | None = None
    audio_mix_manifest_id: str | None = None
    final_text_plan_id: str
    brand_context_version_id: str
    props_hash: str


class RenderOutput(BaseModel):
    render_output_id: str
    render_contract_id: str
    renderer: DeterministicRenderer
    preview_uri: str | None = None
    final_uri: str
    output_hash: str
    renderer_version: str
    manifest_hashes: list[str]
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `SelectDeterministicRendererCommand`, `BuildRendererPropsBundleCommand`, `ValidateRendererInputsCommand`, `StartDeterministicRenderCommand`, `RecordDeterministicRenderOutputCommand`, `FailDeterministicRenderCommand` |
| Events | `DeterministicRendererSelected`, `RendererPropsBundleBuilt`, `RendererInputsValidated`, `DeterministicRenderStarted`, `DeterministicRenderOutputRecorded`, `DeterministicRenderFailed` |
| Workflow | `RenderWorkflow.stage12_deterministic_render` |
| Receipt | `RenderReceipt` with renderer, props hash, input manifest hashes, renderer version, output hashes, duration, cost, and retry count |

## 7. Backward Compatibility and Migration Fallback

Legacy renderer scripts can inform output fixtures and timeline/caption tests. Production renderer props must be generated from Pydantic contracts. Hand-authored TypeScript business logic is not the source of truth.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Renderer flexibility vs. domain authority | Renderer receives props only; Python owns domain state. | Render receipt links back to RenderContract and props hash. |
| Final text quality vs. provider convenience | Deterministic renderer renders final text. | Receipt stores final text plan ID. |
| Retry speed vs. artifact safety | Completed artifacts persist across retry. | Retry receipt references prior output state. |

## 9. Tasks

- Add deterministic renderer contracts.
- Generate TypeScript props from Pydantic models.
- Implement renderer route decision and input validators.
- Add Remotion/Motion Canvas worker invocation boundaries.
- Add render output storage and receipt writer.
- Add tests for final text, brand layers, captions, and retry behavior.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Renderer consumes brand layers, rig, text, captions, motion, timings, audio, variants. | Renderer receives a final flattened image only. |
| AC2 | Final text rendered by deterministic renderer. | Text is baked into provider image. |
| AC3 | Layer not in locked Brand Context fails. | Draft layer renders into final asset. |
| AC4 | Output stores URIs, hashes, renderer version, receipt. | Final URI saved without manifest hashes. |
| AC5 | Retry preserves completed artifacts. | Retry deletes completed preview/final output. |

## 11. Dependencies

- TS-CMF-037 RenderContract.
- TS-CMF-039 assembly manifests.
- TS-CMF-021 locked Brand Context.
- TS-CMF-042 provider capability/receipt.

## 12. Testing Strategy

Unit tests:

- Renderer prop schema validation.
- Brand layer validation.
- Final text plan validation.
- Render retry and idempotency key behavior.

Integration tests:

- Generated TypeScript contract compatibility with Python/Pydantic contracts.
- Remotion render path from RenderContract to output hash.
- Motion Canvas render path from RenderContract to output hash.

Eval and fixture tests:

- Golden render fixture tests for captions, timing, audio alignment, and deterministic frame output.

## 13. Observability, Recovery, and Rollback

- Metrics for renderer route, render duration, input validation failure, output size, and retry count.
- Logs include render contract ID, renderer props hash, output hash, and renderer version.
- Recovery: retry with same props bundle or corrected manifest version.
- Rollback: supersede render output and invalidate dependent evaluation receipts.

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
| Tech Spec ID | TS-CMF-043 |
| Story | 8.2 |
| Requirement Trace | FR-CMF-08.02 |
| Pipeline Trace | Stage 12, RenderContract to deterministic render output |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No TypeScript source-of-truth domain logic, no baked provider text, no unapproved brand layers |
