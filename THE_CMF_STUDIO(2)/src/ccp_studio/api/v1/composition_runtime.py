"""FastAPI adapter for Batch 1 composition runtime contracts."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.composition_runtime import (
    CompositionEvalSuiteRun,
    CompositionOperatorApprovalReceipt,
    CompositionPreflightReceipt,
    FourVideoFormatPlan,
    IntegrationAdapterDecision,
    IntegrationCandidate,
    PrimitiveValidationResult,
    ReviewReadModel,
)
from ccp_studio.services.composition_runtime_service import CompositionRuntimeService


router = APIRouter(prefix="/api/v1/composition-runtime", tags=["composition-runtime"])
_composition_runtime_service = CompositionRuntimeService()


class PlanFourVideoFormatsRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    expression_moment_id: UUID


class PrimitivePreflightRequest(BaseModel):
    route_id: str
    composition_id: str
    visual_feel_contract_id: UUID
    primitive_results: list[PrimitiveValidationResult]


class IntegrationFitEvalRequest(BaseModel):
    candidate: IntegrationCandidate


class EvalSuiteRequest(BaseModel):
    target_object_type: str
    target_object_ref: str
    preflight_receipt_id: UUID
    doctrine_receipt_refs: list[str] = []


class ReviewReadModelRequest(BaseModel):
    target_object_ref: str
    eval_suite_run_id: UUID
    evidence_refs: list[str]


class OperatorApprovalRequest(BaseModel):
    review_read_model_id: UUID
    operator_id: UUID


def set_composition_runtime_service(service: CompositionRuntimeService) -> None:
    global _composition_runtime_service
    _composition_runtime_service = service


def get_composition_runtime_service() -> CompositionRuntimeService:
    return _composition_runtime_service


@router.post("/four-video-plan", response_model=FourVideoFormatPlan)
def plan_four_video_formats(
    request: PlanFourVideoFormatsRequest,
    service: CompositionRuntimeService = Depends(get_composition_runtime_service),
) -> FourVideoFormatPlan:
    return service.plan_four_video_formats(
        organization_id=request.organization_id,
        brand_id=request.brand_id,
        expression_moment_id=request.expression_moment_id,
    )


@router.post("/primitive-preflight", response_model=CompositionPreflightReceipt)
def run_primitive_preflight(
    request: PrimitivePreflightRequest,
    service: CompositionRuntimeService = Depends(get_composition_runtime_service),
) -> CompositionPreflightReceipt:
    return service.validate_primitive_preflight(
        route_id=request.route_id,
        composition_id=request.composition_id,
        visual_feel_contract_id=request.visual_feel_contract_id,
        primitive_results=request.primitive_results,
    )


@router.post("/integrations/evaluate", response_model=IntegrationAdapterDecision)
def evaluate_integration_candidate(
    request: IntegrationFitEvalRequest,
    service: CompositionRuntimeService = Depends(get_composition_runtime_service),
) -> IntegrationAdapterDecision:
    candidate = service.register_integration_candidate(request.candidate)
    return service.run_integration_fit_eval(candidate.integration_candidate_id)


@router.post("/eval-suite", response_model=CompositionEvalSuiteRun)
def run_composition_eval_suite(
    request: EvalSuiteRequest,
    service: CompositionRuntimeService = Depends(get_composition_runtime_service),
) -> CompositionEvalSuiteRun:
    return service.run_composition_eval_suite(
        target_object_type=request.target_object_type,
        target_object_ref=request.target_object_ref,
        preflight_receipt_id=request.preflight_receipt_id,
        doctrine_receipt_refs=request.doctrine_receipt_refs,
    )


@router.post("/review-read-model", response_model=ReviewReadModel)
def build_composition_review_read_model(
    request: ReviewReadModelRequest,
    service: CompositionRuntimeService = Depends(get_composition_runtime_service),
) -> ReviewReadModel:
    return service.build_review_read_model(
        target_object_ref=request.target_object_ref,
        eval_suite_run_id=request.eval_suite_run_id,
        evidence_refs=request.evidence_refs,
    )


@router.post("/operator-approval", response_model=CompositionOperatorApprovalReceipt)
def record_operator_approval(
    request: OperatorApprovalRequest,
    service: CompositionRuntimeService = Depends(get_composition_runtime_service),
) -> CompositionOperatorApprovalReceipt:
    return service.record_operator_approval(
        review_read_model_id=request.review_read_model_id,
        operator_id=request.operator_id,
    )
