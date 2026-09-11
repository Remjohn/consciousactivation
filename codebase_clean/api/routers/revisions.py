from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from ca_contracts import canonical_sha256, utc_now_rfc3339
from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.domain.errors import PipelineConflict, PipelineNotFound

from api.dependencies import get_pipeline, get_studio_bridge
from api.errors import ErrorResponse
from api.schemas.supervision import (
    ChangeRequestProgramModel,
    DirectManipulationInput,
    ExecuteRevisionResponse,
    RefModel,
    RevisionRequestInput,
)
from api.services.campaign_projection import CampaignNotFound, load_campaign_with_revisions, state_object_id
from api.services.human_resolution import (
    HumanResolutionStaleError,
    HumanResolutionValidationError,
    commit_native_edit,
    compile_native_edit_program,
)
from api.services.studio_bridge import StudioBridge, StudioBridgeCrash, StudioBridgeError

logger = logging.getLogger("conscious_activations.api.revisions")
router = APIRouter()

DEFAULT_STUDIO_TOOLS = {
    "studio.adjust_bbox": {"tool_id": "studio.adjust_bbox", "tool_version": "1.0.0", "owner_product": "conscious-activations-studio", "allowed_target_layers": ["COMPOSITION", "TIMELINE_OVERLAY"], "argument_keys": ["axis", "delta_micros", "mode"], "reversible": True},
    "studio.resize_bbox": {"tool_id": "studio.resize_bbox", "tool_version": "1.0.0", "owner_product": "conscious-activations-studio", "allowed_target_layers": ["COMPOSITION", "TIMELINE_OVERLAY"], "argument_keys": ["scale_delta_micros", "anchor"], "reversible": True},
    "studio.trim_segment": {"tool_id": "studio.trim_segment", "tool_version": "1.0.0", "owner_product": "conscious-activations-studio", "allowed_target_layers": ["VIDEO_EDIT_PROGRAM"], "argument_keys": ["edge", "delta_ms", "preserve_word_boundary", "preserve_expression_tail"], "reversible": True},
    "studio.reorder_item": {"tool_id": "studio.reorder_item", "tool_version": "1.0.0", "owner_product": "conscious-activations-studio", "allowed_target_layers": ["VIDEO_EDIT_PROGRAM", "CAROUSEL_SEQUENCE"], "argument_keys": ["relation", "anchor_id"], "reversible": True},
    "studio.edit_text": {"tool_id": "studio.edit_text", "tool_version": "1.0.0", "owner_product": "conscious-activations-studio", "allowed_target_layers": ["COMPOSITION_COPY"], "argument_keys": ["text", "transformation_class"], "reversible": True},
    "studio.set_parameter": {"tool_id": "studio.set_parameter", "tool_version": "1.0.0", "owner_product": "conscious-activations-studio", "allowed_target_layers": ["COMPOSITION", "VIDEO_EDIT_PROGRAM", "TIMELINE_OVERLAY", "CAMPAIGN"], "argument_keys": ["parameter", "value"], "reversible": True},
    "studio.select_candidate": {"tool_id": "studio.select_candidate", "tool_version": "1.0.0", "owner_product": "conscious-activations-studio", "allowed_target_layers": ["CANDIDATE_PORTFOLIO"], "argument_keys": ["candidate_id"], "reversible": True},
    "studio.apply_steering_recipe": {"tool_id": "studio.apply_steering_recipe", "tool_version": "1.0.0", "owner_product": "conscious-activations-studio", "allowed_target_layers": ["COMPOSITION", "VIDEO_EDIT_PROGRAM", "TIMELINE_OVERLAY"], "argument_keys": ["recipe_id", "operation_index", "payload"], "reversible": True},
    "studio.request_semantic_revision": {"tool_id": "studio.request_semantic_revision", "tool_version": "1.0.0", "owner_product": "activative-intelligence-runtime", "allowed_target_layers": ["AIR_REVISION_REQUEST"], "argument_keys": ["request", "reason", "source_ref"], "reversible": False},
}


def _error(status_code: int, error_code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail=ErrorResponse(error_code=error_code, message=message, timestamp=utc_now_rfc3339()).model_dump(),
    )


