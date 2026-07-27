"""Surface action API adapter for TS-CMF-007."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from ccp_studio.contracts.surfaces import SurfaceActionEnvelope, SurfaceCommandResult
from ccp_studio.services.command_bus import create_in_memory_command_bus
from ccp_studio.services.surface_action_service import SurfaceActionService


router = APIRouter(prefix="/api/v1/surface-actions", tags=["surface-actions"])
_surface_action_service = SurfaceActionService(create_in_memory_command_bus())


def set_surface_action_service(service: SurfaceActionService) -> None:
    global _surface_action_service
    _surface_action_service = service


def get_surface_action_service() -> SurfaceActionService:
    return _surface_action_service


@router.post("", response_model=SurfaceCommandResult)
async def submit_surface_action(
    action: SurfaceActionEnvelope,
    service: SurfaceActionService = Depends(get_surface_action_service),
) -> SurfaceCommandResult:
    return service.submit(action)
