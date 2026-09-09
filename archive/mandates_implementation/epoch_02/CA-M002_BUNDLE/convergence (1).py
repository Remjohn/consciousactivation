"""
api/routers/convergence.py
--------------------------
CA-M002 / FR-CONV-001 — Dual-Context Convergence Gate API Router.

Exposes three operator-facing endpoints:

  POST /convergence/{workspace_id}/evaluate
      Evaluates the dual-context convergence predicate for a workspace.
      Returns a ConvergenceReceipt on success.
      Returns 422 with a structured reason on every gate failure.
      DOES NOT allow bypass or force flags.

  GET  /convergence/{workspace_id}/state
      Returns the current convergence gate state for a workspace as a
      read-only projection of the last stored receipt.
      The UI MUST use this to display the blocker to the operator.

  GET  /convergence/{workspace_id}/receipts
      Lists all convergence receipts for a workspace, most-recent first.

Architectural invariants:
  - The UI is a PROJECTION. It cannot bypass, override, or invent local state.
  - All admission decisions are made by ConvergenceGate (runtime), not here.
  - Error responses carry structured reason_code and permitted_next_actions
    so the operator can see exactly why execution is blocked.
"""

from __future__ import annotations

import logging
import sqlite3
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, status

from ca_runtime.convergence_gate import (
    AudienceTensionsRef,
    BypassAttemptError,
    ConvergenceGate,
    ConvergenceGateError,
    ConvergenceStore,
    DownstreamCompilationGuard,
    GuestGenesisRef,
    InvalidAudienceTensionsError,
    InvalidGuestGenesisError,
)
from api.schemas.convergence import (
    AudienceTensionsRefInput,
    ConvergenceGateStateResponse,
    ConvergenceReceiptListResponse,
    ConvergenceReceiptResponse,
    EvaluateConvergenceRequest,
    GuestGenesisRefInput,
)

logger = logging.getLogger("api.routers.convergence")

router = APIRouter()

# Module-level gate singleton (stateless; safe to share across requests)
_gate = ConvergenceGate()


def _get_store(request: Request) -> ConvergenceStore:
    """
    Returns a ConvergenceStore backed by the application's SQLite connection.
    Falls back to an in-memory SQLite connection for environments where the
    application state does not expose a raw connection (e.g. test harnesses).
    """
    try:
        # Try to get the pipeline application's underlying SQLite DB connection.
        # The pipeline app exposes its database; we use the same file-level DB.
        pipeline = request.app.state.pipeline
        conn: sqlite3.Connection = pipeline.db._connect()
        return ConvergenceStore(conn)
    except (AttributeError, Exception):
        # Fallback: in-memory store for environments without full app state.
        conn = sqlite3.connect(":memory:")
        return ConvergenceStore(conn)


def _build_receipt_response(receipt_dict: dict) -> ConvergenceReceiptResponse:
    return ConvergenceReceiptResponse(
        receipt_id=receipt_dict["receipt_id"],
        workspace_id=receipt_dict["workspace_id"],
        status=receipt_dict["status"],
        guest_genesis_territory_id=receipt_dict["guest_genesis_territory_id"],
        guest_genesis_revision_id=receipt_dict["guest_genesis_revision_id"],
        guest_genesis_sha256=receipt_dict["guest_genesis_sha256"],
        audience_tensions_audience_id=receipt_dict["audience_tensions_audience_id"],
        audience_tensions_revision_id=receipt_dict["audience_tensions_revision_id"],
        audience_tensions_sha256=receipt_dict["audience_tensions_sha256"],
        convergence_digest=receipt_dict["convergence_digest"],
        convergence_signature=receipt_dict["convergence_signature"],
        converged_at=receipt_dict["converged_at"],
        gate_version=receipt_dict.get("gate_version", "1.0.0"),
        admitted=receipt_dict.get("status") == "CONVERGED",
    )


