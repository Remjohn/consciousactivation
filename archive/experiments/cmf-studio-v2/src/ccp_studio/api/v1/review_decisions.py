"""FastAPI adapter for TS-CMF-052 governed review decisions."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.review_decisions import ReviewDecisionReceipt
from ccp_studio.services.review_decision_service import ReviewDecisionService


router = APIRouter(prefix="/api/v1/review-decisions", tags=["review-decisions"])
_review_decision_service: ReviewDecisionService | None = None


class ReviewDecisionRequest(BaseModel):
    review_state_id: UUID
    actor_id: UUID
    role_ids: list[str] = Field(default_factory=list)
    object_version_hash: str
    idempotency_key: str
    approval_policy_report_id: UUID | None = None
    reason: str | None = None
    failure_category: str | None = None
    expected_repair: str | None = None
    source_gap_ref: str | None = None
    eligibility_report_id: UUID | None = None
    structural_repair_reason: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)


def set_review_decision_service(service: ReviewDecisionService) -> None:
    global _review_decision_service
    _review_decision_service = service


def get_review_decision_service() -> ReviewDecisionService:
    if _review_decision_service is None:
        raise RuntimeError("ReviewDecisionService must be configured by the application.")
    return _review_decision_service


@router.post("/approve", response_model=ReviewDecisionReceipt)
def approve_asset(
    request: ReviewDecisionRequest,
    service: ReviewDecisionService = Depends(get_review_decision_service),
) -> ReviewDecisionReceipt:
    return service.approve_asset(
        review_state_id=request.review_state_id,
        actor_id=request.actor_id,
        role_ids=request.role_ids,
        object_version_hash=request.object_version_hash,
        idempotency_key=request.idempotency_key,
        approval_policy_report_id=request.approval_policy_report_id,
    )


@router.post("/reject", response_model=ReviewDecisionReceipt)
def reject_asset(
    request: ReviewDecisionRequest,
    service: ReviewDecisionService = Depends(get_review_decision_service),
) -> ReviewDecisionReceipt:
    return service.reject_asset(
        review_state_id=request.review_state_id,
        actor_id=request.actor_id,
        role_ids=request.role_ids,
        object_version_hash=request.object_version_hash,
        reason=request.reason or "Rejected during review.",
        evidence_refs=request.evidence_refs,
        idempotency_key=request.idempotency_key,
    )


@router.post("/request-revision", response_model=ReviewDecisionReceipt)
def request_revision(
    request: ReviewDecisionRequest,
    service: ReviewDecisionService = Depends(get_review_decision_service),
) -> ReviewDecisionReceipt:
    return service.request_revision(
        review_state_id=request.review_state_id,
        actor_id=request.actor_id,
        role_ids=request.role_ids,
        object_version_hash=request.object_version_hash,
        failure_category=request.failure_category or "review",
        evidence_refs=request.evidence_refs,
        expected_repair=request.expected_repair or "repair evidence-backed review finding",
        idempotency_key=request.idempotency_key,
    )


@router.post("/escalate", response_model=ReviewDecisionReceipt)
def escalate_manual_review(
    request: ReviewDecisionRequest,
    service: ReviewDecisionService = Depends(get_review_decision_service),
) -> ReviewDecisionReceipt:
    return service.escalate_manual_review(
        review_state_id=request.review_state_id,
        actor_id=request.actor_id,
        role_ids=request.role_ids,
        object_version_hash=request.object_version_hash,
        reason=request.reason or "Manual escalation requested.",
        idempotency_key=request.idempotency_key,
    )


@router.post("/request-voice-dna-boost", response_model=ReviewDecisionReceipt)
def request_voice_dna_boost(
    request: ReviewDecisionRequest,
    service: ReviewDecisionService = Depends(get_review_decision_service),
) -> ReviewDecisionReceipt:
    if request.eligibility_report_id is None or request.source_gap_ref is None or request.structural_repair_reason is None:
        raise ValueError("Voice-DNA Boost requires eligibility_report_id, source_gap_ref, and structural_repair_reason.")
    return service.request_voice_dna_boost(
        review_state_id=request.review_state_id,
        actor_id=request.actor_id,
        role_ids=request.role_ids,
        object_version_hash=request.object_version_hash,
        source_gap_ref=request.source_gap_ref,
        eligibility_report_id=request.eligibility_report_id,
        structural_repair_reason=request.structural_repair_reason,
        evidence_refs=request.evidence_refs,
        idempotency_key=request.idempotency_key,
    )
