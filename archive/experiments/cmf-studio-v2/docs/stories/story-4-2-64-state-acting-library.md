---
story_id: "4.2"
story_title: "64-State Acting Library"
epic_id: 4
epic_title: "Brand Genesis and Locked Creative Universe"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-04.02"
  - "FR-CMF-04.05"
pipeline_stage: "2"
entry_object: "brand source and generation request"
exit_object: "acting library version"
validation_contract: "likeness/gesture/style gate"
required_receipt: "acting library receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 4.2: 64-State Acting Library

**Epic:** 4 - Brand Genesis and Locked Creative Universe
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-04.02, FR-CMF-04.05 |
| Canonical Pipeline Stage | 2 |
| Entry Object | brand source and generation request |
| Exit Object | acting library version |
| Validation Contract | likeness/gesture/style gate |
| Required Receipt | acting library receipt |
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

As an Operator, I want to generate, evaluate, repair, reject, approve, and lock a 64-state acting library, so that future scenes can express emotion and gesture without identity drift.

**Acceptance Criteria:**

- Given acting references are generated, when the grid is shown, then each reference includes emotional family, gesture family, source inputs, provider receipt, and evaluation state.
- Given likeness, gesture clarity, hand quality, style adherence, or production usability fails, when the Operator reviews the reference, then they can reject, repair, or replace it.
- Given a reference is approved, when the acting library version is locked, then the reference is immutable except through a new version.
- Given production attempts to use an unapproved acting reference, when SceneSpec compilation runs, then the command is blocked.
- Given acting reference evaluation changes, when the library version is already locked, then historical outputs remain tied to their original locked version.

**Technical Notes:** Implement `ActingReference`, `ActingLibraryVersion`, evaluation receipts, provider job linkage, and lock command.

**Legacy and Primitive Mapping:** Brand Genesis V3 64-state acting library, Voice DNA doctrine, CMF visual constitution. Active families: ACT, VSG, SAF.

**Prerequisites:** Story 4.1.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
