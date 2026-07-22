---
story_id: "10.3"
story_title: "Neo4j Relationship Projection"
epic_id: 10
epic_title: "Evidence Memory, Neo4j Projection, and Recovery"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-21"
fr_ids:
  - "FR-CMF-10.03"
  - "FR-CMF-10.04"
pipeline_stage: "14"
entry_object: "domain event checkpoint"
exit_object: "Neo4j projection event"
validation_contract: "rebuild and lag validation"
required_receipt: "projection receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 10.3: Neo4j Relationship Projection

**Epic:** 10 - Evidence Memory, Neo4j Projection, and Recovery
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Traceability

| Field | Value |
|---|---|
| FR IDs | FR-CMF-10.03, FR-CMF-10.04 |
| Canonical Pipeline Stage | 14 |
| Entry Object | domain event checkpoint |
| Exit Object | Neo4j projection event |
| Validation Contract | rebuild and lag validation |
| Required Receipt | projection receipt |
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

As an Operator, I want Neo4j to expose relationships among brand, guest, session, expression, archetype, asset, approval, publishing, provider, and memory entities, so that I can reason about production patterns without risking canonical state.

**Acceptance Criteria:**

- Given domain events are written, when projection runs, then Neo4j nodes and relationships are updated from canonical events.
- Given Neo4j is unavailable, when canonical workflows run, then production continues and projection lag is recorded.
- Given projection is rebuilt, when checkpoints are selected, then the graph is reconstructed from canonical events and validated against expected counts.
- Given a graph query informs an operator insight, when an action is taken, then the actual state change still goes through Command Bus and PostgreSQL canonical state.
- Given projection data conflicts with PostgreSQL, when detected, then projection is marked unhealthy and rebuild is required.

**Technical Notes:** Implement projection outbox, `ProjectionCheckpoint`, Neo4j driver integration, `/api/v1/projections`, and `ProjectionRebuildWorkflow`.

**Legacy and Primitive Mapping:** Product Brief Neo4j state retention updated by architecture boundary. Active families: BUS, FBK, SAF.

**Prerequisites:** Story 10.1 and domain events from prior epics.

## Tech Spec Handoff Requirements

- Include `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, this story file, and feature-specific source docs.
- Include `RequirementTrace` for the FR IDs listed above.
- Include `PipelineStageTrace` with the stage, entry object, exit object, validation contract, and required receipt listed above.
- Preserve the legacy and primitive mapping from this story; do not collapse it into generic prompt language.
- Include CBAR tension, failure scenario, resolution demand, and downstream proof.
- Define Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
