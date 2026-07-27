---
story_id: "7.3"
story_title: "Ideogram 4 CompositionJob Lineage"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-07.03"
  - "FR-CMF-07.04"
pipeline_stage: "10"
entry_object: "SceneSpec and Ideogram route"
exit_object: "`CompositionJob`, plate, analysis"
validation_contract: "text-space and identity boundary"
required_receipt: "composition receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 7.3: Ideogram 4 CompositionJob Lineage

**Epic:** 7 - Complete Editing Sessions and Reproducible Scenes
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-07.03, FR-CMF-07.04 |
| Canonical Pipeline Stage | 10 |
| Entry Object | SceneSpec and Ideogram route |
| Exit Object | `CompositionJob`, plate, analysis |
| Validation Contract | text-space and identity boundary |
| Required Receipt | composition receipt |
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

As a Production Steward, I want Ideogram 4 `CompositionJob` JSON preserved as first-class composition lineage, so that composition plates can guide scenes without becoming final identity or text authority.

**Acceptance Criteria:**

- Given an Ideogram route is selected, when composition is submitted, then the system stores `CompositionJob` JSON, prompt hash, constraints, provider metadata, and correlation ID.
- Given Ideogram returns a composition plate, when saved, then composition plate URI, output hash, composition analysis, and provider receipt are linked to the Complete Editing Session.
- Given the plate contains final-looking text or identity drift, when evaluation runs, then the plate is restricted to background/composition use, rejected, or repaired.
- Given downstream edits occur, when they are recorded, then they reference the originating `CompositionJob` and plate.
- Given a scene is audited, when composition lineage is opened, then the `CompositionJob`, prompt hash, plate URI, analysis, downstream edits, and final text plan are visible.

**Technical Notes:** Implement `CompositionJob`, `CompositionPlan`, provider adapter `providers/ideogram.py`, and composition lineage storage under `brands/{brand_id}/composition-plates/`.

**Legacy and Primitive Mapping:** Product Brief Ideogram 4 doctrine, Creative Pipeline V2. Active families: VSG, SAF, FBK.

**Prerequisites:** Stories 7.1 and 7.2.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
