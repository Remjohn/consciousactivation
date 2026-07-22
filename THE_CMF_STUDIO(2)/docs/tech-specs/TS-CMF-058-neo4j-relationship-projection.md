---
tech_spec_id: "TS-CMF-058"
title: "Neo4j Relationship Projection"
story_id: "10.3"
story_title: "Neo4j Relationship Projection"
epic_id: 10
epic_title: "Evidence Memory, Neo4j Projection, and Recovery"
status: "ready-for-development"
created_at: "2026-06-21"
source_story: "docs/stories/story-10-3-neo4j-relationship-projection.md"
fr_ids:
  - "FR-CMF-10.03"
  - "FR-CMF-10.04"
pipeline_stage: "14"
entry_object: "domain event checkpoint"
exit_object: "Neo4j projection event"
validation_contract: "rebuild and lag validation"
required_receipt: "projection receipt"
runtime_target: "Python / FastAPI / Pydantic v2 / Neo4j driver / event outbox / projection workflow"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-058: Neo4j Relationship Projection

**Status:** Ready for Development  
**Story:** `10.3 - Neo4j Relationship Projection`  
**Implementation Boundary:** Domain event outbox projection, ProjectionCheckpoint, Neo4j node/relationship writer, projection lag, rebuild workflow, projection health, and projection receipt.

## 1. Files Read

| File | Purpose |
|---|---|
| `docs/stories/story-10-3-neo4j-relationship-projection.md` | Story source and acceptance criteria. |
| `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | FR-CMF-10.03 and FR-CMF-10.04 authority. |
| `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md` | PostgreSQL and Neo4j projection doctrine. |
| `THE CMF STUDIO/CCP_STUDIO_GREENFIELD_AGENT_CONTEXT_V2_PYTHON_DSPY_PI.md` | Postgres/Neo4j relationship examples and projection retry behavior. |
| `docs/architecture.md` | AD-008, canonical store boundary, projection nodes, and rebuild workflow. |
| `docs/cmf-studio-pipeline-map.md` | Stage 14 projection trace. |
| `docs/migration/legacy-inventory.md` | Legacy graph/state retention references. |

## 2. Overview

Neo4j is a rebuildable relationship projection. It exposes relationships among brand, guest, session, expression, archetype, asset, approval, publishing, provider, and memory entities for inspection and analysis. Production state transitions still go through Command Bus, PostgreSQL, events, object hashes, and receipts.

Projection is driven from canonical domain events and checkpoints. If Neo4j is unavailable, canonical workflows continue, projection lag is recorded, and the projection can be rebuilt from events.

## 3. Context for Development

### Requirement Trace

| FR | Required Behavior | Spec Coverage |
|---|---|---|
| FR-CMF-10.03 | Maintain canonical business state in the primary data store while exposing Neo4j as a rebuildable relationship projection. | Projection outbox consumer, node/relationship schema, projection health, and command boundary. |
| FR-CMF-10.04 | Rebuild Neo4j projection from canonical events and never let it become the only truth for production decisions. | ProjectionCheckpoint, rebuild workflow, count validation, lag detection, unhealthy marking, and action-through-Command-Bus rule. |

### Pipeline Stage Trace

| Field | Value |
|---|---|
| Canonical Stage | 14 - Publishing, memory, and projection |
| Entry Object | domain event checkpoint |
| Exit Object | Neo4j projection event |
| Validation Contract | rebuild and lag validation |
| Required Receipt | projection receipt |

### Legacy Intelligence Mapping

- Product Brief Neo4j state retention is updated to the architecture boundary: graph as projection, not write model.
- Legacy relationship intelligence becomes projection mappings and fixtures.
- Active primitive families BUS, FBK, and SAF govern relationship visibility, feedback, and production safety.

## 4. Implementation Plan

1. Define `ProjectionCheckpoint`, `ProjectionEvent`, `ProjectionHealth`, `ProjectionLagReport`, `ProjectedNode`, `ProjectedRelationship`, and `ProjectionReceipt`.
2. Implement domain event outbox consumer for projection-eligible events.
3. Map nodes for Brand, Guest, Session, ExpressionMoment, Archetype, AssetDerivative, RenderMode, CompleteEditingSession, ProviderJob, EvaluationReceipt, ApprovalEvent, PublishingIntent, and MemoryEvent.
4. Map relationships with source event ID and projection batch ID.
5. Implement rebuild workflow from selected checkpoints.
6. Validate projected counts and relationship integrity against canonical event counts.
7. Mark projection unhealthy on conflicts and require rebuild.

## 5. Primary Output Schema

```python
from enum import Enum
from typing import Literal
from pydantic import BaseModel


class ProjectionHealthStatus(str, Enum):
    HEALTHY = "healthy"
    LAGGING = "lagging"
    UNAVAILABLE = "unavailable"
    UNHEALTHY_REBUILD_REQUIRED = "unhealthy_rebuild_required"


class ProjectionCheckpoint(BaseModel):
    schema_version: Literal["cmf.projection_checkpoint.v1"]
    checkpoint_id: str
    event_outbox_offset: int
    projected_event_count: int
    projection_version: str
    created_at: str


class ProjectedRelationship(BaseModel):
    relationship_id: str
    from_node_ref: str
    to_node_ref: str
    relationship_type: str
    source_event_id: str
    projection_batch_id: str


class ProjectionHealth(BaseModel):
    projection_name: Literal["neo4j_relationship_projection"]
    status: ProjectionHealthStatus
    last_checkpoint_id: str | None = None
    lag_event_count: int
    conflict_count: int
