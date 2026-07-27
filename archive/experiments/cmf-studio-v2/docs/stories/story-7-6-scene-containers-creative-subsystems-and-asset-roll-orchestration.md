---
story_id: "7.6"
story_title: "Scene Containers, Creative Subsystems, and Asset Roll Orchestration"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-07.09"
pipeline_stage: "9 / 10"
entry_object: "scene intent"
exit_object: "scene container/component/subsystem/asset-roll plan"
validation_contract: "CMF scene orchestration gate"
required_receipt: "scene intelligence receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 7.6: Scene Containers, Creative Subsystems, and Asset Roll Orchestration

**Epic:** 7 - Complete Editing Sessions and Reproducible Scenes
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-07.09 |
| Canonical Pipeline Stage | 9 / 10 |
| Entry Object | scene intent |
| Exit Object | scene container/component/subsystem/asset-roll plan |
| Validation Contract | CMF scene orchestration gate |
| Required Receipt | scene intelligence receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Ensure every production output is created inside a Complete Editing Session with source lineage, Brand Context Version, SceneSpec, composition state, provider jobs, render contracts, evaluation receipts, revisions, and approvals.

**Covers:** FR-CMF-07.01 through FR-CMF-07.09.

**User Value:** Production Stewards and Reviewers can reconstruct why a scene exists and why it looks the way it does.

**Technical Context:** `/api/v1/editing-sessions`, `/api/v1/scenes`, CompleteEditingSessionWorkflow, `complete_editing_sessions`, `creative_states`, `scene_specs`, `scene_container_plans`, `scene_component_selections`, `creative_subsystem_decisions`, `asset_roll_plans`, `composition_jobs`, `asset_selections`, `layer_manifests`, `animation_plans`, `render_contracts`, `render_outputs`.

**CBAR Failure Scenario:** If scene lineage collapses into a final media URL, CMF cannot reproduce, repair, audit, or defend the output. Composition and rendering metadata must be first-class.

## Story Definition

As a Production Steward, I want SceneSpecs to preserve CMF scene-container, scene-component, creative-subsystem, and asset-roll decisions, so that every scene can explain what perceptual and narrative job it is performing.

**Acceptance Criteria:**

- Given a SceneSpec is compiled, when scene orchestration runs, then it selects a biological arc container such as HOOK, SETUP, CHALLENGE, TURNING_POINT, RESOLUTION, or VISION before choosing a cinematic component.
- Given a container is selected, when a component fills it, then the system records why that component is valid for the container and which constraints it satisfies or violates.
- Given creative subsystem gates are relevant, when the SceneSpec is saved, then it records decisions from first-frame imprint, recognition window, gaze transfer, excitation transfer, arousal-pacing, temporal binding, element count, silence container, or other migrated subsystem gates as applicable.
- Given assets are selected, when the Asset Roll Plan is generated, then each A-Roll, B-Roll, C-Roll, D-Roll, or E-Roll item carries its narrative/emotional/explanatory/authentic/cultural function and source or licensing status.
- Given a scene is reviewed or revised, when the Reviewer asks why the scene looks and feels this way, then the system can reconstruct source expression, route, container, component, subsystem gates, asset roll choices, sonic plan, CompositionJob when used, render manifests, and approvals.

**Technical Notes:** Add `SceneContainerPlan`, `SceneComponentSelection`, `CreativeSubsystemDecision`, and `AssetRollPlan` contracts. SceneSpec compilation consumes migrated CMF Master Scene Intelligence, Creative Subsystems, Scene Containers, Scene Components, and Conscious Asset Strategy Guide registry entries.

**Legacy and Primitive Mapping:** CMF Master Scene Intelligence, CMF Creative Subsystems, Scene Containers, Scene Components, Conscious Asset Strategy Guide, PRD-03 CMF. Active families: VSG, STR, VOC, ACT, FBK, SAF.

**Prerequisites:** Stories 7.1 through 7.5 and Story 3.6.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
