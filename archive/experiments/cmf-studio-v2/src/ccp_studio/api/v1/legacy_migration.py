"""Legacy migration API adapter for TS-CMF-013."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.legacy import LegacyDisposition, MigrationLedgerEntry
from ccp_studio.services.migration_service import MigrationService


class ProposeLegacyAssetRequest(BaseModel):
    source_path: str
    legacy_type: str
    registry_family: str | None = None
    canonicality_confidence: float
    source_owner: str
    runtime_language: str | None = None
    valuable_mechanics: list[str]
    known_defects: list[str] = []
    content: str
    disposition: LegacyDisposition
    actor_id: UUID | None = None


router = APIRouter(prefix="/api/v1/legacy-migration", tags=["legacy-migration"])
_migration_service = MigrationService()


def set_migration_service(service: MigrationService) -> None:
    global _migration_service
    _migration_service = service


def get_migration_service() -> MigrationService:
    return _migration_service


@router.post("/assets", response_model=MigrationLedgerEntry)
async def propose_legacy_asset(
    request: ProposeLegacyAssetRequest,
    service: MigrationService = Depends(get_migration_service),
) -> MigrationLedgerEntry:
    return service.propose_asset(
        source_path=request.source_path,
        legacy_type=request.legacy_type,
        registry_family=request.registry_family,
        canonicality_confidence=request.canonicality_confidence,
        source_owner=request.source_owner,
        runtime_language=request.runtime_language,
        valuable_mechanics=request.valuable_mechanics,
        known_defects=request.known_defects,
        content=request.content,
        disposition=request.disposition,
        actor_id=request.actor_id,
    )
