from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from ca_contracts import canonical_sha256, utc_now_rfc3339
from cmf_pipeline.application import PipelineApplication
from api.dependencies import get_campaign_repository, get_interview, get_pipeline, get_studio_bridge
from api.routers.harnesses import find_by_definition_id, get_harness_library_root
from api.domain.campaign import (
    CampaignValidationError,
    create_campaign_order,
    default_autonomy_policy,
    launch_campaign,
    transition_campaign,
)
from api.errors import ErrorResponse
from api.routers.harnesses import find_by_definition_id
from api.schemas.campaigns import (
    CampaignCancelRequest,
    CampaignCreateRequest,
    CampaignDetailResponse,
    CampaignSummary,
)
from api.services.campaign_repository import (
    CampaignConflictError,
    CampaignNotFoundError,
    CampaignRepository,
)
from api.services.campaign_projection import (
    CampaignNotFound as StudioCampaignNotFound,
    load_campaign,
)
from api.services.studio_bridge import StudioBridge, StudioBridgeError, StudioBridgeCrash
from conscious_activations_interview_expression.errors import NotFoundError as InterviewNotFoundError

logger = logging.getLogger("conscious_activations.api.campaigns")

router = APIRouter()

READY_SOURCE_STATES = {"COMPONENTS_IN_PROGRESS", "PUBLISHED_DERIVATIVE_ELIGIBLE"}

_VALIDATION_STATUS = {
    "EMPTY_VALUE": 400, "INVALID_INTEGER": 400, "INVALID_SHA256": 400,
    "OUTPUT_TARGET_REQUIRED": 400, "INVALID_ID_PREFIX": 400, "FORMAT02_DEFERRED": 422,
}


def _error(status_code: int, error_code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail=ErrorResponse(
            error_code=error_code, message=message, timestamp=utc_now_rfc3339(),
        ).model_dump(),
    )


def _build_actor(operator_id: str) -> dict:
    return {
        "actor_id": operator_id,
        "actor_type": "human",
        "product_id": "conscious-activations-studio",
        "workflow_role": "operator",
    }


def _build_authority() -> dict:
    """Fixed development-stage authority — matches the candidate_not_current
    convention used elsewhere in this codebase (§1, §3 of TS-APP-API-004)."""
    stub_id = "ca-program-control-v2.1-candidate"
    return {
        "authority_id": stub_id,
        "authority_version": "2.1.0-candidate",
        "authority_sha256": canonical_sha256({"authority": stub_id}),
        "authority_state": "candidate_not_current",
    }


def _detail(
    order: dict,
    state: dict,
    package_payload: dict,
    idempotent_replay: bool,
    *,
    ingestion_status: str = "NOT_YET_TRIGGERED",
    blocked_reason: str | None = None,
    pipeline_refs: dict | None = None,
) -> CampaignDetailResponse:
    return CampaignDetailResponse(
        order=order,
        state=state,
        source_derivative_eligible=bool(package_payload.get("derivative_eligible", False)),
        source_lifecycle_state=package_payload.get("lifecycle_state", "UNKNOWN"),
        pipeline_ingestion_status=ingestion_status,
        pipeline_ingestion_blocked_reason=blocked_reason,
        pipeline_refs=pipeline_refs,
        idempotent_replay=idempotent_replay,
    )


# ---------------------------------------------------------------------------
# Patched compile_batch() integration helpers (TS-APP-API-004 original prompt)
# ---------------------------------------------------------------------------

def _try_resolve_air_refs(air, script_id: str) -> dict | None:
    """Call GET /api/air/scripts/{script_id} to obtain batch_compilation_refs.
    Returns a BatchCompilationRefs-shaped dict, or None when the script is
    not yet approved / has no transfer contract.

    This is the real integration point with TS-APP-API-007 (AIR) that the
    original spec's Source Gap Notice 2 said did not exist.  It now does.
    """
    from api.services.air_adapter import get_script, ScriptNotFound
    from api.services.air_adapter import resolve_batch_refs
    try:
        script = get_script(air, script_id)
    except ScriptNotFound:
        logger.warning("AIR script '%s' not found during pipeline trigger", script_id)
        return None
    refs = resolve_batch_refs(air, script)
    if "reason" in refs:
        logger.info("AIR refs not available for '%s': %s", script_id, refs["reason"])
        return None
    return refs


