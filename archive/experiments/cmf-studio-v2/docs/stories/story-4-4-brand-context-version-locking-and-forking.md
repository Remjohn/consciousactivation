---
story_id: "4.4"
story_title: "Brand Context Version Locking and Forking"
epic_id: 4
epic_title: "Brand Genesis and Locked Creative Universe"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-04.06"
  - "FR-CMF-04.07"
pipeline_stage: "2"
entry_object: "approved genesis assets"
exit_object: "locked/forked `BrandContextVersion`"
validation_contract: "review and version immutability"
required_receipt: "genesis clearance receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 4.4: Brand Context Version Locking and Forking

**Epic:** 4 - Brand Genesis and Locked Creative Universe
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-04.06, FR-CMF-04.07 |
| Canonical Pipeline Stage | 2 |
| Entry Object | approved genesis assets |
| Exit Object | locked/forked `BrandContextVersion` |
| Validation Contract | review and version immutability |
| Required Receipt | genesis clearance receipt |
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

As an Operator, I want to lock approved Brand Context Versions and fork them for approved changes, so that production can rely on stable creative truth while future changes remain traceable.

**Acceptance Criteria:**

- Given all required Brand Genesis assets pass review, when the Operator locks a Brand Context Version, then the system writes a `GenesisClearanceCertificate`.
- Given a locked version exists, when a production job references it, then the job can only select assets approved within that version.
- Given an Operator changes a core visual identity rule, when future renders need the change, then the system creates a forked Brand Context Version rather than mutating the old version.
- Given an old render is audited, when its brand context is inspected, then it resolves to the exact locked version used at render time.
- Given a stale or cross-brand Brand Context Version is selected, when production starts, then SceneSpec compilation is blocked.

**Technical Notes:** Use immutable `BrandContextVersion`, `GenesisClearanceCertificate`, and version hash references in every downstream SceneSpec and RenderContract.

**Legacy and Primitive Mapping:** Brand Genesis V3 versioning doctrine. Active families: SAF, PER, VSG.

**Prerequisites:** Stories 4.1 through 4.3.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
