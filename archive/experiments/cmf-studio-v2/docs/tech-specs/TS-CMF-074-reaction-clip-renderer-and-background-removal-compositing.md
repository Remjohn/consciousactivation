---
tech_spec_id: "TS-CMF-074"
title: "Reaction Clip Renderer and Background Removal Compositing"
story_id: "8.9"
story_title: "Reaction Clip Renderer and Background Removal Compositing"
epic_id: 8
epic_title: "Governed Rendering and Provider Operations"
status: "ready-for-development"
created_at: "2026-06-23"
source_story: "conversation-approved major update after TS-CMF-073"
fr_ids:
  - "FR-CMF-08.02"
  - "FR-CMF-08.03"
  - "FR-CMF-08.05"
pipeline_stage: "12"
entry_object: "Approved CompositionTemplateJson and RenderContract"
exit_object: "ReactionClipRenderOutput and RenderReceipt"
validation_contract: "background removal, upper-body subject compositing, beat sync, renderer output validation"
required_receipt: "ReactionClipRenderReceipt"
runtime_target: "Python orchestration / Remotion / Motion Canvas / background-removal worker / object storage"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-074: Reaction Clip Renderer and Background Removal Compositing

**Status:** Ready for Development  
**Implementation Boundary:** Build deterministic renderer support for reaction clips using approved composition JSON, upper-body interviewer/guest layers, background removal, beat-synced UI mechanics, captions, audio, and output receipts.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/tech-specs/TS-CMF-043-deterministic-remotion-and-motion-canvas-rendering.md` | Deterministic renderer boundary. |
| `docs/tech-specs/TS-CMF-047-audio-caption-timeline-and-mix-assembly.md` | Audio, caption, and timeline assembly dependencies. |
| `docs/tech-specs/TS-CMF-073-canonical-composition-json-registry-and-preview-approval.md` | Approved composition JSON source. |
| `CCP_Creative_Pipeline_Architecture_V2.md` | Renderer, layer, and composition doctrine. |
| `CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Python/DSPy/Pi orchestration boundary. |

## 2. Overview

The reaction clip renderer turns approved composition JSON into actual short-form video outputs. It must automate visual editing and video editing, not merely export static mockups. The renderer uses deterministic UI mechanics in the upper zone and composited upper-body interviewer/guest footage in the lower zone.

The lower zone assumes background-removed subject layers. The default mode is duo interaction; guest-only mode is allowed when the source moment is a strong solo reaction or the interviewer should be absent.

## 3. Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-08.02 | Deterministic renderers consume approved composition and brand layers. | Remotion/Motion Canvas props derive from approved JSON. |
| FR-CMF-08.03 | Provider adapters and jobs preserve receipts and artifacts. | Background-removal worker and render jobs emit receipts. |
| FR-CMF-08.05 | ComfyUI/GPU worker supports generated visual assets when required. | Scene backgrounds and graphic inserts can route to worker assets. |

## 4. Implementation Plan

1. Add `ReactionClipRendererProps`, `SubjectCutoutLayer`, `BackgroundRemovalJob`, `BeatSyncTimeline`, and `ReactionClipRenderReceipt`.
2. Implement background-removal worker adapter boundary for interviewer and guest footage.
3. Generate deterministic renderer props from approved `CompositionTemplateJson`.
4. Implement Remotion/Motion Canvas components for the seven reaction template codes.
5. Validate safe areas, captions, upper-body crop, audio sync, scene background, and render duration.
6. Store preview/final outputs with input hashes, output hash, renderer version, and receipt.

## 5. Primary Contracts

```python
class SubjectCutoutLayer(BaseModel):
    subject_role: Literal["interviewer", "guest"]
    source_video_ref: str
    cutout_video_ref: str | None
    crop_policy: Literal["upper_body", "head_and_shoulders"]
    background_removed: bool
    quality_score: float


class ReactionClipRendererProps(BaseModel):
    composition_template_id: UUID
    render_contract_id: UUID
    template_code: ReactionEditingTemplateCode
    beat_sync_timeline_id: UUID
    subject_layers: list[SubjectCutoutLayer]
    reaction_ui_state_track: list[dict[str, Any]]
    caption_track_id: UUID | None
    audio_mix_manifest_id: UUID | None
    props_hash: str
```

## 6. Rendering Rules

| Area | Rule |
|---|---|
| Upper zone | Deterministic reaction UI synchronized to question, answer, lock/reveal, and verdict beats. |
| Lower zone | Upper-body interviewer and guest cutouts composited into scene background. |
| Guest-only variant | Allowed only with explicit mode and rationale in composition JSON. |
| Captions | Must not collide with UI mechanic or subject faces. |
| Background removal | Output must pass edge quality and subject continuity threshold before final render. |
| Audio | Interviewer question and guest reaction must align with visual state changes. |

## 7. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CreateBackgroundRemovalJobCommand`, `BuildReactionClipRendererPropsCommand`, `ValidateReactionClipRenderInputsCommand`, `StartReactionClipRenderCommand`, `RecordReactionClipRenderOutputCommand` |
| Events | `BackgroundRemovalJobCreated`, `SubjectCutoutReady`, `ReactionClipRendererPropsBuilt`, `ReactionClipRenderStarted`, `ReactionClipRenderOutputRecorded` |
| Workflow | Stage 12 deterministic reaction render |
| Receipt | `ReactionClipRenderReceipt` |

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Human reaction vs graphic mechanic | Lower human scene remains visible and beat synced. | Render receipt stores subject layers and beat timeline. |
| Automated editing vs quality | Background removal and safe-area validators block bad renders. | Receipt stores quality scores and blockers. |
| Template speed vs reproducibility | Renderer props are generated from approved JSON. | Props hash links to composition hash. |

## 9. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Renderer props derive from approved composition JSON. | Renderer consumes hand-authored local props. |
| AC2 | Background removal jobs create subject cutout layers with quality scores. | Lower scene uses raw rectangular video. |
| AC3 | UI state changes align with transcript/audio beats. | Tier item drops before the guest answers. |
| AC4 | Captions and UI do not cover faces or essential mechanic text. | Caption blocks guest face or selected option. |
| AC5 | Render receipt stores inputs, hashes, quality, output URIs, and retry state. | Video file exists with no reproducibility envelope. |

## 10. Testing Strategy

- Unit tests for renderer props, subject layer, and beat timeline schemas.
- Background-removal adapter tests with fixture outputs and failure scores.
- Renderer validation tests for crop, safe area, caption collision, and duration.
- Golden-frame smoke tests for each template code.
- Workflow tests from approved composition JSON to `ReactionClipRenderReceipt`.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 11. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-074 |
| Requirement Trace | FR-CMF-08.02, FR-CMF-08.03, FR-CMF-08.05 |
| Pipeline Trace | Stage 12, approved composition JSON to rendered reaction clip |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No raw rectangular interview video, no hand-authored renderer truth, no final output without receipt |
