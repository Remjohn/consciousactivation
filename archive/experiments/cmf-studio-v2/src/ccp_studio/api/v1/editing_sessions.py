"""FastAPI adapter for TS-CMF-036 Complete Editing Sessions."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.complete_editing_session import CompleteEditingSession, CompleteEditingSessionReadModel
from ccp_studio.services.complete_editing_session_service import CompleteEditingSessionService


router = APIRouter(prefix="/api/v1/editing-sessions", tags=["editing-sessions"])
_editing_session_service: CompleteEditingSessionService | None = None


class CreateCompleteEditingSessionRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    source_expression_moment_id: UUID
    asset_route_receipt_id: UUID
    asset_package_item_id: UUID | None = None
    brand_context_version_id: UUID
    actor_id: UUID


def set_editing_session_service(service: CompleteEditingSessionService) -> None:
    global _editing_session_service
    _editing_session_service = service


def get_editing_session_service() -> CompleteEditingSessionService:
    if _editing_session_service is None:
        raise RuntimeError("CompleteEditingSessionService must be configured by the application.")
    return _editing_session_service


@router.post("", response_model=CompleteEditingSession)
def create_complete_editing_session(
    request: CreateCompleteEditingSessionRequest,
    service: CompleteEditingSessionService = Depends(get_editing_session_service),
) -> CompleteEditingSession:
    return service.create_session(
        organization_id=request.organization_id,
        brand_id=request.brand_id,
        source_expression_moment_id=request.source_expression_moment_id,
        asset_route_receipt_id=request.asset_route_receipt_id,
        asset_package_item_id=request.asset_package_item_id,
        brand_context_version_id=request.brand_context_version_id,
        actor_id=request.actor_id,
    )


@router.get("/{complete_editing_session_id}", response_model=CompleteEditingSessionReadModel)
def get_complete_editing_session(
    complete_editing_session_id: UUID,
    service: CompleteEditingSessionService = Depends(get_editing_session_service),
) -> CompleteEditingSessionReadModel:
    return service.read_model(complete_editing_session_id)
