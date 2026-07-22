---
story_id: "7.7"
story_title: "Reaction Editing Template Routing"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-23"
fr_ids:
  - "FR-CMF-06.05"
  - "FR-CMF-06.06"
  - "FR-CMF-07.02"
  - "FR-CMF-08.02"
pipeline_stage: "8/9"
entry_object: "accepted asset route receipt"
exit_object: "`ReactionTemplateRouteReceipt`, `SceneSpec` template lineage"
validation_contract: "reaction template compatibility, live slot fit, source support, primitive obligations"
required_receipt: "ReactionTemplateRouteReceipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 7.7: Reaction Editing Template Routing

**Epic:** 7 - Complete Editing Sessions and Reproducible Scenes  
**Status:** Ready for Tech Spec  
**Source:** PRD-CMF-06.09A and PRD-CMF-07.02 update

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-06.05, FR-CMF-06.06, FR-CMF-07.02, FR-CMF-08.02 |
| Canonical Pipeline Stage | 8/9 |
| Entry Object | accepted asset route receipt |
| Exit Object | `ReactionTemplateRouteReceipt`, `SceneSpec` template lineage |
| Validation Contract | reaction template compatibility, live slot fit, source support, primitive obligations |
| Required Receipt | ReactionTemplateRouteReceipt |
| Source PRD | `docs/prd/modules/PRD_CMF_06_Interview_Expression_Routing.md`, `docs/prd/modules/PRD_CMF_07_Editing_Composition_Rendering.md` |
| Source Legacy Inventory | `apps/react-debate`, `apps/react-tierlist`, `apps/react-ranking-quiz`, `apps/react-blind-rank`, `apps/react-elimination`, `apps/react-authority-quiz`, `apps/react-mirror-quiz` |

## Story Definition

As a Production Steward, I want approved Expression Moments to route into governed reaction editing templates, so that live filmed guest material can become Goal-style ranking clips, tier lists, debates, quizzes, polls, and other animated reaction formats without losing source truth or scene reproducibility.

## Acceptance Criteria

- Given an accepted AssetRouteReceipt exists, when a reaction editing template is selected, then the system writes a `ReactionTemplateRouteReceipt` with template code, content format code, source evidence, live slot requirements, motion grammar, and SceneSpec requirement patch.
- Given a template is requested, when its content format is incompatible, then routing is blocked before SceneSpec compilation.
- Given an Interview Asset Contract targets a reaction template before filming, when the Conscious Interview Brief is compiled, then the question must specify the live answer slots required by that template.
- Given a Complete Editing Session compiles a SceneSpec from a reaction template route, when render props are produced, then `reaction_template_route_id` and `reaction_template_code` are preserved.
- Given a render is requested for a reaction template, when live slot mapping or source support is missing, then approval/rendering is blocked.

## Technical Notes

Implement `ReactionEditingTemplate`, `LiveClipSlotSpec`, `TemplateMotionGrammar`, `ReactionTemplateRoute`, and `ReactionTemplateRouteReceipt`. Seed canonical templates for `VRS-SPLIT`, `TRK-TIER`, `RNK-BLIND`, `RNK-PROPOSAL`, `ELM-BRACKET`, `MIR-QUIZ`, and `AUTH-LADDER`. The renderer contract should route these to Remotion/Motion Canvas templates, not to generic prompt-only video generation.

## Legacy and Primitive Mapping

Legacy Conscious Reactions mechanics become production editing grammars. Active families: FBK, TRG, STR, VSG, PSY.

## Prerequisites

Stories 6.5, 6.6, 7.1, 7.2, and 8.2.
