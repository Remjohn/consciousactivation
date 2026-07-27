"""FastAPI orchestration route adapter for TS-CMF-002."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.orchestration import (
    ActiveObjectRef,
    AgentHandoffPacket,
    OrchestrationRun,
    StageExecutionPlan,
    ValidationContract,
)
from ccp_studio.services.orchestration import OrchestrationService
from ccp_studio.workflows.orchestration_run import OrchestrationRunWorkflow, PreparedStage


class PrepareStageRequest(BaseModel):
    organization_id: str
    brand_id: str
    actor_id: str
    active_object: ActiveObjectRef
    requested_outcome: str
    pipeline_stage: str
    expected_exit_object_type: str
    allowed_actor_or_service: str
    required_inputs: list[str]
    allowed_actions: list[str]
    blocked_actions: list[str]
    downstream_proof_obligation: str
    success_criteria: list[str]
    failure_criteria: list[str]
    required_receipt_types: list[str]
    required_evidence_refs: list[str]
    source_evidence_refs: list[str]
    upstream_receipt_ids: list[str]


class PrepareStageResponse(BaseModel):
    run: OrchestrationRun
    plan: StageExecutionPlan
    validation_contract: ValidationContract
    handoff_packet: AgentHandoffPacket


router = APIRouter(prefix="/api/v1/orchestration", tags=["orchestration"])
_orchestration_service = OrchestrationService()


def set_orchestration_service(service: OrchestrationService) -> None:
    global _orchestration_service
    _orchestration_service = service


def get_orchestration_service() -> OrchestrationService:
    return _orchestration_service


@router.post("/prepare-stage", response_model=PrepareStageResponse)
async def prepare_stage(
    request: PrepareStageRequest,
    service: OrchestrationService = Depends(get_orchestration_service),
) -> PrepareStageResponse:
    from uuid import UUID

    prepared: PreparedStage = OrchestrationRunWorkflow(service).prepare_stage(
        organization_id=UUID(request.organization_id),
        brand_id=UUID(request.brand_id),
        actor_id=UUID(request.actor_id),
        active_object=request.active_object,
        requested_outcome=request.requested_outcome,
        pipeline_stage=request.pipeline_stage,
        expected_exit_object_type=request.expected_exit_object_type,
        allowed_actor_or_service=request.allowed_actor_or_service,
        required_inputs=request.required_inputs,
        allowed_actions=request.allowed_actions,
        blocked_actions=request.blocked_actions,
        downstream_proof_obligation=request.downstream_proof_obligation,
        success_criteria=request.success_criteria,
        failure_criteria=request.failure_criteria,
        required_receipt_types=request.required_receipt_types,
        required_evidence_refs=request.required_evidence_refs,
        source_evidence_refs=request.source_evidence_refs,
        upstream_receipt_ids=[UUID(item) for item in request.upstream_receipt_ids],
    )
    return PrepareStageResponse(
        run=prepared.run,
        plan=prepared.plan,
        validation_contract=prepared.validation_contract,
        handoff_packet=prepared.handoff_packet,
    )
