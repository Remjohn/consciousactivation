"""FastAPI Router for Release, Ship, Outcome and Selective Learning Runtime Operations."""

from __future__ import annotations

import logging
from typing import Any, Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from api.schemas.release_ship import (
    AuthorizeReleaseInput,
    CaptureOutcomeInput,
    CreateReleaseSessionInput,
    ExecuteShipInput,
    ProposeLearningInput,
    RatifyProposalInput,
    ReleaseSessionResponse,
    VerifyFinalQAInput,
)
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_state_runtime import UniversalProgramStateRuntime
from ca_runtime.release_ship_outcome_program import (
    AntiRewardHackingViolationError,
    EvidenceIntegrityViolationError,
    IncompleteQAError,
    InvalidStateTransitionError,
    LaneAuthorityViolationError,
    MissingEvidenceLineageError,
    OntologyMutationViolationError,
    OperatorAuthorizationRequiredError,
    ReleaseShipOutcomeCoordinator,
    ReleaseShipProgramError,
    RenderQAFailureError,
    SemanticQAFailureError,
    ShipmentExecutionFailureError,
    SyntheticProductionBlockedError,
    WorkspaceScopeViolationError,
)

logger = logging.getLogger("conscious_activations.api.release_ship")

router = APIRouter()

# Global runtime coordinator
_runtime = UniversalProgramStateRuntime()


def get_coordinator() -> ReleaseShipOutcomeCoordinator:
    return ReleaseShipOutcomeCoordinator(runtime=_runtime)


