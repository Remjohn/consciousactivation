---
story_id: "4.5"
story_title: "Production Gate to Locked Brand Context"
epic_id: 4
epic_title: "Brand Genesis and Locked Creative Universe"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-04.07"
pipeline_stage: "9 / 10"
entry_object: "production job request"
exit_object: "allowed or blocked SceneSpec compile"
validation_contract: "locked brand context"
required_receipt: "brand context gate receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 4.5: Production Gate to Locked Brand Context

**Epic:** 4 - Brand Genesis and Locked Creative Universe
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-04.07 |
| Canonical Pipeline Stage | 9 / 10 |
| Entry Object | production job request |
| Exit Object | allowed or blocked SceneSpec compile |
| Validation Contract | locked brand context |
| Required Receipt | brand context gate receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Let Operators manufacture, evaluate, repair, approve, and lock the brand creative universe before production depends on it.

**Covers:** FR-CMF-04.01 through FR-CMF-04.07.

**User Value:** Operators and Production Stewards can reuse approved identity, acting, visual, sonic, motion, prop, and publishing assets instead of reinventing the brand for each clip.

**Technical Context:** `/api/v1/brand-genesis`, BrandGenesisWorkflow, `brand_genesis_sessions`, `brand_context_versions`, `genesis_clearance_certificates`, `acting_references`, `rig_manifests`, `micro_semiotic_anchors`, `motion_recipes`, `sfx_assets`, `composition_preferences`.

**CBAR Failure Scenario:** If production starts before brand context is locked, every asset becomes a one-off taste decision. Brand Genesis must therefore produce immutable, reviewed creative truth before rendering begins.

## Story Definition

As a Production Steward, I want production jobs to require an approved, locked, brand-scoped context, so that no scene can use unapproved or stale identity assets.

**Acceptance Criteria:**

- Given a Complete Editing Session is created, when Brand Context Version is missing or unlocked, then the command fails.
- Given a SceneSpec selects acting references, props, anchors, motion recipes, SFX assets, or caption rules, when validation runs, then each selection must belong to the locked brand context.
- Given a Brand Context Version is superseded, when an old scene is revised, then the Operator must choose whether to preserve original context or explicitly fork into the new approved context.
- Given provider jobs are queued, when they reference brand assets, then provider receipts include Brand Context Version ID and selected asset hashes.
- Given a Reviewer inspects a render, when context lineage is opened, then they can see the locked creative universe behind it.

**Technical Notes:** Enforce brand context gates in CompleteEditingSessionWorkflow, SceneSpec compilation, provider request construction, and review views.

**Legacy and Primitive Mapping:** CMF lineage doctrine, Brand Genesis V3, Creative Pipeline V2. Active families: VSG, SAF, FBK.

**Prerequisites:** Stories 4.1 through 4.4.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
