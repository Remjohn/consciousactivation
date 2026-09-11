from __future__ import annotations

import json
from fastapi import APIRouter, Depends, File, Form, Header, HTTPException, Request, UploadFile
from ca_contracts import bytes_sha256, utc_now_rfc3339

from cmf_activative_intelligence.application import AirApplication
from conscious_activations_interview_composer.application import InterviewComposerApplication
from conscious_activations_interview_composer.errors import (
    ConflictError, InterviewComposerError, NotFoundError, ValidationError,
)

from api.config import load_config
from api.dependencies import get_air, get_composer
from api.errors import ErrorResponse
from api.schemas import interview_composer as schemas
from api.services.composer_air_bridge import (
    BrandCrossReferenceError,
    compile_relationship_program,
    resolve_brand_voice_refs,
)
from api.services.media_store import save_upload

router = APIRouter()

_DOMAIN_ERROR_MAP = {
    ValidationError: (422, "VALIDATION_FAILED"),
    ConflictError: (409, "CONFLICT"),
    NotFoundError: (404, "NOT_FOUND"),
}


def _error(code: str, message: str, status: int) -> HTTPException:
    return HTTPException(status_code=status, detail=ErrorResponse(
        error_code=code, message=message, timestamp=utc_now_rfc3339(),
    ).model_dump())


def _domain_error_to_http(exc: InterviewComposerError) -> HTTPException:
    status_code, code = _DOMAIN_ERROR_MAP.get(type(exc), (500, "INTERNAL_ERROR"))
    return _error(code, str(exc), status_code)


VALID_CONTEXT_CLASSES = {
    "IDENTITY_DNA",
    "CONTEXT_PREMISE",
    "RESONANCE_REFERENCE",
    "BRAND_VOICE",
    "EVIDENCE_SOURCE",
    "INTERVIEW_RECORDING",
    "CAPTION_TRACK",
}


