"""FastAPI adapter for TS-CMF-031 extraction candidates."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.extraction import ExtractionReceipt
from ccp_studio.services.extraction_service import ExtractionService


router = APIRouter(prefix="/api/v1/expression-moments", tags=["expression-moments"])
_extraction_service: ExtractionService | None = None


class RunExtractionRequest(BaseModel):
    actor_id: UUID
    skill_key: str | None = None


def set_extraction_service(service: ExtractionService) -> None:
    global _extraction_service
    _extraction_service = service


def get_extraction_service() -> ExtractionService:
    if _extraction_service is None:
        raise RuntimeError("ExtractionService must be configured by the application.")
    return _extraction_service


@router.post("/brands/{brand_id}/sessions/{expression_session_id}/candidates", response_model=ExtractionReceipt)
def run_expression_candidate_extraction(
    brand_id: UUID,
    organization_id: UUID,
    expression_session_id: UUID,
    request: RunExtractionRequest,
    service: ExtractionService = Depends(get_extraction_service),
) -> ExtractionReceipt:
    return service.run_extraction(
        organization_id=organization_id,
        brand_id=brand_id,
        expression_session_id=expression_session_id,
        skill_key=request.skill_key,
        actor_id=request.actor_id,
    )