def _build_revision_context(campaign: dict[str, Any]) -> dict[str, Any]:
    return {
        "tools": list(DEFAULT_STUDIO_TOOLS.values()),
        "steering_recipes": [],
        "allowed_node_ids": [node["node_id"] for node in campaign.get("run_nodes", [])],
        "target_layers_by_ref": {},
        "state_version": campaign["state"]["version"],
        "default_validation_plan": ["source_fidelity_recheck", "voice_dna_recheck", "final_script_revision_required_if_semantic"],
        "default_invariants": ["upstream_semantic_authority_preserved", "source_lineage_preserved"],
        "wrong_reading_locks": [],
    }


@router.post("/revisions", response_model=ChangeRequestProgramModel, status_code=201)
def compile_revision(body: RevisionRequestInput, pipeline: PipelineApplication = Depends(get_pipeline), bridge: StudioBridge = Depends(get_studio_bridge)):
    campaign_id = body.run_ref.object_id.split(":")[-1] if ":" in body.run_ref.object_id else body.run_ref.object_id
    try:
        campaign = load_campaign_with_revisions(pipeline, campaign_id)
    except CampaignNotFound as exc:
        raise _error(404, "CAMPAIGN_NOT_FOUND", str(exc)) from exc
    try:
        result = bridge.call("compile-natural-language-revision", {"request": body.model_dump(mode="json"), "context": _build_revision_context(campaign)})
    except StudioBridgeError as exc:
        raise _error(422, exc.code, str(exc)) from exc
    except StudioBridgeCrash as exc:
        raise _error(500, "STUDIO_BRIDGE_CRASH", str(exc)) from exc
    return ChangeRequestProgramModel.model_validate(result)


@router.post("/revisions/direct", response_model=ChangeRequestProgramModel, status_code=201)
def compile_direct_manipulation(body: DirectManipulationInput, pipeline: PipelineApplication = Depends(get_pipeline), bridge: StudioBridge = Depends(get_studio_bridge)):
    campaign_id = body.run_ref.object_id.split(":")[-1] if ":" in body.run_ref.object_id else body.run_ref.object_id
    if body.manipulation_type in {"SUBSTITUTE_ASSET", "ADJUST_TIMING"}:
        try:
            campaign = load_campaign_with_revisions(pipeline, campaign_id)
            if body.expected_state_version != int(campaign["state"]["version"]):
                raise _error(409, "STALE_STATE_VERSION", f"expected state version {body.expected_state_version}, current {campaign["state"]["version"]}")
            program = compile_native_edit_program(
                campaign_id=campaign_id,
                state=campaign["state"],
                state_revision=campaign["state_revision"],
                target_ref=body.target_ref.model_dump(),
                target_node_id=body.target_node_id,
                manipulation_type=body.manipulation_type,
                arguments=body.arguments,
                operator_actor=body.operator_actor.model_dump(),
            )
            stored = pipeline.repository.store_object(
                "studio_change_request_program",
                program.as_dict(),
                idempotency_key=f"compile:{program.program_id}",
                object_id=program.program_id,
            )
            return ChangeRequestProgramModel(
                program_id=program.program_id,
                compilation_status="COMPILED",
                request_ref=body.target_ref,
                interpretation=f"Bounded native edit: {body.manipulation_type} on {body.target_node_id}",
                target_layer_or_nodes=[body.target_node_id],
                exact_operations=[{
                    "operation_id": f"operation:{canonical_sha256(program.as_dict())[:24]}",
                    "target_ref": body.target_ref.model_dump(),
                    "target_node_id": body.target_node_id,
                    "target_layer": "VIDEO_EDIT_PROGRAM",
                    "tool_id": f"studio.native_edit.{body.manipulation_type.lower()}",
                    "tool_version": "1.0.0",
                    "arguments": body.arguments,
                    "preconditions": ["state_version_matches", "timeline_item_editable", "bounds_valid"],
                    "expected_effect": "persist bounded native edit and HumanResolutionEpisode",
                }],
                declared_invariants=["INV-HUMAN-RESOLUTION-001", "no_ui_only_state", "no_release_bypass"],
                required_transformations=["persist canonical timeline revision", "record before_after_diff"],
                creative_degrees_of_freedom=[],
                invalidated_downstream_nodes=[],
                validation_plan=["cas", "bounds", "before_after_diff", "persisted_state_reopen"],
                preview_required=True,
                confidence_micros=1_000_000,
                escalation=None,
                source_kind="DIRECT_MANIPULATION",
                expected_state_version=body.expected_state_version,
                program_sha256=stored["object"]["canonical_sha256"],
            )
        except CampaignNotFound as exc:
            raise _error(404, "CAMPAIGN_NOT_FOUND", str(exc)) from exc
        except HumanResolutionValidationError as exc:
            raise _error(422, exc.code, str(exc)) from exc
        except PipelineConflict as exc:
            raise _error(409, "CONFLICT", str(exc)) from exc

    try:
        campaign = load_campaign_with_revisions(pipeline, campaign_id)
    except CampaignNotFound as exc:
        raise _error(404, "CAMPAIGN_NOT_FOUND", str(exc)) from exc
    try:
        result = bridge.call("compile-direct-manipulation", {"delta": body.model_dump(mode="json"), "context": _build_revision_context(campaign)})
    except StudioBridgeError as exc:
        raise _error(422, exc.code, str(exc)) from exc
    except StudioBridgeCrash as exc:
        raise _error(500, "STUDIO_BRIDGE_CRASH", str(exc)) from exc
    return ChangeRequestProgramModel.model_validate(result)