@router.post(
    "/{workspace_id}/evaluate",
    response_model=ConvergenceReceiptResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluate dual-context convergence gate (FR-CONV-001)",
    description=(
        "Evaluates Guest Genesis Semantic Territory and Audience Tensions against "
        "the canonical convergence predicate. Returns a signed receipt on success. "
        "Returns 422 with a structured reason and permitted next actions on every "
        "gate failure. No bypass path exists."
    ),
    tags=["convergence"],
)
def evaluate_convergence(
    workspace_id: str,
    body: EvaluateConvergenceRequest,
    request: Request,
) -> ConvergenceReceiptResponse:
    """
    POST /convergence/{workspace_id}/evaluate

    Evaluates the convergence gate for the supplied workspace.
    The body must contain valid GuestGenesisRef and AudienceTensionsRef.

    On success:  HTTP 200 + ConvergenceReceiptResponse (status=CONVERGED, admitted=True)
    On failure:  HTTP 422 + structured error with reason_code and permitted_next_actions

    The UI MUST NOT attempt to retry with force=True; no such flag exists.
    """
    # Validate workspace alignment between path parameter and body
    if body.guest_genesis.workspace_id != workspace_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error_code": "WORKSPACE_MISMATCH",
                "message": (
                    f"guest_genesis.workspace_id '{body.guest_genesis.workspace_id}' "
                    f"does not match path workspace_id '{workspace_id}'"
                ),
                "permitted_next_actions": ["align_workspace_id"],
            },
        )
    if body.audience_tensions.workspace_id != workspace_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error_code": "WORKSPACE_MISMATCH",
                "message": (
                    f"audience_tensions.workspace_id '{body.audience_tensions.workspace_id}' "
                    f"does not match path workspace_id '{workspace_id}'"
                ),
                "permitted_next_actions": ["align_workspace_id"],
            },
        )

    try:
        guest_genesis_ref = GuestGenesisRef(
            workspace_id=body.guest_genesis.workspace_id,
            territory_id=body.guest_genesis.territory_id,
            revision_id=body.guest_genesis.revision_id,
            sha256_digest=body.guest_genesis.sha256_digest,
            ratified_state=body.guest_genesis.ratified_state,
            wrong_reading_locks=tuple(body.guest_genesis.wrong_reading_locks),
            vocabulary_boundaries=tuple(body.guest_genesis.vocabulary_boundaries),
        )
    except (InvalidGuestGenesisError, ConvergenceGateError) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error_code": e.reason_code,
                "message": str(e),
                "details": e.details,
                "permitted_next_actions": e.permitted_next_actions,
            },
        )

    try:
        audience_tensions_ref = AudienceTensionsRef(
            workspace_id=body.audience_tensions.workspace_id,
            audience_id=body.audience_tensions.audience_id,
            revision_id=body.audience_tensions.revision_id,
            sha256_digest=body.audience_tensions.sha256_digest,
            tension_state=body.audience_tensions.tension_state,
            tension_count=body.audience_tensions.tension_count,
            active_tension_labels=tuple(body.audience_tensions.active_tension_labels),
        )
    except (InvalidAudienceTensionsError, ConvergenceGateError) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error_code": e.reason_code,
                "message": str(e),
                "details": e.details,
                "permitted_next_actions": e.permitted_next_actions,
            },
        )

    try:
        store = _get_store(request)
        guard = DownstreamCompilationGuard(gate=_gate, store=store)
        receipt = guard.assert_convergence(
            workspace_id=workspace_id,
            guest_genesis=guest_genesis_ref,
            audience_tensions=audience_tensions_ref,
            downstream_program_id="convergence_gate_evaluation",
        )
    except BypassAttemptError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error_code": e.reason_code,
                "message": str(e),
                "permitted_next_actions": e.permitted_next_actions,
            },
        )
    except ConvergenceGateError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error_code": e.reason_code,
                "message": str(e),
                "details": e.details,
                "permitted_next_actions": e.permitted_next_actions,
            },
        )
    except Exception:
        logger.exception("Unexpected error during convergence evaluation for workspace '%s'", workspace_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "CONVERGENCE_EVALUATION_FAILED",
                "message": "An unexpected error occurred during convergence evaluation.",
            },
        )

    return _build_receipt_response(receipt.to_dict())


@router.get(
    "/{workspace_id}/state",
    response_model=ConvergenceGateStateResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current convergence gate state for a workspace",
    description=(
        "Returns the current dual-context convergence gate state as a read-only "
        "projection of the most recent stored receipt. The UI MUST use this to "
        "display the blocker to the operator without duplicating authority."
    ),
    tags=["convergence"],
)
def get_convergence_state(
    workspace_id: str,
    request: Request,
) -> ConvergenceGateStateResponse:
    """
    GET /convergence/{workspace_id}/state

    Projects the current convergence gate state.
    Returns admitted=False with a blocker explanation if no valid receipt exists.
    The UI should surface the blocker message to guide the operator to the next action.
    """
    try:
        store = _get_store(request)
        guard = DownstreamCompilationGuard(gate=_gate, store=store)
        state = guard.get_gate_state(workspace_id)
    except Exception:
        logger.exception("Failed to retrieve convergence state for workspace '%s'", workspace_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "CONVERGENCE_STATE_RETRIEVAL_FAILED",
                "message": "Failed to retrieve convergence gate state.",
            },
        )

    receipt_response: Optional[ConvergenceReceiptResponse] = None
    if state.get("receipt"):
        receipt_response = _build_receipt_response(state["receipt"])

    blocker = None
    if not state["admitted"]:
        blocker = {
            "message": (
                "Dual-context convergence gate is not satisfied for this workspace. "
                "Both Guest Genesis Semantic Territory (TERRITORY_RATIFIED) and "
                "Audience Tensions (at least one active tension) must be present, "
                "valid, and independently verified before downstream narrative "
                "compilation can proceed. Evaluate the gate via POST /{workspace_id}/evaluate."
            ),
            "gate_invariant": "FR-CONV-001",
            "permitted_next_actions": [
                "POST /convergence/{workspace_id}/evaluate",
                "run_program:guest_genesis_semantic_territory_program",
                "run_program:audience_context_program",
            ],
        }

    return ConvergenceGateStateResponse(
        workspace_id=workspace_id,
        status=state["status"],
        admitted=state["admitted"],
        gate_invariant=state.get("gate_invariant", "FR-CONV-001"),
        receipt=receipt_response,
        blocker=blocker,
    )


@router.get(
    "/{workspace_id}/receipts",
    response_model=ConvergenceReceiptListResponse,
    status_code=status.HTTP_200_OK,
    summary="List convergence receipts for a workspace",
    description="Returns all convergence receipts for a workspace, most-recent first.",
    tags=["convergence"],
)
def list_convergence_receipts(
    workspace_id: str,
    request: Request,
    limit: int = 20,
) -> ConvergenceReceiptListResponse:
    """
    GET /convergence/{workspace_id}/receipts

    Lists stored convergence receipts for a workspace.
    Useful for operator audit trail and provenance inspection.
    """
    try:
        store = _get_store(request)
        receipts = store.list_receipts(workspace_id, limit=limit)
    except Exception:
        logger.exception("Failed to list convergence receipts for workspace '%s'", workspace_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "CONVERGENCE_RECEIPT_LIST_FAILED",
                "message": "Failed to list convergence receipts.",
            },
        )

    return ConvergenceReceiptListResponse(
        workspace_id=workspace_id,
        receipts=[_build_receipt_response(r.to_dict()) for r in receipts],
        total=len(receipts),
    )
