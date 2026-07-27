---
story_id: "10.5"
story_title: "Workflow Recovery Actions"
epic_id: 10
epic_title: "Evidence Memory, Neo4j Projection, and Recovery"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-10.06"
pipeline_stage: "operations overlay"
entry_object: "failed workflow/job"
exit_object: "`RecoveryAction`"
validation_contract: "idempotent safe-action validation"
required_receipt: "recovery receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 10.5: Workflow Recovery Actions

**Epic:** 10 - Evidence Memory, Neo4j Projection, and Recovery
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-10.06 |
| Canonical Pipeline Stage | operations overlay |
| Entry Object | failed workflow/job |
| Exit Object | `RecoveryAction` |
| Validation Contract | idempotent safe-action validation |
| Required Receipt | recovery receipt |
| Source PRD | `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` |
| Source Architecture | `docs/architecture.md` |
| Source Pipeline Map | `docs/cmf-studio-pipeline-map.md` |
| Source Legacy Inventory | `docs/migration/legacy-inventory.md` |

## Epic Context

**Epic Goal:** Let CMF STUDIO learn from approved evidence, expose relationship intelligence through Neo4j, and recover workflows without hidden scripts or manual database edits.

**Covers:** FR-CMF-10.01 through FR-CMF-10.07.

**User Value:** Operators can inspect memory, relationships, queues, failures, costs, blockers, and recovery actions while canonical state remains safe and rebuildable.

**Technical Context:** `/api/v1/memory`, `/api/v1/operations`, `/api/v1/projections`, `memory_admission_candidates`, `memory_events`, `projection_checkpoints`, `operational_incidents`, `recovery_actions`, Neo4j projection, domain event outbox.

**CBAR Failure Scenario:** If memory becomes lore, it will corrupt future interviews and routes. If Neo4j becomes canonical, production decisions become unrecoverable. Evidence memory and graph projection must remain governed and rebuildable.

## Story Definition

As an Operator, I want to retry, resume, cancel, compensate, or quarantine provider jobs and workflows idempotently, so that routine failures can be recovered safely.

**Acceptance Criteria:**

- Given a workflow is paused or failed, when the Operator opens recovery, then safe actions are derived from current state, completed artifacts, receipts, and consent compatibility.
- Given retry is safe, when submitted, then only incomplete work is retried.
- Given cancel is selected, when valid, then the workflow records terminal or compensated state with receipt.
- Given quarantine is required, when approved, then affected assets, memory, provider jobs, or publishing intents are blocked from future use.
- Given recovery would corrupt completed work or duplicate external action, when validation runs, then the command is blocked.

**Technical Notes:** Durable workflows own recovery semantics. Use `RecoveryAction`, `OperationalIncident`, workflow checkpoint IDs, and idempotency keys.

**Legacy and Primitive Mapping:** Receipt-chain and CBAR failure handling doctrine. Active families: SAF, FBK.

**Prerequisites:** Stories 8.7, 10.3, and 10.4.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
