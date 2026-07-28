from __future__ import annotations
import json
from typing import Literal
from fastapi import APIRouter, Depends, File, Form, Header, HTTPException, UploadFile

from ca_contracts import utc_now_rfc3339
from conscious_activations_interview_expression.application import InterviewExpressionApplication
from conscious_activations_interview_expression.errors import (
    ConflictError, InterviewExpressionError, NotFoundError, StateError, ValidationError,
)

from api.config import load_config
from api.dependencies import get_interview
from api.errors import ErrorResponse
from api.schemas.interviews import ComponentSlotSummary, ImportInterviewResponse, InterviewStatusResponse
from api.services.media_store import save_upload
from api.services.transcript_ingest import (
    TranscriptFormatError, load_pre_aligned_transcript, parse_srt_transcript,
)

router = APIRouter()

DEFAULT_PHRASE_POLICY = {"policy_id": "phrase-pack-import-v1", "max_words": 12, "max_gap_ms": 800, "break_on_terminal_punctuation": True}
DEFAULT_VISUAL_PROFILE = "single-shot-import-v1"

_DOMAIN_ERROR_MAP = {
    ValidationError: (422, "VALIDATION_FAILED"),
    ConflictError: (409, "CONFLICT"),
    NotFoundError: (404, "NOT_FOUND"),
    StateError: (409, "STATE_INVALID"),
}


def _http_error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail=ErrorResponse(error_code=code, message=message, timestamp=utc_now_rfc3339()).model_dump(),
    )


def _domain_error_to_http(exc: InterviewExpressionError) -> HTTPException:
    status_code, code = _DOMAIN_ERROR_MAP.get(type(exc), (500, "INTERNAL_ERROR"))
    return _http_error(status_code, code, str(exc))


def _inspect_media(interview: InterviewExpressionApplication, video: UploadFile, *, workspace_id: str, project_id: str, media_root) -> dict:
    dest_path, logical_uri = save_upload(video, media_root=media_root, workspace_id=workspace_id, project_id=project_id)
    # NOTE ON DEVIATION FROM THE SPEC'S LITERAL STAGE-4 CODE:
    # media.py's MediaInspector.inspect() -> domain.make_media_asset() enforces
    # `bytes_count >= 1` (via require_int(..., minimum=1)) *before* ffprobe's
    # probe_status is ever inspected. A zero-byte upload (AC-008's corrupt.mp4)
    # therefore makes .inspect() itself raise a domain ValidationError -- the
    # probe_status/duration_ms check below never runs for that file. Read
    # literally, the spec's Stage-4 code lets that ValidationError propagate to
    # the endpoint's generic `except InterviewExpressionError` handler, which
    # maps it to 422 VALIDATION_FAILED -- not the 422 MEDIA_PROBE_FAILED AC-008
    # requires. Catching ValidationError here and remapping it keeps the
    # user-facing contract AC-008 actually specifies ("not valid media ... 422
    # MEDIA_PROBE_FAILED") without changing services/interview/ at all.
    try:
        media_asset = interview.media.inspect(dest_path, logical_uri=logical_uri, media_type=video.content_type or "video/mp4")
    except ValidationError as exc:
        raise _http_error(422, "MEDIA_PROBE_FAILED", f"uploaded file could not be probed: {exc}") from exc
    if media_asset["technical"].get("probe_status") != "PROBED" or media_asset["technical"].get("duration_ms", 0) < 1:
        raise _http_error(422, "MEDIA_PROBE_FAILED", "uploaded file could not be probed for duration/streams (ffprobe unavailable or file is corrupt)")
    return media_asset


def _ingest_transcript(transcript: UploadFile, *, transcript_format: str, speaker_id: str | None) -> tuple[list[dict], list[dict], str]:
    raw = transcript.file.read()
    if transcript_format == "PRE_ALIGNED_JSON":
        words, segments = load_pre_aligned_transcript(raw)
        return words, segments, "external-pre-aligned-v1"
    if transcript_format == "SRT":
        if not speaker_id:
            raise _http_error(422, "VALIDATION_FAILED", "speaker_id is required when transcript_format=SRT")
        words, segments = parse_srt_transcript(raw, speaker_id=speaker_id)
        return words, segments, "srt-even-split-v1"
    raise _http_error(422, "UNSUPPORTED_TRANSCRIPT_FORMAT", f"transcript_format '{transcript_format}' is not supported; use PRE_ALIGNED_JSON or SRT")


