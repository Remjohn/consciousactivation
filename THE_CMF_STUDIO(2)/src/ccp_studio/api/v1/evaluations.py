"""FastAPI adapter for TS-CMF-050 evaluation receipts."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.evaluation_receipts import EvaluationReceipt, EvaluationReviewReadModel
from ccp_studio.services.evaluation_receipt_service import EvaluationReceiptService


router = APIRouter(prefix="/api/v1/evaluations", tags=["evaluations"])
_evaluation_receipt_service: EvaluationReceiptService | None = None


class GenerateEvaluationReceiptRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    object_type: str
    object_id: UUID
    object_hash: str
    actor_id: UUID
    category_inputs: list[dict[str, Any]] = Field(default_factory=list)
    threshold_profile_id: str = "cmf.default.thresholds.v1"
    previous_receipt_id: UUID | None = None
    warnings: list[str] = Field(default_factory=list)


class RerunEvaluationRequest(BaseModel):
    previous_receipt_id: UUID
    revised_object_hash: str
    actor_id: UUID
    category_inputs: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


def set_evaluation_receipt_service(service: EvaluationReceiptService) -> None:
    global _evaluation_receipt_service
    _evaluation_receipt_service = service


def get_evaluation_receipt_service() -> EvaluationReceiptService:
    if _evaluation_receipt_service is None:
        raise RuntimeError("EvaluationReceiptService must be configured by the application.")
    return _evaluation_receipt_service


@router.post("/receipts", response_model=EvaluationReceipt)
def generate_evaluation_receipt(
    request: GenerateEvaluationReceiptRequest,
    service: EvaluationReceiptService = Depends(get_evaluation_receipt_service),
) -> EvaluationReceipt:
    return service.generate_evaluation_receipt(**request.model_dump())


@router.post("/reruns", response_model=EvaluationReceipt)
def rerun_evaluation_after_revision(
    request: RerunEvaluationRequest,
    service: EvaluationReceiptService = Depends(get_evaluation_receipt_service),
) -> EvaluationReceipt:
    return service.rerun_after_revision(**request.model_dump())


@router.get("/receipts/{evaluation_receipt_id}/review", response_model=EvaluationReviewReadModel)
def get_evaluation_review_read_model(
    evaluation_receipt_id: UUID,
    service: EvaluationReceiptService = Depends(get_evaluation_receipt_service),
) -> EvaluationReviewReadModel:
    return service.build_review_read_model(evaluation_receipt_id)