@router.post("/revisions/{program_id}/execute", response_model=ExecuteRevisionResponse)
def execute_revision(program_id: str, pipeline: PipelineApplication = Depends(get_pipeline), bridge: StudioBridge = Depends(get_studio_bridge)):
    try:
        stored = pipeline.repository.get_object(program_id)
    except PipelineNotFound:
        raise _error(404, "REVISION_NOT_FOUND", program_id)
    program = stored["payload"]
    if program.get("manipulation_type") in {"SUBSTITUTE_ASSET", "ADJUST_TIMING"} and program.get("campaign_id"):
        try:
            result = commit_native_edit(
                pipeline=pipeline,
                campaign_id=str(program["campaign_id"]),
                program=program,
                idempotency_key=f"execute:{program_id}",
                expected_state_version=int(program["expected_state_version"]),
            )
        except HumanResolutionStaleError as exc:
            raise _error(409, "STALE_STATE_VERSION", str(exc)) from exc
        except HumanResolutionValidationError as exc:
            raise _error(422, exc.code, str(exc)) from exc
        except PipelineConflict as exc:
            raise _error(409, "CONFLICT", str(exc)) from exc
        response_program = ChangeRequestProgramModel.model_validate({
            "program_id": program_id,
            "compilation_status": "COMPILED",
            "request_ref": program["target_ref"],
            "interpretation": f"Executed bounded native edit {program['manipulation_type']}",
            "target_layer_or_nodes": [program["target_node_id"]],
            "exact_operations": [{
                "operation_id": f"operation:{canonical_sha256(program)[:24]}",
                "target_ref": program["target_ref"],
                "target_node_id": program["target_node_id"],
                "target_layer": "VIDEO_EDIT_PROGRAM",
                "tool_id": f"studio.native_edit.{str(program['manipulation_type']).lower()}",
                "tool_version": "1.0.0",
                "arguments": program["arguments"],
                "preconditions": ["state_version_matches", "timeline_item_editable", "bounds_valid"],
                "expected_effect": "persist bounded native edit and HumanResolutionEpisode",
            }],
            "declared_invariants": ["INV-HUMAN-RESOLUTION-001", "no_ui_only_state", "no_release_bypass"],
            "required_transformations": ["persist canonical timeline revision", "record before_after_diff"],
            "creative_degrees_of_freedom": [],
            "invalidated_downstream_nodes": [],
            "validation_plan": ["cas", "bounds", "before_after_diff", "persisted_state_reopen"],
            "preview_required": True,
            "confidence_micros": 1_000_000,
            "escalation": None,
            "source_kind": "DIRECT_MANIPULATION",
            "expected_state_version": int(program["expected_state_version"]),
            "program_sha256": stored["canonical_sha256"],
        })
        return ExecuteRevisionResponse(program=response_program, campaign=result["campaign"], rerun={"required": True, "status": "QA_REQUIRED"}, episode=result["episode"], receipt=result["receipt"])

    return ExecuteRevisionResponse(
        program=ChangeRequestProgramModel(
            program_id=program_id,
            compilation_status="COMPILED",
            request_ref=RefModel(object_id="", version="", sha256="0" * 64),
            interpretation="Execution acknowledged",
            target_layer_or_nodes=[],
            exact_operations=[],
            declared_invariants=[],
            required_transformations=[],
            creative_degrees_of_freedom=[],
            invalidated_downstream_nodes=[],
            validation_plan=[],
            preview_required=False,
            confidence_micros=0,
            escalation=None,
            source_kind="NATURAL_LANGUAGE",
            expected_state_version=0,
            program_sha256=stored["canonical_sha256"],
        )
    )
