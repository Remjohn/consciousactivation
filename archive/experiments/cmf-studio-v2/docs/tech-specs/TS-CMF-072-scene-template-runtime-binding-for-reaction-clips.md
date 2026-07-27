---
tech_spec_id: "TS-CMF-072"
title: "Scene Template Runtime Binding for Reaction Clips"
story_id: "7.8"
story_title: "Scene Template Runtime Binding for Reaction Clips"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-23"
source_story: "conversation-approved major update after TS-CMF-071"
fr_ids:
  - "FR-CMF-07.02"
  - "FR-CMF-07.09"
  - "FR-CMF-08.02"
pipeline_stage: "9 / 10"
entry_object: "ReactionTemplateRouteReceipt and SceneSpec"
exit_object: "SceneTemplateBindingReceipt"
validation_contract: "legacy scene-template compatibility, container/component/effect fit, reaction clip layout fit"
required_receipt: "SceneTemplateBindingReceipt"
runtime_target: "Python / Pydantic v2 / Registry Service / SceneSpec Compiler / Command Bus"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-072: Scene Template Runtime Binding for Reaction Clips

**Status:** Ready for Development  
**Implementation Boundary:** Binding reaction editing template routes to the migrated CMF scene-builder runtime asset before production composition JSON or renderer templates are created.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/tech-specs/TS-CMF-041-scene-containers-creative-subsystems-and-asset-roll-orchestration.md` | Existing scene intelligence contracts. |
| `docs/tech-specs/TS-CMF-071-reaction-editing-template-routing.md` | Reaction template route and live slot contracts. |
| `registries/cmf-assembler-schemas/dep_vid_035_scene_intelligence_runtime.schema.json` | Schema for compiled scene-builder/editor-regeneration runtime assets. |
| `reference/conscious-rivers/src/ccp/harness/intelligence/scene_intelligence/runtime/scene_builder.runtime.json` | Legacy runtime source with 6 containers, 19 components, 25 scene templates, and 100 effects. |
| `reference/conscious-rivers/src/ccp/harness/intelligence/CMF_Master_Scene_Intelligence.md` | Scene intelligence doctrine and orchestration source. |
| `reference/conscious-rivers/src/ccp/harness/intelligence/CMF_Scene_Containers_Definitions.md` | Container definitions. |
| `reference/conscious-rivers/src/ccp/harness/intelligence/CMF_Scene_Components_Definitions.md` | Component definitions. |

## 2. Overview

Reaction editing templates must not become a parallel template system. Every reaction clip must bind to the existing CMF scene intelligence model: container, component, scene template, effect stack, text policy, cognitive load, attention mode, continuity requirement, and asset-roll role.

This spec repairs the gap between `ReactionTemplateRoute` and the old scene-builder runtime. The output is a binding receipt that proves why a reaction template such as `VRS-SPLIT`, `TRK-TIER`, or `MIR-QUIZ` is compatible with a specific legacy or migrated scene template.

## 3. Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-07.02 | SceneSpec compilation must preserve template lineage. | SceneSpec stores reaction route plus scene-template binding. |
| FR-CMF-07.09 | Scene containers/components/subsystems and asset-roll decisions must be preserved. | Binding references container, component, template, effect stack, and asset-roll role. |
| FR-CMF-08.02 | Deterministic renderers must consume approved scene and template instructions. | Renderer receives binding ID, template ID, and effect constraints. |

## 4. Implementation Plan

1. Add `SceneTemplateRuntimeAsset` loader for migrated scene-builder runtime JSON.
2. Add `SceneTemplateBinding`, `SceneTemplateBindingCandidate`, and `SceneTemplateBindingReceipt`.
3. Add compatibility rules between `ReactionEditingTemplateCode` and runtime scene templates.
4. Require scene-template binding before final composition JSON can be approved.
5. Store binding fields in `SceneSpec`, `RenderContract`, and reconstruction audit view.
6. Add command bus support for `BindReactionRouteToSceneTemplateCommand`.

## 5. Primary Contracts

```python
class SceneTemplateBinding(BaseModel):
    schema_version: Literal["cmf.scene_template_binding.v1"]
    scene_template_binding_id: UUID
    scene_spec_id: UUID
    reaction_template_route_id: UUID
    reaction_template_code: ReactionEditingTemplateCode
    runtime_asset_id: str
    runtime_version: str
    scene_template_id: str
    container_id: str
    component_ids: list[str]
    effect_ids: list[str]
    target_attention_mode: str
    text_policy: str
    av_congruence_mode: str
    continuity_requirement: str
    base_cls: float
    recommended_duration_seconds: dict[str, float]
    binding_rationale: str
    rejected_candidate_ids: list[str] = []


