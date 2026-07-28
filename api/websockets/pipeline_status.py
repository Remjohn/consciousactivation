from __future__ import annotations

from typing import Any

import anyio
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse

from api.dependencies import get_pipeline, get_pipeline_ws
from api.errors import ErrorResponse
from api.schemas.pipeline_status import RunEventsResponse, RunStatusEnvelope
from api.services.campaign_run_lookup import (
    CampaignHasMultipleRuns,
    CampaignHasNoRun,
    resolve_campaign_run_id,
)
from ca_contracts import utc_now_rfc3339
from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.domain.errors import PipelineNotFound

router = APIRouter()

TERMINAL_RUN_STATES = {"COMPLETED", "FAILED", "CANCELLED", "INVALIDATED"}
MIN_POLL_INTERVAL_MS = 250
MAX_POLL_INTERVAL_MS = 5000


async def _snapshot(pipeline: PipelineApplication, run_id: str) -> dict[str, Any]:
    return await run_in_threadpool(pipeline.runs.status, run_id)


async def _replay(pipeline: PipelineApplication, run_id: str) -> dict[str, Any]:
    return await run_in_threadpool(pipeline.runs.replay, run_id)


def _diff_messages(
    run_id: str,
    previous: dict[str, Any] | None,
    current: dict[str, Any],
) -> list[dict[str, Any]]:
    if previous is None or current["revision"] == previous["revision"]:
        return []
    messages: list[dict[str, Any]] = []
    previous_nodes = {n["node_id"]: n for n in previous["nodes"]}
    for node in current["nodes"]:
        if previous_nodes.get(node["node_id"]) != node:
            messages.append({
                "type": "node_state_changed",
                "retrieved_at_utc": utc_now_rfc3339(),
                "run_id": run_id,
                "node": node,
            })
    run_fields = ("state", "revision", "cancel_requested", "current_checkpoint_id")
    if any(current[f] != previous[f] for f in run_fields):
        messages.append({
            "type": "run_state_changed",
            "retrieved_at_utc": utc_now_rfc3339(),
            "run_id": run_id,
            "workflow_id": current["workflow_id"],
            **{f: current[f] for f in run_fields},
        })
    return messages


async def _stream(
    websocket: WebSocket,
    pipeline: PipelineApplication,
    run_id: str,
    *,
    skip_accept: bool = False,
) -> None:
    """Poll-and-diff bridge for a single run.

    Parameters
    ----------
    skip_accept : bool
        When True, the caller has already called ``await websocket.accept()``.
        Used by ``ws_campaign_status`` which must accept before resolving the
        campaign→run lookup so it can send typed close codes.  The plain
        ``ws_run_status`` path leaves this False so ``_stream`` handles accept.
    """
    config = websocket.app.state.config
    poll_ms = int(
        websocket.query_params.get("poll_interval_ms", config.ws_poll_interval_ms)
    )
    poll_ms = max(MIN_POLL_INTERVAL_MS, min(MAX_POLL_INTERVAL_MS, poll_ms))
    include_history = (
        websocket.query_params.get("include_history", "false").lower() == "true"
    )

    if not skip_accept:
        await websocket.accept()

    try:
        current = await _snapshot(pipeline, run_id)
    except PipelineNotFound:
        await websocket.close(code=4404, reason=f"run not found: {run_id}")
        return

    await websocket.send_json({
        "type": "snapshot",
        "retrieved_at_utc": utc_now_rfc3339(),
        "run": current,
    })

    if include_history:
        history = await _replay(pipeline, run_id)
        await websocket.send_json({
            "type": "history",
            "retrieved_at_utc": utc_now_rfc3339(),
            "event_count": history["event_count"],
            "event_stream_sha256": history["event_stream_sha256"],
            "events": history["events"],
        })

    try:
        while True:
            if current["state"] in TERMINAL_RUN_STATES:
                await websocket.send_json({
                    "type": "run_terminal",
                    "retrieved_at_utc": utc_now_rfc3339(),
                    "run": current,
                })
                await websocket.close(code=1000, reason="run reached terminal state")
                return
            await anyio.sleep(poll_ms / 1000)
            new_snapshot = await _snapshot(pipeline, run_id)
            for message in _diff_messages(run_id, current, new_snapshot):
                await websocket.send_json(message)
            current = new_snapshot
    except WebSocketDisconnect:
        return


# ---------------------------------------------------------------------------
# WebSocket endpoints
# ---------------------------------------------------------------------------


