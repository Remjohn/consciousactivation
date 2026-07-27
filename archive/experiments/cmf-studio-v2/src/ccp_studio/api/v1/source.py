"""Source ingestion API adapter for TS-CMF-009."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.source import RecordingConfiguration
from ccp_studio.services.source_ingestion import SourceIngestionService


class RecordingConfigurationRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    session_id: UUID
    expected_master_source: str
    backup_route: str
    platform_source: str | None = None
    upload_method: str
    file_safety_expectations: list[str]
    quality_requirements: list[str]


router = APIRouter(prefix="/api/v1/source", tags=["source"])
_source_ingestion = SourceIngestionService()


def set_source_ingestion_service(service: SourceIngestionService) -> None:
    global _source_ingestion
    _source_ingestion = service


def get_source_ingestion_service() -> SourceIngestionService:
    return _source_ingestion


@router.post("/recording-configurations", response_model=RecordingConfiguration)
async def submit_recording_configuration(
    request: RecordingConfigurationRequest,
    service: SourceIngestionService = Depends(get_source_ingestion_service),
) -> RecordingConfiguration:
    return service.submit_recording_configuration(
        organization_id=request.organization_id,
        brand_id=request.brand_id,
        session_id=request.session_id,
        expected_master_source=request.expected_master_source,
        backup_route=request.backup_route,
        platform_source=request.platform_source,
        upload_method=request.upload_method,
        file_safety_expectations=request.file_safety_expectations,
        quality_requirements=request.quality_requirements,
    )
