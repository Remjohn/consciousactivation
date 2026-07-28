from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from ca_contracts import utc_now_rfc3339
from api.dependencies import get_pipeline, get_studio_bridge
from api.errors import ErrorResponse
from api.schemas.supervision import (
    AuditExportManifestModel,
    ShipDecisionModel,
    ShipRequestInput,
)
from api.services.campaign_projection import (
    CampaignNotFound,
    load_campaign,
)
from api.services.studio_bridge import StudioBridge, StudioBridgeError, StudioBridgeCrash
from cmf_pipeline.application import PipelineApplication

logger = logging.getLogger("conscious_activations.api.ship")

router = APIRouter()


def _error(status_code: int, error_code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail=ErrorResponse(
            error_code=error_code, message=message, timestamp=utc_now_rfc3339(),
        ).model_dump(),
    )


@router.post("/ship", response_model=ShipDecisionModel, status_code=201)
def request_ship(
    body: ShipRequestInput,
    pipeline: PipelineApplication = Depends(get_pipeline),
    bridge: StudioBridge = Depends(get_studio_bridge),
):
    campaign_id = body.campaign_ref.object_id.split(":")[-1] if ":" in body.campaign_ref.object_id else body.campaign_ref.object_id
    try:
        campaign = load_campaign(pipeline, campaign_id)
    except CampaignNotFound as exc:
        raise _error(404, "CAMPAIGN_NOT_FOUND", str(exc)) from exc

    campaign_state = campaign["state"]
    request_payload = {"request": body.model_dump(mode="json"), "campaign": campaign_state}

    try:
        result = bridge.call("evaluate-ship-request", request_payload)
    except StudioBridgeError as exc:
        raise _error(422, exc.code, exc.message) from exc
    except StudioBridgeCrash as exc:
        logger.error("Studio bridge crash: %s", exc)
        raise _error(500, "STUDIO_BRIDGE_CRASH", str(exc)) from exc

    return ShipDecisionModel.model_validate(result)


@router.get("/audit-export", response_model=AuditExportManifestModel)
def get_audit_export(
    campaign_id: str = Query(..., description="The campaign to export"),
    pipeline: PipelineApplication = Depends(get_pipeline),
    bridge: StudioBridge = Depends(get_studio_bridge),
):
    try:
        campaign = load_campaign(pipeline, campaign_id)
    except CampaignNotFound as exc:
        raise _error(404, "CAMPAIGN_NOT_FOUND", str(exc)) from exc

    campaign_state = campaign["state"]
    campaign_order = campaign["order"]

    campaign_ref = {
        "object_id": campaign_state["campaign_id"],
        "version": str(campaign_state["version"]),
        "sha256": campaign_state.get("order_ref", {}).get("sha256", "0" * 64),
    }

    manifest_input = {
        "campaign_ref": campaign_ref,
        "source_refs": [campaign_order.get("source_ref", {})] if campaign_order.get("source_ref") else [],
        "semantic_refs": [],
        "run_refs": campaign_state.get("run_refs", []),
        "artifact_refs": campaign_state.get("artifact_refs", []),
        "evaluation_refs": campaign_state.get("evaluation_refs", []),
        "command_refs": [],
        "receipt_refs": [],
        "human_resolution_refs": [],
        "ship_decision": None,
        "replay_instructions": [],
    }

    try:
        result = bridge.call("build-audit-export-manifest", manifest_input)
    except StudioBridgeError as exc:
        raise _error(422, exc.code, exc.message) from exc
    except StudioBridgeCrash as exc:
        logger.error("Studio bridge crash: %s", exc)
        raise _error(500, "STUDIO_BRIDGE_CRASH", str(exc)) from exc

    return AuditExportManifestModel.model_validate(result)