@router.websocket("/runs/{run_id}/status")
async def ws_run_status(
    websocket: WebSocket,
    run_id: str,
    pipeline: PipelineApplication = Depends(get_pipeline_ws),
) -> None:
    await _stream(websocket, pipeline, run_id)


@router.websocket("/campaigns/{campaign_id}/status")
async def ws_campaign_status(
    websocket: WebSocket,
    campaign_id: str,
    pipeline: PipelineApplication = Depends(get_pipeline_ws),
) -> None:
    # Accept first so we can send typed close codes on resolution failure
    await websocket.accept()
    try:
        run_id = await run_in_threadpool(
            resolve_campaign_run_id, pipeline.repository, campaign_id
        )
    except CampaignHasNoRun:
        await websocket.close(
            code=4404, reason=f"campaign has no linked run: {campaign_id}"
        )
        return
    except CampaignHasMultipleRuns:
        await websocket.close(
            code=4409, reason=f"campaign has multiple linked runs: {campaign_id}"
        )
        return
    await _stream(websocket, pipeline, run_id, skip_accept=True)


# ---------------------------------------------------------------------------
# REST fallback endpoints
# ---------------------------------------------------------------------------


@router.get("/runs/{run_id}/status", response_model=RunStatusEnvelope)
async def get_run_status(
    run_id: str,
    request: Request,
    pipeline: PipelineApplication = Depends(get_pipeline),
) -> JSONResponse:
    try:
        run = await _snapshot(pipeline, run_id)
    except PipelineNotFound as exc:
        return JSONResponse(
            status_code=404,
            content=ErrorResponse(
                error_code="NOT_FOUND",
                message=str(exc),
                service="pipeline",
                timestamp=utc_now_rfc3339(),
            ).model_dump(),
        )
    return JSONResponse(
        content=RunStatusEnvelope(
            retrieved_at_utc=utc_now_rfc3339(), run=run
        ).model_dump()
    )


@router.get("/runs/{run_id}/status/events", response_model=RunEventsResponse)
async def get_run_events(
    run_id: str,
    pipeline: PipelineApplication = Depends(get_pipeline),
) -> JSONResponse:
    try:
        history = await _replay(pipeline, run_id)
    except PipelineNotFound as exc:
        return JSONResponse(
            status_code=404,
            content=ErrorResponse(
                error_code="NOT_FOUND",
                message=str(exc),
                service="pipeline",
                timestamp=utc_now_rfc3339(),
            ).model_dump(),
        )
    return JSONResponse(content=RunEventsResponse(**history).model_dump())


@router.get("/campaigns/{campaign_id}/status", response_model=RunStatusEnvelope)
async def get_campaign_status(
    campaign_id: str,
    pipeline: PipelineApplication = Depends(get_pipeline),
) -> JSONResponse:
    try:
        run_id = await run_in_threadpool(
            resolve_campaign_run_id, pipeline.repository, campaign_id
        )
    except CampaignHasNoRun as exc:
        return JSONResponse(
            status_code=404,
            content=ErrorResponse(
                error_code="CAMPAIGN_HAS_NO_RUN",
                message=str(exc),
                service="pipeline",
                timestamp=utc_now_rfc3339(),
            ).model_dump(),
        )
    except CampaignHasMultipleRuns as exc:
        return JSONResponse(
            status_code=409,
            content=ErrorResponse(
                error_code="CAMPAIGN_HAS_MULTIPLE_RUNS",
                message=str(exc),
                service="pipeline",
                timestamp=utc_now_rfc3339(),
            ).model_dump(),
        )
    return await get_run_status(run_id, None, pipeline)  # type: ignore[arg-type]


@router.get("/campaigns/{campaign_id}/status/events", response_model=RunEventsResponse)
async def get_campaign_events(
    campaign_id: str,
    pipeline: PipelineApplication = Depends(get_pipeline),
) -> JSONResponse:
    try:
        run_id = await run_in_threadpool(
            resolve_campaign_run_id, pipeline.repository, campaign_id
        )
    except CampaignHasNoRun as exc:
        return JSONResponse(
            status_code=404,
            content=ErrorResponse(
                error_code="CAMPAIGN_HAS_NO_RUN",
                message=str(exc),
                service="pipeline",
                timestamp=utc_now_rfc3339(),
            ).model_dump(),
        )
    except CampaignHasMultipleRuns as exc:
        return JSONResponse(
            status_code=409,
            content=ErrorResponse(
                error_code="CAMPAIGN_HAS_MULTIPLE_RUNS",
                message=str(exc),
                service="pipeline",
                timestamp=utc_now_rfc3339(),
            ).model_dump(),
        )
    return await get_run_events(run_id, pipeline)