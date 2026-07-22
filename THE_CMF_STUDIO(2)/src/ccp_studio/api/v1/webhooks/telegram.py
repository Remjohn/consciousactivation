"""Telegram webhook adapter for TS-CMF-007."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.surfaces import SurfaceActionEnvelope, SurfaceCommandResult
from ccp_studio.services.command_bus import create_in_memory_command_bus
from ccp_studio.services.surface_action_service import SurfaceActionService
from ccp_studio.services.telegram_auth_service import TelegramAuthService


class TelegramSurfaceActionRequest(BaseModel):
    init_data: str
    action: SurfaceActionEnvelope


router = APIRouter(prefix="/api/v1/webhooks/telegram", tags=["telegram"])
_telegram_auth = TelegramAuthService(bot_token="test-token")
_surface_action_service = SurfaceActionService(create_in_memory_command_bus())


def set_telegram_auth(service: TelegramAuthService) -> None:
    global _telegram_auth
    _telegram_auth = service


def get_telegram_auth() -> TelegramAuthService:
    return _telegram_auth


def set_surface_action_service(service: SurfaceActionService) -> None:
    global _surface_action_service
    _surface_action_service = service


def get_surface_action_service() -> SurfaceActionService:
    return _surface_action_service


@router.post("/surface-action", response_model=SurfaceCommandResult)
async def submit_telegram_surface_action(
    request: TelegramSurfaceActionRequest,
    auth: TelegramAuthService = Depends(get_telegram_auth),
    service: SurfaceActionService = Depends(get_surface_action_service),
) -> SurfaceCommandResult:
    auth.verify_init_data(request.init_data)
    return service.submit(request.action)
