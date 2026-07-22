---
story_id: "6.7"
story_title: "Rejected Candidate and Coalition-Fatality Memory"
epic_id: 6
epic_title: "Complete Expression Sessions and Guest Asset Packs"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-06.08"
pipeline_stage: "6 / 7 / 14"
entry_object: "rejected candidate/route"
exit_object: "failure corpus or memory candidate"
validation_contract: "consent and non-truth admission gate"
required_receipt: "rejection receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 6.7: Rejected Candidate and Coalition-Fatality Memory

**Epic:** 6 - Complete Expression Sessions and Guest Asset Packs
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-06.08 |
| Canonical Pipeline Stage | 6 / 7 / 14 |
| Entry Object | rejected candidate/route |
| Exit Object | failure corpus or memory candidate |
| Validation Contract | consent and non-truth admission gate |
| Required Receipt | rejection receipt |
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

As an Operator, I want failed candidates, rejected routes, and coalition-fatality evidence preserved without becoming truth, so that future compilers learn from failures safely.

**Acceptance Criteria:**

- Given a candidate is rejected, when rejection is saved, then the system stores reason, evidence, reviewer, route attempt, and failure category.
- Given a route fails because source support is insufficient, when the failure is stored, then it is available as negative evidence for JIT compilers and future routing evals.
- Given rejected material contains sensitive or consent-incompatible content, when preservation is attempted, then it is blocked or quarantined according to consent policy.
- Given a future compiler references a rejected pattern, when it uses the evidence, then it must cite the rejection and cannot treat it as approved truth.
- Given memory admission is later proposed from rejected evidence, when reviewed, then it requires explicit evidence and cannot bypass memory gates.

**Technical Notes:** Store rejected candidates, route failures, and failure corpora with source references and consent checks. Do not admit as memory until Epic 10 gates.

**Legacy and Primitive Mapping:** SFL failure corpus, CBAR, RSCS evaluation. Active families: FBK, SAF, STR.

**Prerequisites:** Stories 6.3 through 6.6.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
