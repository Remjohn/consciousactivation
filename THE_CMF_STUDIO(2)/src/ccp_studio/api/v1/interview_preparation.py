"""Interview preparation API adapter for TS-CMF-024."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.context import ContextCompilationReceipt
from ccp_studio.services.context_compilation_service import ContextCompilationService
from ccp_studio.services.research_service import ResearchService


class CompileContextArtifactsRequest(BaseModel):
    organization_id: UUID
    research_field_id: UUID
    evidence_ids: list[UUID]
    operator_id: UUID
    audience_scope: str
    compiler_actor_id: UUID
    guest_id: UUID | None = None
    guest_profile_hints: list[str] = []
    operator_notes: list[str] = []
    premise_statement: str | None = None


router = APIRouter(prefix="/api/v1/interviews/preparation", tags=["interview-preparation"])
_context_service = ContextCompilationService(research_service=ResearchService())


def set_context_compilation_service(service: ContextCompilationService) -> None:
    global _context_service
    _context_service = service


def get_context_compilation_service() -> ContextCompilationService:
    return _context_service


@router.post("/brands/{brand_id}/context-artifacts", response_model=ContextCompilationReceipt)
async def compile_context_artifacts(
    brand_id: UUID,
    request: CompileContextArtifactsRequest,
    service: ContextCompilationService = Depends(get_context_compilation_service),
) -> ContextCompilationReceipt:
    return service.compile_context_artifacts(
        organization_id=request.organization_id,
        brand_id=brand_id,
        research_field_id=request.research_field_id,
        evidence_ids=request.evidence_ids,
        operator_id=request.operator_id,
        audience_scope=request.audience_scope,
        compiler_actor_id=request.compiler_actor_id,
        guest_id=request.guest_id,
        guest_profile_hints=request.guest_profile_hints,
        operator_notes=request.operator_notes,
        premise_statement=request.premise_statement,
    )
