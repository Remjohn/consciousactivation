---
tech_spec_id: "TS-CMF-142"
title: "Live Operations Event Stream and Read Model Sync"
story_id: "15.7"
story_title: "Keep the Operator Cockpit Live and Trustworthy"
epic_id: 15
epic_title: "Operator Operations Runtime and Agentic Control"
status: "ready-for-development"
created_at: "2026-06-26"
fr_ids:
  - "FR-CMF-09"
  - "FR-CMF-10"
pipeline_stage: "event projection, operations read models, command status, and UI synchronization"
entry_object: "DomainEvent, UiActionReceipt, StageArtifactReceipt"
exit_object: "OperationsEventFrame, ReadModelSyncReceipt, OperatorLiveState"
validation_contract: "event ordering, idempotency, stale state detection, scope filtering, receipt-linked UI refresh"
required_receipt: "ReadModelSyncReceipt"
runtime_target: "FastAPI SSE/WebSocket or polling / projection service / React state sync"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# TS-CMF-142: Live Operations Event Stream and Read Model Sync

## 1. Files Read

| Path | Why It Matters |
|---|---|
| `THE CMF STUDIO/docs/architecture.md` | Defines receipts, projections, operations boards, and rebuildable Neo4j/read-model philosophy. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-059-operations-board.md` | Operations board dependency. |
| `THE CMF STUDIO/docs/tech-specs/TS-CMF-060-workflow-recovery-actions.md` | Recovery actions dependency. |
| `THE CMF STUDIO/src/ccp_studio/services/operations_board_service.py` | Existing operations board service and command handler owner. |
| `THE CMF STUDIO/src/ccp_studio/services/projection_service.py` | Existing projection service owner. |
| `THE CMF STUDIO/src/ccp_studio/contracts/operator_ui.py` | Existing UI state/receipt contracts. |
| `THE CMF STUDIO/operator-web/src/App.jsx` | Current frontend has static state and needs live sync. |

## 2. Overview

The operator cockpit should feel alive because the factory is alive: agents propose work, render jobs start and finish, evals fail, revisions enter repair, Telegram decisions arrive, and provider workers report status. The current React app is static. This spec defines the event stream and read-model synchronization layer that turns it into a real operations room.

The event stream does not replace canonical persistence. It transports receipt-linked updates to the browser and Telegram surfaces. Every event must be scoped, ordered, idempotent, and linked to source receipts. The UI can update optimistically while a command is pending, but live state must be reconciled against read-model snapshots and object versions.

CMF can implement this with Server-Sent Events first, WebSocket later, or scoped polling where infrastructure is simpler. The important requirement is not the transport; it is that the operator sees current command status, blockers, and queue changes without trusting local React state.

## 3. Context for Development

### Architecture Traceability

| DEP-ID | Dependency | Required Behavior |
|---|---|---|
| DEP-CMF-142-001 | `OperationsEventFrame` | Transport wrapper for domain/read-model events. |
| DEP-CMF-142-002 | `ReadModelSyncReceipt` | Proof that UI read model was refreshed from receipt-backed state. |
| DEP-CMF-142-003 | `OperatorLiveState` | Aggregated live state for control tower. |
| DEP-CMF-142-004 | `EventCursor` | Ordered resume cursor. |
| DEP-CMF-142-005 | `ScopeFilter` | Organization, brand, guest, object, and route filtering. |

### Existing Backend Integration

| Backend Owner | Required Extension |
|---|---|
| `services/operations_board_service.py` | Publish operations event frames and live state. |
| `services/projection_service.py` | Update and rebuild read models from receipts/events. |
| `api/v1/operator_ui.py` | Add live event endpoint or polling state endpoint. |
| `operator-web` | Add live sync client and object-version reconciliation. |

### ADR-05 Primitive Implementation

Primitive/eval failures should stream as blocker updates, not hidden logs. The UI must receive changes when eval receipts create or clear primitive blockers.

### CBAR Mandate Enforcement

| CBAR Mandate | Implementation Rule |
|---|---|
| Phase3-M04 Telemetry Surfacing | Events expose command, agent, workflow, render, eval, revision, and approval changes. |
| Phase5-M01 Verifiable Artifact | Every event frame links to receipt id or source event id. |
| Phase1-M05 Deterministic Override | Stale cursor forces snapshot refresh. |

## 4. PRD and FR-CMF Requirement Trace

| Requirement | Implementation Meaning |
|---|---|
| FR-CMF-09 | Review and approval states update as receipts arrive. |
| FR-CMF-10 | Operations board, recovery, memory, and projections remain live and rebuildable. |

## 5. Canonical Pipeline Stage Trace

The stream covers all stages but especially long-running transitions: provider jobs, renders, evals, revisions, approvals, publishing intents, and recovery actions.

## 6. Greenfield Integration and Legacy Migration Context

Legacy operations dashboards may inform event categories, but production event schema is CMF-native and receipt-linked.

## 7. Architecture Component Map

| Component | Owner | Responsibility |
|---|---|---|
| `EventFrameBuilder` | Backend | Convert domain receipts/events into scoped frames. |
| `OperationsEventEndpoint` | API | SSE/WebSocket/poll endpoint. |
| `ReadModelSyncService` | Projection | Refresh read model and issue sync receipt. |
| `LiveStateClient` | Frontend | Subscribe, reconcile, refetch stale snapshots. |
| `CommandStatusPanel` | Frontend | Display pending and terminal command state. |

## 8. Implementation Plan

1. Add `OperationsEventFrame`, `EventCursor`, `OperatorLiveState`, and `ReadModelSyncReceipt` contracts.
2. Add `GET /api/v1/operator-ui/events` with brand workspace, guest, cursor, and route query parameters.
3. Implement SSE first unless deployment blocks it; polling fallback is allowed.
4. Emit frames for command accepted/rejected/failed/succeeded, agent action/proposal, provider job started/finished/failed, render output ready, eval receipt created, approval blocker changed, revision state changed, Telegram action received, and publishing intent changed.
5. Add frontend live sync client.
6. Add snapshot refresh on cursor gap, schema version mismatch, auth change, or scope change.
7. Add visual state for connected, reconnecting, stale, fixture, and failed.

## 9. Primary Pydantic Output Schema

```python
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field

