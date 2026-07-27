"""Brand API helpers for TS-CMF-004."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.workspace_lifecycle import ActiveBrandContext
from ccp_studio.services.workspace_service import WorkspaceService


class SwitchActiveBrandRequest(BaseModel):
    actor_id: UUID
    role_ids: list[str]
    organization_id: UUID
    brand_id: UUID
    source_surface: str


router = APIRouter(prefix="/api/v1/brands", tags=["brands"])
_workspace_service = WorkspaceService()


def set_workspace_service(service: WorkspaceService) -> None:
    global _workspace_service
    _workspace_service = service


def get_workspace_service() -> WorkspaceService:
    return _workspace_service


@router.post("/{brand_id}/active-context", response_model=ActiveBrandContext)
async def switch_active_brand(
    brand_id: UUID,
    request: SwitchActiveBrandRequest,
    service: WorkspaceService = Depends(get_workspace_service),
) -> ActiveBrandContext:
    return service.switch_active_brand_context(
        actor_id=request.actor_id,
        role_ids=request.role_ids,
        organization_id=request.organization_id,
        brand_id=brand_id,
        source_surface=request.source_surface,
    )