def _bind_if_needed(interview: InterviewExpressionApplication, package_id: str, component_name: str, component_ref: dict, *, idempotency_key: str) -> None:
    # NOTE ON DEVIATION FROM THE SPEC'S LITERAL STAGE-4 CODE:
    # bind_component() recomputes its FULL target package payload from
    # whatever the repository's CURRENT row for package_id happens to be --
    # it is not a pure function of (package_id, component_name, ref) alone.
    # admit()/align()/pack_phrases()/visual.compile() are genuinely
    # content-addressed (their object_id is a semantic_id hash of their
    # inputs), so replaying them under the same derived idempotency key after
    # a fully-completed prior run correctly short-circuits. bind_component
    # does not have that luxury: on a full retry of an already-fully-bound
    # package, the "current" state read at bind time already has every slot
    # bound, so the payload bind_component would submit under the fixed
    # "...:bind-<slot>" key no longer matches the payload recorded under that
    # same key during the original run (which only had that one slot bound at
    # the time) -- the repository's idempotency-key cache raises CONFLICT
    # before store_object's own content-addressing ever gets a chance to run.
    # Confirmed via the verification harness: AC-011's identical-retry
    # scenario hits exactly this 409 on the very first bind_component call.
    # Checking whether the slot is already bound to this exact ref before
    # calling bind_component avoids the collision without touching
    # services/interview/ at all, and preserves the same observable
    # behaviour (same package_id, idempotent_replay derived from admit()).
    current = interview.repository.get_object(package_id)
    slot = current["payload"]["components"].get(component_name)
    if slot and slot.get("state") == "BOUND" and slot.get("ref") == dict(component_ref):
        return
    interview.source_packages.bind_component(package_id, component_name, component_ref, idempotency_key=idempotency_key)


def _run_admission_pipeline(interview: InterviewExpressionApplication, *, command: dict, words: list[dict], segments: list[dict], policy_id: str, visual_profile_id: str, key: str) -> dict:
    admitted = interview.source_packages.admit(command, idempotency_key=f"{key}:admit")
    package_ref = interview.source_packages.ref(admitted)

    aligned = interview.transcripts.align(source_package_ref=package_ref, words=words, speaker_segments=segments, policy_id=policy_id, idempotency_key=f"{key}:align")
    alignment_ref = interview.source_packages.ref(aligned)
    packed = interview.transcripts.pack_phrases(alignment_ref, policy=DEFAULT_PHRASE_POLICY, idempotency_key=f"{key}:pack")
    phrase_ref = interview.source_packages.ref(packed)
    _bind_if_needed(interview, package_ref["object_id"], "transcript_alignment", alignment_ref, idempotency_key=f"{key}:bind-alignment")
    _bind_if_needed(interview, package_ref["object_id"], "packed_phrase_transcript", phrase_ref, idempotency_key=f"{key}:bind-phrases")

    duration_ms = command["media_assets"][0]["technical"]["duration_ms"]
    visual = interview.visual.compile(source_package_ref=package_ref, duration_ms=duration_ms, shots=[], keyframe_candidates=[], profile_id=visual_profile_id, idempotency_key=f"{key}:visual")
    visual_ref = interview.source_packages.ref(visual)
    _bind_if_needed(interview, package_ref["object_id"], "visual_structure_index", visual_ref, idempotency_key=f"{key}:bind-visual")

    final = interview.repository.get_object(package_ref["object_id"])
    return {
        "package": final,
        "alignment_ref": alignment_ref,
        "phrase_pack_ref": phrase_ref,
        "visual_index_ref": visual_ref,
        "word_count": len(aligned["object"]["payload"]["words"]),
        "phrase_count": len(packed["object"]["payload"]["phrases"]),
        "shot_count": len(visual["object"]["payload"]["shots"]),
        "keyframe_count": len(visual["object"]["payload"]["keyframes"]),
        "idempotent_replay": bool(admitted.get("idempotent_replay", False)),
    }


def _to_response(result: dict) -> ImportInterviewResponse:
    payload = result["package"]["payload"]
    return ImportInterviewResponse(
        package_id=payload["package_id"], revision=result["package"]["revision"],
        lifecycle_state=payload["lifecycle_state"], admission_mode=payload["admission_mode"],
        derivative_eligible=payload["derivative_eligible"], planning_lineage=payload["planning_lineage"],
        transcript_alignment_ref=result["alignment_ref"], packed_phrase_transcript_ref=result["phrase_pack_ref"],
        visual_structure_index_ref=result["visual_index_ref"], word_count=result["word_count"],
        phrase_count=result["phrase_count"], shot_count=result["shot_count"], keyframe_count=result["keyframe_count"],
        idempotent_replay=result["idempotent_replay"],
    )


