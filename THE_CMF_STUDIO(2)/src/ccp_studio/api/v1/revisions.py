"""FastAPI adapter for TS-CMF-040 revisions and reconstruction."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.revision import FinalApprovalBinding, ReconstructionAuditView, RevisionRequest
from ccp_studio.services.revision_service import RevisionService


router = APIRouter(prefix="/api/v1/revisions", tags=["revisions"])
_revision_service: RevisionService | None = None


class RequestRevisionRequest(BaseModel):
    complete_editing_session_id: UUID
    actor_id: UUID
    reason: str
    target_object_type: str
    target_object_id: UUID
    deltas: list[dict[str, Any]]
    prior_version_id: UUID
    evaluation_state: str = "reviewed_for_revision"
    evaluation_receipt_ids: list[UUID] = []


class ApproveFinalVersionRequest(BaseModel):
    complete_editing_session_id: UUID
    final_version_id: UUID
    actor_id: UUID
    human_decision_ref: str


def set_revision_service(service: RevisionService) -> None:
    global _revision_service
    _revision_service = service


def get_revision_service() -> RevisionService:
    if _revision_service is None:
        raise RuntimeError("RevisionService must be configured by the application.")
    return _revision_service


@router.post("", response_model=RevisionRequest)
def request_revision(
    request: RequestRevisionRequest,
    service: RevisionService = Depends(get_revision_service),
) -> RevisionRequest:
    return service.request_scene_revision(
        complete_editing_session_id=request.complete_editing_session_id,
        requested_by_user_id=request.actor_id,
        reason=request.reason,
        target_object_type=request.target_object_type,
        target_object_id=request.target_object_id,
        deltas=request.deltas,
        prior_version_id=request.prior_version_id,
        evaluation_state=request.evaluation_state,
        evaluation_receipt_ids=request.evaluation_receipt_ids,
    )


@router.post("/approve", response_model=FinalApprovalBinding)
def approve_final_version(
    request: ApproveFinalVersionRequest,
    service: RevisionService = Depends(get_revision_service),
) -> FinalApprovalBinding:
    return service.approve_final_version(
        complete_editing_session_id=request.complete_editing_session_id,
        final_version_id=request.final_version_id,
        approved_by_actor_id=request.actor_id,
        human_decision_ref=request.human_decision_ref,
    )


@router.get("/sessions/{complete_editing_session_id}/audit", response_model=ReconstructionAuditView)
def reconstruction_audit(
    complete_editing_session_id: UUID,
    service: RevisionService = Depends(get_revision_service),
) -> ReconstructionAuditView:
    return service.build_reconstruction_audit_view(complete_editing_session_id=complete_editing_session_id)
