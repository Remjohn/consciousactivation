from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from ca_contracts import utc_now_rfc3339

from api.dependencies import get_air
from api.errors import ErrorResponse
from api.schemas import air as schemas
from api.services import air_adapter, air_projection
from cmf_activative_intelligence.domain import AirValidationError
from cmf_activative_intelligence.repositories.air_repository import ObjectVersionConflict

router = APIRouter()


def _error(code: str, message: str, status: int) -> HTTPException:
    return HTTPException(status_code=status, detail=ErrorResponse(error_code=code, message=message, timestamp=utc_now_rfc3339()).model_dump())


@router.get("/hypotheses/{portfolio_id}", response_model=schemas.HypothesisPortfolioDetail)
def get_hypothesis_portfolio(portfolio_id: str, air=Depends(get_air)):
    try:
        portfolio = air_adapter.get_portfolio(air, portfolio_id)
    except air_adapter.PortfolioNotFound:
        raise _error("PORTFOLIO_NOT_FOUND", f"no activation_hypothesis_portfolio with id '{portfolio_id}'", 404)
    return air_projection.project_portfolio_detail(air, portfolio)


@router.post("/hypotheses/{portfolio_id}/select", response_model=schemas.HypothesisSelectionResponse)
def select_hypothesis(portfolio_id: str, body: schemas.HypothesisSelectionRequest, air=Depends(get_air)):
    try:
        result = air_adapter.select_hypothesis(air, portfolio_id, body.model_dump())
    except air_adapter.PortfolioNotFound:
        raise _error("PORTFOLIO_NOT_FOUND", f"no activation_hypothesis_portfolio with id '{portfolio_id}'", 404)
    except air_adapter.PortfolioNotOpen as exc:
        raise _error("PORTFOLIO_NOT_OPEN", f"portfolio_state is '{exc}', expected 'OPEN'", 409)
    except air_adapter.CandidateJudgmentsIncomplete as exc:
        raise _error("CANDIDATE_JUDGMENTS_INCOMPLETE", f"missing={sorted(exc.missing)} extra={sorted(exc.extra)}", 422)
    except air_adapter.UnknownCandidate as exc:
        raise _error("UNKNOWN_CANDIDATE", f"'{exc}' is not a candidate in this portfolio", 404)
    except air_adapter.SelectionNotSupportedByScores as exc:
        raise _error("SELECTION_NOT_SUPPORTED_BY_SCORES", f"comparison decided {exc.decision}, not a decisive win for '{body.selected_hypothesis_id}'; no writes were made past compare_portfolio", 409)
    except ObjectVersionConflict:
        raise _error("CONFLICT", "portfolio was modified concurrently; re-fetch and retry", 409)
    except AirValidationError as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)
    return {
        "portfolio": air_projection.project_portfolio_detail(air, air_adapter.get_portfolio(air, portfolio_id)),
        "decision": result["decision"],
        "stop_reason": result["stop_reason"],
        "selected_hypothesis_ref": result["selected_hypothesis_ref"],
        "comparison_ref": result["comparison_ref"],
        "stopping_receipt_ref": result["stopping_receipt_ref"],
        "planned_pack_ref": result["planned_pack_ref"],
        "promotion_ref": result["promotion_ref"],
    }


@router.get("/scripts/{script_id}", response_model=schemas.FinalScriptDetail)
def get_script(script_id: str, air=Depends(get_air)):
    try:
        script = air_adapter.get_script(air, script_id)
    except air_adapter.ScriptNotFound:
        raise _error("SCRIPT_NOT_FOUND", f"no final_script_package with id '{script_id}'", 404)
    return air_projection.project_script_detail(air, script)


@router.post("/scripts/{script_id}/approve", response_model=schemas.ScriptApprovalResponse)
def approve_script(script_id: str, body: schemas.ScriptApprovalRequest, air=Depends(get_air)):
    try:
        result = air_adapter.approve_script(air, script_id, body.model_dump())
    except air_adapter.ScriptNotFound:
        raise _error("SCRIPT_NOT_FOUND", f"no final_script_package with id '{script_id}'", 404)
    except air_adapter.ScriptAlreadyApproved:
        raise _error("ALREADY_APPROVED", f"'{script_id}' is already operator_approved; retry with the same idempotency_key if this was meant to be a replay", 409)
    except AirValidationError as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)
    return {
        "approval_ref": {k: result["approval"][k2] for k, k2 in (("object_id", "object_id"), ("version", "semantic_version"), ("sha256", "canonical_sha256"))},
        "decision": "APPROVE",
        "script": air_projection.project_script_detail(air, result["script"]),
    }


@router.post("/scripts/{script_id}/transfer-contract", response_model=schemas.TransferContractResponse)
def create_transfer_contract(script_id: str, body: schemas.TransferContractRequest, air=Depends(get_air)):
    try:
        contract = air_adapter.create_transfer_contract(air, script_id, body.model_dump())
    except air_adapter.ScriptNotFound:
        raise _error("SCRIPT_NOT_FOUND", f"no final_script_package with id '{script_id}'", 404)
    except air_adapter.ScriptNotApproved:
        raise _error("SCRIPT_NOT_APPROVED", f"final_script_package '{script_id}' has operator_approved=false; a transfer contract cannot be created until FR-APP-032 approval is recorded", 409)
    except AirValidationError as exc:
        raise _error("VALIDATION_ERROR", str(exc), 422)
    return {
        "contract_ref": {"object_id": contract["object_id"], "version": contract["semantic_version"], "sha256": contract["canonical_sha256"]},
        "final_script_ref": contract["payload"]["final_script_ref"],
    }