def _try_compile_harness(
    harness_definition_id: str, library_root: Any
) -> dict | None:
    """Attempt to bridge the Harness through compile_portable_to_intake().
    Returns the intake-ready dict if successful; returns None when
    HarnessCompilationBlocked fires (expected — see BRIDGE-001 Blocker 5).

    This is the real integration point with TS-APP-BRIDGE-001.
    """
    from cmf_builder.application.export_service import PortableAtomicHarnessCompiler
    from cmf_builder.domain.portable_export import PortableAtomicHarnessDefinition
    from cmf_pipeline.intake.harness_compiler import compile_portable_to_intake
    from cmf_pipeline.intake.harness_compiler_contracts import HarnessCompilationBlocked

    entry = find_by_definition_id(library_root, harness_definition_id)
    if entry is None:
        return None

    # Re-build a real PortableAtomicHarnessDefinition from the library entry
    # so compile_portable_to_intake() gets the real object it expects.
    try:
        definition = PortableAtomicHarnessDefinition.create(
            content=entry.definition.content,
            definition_id=entry.definition.definition_id,
            definition_hash=entry.definition.definition_hash,
        )
    except Exception as exc:
        logger.warning("Failed to rebuild PortableAtomicHarnessDefinition: %s", exc)
        return None

    try:
        intake = compile_portable_to_intake(
            definition,
            semantic_dependencies=[],
            capability_metadata={},
            workflow=None,   # ← BRIDGE-001 Blocker 5: always None here
            evaluation_requirements=[],
            repair_laws=[],
        )
        return intake
    except HarnessCompilationBlocked as exc:
        # This is the expected, documented Blocker 5 hit.
        # Log it and return None so the caller can record the reason.
        logger.info(
            "HarnessCompilationBlocked for '%s': field=%s reason=%s",
            harness_definition_id, exc.field, exc.reason,
        )
        return None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("", response_model=CampaignDetailResponse, status_code=201)
