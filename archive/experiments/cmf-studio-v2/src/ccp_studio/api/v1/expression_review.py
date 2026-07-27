"""FastAPI adapter for TS-CMF-032 Expression Moment review."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.expression_review import (
    ExpressionMomentBoundary,
    ExpressionMomentReviewSurfaceItem,
    ExpressionReviewReceipt,
    ReviewRejectionCode,
)
from ccp_studio.services.expression_review_service import ExpressionReviewService


router = APIRouter(prefix="/api/v1/expression-moments", tags=["expression-moments"])
_expression_review_service: ExpressionReviewService | None = None


class ApproveExpressionMomentRequest(BaseModel):
    actor_id: UUID
    rationale: str
    annotations: list[str] = []
    boundary: ExpressionMomentBoundary | None = None


class RejectExpressionMomentRequest(BaseModel):
    actor_id: UUID
    rationale: str
    rejection_code: ReviewRejectionCode


class SensitivityHoldRequest(BaseModel):
    actor_id: UUID
    reason: str
    consent_record_version_id: UUID | None = None


def set_expression_review_service(service: ExpressionReviewService) -> None:
    global _expression_review_service
    _expression_review_service = service


def get_expression_review_service() -> ExpressionReviewService:
    if _expression_review_service is None:
        raise RuntimeError("ExpressionReviewService must be configured by the application.")
    return _expression_review_service


@router.get("/brands/{brand_id}/candidates/{candidate_id}/review-surface", response_model=ExpressionMomentReviewSurfaceItem)
def get_candidate_review_surface(
    brand_id: UUID,
    organization_id: UUID,
    candidate_id: UUID,
    service: ExpressionReviewService = Depends(get_expression_review_service),
) -> ExpressionMomentReviewSurfaceItem:
    return service.review_surface_for_candidate(
        organization_id=organization_id,
        brand_id=brand_id,
        candidate_id=candidate_id,
    )


@router.post("/brands/{brand_id}/candidates/{candidate_id}/approve", response_model=ExpressionReviewReceipt)
def approve_expression_moment(
    brand_id: UUID,
    organization_id: UUID,
    candidate_id: UUID,
    request: ApproveExpressionMomentRequest,
    service: ExpressionReviewService = Depends(get_expression_review_service),
) -> ExpressionReviewReceipt:
    return service.approve_expression_moment(
        organization_id=organization_id,
        brand_id=brand_id,
        candidate_id=candidate_id,
        reviewer_actor_id=request.actor_id,
        rationale=request.rationale,
        boundary=request.boundary,
        annotations=request.annotations,
    )


@router.post("/brands/{brand_id}/candidates/{candidate_id}/reject", response_model=ExpressionReviewReceipt)
def reject_expression_moment(
    brand_id: UUID,
    organization_id: UUID,
    candidate_id: UUID,
    request: RejectExpressionMomentRequest,
    service: ExpressionReviewService = Depends(get_expression_review_service),
) -> ExpressionReviewReceipt:
    return service.reject_expression_moment_candidate(
        organization_id=organization_id,
        brand_id=brand_id,
        candidate_id=candidate_id,
        reviewer_actor_id=request.actor_id,
        rationale=request.rationale,
        rejection_code=request.rejection_code,
    )


@router.post("/brands/{brand_id}/moments/{expression_moment_id}/hold", response_model=ExpressionReviewReceipt)
def place_expression_moment_hold(
    brand_id: UUID,
    organization_id: UUID,
    expression_moment_id: UUID,
    request: SensitivityHoldRequest,
    service: ExpressionReviewService = Depends(get_expression_review_service),
) -> ExpressionReviewReceipt:
    return service.place_sensitivity_hold(
        organization_id=organization_id,
        brand_id=brand_id,
        expression_moment_id=expression_moment_id,
        reviewer_actor_id=request.actor_id,
        reason=request.reason,
        consent_record_version_id=request.consent_record_version_id,
    )
