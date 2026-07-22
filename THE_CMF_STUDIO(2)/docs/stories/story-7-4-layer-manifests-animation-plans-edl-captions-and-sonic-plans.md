---
story_id: "7.4"
story_title: "Layer Manifests, Animation Plans, EDL, Captions, and Sonic Plans"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-07.05"
  - "FR-CMF-07.06"
pipeline_stage: "12"
entry_object: "approved SceneSpec"
exit_object: "layer, animation, timeline, caption, sonic manifests"
validation_contract: "brand layer and timing validation"
required_receipt: "assembly-plan receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 7.4: Layer Manifests, Animation Plans, EDL, Captions, and Sonic Plans

**Epic:** 7 - Complete Editing Sessions and Reproducible Scenes
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-07.05, FR-CMF-07.06 |
| Canonical Pipeline Stage | 12 |
| Entry Object | approved SceneSpec |
| Exit Object | layer, animation, timeline, caption, sonic manifests |
| Validation Contract | brand layer and timing validation |
| Required Receipt | assembly-plan receipt |
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

As a Production Steward, I want approved brand layers, manifests, animation plans, EDLs, caption manifests, and sonic plans created and evaluated, so that deterministic rendering can assemble assets transparently.

**Acceptance Criteria:**

- Given a SceneSpec is approved for deterministic rendering, when assembly planning runs, then it produces layer manifest, animation plan, edit decision list, timeline manifest, caption manifest, and sonic plan.
- Given audio components include source, interviewer, repaired source, synthetic bridge, SFX, and music, when the sonic plan is built, then each component is classified and traceable.
- Given caption timing conflicts with source timing, when evaluation runs, then the plan fails for repair.
- Given an animation plan selects rig layers, when validated, then those layers must belong to the locked Brand Context Version.
- Given a plan passes, when provider/render jobs run, then receipts include manifest hashes and selected asset IDs.

**Technical Notes:** Implement `LayerManifest`, `AnimationPlan`, `TimelineManifest`, `CaptionManifest`, `AudioMixManifest`, and EDL contracts.

**Legacy and Primitive Mapping:** Legacy audio engine, caption engine, timeline generator, rig manifests. Active families: VSG, VOC, SAF.

**Prerequisites:** Stories 7.1 through 7.3.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
