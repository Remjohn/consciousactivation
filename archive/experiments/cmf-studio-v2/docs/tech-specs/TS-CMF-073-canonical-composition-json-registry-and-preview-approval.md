---
tech_spec_id: "TS-CMF-073"
title: "Canonical Composition JSON Registry and Preview Approval"
story_id: "7.9"
story_title: "Canonical Composition JSON Registry and Preview Approval"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-23"
source_story: "conversation-approved major update after TS-CMF-072"
fr_ids:
  - "FR-CMF-07.02"
  - "FR-CMF-07.09"
  - "FR-CMF-08.02"
  - "FR-CMF-09.01"
pipeline_stage: "10 / 11"
entry_object: "SceneTemplateBindingReceipt"
exit_object: "CompositionTemplateApprovalReceipt"
validation_contract: "canonical composition JSON schema, preview render, approval blocker"
required_receipt: "CompositionTemplateApprovalReceipt"
runtime_target: "Python / Pydantic v2 / JSON Schema / Preview Renderer / Command Bus"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-073: Canonical Composition JSON Registry and Preview Approval

**Status:** Ready for Development  
**Implementation Boundary:** Composition JSON as the canonical source of truth for all reaction clip layouts, visual previews, approval gates, and renderer props.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/tech-specs/TS-CMF-038-ideogram-4-compositionjob-lineage.md` | Existing CompositionJob lineage requirements. |
| `docs/tech-specs/TS-CMF-071-reaction-editing-template-routing.md` | Reaction template route source. |
| `docs/tech-specs/TS-CMF-072-scene-template-runtime-binding-for-reaction-clips.md` | Required upstream scene-template binding. |
| `docs/ux/mockups/reaction-clip-templates/_reaction-clip-compositions.draft.json` | Draft preview source generated during visual exploration. |
| `CCP_Creative_Pipeline_Architecture_V2.md` | SceneSpec and composition source-of-truth doctrine. |

## 2. Overview

All production compositions must be JSON-first. PNG previews, Remotion props, Motion Canvas props, and operator thumbnails are derived artifacts. They cannot become the source of truth.

For reaction clips, the canonical composition JSON must preserve the stacked interview-first layout:

```text
upper zone: reaction mechanic UI
lower zone: upper-body interviewer/guest interaction scene
variant: guest-only reaction scene when interaction is unnecessary
```

This spec creates a registry and approval workflow for composition JSON before building final renderer templates.

## 3. Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-07.02 | SceneSpec must compile composition and render state from route lineage. | Composition JSON references SceneSpec, reaction route, and scene-template binding. |
| FR-CMF-07.09 | Scene container/component decisions must remain visible. | Composition JSON stores binding refs and zone rationale. |
| FR-CMF-08.02 | Renderer consumes approved brand layers and typed render inputs. | Renderer props derive from approved composition JSON. |
| FR-CMF-09.01 | Review must have evidence and approval blockers. | Preview approval receipt blocks unapproved JSON. |

## 4. Implementation Plan

1. Add `CompositionTemplateJson`, `CompositionZone`, `HumanSceneLayer`, `ReactionUiLayer`, `BeatSyncRule`, and `CompositionTemplateApprovalReceipt`.
2. Add JSON Schema generation and validation for composition templates.
3. Add draft, previewed, approved, rejected, superseded lifecycle states.
4. Add preview renderer contract that produces PNG/contact-sheet previews from JSON.
5. Add approval blocker: no production renderer template without approved composition JSON.
6. Add registry entries for each reaction template code and scene-template binding.

## 5. Primary Contracts

```python
class CompositionZone(BaseModel):
    zone_key: Literal["reaction_ui_zone", "human_scene_zone"]
    position: Literal["upper", "lower"]
    height_ratio: float
    safe_area: dict[str, int]
    layer_refs: list[str]
    rationale: str


class CompositionTemplateJson(BaseModel):
    schema_version: Literal["cmf.composition_template.v1"]
    composition_template_id: UUID
    template_code: ReactionEditingTemplateCode
    scene_template_binding_id: UUID
    canvas: dict[str, Any]
    zones: list[CompositionZone]
    beat_sync_rules: list[BeatSyncRule]
    required_asset_roles: list[str]
    renderer_targets: list[str]
    eval_obligations: list[str]
    state: Literal["draft", "previewed", "approved", "rejected", "superseded"]
    json_hash: str
```

## 6. Required JSON Fields

| Field | Requirement |
|---|---|
| `canvas` | Width, height, aspect ratio, FPS, platform variants. |
| `zones` | Reaction UI zone and human scene zone with safe areas. |
| `human_scene` | `duo_interaction` default, `guest_only_reaction` supported. |
| `subjects` | Interviewer and guest upper-body layers with background removed. |
| `beat_sync_rules` | Interviewer question, guest answer, mechanic state, reveal/lock. |
| `scene_template_binding_id` | Required upstream binding from TS-CMF-072. |
| `renderer_targets` | Remotion, Motion Canvas, or approved deterministic route. |
| `eval_obligations` | Primitive, scene, composition, text, and source-lineage gates. |

## 7. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `CreateCompositionTemplateDraftCommand`, `RenderCompositionPreviewCommand`, `ApproveCompositionTemplateCommand`, `RejectCompositionTemplateCommand`, `SupersedeCompositionTemplateCommand` |
| Events | `CompositionTemplateDraftCreated`, `CompositionPreviewRendered`, `CompositionTemplateApproved`, `CompositionTemplateRejected`, `CompositionTemplateSuperseded` |
| Workflow | Stage 10 composition approval after scene-template binding and before renderer template build |
| Receipt | `CompositionTemplateApprovalReceipt` |

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Visual approval vs canonical truth | Preview is rendered from JSON and never edited as source. | Approval receipt stores JSON hash and preview hash. |
| Flexible layouts vs interview-first doctrine | Reaction UI above, human interaction below is the default layout contract. | JSON stores zones and mode. |
| Template reuse vs guest confusion | Composition references brand/guest scope and content asset code. | UI and receipts show scoped object header. |

## 9. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Every preview image has a source composition JSON hash. | PNG exists without JSON source. |
| AC2 | Composition JSON requires scene-template binding. | Template JSON bypasses old scene builder. |
| AC3 | Production templates cannot be built from rejected/unpreviewed JSON. | Renderer consumes draft JSON directly. |
| AC4 | Human scene supports duo and guest-only modes. | Layout assumes only abstract graphics. |
| AC5 | Approval receipt stores reviewer, hashes, blocker state, and lineage. | Approval is a filename note. |

## 10. Testing Strategy

- Schema validation tests for required zones and subject layers.
- Hash stability tests for JSON and preview artifact.
- Approval blocker tests for missing preview, missing binding, missing beat sync, or rejected state.
- Renderer props generation tests proving approved JSON becomes deterministic renderer input.
- UI read-model tests proving operator can inspect JSON, preview, lineage, and blockers.

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
| Tech Spec ID | TS-CMF-073 |
| Requirement Trace | FR-CMF-07.02, FR-CMF-07.09, FR-CMF-08.02, FR-CMF-09.01 |
| Pipeline Trace | Stage 10/11, scene-template binding to approved composition JSON |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No image-only templates, no unapproved JSON, no composition outside lineage |
