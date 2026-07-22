"""FastAPI adapter for TS-CMF-060 workflow recovery."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.workflow_recovery import RecoveryValidationReport, WorkflowRecoveryActionType, WorkflowRecoveryReceipt
from ccp_studio.services.workflow_recovery_service import WorkflowRecoveryService


router = APIRouter(prefix="/api/v1/operations/recovery", tags=["workflow-recovery"])
_workflow_recovery_service: WorkflowRecoveryService | None = None


class BuildRecoveryValidationReportRequest(BaseModel):
    workflow_id: str
    failed_object_ref: str
    completed_artifact_refs: list[str] = Field(default_factory=list)
    receipt_refs: list[str] = Field(default_factory=list)
    consent_compatible: bool
    publishing_side_effect_risk: bool = False
    memory_side_effect_risk: bool = False
    provider_cost_risk: bool = False
    severity: str = "medium"
    summary: str | None = None


class ApplyRecoveryActionRequest(BaseModel):
    incident_id: UUID
    action_type: WorkflowRecoveryActionType
    requested_by_user_id: UUID
    role_ids: list[str] = Field(default_factory=list)
    reason: str
    idempotency_key: str


def set_workflow_recovery_service(service: WorkflowRecoveryService) -> None:
    global _workflow_recovery_service
    _workflow_recovery_service = service


def get_workflow_recovery_service() -> WorkflowRecoveryService:
    if _workflow_recovery_service is None:
        raise RuntimeError("WorkflowRecoveryService must be configured by the application.")
    return _workflow_recovery_service


@router.post("/validation-reports", response_model=RecoveryValidationReport)
def build_recovery_validation_report(
    request: BuildRecoveryValidationReportRequest,
    service: WorkflowRecoveryService = Depends(get_workflow_recovery_service),
) -> RecoveryValidationReport:
    return service.build_recovery_validation_report(**request.model_dump())


@router.post("/actions", response_model=WorkflowRecoveryReceipt)
def apply_recovery_action(
    request: ApplyRecoveryActionRequest,
    service: WorkflowRecoveryService = Depends(get_workflow_recovery_service),
) -> WorkflowRecoveryReceipt:
    return service.apply_recovery_action(**request.model_dump())
