"""Registry API adapter for TS-CMF-014."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.registry import RegistryEntry, RegistryFamily
from ccp_studio.repositories.migration_ledger_entries import InMemoryMigrationLedgerRepository
from ccp_studio.services.registry_service import RegistryService


class ConvertRegistryRequest(BaseModel):
    migration_ledger_entry_id: UUID
    registry_family: RegistryFamily
    payload: dict
    reviewer_actor_id: UUID


router = APIRouter(prefix="/api/v1/registries", tags=["registries"])
_registry_service = RegistryService(InMemoryMigrationLedgerRepository())


def set_registry_service(service: RegistryService) -> None:
    global _registry_service
    _registry_service = service


def get_registry_service() -> RegistryService:
    return _registry_service


@router.post("/convert", response_model=RegistryEntry)
async def convert_registry(
    request: ConvertRegistryRequest,
    service: RegistryService = Depends(get_registry_service),
) -> RegistryEntry:
    return service.convert_legacy_asset_to_registry(
        migration_ledger_entry_id=request.migration_ledger_entry_id,
        registry_family=request.registry_family,
        payload=request.payload,
        reviewer_actor_id=request.reviewer_actor_id,
    )
