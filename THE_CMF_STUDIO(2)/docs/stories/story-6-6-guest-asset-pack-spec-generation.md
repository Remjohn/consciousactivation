---
story_id: "6.6"
story_title: "Guest Asset Pack Spec Generation"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-06.06"
pipeline_stage: "8"
entry_object: "route receipts and offer"
exit_object: "`AssetPackageSpec`"
validation_contract: "source sufficiency and commercial guardrail"
required_receipt: "package spec receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 6.6: Guest Asset Pack Spec Generation

**Epic:** 6 - Complete Expression Sessions and Guest Asset Packs
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-06.06 |
| Canonical Pipeline Stage | 8 |
| Entry Object | route receipts and offer |
| Exit Object | `AssetPackageSpec` |
| Validation Contract | source sufficiency and commercial guardrail |
| Required Receipt | package spec receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Convert live narrative induction and grounded transcript/source extraction into approved Expression Moments, valid routes, and source-backed Guest Asset Pack specs.

**Covers:** FR-CMF-06.01 through FR-CMF-06.08.

**User Value:** Operators and Reviewers can transform an interview into routable assets without fabricating beyond source expression.

**Technical Context:** `/api/v1/expression-sessions`, `/api/v1/expression-moments`, `/api/v1/asset-packages`, CompleteExpressionSessionWorkflow, recording artifacts, transcript revisions, timestamped anchor hits, expression moments, archetype routes, asset package specs.

**CBAR Failure Scenario:** If the system only hunts clips after the transcript exists, it misses the human induction layer. If it routes by generic format, it fabricates. The resolution is dual-layer extraction plus valid route registries.

## Story Definition

As a Production Steward, I want to generate trial Guest Asset Pack specs from approved, routed Expression Moments, so that pack deliverables remain source-backed and commercially aligned.

**Acceptance Criteria:**

- Given enough approved source material exists, when a trial Guest Asset Pack spec is generated, then it targets 4 videos, 2 carousels, 2 meme visuals, 2 poll visuals, and 2-3 reaction seeds where source supports them.
- Given source material does not support one item, when the pack is generated, then the system marks the gap instead of inventing material.
- Given a package item is listed, when reviewed, then it maps to Expression Moment, route, registry entry, brand context requirement, evaluation state, and production readiness.
- Given the commercial entitlement is trial Guest Asset Pack, when pack scope is rendered, then it uses `$29/week` trial language only.
- Given a package is approved, when Complete Editing Sessions are created, then each item carries source lineage and route state.

**Technical Notes:** Implement `AssetPackageSpec`, `AssetPackageItem`, `/api/v1/asset-packages`, and package evaluation receipt.

**Legacy and Primitive Mapping:** V9.1 Guest Asset Pack standard. Active families: BUS, STR, FBK.

**Prerequisites:** Stories 6.1 through 6.5.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
