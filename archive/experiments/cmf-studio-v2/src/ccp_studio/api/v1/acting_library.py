"""Acting library API adapter for TS-CMF-019."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.acting_library import ActingLibraryVersion, ActingReference
from ccp_studio.repositories.brand_genesis_sessions import InMemoryBrandGenesisRepository
from ccp_studio.services.acting_library_service import ActingLibraryService


class GenerateActingGridRequest(BaseModel):
    organization_id: UUID
    brand_genesis_session_id: UUID
    source_artifact_ids: list[UUID]
    provider_name: str


router = APIRouter(prefix="/api/v1/acting-library", tags=["acting-library"])
_acting_library_service = ActingLibraryService(InMemoryBrandGenesisRepository())


def set_acting_library_service(service: ActingLibraryService) -> None:
    global _acting_library_service
    _acting_library_service = service


def get_acting_library_service() -> ActingLibraryService:
    return _acting_library_service


@router.post("/brands/{brand_id}/grid", response_model=ActingLibraryVersion)
async def generate_acting_grid(
    brand_id: UUID,
    request: GenerateActingGridRequest,
    service: ActingLibraryService = Depends(get_acting_library_service),
) -> ActingLibraryVersion:
    return service.generate_reference_grid(
        organization_id=request.organization_id,
        brand_id=brand_id,
        brand_genesis_session_id=request.brand_genesis_session_id,
        source_artifact_ids=request.source_artifact_ids,
        provider_name=request.provider_name,
    )


@router.post("/brands/{brand_id}/versions/{version_id}/lock", response_model=ActingLibraryVersion)
async def lock_acting_library(
    brand_id: UUID,
    version_id: UUID,
    organization_id: UUID,
    service: ActingLibraryService = Depends(get_acting_library_service),
) -> ActingLibraryVersion:
    return service.lock_library_version(
        organization_id=organization_id,
        brand_id=brand_id,
        acting_library_version_id=version_id,
    )


@router.get("/brands/{brand_id}/versions/{version_id}/references/{reference_id}", response_model=ActingReference)
async def get_selectable_acting_reference(
    brand_id: UUID,
    version_id: UUID,
    reference_id: UUID,
    organization_id: UUID,
    service: ActingLibraryService = Depends(get_acting_library_service),
) -> ActingReference:
    return service.assert_reference_selectable_for_scenespec(
        organization_id=organization_id,
        brand_id=brand_id,
        acting_library_version_id=version_id,
        acting_reference_id=reference_id,
    )
