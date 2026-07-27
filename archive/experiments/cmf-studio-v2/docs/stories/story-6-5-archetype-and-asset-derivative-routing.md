---
story_id: "6.5"
story_title: "Archetype and Asset Derivative Routing"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-06.05"
  - "FR-CMF-06.07"
pipeline_stage: "7"
entry_object: "approved Expression Moment"
exit_object: "`AssetRouteReceipt`"
validation_contract: "registry route and source support"
required_receipt: "routing receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 6.5: Archetype and Asset Derivative Routing

**Epic:** 6 - Complete Expression Sessions and Guest Asset Packs
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-06.05, FR-CMF-06.07 |
| Canonical Pipeline Stage | 7 |
| Entry Object | approved Expression Moment |
| Exit Object | `AssetRouteReceipt` |
| Validation Contract | registry route and source support |
| Required Receipt | routing receipt |
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

As a Production Steward, I want approved Expression Moments routed through Core Content Archetype, Asset Derivative, Meme Mechanism, Reaction Archetype, and CMF Render Mode registries, so that every output format is valid and source-supported.

**Acceptance Criteria:**

- Given an Expression Moment is approved, when routing runs, then it evaluates only active migrated registry entries.
- Given a route is selected, when the receipt is written, then it includes expression moment ID, route ID, registry versions, evidence, route rationale, and failure alternatives.
- Given an Expression Moment lacks evidence for a requested route, when routing runs, then the route is rejected rather than fabricated.
- Given a format is unsupported by the registries, when requested, then the system blocks it with a clear unsupported-format receipt.
- Given a route passes, when an Asset Package Spec is generated later, then route lineage remains attached.

**Technical Notes:** Implement `ArchetypeRoute`, registry query service, `RouteSelectionProgram`, and unsupported-format rejection.

**Legacy and Primitive Mapping:** Archetype System Migration Proposition, 96 archetype prompts, 34 creative subsystems. Active families: STR, HUM, TRG, PSY.

**Prerequisites:** Stories 3.2, 3.3, and 6.4.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
