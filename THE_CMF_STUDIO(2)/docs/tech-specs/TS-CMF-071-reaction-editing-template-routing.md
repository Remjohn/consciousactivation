---
tech_spec_id: "TS-CMF-071"
title: "Reaction Editing Template Routing"
story_id: "7.7"
story_title: "Reaction Editing Template Routing"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-development"
created_at: "2026-06-23"
source_story: "docs/stories/story-7-7-reaction-editing-template-routing.md"
fr_ids:
  - "FR-CMF-06.05"
  - "FR-CMF-06.06"
  - "FR-CMF-07.02"
  - "FR-CMF-08.02"
pipeline_stage: "8/9"
entry_object: "accepted asset route receipt"
exit_object: "ReactionTemplateRouteReceipt and SceneSpec template lineage"
validation_contract: "reaction template compatibility, live slot fit, source support, primitive obligations"
required_receipt: "ReactionTemplateRouteReceipt"
runtime_target: "Python / FastAPI / Pydantic v2 / Command Bus / Remotion or Motion Canvas"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-071: Reaction Editing Template Routing

**Status:** Ready for Development  
**Story:** `7.7 - Reaction Editing Template Routing`  
**Implementation Boundary:** Registry, route planner, live clip slot contract, motion grammar contract, receipt, SceneSpec lineage, and UI format compatibility.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-7-7-reaction-editing-template-routing.md` | Story source and acceptance criteria. |
| `docs/prd/modules/PRD_CMF_06_Interview_Expression_Routing.md` | Interview route and reaction template product requirements. |
| `docs/prd/modules/PRD_CMF_07_Editing_Composition_Rendering.md` | SceneSpec and renderer lineage requirement. |
| `docs/content-asset-code-and-format-registry.md` | Content format and reaction template code registry. |
| `THE CMF STUDIO/CCP V9.1 — Expression Capture & Archetype Routing Update.md` | Reaction seeds and Conscious Reactions Editing source. |
| `THE CMF STUDIO/CCP Archetype System Migration Proposition.docx.md` | Solo reaction, debate, vote, jury, duel, validation, quiz/ranking references. |
| Legacy app refs | `apps/react-debate`, `apps/react-tierlist`, `apps/react-ranking-quiz`, `apps/react-blind-rank`, `apps/react-elimination`, `apps/react-authority-quiz`, `apps/react-mirror-quiz`. |

## 2. Overview

Reaction editing templates convert a source-backed live guest answer into an animated social-native video or visual composition. They are not standalone interactive toys. They are governed editing grammars used by CMF after route approval and before SceneSpec compilation.

The live-filmed interview changes the role of these templates: Interview Asset Contracts can now ask questions that intentionally produce the required edit slots. For example, a tier-list template needs rankable items and a top-tier rationale; a versus template needs two sides and a verdict; an authority ladder needs a diagnostic question and level explanation.

## 3. Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-06.05 | Route approved Expression Moments through valid registries. | Reaction template registry and route planner. |
| FR-CMF-06.06 | Generate package specs from source-supported routes. | Compatible format/template selection for Guest Asset Packs. |
| FR-CMF-07.02 | Compile SceneSpec and RenderContract from route state. | SceneSpec stores `reaction_template_route_id` and `reaction_template_code`. |
| FR-CMF-08.02 | Route deterministic assets through Remotion/Motion Canvas. | Motion grammar selects renderer route and composition ID. |

## 4. Implementation Plan

1. Add `ReactionEditingTemplate`, `LiveClipSlotSpec`, `TemplateMotionGrammar`, `ReactionTemplateRoute`, and `ReactionTemplateRouteReceipt`.
2. Seed canonical templates: `VRS-SPLIT`, `TRK-TIER`, `RNK-BLIND`, `RNK-PROPOSAL`, `ELM-BRACKET`, `MIR-QUIZ`, `AUTH-LADDER`.
3. Add `ReactionEditingTemplateService.plan_template_route`.
4. Require accepted AssetRouteReceipt and compatible content format.
5. Emit `ReactionTemplateRouteReceipt` with source evidence, live slot keys, motion grammar, primitive obligations, and SceneSpec patch.
6. Add optional SceneSpec and RenderContract fields for template route/code.
7. Expose template compatibility in `ContentAssetFormatRegistryState`.

## 5. Primary Contracts

```python
class ReactionEditingTemplate(BaseModel):
    template_code: ReactionEditingTemplateCode
    display_name: str
    family: ReactionEditingFamily
    valid_content_format_codes: list[str]
    source_app_refs: list[str]
    interview_question_instruction: str
    live_clip_slots: list[LiveClipSlotSpec]
    motion_grammar: TemplateMotionGrammar
    primitive_eval_obligations: list[str]


class ReactionTemplateRouteReceipt(BaseModel):
    expression_moment_id: UUID
    asset_route_receipt_id: UUID
    reaction_template_route_id: UUID | None
    template_code: ReactionEditingTemplateCode | None
    content_format_code: str | None
    source_support_evidence: list[str]
    live_clip_slot_keys: list[str]
    scene_spec_requirement_patch: dict[str, Any]
    decision_code: str
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `PlanReactionTemplateRouteCommand`, `ListReactionEditingTemplatesCommand` |
| Events | Command Bus success/failure events |
| Workflow | Route/package planning before `CompleteEditingSessionWorkflow.stage9_compile_scene_spec` |
| Receipt | `ReactionTemplateRouteReceipt` |

## 7. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Fast social format vs source truth | Only accepted AssetRouteReceipts can select templates. | Receipt stores expression moment and route receipt. |
| Template excitement vs interview-first doctrine | Interview questions must produce live slots for the selected grammar. | Interview Asset Contract cites template slot requirements. |
| Legacy app reuse vs runtime disorder | Legacy apps are references; templates become typed Pydantic contracts. | Registry stores source app refs and motion grammar. |
| Renderer convenience vs reproducibility | SceneSpec and RenderContract store template route/code. | Renderer props include template lineage. |

## 8. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Accepted route produces `REACTION_TEMPLATE_ROUTE_ACCEPTED`. | Template selected from a rejected route. |
| AC2 | Content format mismatch blocks route. | `MIR-QUIZ` renders as unrelated Super Visual. |
| AC3 | Live slot keys are present in receipt. | Tier list has no rank-item slot. |
| AC4 | SceneSpec and renderer props preserve template route/code. | Render sees only `short_video`. |
| AC5 | UI format registry shows compatible template codes. | Operator cannot tell which format becomes tier/ranking/debate. |

## 9. Testing Strategy

- Unit tests for default template registry and source app references.
- Service tests for accepted route to template receipt.
- Compatibility failure tests for content format mismatch.
- SceneSpec tests proving template route/code enter renderer props.
- Command Bus tests for `PlanReactionTemplateRouteCommand`.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 10. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-071 |
| Story | 7.7 |
| Requirement Trace | FR-CMF-06.05, FR-CMF-06.06, FR-CMF-07.02, FR-CMF-08.02 |
| Pipeline Trace | Stage 8/9, accepted route to template route receipt and SceneSpec lineage |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No generic prompt-only ranking videos, no unsupported newsletters, no template route without source support |