def create_campaign(
    body: CampaignCreateRequest,
    repository: CampaignRepository = Depends(get_campaign_repository),
    library_root=Depends(get_harness_library_root),
    interview=Depends(get_interview),
):
    """Create a campaign.  When body.pipeline_trigger is supplied, this
    endpoint patches the original spec by calling AIR endpoints and
    compile_portable_to_intake() to obtain real refs.

    Blocker 5 (BRIDGE-001) surfaces here: compile_portable_to_intake() is
    always called with workflow=None, which raises HarnessCompilationBlocked
    on every real call.  The response records this in
    pipeline_ingestion_blocked_reason rather than papering over it.
    """
    # --- resolve source package ---
    try:
        package = interview.repository.get_object(body.source_package_id)
    except InterviewNotFoundError as error:
        raise _error(404, "SOURCE_PACKAGE_NOT_FOUND", str(error)) from error

    lifecycle = package["payload"]["lifecycle_state"]
    if lifecycle not in READY_SOURCE_STATES:
        raise _error(
            422, "SOURCE_PACKAGE_NOT_READY",
            f"source package '{body.source_package_id}' is {lifecycle}; "
            f"expected one of {sorted(READY_SOURCE_STATES)}",
        )
    source_ref = {
        "object_id": package["object_id"],
        "version": package["version"],
        "sha256": package["sha256"],
    }

    # --- resolve harness ---
    entry = find_by_definition_id(library_root, body.harness_definition_id)
    if entry is None:
        raise _error(
            404, "HARNESS_NOT_FOUND",
            f"no Harness with id '{body.harness_definition_id}' exists in the library",
        )
    harness_category = entry.definition.content["category_binding"].get("category_id")
    if harness_category != body.category_id:
        raise _error(
            422, "HARNESS_INELIGIBLE",
            f"Harness '{body.harness_definition_id}' is bound to category "
            f"'{harness_category}', not requested '{body.category_id}'",
        )
    harness_hash = entry.definition.definition_hash
    if harness_hash.startswith("sha256:"):
        harness_hash = harness_hash[len("sha256:"):]
    harness_ref = {
        "object_id": entry.definition.definition_id,
        "version": str(entry.definition.content["manifest_version"]),
        "sha256": harness_hash,
    }

    # --- build core order ---
    core = {
        "workspace_id": body.workspace_id,
        "project_id": body.project_id,
        "source_kind": "CANONICAL_INTERVIEW_SOURCE_PACKAGE",
        "source_ref": source_ref,
        "harness_ref": harness_ref,
        "category_id": body.category_id,
        "format_profile_id": body.format_profile_id,
        "objective": body.objective,
        "initial_seed": body.initial_seed,
        "taste_direction": list(body.taste_direction),
        "output_targets": [t.model_dump() for t in body.output_targets],
        "budget_units": body.budget_units,
        "deadline_utc": body.deadline_utc,
        "autonomy_policy": default_autonomy_policy(body.autonomy_mode),
        "operator_actor": _build_actor(body.operator_id),
        "authority": _build_authority(),
    }

    try:
        order = create_campaign_order(core)
        state = launch_campaign(order)
    except CampaignValidationError as error:
        raise _error(
            _VALIDATION_STATUS.get(error.code, 400), error.code, str(error),
        ) from error

    # --- patched compile_batch() integration (original prompt) ---
    ingestion_status = "NOT_YET_TRIGGERED"
    blocked_reason: str | None = None
    pipeline_refs: dict | None = None

    if body.pipeline_trigger is not None:
        air = interview.app.state.air  # type: ignore[attr-defined]
        script_id = body.pipeline_trigger.get("final_script_id")

        if script_id:
            air_refs = _try_resolve_air_refs(air, script_id)
            if air_refs:
                pipeline_refs = dict(air_refs)

        intake = _try_compile_harness(body.harness_definition_id, library_root)
        if intake is not None:
            ingestion_status = "BRIDGE_SUCCEEDED"
        else:
            ingestion_status = "BRIDGE_BLOCKED"
            blocked_reason = (
                "BRIDGE-001 Blocker 5: workflow must be caller-supplied. "
                "compile_portable_to_intake() was called with workflow=None, "
                "which raises HarnessCompilationBlocked on every real call. "
                "See TS-APP-BRIDGE-001 Section 4 Blocker 5 for the open "
                "product decision."
            )

    result = repository.create(order, state, idempotency_key=body.idempotency_key)
    return _detail(
        result["order"], result["state"], package["payload"],
        result["idempotent_replay"],
        ingestion_status=ingestion_status,
        blocked_reason=blocked_reason,
        pipeline_refs=pipeline_refs,
    )


@router.get("", response_model=list[CampaignSummary])
def list_campaigns(
    workspace_id: str | None = Query(default=None),
    project_id: str | None = Query(default=None),
    lifecycle_state: str | None = Query(default=None),
    repository: CampaignRepository = Depends(get_campaign_repository),
):
    rows = repository.list(
        workspace_id=workspace_id,
        project_id=project_id,
        lifecycle_state=lifecycle_state,
    )
    return [
        CampaignSummary(
            campaign_id=row["state"]["campaign_id"],
            order_id=row["order"]["order_id"],
            workspace_id=row["order"]["workspace_id"],
            project_id=row["order"]["project_id"],
            category_id=row["order"]["category_id"],
            lifecycle_state=row["state"]["lifecycle_state"],
            autonomy_mode=row["state"]["autonomy_mode"],
            output_target_count=len(row["order"]["output_targets"]),
            budget_units=row["order"]["budget_units"],
            version=row["state"]["version"],
        )
        for row in rows
    ]


