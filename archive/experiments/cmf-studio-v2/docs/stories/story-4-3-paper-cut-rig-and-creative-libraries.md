---
story_id: "4.3"
story_title: "Paper-Cut Rig and Creative Libraries"
epic_id: 4
epic_title: "Brand Genesis and Locked Creative Universe"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-04.03"
  - "FR-CMF-04.04"
  - "FR-CMF-04.05"
pipeline_stage: "2"
entry_object: "creative generation request"
exit_object: "rig and creative libraries"
validation_contract: "layer/anchor/preview validation"
required_receipt: "creative library receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 4.3: Paper-Cut Rig and Creative Libraries

**Epic:** 4 - Brand Genesis and Locked Creative Universe
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-04.03, FR-CMF-04.04, FR-CMF-04.05 |
| Canonical Pipeline Stage | 2 |
| Entry Object | creative generation request |
| Exit Object | rig and creative libraries |
| Validation Contract | layer/anchor/preview validation |
| Required Receipt | creative library receipt |
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

As an Operator, I want to create and validate the paper-cut avatar rig, props, micro-semiotic anchors, motion recipes, SFX libraries, composition preferences, platform profiles, and publishing profiles, so that rendering has reusable, approved brand parts.

**Acceptance Criteria:**

- Given a paper-cut rig is generated, when validation runs, then the rig manifest includes layer separation, pivot points, mouth shapes, eye/brow variants, gesture variants, body layers, and preview tests.
- Given a rig preview fails mouth, pivot, layer, or gesture validation, when review opens, then the Operator can repair or reject the rig before lock.
- Given props, anchors, motion recipes, or SFX assets are added, when saved, then each has source, version hash, use constraints, and evaluation state.
- Given a platform profile is configured, when render contracts are compiled, then platform variants inherit caption, negative-space, aspect, and publishing requirements.
- Given a creative library item is cross-brand, when selected, then brand scope validation blocks it.

**Technical Notes:** Implement `RigManifest`, `MicroSemioticAnchor`, `MotionRecipe`, `SfxAsset`, `CompositionPreference`, `PlatformProfile`, and object storage in `brand-genesis`, `rigs`, and `acting-library` paths.

**Legacy and Primitive Mapping:** Brand Genesis V3, Creative Pipeline V2, legacy CMF engine references. Active families: VSG, ACT, VOC, SAF.

**Prerequisites:** Stories 4.1 and 4.2.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
