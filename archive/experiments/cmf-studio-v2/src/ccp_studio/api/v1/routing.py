"""FastAPI adapter for TS-CMF-033 routing."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.routing import AssetRouteReceipt
from ccp_studio.services.routing_service import RoutingService


router = APIRouter(prefix="/api/v1/expression-moments", tags=["expression-moments"])
_routing_service: RoutingService | None = None


class RouteExpressionMomentRequest(BaseModel):
    actor_id: UUID
    requested_format: str | None = None


def set_routing_service(service: RoutingService) -> None:
    global _routing_service
    _routing_service = service


def get_routing_service() -> RoutingService:
    if _routing_service is None:
        raise RuntimeError("RoutingService must be configured by the application.")
    return _routing_service


@router.post("/brands/{brand_id}/moments/{expression_moment_id}/routes", response_model=AssetRouteReceipt)
def route_expression_moment(
    brand_id: UUID,
    organization_id: UUID,
    expression_moment_id: UUID,
    request: RouteExpressionMomentRequest,
    service: RoutingService = Depends(get_routing_service),
) -> AssetRouteReceipt:
    return service.route_expression_moment(
        organization_id=organization_id,
        brand_id=brand_id,
        expression_moment_id=expression_moment_id,
        requested_format=request.requested_format,
        actor_id=request.actor_id,
    )
