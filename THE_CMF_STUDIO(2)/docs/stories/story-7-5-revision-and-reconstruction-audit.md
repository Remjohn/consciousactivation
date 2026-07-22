---
story_id: "7.5"
story_title: "Revision and Reconstruction Audit"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-07.07"
  - "FR-CMF-07.08"
pipeline_stage: "9 / 12 / 13"
entry_object: "revision request"
exit_object: "revision chain and audit view"
validation_contract: "lineage preservation"
required_receipt: "revision receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 7.5: Revision and Reconstruction Audit

**Epic:** 7 - Complete Editing Sessions and Reproducible Scenes
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-07.07, FR-CMF-07.08 |
| Canonical Pipeline Stage | 9 / 12 / 13 |
| Entry Object | revision request |
| Exit Object | revision chain and audit view |
| Validation Contract | lineage preservation |
| Required Receipt | revision receipt |
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

As a Reviewer or Operator, I want revisions to preserve source lineage, composition lineage, provider receipts, evaluation history, version history, and approval history, so that final scenes remain reconstructable.

**Acceptance Criteria:**

- Given a scene is revised, when the revision command is saved, then it records reason, changed fields, prior version, actor, source lineage, provider receipts, and evaluation state.
- Given a scene is revised multiple times, when final audit opens, then every revision can be traced to source expression, route, brand context, provider job, evaluation receipt, and human decision.
- Given a revision would drop source lineage, when validation runs, then it is blocked.
- Given a render is approved after revisions, when approval is saved, then approval references the final version and prior revision chain.
- Given a user asks why a scene looks the way it does, when reconstruction runs, then the system resolves source, route, brand context, composition JSON, provider jobs, render manifests, and approvals.

**Technical Notes:** Implement revision history for `complete_editing_sessions`, `scene_specs`, `render_outputs`, `evaluation_receipts`, and approval events.

**Legacy and Primitive Mapping:** CMF beat-fingerprint/manifest lineage doctrine. Active families: FBK, SAF, PER.

**Prerequisites:** Stories 7.1 through 7.4.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
