"""Research API adapter for TS-CMF-023."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.research import ResearchField
from ccp_studio.services.research_service import ResearchService


class CreateResearchFieldRequest(BaseModel):
    organization_id: UUID
    objective: str
    source_scope: list[str]
    created_by_actor_id: UUID
    guest_id: UUID | None = None


router = APIRouter(prefix="/api/v1/research", tags=["research"])
_research_service = ResearchService()


def set_research_service(service: ResearchService) -> None:
    global _research_service
    _research_service = service


def get_research_service() -> ResearchService:
    return _research_service


@router.post("/brands/{brand_id}/fields", response_model=ResearchField)
async def create_research_field(
    brand_id: UUID,
    request: CreateResearchFieldRequest,
    service: ResearchService = Depends(get_research_service),
) -> ResearchField:
    return service.create_field(
        organization_id=request.organization_id,
        brand_id=brand_id,
        objective=request.objective,
        source_scope=request.source_scope,
        created_by_actor_id=request.created_by_actor_id,
        guest_id=request.guest_id,
    )
