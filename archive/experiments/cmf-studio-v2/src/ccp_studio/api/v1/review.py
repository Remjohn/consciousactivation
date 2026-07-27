"""Review evidence API adapter for TS-CMF-012."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.review_evidence import ApprovalEvidenceView, SourceReference
from ccp_studio.repositories.consent_record_versions import InMemoryConsentRepository
from ccp_studio.repositories.source_artifacts import InMemorySourceArtifactRepository
from ccp_studio.services.review_evidence_service import ReviewEvidenceService


class GenerateApprovalEvidenceViewRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    guest_or_client_id: UUID
    object_type: str
    object_id: UUID
    source_references: list[SourceReference]
    evaluation_receipt_ids: list[UUID]
    audio_mix_manifest_id: UUID | None = None
    file_provenance_refs: list[str] = []
    telegram_complexity_score: int = 0


router = APIRouter(prefix="/api/v1/review", tags=["review"])
_review_service = ReviewEvidenceService(InMemoryConsentRepository(), InMemorySourceArtifactRepository())


def set_review_service(service: ReviewEvidenceService) -> None:
    global _review_service
    _review_service = service


def get_review_service() -> ReviewEvidenceService:
    return _review_service


@router.post("/evidence", response_model=ApprovalEvidenceView)
async def generate_approval_evidence_view(
    request: GenerateApprovalEvidenceViewRequest,
    service: ReviewEvidenceService = Depends(get_review_service),
) -> ApprovalEvidenceView:
    return service.generate_evidence_view(
        organization_id=request.organization_id,
        brand_id=request.brand_id,
        guest_or_client_id=request.guest_or_client_id,
        object_type=request.object_type,
        object_id=request.object_id,
        source_references=request.source_references,
        evaluation_receipt_ids=request.evaluation_receipt_ids,
        audio_mix_manifest_id=request.audio_mix_manifest_id,
        file_provenance_refs=request.file_provenance_refs,
        telegram_complexity_score=request.telegram_complexity_score,
    )
