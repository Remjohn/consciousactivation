"""FastAPI adapter for TS-CMF-057 memory governance."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.memory_governance import MemoryGovernanceActionType, MemoryGovernanceReceipt, MemoryReviewState, MemoryUsagePolicyDecision
from ccp_studio.services.memory_governance_service import MemoryGovernanceService


router = APIRouter(prefix="/api/v1/memory/governance", tags=["memory-governance"])
_memory_governance_service: MemoryGovernanceService | None = None


class MemoryGovernanceRequest(BaseModel):
    memory_event_id: UUID
    requested_by_user_id: UUID
    role_ids: list[str] = Field(default_factory=list)
    reason: str
    evidence_refs: list[str] = Field(min_length=1)
    idempotency_key: str
    corrected_statement: str | None = None


class MemoryUsageValidationRequest(BaseModel):
    memory_event_id: UUID
    compiler_or_agent: str
    usage_purpose: str


def set_memory_governance_service(service: MemoryGovernanceService) -> None:
    global _memory_governance_service
    _memory_governance_service = service


def get_memory_governance_service() -> MemoryGovernanceService:
    if _memory_governance_service is None:
        raise RuntimeError("MemoryGovernanceService must be configured by the application.")
    return _memory_governance_service


@router.get("/{memory_event_id}", response_model=MemoryReviewState)
def build_memory_review_state(
    memory_event_id: UUID,
    service: MemoryGovernanceService = Depends(get_memory_governance_service),
) -> MemoryReviewState:
    return service.build_memory_review_state(memory_event_id)


@router.post("/{action_type}", response_model=MemoryGovernanceReceipt)
def apply_memory_governance_action(
    action_type: MemoryGovernanceActionType,
    request: MemoryGovernanceRequest,
    service: MemoryGovernanceService = Depends(get_memory_governance_service),
) -> MemoryGovernanceReceipt:
    kwargs = request.model_dump()
    if action_type == MemoryGovernanceActionType.correct:
        return service.correct_memory(**kwargs)
    if action_type == MemoryGovernanceActionType.reverse:
        kwargs.pop("corrected_statement", None)
        return service.reverse_memory(**kwargs)
    if action_type == MemoryGovernanceActionType.expire:
        kwargs.pop("corrected_statement", None)
        return service.expire_memory(**kwargs)
    if action_type == MemoryGovernanceActionType.quarantine:
        kwargs.pop("corrected_statement", None)
        return service.quarantine_memory(**kwargs)
    kwargs.pop("corrected_statement", None)
    return service.release_memory_from_quarantine(**kwargs)


@router.post("/usage/validate", response_model=MemoryUsagePolicyDecision)
def validate_memory_usage(
    request: MemoryUsageValidationRequest,
    service: MemoryGovernanceService = Depends(get_memory_governance_service),
) -> MemoryUsagePolicyDecision:
    return service.validate_memory_usage(**request.model_dump())