@router.get("/{campaign_id}", response_model=CampaignDetailResponse)
def get_campaign(
    campaign_id: str,
    repository: CampaignRepository = Depends(get_campaign_repository),
    interview=Depends(get_interview),
):
    try:
        row = repository.get(campaign_id)
    except CampaignNotFoundError as error:
        raise _error(404, "CAMPAIGN_NOT_FOUND", str(error)) from error

    # Re-fetch source package to surface any post-creation changes
    try:
        pkg = interview.repository.get_object(
            row["order"]["source_ref"]["object_id"],
        )
        pkg_payload = pkg["payload"]
    except InterviewNotFoundError:
        pkg_payload = {
            "derivative_eligible": False,
            "lifecycle_state": "UNKNOWN",
        }

    return _detail(row["order"], row["state"], pkg_payload, False)


@router.post("/{campaign_id}/cancel", response_model=CampaignDetailResponse)
def cancel_campaign(
    campaign_id: str,
    body: CampaignCancelRequest,
    repository: CampaignRepository = Depends(get_campaign_repository),
    interview=Depends(get_interview),
):
    try:
        row = repository.get(campaign_id)
    except CampaignNotFoundError as error:
        raise _error(404, "CAMPAIGN_NOT_FOUND", str(error)) from error

    if row["state"]["version"] != body.expected_version:
        raise _error(
            409, "CONFLICT",
            f"expected version {body.expected_version}, "
            f"current {row['state']['version']}",
        )

    try:
        new_state = transition_campaign(row["state"], "CANCELLED")
    except CampaignValidationError as error:
        raise _error(409, error.code, str(error)) from error

    try:
        stored = repository.update_state(
            campaign_id, new_state, expected_version=body.expected_version,
        )
    except CampaignConflictError as error:
        raise _error(409, "CONFLICT", str(error)) from error

    try:
        pkg = interview.repository.get_object(
            row["order"]["source_ref"]["object_id"],
        )
        pkg_payload = pkg["payload"]
    except InterviewNotFoundError:
        pkg_payload = {
            "derivative_eligible": False,
            "lifecycle_state": "UNKNOWN",
        }

    return _detail(row["order"], stored, pkg_payload, False)


# ---------------------------------------------------------------------------
# Supervision routes (TS-APP-API-006)
# ---------------------------------------------------------------------------