class EventCursor(BaseModel):
    stream_id: str
    offset: int = Field(ge=0)
    issued_at: datetime

class OperationsEventFrame(BaseModel):
    schema_version: Literal["cmf.operations_event_frame.v1"] = "cmf.operations_event_frame.v1"
    frame_id: UUID
    cursor: EventCursor
    event_type: str
    brand_workspace_id: UUID
    guest_id: UUID | None = None
    active_object_type: str | None = None
    active_object_id: UUID | None = None
    receipt_id: UUID | None = None
    payload: dict = Field(default_factory=dict)
    created_at: datetime

class ReadModelSyncReceipt(BaseModel):
    schema_version: Literal["cmf.read_model_sync_receipt.v1"] = "cmf.read_model_sync_receipt.v1"
    receipt_id: UUID
    read_model_type: str
    read_model_ref: str
    source_event_frame_ids: list[UUID] = Field(default_factory=list)
    object_version: str
    sync_status: Literal["current", "stale", "partial", "failed"]
    synced_at: datetime
```

## 10. Commands, Events, Workflows, and Receipts

| Object | Requirement |
|---|---|
| `OperationsEventFrame` | Transport event to surfaces. |
| `ReadModelSyncReceipt` | Proves snapshot refresh. |
| `operator.live_state.synced` | Event after UI sync. |
| `operator.live_state.stale` | Event when cursor gap or version mismatch occurs. |

## 11. DSPy Programs, JIT Skills, or Deterministic Services

No intelligence execution happens in the event stream. It only reports state and receipts.

## 12. Provider, Renderer, Projection, or Worker Boundaries

Providers/workers publish status to CMF backend, which converts them into event frames. UI does not subscribe to external provider streams.

## 13. CBAR Constraint Pass

| Constraint | Pass Condition |
|---|---|
| Tension | Operators need live feedback; local state can lie. |
| Failure Scenario | UI still shows "rendering" after eval hard-failed. |
| Resolution Demand | Receipt-linked event updates review/render lanes. |
| Downstream Proof | Read-model sync receipt records current object version. |

## 14. Acceptance Criteria with Failure Examples

| AC | Acceptance Criteria | Failure Example | CBAR |
|---|---|---|---|
| AC142-01 | UI receives command terminal state without manual refresh. | Command stays pending after backend succeeded. | Phase3-M04 |
| AC142-02 | Cursor gap triggers snapshot refresh. | UI applies out-of-order event as current truth. | Phase1-M05 |
| AC142-03 | Events are scoped by brand/guest/object. | Adele event appears in Claude workspace. | Phase4-M04 |
| AC142-04 | Every event links to receipt or source event where applicable. | Render-ready event has no render receipt id. | Phase5-M01 |
| AC142-05 | Primitive/eval blocker changes update review UI. | Approval button remains enabled after eval hard fail. | Phase4-M04 |

## 15. Dependencies

| Dependency | Required Before Build |
|---|---|
| TS-CMF-001 | Receipts/events command spine. |
| TS-CMF-059 | Operations board. |
| TS-CMF-060 | Recovery actions. |
| TS-CMF-136 | Frontend API client. |
| TS-CMF-137 | Backend composition root. |

## 16. Testing Strategy

| Test Type | Required Tests |
|---|---|
| Unit | Event frames validate scope and receipt links. |
| Unit | Cursor gap detection works. |
| Integration | Command receipt emits event and UI refreshes read model. |
| Negative | Cross-workspace events are filtered. |
| E2E | Render/eval/revision state changes appear live in UI. |

## 17. Observability, Recovery, and Rollback

1. Track event lag and dropped connections.
2. Provide polling fallback if SSE/WebSocket unavailable.
3. Store last cursor per session.
4. Roll back by disabling live stream and using explicit refresh, not local mocks.

## 18. Spec Audit Receipt

| Field | Value |
|---|---|
| Spec id | TS-CMF-142 |
| Protocol | CMF/ERA3 18-section spec |
| Live state source | Receipt-linked events/read models |
| Cross-scope leakage | Blocked |
| Status | ready-for-development |
