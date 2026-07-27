---
story_id: "7.1"
story_title: "Complete Editing Session Creation From Approved Source"
epic_id: 7
epic_title: "Complete Editing Sessions and Reproducible Scenes"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-07.01"
pipeline_stage: "9"
entry_object: "approved moment, route, brand context"
exit_object: "`CompleteEditingSession`"
validation_contract: "source approval and brand lock"
required_receipt: "editing session receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 7.1: Complete Editing Session Creation From Approved Source

**Epic:** 7 - Complete Editing Sessions and Reproducible Scenes
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-07.01 |
| Canonical Pipeline Stage | 9 |
| Entry Object | approved moment, route, brand context |
| Exit Object | `CompleteEditingSession` |
| Validation Contract | source approval and brand lock |
| Required Receipt | editing session receipt |
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

As a Production Steward, I want to create Complete Editing Sessions only from approved Expression Moments, route decisions, Asset Package items, and locked Brand Context Versions, so that editing never begins from unsupported material.

**Acceptance Criteria:**

- Given an approved Expression Moment and route exist, when a Complete Editing Session is created, then it binds source expression, route, asset package item if present, locked Brand Context Version, actor, brand, and status.
- Given Expression Moment approval is missing, when creation is attempted, then the command fails.
- Given Brand Context Version is unlocked or stale, when creation is attempted, then the command fails.
- Given the session is created, when persisted, then `CompleteEditingSessionCreated` event and audit receipt are written.
- Given the session is queried, when displayed, then source, route, brand context, and production readiness are visible.

**Technical Notes:** Implement `CompleteEditingSession`, `CreateCompleteEditingSession`, and workflow start after source/brand gates.

**Legacy and Primitive Mapping:** Creative Pipeline V2, V9.1 expression routing, Brand Genesis V3. Active families: SAF, STR, VSG.

**Prerequisites:** Epics 1 through 6.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
