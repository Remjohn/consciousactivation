"""FastAPI adapter for TS-CMF-028 induction rationale actions."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.induction import InductionRationaleInspection, InductionRationaleReceipt
from ccp_studio.services.context_compilation_service import ContextCompilationService
from ccp_studio.services.induction_rationale_service import InductionRationaleService
from ccp_studio.services.matrix_service import MatrixService
from ccp_studio.services.pre_induction_service import PreInductionService
from ccp_studio.services.research_service import ResearchService


router = APIRouter(prefix="/api/v1/induction", tags=["induction"])


class CompileInductionRationaleRequest(BaseModel):
    pre_induction_plan_id: UUID
    matrix_brief_id: UUID
    actor_id: UUID
    interview_deck_id: UUID | None = None
    include_emotional_dna: bool = True
    include_voice_dna: bool = True


_research_service = ResearchService()
_context_service = ContextCompilationService(research_service=_research_service)
_matrix_service = MatrixService(context_service=_context_service)
_pre_induction_service = PreInductionService(context_service=_context_service, matrix_service=_matrix_service)
_induction_service = InductionRationaleService(
    context_service=_context_service,
    matrix_service=_matrix_service,
    pre_induction_service=_pre_induction_service,
)


def set_induction_rationale_service(service: InductionRationaleService) -> None:
    global _induction_service
    _induction_service = service


def get_induction_rationale_service() -> InductionRationaleService:
    return _induction_service


@router.post("/brands/{brand_id}/rationales", response_model=InductionRationaleReceipt)
def compile_induction_rationales(
    brand_id: UUID,
    organization_id: UUID,
    request: CompileInductionRationaleRequest,
    service: InductionRationaleService = Depends(get_induction_rationale_service),
) -> InductionRationaleReceipt:
    return service.compile_induction_rationales(
        organization_id=organization_id,
        brand_id=brand_id,
        pre_induction_plan_id=request.pre_induction_plan_id,
        matrix_brief_id=request.matrix_brief_id,
        interview_deck_id=request.interview_deck_id,
        include_emotional_dna=request.include_emotional_dna,
        include_voice_dna=request.include_voice_dna,
        actor_id=request.actor_id,
    )


@router.get("/brands/{brand_id}/moves/{planned_move_id}/rationale", response_model=InductionRationaleInspection)
def inspect_move_rationale(
    brand_id: UUID,
    organization_id: UUID,
    planned_move_id: UUID,
    service: InductionRationaleService = Depends(get_induction_rationale_service),
) -> InductionRationaleInspection:
    return service.inspect_rationale_for_move(
        organization_id=organization_id,
        brand_id=brand_id,
        planned_move_id=planned_move_id,
    )
