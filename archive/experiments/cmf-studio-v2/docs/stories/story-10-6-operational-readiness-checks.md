---
story_id: "10.6"
story_title: "Operational Readiness Checks"
epic_id: 10
epic_title: "Evidence Memory, Neo4j Projection, and Recovery"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-10.07"
pipeline_stage: "release readiness overlay"
entry_object: "system fixtures and production chain"
exit_object: "readiness report"
validation_contract: "full brand-cycle and rebuild gates"
required_receipt: "readiness receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 10.6: Operational Readiness Checks

**Epic:** 10 - Evidence Memory, Neo4j Projection, and Recovery
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-10.07 |
| Canonical Pipeline Stage | release readiness overlay |
| Entry Object | system fixtures and production chain |
| Exit Object | readiness report |
| Validation Contract | full brand-cycle and rebuild gates |
| Required Receipt | readiness receipt |
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

As an Owner or Operator, I want operational readiness checks for restore drills, provider outage handling, GPU worker shutdown, memory rebuild, Neo4j projection rebuild, and a complete brand cycle, so that the system proves readiness before real production pressure.

**Acceptance Criteria:**

- Given readiness checks run, when restore drill is executed, then the system verifies canonical state, object storage references, receipts, and projection rebuild ability.
- Given provider outage simulation runs, when jobs are interrupted, then recovery actions preserve completed artifacts and avoid duplicate external side effects.
- Given GPU worker shutdown check runs, when queue drains, then cost reporting and shutdown state are recorded.
- Given memory rebuild check runs, when memory events are replayed, then approved, expired, reversed, and quarantined states are preserved.
- Given full brand cycle check runs, when it completes, then it proves Brand Genesis, interview prep, expression session, package generation, editing, rendering, review, publishing intent, memory, operations, and projection health without manual database edits.

**Technical Notes:** Implement readiness commands, automated checks, fixtures, and reports under operations. These checks become release gates for production operation.

**Legacy and Primitive Mapping:** Product Brief final human acceptance, Greenfield Context release gates, Legacy Inventory spec/build protocols. Active families: SAF, BUS, FBK.

**Prerequisites:** Stories 10.1 through 10.5.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
