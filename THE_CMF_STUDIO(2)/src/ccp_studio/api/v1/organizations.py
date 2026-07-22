"""Organization API adapter for TS-CMF-004."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.workspace_lifecycle import WorkspaceInspectionSnapshot
from ccp_studio.services.workspace_service import WorkspaceService


class WorkspaceInspectionRequest(BaseModel):
    actor_id: UUID
    role_ids: list[str]
    organization_id: UUID
    brand_id: UUID


router = APIRouter(prefix="/api/v1/organizations", tags=["organizations"])
_workspace_service = WorkspaceService()


def set_workspace_service(service: WorkspaceService) -> None:
    global _workspace_service
    _workspace_service = service


def get_workspace_service() -> WorkspaceService:
    return _workspace_service


@router.post("/{organization_id}/brands/{brand_id}/inspect", response_model=WorkspaceInspectionSnapshot)
async def inspect_workspace(
    organization_id: UUID,
    brand_id: UUID,
    request: WorkspaceInspectionRequest,
    service: WorkspaceService = Depends(get_workspace_service),
) -> WorkspaceInspectionSnapshot:
    return service.inspect_workspace(
        actor_id=request.actor_id,
        role_ids=request.role_ids,
        organization_id=organization_id,
        brand_id=brand_id,
    )
