from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel


class NodeStatus(BaseModel):
    node_id: str
    state: str  # NodeState value: BLOCKED|READY|DISPATCHED|RUNNING|SUCCEEDED|FAILED|CANCELLED|INVALIDATED|QUARANTINED
    attempt_count: int
    dispatch_ordinal: int | None
    output_ref: dict[str, Any] | None
    failure: dict[str, Any] | None


class RunStatus(BaseModel):
    run_id: str
    workflow_id: str
    state: str  # RunState value
    revision: int
    cancel_requested: bool
    current_checkpoint_id: str | None
    nodes: list[NodeStatus]


class RunStatusEnvelope(BaseModel):
    retrieved_at_utc: str  # this API layer's observation timestamp — not from the domain
    run: RunStatus


class RunEventItem(BaseModel):
    sequence: int
    event_type: str
    aggregate_id: str
    payload: dict[str, Any]
    event_sha256: str


class RunEventsResponse(BaseModel):
    run_id: str
    event_count: int
    event_stream_sha256: str
    events: list[RunEventItem]
    current_state: RunStatus
    historical_events_rewritten: bool


# --- WebSocket message envelope shapes (sent as plain JSON, documented here for the frontend) ---


class WSSnapshotMessage(BaseModel):
    type: Literal["snapshot"] = "snapshot"
    retrieved_at_utc: str
    run: RunStatus


class WSHistoryMessage(BaseModel):
    type: Literal["history"] = "history"
    retrieved_at_utc: str
    event_count: int
    event_stream_sha256: str
    events: list[RunEventItem]


class WSNodeStateChangedMessage(BaseModel):
    type: Literal["node_state_changed"] = "node_state_changed"
    retrieved_at_utc: str
    run_id: str
    node: NodeStatus


class WSRunStateChangedMessage(BaseModel):
    type: Literal["run_state_changed"] = "run_state_changed"
    retrieved_at_utc: str
    run_id: str
    workflow_id: str
    state: str
    revision: int
    cancel_requested: bool
    current_checkpoint_id: str | None


class WSRunTerminalMessage(BaseModel):
    type: Literal["run_terminal"] = "run_terminal"
    retrieved_at_utc: str
    run: RunStatus