@router.post("/research", status_code=201, response_model=schemas.GuestResearchPackageResponse)
async def create_research_package(
    guest_name: str = Form(default=""),
    source_urls_json: str = Form("[]"),
    workspace_id: str = Form(default=""),
    project_id: str = Form(default=""),
    operator_id: str = Form(default=""),
    authority_scope: str = Form(default=""),
    assertion_id: str = Form(default=""),
    documents: list[UploadFile] = File(default=[]),
    document_metadata_json: str = Form("[]"),
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    composer: InterviewComposerApplication = Depends(get_composer),
):
    if not guest_name or not guest_name.strip():
        raise _error("GUEST_NAME_INVALID", "guest_name cannot be empty or whitespace only", 422)
    if not workspace_id or not workspace_id.strip():
        raise _error("WORKSPACE_REQUIRED", "workspace_id is required", 422)
    if not operator_id or not operator_id.strip() or not authority_scope or not authority_scope.strip() or not assertion_id or not assertion_id.strip():
        raise _error("AUTHORITY_REQUIRED", "operator_id, authority_scope, and assertion_id are required", 422)

    try:
        source_urls_raw = json.loads(source_urls_json)
    except json.JSONDecodeError as exc:
        raise _error("VALIDATION_FAILED", f"source_urls_json is not valid JSON: {exc}", 422) from exc

    try:
        doc_metadata_raw = json.loads(document_metadata_json) if document_metadata_json else []
    except json.JSONDecodeError as exc:
        raise _error("VALIDATION_FAILED", f"document_metadata_json is not valid JSON: {exc}", 422) from exc

    source_urls = []
    for item in source_urls_raw:
        if isinstance(item, str):
            source_urls.append(item)
        elif isinstance(item, dict) and "url" in item:
            source_urls.append(item["url"])

    config = load_config()
    uploaded = []
    for idx, doc in enumerate(documents):
        data = await doc.read()
        dest_path, logical_uri = save_upload(
            doc, media_root=config.ca_media_root,
            workspace_id=workspace_id, project_id=project_id,
        )
        meta = {}
        if isinstance(doc_metadata_raw, list) and idx < len(doc_metadata_raw) and isinstance(doc_metadata_raw[idx], dict):
            meta = doc_metadata_raw[idx]
        elif isinstance(doc_metadata_raw, dict):
            meta = doc_metadata_raw.get(doc.filename or "", {})

        context_class = meta.get("context_class")
        if not context_class:
            # Check if file is caption track by extension (.vtt, .srt)
            fname = (doc.filename or "").lower()
            if fname.endswith(".vtt") or fname.endswith(".srt"):
                context_class = "CAPTION_TRACK"
            else:
                context_class = "EVIDENCE_SOURCE"

        if context_class not in VALID_CONTEXT_CLASSES:
            raise _error("INVALID_CONTEXT_CLASS", f"Unknown context_class '{context_class}'. Must be one of {sorted(VALID_CONTEXT_CLASSES)}", 422)

        # Tiered limit checks per DEC-GST-001 v2
        fname = (doc.filename or "").lower()
        content_type = (doc.content_type or "").lower()
        if context_class == "CAPTION_TRACK":
            max_bytes = 10 * 1024 * 1024  # 10MB
        elif context_class == "INTERVIEW_RECORDING":
            if content_type.startswith("video/") or fname.endswith((".mp4", ".mov", ".mkv", ".webm")):
                max_bytes = 4 * 1024 * 1024 * 1024  # 4GB
            elif content_type in ("audio/wav", "audio/x-wav") or fname.endswith(".wav"):
                max_bytes = 1024 * 1024 * 1024  # 1GB
            elif content_type.startswith("audio/"):
                max_bytes = 500 * 1024 * 1024  # 500MB
            else:
                max_bytes = 4 * 1024 * 1024 * 1024
        else:
            max_bytes = 50 * 1024 * 1024  # 50MB Documents

        if len(data) > max_bytes:
            raise _error(
                "MEDIA_SIZE_EXCEEDED",
                f"File '{doc.filename}' ({len(data)} bytes) exceeds tier limit of {max_bytes} bytes for class '{context_class}'",
                422,
            )

        client_sha = meta.get("client_sha256")
        server_sha = bytes_sha256(data)
        if client_sha and client_sha.lower() != server_sha.lower():
            raise _error(
                "MEDIA_HASH_MISMATCH",
                f"Client SHA-256 mismatch for '{doc.filename}': provided {client_sha}, computed {server_sha}",
                422,
            )

        caption_for = meta.get("caption_for")
        brand_ref = meta.get("brand_ref")

        uploaded.append({
            "asset_id": logical_uri,
            "sha256": server_sha,
            "bytes": len(data),
            "media_type": doc.content_type or "application/octet-stream",
            "original_filename": doc.filename or "unnamed",
            "context_class": context_class,
            "caption_for": caption_for,
            "brand_ref": brand_ref,
        })

    # Validate caption_for references
    recording_identifiers = {
        u["asset_id"] for u in uploaded if u["context_class"] == "INTERVIEW_RECORDING"
    } | {
        u["original_filename"] for u in uploaded if u["context_class"] == "INTERVIEW_RECORDING"
    }

    for u in uploaded:
        if u["caption_for"]:
            target = u["caption_for"]
            if target not in recording_identifiers:
                raise _error(
                    "INVALID_CAPTION_TARGET",
                    f"caption_for '{target}' does not reference an asset with context_class 'INTERVIEW_RECORDING'",
                    422,
                )

    key = idempotency_key or f"research:{workspace_id}:{project_id}:{guest_name}"
    try:
        result = composer.research.create_package(
            {
                "workspace_id": workspace_id, "project_id": project_id,
                "guest_name": guest_name, "source_urls": source_urls,
                "uploaded_documents": uploaded,
                "composer_authority": {
                    "operator_id": operator_id,
                    "authority_scope": authority_scope,
                    "assertion_id": assertion_id,
                },
            },
            idempotency_key=key,
        )
    except InterviewComposerError as exc:
        raise _domain_error_to_http(exc) from exc
    payload = result["object"]["payload"]
    return schemas.GuestResearchPackageResponse(
        research_package_id=payload["research_package_id"],
        revision=result["object"]["revision"],
        guest_name=payload["guest_name"],
        source_urls=payload["source_urls"],
        uploaded_documents=payload["uploaded_documents"],
        idempotent_replay=result.get("idempotent_replay", False),
    )


