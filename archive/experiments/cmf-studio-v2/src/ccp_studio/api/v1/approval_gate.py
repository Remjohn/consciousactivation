"""FastAPI adapter for TS-CMF-053 approval blockers."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.approval_gate import ApprovalBlockerReceipt, ApprovalPolicyReport, ContentFormatValidation
from ccp_studio.services.approval_gate_service import ApprovalGateService


router = APIRouter(prefix="/api/v1/approval-gate", tags=["approval-gate"])
_approval_gate_service: ApprovalGateService | None = None


class ApprovalGateRequest(BaseModel):
    gate_input: dict[str, Any]


class ContentFormatRequest(BaseModel):
    platform_variant_id: str
    format_key: str
    registry_version_id: str
    valid_content_formats: list[str] = Field(default_factory=list)


class ClearBlockerRequest(BaseModel):
    approval_blocker_receipt_id: UUID
    blocker_id: UUID
    actor_id: UUID
    evidence_refs: list[str] = Field(default_factory=list)


def set_approval_gate_service(service: ApprovalGateService) -> None:
    global _approval_gate_service
    _approval_gate_service = service


def get_approval_gate_service() -> ApprovalGateService:
    if _approval_gate_service is None:
        raise RuntimeError("ApprovalGateService must be configured by the application.")
    return _approval_gate_service


@router.post("/evaluate", response_model=ApprovalPolicyReport)
def evaluate_approval_gate(
    request: ApprovalGateRequest,
    service: ApprovalGateService = Depends(get_approval_gate_service),
) -> ApprovalPolicyReport:
    return service.evaluate_approval_gate(request.gate_input)


@router.post("/content-format", response_model=ContentFormatValidation)
def validate_content_format(
    request: ContentFormatRequest,
    service: ApprovalGateService = Depends(get_approval_gate_service),
) -> ContentFormatValidation:
    return service.validate_content_format(**request.model_dump())


@router.post("/clear-blocker", response_model=ApprovalBlockerReceipt)
def clear_approval_blocker(
    request: ClearBlockerRequest,
    service: ApprovalGateService = Depends(get_approval_gate_service),
) -> ApprovalBlockerReceipt:
    return service.clear_approval_blocker(**request.model_dump())

