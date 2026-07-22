---
story_id: "6.3"
story_title: "Anchor Hit and Expression Moment Candidate Detection"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-06.03"
pipeline_stage: "6"
entry_object: "aligned transcript/source"
exit_object: "candidate Expression Moments"
validation_contract: "source truth and JIT skill validation"
required_receipt: "extraction receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 6.3: Anchor Hit and Expression Moment Candidate Detection

**Epic:** 6 - Complete Expression Sessions and Guest Asset Packs
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-06.03 |
| Canonical Pipeline Stage | 6 |
| Entry Object | aligned transcript/source |
| Exit Object | candidate Expression Moments |
| Validation Contract | source truth and JIT skill validation |
| Required Receipt | extraction receipt |
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

As an Operator, I want the system to detect anchor hits, emotional shifts, transcript segments, timestamps, cues, and candidate Expression Moments, so that review starts from source-backed possibilities.

**Acceptance Criteria:**

- Given aligned transcript and source artifacts exist, when extraction runs, then each candidate includes timestamp range, transcript segment, source artifact reference, induction context, anchor hit, route rationale, and confidence.
- Given an emotional shift is detected, when candidate output is produced, then the system cites evidence rather than only labeling sentiment.
- Given a candidate lacks source support, when extraction completes, then it is marked rejected candidate or needs review, not approved.
- Given a JIT Skill compiler participates, when it emits candidates, then it returns saturation context, contrast output, and anti-draft calibration.
- Given extraction fails, when the workflow retries, then previous accepted artifacts and receipts remain intact.

**Technical Notes:** Implement `TimestampedAnchorHit`, `ExpressionMomentCandidate`, DSPy extraction programs, and JIT compiler receipts.

**Legacy and Primitive Mapping:** V9/V9.1 expression extraction, 96 archetype prompts, JIT skills, RSCS. Active families: STR, TRG, PSY, VOC.

**Prerequisites:** Stories 6.1 and 6.2.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
