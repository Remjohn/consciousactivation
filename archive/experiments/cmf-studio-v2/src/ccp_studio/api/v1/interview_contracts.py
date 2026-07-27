"""Interview Asset Contract API adapter for TS-CMF-027."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.interview_contracts import ContractCompilationReceipt, InterviewDeck
from ccp_studio.services.context_compilation_service import ContextCompilationService
from ccp_studio.services.interview_contract_service import InterviewContractService
from ccp_studio.services.matrix_service import MatrixService
from ccp_studio.services.pre_induction_service import PreInductionService
from ccp_studio.services.research_service import ResearchService


class CompileInterviewDeckRequest(BaseModel):
    organization_id: UUID
    pre_induction_plan_id: UUID
    matrix_brief_id: UUID
    compiled_by_actor_id: UUID


router = APIRouter(prefix="/api/v1/interviews/preparation", tags=["interview-contracts"])
_context_service = ContextCompilationService(research_service=ResearchService())
_matrix_service = MatrixService(context_service=_context_service)
_contract_service = InterviewContractService(
    pre_induction_service=PreInductionService(context_service=_context_service, matrix_service=_matrix_service),
    matrix_service=_matrix_service,
)


def set_interview_contract_service(service: InterviewContractService) -> None:
    global _contract_service
    _contract_service = service


def get_interview_contract_service() -> InterviewContractService:
    return _contract_service


@router.post("/brands/{brand_id}/interview-deck", response_model=InterviewDeck)
async def compile_interview_deck(
    brand_id: UUID,
    request: CompileInterviewDeckRequest,
    service: InterviewContractService = Depends(get_interview_contract_service),
) -> InterviewDeck:
    return service.compile_interview_deck(
        organization_id=request.organization_id,
        brand_id=brand_id,
        pre_induction_plan_id=request.pre_induction_plan_id,
        matrix_brief_id=request.matrix_brief_id,
        compiled_by_actor_id=request.compiled_by_actor_id,
    )


@router.post("/brands/{brand_id}/interview-deck/{interview_deck_id}/evaluate", response_model=ContractCompilationReceipt)
async def evaluate_interview_deck(
    brand_id: UUID,
    interview_deck_id: UUID,
    organization_id: UUID,
    evaluator_actor_id: UUID,
    service: InterviewContractService = Depends(get_interview_contract_service),
) -> ContractCompilationReceipt:
    return service.evaluate_interview_plan(
        organization_id=organization_id,
        brand_id=brand_id,
        interview_deck_id=interview_deck_id,
        evaluator_actor_id=evaluator_actor_id,
    )
