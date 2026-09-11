from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from api.dependencies import get_pipeline
from api.services.campaign_projection import CampaignNotFound, load_campaign_with_revisions, state_object_id
from api.services.human_resolution import compile_native_edit_program, commit_native_edit
from cae_asset_intelligence.candidate_preview import (
    AutoAcceptanceBlockedError,
    CandidateDecision,
    CandidatePreviewCard,
    CandidatePreviewSession,
    CandidateSelectionError,
    CandidateStaleVersionError,
    NavigationDirection,
    POLICY_ID,
    build_portfolio,
    decide_session,
    navigate_session,
)
from ca_contracts import canonical_sha256, utc_now_rfc3339
from cmf_pipeline.domain.errors import PipelineConflict, PipelineNotFound

router = APIRouter()
SESSION_TYPE = "visual_candidate_session"
PORTFOLIO_TYPE = "visual_candidate_portfolio"
RECEIPT_TYPE = "visual_candidate_decision_receipt"


class CandidateSessionCreate(BaseModel):
    workspace_id: str = Field(min_length=1)
    request_ref: dict[str, str]
    target_ref: dict[str, str]
    target_node_id: str = Field(min_length=1)
    candidates: list[CandidatePreviewCard] = Field(min_length=1)


class NavigateInput(BaseModel):
    direction: Literal["NEXT", "PREVIOUS"]
    expected_version: int = Field(ge=1)


class DecisionInput(BaseModel):
    candidate_id: str = Field(min_length=1)
    decision: Literal["ACCEPT", "REJECT", "AUTO_ACCEPT"]
    expected_version: int = Field(ge=1)
    operator_actor: dict[str, Any] | None = None
    rationale: str | None = None


class PromoteInput(BaseModel):
    expected_version: int = Field(ge=1)
    operator_actor: dict[str, Any]


class SearchAgainInput(BaseModel):
    expected_version: int = Field(ge=1)
    request_ref: dict[str, str]
    candidates: list[CandidatePreviewCard] = Field(min_length=1)


def _error(code: str, message: str, status: int = 422) -> HTTPException:
    return HTTPException(status_code=status, detail={"error_code": code, "message": message, "timestamp": utc_now_rfc3339()})


def _load_session(pipeline: Any, session_id: str) -> tuple[dict, CandidatePreviewSession, dict, dict]:
    try:
        session_obj = pipeline.repository.get_object(f"visual-candidate-session:{session_id}")
    except PipelineNotFound as exc:
        raise _error("CANDIDATE_SESSION_NOT_FOUND", session_id, 404) from exc
    session = CandidatePreviewSession(**session_obj["payload"])
    try:
        portfolio_obj = pipeline.repository.get_object(session.active_portfolio_ref["object_id"])
    except PipelineNotFound as exc:
        raise _error("CANDIDATE_PORTFOLIO_NOT_FOUND", session.active_portfolio_ref["object_id"], 500) from exc
    portfolio = portfolio_obj["payload"]
    campaign = load_campaign_with_revisions(pipeline, session.campaign_id)
    return campaign, session, portfolio, session_obj


def _persist_session(pipeline: Any, session: CandidatePreviewSession, *, expected_revision: int) -> dict:
    return pipeline.repository.store_object(
        SESSION_TYPE,
        session.model_dump(mode="json"),
        object_id=f"visual-candidate-session:{session.session_id}",
        idempotency_key=f"visual-candidate-session:{session.session_id}:v{session.version}",
        expected_revision=expected_revision,
    )


@router.post("/campaigns/{campaign_id}/candidate-sessions")
def create_candidate_session(campaign_id: str, body: CandidateSessionCreate, pipeline: Any = Depends(get_pipeline)):
    try:
        campaign = load_campaign_with_revisions(pipeline, campaign_id)
    except CampaignNotFound as exc:
        raise _error("CAMPAIGN_NOT_FOUND", str(exc), 404) from exc
    if body.workspace_id != str(campaign["order"].get("workspace_id", body.workspace_id)):
        raise _error("WORKSPACE_MISMATCH", "candidate session workspace does not match campaign")
    if not body.target_ref.get("object_id") or not body.target_ref.get("version") or not body.target_ref.get("sha256"):
        raise _error("MALFORMED_TARGET_REF", "target_ref must include object_id, version and sha256")
    session_seed = canonical_sha256({
        "campaign_id": campaign_id,
        "workspace_id": body.workspace_id,
        "request_ref": body.request_ref,
        "target_ref": body.target_ref,
        "target_node_id": body.target_node_id,
        "candidates": [candidate.model_dump(mode="json") for candidate in body.candidates],
    })
    session_id = f"CVS-{session_seed[:20]}"
    portfolio = build_portfolio(session_id=session_id, request_ref=body.request_ref, candidates=body.candidates)
    portfolio_obj = pipeline.repository.store_object(
        PORTFOLIO_TYPE,
        portfolio.model_dump(mode="json"),
        object_id=portfolio.portfolio_id,
        idempotency_key=f"{session_id}:portfolio:{portfolio.portfolio_sha256}",
    )
    first_id = portfolio.candidates[0].candidate_id
    session = CandidatePreviewSession(
        session_id=session_id,
        campaign_id=campaign_id,
        workspace_id=body.workspace_id,
        target_ref=body.target_ref,
        target_node_id=body.target_node_id,
        request_ref=body.request_ref,
        active_portfolio_ref={"object_id": portfolio.portfolio_id, "version": str(portfolio_obj["object"]["revision"]), "sha256": portfolio.portfolio_sha256},
        current_index=0,
        seen_candidate_ids=(first_id,),
    )
    session_obj = pipeline.repository.store_object(
        SESSION_TYPE,
        session.model_dump(mode="json"),
        object_id=f"visual-candidate-session:{session_id}",
        idempotency_key=f"{session_id}:session:v1",
    )
    return _projection(session, portfolio, session_obj["object"]["canonical_sha256"])


