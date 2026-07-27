"""Neo4j relationship projection contracts for TS-CMF-058."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class ProjectionHealthStatus(str, Enum):
    healthy = "healthy"
    lagging = "lagging"
    unavailable = "unavailable"
    unhealthy_rebuild_required = "unhealthy_rebuild_required"


class ProjectedNode(BaseModel):
    schema_version: Literal["cmf.projected_node.v1"] = "cmf.projected_node.v1"
    node_ref: str = Field(min_length=1)
    node_type: str = Field(min_length=1)
    source_event_id: UUID
    properties: dict[str, Any] = Field(default_factory=dict)


class ProjectedRelationship(BaseModel):
    schema_version: Literal["cmf.projected_relationship.v1"] = "cmf.projected_relationship.v1"
    relationship_id: UUID
    from_node_ref: str = Field(min_length=1)
    to_node_ref: str = Field(min_length=1)
    relationship_type: str = Field(min_length=1)
    source_event_id: UUID
    projection_batch_id: UUID
    properties: dict[str, Any] = Field(default_factory=dict)


class ProjectionCheckpoint(BaseModel):
    schema_version: Literal["cmf.projection_checkpoint.v1"]
    checkpoint_id: UUID
    event_outbox_offset: int = Field(ge=0)
    projected_event_count: int = Field(ge=0)
    projection_version: str = Field(min_length=1)
    created_at: datetime


class ProjectionEvent(BaseModel):
    schema_version: Literal["cmf.projection_event.v1"]
    projection_event_id: UUID
    source_event_id: UUID
    event_outbox_offset: int = Field(ge=0)
    projection_batch_id: UUID
    node_count: int = Field(ge=0)
    relationship_count: int = Field(ge=0)
    checkpoint_id: UUID | None = None
    projected_at: datetime


class ProjectionLagReport(BaseModel):
    schema_version: Literal["cmf.projection_lag_report.v1"]
    lag_report_id: UUID
    expected_event_count: int = Field(ge=0)
    projected_event_count: int = Field(ge=0)
    lag_event_count: int = Field(ge=0)
    status: ProjectionHealthStatus
    created_at: datetime


class ProjectionHealth(BaseModel):
    schema_version: Literal["cmf.projection_health.v1"]
    projection_name: Literal["neo4j_relationship_projection"] = "neo4j_relationship_projection"
    status: ProjectionHealthStatus
    last_checkpoint_id: UUID | None = None
    lag_event_count: int = Field(ge=0)
    conflict_count: int = Field(ge=0)
    message: str = Field(min_length=1)
    checked_at: datetime


class GraphInsightActionDecision(BaseModel):
    schema_version: Literal["cmf.graph_insight_action_decision.v1"]
    graph_query_ref: str = Field(min_length=1)
    requested_action: str = Field(min_length=1)
    direct_graph_mutation_allowed: bool
    required_command_type: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class ProjectionReceipt(BaseModel):
    schema_version: Literal["cmf.projection_receipt.v1"]
    projection_receipt_id: UUID
    checkpoint_id: UUID | None = None
    event_range_start: int = Field(ge=0)
    event_range_end: int = Field(ge=0)
    node_count: int = Field(ge=0)
    relationship_count: int = Field(ge=0)
    lag_event_count: int = Field(ge=0)
    conflict_count: int = Field(ge=0)
    rebuild_result: str = Field(min_length=1)
    health_status: ProjectionHealthStatus
    receipt_hash: str = Field(min_length=1)
    written_at: datetime


class ProjectionDomainEvent(BaseModel):
    schema_version: Literal["cmf.projection_domain_event.v1"]
    projection_domain_event_id: UUID
    event_type: str = Field(min_length=1)
    checkpoint_id: UUID | None = None
    projection_event_id: UUID | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


def projection_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_projection_checkpoint(
    *,
    event_outbox_offset: int,
    projected_event_count: int,
    projection_version: str,
) -> ProjectionCheckpoint:
    return ProjectionCheckpoint(
        schema_version="cmf.projection_checkpoint.v1",
        checkpoint_id=uuid4(),
        event_outbox_offset=event_outbox_offset,
        projected_event_count=projected_event_count,
        projection_version=projection_version,
        created_at=utc_now(),
    )


def new_projection_receipt(
    *,
    checkpoint_id: UUID | None,
    event_range_start: int,
    event_range_end: int,
    node_count: int,
    relationship_count: int,
    lag_event_count: int,
    conflict_count: int,
    rebuild_result: str,
    health_status: ProjectionHealthStatus,
) -> ProjectionReceipt:
    payload = {
        "checkpoint_id": checkpoint_id,
        "event_range_start": event_range_start,
        "event_range_end": event_range_end,
        "node_count": node_count,
        "relationship_count": relationship_count,
        "lag_event_count": lag_event_count,
        "conflict_count": conflict_count,
        "rebuild_result": rebuild_result,
        "health_status": health_status.value,
    }
    return ProjectionReceipt(
        schema_version="cmf.projection_receipt.v1",
        projection_receipt_id=uuid4(),
        checkpoint_id=checkpoint_id,
        event_range_start=event_range_start,
        event_range_end=event_range_end,
        node_count=node_count,
        relationship_count=relationship_count,
        lag_event_count=lag_event_count,
        conflict_count=conflict_count,
        rebuild_result=rebuild_result,
        health_status=health_status,
        receipt_hash=projection_hash(payload),
        written_at=utc_now(),
    )
