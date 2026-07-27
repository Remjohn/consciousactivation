"""Matrix of Edging API adapter for TS-CMF-025."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.matrix import MatrixOfEdgingBrief, MatrixReceipt
from ccp_studio.services.context_compilation_service import ContextCompilationService
from ccp_studio.services.matrix_service import MatrixService
from ccp_studio.services.research_service import ResearchService


class CompileMatrixBriefRequest(BaseModel):
    organization_id: UUID
    guest_dossier_id: UUID
    audience_reality_brief_id: UUID
    context_premise_id: UUID
    trigger_map_id: UUID | None = None
    compiled_by_actor_id: UUID
    primitive_refs: list[str] | None = None


router = APIRouter(prefix="/api/v1/interviews/preparation", tags=["matrix"])
_matrix_service = MatrixService(
    context_service=ContextCompilationService(research_service=ResearchService())
)


def set_matrix_service(service: MatrixService) -> None:
    global _matrix_service
    _matrix_service = service


def get_matrix_service() -> MatrixService:
    return _matrix_service


@router.post("/brands/{brand_id}/matrix", response_model=MatrixOfEdgingBrief)
async def compile_matrix_brief(
    brand_id: UUID,
    request: CompileMatrixBriefRequest,
    service: MatrixService = Depends(get_matrix_service),
) -> MatrixOfEdgingBrief:
    return service.compile_matrix_brief(
        organization_id=request.organization_id,
        brand_id=brand_id,
        guest_dossier_id=request.guest_dossier_id,
        audience_reality_brief_id=request.audience_reality_brief_id,
        context_premise_id=request.context_premise_id,
        trigger_map_id=request.trigger_map_id,
        primitive_refs=request.primitive_refs,
        compiled_by_actor_id=request.compiled_by_actor_id,
    )


@router.post("/brands/{brand_id}/matrix/{matrix_brief_id}/evaluate", response_model=MatrixReceipt)
async def evaluate_matrix_brief(
    brand_id: UUID,
    matrix_brief_id: UUID,
    organization_id: UUID,
    evaluator_actor_id: UUID,
    service: MatrixService = Depends(get_matrix_service),
) -> MatrixReceipt:
    return service.evaluate_matrix_collision(
        organization_id=organization_id,
        brand_id=brand_id,
        matrix_brief_id=matrix_brief_id,
        evaluator_actor_id=evaluator_actor_id,
    )
