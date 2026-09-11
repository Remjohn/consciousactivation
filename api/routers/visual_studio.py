from __future__ import annotations

from typing import Any, Literal, TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from ca_contracts import canonical_sha256, utc_now_rfc3339
if TYPE_CHECKING:
    from cmf_pipeline.application import PipelineApplication
from api.dependencies import get_pipeline, get_studio_bridge
from api.errors import ErrorResponse
from api.services.campaign_projection import CampaignNotFound, load_campaign, state_object_id
from api.services.studio_bridge import StudioBridge, StudioBridgeCrash, StudioBridgeError
from api.services.visual_studio_contracts import assert_operator, build_visual_validation
from api.services.visual_chat import VisualChatRequest, compile_visual_chat, VisualChatValidationError

router = APIRouter()

FeedbackDecision = Literal["GOOD", "NEEDS_EDIT", "REJECT"]
FeedbackReason = Literal["SOURCE_MISMATCH", "WRONG_READING", "COMPOSITION", "TRANSFORMATION", "SOURCE_QUALITY", "OTHER"]

class FeedbackInput(BaseModel):
    revision_ref: dict[str, str]
    target_ref: dict[str, str] | None = None
    decision: FeedbackDecision
    reason: FeedbackReason | None = None
    note: str = ""
    operator_actor: dict[str, str]
    expected_state_version: int = Field(ge=1)

class VisualProposalInput(BaseModel):
    target_ref: dict[str, str]
    target_node_id: str
    natural_language_request: str = Field(min_length=1)
    operator_actor: dict[str, str]
    expected_state_version: int = Field(ge=1)

class TransformProposalInput(BaseModel):
    target_ref: dict[str, str]
    target_node_id: str
    manipulation_type: Literal["MOVE_BBOX", "RESIZE_BBOX", "TRIM_SEGMENT"]
    arguments: dict[str, str | int | bool] = Field(default_factory=dict)
    operator_actor: dict[str, str]
    expected_state_version: int = Field(ge=1)

class VisualChatInput(BaseModel):
    natural_language_request: str = Field(min_length=1, max_length=2000)
    target_ref: dict[str, str]
    target_node_id: str = Field(min_length=1)
    operator_actor: dict[str, str]
    expected_state_version: int = Field(ge=1)
    action: str | None = None
    candidate_refs: list[dict[str, str]] = Field(default_factory=list)
    canonical_revision_ref: dict[str, str] | None = None


def _error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail=ErrorResponse(error_code=code, message=message, timestamp=utc_now_rfc3339()).model_dump())


def _campaign(pipeline: Any, campaign_id: str) -> dict:
    try:
        return load_campaign(pipeline, campaign_id)
    except CampaignNotFound as exc:
        raise _error(404, "CAMPAIGN_NOT_FOUND", str(exc)) from exc


@router.get("/campaigns/{campaign_id}")
def get_visual_studio(campaign_id: str, pipeline: Any = Depends(get_pipeline)):
    campaign = _campaign(pipeline, campaign_id)
    order, state = campaign["order"], campaign["state"]
    timeline = None
    if state.get("video_edit_program") is not None:
        from api.routers.campaigns import _timeline_projection_from_state
        timeline = _timeline_projection_from_state(campaign_id, state).model_dump(mode="json")
    items = timeline.get("items", []) if timeline else []
    layers = []
    for item in items:
        layers.append({
            "layer_id": item.get("item_id"),
            "kind": item.get("kind", "UNKNOWN"),
            "role": item.get("role", "UNKNOWN"),
            "source_ref": item.get("source_ref"),
            "source_range_ms": [item.get("source_start_ms"), item.get("source_end_ms")],
            "artifact_ref": item.get("artifact_ref"),
            "editable_operations": item.get("editable_operations", []),
            "keyframes": item.get("keyframes") or (item.get("motion_plan") or {}).get("keyframes", []),
        })
    selected = layers[0] if layers else None
    validation = build_visual_validation(selected, len(items))
    preview_artifact = next((x.get("artifact_ref") for x in items if x.get("artifact_ref") and str(x.get("artifact_ref", {}).get("media_type", "")).startswith("video")), None)
    return {
        "campaign_ref": {"object_id": state.get("campaign_id", campaign_id), "version": str(state.get("version", 1)), "sha256": canonical_sha256(state)},
        "source": {"source_ref": order.get("source_ref"), "source_kind": order.get("source_kind"), "evidence_status": "LINKED_CANONICAL_REF" if order.get("source_ref") else "MISSING"},
        "composition": {"timeline": timeline, "layers": layers, "state": "CANONICAL" if timeline else "NO_CANONICAL_COMPOSITION"},
        "selected_layer": selected,
        "preview": {"available": bool(preview_artifact), "artifact_ref": preview_artifact, "proof_class": "CANONICAL_ARTIFACT_REFERENCE_ONLY" if preview_artifact else "UNAVAILABLE"},
        "validation": validation,
        "keyframe_inspection": {
            "status": validation["keyframes"],
            "selected_layer_keyframes": (selected or {}).get("keyframes", []),
        },
        "revision": {"state_version": int(state.get("version", 1)), "revision_ref": {"object_id": state_object_id(campaign_id), "version": str(state.get("version", 1)), "sha256": canonical_sha256(state)}},
        "studio_path": ["RETRIEVE", "TRANSFORM", "COMPOSE", "GENERATE"],
        "operator_actions": ["GOOD", "NEEDS_EDIT", "REJECT", "REGENERATE", "COMPILE"],
    }