@router.get("/research/{research_package_id}", response_model=schemas.GuestResearchPackageResponse)
def get_research_package(
    research_package_id: str,
    composer: InterviewComposerApplication = Depends(get_composer),
):
    try:
        stored = composer.repository.get_object(research_package_id)
    except NotFoundError as exc:
        raise _error("NOT_FOUND", str(exc), 404) from exc
    payload = stored["payload"]
    return schemas.GuestResearchPackageResponse(
        research_package_id=payload["research_package_id"],
        revision=stored["revision"],
        guest_name=payload["guest_name"],
        source_urls=payload["source_urls"],
        uploaded_documents=payload["uploaded_documents"],
        idempotent_replay=False,
    )


@router.post("/brief", status_code=201, response_model=schemas.ActivativeInterviewBriefResponse)
def create_brief(
    body: schemas.ComposeBriefRequest,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    composer: InterviewComposerApplication = Depends(get_composer),
    air: AirApplication = Depends(get_air),
):
    try:
        research = composer.repository.get_object(body.research_package_id)
    except NotFoundError as exc:
        raise _error("RESEARCH_PACKAGE_NOT_FOUND", str(exc), 404) from exc
    try:
        bcr = body.brand_context_ref.model_dump() if body.brand_context_ref else None
        vdr = body.voice_dna_ref.model_dump() if body.voice_dna_ref else None
        resolve_brand_voice_refs(air, brand_context_ref=bcr, voice_dna_ref=vdr)
    except BrandCrossReferenceError as exc:
        code = (
            "BRAND_VOICE_MISMATCH"
            if exc.field == "voice_dna_ref" and "belong" in str(exc)
            else (
                "BRAND_CONTEXT_NOT_FOUND"
                if exc.field == "brand_context_ref"
                else "VOICE_DNA_NOT_FOUND"
            )
        )
        status = 422 if code == "BRAND_VOICE_MISMATCH" else 404
        raise _error(code, str(exc), status) from exc
    research_ref = {
        "object_id": research["object_id"],
        "version": research["version"],
        "sha256": research["sha256"],
    }
    key = idempotency_key or f"brief:{body.research_package_id}:{body.guest_name}"
    try:
        result = composer.briefs.create_brief(
            {
                "research_package_ref": research_ref,
                "brand_context_ref": body.brand_context_ref.model_dump() if body.brand_context_ref else None,
                "voice_dna_ref": body.voice_dna_ref.model_dump() if body.voice_dna_ref else None,
                "guest_name": body.guest_name,
                "tension_hypothesis": body.tension_hypothesis,
                "matrix_of_edging_seed": body.matrix_of_edging_seed.model_dump(),
                "planned_questions": [q.model_dump() for q in body.planned_questions],
                "expression_targets": body.expression_targets,
                "composer_authority": {
                    "operator_id": body.operator_id,
                    "authority_scope": body.authority_scope,
                    "assertion_id": body.assertion_id,
                },
            },
            idempotency_key=key,
        )
    except InterviewComposerError as exc:
        raise _domain_error_to_http(exc) from exc
    return _brief_to_response(result)