class SceneTemplateBindingReceipt(BaseModel):
    scene_template_binding_receipt_id: UUID
    scene_template_binding_id: UUID | None
    decision_code: str
    validation_passed: bool
    evidence_refs: list[str]
    registry_versions: dict[str, str]
```

## 6. Compatibility Rules

| Reaction Template | Required Runtime Fit |
|---|---|
| `VRS-SPLIT` | Contrast, juxtaposition, or binary choice scene template with clear text policy and low-to-medium CLS. |
| `TRK-TIER` | Ranking/list scene template with high readability, ordered reveal, and repeatable item motion. |
| `RNK-BLIND` | Suspense/reveal template with lock/reveal state and retention loop. |
| `RNK-PROPOSAL` | Educational correction or proposal board template with principle distillation. |
| `ELM-BRACKET` | Elimination or decision-tree template with escalating stakes. |
| `MIR-QUIZ` | Identity mirror or audience self-diagnosis template with ethical framing. |
| `AUTH-LADDER` | Teaching sequence or authority progression template with compressed principle transfer. |

## 7. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `LoadSceneTemplateRuntimeAssetCommand`, `BindReactionRouteToSceneTemplateCommand`, `RejectSceneTemplateBindingCommand` |
| Events | `SceneTemplateRuntimeAssetLoaded`, `ReactionRouteSceneTemplateBound`, `SceneTemplateBindingRejected` |
| Workflow | Complete Editing Session stage 9/10 after reaction template routing and before composition JSON approval |
| Receipt | `SceneTemplateBindingReceipt` |

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| New reaction mechanics vs old CMF orchestration | Reaction templates bind to scene runtime templates before rendering. | Binding receipt stores runtime template and rationale. |
| Pretty layout vs cognitive rhythm | Binding preserves CLS, attention mode, continuity, and text policy. | Eval receipt can inspect these fields. |
| Fast approval vs reproducibility | No final composition JSON without binding. | Approval blocker checks binding receipt. |

## 9. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | `ReactionTemplateRouteReceipt` can produce a `SceneTemplateBindingReceipt`. | Reaction route proceeds directly to renderer. |
| AC2 | Binding stores runtime asset ID/version and scene template ID. | Only a visual mockup path is stored. |
| AC3 | Binding blocks incompatible scene template choices. | Blind rank uses static quote-card scene. |
| AC4 | SceneSpec reconstruction shows route, binding, component, effect, and asset-roll lineage. | Reviewer cannot know which old scene template was used. |
| AC5 | Final composition approval is blocked when binding is missing. | Operator approves JSON that bypasses scene intelligence. |

## 10. Testing Strategy

- Unit tests for runtime asset parsing and hash/version extraction.
- Compatibility tests for each reaction template code.
- Failure tests for missing runtime version, missing scene template ID, high text-policy conflict, and incompatible container.
- Workflow test proving binding occurs between reaction route and composition JSON.
- Reconstruction test proving binding appears in audit view and receipt lineage.

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
| Tech Spec ID | TS-CMF-072 |
| Requirement Trace | FR-CMF-07.02, FR-CMF-07.09, FR-CMF-08.02 |
| Pipeline Trace | Stage 9/10, reaction route to scene-template binding |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No parallel reaction template system, no final JSON without scene-template binding |