@router.post("/campaigns/{campaign_id}/feedback")
def record_feedback(campaign_id: str, body: FeedbackInput, pipeline: Any = Depends(get_pipeline)):
    assert_operator(body.operator_actor)
    campaign = _campaign(pipeline, campaign_id)
    state = campaign["state"]
    if body.expected_state_version != int(state.get("version", 0)):
        raise _error(409, "STALE_STATE_VERSION", f"expected state version {body.expected_state_version}, current {state.get('version')}")
    payload = {
        "feedback_id": None,
        "campaign_ref": {"object_id": state["campaign_id"], "version": str(state["version"]), "sha256": canonical_sha256(state)},
        "revision_ref": body.revision_ref,
        "target_ref": body.target_ref,
        "decision": body.decision,
        "reason": body.reason,
        "note": body.note,
        "operator_actor": body.operator_actor,
    }
    payload["feedback_id"] = f"visual-feedback:{canonical_sha256(payload)[:24]}"
    stored = pipeline.repository.store_object("studio_visual_feedback", payload, idempotency_key=payload["feedback_id"], object_id=payload["feedback_id"], now=utc_now_rfc3339())
    return {"feedback_ref": {"object_id": stored["object"]["object_id"], "version": str(stored["object"]["revision"]), "sha256": stored["object"]["canonical_sha256"]}, "decision": body.decision, "idempotent_replay": bool(stored.get("idempotent_replay")), "immutable": True}


@router.post("/campaigns/{campaign_id}/proposals")
def compile_visual_proposal(campaign_id: str, body: VisualProposalInput, pipeline: Any = Depends(get_pipeline), bridge: StudioBridge = Depends(get_studio_bridge)):
    assert_operator(body.operator_actor)
    campaign = _campaign(pipeline, campaign_id)
    state = campaign["state"]
    if body.expected_state_version != int(state.get("version", 0)):
        raise _error(409, "STALE_STATE_VERSION", f"expected state version {body.expected_state_version}, current {state.get('version')}")
    current_ref = {"object_id": state_object_id(campaign_id), "version": str(state.get("version", 1)), "sha256": canonical_sha256(state)}
    run_ref = state.get("run_refs", [None])[0] or current_ref
    request = {
        "request_id": f"visual-chat:{canonical_sha256({'campaign_id': campaign_id, 'text': body.natural_language_request, 'target': body.target_ref, 'version': body.expected_state_version})[:24]}",
        "run_ref": run_ref,
        "target_refs": [body.target_ref],
        "target_node_ids": [body.target_node_id],
        "category_id": campaign["order"].get("category_id", ""),
        "natural_language_request": body.natural_language_request,
        "current_state_ref": current_ref,
        "evaluation_ref": None,
        "jit_capsule_ref": current_ref,
        "permitted_tool_registry_ref": campaign["order"].get("harness_ref", current_ref),
        "operator_actor": body.operator_actor,
        "expected_state_version": body.expected_state_version,
    }
    context = {"tools": [], "steering_recipes": [], "allowed_node_ids": [body.target_node_id], "target_layers_by_ref": {body.target_ref["object_id"]: "COMPOSITION"}, "state_version": int(state["version"]), "default_validation_plan": ["source_lineage_recheck", "geometry_recheck", "state_version_recheck"], "default_invariants": ["upstream_semantic_authority_preserved", "source_lineage_preserved"], "wrong_reading_locks": []}
    try:
        return bridge.call("compile-natural-language-revision", {"request": request, "context": context})
    except StudioBridgeError as exc:
        raise _error(422, exc.code, str(exc)) from exc
    except StudioBridgeCrash as exc:
        raise _error(502, "STUDIO_BRIDGE_CRASH", str(exc)) from exc

