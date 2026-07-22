"""Brand Genesis API adapter for TS-CMF-018."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.brand_genesis import (
    BrandGenesisSession,
    BrandGenesisWorkflowRun,
    BrandSourceInput,
    NegativeSpaceInput,
    VisualConstitutionInput,
    VoiceDnaReference,
)
from ccp_studio.repositories.consent_record_versions import InMemoryConsentRepository
from ccp_studio.repositories.source_artifacts import InMemorySourceArtifactRepository
from ccp_studio.services.brand_genesis_service import BrandGenesisService


class CreateBrandGenesisSessionRequest(BaseModel):
    organization_id: UUID
    actor_id: UUID
    brand_notes: str
    audience_summary: str
    offer_summary: str
    forbidden_tone: list[str]
    visual_preferences: list[str]
    voice_dna_references: list[VoiceDnaReference]
    source_inputs: list[BrandSourceInput]
    visual_constitution_input: VisualConstitutionInput | None = None
    negative_space_input: NegativeSpaceInput | None = None


class StartBrandGenesisWorkflowRequest(BaseModel):
    organization_id: UUID
    actor_id: UUID


router = APIRouter(prefix="/api/v1/brand-genesis", tags=["brand-genesis"])
_brand_genesis_service = BrandGenesisService(InMemoryConsentRepository(), InMemorySourceArtifactRepository())


def set_brand_genesis_service(service: BrandGenesisService) -> None:
    global _brand_genesis_service
    _brand_genesis_service = service


def get_brand_genesis_service() -> BrandGenesisService:
    return _brand_genesis_service


@router.post("/brands/{brand_id}/sessions", response_model=BrandGenesisSession)
async def create_brand_genesis_session(
    brand_id: UUID,
    request: CreateBrandGenesisSessionRequest,
    service: BrandGenesisService = Depends(get_brand_genesis_service),
) -> BrandGenesisSession:
    return service.create_session(
        organization_id=request.organization_id,
        brand_id=brand_id,
        brand_notes=request.brand_notes,
        audience_summary=request.audience_summary,
        offer_summary=request.offer_summary,
        forbidden_tone=request.forbidden_tone,
        visual_preferences=request.visual_preferences,
        voice_dna_references=request.voice_dna_references,
        source_inputs=request.source_inputs,
        visual_constitution_input=request.visual_constitution_input,
        negative_space_input=request.negative_space_input,
        created_by_actor_id=request.actor_id,
    )


@router.post("/brands/{brand_id}/sessions/{session_id}/start", response_model=BrandGenesisWorkflowRun)
async def start_brand_genesis_workflow(
    brand_id: UUID,
    session_id: UUID,
    request: StartBrandGenesisWorkflowRequest,
    service: BrandGenesisService = Depends(get_brand_genesis_service),
) -> BrandGenesisWorkflowRun:
    return service.start_workflow(
        organization_id=request.organization_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        actor_id=request.actor_id,
    )


@router.get("/brands/{brand_id}/sessions/{session_id}", response_model=BrandGenesisSession)
async def get_brand_genesis_session(
    brand_id: UUID,
    session_id: UUID,
    organization_id: UUID,
    service: BrandGenesisService = Depends(get_brand_genesis_service),
) -> BrandGenesisSession:
    return service.get_session(
        organization_id=organization_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
    )
