"""TS-CAE-PROG-001 & M46 -- Governed Program Registry, Discovery, and Operator Application API.

Endpoints:
- Discovery:
  - GET /api/programs: List registered program packages with SHA-256 fingerprints
  - GET /api/programs/{program_id}: Detailed inspection of program package, authority lanes, and skills
  - POST /api/programs/{program_id}/preflight: Fail-closed preflight validation for tenant session
- Executions:
  - GET /api/programs/executions: List program execution aggregates with filtering
  - POST /api/programs/executions: Instantiate and run a program
  - GET /api/programs/executions/{aggregate_id}: Inspect single execution aggregate & context
  - POST /api/programs/executions/{aggregate_id}/pause: Safely pause running program (CAS-protected)
  - POST /api/programs/executions/{aggregate_id}/resume: Resume paused program (CAS-protected)
  - POST /api/programs/executions/{aggregate_id}/approve: Authorize human gate (CAS-protected, COMMANDER lane)
  - POST /api/programs/executions/{aggregate_id}/reject: Reject milestone with disposition routing (CAS-protected)
  - POST /api/programs/executions/{aggregate_id}/repair: Governed state repair / direct manipulation
- Lineage & Trace Projections:
  - GET /api/programs/executions/{aggregate_id}/lineage: Full cryptographic artifact lineage graph
  - GET /api/programs/executions/{aggregate_id}/trace: Execution trace DAG and transition audit
- Chat Supervision Grammar:
  - POST /api/programs/operator/chat: Direct dispatch of operator chat commands to authoritative backend
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from pathlib import Path

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response, status
from pydantic import BaseModel, Field

from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_registry import (
    ProgramNotFoundError,
    ProgramPackage,
    ProgramPreflightResult,
    ProgramRegistry,
    ProgramStatus,
    get_program_registry,
)
from ca_runtime.program_state_runtime import (
    ProgramAuthorityLaneViolationError,
    ProgramStateAggregate,
    ProgramStateAggregateNotFoundError,
    ProgramStateLifecycle,
    ProgramStateVersionConflictError,
    ProgramTransitionBlockedError,
)
from ca_runtime.program_operator_runtime import (
    ArtifactLineageGraph,
    ExecutionTraceProjection,
    ProgramOperatorRuntimeService,
    RejectionDispositionRoute,
)
from api.schemas.operator import (
    ApproveGateRequest,
    ArtifactLineageGraphResponse,
    ChatCommandRequest,
    ChatCommandResponse,
    ExecutionTraceProjectionResponse,
    PauseExecutionRequest,
    ProgramExecutionDetailResponse,
    ProgramExecutionListResponse,
    ProgramExecutionSummaryResponse,
    RejectGateRequest,
    RepairExecutionRequest,
    ResumeExecutionRequest,
    RunProgramRequest,
)

logger = logging.getLogger("conscious_activations.api.programs")

router = APIRouter()


class ProgramSummaryResponse(BaseModel):
    program_id: str
    version: str
    status: str
    purpose: str
    lanes: List[str]
    manifest_sha256: str
    package_sha256: str
    skills_count: int
    operations_count: int


class ProgramListResponse(BaseModel):
    programs: List[ProgramSummaryResponse]
    total: int


class PreflightRequest(BaseModel):
    workspace_id: str = Field(..., min_length=1)
    context_refs: List[str] = Field(default_factory=list)
    version: Optional[str] = Field(default=None)


_default_operator_service: Optional[ProgramOperatorRuntimeService] = None


def get_registry() -> ProgramRegistry:
    return get_program_registry()


def get_operator_service() -> ProgramOperatorRuntimeService:
    global _default_operator_service
    if _default_operator_service is None:
        _default_operator_service = ProgramOperatorRuntimeService(
            program_registry=get_program_registry()
        )
    return _default_operator_service


def _set_state_headers(response: Response, agg: ProgramStateAggregate) -> None:
    """Sets standard CAE anti-stale concurrency headers."""
    response.headers["X-CAE-State-Version"] = str(agg.version)
    response.headers["X-CAE-State-SHA256"] = agg.state_hash
    response.headers["X-CAE-Updated-At"] = agg.updated_at


def _resolve_cas_headers(
    req_version: Optional[int],
    req_sha256: Optional[str],
    header_version: Optional[str],
    header_sha256: Optional[str],
) -> tuple[Optional[int], Optional[str]]:
    """Resolves version and hash from either request body or HTTP If-Match headers."""
    eff_version = req_version
    if eff_version is None and header_version is not None:
        try:
            eff_version = int(header_version.strip('"'))
        except ValueError:
            pass

    eff_sha256 = req_sha256
    if eff_sha256 is None and header_sha256 is not None:
        eff_sha256 = header_sha256.strip('"')

    return eff_version, eff_sha256


# ============================================================================
# 1. Program Discovery & Inspection
# ============================================================================

@router.get("", response_model=ProgramListResponse)
def list_programs(
    status_filter: Optional[ProgramStatus] = Query(default=None, alias="status", description="Filter by program status"),
    registry: ProgramRegistry = Depends(get_registry),
) -> ProgramListResponse:
    """Lists all registered program packages."""
    pkgs = registry.list_programs(status=status_filter)
    summaries = [
        ProgramSummaryResponse(
            program_id=pkg.program_id,
            version=pkg.version,
            status=pkg.manifest.status.value,
            purpose=pkg.manifest.purpose,
            lanes=pkg.manifest.lanes,
            manifest_sha256=pkg.manifest_sha256,
            package_sha256=pkg.package_sha256,
            skills_count=len(pkg.manifest.skills),
            operations_count=len(pkg.manifest.operations),
        )
        for pkg in pkgs
    ]
    return ProgramListResponse(programs=summaries, total=len(summaries))


# ============================================================================
# 2. Execution Aggregates Management
# ============================================================================

@router.get("/executions", response_model=ProgramExecutionListResponse)
def list_executions(
    workspace_id: Optional[str] = Query(default=None),
    program_id: Optional[str] = Query(default=None),
    lifecycle: Optional[ProgramStateLifecycle] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    service: ProgramOperatorRuntimeService = Depends(get_operator_service),
) -> ProgramExecutionListResponse:
    """Lists execution aggregates with filtering by workspace, program, and lifecycle."""
    aggregates, total = service.list_executions(
        workspace_id=workspace_id,
        program_id=program_id,
        lifecycle=lifecycle,
        limit=limit,
        offset=offset,
    )
    summaries = [
        ProgramExecutionSummaryResponse(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            lifecycle=agg.lifecycle.value,
            current_state=agg.current_state,
            version=agg.version,
            state_hash=agg.state_hash,
            last_receipt_id=agg.last_receipt_id,
            created_at=agg.created_at,
            updated_at=agg.updated_at,
        )
        for agg in aggregates
    ]
    return ProgramExecutionListResponse(executions=summaries, total=total)


@router.post("/executions", response_model=ProgramExecutionSummaryResponse, status_code=status.HTTP_201_CREATED)
def run_program(
    request: RunProgramRequest,
    response: Response,
    service: ProgramOperatorRuntimeService = Depends(get_operator_service),
) -> ProgramExecutionSummaryResponse:
    """Instantiates and starts a Program execution under COMMANDER authorization."""
    try:
        agg = service.run_program(
            program_id=request.program_id,
            workspace_id=request.workspace_id,
            actor_id=request.actor_id,
            initial_data=request.initial_data,
            context_claims=request.context_claims,
        )
        _set_state_headers(response, agg)
        return ProgramExecutionSummaryResponse(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            lifecycle=agg.lifecycle.value,
            current_state=agg.current_state,
            version=agg.version,
            state_hash=agg.state_hash,
            last_receipt_id=agg.last_receipt_id,
            created_at=agg.created_at,
            updated_at=agg.updated_at,
        )
    except ProgramTransitionBlockedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "TRANSITION_BLOCKED", "message": str(e), "details": e.details},
        )
    except ProgramAuthorityLaneViolationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error_code": "AUTHORITY_LANE_VIOLATION", "message": str(e)},
        )
    except Exception as e:
        logger.exception("Failed to run program")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "RUN_FAILED", "message": str(e)},
        )


@router.get("/executions/{aggregate_id:path}/lineage", response_model=ArtifactLineageGraphResponse)
def get_artifact_lineage(
    aggregate_id: str,
    artifact_id: Optional[str] = Query(default=None),
    service: ProgramOperatorRuntimeService = Depends(get_operator_service),
) -> ArtifactLineageGraphResponse:
    """Retrieves the lossless cryptographic asset lineage graph for an execution."""
    try:
        graph = service.project_artifact_lineage(aggregate_id=aggregate_id, artifact_id=artifact_id)
        return ArtifactLineageGraphResponse(
            aggregate_id=graph.aggregate_id,
            artifact_id=graph.artifact_id,
            is_lossless=graph.is_lossless,
            verification_status=graph.verification_status.value,
            nodes=[
                {
                    "node_id": n.node_id,
                    "node_type": n.node_type.value,
                    "label": n.label,
                    "sha256": n.sha256,
                    "lane": n.lane.value,
                    "receipt_ref": n.receipt_ref,
                    "timestamp": n.timestamp,
                    "metadata": n.metadata,
                }
                for n in graph.nodes
            ],
            edges=[
                {
                    "edge_id": e.edge_id,
                    "source_node_id": e.source_node_id,
                    "target_node_id": e.target_node_id,
                    "transformation_op": e.transformation_op,
                    "lane": e.lane.value,
                    "receipt_ref": e.receipt_ref,
                    "metadata": e.metadata,
                }
                for e in graph.edges
            ],
            root_evidence_ids=graph.root_evidence_ids,
            terminal_artifact_ids=graph.terminal_artifact_ids,
            verification_digest=graph.verification_digest,
        )
    except ProgramStateAggregateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Execution aggregate '{aggregate_id}' not found"},
        )


@router.get("/executions/{aggregate_id:path}/trace", response_model=ExecutionTraceProjectionResponse)
def get_execution_trace(
    aggregate_id: str,
    service: ProgramOperatorRuntimeService = Depends(get_operator_service),
) -> ExecutionTraceProjectionResponse:
    """Retrieves the execution trace DAG, transition audit ledger, and blockers."""
    try:
        trace = service.project_execution_trace(aggregate_id=aggregate_id)
        return ExecutionTraceProjectionResponse(
            aggregate_id=trace.aggregate_id,
            workspace_id=trace.workspace_id,
            program_id=trace.program_id,
            program_version=trace.program_version,
            lifecycle=trace.lifecycle.value,
            current_state=trace.current_state,
            version=trace.version,
            state_hash=trace.state_hash,
            last_receipt_id=trace.last_receipt_id,
            created_at=trace.created_at,
            updated_at=trace.updated_at,
            allowable_transitions=trace.allowable_transitions,
            trace_nodes=[
                {
                    "step_index": t.step_index,
                    "transition_id": t.transition_id,
                    "transition_name": t.transition_name,
                    "trigger_operation": t.trigger_operation,
                    "lane": t.lane.value,
                    "actor_id": t.actor_id,
                    "from_state": t.from_state,
                    "to_state": t.to_state,
                    "committed_version": t.committed_version,
                    "receipt_id": t.receipt_id,
                    "timestamp": t.timestamp,
                    "duration_ms": t.duration_ms,
                    "status": t.status,
                    "payload_summary": t.payload_summary,
                }
                for t in trace.trace_nodes
            ],
            blockers=trace.blockers,
        )
    except ProgramStateAggregateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Execution aggregate '{aggregate_id}' not found"},
        )


@router.get("/executions/{aggregate_id:path}", response_model=ProgramExecutionDetailResponse)
def get_execution_details(
    aggregate_id: str,
    active_lane: Optional[AuthorityLane] = Query(default=None),
    response: Response = None,
    service: ProgramOperatorRuntimeService = Depends(get_operator_service),
) -> ProgramExecutionDetailResponse:
    """Inspects a single execution aggregate and its local context."""
    try:
        agg, ctx = service.get_execution(aggregate_id=aggregate_id, active_lane=active_lane)
        if response:
            _set_state_headers(response, agg)

        contracts: Dict[str, Any] = {}
        machine = service.runtime._state_machines.get(agg.program_id)
        if machine:
            for t_name, c in machine.transitions.items():
                contracts[t_name] = {
                    "from_state": c.from_state,
                    "to_state": c.to_state,
                    "required_lane": c.required_lane.value,
                    "trigger_operation": c.trigger_operation,
                    "preconditions": list(c.preconditions),
                    "side_effect_class": c.side_effect_class.value,
                }

        return ProgramExecutionDetailResponse(
            aggregate=ProgramExecutionSummaryResponse(
                aggregate_id=agg.aggregate_id,
                workspace_id=agg.workspace_id,
                program_id=agg.program_id,
                program_version=agg.program_version,
                lifecycle=agg.lifecycle.value,
                current_state=agg.current_state,
                version=agg.version,
                state_hash=agg.state_hash,
                last_receipt_id=agg.last_receipt_id,
                created_at=agg.created_at,
                updated_at=agg.updated_at,
            ),
            state_data=agg.state_data,
            allowable_transitions=ctx.allowable_transitions,
            transition_contracts=contracts,
            active_lane=active_lane.value if active_lane else None,
        )
    except ProgramStateAggregateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Execution aggregate '{aggregate_id}' not found"},
        )


@router.post("/executions/{aggregate_id:path}/pause", response_model=ProgramExecutionSummaryResponse)
def pause_execution(
    aggregate_id: str,
    request: PauseExecutionRequest,
    response: Response,
    if_match_version: Optional[str] = Header(default=None, alias="If-Match-State-Version"),
    if_match_sha256: Optional[str] = Header(default=None, alias="If-Match-State-SHA256"),
    service: ProgramOperatorRuntimeService = Depends(get_operator_service),
) -> ProgramExecutionSummaryResponse:
    """Safely pauses an execution at the current node boundary with CAS protection."""
    exp_version, exp_sha256 = _resolve_cas_headers(
        request.expected_version, request.expected_state_sha256, if_match_version, if_match_sha256
    )
    try:
        agg = service.pause_program(
            aggregate_id=aggregate_id,
            actor_id=request.actor_id,
            expected_version=exp_version,
            expected_state_sha256=exp_sha256,
        )
        _set_state_headers(response, agg)
        return ProgramExecutionSummaryResponse(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            lifecycle=agg.lifecycle.value,
            current_state=agg.current_state,
            version=agg.version,
            state_hash=agg.state_hash,
            last_receipt_id=agg.last_receipt_id,
            created_at=agg.created_at,
            updated_at=agg.updated_at,
        )
    except ProgramStateVersionConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error_code": "STALE_STATE_MUTATION_REJECTED",
                "message": str(e),
                "aggregate_id": e.aggregate_id,
                "expected_version": e.expected_version,
                "actual_version": e.actual_version,
            },
        )
    except ProgramTransitionBlockedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "TRANSITION_BLOCKED", "message": str(e)},
        )
    except ProgramStateAggregateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Execution aggregate '{aggregate_id}' not found"},
        )


@router.post("/executions/{aggregate_id:path}/resume", response_model=ProgramExecutionSummaryResponse)
def resume_execution(
    aggregate_id: str,
    request: ResumeExecutionRequest,
    response: Response,
    if_match_version: Optional[str] = Header(default=None, alias="If-Match-State-Version"),
    if_match_sha256: Optional[str] = Header(default=None, alias="If-Match-State-SHA256"),
    service: ProgramOperatorRuntimeService = Depends(get_operator_service),
) -> ProgramExecutionSummaryResponse:
    """Resumes a paused execution from checkpoint with CAS protection."""
    exp_version, exp_sha256 = _resolve_cas_headers(
        request.expected_version, request.expected_state_sha256, if_match_version, if_match_sha256
    )
    try:
        agg = service.resume_program(
            aggregate_id=aggregate_id,
            actor_id=request.actor_id,
            expected_version=exp_version,
            expected_state_sha256=exp_sha256,
        )
        _set_state_headers(response, agg)
        return ProgramExecutionSummaryResponse(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            lifecycle=agg.lifecycle.value,
            current_state=agg.current_state,
            version=agg.version,
            state_hash=agg.state_hash,
            last_receipt_id=agg.last_receipt_id,
            created_at=agg.created_at,
            updated_at=agg.updated_at,
        )
    except ProgramStateVersionConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error_code": "STALE_STATE_MUTATION_REJECTED",
                "message": str(e),
                "aggregate_id": e.aggregate_id,
                "expected_version": e.expected_version,
                "actual_version": e.actual_version,
            },
        )
    except ProgramTransitionBlockedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "TRANSITION_BLOCKED", "message": str(e)},
        )
    except ProgramStateAggregateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Execution aggregate '{aggregate_id}' not found"},
        )


@router.post("/executions/{aggregate_id:path}/approve", response_model=ProgramExecutionSummaryResponse)
def approve_execution_gate(
    aggregate_id: str,
    request: ApproveGateRequest,
    response: Response,
    if_match_version: Optional[str] = Header(default=None, alias="If-Match-State-Version"),
    if_match_sha256: Optional[str] = Header(default=None, alias="If-Match-State-SHA256"),
    service: ProgramOperatorRuntimeService = Depends(get_operator_service),
) -> ProgramExecutionSummaryResponse:
    """Authorizes human gate milestone with signed receipt under COMMANDER lane."""
    exp_version, exp_sha256 = _resolve_cas_headers(
        request.expected_version, request.expected_state_sha256, if_match_version, if_match_sha256
    )
    try:
        res = service.approve_program(
            aggregate_id=aggregate_id,
            actor_id=request.actor_id,
            gate_id=request.gate_id,
            decision=request.decision,
            expected_version=exp_version,
            expected_state_sha256=exp_sha256,
            payload=request.payload or {"notes": request.notes},
        )
        agg = res.aggregate
        _set_state_headers(response, agg)
        return ProgramExecutionSummaryResponse(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            lifecycle=agg.lifecycle.value,
            current_state=agg.current_state,
            version=agg.version,
            state_hash=agg.state_hash,
            last_receipt_id=agg.last_receipt_id,
            created_at=agg.created_at,
            updated_at=agg.updated_at,
        )
    except ProgramStateVersionConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error_code": "STALE_STATE_MUTATION_REJECTED",
                "message": str(e),
                "aggregate_id": e.aggregate_id,
                "expected_version": e.expected_version,
                "actual_version": e.actual_version,
            },
        )
    except ProgramAuthorityLaneViolationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error_code": "AUTHORITY_LANE_VIOLATION", "message": str(e)},
        )
    except ProgramStateAggregateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Execution aggregate '{aggregate_id}' not found"},
        )


@router.post("/executions/{aggregate_id:path}/reject", response_model=ProgramExecutionSummaryResponse)
def reject_execution_gate(
    aggregate_id: str,
    request: RejectGateRequest,
    response: Response,
    if_match_version: Optional[str] = Header(default=None, alias="If-Match-State-Version"),
    if_match_sha256: Optional[str] = Header(default=None, alias="If-Match-State-SHA256"),
    service: ProgramOperatorRuntimeService = Depends(get_operator_service),
) -> ProgramExecutionSummaryResponse:
    """Authoritatively rejects milestone candidate with typed disposition routing."""
    exp_version, exp_sha256 = _resolve_cas_headers(
        request.expected_version, request.expected_state_sha256, if_match_version, if_match_sha256
    )
    try:
        route = RejectionDispositionRoute(request.disposition_route)
    except ValueError:
        route = RejectionDispositionRoute.RETURN_TO_HUNTER

    try:
        res = service.reject_program(
            aggregate_id=aggregate_id,
            actor_id=request.actor_id,
            rejection_reason=request.rejection_reason,
            disposition_route=route,
            feedback_notes=request.feedback_notes,
            gate_id=request.gate_id,
            expected_version=exp_version,
            expected_state_sha256=exp_sha256,
        )
        agg = res.aggregate
        _set_state_headers(response, agg)
        return ProgramExecutionSummaryResponse(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            lifecycle=agg.lifecycle.value,
            current_state=agg.current_state,
            version=agg.version,
            state_hash=agg.state_hash,
            last_receipt_id=agg.last_receipt_id,
            created_at=agg.created_at,
            updated_at=agg.updated_at,
        )
    except ProgramStateVersionConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error_code": "STALE_STATE_MUTATION_REJECTED",
                "message": str(e),
                "aggregate_id": e.aggregate_id,
                "expected_version": e.expected_version,
                "actual_version": e.actual_version,
            },
        )
    except ProgramAuthorityLaneViolationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error_code": "AUTHORITY_LANE_VIOLATION", "message": str(e)},
        )
    except ProgramStateAggregateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Execution aggregate '{aggregate_id}' not found"},
        )


@router.post("/executions/{aggregate_id:path}/repair", response_model=ProgramExecutionSummaryResponse)
def repair_execution_state(
    aggregate_id: str,
    request: RepairExecutionRequest,
    response: Response,
    if_match_version: Optional[str] = Header(default=None, alias="If-Match-State-Version"),
    if_match_sha256: Optional[str] = Header(default=None, alias="If-Match-State-SHA256"),
    service: ProgramOperatorRuntimeService = Depends(get_operator_service),
) -> ProgramExecutionSummaryResponse:
    """Applies governed repair or direct manipulation to state aggregate."""
    exp_version, exp_sha256 = _resolve_cas_headers(
        request.expected_version, request.expected_state_sha256, if_match_version, if_match_sha256
    )
    try:
        res = service.repair_program(
            aggregate_id=aggregate_id,
            actor_id=request.actor_id,
            repair_action=request.repair_action,
            repair_payload=request.repair_payload,
            target_state=request.target_state,
            expected_version=exp_version,
            expected_state_sha256=exp_sha256,
        )
        agg = res.aggregate
        _set_state_headers(response, agg)
        return ProgramExecutionSummaryResponse(
            aggregate_id=agg.aggregate_id,
            workspace_id=agg.workspace_id,
            program_id=agg.program_id,
            program_version=agg.program_version,
            lifecycle=agg.lifecycle.value,
            current_state=agg.current_state,
            version=agg.version,
            state_hash=agg.state_hash,
            last_receipt_id=agg.last_receipt_id,
            created_at=agg.created_at,
            updated_at=agg.updated_at,
        )
    except ProgramStateVersionConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error_code": "STALE_STATE_MUTATION_REJECTED",
                "message": str(e),
                "aggregate_id": e.aggregate_id,
                "expected_version": e.expected_version,
                "actual_version": e.actual_version,
            },
        )
    except ProgramAuthorityLaneViolationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error_code": "AUTHORITY_LANE_VIOLATION", "message": str(e)},
        )
    except ProgramStateAggregateNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Execution aggregate '{aggregate_id}' not found"},
        )


# ============================================================================
# 3. Chat Supervision Dispatcher
# ============================================================================

@router.post("/operator/chat", response_model=ChatCommandResponse)
def dispatch_operator_chat(
    request: ChatCommandRequest,
    response: Response,
    if_match_version: Optional[str] = Header(default=None, alias="If-Match-State-Version"),
    if_match_sha256: Optional[str] = Header(default=None, alias="If-Match-State-SHA256"),
    service: ProgramOperatorRuntimeService = Depends(get_operator_service),
) -> ChatCommandResponse:
    """Dispatches operator slash commands directly to authoritative backend state operations."""
    exp_version, exp_sha256 = _resolve_cas_headers(
        request.expected_version, request.expected_state_sha256, if_match_version, if_match_sha256
    )
    res = service.dispatch_chat_command(
        command_str=request.command,
        workspace_id=request.workspace_id,
        actor_id=request.actor_id,
        current_aggregate_id=request.current_aggregate_id,
        expected_version=exp_version,
        expected_state_sha256=exp_sha256,
    )
    if res.state_version is not None and res.state_hash is not None:
        response.headers["X-CAE-State-Version"] = str(res.state_version)
        response.headers["X-CAE-State-SHA256"] = res.state_hash

    return ChatCommandResponse(
        command=res.command,
        action_type=res.action_type.value,
        lane=res.lane.value,
        success=res.success,
        message=res.message,
        aggregate_id=res.aggregate_id,
        state_version=res.state_version,
        state_hash=res.state_hash,
        receipt_id=res.receipt_id,
        data=res.data,
        warnings=res.warnings,
    )


# ============================================================================
# 4. Program Package Manifest & Preflight Inspections
# ============================================================================

@router.get("/{program_id}", response_model=Dict[str, Any])
def get_program_details(
    program_id: str,
    version: Optional[str] = Query(default=None, description="Specific SemVer version"),
    service: ProgramOperatorRuntimeService = Depends(get_operator_service),
) -> Dict[str, Any]:
    """Inspects a registered program package and its state machine definition."""
    try:
        return service.inspect_program_definition(program_id=program_id, version=version)
    except ProgramNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Program '{program_id}' not found"},
        )


@router.post("/{program_id}/preflight", response_model=ProgramPreflightResult)
def preflight_program(
    program_id: str,
    request: PreflightRequest,
    registry: ProgramRegistry = Depends(get_registry),
) -> ProgramPreflightResult:
    """Performs a fail-closed preflight check on a program package for an operator session."""
    try:
        return registry.preflight(
            program_id=program_id,
            workspace_id=request.workspace_id,
            context_refs=request.context_refs,
            version=request.version,
        )
    except ProgramNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error_code": "NOT_FOUND", "message": f"Program '{program_id}' not found"},
        )