@router.get("/candidate-sessions/{session_id}")
def get_candidate_session(session_id: str, pipeline: Any = Depends(get_pipeline)):
    _, session, portfolio_payload, session_obj = _load_session(pipeline, session_id)
    from cae_asset_intelligence.candidate_preview import CandidatePortfolio
    portfolio = CandidatePortfolio(**portfolio_payload)
    return _projection(session, portfolio, session_obj["canonical_sha256"])


@router.post("/candidate-sessions/{session_id}/navigate")
def navigate_candidate_session(session_id: str, body: NavigateInput, pipeline: Any = Depends(get_pipeline)):
    _, session, portfolio_payload, session_obj = _load_session(pipeline, session_id)
    from cae_asset_intelligence.candidate_preview import CandidatePortfolio
    portfolio = CandidatePortfolio(**portfolio_payload)
    try:
        next_session = navigate_session(session, portfolio, direction=NavigationDirection(body.direction), expected_version=body.expected_version)
        stored = _persist_session(pipeline, next_session, expected_revision=session_obj["revision"])
    except CandidateStaleVersionError as exc:
        raise _error("STALE_CANDIDATE_SESSION", str(exc), 409) from exc
    return _projection(next_session, portfolio, stored["object"]["canonical_sha256"])


@router.post("/candidate-sessions/{session_id}/decisions")
def decide_candidate(session_id: str, body: DecisionInput, pipeline: Any = Depends(get_pipeline)):
    campaign, session, portfolio_payload, session_obj = _load_session(pipeline, session_id)
    from cae_asset_intelligence.candidate_preview import CandidatePortfolio
    portfolio = CandidatePortfolio(**portfolio_payload)
    revision_ref = {"object_id": state_object_id(session.campaign_id), "version": str(campaign["state"]["version"]), "sha256": canonical_sha256(campaign["state"])}
    try:
        next_session, receipt, policy_report = decide_session(
            session,
            portfolio,
            candidate_id=body.candidate_id,
            decision=CandidateDecision(body.decision),
            expected_version=body.expected_version,
            operator_ref=body.operator_actor,
            rationale=body.rationale,
            revision_ref=revision_ref,
        )
        receipt_obj = pipeline.repository.store_object(
            RECEIPT_TYPE,
            receipt.model_dump(mode="json"),
            object_id=receipt.receipt_id,
            idempotency_key=receipt.receipt_id,
        )
        next_session = next_session.model_copy(update={"last_receipt_ref": {"object_id": receipt.receipt_id, "version": str(receipt_obj["object"]["revision"]), "sha256": receipt.receipt_sha256}})
        stored = _persist_session(pipeline, next_session, expected_revision=session_obj["revision"])
    except (CandidateStaleVersionError, PipelineConflict) as exc:
        raise _error("STALE_CANDIDATE_SESSION", str(exc), 409) from exc
    except AutoAcceptanceBlockedError as exc:
        raise _error("AUTO_ACCEPT_BLOCKED", str(exc), 422) from exc
    except CandidateSelectionError as exc:
        raise _error("CANDIDATE_DECISION_REJECTED", str(exc), 422) from exc
    return {**_projection(next_session, portfolio, stored["object"]["canonical_sha256"]), "decision_receipt": receipt.model_dump(mode="json"), "policy_report": policy_report}