@router.post("/sessions/create", response_model=ReleaseSessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    payload: CreateReleaseSessionInput,
    coordinator: ReleaseShipOutcomeCoordinator = Depends(get_coordinator),
) -> ReleaseSessionResponse:
    """Initializes a new release/ship/outcome session aggregate."""
    try:
        aggregate = coordinator.initialize_session(
            candidate_id=payload.candidate_id,
            workspace_id=payload.workspace_id,
            actor_id=payload.actor_id,
            artifact_ref=payload.artifact_ref,
        )
        return ReleaseSessionResponse(
            aggregate_id=str(aggregate.aggregate_id),
            program_id=aggregate.program_id,
            workspace_id=str(aggregate.workspace_id),
            current_state=aggregate.current_state,
            state_data=aggregate.state_data,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/qa/verify", status_code=status.HTTP_200_OK)
def verify_qa(
    payload: VerifyFinalQAInput,
    coordinator: ReleaseShipOutcomeCoordinator = Depends(get_coordinator),
) -> Dict[str, Any]:
    """Verifies Dual-Axis QA results under ANALYST lane."""
    try:
        record = coordinator.verify_final_qa(
            aggregate_id=payload.aggregate_id,
            actor_id=payload.actor_id,
            actor_lane=AuthorityLane(payload.actor_lane),
            semantic_qa_result=payload.semantic_qa_result,
            render_qa_result=payload.render_qa_result,
            evidence_segment=payload.evidence_segment,
            wrong_reading_locks=payload.wrong_reading_locks,
            is_synthetic=payload.is_synthetic,
        )
        return {"status": "QA_VERIFIED", "qa_record": record.to_dict()}
    except SyntheticProductionBlockedError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Synthetic production blocked: {str(e)}")
    except (MissingEvidenceLineageError, IncompleteQAError) as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except EvidenceIntegrityViolationError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except (SemanticQAFailureError, RenderQAFailureError) as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except (LaneAuthorityViolationError, WorkspaceScopeViolationError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ReleaseShipProgramError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/authorize", status_code=status.HTTP_200_OK)
def authorize_release(
    payload: AuthorizeReleaseInput,
    coordinator: ReleaseShipOutcomeCoordinator = Depends(get_coordinator),
) -> Dict[str, Any]:
    """Grants backend-authoritative operator release authorization under COMMANDER lane."""
    try:
        auth = coordinator.authorize_release(
            aggregate_id=payload.aggregate_id,
            operator_id=payload.operator_id,
            actor_lane=AuthorityLane(payload.actor_lane),
            decision=payload.decision,
            target_channels=payload.target_channels,
            rationale=payload.rationale,
            release_manifest_sha256=payload.release_manifest_sha256,
        )
        return {"status": "RELEASE_AUTHORIZED", "authorization": auth.to_dict()}
    except OperatorAuthorizationRequiredError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except (LaneAuthorityViolationError, WorkspaceScopeViolationError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ReleaseShipProgramError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/ship", status_code=status.HTTP_200_OK)
def execute_ship(
    payload: ExecuteShipInput,
    coordinator: ReleaseShipOutcomeCoordinator = Depends(get_coordinator),
) -> Dict[str, Any]:
    """Executes physical or distribution shipment under COMPOSER lane."""
    try:
        receipt = coordinator.execute_ship(
            aggregate_id=payload.aggregate_id,
            actor_id=payload.actor_id,
            actor_lane=AuthorityLane(payload.actor_lane),
            target_channel=payload.target_channel,
            delivery_endpoint=payload.delivery_endpoint,
            simulate_channel_failure=payload.simulate_channel_failure,
        )
        return {"status": "SHIPPED", "shipment_receipt": receipt.to_dict()}
    except ShipmentExecutionFailureError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Shipment execution failed: {str(e)}")
    except OperatorAuthorizationRequiredError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except (LaneAuthorityViolationError, WorkspaceScopeViolationError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ReleaseShipProgramError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/outcomes/capture", status_code=status.HTTP_200_OK)
def capture_outcome(
    payload: CaptureOutcomeInput,
    coordinator: ReleaseShipOutcomeCoordinator = Depends(get_coordinator),
) -> Dict[str, Any]:
    """Captures empirical real-world outcome metrics under HUNTER lane."""
    try:
        outcome, receipt, obs_record = coordinator.capture_outcome(
            aggregate_id=payload.aggregate_id,
            actor_id=payload.actor_id,
            actor_lane=AuthorityLane(payload.actor_lane),
            domain=payload.domain,
            metrics=payload.metrics,
            predicted_composite_score=payload.predicted_composite_score,
            observed_normalized_score=payload.observed_normalized_score,
            evaluator_scores=payload.evaluator_scores,
            is_grounded=payload.is_grounded,
            misleading_context=payload.misleading_context,
            notes=payload.notes,
        )
        return {
            "status": "OUTCOME_CAPTURED",
            "outcome": outcome.model_dump(mode="json"),
            "receipt": receipt.model_dump(mode="json"),
            "observation_record": obs_record.to_dict(),
        }
    except AntiRewardHackingViolationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Anti-reward-hack blocked: {str(e)}")
    except (LaneAuthorityViolationError, WorkspaceScopeViolationError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ReleaseShipProgramError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/learning/propose", status_code=status.HTTP_200_OK)
def propose_learning(
    payload: ProposeLearningInput,
    coordinator: ReleaseShipOutcomeCoordinator = Depends(get_coordinator),
) -> Dict[str, Any]:
    """Generates advisory selective learning proposals under ANALYST lane."""
    try:
        proposals = coordinator.propose_learning(
            aggregate_id=payload.aggregate_id,
            actor_id=payload.actor_id,
            actor_lane=AuthorityLane(payload.actor_lane),
            min_recurrence=payload.min_recurrence,
        )
        return {
            "status": "LEARNING_PROPOSED",
            "proposals": [p.model_dump(mode="json") for p in proposals],
        }
    except (LaneAuthorityViolationError, WorkspaceScopeViolationError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ReleaseShipProgramError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/learning/ratify", status_code=status.HTTP_200_OK)
def ratify_proposal(
    payload: RatifyProposalInput,
    coordinator: ReleaseShipOutcomeCoordinator = Depends(get_coordinator),
) -> Dict[str, Any]:
    """Operator ratifies an advisory learning proposal under COMMANDER lane."""
    try:
        record = coordinator.ratify_learning_proposal(
            aggregate_id=payload.aggregate_id,
            operator_id=payload.operator_id,
            actor_lane=AuthorityLane(payload.actor_lane),
            proposal_id=payload.proposal_id,
            decision=payload.decision,
        )
        return {"status": "RATIFIED", "record": record}
    except (LaneAuthorityViolationError, WorkspaceScopeViolationError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ReleaseShipProgramError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/status", status_code=status.HTTP_200_OK)
def get_release_status(
    coordinator: ReleaseShipOutcomeCoordinator = Depends(get_coordinator),
) -> Dict[str, Any]:
    """Returns release, ship, outcome runtime health and state machine status."""
    return {
        "status": "READY",
        "program_id": "release_ship_outcome_program",
        "state_machine": "RELEASE_SHIP_OUTCOME_STATE_MACHINE_V1",
        "supported_lanes": ["COMMANDER", "HUNTER", "COMPOSER", "ANALYST"],
    }


@router.get("/aggregates/{aggregate_id}", response_model=ReleaseSessionResponse)
def get_aggregate(
    aggregate_id: str,
    coordinator: ReleaseShipOutcomeCoordinator = Depends(get_coordinator),
) -> ReleaseSessionResponse:
    """Fetches full state aggregate by aggregate_id."""
    try:
        aggregate = coordinator.runtime.get_aggregate(aggregate_id)
        return ReleaseSessionResponse(
            aggregate_id=str(aggregate.aggregate_id),
            program_id=aggregate.program_id,
            workspace_id=str(aggregate.workspace_id),
            current_state=aggregate.current_state,
            state_data=aggregate.state_data,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aggregate {aggregate_id} not found: {str(e)}")
