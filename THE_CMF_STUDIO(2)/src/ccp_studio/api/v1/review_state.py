"""FastAPI adapter for TS-CMF-051 evidence-rich review state."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.review_state import EvaluationFailureView, ReviewEvidenceState
from ccp_studio.contracts.surfaces import DeepLinkTarget
from ccp_studio.services.review_state_service import ReviewStateService


router = APIRouter(prefix="/api/v1/review-states", tags=["review-states"])
_review_state_service: ReviewStateService | None = None


class BuildReviewEvidenceStateRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    approval_evidence_view_id: UUID
    actor_id: UUID
    preview_ref: str | None = None
    source_quote_ref: str | None = None
    archetype_route_ref: str | None = None
    brand_context_version_id: UUID | None = None
    selected_asset_refs: list[str] = Field(default_factory=list)
    render_output_refs: list[str] = Field(default_factory=list)
    rendered_with_consent_record_version_id: UUID | None = None
    telegram_complexity_score: int = 0
    surface_route: str | None = None


class PwaDeepLinkRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    object_type: str
    object_id: UUID
    route: str
    required_reason: str = "PWA_REVIEW_REQUIRED"


def set_review_state_service(service: ReviewStateService) -> None:
    global _review_state_service
    _review_state_service = service


def get_review_state_service() -> ReviewStateService:
    if _review_state_service is None:
        raise RuntimeError("ReviewStateService must be configured by the application.")
    return _review_state_service


@router.post("", response_model=ReviewEvidenceState)
def build_review_evidence_state(
    request: BuildReviewEvidenceStateRequest,
    service: ReviewStateService = Depends(get_review_state_service),
) -> ReviewEvidenceState:
    return service.build_review_evidence_state(**request.model_dump())


@router.get("/{review_state_id}/failures/{category}", response_model=EvaluationFailureView)
def expand_evaluation_failure(
    review_state_id: UUID,
    category: str,
    service: ReviewStateService = Depends(get_review_state_service),
) -> EvaluationFailureView:
    return service.expand_evaluation_failure(review_state_id=review_state_id, category=category)


@router.get("/{review_state_id}/completeness", response_model=dict[str, str])
def validate_review_evidence_completeness(
    review_state_id: UUID,
    service: ReviewStateService = Depends(get_review_state_service),
) -> dict[str, str]:
    return service.validate_review_evidence_completeness(review_state_id)


@router.post("/pwa-deep-links", response_model=DeepLinkTarget)
def create_pwa_review_deep_link(
    request: PwaDeepLinkRequest,
    service: ReviewStateService = Depends(get_review_state_service),
) -> DeepLinkTarget:
    return service.create_pwa_review_deep_link(**request.model_dump())