def _brief_to_response(result: dict) -> schemas.ActivativeInterviewBriefResponse:
    payload = result["object"]["payload"]
    brief_ref = {
        "object_id": payload["brief_id"],
        "version": result["object"]["version"],
        "sha256": result["object"]["sha256"],
    }
    return schemas.ActivativeInterviewBriefResponse(
        brief_id=payload["brief_id"],
        revision=result["object"]["revision"],
        research_package_ref=payload["research_package_ref"],
        brand_context_ref=payload["brand_context_ref"],
        voice_dna_ref=payload["voice_dna_ref"],
        guest_name=payload["guest_name"],
        content_origin=payload["content_origin"],
        tension_hypothesis=payload["tension_hypothesis"],
        matrix_of_edging_seed=payload["matrix_of_edging_seed"],
        planned_questions=payload["planned_questions"],
        expression_targets=payload["expression_targets"],
        hypothesis_pipeline_status=payload["hypothesis_pipeline_status"],
        planning_lineage_template=schemas.PlanningLineageTemplate(
            brief_ref=brief_ref,
            planned_aip_ref=None,
            iac_ref=None,
            arm_receipt_ref=None,
            planned_object_digests=None,
        ),
        idempotent_replay=result.get("idempotent_replay", False),
    )


@router.get("/briefs/{brief_id}", response_model=schemas.ActivativeInterviewBriefResponse)
def get_brief(
    brief_id: str,
    composer: InterviewComposerApplication = Depends(get_composer),
):
    try:
        stored = composer.repository.get_object(brief_id)
    except NotFoundError as exc:
        raise _error("BRIEF_NOT_FOUND", str(exc), 404) from exc
    return _brief_to_response({"object": stored, "idempotent_replay": False})


@router.post("/sessions", status_code=201, response_model=schemas.ComposerSessionResponse)
def create_session(
    body: schemas.ComposeSessionRequest,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    composer: InterviewComposerApplication = Depends(get_composer),
    air: AirApplication = Depends(get_air),
):
    try:
        brief = composer.repository.get_object(body.brief_id)
    except NotFoundError as exc:
        raise _error("BRIEF_NOT_FOUND", str(exc), 404) from exc
    brief_ref = {
        "object_id": brief["object_id"],
        "version": brief["version"],
        "sha256": brief["sha256"],
    }
    research_payload = brief["payload"]["research_package_ref"]
    key = idempotency_key or f"session:{body.brief_id}"
    relationship_state_ref, progression_ref = compile_relationship_program(
        air,
        brief_ref=brief_ref,
        research_package_ref=research_payload,
        idempotency_key=key,
    )
    try:
        result = composer.sessions.create_session(
            brief_ref=brief_ref,
            relationship_state_ref=relationship_state_ref,
            progression_ref=progression_ref,
            recording_date=body.recording_date,
            composer_authority={
                "operator_id": body.operator_id,
                "authority_scope": body.authority_scope,
                "assertion_id": body.assertion_id,
            },
            idempotency_key=key,
        )
    except InterviewComposerError as exc:
        raise _domain_error_to_http(exc) from exc
    payload = result["object"]["payload"]
    return schemas.ComposerSessionResponse(
        session_id=payload["session_id"],
        revision=result["object"]["revision"],
        brief_ref=payload["brief_ref"],
        relationship_state_ref=payload["relationship_state_ref"],
        progression_ref=payload["progression_ref"],
        stage=payload["stage"],
        recording_date=payload["recording_date"],
        idempotent_replay=result.get("idempotent_replay", False),
    )


@router.get("/sessions/{session_id}", response_model=schemas.ComposerSessionResponse)
def get_session(
    session_id: str,
    composer: InterviewComposerApplication = Depends(get_composer),
):
    try:
        stored = composer.repository.get_object(session_id)
    except NotFoundError as exc:
        raise _error("SESSION_NOT_FOUND", str(exc), 404) from exc
    payload = stored["payload"]
    return schemas.ComposerSessionResponse(
        session_id=payload["session_id"],
        revision=stored["revision"],
        brief_ref=payload["brief_ref"],
        relationship_state_ref=payload["relationship_state_ref"],
        progression_ref=payload["progression_ref"],
        stage=payload["stage"],
        recording_date=payload["recording_date"],
        idempotent_replay=False,
    )