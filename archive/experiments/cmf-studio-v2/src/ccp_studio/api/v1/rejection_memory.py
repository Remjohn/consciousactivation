"""FastAPI adapter for TS-CMF-035 rejection memory."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.rejection_memory import NegativeEvidenceRef, RejectionCategory, RejectionReceipt
from ccp_studio.services.rejection_memory_service import RejectionMemoryService


router = APIRouter(prefix="/api/v1/rejection-memory", tags=["rejection-memory"])
_rejection_memory_service: RejectionMemoryService | None = None


class RecordRejectedCandidateRequest(BaseModel):
    actor_id: UUID
    candidate_id: UUID
    category: RejectionCategory
    reason: str
    route_attempt_receipt_id: UUID | None = None
    consent_record_version_id: UUID | None = None
    sensitive_material: bool = False


class ReferenceNegativeEvidenceRequest(BaseModel):
    compiler_or_evaluator: str
    usage_purpose: str


def set_rejection_memory_service(service: RejectionMemoryService) -> None:
    global _rejection_memory_service
    _rejection_memory_service = service


def get_rejection_memory_service() -> RejectionMemoryService:
    if _rejection_memory_service is None:
        raise RuntimeError("RejectionMemoryService must be configured by the application.")
    return _rejection_memory_service


@router.post("/brands/{brand_id}/rejected-candidates", response_model=RejectionReceipt)
def record_rejected_candidate(
    brand_id: UUID,
    organization_id: UUID,
    request: RecordRejectedCandidateRequest,
    service: RejectionMemoryService = Depends(get_rejection_memory_service),
) -> RejectionReceipt:
    return service.record_rejected_expression_candidate(
        organization_id=organization_id,
        brand_id=brand_id,
        candidate_id=request.candidate_id,
        category=request.category,
        reason=request.reason,
        reviewer_id=request.actor_id,
        route_attempt_receipt_id=request.route_attempt_receipt_id,
        consent_record_version_id=request.consent_record_version_id,
        sensitive_material=request.sensitive_material,
    )


@router.post("/negative-evidence/{rejection_receipt_id}", response_model=NegativeEvidenceRef)
def reference_negative_evidence(
    rejection_receipt_id: UUID,
    request: ReferenceNegativeEvidenceRequest,
    service: RejectionMemoryService = Depends(get_rejection_memory_service),
) -> NegativeEvidenceRef:
    return service.reference_negative_evidence(
        rejection_receipt_id=rejection_receipt_id,
        compiler_or_evaluator=request.compiler_or_evaluator,
        usage_purpose=request.usage_purpose,
    )