@router.post("/campaigns/{campaign_id}/transform-proposals")
def compile_transform_proposal(campaign_id: str, body: TransformProposalInput, pipeline: Any = Depends(get_pipeline), bridge: StudioBridge = Depends(get_studio_bridge)):
    assert_operator(body.operator_actor)
    campaign = _campaign(pipeline, campaign_id)
    state = campaign["state"]
    if body.expected_state_version != int(state.get("version", 0)):
        raise _error(409, "STALE_STATE_VERSION", f"expected state version {body.expected_state_version}, current {state.get('version')}")
    current_ref = {"object_id": state_object_id(campaign_id), "version": str(state.get("version", 1)), "sha256": canonical_sha256(state)}
    delta = {
        "delta_id": f"visual-transform:{canonical_sha256({'campaign_id': campaign_id, 'target': body.target_ref, 'node': body.target_node_id, 'type': body.manipulation_type, 'arguments': body.arguments, 'version': body.expected_state_version})[:24]}",
        "run_ref": state.get("run_refs", [None])[0] or current_ref,
        "target_ref": body.target_ref,
        "target_node_id": body.target_node_id,
        "manipulation_type": body.manipulation_type,
        "arguments": body.arguments,
        "current_state_ref": current_ref,
        "operator_actor": body.operator_actor,
        "expected_state_version": body.expected_state_version,
    }
    context = {"state_version": int(state["version"])}
    try:
        return bridge.call("compile-direct-manipulation", {"delta": delta, "context": context})
    except StudioBridgeError as exc:
        raise _error(422, exc.code, str(exc)) from exc
    except StudioBridgeCrash as exc:
        raise _error(502, "STUDIO_BRIDGE_CRASH", str(exc)) from exc


@router.post("/campaigns/{campaign_id}/chat/proposals")
def compile_chat_proposal(campaign_id: str, body: VisualChatInput, pipeline: Any = Depends(get_pipeline)):
    """Compile an immutable typed proposal; canonical state is never mutated."""
    assert_operator(body.operator_actor)
    campaign = _campaign(pipeline, campaign_id)
    state = campaign["state"]
    current_version = int(state.get("version", 0))
    if body.expected_state_version != current_version:
        raise _error(409, "STALE_STATE_VERSION", f"expected state version {body.expected_state_version}, current {state.get('version')}")
    current_ref = {
        "object_id": state_object_id(campaign_id),
        "version": str(state.get("version", 1)),
        "sha256": canonical_sha256(state),
    }
    try:
        request = VisualChatRequest(
            natural_language_request=body.natural_language_request,
            target_ref=body.target_ref,
            target_node_id=body.target_node_id,
            operator_actor=body.operator_actor,
            expected_state_version=body.expected_state_version,
            action=body.action,
            candidate_refs=tuple(body.candidate_refs),
            canonical_revision_ref=body.canonical_revision_ref,
        )
        proposal = compile_visual_chat(
            request,
            canonical_revision_ref=current_ref,
            current_state_version=current_version,
        )
    except (ValueError, VisualChatValidationError) as exc:
        raise _error(422, "VISUAL_CHAT_PROPOSAL_BLOCKED", str(exc)) from exc
    stored = pipeline.repository.store_object(
        "visual_chat_proposal",
        proposal.model_dump(mode="json"),
        idempotency_key=proposal.proposal_id,
        object_id=proposal.proposal_id,
        semantic_version=proposal.proposal_version,
        lifecycle_state=proposal.status.value,
        now=utc_now_rfc3339(),
    )
    return {
        "proposal": proposal.model_dump(mode="json"),
        "proposal_ref": {
            "object_id": stored["object"]["object_id"],
            "version": str(stored["object"]["revision"]),
            "sha256": stored["object"]["canonical_sha256"],
        },
        "idempotent_replay": bool(stored.get("idempotent_replay")),
    }
