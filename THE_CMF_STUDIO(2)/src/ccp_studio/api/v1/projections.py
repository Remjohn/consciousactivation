"""FastAPI adapter for TS-CMF-058 projection operations."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.projection import GraphInsightActionDecision, ProjectionHealth, ProjectionReceipt
from ccp_studio.services.projection_service import ProjectionService


router = APIRouter(prefix="/api/v1/projections", tags=["projections"])
_projection_service: ProjectionService | None = None


class ProjectDomainEventRequest(BaseModel):
    domain_event: dict[str, Any]
    event_outbox_offset: int
    idempotency_key: str | None = None


class RebuildProjectionRequest(BaseModel):
    domain_events: list[dict[str, Any]] = Field(default_factory=list)
    from_checkpoint_id: UUID | None = None
    idempotency_key: str | None = None


class ProjectionCountValidationRequest(BaseModel):
    expected_event_count: int


class MarkUnhealthyRequest(BaseModel):
    reason: str
    conflict_count: int = 1


class GraphInsightActionRequest(BaseModel):
    graph_query_ref: str
    requested_action: str
    required_command_type: str
    direct_graph_mutation_requested: bool = False


def set_projection_service(service: ProjectionService) -> None:
    global _projection_service
    _projection_service = service


def get_projection_service() -> ProjectionService:
    if _projection_service is None:
        raise RuntimeError("ProjectionService must be configured by the application.")
    return _projection_service


@router.post("/events", response_model=ProjectionReceipt)
def project_domain_event(
    request: ProjectDomainEventRequest,
    service: ProjectionService = Depends(get_projection_service),
) -> ProjectionReceipt:
    return service.project_domain_event(**request.model_dump())


@router.post("/rebuild", response_model=ProjectionReceipt)
def rebuild_projection(
    request: RebuildProjectionRequest,
    service: ProjectionService = Depends(get_projection_service),
) -> ProjectionReceipt:
    return service.rebuild_neo4j_projection(**request.model_dump())


@router.post("/validate-counts", response_model=ProjectionHealth)
def validate_projection_counts(
    request: ProjectionCountValidationRequest,
    service: ProjectionService = Depends(get_projection_service),
) -> ProjectionHealth:
    return service.validate_projection_counts(**request.model_dump())


@router.post("/mark-unhealthy", response_model=ProjectionReceipt)
def mark_projection_unhealthy(
    request: MarkUnhealthyRequest,
    service: ProjectionService = Depends(get_projection_service),
) -> ProjectionReceipt:
    return service.mark_projection_unhealthy(**request.model_dump())


@router.post("/graph-insight-action", response_model=GraphInsightActionDecision)
def graph_insight_action_boundary(
    request: GraphInsightActionRequest,
    service: ProjectionService = Depends(get_projection_service),
) -> GraphInsightActionDecision:
    return service.graph_insight_action_boundary(**request.model_dump())