@router.post("/candidate-sessions/{session_id}/search-again")
def search_again(session_id: str, body: SearchAgainInput, pipeline: Any = Depends(get_pipeline)):
    _, session, _, session_obj = _load_session(pipeline, session_id)
    if body.expected_version != session.version:
        raise _error("STALE_CANDIDATE_SESSION", f"expected candidate session version {body.expected_version}, current {session.version}", 409)
    portfolio = build_portfolio(session_id=session_id, request_ref=body.request_ref, candidates=body.candidates)
    portfolio_obj = pipeline.repository.store_object(
        PORTFOLIO_TYPE,
        portfolio.model_dump(mode="json"),
        object_id=portfolio.portfolio_id,
        idempotency_key=f"{session_id}:portfolio:{portfolio.portfolio_sha256}",
    )
    next_session = session.model_copy(update={
        "request_ref": body.request_ref,
        "active_portfolio_ref": {"object_id": portfolio.portfolio_id, "version": str(portfolio_obj["object"]["revision"]), "sha256": portfolio.portfolio_sha256},
        "current_index": 0,
        "selected_candidate_id": None,
        "status": "INSPECTING",
        "version": session.version + 1,
        "seen_candidate_ids": tuple(dict.fromkeys((*session.seen_candidate_ids, portfolio.candidates[0].candidate_id))),
    })
    stored = _persist_session(pipeline, next_session, expected_revision=session_obj["revision"])
    return _projection(next_session, portfolio, stored["object"]["canonical_sha256"])


@router.post("/candidate-sessions/{session_id}/promote")
def promote_candidate(session_id: str, body: PromoteInput, pipeline: Any = Depends(get_pipeline)):
    campaign, session, portfolio_payload, session_obj = _load_session(pipeline, session_id)
    from cae_asset_intelligence.candidate_preview import CandidatePortfolio
    portfolio = CandidatePortfolio(**portfolio_payload)
    if body.expected_version != session.version:
        raise _error("STALE_CANDIDATE_SESSION", f"expected candidate session version {body.expected_version}, current {session.version}", 409)
    if body.operator_actor.get("actor_type") != "human" or body.operator_actor.get("workflow_role") != "operator":
        raise _error("OPERATOR_AUTHORIZATION_REQUIRED", "promotion requires a human operator actor", 403)
    if not session.selected_candidate_id:
        raise _error("CANDIDATE_NOT_SELECTED", "accept a candidate before promotion")
    selected = next((candidate for candidate in portfolio.candidates if candidate.candidate_id == session.selected_candidate_id), None)
    if selected is None:
        raise _error("SELECTED_CANDIDATE_MISSING", session.selected_candidate_id, 422)

    # Promote through the existing canonical campaign/VAE timeline substitution path.
    state = campaign["state"]
    current_ref = selected.source_ref.model_dump(mode="json")
    program = compile_native_edit_program(
        campaign_id=session.campaign_id,
        state=state,
        state_revision=campaign["state_revision"],
        target_ref=session.target_ref,
        target_node_id=session.target_node_id,
        manipulation_type="SUBSTITUTE_ASSET",
        arguments={"source_ref": current_ref},
        operator_actor=body.operator_actor,
    )
    result = commit_native_edit(
        pipeline=pipeline,
        campaign_id=session.campaign_id,
        program=program.as_dict(),
        idempotency_key=f"m0087:promote:{session.session_id}:{session.selected_candidate_id}:{body.expected_version}",
        expected_state_version=state["version"],
    )
    new_campaign = result["campaign"]
    promotion_ref = {"object_id": state_object_id(session.campaign_id), "version": str(new_campaign["version"]), "sha256": canonical_sha256(new_campaign)}
    next_session = session.model_copy(update={
        "status": "PROMOTED",
        "version": session.version + 1,
        "promotion_ref": promotion_ref,
    })
    stored = _persist_session(pipeline, next_session, expected_revision=session_obj["revision"])
    return {"session": next_session.model_dump(mode="json"), "promotion_ref": promotion_ref, "campaign": new_campaign, "promotion_episode": result["episode"], "receipt": result["receipt"], "session_revision_sha256": stored["object"]["canonical_sha256"]}


def _projection(session: CandidatePreviewSession, portfolio: Any, session_sha: str) -> dict[str, Any]:
    current = portfolio.candidates[session.current_index]
    return {
        "session": session.model_dump(mode="json"),
        "portfolio": portfolio.model_dump(mode="json"),
        "current_candidate": current.model_dump(mode="json"),
        "selection_state": {"selected_candidate_id": session.selected_candidate_id, "rejected_candidate_ids": list(session.rejected_candidate_ids)},
        "provenance": {"session_ref": {"object_id": f"visual-candidate-session:{session.session_id}", "version": str(session.version), "sha256": session_sha}},
        "controls": {"navigation": ["PREVIOUS", "NEXT"], "decisions": ["ACCEPT", "REJECT", "AUTO_ACCEPT"], "search_again": True, "promote": session.selected_candidate_id is not None},
    }
