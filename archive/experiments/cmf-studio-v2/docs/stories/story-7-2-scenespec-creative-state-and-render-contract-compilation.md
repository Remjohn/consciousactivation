---
story_id: "7.2"
story_title: "SceneSpec, Creative State, and Render Contract Compilation"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-07.02"
pipeline_stage: "9"
entry_object: "editing session"
exit_object: "`SceneSpec`, `CreativeState`, `RenderContract`"
validation_contract: "asset/variant/revision validation"
required_receipt: "SceneSpec receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 7.2: SceneSpec, Creative State, and Render Contract Compilation

**Epic:** 7 - Complete Editing Sessions and Reproducible Scenes
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-07.02 |
| Canonical Pipeline Stage | 9 |
| Entry Object | editing session |
| Exit Object | `SceneSpec`, `CreativeState`, `RenderContract` |
| Validation Contract | asset/variant/revision validation |
| Required Receipt | SceneSpec receipt |
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

As a Production Steward, I want the system to compile SceneSpecs, Creative State, Render Contracts, asset selections, renderer routes, evaluation requirements, platform variants, and revision policies, so that each job is executable and reviewable.

**Acceptance Criteria:**

- Given a Complete Editing Session exists, when compilation runs, then it produces `SceneSpec`, `CreativeState`, `RenderContract`, `AssetSelection`, platform variants, evaluation requirements, and revision policy.
- Given selected assets are not approved in the locked Brand Context Version, when compilation validates, then it fails.
- Given platform variants require captions or negative space, when Render Contract is compiled, then those constraints are explicit.
- Given revision policy is missing, when provider jobs are queued, then the workflow blocks until the policy exists.
- Given compilation succeeds, when the receipt is written, then it references source expression, route, brand context, and input hashes.

**Technical Notes:** Use `SceneSpecCompiled` event, `scene_specs`, `creative_states`, `render_contracts`, and contract tests.

**Legacy and Primitive Mapping:** CMF engine manifest lineage, Creative Pipeline V2. Active families: VSG, STR, FBK.

**Prerequisites:** Story 7.1.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