```

## 6. Commands, Events, Workflows, and Receipts

| Type | Names |
|---|---|
| Commands | `ProjectDomainEventCommand`, `CreateProjectionCheckpointCommand`, `RebuildNeo4jProjectionCommand`, `ValidateProjectionCountsCommand`, `MarkProjectionUnhealthyCommand`, `RetryProjectionLagCommand` |
| Events | `DomainEventProjected`, `ProjectionCheckpointCreated`, `Neo4jProjectionRebuilt`, `ProjectionCountsValidated`, `ProjectionMarkedUnhealthy`, `ProjectionLagRetryScheduled` |
| Workflow | `ProjectionRebuildWorkflow.stage14_rebuild_graph_projection` |
| Receipt | `ProjectionReceipt` with checkpoint, event range, node counts, relationship counts, lag, conflicts, rebuild result, and health status |

## 7. Backward Compatibility and Migration Fallback

Legacy graph or state-retention ideas are imported only as projection mapping references. If historical graph data cannot be rebuilt from current canonical events, it remains an archived reference and cannot drive production decisions.

## 8. CBAR Constraint Pass

| Tension | Resolution Demand | Downstream Proof |
|---|---|---|
| Rich graph query vs. production truth | Graph informs insight only; actions still use Command Bus and canonical state. | Tests reject direct graph-driven mutation. |
| Projection failure vs. workflow continuity | Canonical workflows continue while lag is tracked. | Failure taxonomy marks projection lag and retry. |
| Relationship intelligence vs. drift | Rebuild validates counts and relationships against events. | Unhealthy projection requires rebuild receipt. |

## 9. Tasks

- Add projection contracts and persistence.
- Implement outbox projection consumer.
- Add Neo4j node and relationship writers.
- Add projection checkpointing.
- Add rebuild workflow.
- Add lag and conflict health reporting.
- Add projection APIs and read queries.

## 10. Acceptance Criteria with Failure Examples

| AC | Pass Condition | Failure Example |
|---|---|---|
| AC1 | Domain events update Neo4j nodes and relationships. | Graph is edited manually. |
| AC2 | Neo4j outage does not stop canonical workflows; lag is recorded. | Provider/review workflow fails because graph is down. |
| AC3 | Rebuild from checkpoints reconstructs graph and validates counts. | Rebuild creates graph with unknown event gaps. |
| AC4 | Operator insight still acts through Command Bus and primary state. | Graph query directly approves or blocks an asset. |
| AC5 | Conflict with primary state marks projection unhealthy and requires rebuild. | Conflicting graph data remains marked healthy. |

## 11. Dependencies

- TS-CMF-001 command spine.
- TS-CMF-002 pipeline stage records.
- TS-CMF-054 Publishing Intent.
- TS-CMF-056 memory admission.
- TS-CMF-057 memory governance.

## 12. Testing Strategy


Unit tests:

- Unit tests for projection checkpoint and health schemas.
- Integration tests from outbox events to Neo4j projection writes.
- Outage tests proving canonical workflows continue.
- Rebuild tests from checkpoint and full event replay.
- Conflict tests proving unhealthy marking.
- Command-boundary tests preventing graph-driven mutation.

Integration tests:

- Workflow test from `domain event checkpoint` to `Neo4j projection event` through pipeline stage `14`.
- Command Bus test proving `projection receipt` is emitted, persisted, and linked to the workflow state.
- Source-spine test proving Product Brief, PRD, architecture, pipeline map, and Legacy Inventory assumptions are represented by fixtures, contracts, or receipts.

Eval and recovery tests:

- Acceptance-criteria fixture test covering the documented pass path and failure examples.
- Recovery or replay test proving idempotency, compensation, blocked-state handling, or rollback behavior from Section 13.

## 13. Observability, Recovery, and Rollback

- Metrics for projected events, projection lag, rebuild duration, node counts, relationship counts, conflicts, and failed writes.
- Logs include checkpoint ID, event range, projection batch ID, graph write count, and health status.
- Recovery retries lagging events or rebuilds from checkpoint.
- Rollback clears projection database and rebuilds from canonical events; canonical production state is untouched.

## Doctrine-Driven Test Harness Binding

This spec must be verified through TS-CMF-077 before implementation is considered complete. The test plan for this spec must identify the documented doctrine sources it depends on, the operational invariants those sources imply, the primitive or eval obligations that apply to its outputs, and the negative fixtures that prove forbidden shortcuts are blocked. Passing tests must emit or validate the required receipt chain, and any hard failure must map to an approval blocker when this spec touches review, rendering, publishing, memory, agents, adapters, or operator actions.

Minimum binding requirements:

- cite source doctrine or registry refs used by this spec;
- declare contract, workflow, receipt, and read-model invariants;
- include at least one negative or drift fixture for every forbidden shortcut named in the spec;
- prove required receipts are emitted, immutable, reconstructable, and linked to pipeline stage state;
- expose failed doctrine, primitive, or eval obligations as blocker-ready test output.

## 14. Spec Audit Receipt

| Field | Value |
|---|---|
| Tech Spec ID | TS-CMF-058 |
| Story | 10.3 |
| Requirement Trace | FR-CMF-10.03, FR-CMF-10.04 |
| Pipeline Trace | Stage 14, domain event checkpoint to Neo4j projection event |
| Legacy Inventory Referenced | Yes |
| CBAR Included | Yes |
| Forbidden Drift Check | No graph write model, no graph-only production truth, no projection blocking canonical workflows |