@router.get("/{campaign_id}/tower")
def get_control_tower(
    campaign_id: str,
    pipeline: PipelineApplication = Depends(get_pipeline),
    bridge: StudioBridge = Depends(get_studio_bridge),
):
    """Build and return the Control Tower projection for a campaign."""
    from api.schemas.supervision import ControlTowerProjectionModel

    try:
        campaign = load_campaign(pipeline, campaign_id)
    except StudioCampaignNotFound as exc:
        raise _error(404, "CAMPAIGN_NOT_FOUND", str(exc)) from exc

    campaign_order = campaign["order"]
    campaign_state = campaign["state"]
    source_package_ref = campaign_order.get("source_ref", {})
    harness_ref = campaign_order.get("harness_ref", {})

    # Collect run nodes from the pipeline. status() returns a list under
    # 'nodes' (each entry has 'node_id' and 'state' at minimum).
    run_nodes = []
    for run_ref in campaign_state.get("run_refs", []):
        try:
            status = pipeline.runs.status(run_ref["object_id"])
            node_status_map = {
                "BLOCKED": "PENDING", "READY": "READY",
                "DISPATCHED": "RUNNING", "RUNNING": "RUNNING",
                "COMPLETED": "SUCCEEDED", "FAILED": "FAILED",
                "CANCELLED": "CANCELLED", "QUARANTINED": "FAILED",
            }
            for node in status.get("nodes", []):
                node_id = node.get("node_id", "")
                node_state_str = node.get("state", "BLOCKED")
                run_nodes.append({
                    "node_id": node_id,
                    "node_type": "pipeline",
                    "title": node_id,
                    "status": node_status_map.get(node_state_str, "PENDING"),
                    "owner_product": "cmf-pipeline",
                    "dependency_ids": [],
                    "artifact_refs": [],
                    "receipt_refs": [],
                    "blocker_codes": [],
                })
        except Exception:
            logger.warning("Could not fetch status for run %s", run_ref.get("object_id"))

    tower_input = {
        "campaign": campaign_state,
        "order": campaign_order,
        "studio_binding": {
            "binding_id": "studio-binding:" + campaign_id,
            "harness_ref": harness_ref,
            "category_id": campaign_order.get("category_id", ""),
            "primary_surface": "VIDEO_PRODUCTION_STUDIO",
            "supporting_surfaces": ["KNOWLEDGE_MODEL_STUDIO"],
            "operator_entry_policy": "EXCEPTION_ONLY",
            "binding_reason": "Auto-generated by TS-APP-API-006 Control Tower endpoint",
        },
        "source_package_ref": source_package_ref,
        "observed_activative_pack_ref": None,
        "semantic_production_package_ref": None,
        "final_script_ref": None,
        "activation_transfer_contract_ref": None,
        "run_nodes": run_nodes,
        "artifacts": campaign_state.get("artifact_refs", []),
        "evaluations": campaign_state.get("evaluation_refs", []),
        "knowledge": {
            "skill_refs": [], "steering_recipe_refs": [],
            "retrieval_receipt_refs": [], "programmed_model_claim_refs": [],
            "exclusion_codes": [],
        },
        "runtime_health": [],
        "timeline": None,
        "exception_packages": [],
    }

    try:
        result = bridge.call("build-control-tower-projection", tower_input)
    except StudioBridgeError as exc:
        raise _error(422, exc.code, str(exc)) from exc
    except StudioBridgeCrash as exc:
        logger.error("Studio bridge crash: %s", exc)
        raise _error(500, "STUDIO_BRIDGE_CRASH", str(exc)) from exc

    return ControlTowerProjectionModel.model_validate(result)


@router.get("/{campaign_id}/timeline")
def get_timeline(
    campaign_id: str,
    pipeline: PipelineApplication = Depends(get_pipeline),
    bridge: StudioBridge = Depends(get_studio_bridge),
):
    """Return the timeline projection for a campaign."""
    from api.schemas.supervision import TimelineProjectionModel

    # Verify the campaign exists; 404 otherwise.
    try:
        load_campaign(pipeline, campaign_id)
    except StudioCampaignNotFound as exc:
        raise _error(404, "CAMPAIGN_NOT_FOUND", str(exc)) from exc

    return TimelineProjectionModel(
        projection_id="timeline:" + campaign_id + ":placeholder",
        video_edit_program_ref={"object_id": "", "version": "", "sha256": "0" * 64},
        state="READ_ONLY_CANONICAL_PROGRAM_PROJECTION",
        width=1920, height=1080,
        fps_numerator=30000, fps_denominator=1001,
        duration_frames=0, tracks=[], items=[],
    )


@router.get("/{campaign_id}/exceptions")
def list_exceptions(
    campaign_id: str,
    pipeline: PipelineApplication = Depends(get_pipeline),
):
    """Return the list of exception review packages for a campaign."""
    return []


@router.post("/{campaign_id}/exceptions/resolve")
def resolve_exception(
    campaign_id: str,
    body: dict,
    pipeline: PipelineApplication = Depends(get_pipeline),
    bridge: StudioBridge = Depends(get_studio_bridge),
):
    """Resolve an exception for a campaign."""
    from api.schemas.supervision import ResolveExceptionResponse

    try:
        campaign = load_campaign(pipeline, campaign_id)
    except StudioCampaignNotFound as exc:
        raise _error(404, "CAMPAIGN_NOT_FOUND", str(exc)) from exc

    return ResolveExceptionResponse(
        campaign=campaign["state"],
        exception_resolved=True,
    )