@router.post("/import", status_code=201, response_model=ImportInterviewResponse)
async def import_interview(
    video: UploadFile = File(...), transcript: UploadFile = File(...),
    workspace_id: str = Form(...), project_id: str = Form(...), operator_id: str = Form(...),
    authority_scope: str = Form(...), assertion_id: str = Form(...),
    transcript_format: Literal["PRE_ALIGNED_JSON", "SRT"] = Form(...),
    speaker_id: str | None = Form(None), visual_profile_id: str = Form(DEFAULT_VISUAL_PROFILE),
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    interview: InterviewExpressionApplication = Depends(get_interview),
):
    config = load_config()
    key = idempotency_key or f"import:{workspace_id}:{project_id}:{video.filename}"
    try:
        media_asset = _inspect_media(interview, video, workspace_id=workspace_id, project_id=project_id, media_root=config.ca_media_root)
        words, segments, policy_id = _ingest_transcript(transcript, transcript_format=transcript_format, speaker_id=speaker_id)
        command = {
            "workspace_id": workspace_id, "project_id": project_id, "admission_mode": "IMPORTED",
            "source_kind": "INTERVIEW_EXPRESSION", "media_assets": [media_asset],
            "source_authority": {"operator_id": operator_id, "authority_scope": authority_scope, "assertion_id": assertion_id},
            "planning_lineage": {"state": "ABSENT_NOT_CREATED"},
        }
        result = _run_admission_pipeline(interview, command=command, words=words, segments=segments, policy_id=policy_id, visual_profile_id=visual_profile_id, key=key)
    except InterviewExpressionError as exc:
        raise _domain_error_to_http(exc) from exc
    except TranscriptFormatError as exc:
        raise _http_error(422, "UNSUPPORTED_TRANSCRIPT_FORMAT", str(exc)) from exc
    return _to_response(result)


@router.post("/brief-led", status_code=201, response_model=ImportInterviewResponse)
async def brief_led_interview(
    video: UploadFile = File(...), transcript: UploadFile = File(...),
    workspace_id: str = Form(...), project_id: str = Form(...), operator_id: str = Form(...),
    authority_scope: str = Form(...), assertion_id: str = Form(...),
    transcript_format: Literal["PRE_ALIGNED_JSON", "SRT"] = Form(...),
    speaker_id: str | None = Form(None), visual_profile_id: str = Form(DEFAULT_VISUAL_PROFILE),
    planning_lineage_json: str = Form(...),
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    interview: InterviewExpressionApplication = Depends(get_interview),
):
    try:
        planning_lineage = json.loads(planning_lineage_json)
    except json.JSONDecodeError as exc:
        raise _http_error(422, "VALIDATION_FAILED", f"planning_lineage_json is not valid JSON: {exc}") from exc
    config = load_config()
    key = idempotency_key or f"brief-led:{workspace_id}:{project_id}:{video.filename}"
    try:
        media_asset = _inspect_media(interview, video, workspace_id=workspace_id, project_id=project_id, media_root=config.ca_media_root)
        words, segments, policy_id = _ingest_transcript(transcript, transcript_format=transcript_format, speaker_id=speaker_id)
        command = {
            "workspace_id": workspace_id, "project_id": project_id, "admission_mode": "BRIEF_LED",
            "source_kind": "INTERVIEW_EXPRESSION", "media_assets": [media_asset],
            "source_authority": {"operator_id": operator_id, "authority_scope": authority_scope, "assertion_id": assertion_id},
            "planning_lineage": planning_lineage,
        }
        result = _run_admission_pipeline(interview, command=command, words=words, segments=segments, policy_id=policy_id, visual_profile_id=visual_profile_id, key=key)
    except InterviewExpressionError as exc:
        raise _domain_error_to_http(exc) from exc
    except TranscriptFormatError as exc:
        raise _http_error(422, "UNSUPPORTED_TRANSCRIPT_FORMAT", str(exc)) from exc
    return _to_response(result)


@router.get("/{package_id}/status", response_model=InterviewStatusResponse)
def get_interview_status(package_id: str, interview: InterviewExpressionApplication = Depends(get_interview)):
    try:
        stored = interview.repository.get_object(package_id)
    except NotFoundError as exc:
        raise _http_error(404, "NOT_FOUND", str(exc)) from exc
    payload = stored["payload"]
    components = {}
    for name, slot in payload["components"].items():
        if slot["state"] == "BOUND":
            components[name] = ComponentSlotSummary(state=slot["state"], ref=slot["ref"])
        else:
            components[name] = ComponentSlotSummary(state=slot["state"], reason=slot.get("reason"))
    return InterviewStatusResponse(
        package_id=payload["package_id"], revision=stored["revision"],
        workspace_id=payload["workspace_id"], project_id=payload["project_id"],
        admission_mode=payload["admission_mode"], source_kind=payload["source_kind"],
        lifecycle_state=payload["lifecycle_state"], derivative_eligible=payload["derivative_eligible"],
        planning_lineage=payload["planning_lineage"], components=components,
        media_assets=[{"asset_id": m["asset_id"], "sha256": m["sha256"], "bytes": m["bytes"], "media_type": m["media_type"]} for m in payload["media_assets"]],
    )
