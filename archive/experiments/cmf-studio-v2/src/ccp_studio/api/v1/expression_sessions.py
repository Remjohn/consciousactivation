"""FastAPI adapter for TS-CMF-029 Complete Expression Sessions."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.expression_session import CompleteExpressionSession, SessionStartReceipt
from ccp_studio.services.consent_service import ConsentService
from ccp_studio.services.expression_session_service import CompleteExpressionSessionService
from ccp_studio.services.interview_contract_service import InterviewContractService
from ccp_studio.services.matrix_service import MatrixService
from ccp_studio.services.pre_induction_service import PreInductionService
from ccp_studio.services.source_ingestion import SourceIngestionService
from ccp_studio.services.context_compilation_service import ContextCompilationService
from ccp_studio.services.research_service import ResearchService


router = APIRouter(prefix="/api/v1/expression-sessions", tags=["expression-sessions"])


class CreateExpressionSessionRequest(BaseModel):
    guest_id: UUID
    operator_id: UUID
    interview_deck_id: UUID
    consent_record_version_id: UUID
    conversation_language: str = "en"
    expected_master_source: str
    backup_route: str
    platform_source: str | None = None
    upload_method: str = "operator_upload"
    file_safety_expectations: list[str] = []
    quality_requirements: list[str]
    quality_gate_passed: bool = True


_research_service = ResearchService()
_context_service = ContextCompilationService(research_service=_research_service)
_matrix_service = MatrixService(context_service=_context_service)
_pre_induction_service = PreInductionService(context_service=_context_service, matrix_service=_matrix_service)
_interview_contract_service = InterviewContractService(pre_induction_service=_pre_induction_service, matrix_service=_matrix_service)
_expression_session_service = CompleteExpressionSessionService(
    consent_service=ConsentService(),
    source_service=SourceIngestionService(),
    interview_contract_service=_interview_contract_service,
)


def set_expression_session_service(service: CompleteExpressionSessionService) -> None:
    global _expression_session_service
    _expression_session_service = service


def get_expression_session_service() -> CompleteExpressionSessionService:
    return _expression_session_service


@router.post("/brands/{brand_id}", response_model=CompleteExpressionSession)
def create_expression_session(
    brand_id: UUID,
    organization_id: UUID,
    request: CreateExpressionSessionRequest,
    service: CompleteExpressionSessionService = Depends(get_expression_session_service),
) -> CompleteExpressionSession:
    return service.create_session(
        organization_id=organization_id,
        brand_id=brand_id,
        guest_id=request.guest_id,
        operator_id=request.operator_id,
        interview_deck_id=request.interview_deck_id,
        consent_record_version_id=request.consent_record_version_id,
        conversation_language=request.conversation_language,
        created_by_actor_id=request.operator_id,
        expected_master_source=request.expected_master_source,
        backup_route=request.backup_route,
        platform_source=request.platform_source,
        upload_method=request.upload_method,
        file_safety_expectations=request.file_safety_expectations,
        quality_requirements=request.quality_requirements,
        quality_gate_passed=request.quality_gate_passed,
    )


@router.post("/brands/{brand_id}/{expression_session_id}/validate", response_model=SessionStartReceipt)
def validate_expression_session(
    brand_id: UUID,
    organization_id: UUID,
    expression_session_id: UUID,
    actor_id: UUID,
    service: CompleteExpressionSessionService = Depends(get_expression_session_service),
) -> SessionStartReceipt:
    return service.validate_readiness(
        organization_id=organization_id,
        brand_id=brand_id,
        expression_session_id=expression_session_id,
        actor_id=actor_id,
    )


@router.post("/brands/{brand_id}/{expression_session_id}/start", response_model=CompleteExpressionSession)
def start_expression_session(
    brand_id: UUID,
    organization_id: UUID,
    expression_session_id: UUID,
    actor_id: UUID,
    service: CompleteExpressionSessionService = Depends(get_expression_session_service),
) -> CompleteExpressionSession:
    return service.start_session(
        organization_id=organization_id,
        brand_id=brand_id,
        expression_session_id=expression_session_id,
        actor_id=actor_id,
    )
