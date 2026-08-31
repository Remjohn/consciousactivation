"""FastAPI Router for Visual Asset Editor (VAE) Delegation and Runtime Operations."""

from __future__ import annotations

import logging
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.dependencies import get_pipeline, get_vae
from api.schemas.vae import (
    VAEAdmissionRequest,
    VAEAdmissionResponse,
    VAEJobExecutionRequest,
    VAEJobExecutionResponse,
    VAEResultAcknowledgementRequest,
    VAEResultAcknowledgementResponse,
    VAEStatusResponse,
)
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_state_runtime import UniversalProgramStateRuntime
from ca_runtime.vae_delegation_program import (
    BoundedRepairExceededError,
    ConsumptionAuthorityViolationError,
    DualAxisQAViolationError,
    EvidenceHashMismatchError,
    LaneAuthorityViolationError,
    SourceLineageMissingError,
    SyntheticProductionBlockedError,
    VAEDelegationCoordinator,
    VAEDelegationProgramError,
    WorkspaceScopeViolationError,
    WrongReadingLockMissingError,
)

logger = logging.getLogger("conscious_activations.api.vae")

router = APIRouter()

# Shared runtime coordinator singleton
_runtime = UniversalProgramStateRuntime()


def get_coordinator(request: Request) -> VAEDelegationCoordinator:
    vae_app = getattr(request.app.state, "vae", None)
    pipeline_app = getattr(request.app.state, "pipeline", None)
    delegation_svc = getattr(pipeline_app, "visual_delegation", None) if pipeline_app else None
    return VAEDelegationCoordinator(runtime=_runtime, vae_app=vae_app, delegation_service=delegation_svc)


