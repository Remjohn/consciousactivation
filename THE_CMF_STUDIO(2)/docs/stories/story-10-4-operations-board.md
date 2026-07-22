---
story_id: "10.4"
story_title: "Operations Board"
epic_id: 10
epic_title: "Evidence Memory, Neo4j Projection, and Recovery"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-10.05"
pipeline_stage: "operations overlay"
entry_object: "queues/incidents/jobs"
exit_object: "operations board state"
validation_contract: "canonical-state-only reads"
required_receipt: "operations receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 10.4: Operations Board

**Epic:** 10 - Evidence Memory, Neo4j Projection, and Recovery
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-10.05 |
| Canonical Pipeline Stage | operations overlay |
| Entry Object | queues/incidents/jobs |
| Exit Object | operations board state |
| Validation Contract | canonical-state-only reads |
| Required Receipt | operations receipt |
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

As an Operator, I want an Operations Board showing queue depth, active workers, render tier, provider status, failures, retries, checkpoints, costs, consent blockers, approval blockers, publish readiness, and memory blockers, so that the full system is operable without hidden scripts.

**Acceptance Criteria:**

- Given jobs are running, when the Operations Board opens, then it shows queue depth, active workers, GPU tier, provider status, workflow checkpoints, retry state, costs, and blockers.
- Given a provider outage occurs, when the board refreshes, then affected jobs, completed artifacts, safe retries, costs, blockers, and recommended recovery actions are visible.
- Given consent or approval blocks work, when the board renders, then the blocker links to the exact object and required decision.
- Given a worker is draining, when no jobs remain, then shutdown status and final cost are visible.
- Given an incident is resolved, when recovery completes, then incident history and receipts remain available.

**Technical Notes:** Read from `provider_jobs`, `operational_incidents`, `recovery_actions`, workflow checkpoints, cost receipts, and projection health. No manual database edits.

**Legacy and Primitive Mapping:** Legacy operations and circuit-breaker references. Active families: FBK, BUS, FRC, SAF.

**Prerequisites:** Epics 1 through 9 and Story 10.3.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
