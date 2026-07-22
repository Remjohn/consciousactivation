"""FastAPI command spine route."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from ccp_studio.contracts.commands import CommandEnvelope, CommandResult
from ccp_studio.services.command_bus import CommandBus, create_in_memory_command_bus

router = APIRouter(prefix="/api/v1", tags=["commands"])

_command_bus = create_in_memory_command_bus()


def set_command_bus(bus: CommandBus) -> None:
    global _command_bus
    _command_bus = bus


def get_command_bus() -> CommandBus:
    return _command_bus


@router.post("/commands", response_model=CommandResult)
async def submit_command(
    envelope: CommandEnvelope,
    command_bus: CommandBus = Depends(get_command_bus),
) -> CommandResult:
    return command_bus.submit(envelope)

