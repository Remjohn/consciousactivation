---
story_id: "4.1"
story_title: "Brand Genesis Intake and Session Creation"
epic_id: 4
epic_title: "Brand Genesis and Locked Creative Universe"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-04.01"
pipeline_stage: "2"
entry_object: "brand intake and consent"
exit_object: "`BrandGenesisSession`"
validation_contract: "source/consent completeness"
required_receipt: "genesis start receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 4.1: Brand Genesis Intake and Session Creation

**Epic:** 4 - Brand Genesis and Locked Creative Universe
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-04.01 |
| Canonical Pipeline Stage | 2 |
| Entry Object | brand intake and consent |
| Exit Object | `BrandGenesisSession` |
| Validation Contract | source/consent completeness |
| Required Receipt | genesis start receipt |
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

As an Operator, I want to run Brand Genesis from consent, source media, brand notes, audience, offer, forbidden tone, visual preferences, Voice DNA, visual constitution, and negative-space inputs, so that the creative universe starts from grounded brand evidence.

**Acceptance Criteria:**

- Given an Operator creates a Brand Genesis Session, when required intake is submitted, then the system records brand notes, audience, offer, forbidden tone, visual preferences, Voice DNA references, source media, negative-space inputs, and consent compatibility.
- Given source media lacks consent, when Brand Genesis starts, then the workflow is blocked with `CONSENT_SCOPE_BLOCKED`.
- Given intake is incomplete, when generation is requested, then the system shows missing evidence rather than fabricating a brand constitution.
- Given intake passes, when the workflow starts, then a `BrandGenesisSession` record and receipt are created.
- Given a session is brand-scoped, when another brand is active, then the session cannot be queried or reused across brand boundaries.

**Technical Notes:** Use BrandGenesisWorkflow first steps, `BrandGenesisSession`, `BrandSourceInput`, `VoiceDnaReference`, consent policy, and object storage under `brands/{brand_id}/brand-genesis/`.

**Legacy and Primitive Mapping:** Brand Genesis V3 and Legacy Inventory visual/sonic doctrine. Active families: VSG, VOC, SAF, PER.

**Prerequisites:** Epics 1 through 3.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
