"""FastAPI adapter for TS-CMF-056 evidence-backed memory admission."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.memory_admission import MemoryAdmissionCandidate, MemoryAdmissionReceipt, MemoryPolicyDecision, MemoryUsageCitation
from ccp_studio.services.memory_admission_service import MemoryAdmissionService


router = APIRouter(prefix="/api/v1/memory", tags=["memory-admission"])
_memory_admission_service: MemoryAdmissionService | None = None


class ProposeMemoryAdmissionRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    memory_type: str
    proposed_from_event_id: str
    proposed_statement: str
    evidence_refs: list[dict[str, Any]] = Field(default_factory=list)
    confidence: float
    scope: str
    consent_record_version_id: UUID | None = None
    consent_compatible: bool
    provenance_summary: str
    proposed_by_actor_id: UUID
    originating_route_ref: str | None = None
    downstream_usage_constraints: list[str] = Field(default_factory=list)
    idempotency_key: str | None = None


class MemoryAdmissionDecisionRequest(BaseModel):
    candidate_id: UUID
    reviewer_id: UUID
    role_ids: list[str] = Field(default_factory=list)
    reason: str | None = None
    idempotency_key: str


class MemoryUsageCitationRequest(BaseModel):
    memory_event_id: UUID
    compiler_or_agent: str
    citing_object_ref: str
    evidence_refs: list[dict[str, Any]]
    idempotency_key: str


def set_memory_admission_service(service: MemoryAdmissionService) -> None:
    global _memory_admission_service
    _memory_admission_service = service


def get_memory_admission_service() -> MemoryAdmissionService:
    if _memory_admission_service is None:
        raise RuntimeError("MemoryAdmissionService must be configured by the application.")
    return _memory_admission_service


@router.post("/candidates", response_model=MemoryAdmissionCandidate)
def propose_memory_admission(
    request: ProposeMemoryAdmissionRequest,
    service: MemoryAdmissionService = Depends(get_memory_admission_service),
) -> MemoryAdmissionCandidate:
    return service.propose_memory_admission(**request.model_dump())


@router.get("/candidates/{candidate_id}/evidence", response_model=MemoryPolicyDecision)
def validate_memory_evidence(
    candidate_id: UUID,
    service: MemoryAdmissionService = Depends(get_memory_admission_service),
) -> MemoryPolicyDecision:
    return service.validate_memory_evidence(candidate_id)


@router.get("/candidates/{candidate_id}/consent", response_model=MemoryPolicyDecision)
def validate_memory_consent(
    candidate_id: UUID,
    service: MemoryAdmissionService = Depends(get_memory_admission_service),
) -> MemoryPolicyDecision:
    return service.validate_memory_consent(candidate_id)


@router.post("/approve", response_model=MemoryAdmissionReceipt)
def approve_memory_admission(
    request: MemoryAdmissionDecisionRequest,
    service: MemoryAdmissionService = Depends(get_memory_admission_service),
) -> MemoryAdmissionReceipt:
    return service.approve_memory_admission(**request.model_dump(exclude={"reason"}))


@router.post("/reject", response_model=MemoryAdmissionReceipt)
def reject_memory_admission(
    request: MemoryAdmissionDecisionRequest,
    service: MemoryAdmissionService = Depends(get_memory_admission_service),
) -> MemoryAdmissionReceipt:
    return service.reject_memory_admission(
        candidate_id=request.candidate_id,
        reviewer_id=request.reviewer_id,
        role_ids=request.role_ids,
        reason=request.reason or "Rejected by memory reviewer.",
        idempotency_key=request.idempotency_key,
    )


@router.post("/quarantine", response_model=MemoryAdmissionReceipt)
def quarantine_memory_candidate(
    request: MemoryAdmissionDecisionRequest,
    service: MemoryAdmissionService = Depends(get_memory_admission_service),
) -> MemoryAdmissionReceipt:
    return service.quarantine_memory_candidate(
        candidate_id=request.candidate_id,
        reviewer_id=request.reviewer_id,
        role_ids=request.role_ids,
        reason=request.reason or "Quarantined by memory reviewer.",
        idempotency_key=request.idempotency_key,
    )


@router.post("/citations", response_model=MemoryUsageCitation)
def record_memory_usage_citation(
    request: MemoryUsageCitationRequest,
    service: MemoryAdmissionService = Depends(get_memory_admission_service),
) -> MemoryUsageCitation:
    return service.record_memory_usage_citation(**request.model_dump())
