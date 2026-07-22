---
story_id: "6.1"
story_title: "Complete Expression Session Creation"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-06.01"
pipeline_stage: "5"
entry_object: "approved contracts and setup"
exit_object: "`CompleteExpressionSession`"
validation_contract: "consent and recording readiness"
required_receipt: "session start receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 6.1: Complete Expression Session Creation

**Epic:** 6 - Complete Expression Sessions and Guest Asset Packs
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-06.01 |
| Canonical Pipeline Stage | 5 |
| Entry Object | approved contracts and setup |
| Exit Object | `CompleteExpressionSession` |
| Validation Contract | consent and recording readiness |
| Required Receipt | session start receipt |
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

As an Operator, I want to create and manage a Complete Expression Session from approved interview contracts, recording configuration, source artifacts, quality gates, and consent state, so that capture begins from a governed plan.

**Acceptance Criteria:**

- Given an approved Interview Asset Contract exists, when the Operator creates a session, then the session binds brand ID, guest/client, consent state, recording configuration, source requirements, interview contract, and status.
- Given consent or recording setup is incomplete, when session start is requested, then the command is blocked.
- Given the Operator changes active brand context, when the session is queried, then only sessions from the active brand are returned.
- Given a session starts, when the command succeeds, then `CompleteExpressionSessionStarted` event and audit receipt are written.
- Given the session is paused or marked failed, when status changes, then state transitions use explicit statuses.

**Technical Notes:** Implement `CompleteExpressionSession`, `CreateCompleteExpressionSession`, session status machine, and workflow start command.

**Legacy and Primitive Mapping:** V9.1 Complete Expression Session schema. Active families: SAF, STR, FBK.

**Prerequisites:** Epics 1 through 5.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
