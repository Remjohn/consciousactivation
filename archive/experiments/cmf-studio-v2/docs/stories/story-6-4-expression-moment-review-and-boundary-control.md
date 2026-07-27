---
story_id: "6.4"
story_title: "Expression Moment Review and Boundary Control"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-06.04"
pipeline_stage: "6"
entry_object: "moment candidates"
exit_object: "approved/superseded Expression Moments"
validation_contract: "reviewer boundary gate"
required_receipt: "expression review receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 6.4: Expression Moment Review and Boundary Control

**Epic:** 6 - Complete Expression Sessions and Guest Asset Packs
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-06.04 |
| Canonical Pipeline Stage | 6 |
| Entry Object | moment candidates |
| Exit Object | approved/superseded Expression Moments |
| Validation Contract | reviewer boundary gate |
| Required Receipt | expression review receipt |
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

As a Reviewer, I want to approve, reject, fix boundaries, split, merge, annotate, or place sensitivity holds on Expression Moments, so that only truthful, usable source fragments reach routing.

**Acceptance Criteria:**

- Given candidates exist, when the Reviewer opens the review surface, then each candidate shows source video/audio reference, transcript segment, timestamp range, induction context, route rationale, and sensitivity flags.
- Given a boundary is wrong, when the Reviewer fixes it, then the system writes a supersession record and preserves the original candidate.
- Given two candidates belong together, when merge is approved, then the merged Expression Moment records both source ranges.
- Given a sensitivity hold is placed, when routing is attempted, then routing is blocked until the hold is resolved.
- Given an Expression Moment is approved, when stored, then it becomes immutable except through supersession.

**Technical Notes:** Implement `ExpressionMoment`, review commands, status machine, and immutable approval events.

**Legacy and Primitive Mapping:** V9.1 review doctrine, CBAR, receipt chain. Active families: FBK, SAF, PER.

**Prerequisites:** Stories 6.1 through 6.3.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
