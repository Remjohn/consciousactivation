"""Pre-induction API adapter for TS-CMF-026."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.pre_induction import PreInductionPlan, PreInductionReceipt
from ccp_studio.services.context_compilation_service import ContextCompilationService
from ccp_studio.services.matrix_service import MatrixService
from ccp_studio.services.pre_induction_service import PreInductionService
from ccp_studio.services.research_service import ResearchService


class CompilePreInductionPlanRequest(BaseModel):
    organization_id: UUID
    guest_id: UUID | None = None
    operator_id: UUID
    context_premise_id: UUID
    matrix_brief_id: UUID
    resonance_context_id: UUID | None = None
    compiled_by_actor_id: UUID


router = APIRouter(prefix="/api/v1/interviews/preparation", tags=["pre-induction"])
_context_service = ContextCompilationService(research_service=ResearchService())
_pre_induction_service = PreInductionService(
    context_service=_context_service,
    matrix_service=MatrixService(context_service=_context_service),
)


def set_pre_induction_service(service: PreInductionService) -> None:
    global _pre_induction_service
    _pre_induction_service = service


def get_pre_induction_service() -> PreInductionService:
    return _pre_induction_service


@router.post("/brands/{brand_id}/pre-induction", response_model=PreInductionPlan)
async def compile_pre_induction_plan(
    brand_id: UUID,
    request: CompilePreInductionPlanRequest,
    service: PreInductionService = Depends(get_pre_induction_service),
) -> PreInductionPlan:
    return service.compile_pre_induction_plan(
        organization_id=request.organization_id,
        brand_id=brand_id,
        guest_id=request.guest_id,
        operator_id=request.operator_id,
        context_premise_id=request.context_premise_id,
        matrix_brief_id=request.matrix_brief_id,
        resonance_context_id=request.resonance_context_id,
        compiled_by_actor_id=request.compiled_by_actor_id,
    )


@router.post("/brands/{brand_id}/pre-induction/{pre_induction_plan_id}/evaluate", response_model=PreInductionReceipt)
async def evaluate_pre_induction_plan(
    brand_id: UUID,
    pre_induction_plan_id: UUID,
    organization_id: UUID,
    evaluator_actor_id: UUID,
    service: PreInductionService = Depends(get_pre_induction_service),
) -> PreInductionReceipt:
    return service.evaluate_pre_induction_plan(
        organization_id=organization_id,
        brand_id=brand_id,
        pre_induction_plan_id=pre_induction_plan_id,
        evaluator_actor_id=evaluator_actor_id,
    )