@router.post("/demands/admit", response_model=VAEAdmissionResponse, status_code=status.HTTP_201_CREATED)
def admit_demand(
    payload: VAEAdmissionRequest,
    coordinator: VAEDelegationCoordinator = Depends(get_coordinator),
) -> VAEAdmissionResponse:
    """Admits a visual asset demand into the governed VAE delegation runtime (COMMANDER Lane)."""
    try:
        aggregate = coordinator.admit_demand(
            workspace_id=payload.workspace_id,
            program_id=payload.program_id,
            demand_payload=payload.demand_payload,
            operator_id=payload.operator_id,
            lane=AuthorityLane.COMMANDER,
        )
        demand_rec = aggregate.state_data["demand"]
        return VAEAdmissionResponse(
            status="ADMITTED",
            aggregate_id=aggregate.aggregate_id,
            request_id=demand_rec["request_id"],
            demand_hash=demand_rec["demand_hash"],
            scene_index=demand_rec["scene_index"],
            admitted_at=demand_rec["created_at"],
        )
    except SyntheticProductionBlockedError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Synthetic demand blocked: {str(e)}")
    except WrongReadingLockMissingError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Wrong-reading lock missing: {str(e)}")
    except SourceLineageMissingError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Source lineage missing: {str(e)}")
    except EvidenceHashMismatchError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Evidence hash mismatch: {str(e)}")
    except (WorkspaceScopeViolationError, LaneAuthorityViolationError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except VAEDelegationProgramError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/jobs/execute", response_model=VAEJobExecutionResponse)
def execute_job(
    payload: VAEJobExecutionRequest,
    coordinator: VAEDelegationCoordinator = Depends(get_coordinator),
) -> VAEJobExecutionResponse:
    """Executes production planning (HUNTER), generation (COMPOSER), and technical QA (ANALYST)."""
    try:
        # Phase 1: Compile Plan (HUNTER)
        agg_plan = coordinator.compile_production_plan(
            aggregate_id=payload.aggregate_id,
            producer_actor_id=payload.producer_actor_id or payload.worker_id,
            evaluator_actor_id=payload.evaluator_actor_id or payload.worker_id,
            lane=AuthorityLane.HUNTER,
        )

        # Phase 2: Generate Asset (COMPOSER)
        agg_gen = coordinator.generate_visual_asset(
            aggregate_id=agg_plan.aggregate_id,
            worker_id=payload.worker_id,
            lane=AuthorityLane.COMPOSER,
        )

        # Phase 3: Evaluate Technical Quality (ANALYST)
        agg_eval = coordinator.evaluate_technical_quality(
            aggregate_id=agg_gen.aggregate_id,
            evaluator_actor_id=payload.evaluator_actor_id or payload.worker_id,
            force_render_fail=payload.force_render_fail,
            semantic_qa_result=payload.semantic_qa,
            lane=AuthorityLane.ANALYST,
        )

        plan_rec = agg_eval.state_data["production_plan"]
        art_rec = agg_eval.state_data["artifact"]
        tech_rec = agg_eval.state_data["technical_evaluation"]

        return VAEJobExecutionResponse(
            status="EXECUTED",
            aggregate_id=agg_eval.aggregate_id,
            plan_id=plan_rec["plan_id"],
            artifact_id=art_rec["artifact_id"],
            candidate_uri=art_rec["candidate_uri"],
            mask_uri=art_rec.get("segmentation_mask_uri"),
            cutout_uri=art_rec.get("matting_cutout_uri"),
            gnm_uri=art_rec.get("gnm_reference_uri"),
            technical_verdict=tech_rec["hard_gate_result"],
            evaluated_at=tech_rec["evaluated_at"],
        )
    except (WorkspaceScopeViolationError, LaneAuthorityViolationError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except VAEDelegationProgramError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/results/acknowledge", response_model=VAEResultAcknowledgementResponse)
def acknowledge_result(
    payload: VAEResultAcknowledgementRequest,
    coordinator: VAEDelegationCoordinator = Depends(get_coordinator),
) -> VAEResultAcknowledgementResponse:
    """Issues authoritative Pipeline acknowledgement with consumption authorization (COMMANDER Lane)."""
    try:
        aggregate, receipt = coordinator.acknowledge_result(
            aggregate_id=payload.aggregate_id,
            operator_id=payload.operator_id,
            decision=payload.decision,
            consumption_authorized=payload.consumption_authorized,
            lane=AuthorityLane.COMMANDER,
        )
        return VAEResultAcknowledgementResponse(
            status="ACKNOWLEDGED",
            aggregate_id=aggregate.aggregate_id,
            acknowledgement_id=receipt.acknowledgement_id,
            receipt_id=receipt.receipt_id,
            receipt_sha256=receipt.receipt_sha256,
            consumption_authorized=receipt.consumption_authorized,
            decision=receipt.decision,
            acknowledged_at=receipt.approved_at,
        )
    except ConsumptionAuthorityViolationError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Consumption authority violation: {str(e)}")
    except DualAxisQAViolationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Dual-axis QA violation: {str(e)}")
    except (WorkspaceScopeViolationError, LaneAuthorityViolationError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except VAEDelegationProgramError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/status", response_model=VAEStatusResponse)
def get_status(request: Request) -> VAEStatusResponse:
    """Returns VAE service health and delegation runtime configuration."""
    vae_app = getattr(request.app.state, "vae", None)
    if vae_app is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="VAE service not initialized")
    stat = vae_app.status()
    storage_root = str(getattr(vae_app, "storage_root", getattr(vae_app.store, "root", "")))
    delegation_root = str(getattr(vae_app, "delegation_root", getattr(vae_app.contracts, "root", "")))
    return VAEStatusResponse(
        status="OPERATIONAL",
        lifecycle_state=stat.get("lifecycle_state", "active"),
        storage_root=storage_root,
        delegation_root=delegation_root,
        contracts_version="1.1.0-rc.4",
        repository=stat.get("repository", {}),
    )


@router.get("/aggregates/{aggregate_id}", response_model=Dict[str, Any])
def get_aggregate(
    aggregate_id: str,
    coordinator: VAEDelegationCoordinator = Depends(get_coordinator),
) -> Dict[str, Any]:
    """Inspects the active state aggregate and transition ledger for a delegation session."""
    try:
        agg = coordinator.runtime.get_aggregate(aggregate_id)
        return {
            "aggregate_id": agg.aggregate_id,
            "program_id": agg.program_id,
            "current_state": agg.current_state,
            "version": agg.version,
            "workspace_id": agg.workspace_id,
            "created_at": agg.created_at,
            "updated_at": agg.updated_at,
            "state_data": agg.state_data,
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aggregate '{aggregate_id}' not found: {str(e)}")
