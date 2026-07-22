"""
CMF Editor FastAPI Backend Bridge
FR-VID-10 §4 Stage 9: HTTP API between React frontend and Python backend
for manifest CRUD, generation triggers, render requests, FFmpeg operations,
asset management, and AI Copilot LLM proxy.

Endpoints match DEP-VID-029 Editor API Contract.
"""

import json
import os
import uuid
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, UploadFile, File, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ─── App setup ───
app = FastAPI(
    title="CMF Editor API",
    version="1.0.0",
    description="Backend bridge for FR-VID-10 CMF Editor",
)

# CORS — Stage 9 Step 4: Allow localhost:3000 (Next.js dev) + production domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        os.getenv("CMF_PRODUCTION_ORIGIN", "https://app.cmf.video"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Storage path (local filesystem; S3 adapter in production) ───
MANIFEST_DIR = Path(os.getenv("CMF_MANIFEST_DIR", "data/manifests"))
ASSET_DIR = Path(os.getenv("CMF_ASSET_DIR", "data/assets"))
MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
ASSET_DIR.mkdir(parents=True, exist_ok=True)


# ─── Auth helper — Stage 9 Step 3 ───
def _verify_token(authorization: Optional[str]) -> str:
    """Extract and verify bearer token. Returns user_id."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization[7:]
    # Token validation delegates to CMF auth system (FR-VID-09)
    # For local development, accept any non-empty token
    if not token:
        raise HTTPException(status_code=401, detail="Empty token")
    return token


# ─── Request/Response Models ───

class ManifestPatchOp(BaseModel):
    op: str = Field(..., pattern=r"^(add|remove|replace|move|copy|test)$")
    path: str
    value: Any = None


class RegenerationRequest(BaseModel):
    beat_index: int = Field(..., ge=0)
    mode: str = Field(..., pattern=r"^(T2I_ONLY|I2V_ONLY|BOTH)$")
    revision_note: Optional[str] = None


class RenderRequest(BaseModel):
    quality_tier: str = Field(..., pattern=r"^(preview|review|final)$")
    platform_preset: str
    include_captions: bool = True
    export_srt: bool = False


class FFmpegTrimRequest(BaseModel):
    input_url: str
    start_sec: float = Field(..., ge=0)
    end_sec: float = Field(..., gt=0)


class FFmpegConcatRequest(BaseModel):
    input_urls: list[str] = Field(..., min_length=2)


class FFmpegExtractAudioRequest(BaseModel):
    input_url: str


class CopilotRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    manifest: dict
    conversation_history: list[dict] = []


class ErrorResponse(BaseModel):
    """Consistent error format per Stage 9 Step 5."""
    error: str
    code: str
    details: Optional[dict] = None


# ─── In-memory job store (production: Redis/DB) ───
_jobs: dict[str, dict] = {}


def _manifest_path(video_id: str) -> Path:
    """Resolve manifest file path. Validates video_id to prevent path traversal."""
    safe_id = Path(video_id).name  # strip any directory components
    if safe_id != video_id or ".." in video_id:
        raise HTTPException(status_code=400, detail="Invalid video_id")
    return MANIFEST_DIR / f"{safe_id}.json"


# ════════════════════════════════════════════
# Manifest CRUD — DEP-VID-029 §endpoints.manifest_*
# ════════════════════════════════════════════

@app.get("/api/editor/{video_id}/manifest")
async def get_manifest(video_id: str, authorization: str = Header(None)):
    """GET manifest JSON for a video. Source: filesystem (S3 in production)."""
    _verify_token(authorization)
    path = _manifest_path(video_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Manifest not found for {video_id}")
    return json.loads(path.read_text(encoding="utf-8"))


@app.put("/api/editor/{video_id}/manifest")
async def save_manifest(video_id: str, manifest: dict, authorization: str = Header(None)):
    """PUT full manifest JSON. Writes to filesystem + updates timestamp."""
    _verify_token(authorization)
    path = _manifest_path(video_id)

    # Basic schema validation — beats array must exist
    if "beats" not in manifest or not isinstance(manifest.get("beats"), list):
        raise HTTPException(status_code=422, detail="Manifest must contain a 'beats' array")

    from datetime import datetime, timezone
    manifest["last_saved_at"] = datetime.now(timezone.utc).isoformat()

    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


@app.patch("/api/editor/{video_id}/manifest")
async def patch_manifest(
    video_id: str,
    operations: list[ManifestPatchOp],
    authorization: str = Header(None),
):
    """
    Apply JSON Patch (RFC 6902) to the manifest.
    Validates patch, applies, saves, returns updated manifest.
    """
    _verify_token(authorization)
    path = _manifest_path(video_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Manifest not found for {video_id}")

    manifest = json.loads(path.read_text(encoding="utf-8"))

    # Apply each patch operation
    for op in operations:
        segments = [s for s in op.path.split("/") if s]
        if not segments:
            raise HTTPException(status_code=422, detail=f"Empty patch path")

        if op.op == "replace":
            target = manifest
            for seg in segments[:-1]:
                key = int(seg) if seg.isdigit() else seg
                if isinstance(target, list) and isinstance(key, int):
                    if key < 0 or key >= len(target):
                        raise HTTPException(status_code=422, detail=f"Index {key} out of range")
                    target = target[key]
                elif isinstance(target, dict):
                    if key not in target:
                        raise HTTPException(status_code=422, detail=f"Key '{key}' not found")
                    target = target[key]
                else:
                    raise HTTPException(status_code=422, detail=f"Cannot traverse path {op.path}")

            last = int(segments[-1]) if segments[-1].isdigit() else segments[-1]
            if isinstance(target, list) and isinstance(last, int):
                if last < 0 or last >= len(target):
                    raise HTTPException(status_code=422, detail=f"Index {last} out of range")
                target[last] = op.value
            elif isinstance(target, dict):
                target[last] = op.value
            else:
                raise HTTPException(status_code=422, detail=f"Cannot set value at {op.path}")
        elif op.op == "add":
            # Add operation for arrays
            target = manifest
            for seg in segments[:-1]:
                key = int(seg) if seg.isdigit() else seg
                target = target[key] if isinstance(target, dict) else target[int(key)]
            last = segments[-1]
            if last == "-" and isinstance(target, list):
                target.append(op.value)
            elif isinstance(target, dict):
                target[last] = op.value
        elif op.op == "remove":
            target = manifest
            for seg in segments[:-1]:
                key = int(seg) if seg.isdigit() else seg
                target = target[key] if isinstance(target, dict) else target[int(key)]
            last = int(segments[-1]) if segments[-1].isdigit() else segments[-1]
            if isinstance(target, list) and isinstance(last, int):
                target.pop(last)
            elif isinstance(target, dict):
                del target[last]
        else:
            raise HTTPException(status_code=422, detail=f"Unsupported op: {op.op}")

    # Validate frame math after patch
    beats = manifest.get("beats", [])
    expected_start = 0
    for i, beat in enumerate(beats):
        if beat.get("start_frame") != expected_start:
            raise HTTPException(
                status_code=422,
                detail=f"Frame math error: beat {i} start_frame should be {expected_start}, got {beat.get('start_frame')}",
            )
        expected_start += beat.get("duration_frames", 0)

    from datetime import datetime, timezone
    manifest["last_saved_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


# ════════════════════════════════════════════
# Generation — DEP-VID-029 §endpoints.regenerate_*
# ════════════════════════════════════════════

@app.post("/api/editor/{video_id}/regenerate")
async def start_regeneration(
    video_id: str,
    request: RegenerationRequest,
    authorization: str = Header(None),
):
    """
    Trigger beat-level regeneration via Pipeline Commander (FR-VID-09).
    Routes to FR-VID-05 → FR-VID-02/03/04.
    """
    _verify_token(authorization)

    job_id = f"regen-{uuid.uuid4().hex[:12]}"
    _jobs[job_id] = {
        "type": "regeneration",
        "video_id": video_id,
        "beat_index": request.beat_index,
        "mode": request.mode,
        "revision_note": request.revision_note,
        "status": "PENDING",
    }

    # In production: dispatch to Pipeline Commander via internal API
    # commander.dispatch_regeneration(video_id, request.beat_index, request.mode, request.revision_note)

    return {"job_id": job_id}


@app.get("/api/editor/{video_id}/regenerate/{job_id}")
async def poll_regeneration(
    video_id: str, job_id: str, authorization: str = Header(None)
):
    """Poll regeneration job status."""
    _verify_token(authorization)

    job = _jobs.get(job_id)
    if not job or job["video_id"] != video_id:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    return {
        "status": job["status"],
        "result_manifest": job.get("result_manifest"),
    }


# ════════════════════════════════════════════
# Rendering — DEP-VID-029 §endpoints.render_*
# ════════════════════════════════════════════

@app.post("/api/editor/{video_id}/render")
async def start_render(
    video_id: str,
    request: RenderRequest,
    authorization: str = Header(None),
):
    """
    Trigger render job via FR-VID-08 render orchestrator.
    Body specifies quality tier, platform preset, caption options.
    """
    _verify_token(authorization)

    job_id = f"render-{uuid.uuid4().hex[:12]}"
    _jobs[job_id] = {
        "type": "render",
        "video_id": video_id,
        "quality_tier": request.quality_tier,
        "platform_preset": request.platform_preset,
        "include_captions": request.include_captions,
        "export_srt": request.export_srt,
        "status": "PENDING",
        "progress_pct": 0,
    }

    # In production: dispatch to FR-VID-08 render orchestrator
    # render_orchestrator.start(video_id, request.quality_tier, request.platform_preset, ...)

    return {"job_id": job_id}


@app.get("/api/editor/{video_id}/render/{job_id}")
async def poll_render_status(
    video_id: str, job_id: str, authorization: str = Header(None)
):
    """Poll render job status with progress percentage."""
    _verify_token(authorization)

    job = _jobs.get(job_id)
    if not job or job["video_id"] != video_id:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    return {
        "status": job["status"],
        "progress_pct": job.get("progress_pct", 0),
        "output_url": job.get("output_url"),
        "file_size_mb": job.get("file_size_mb"),
    }


# ════════════════════════════════════════════
# FFmpeg Operations — DEP-VID-029 §endpoints.ffmpeg_*
# ════════════════════════════════════════════

@app.post("/api/editor/ffmpeg/trim")
async def ffmpeg_trim(request: FFmpegTrimRequest, authorization: str = Header(None)):
    """Trim a clip server-side. Returns URL of trimmed output."""
    _verify_token(authorization)
    if request.end_sec <= request.start_sec:
        raise HTTPException(status_code=422, detail="end_sec must be greater than start_sec")

    # In production: invoke FFmpeg subprocess
    # output_path = ffmpeg.trim(request.input_url, request.start_sec, request.end_sec)
    output_url = f"/api/editor/assets/trimmed-{uuid.uuid4().hex[:8]}.mp4"
    return {"output_url": output_url}


@app.post("/api/editor/ffmpeg/concat")
async def ffmpeg_concat(request: FFmpegConcatRequest, authorization: str = Header(None)):
    """Concatenate multiple clips server-side."""
    _verify_token(authorization)
    output_url = f"/api/editor/assets/concat-{uuid.uuid4().hex[:8]}.mp4"
    return {"output_url": output_url}


@app.post("/api/editor/ffmpeg/extract-audio")
async def ffmpeg_extract_audio(
    request: FFmpegExtractAudioRequest, authorization: str = Header(None)
):
    """Extract audio waveform data for visualization."""
    _verify_token(authorization)
    # In production: decode audio, compute waveform samples
    waveform_data = [0.0] * 100  # placeholder
    return {"waveform_data": waveform_data}


# ════════════════════════════════════════════
# Assets — DEP-VID-029 §endpoints.asset_*
# ════════════════════════════════════════════

@app.post("/api/editor/{video_id}/assets/upload")
async def upload_asset(
    video_id: str,
    file: UploadFile = File(...),
    authorization: str = Header(None),
):
    """Upload asset file (video or image). Returns asset URL."""
    _verify_token(authorization)

    # Validate file type
    allowed_types = {"video/mp4", "video/webm", "image/png", "image/jpeg", "image/webp"}
    if file.content_type and file.content_type not in allowed_types:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported file type: {file.content_type}. Allowed: {allowed_types}",
        )

    # Save to local storage (S3 in production)
    safe_video_id = Path(video_id).name
    video_asset_dir = ASSET_DIR / safe_video_id
    video_asset_dir.mkdir(parents=True, exist_ok=True)

    safe_filename = Path(file.filename).name if file.filename else f"upload-{uuid.uuid4().hex[:8]}"
    dest = video_asset_dir / safe_filename
    content = await file.read()
    dest.write_bytes(content)

    asset_url = f"/api/editor/{video_id}/assets/{safe_filename}"
    return {"asset_url": asset_url}


@app.get("/api/editor/{video_id}/assets/search")
async def search_assets(
    video_id: str,
    q: str = Query(..., min_length=1, max_length=200),
    source: str = Query("local", pattern=r"^(pexels|pixabay|local)$"),
    authorization: str = Header(None),
):
    """Search E-Roll library (Pexels, Pixabay, local). Returns results."""
    _verify_token(authorization)

    # In production: delegate to CMF Hunters (Pexels/Pixabay APIs) or local asset index
    results: list[dict] = []
    return {"results": results}


# ════════════════════════════════════════════
# AI Copilot — DEP-VID-029 §endpoints.copilot_chat
# ════════════════════════════════════════════

@app.post("/api/editor/copilot")
async def copilot_chat(request: CopilotRequest, authorization: str = Header(None)):
    """
    Send chat message + manifest to LLM for classified edit routing.
    Returns edit_class, intent_summary, and patch (for local edits)
    or regeneration params (for generative edits).
    """
    _verify_token(authorization)

    # Construct system prompt per FR-VID-10 §4 Stage 8 Step 2
    system_prompt = (
        "You are the CMF Editor Copilot. You receive a video manifest JSON and a user editing instruction. "
        "Return a JSON object with `edit_class` (one of EC-01 through EC-13 per EDIT_TAXONOMY.md), "
        "`intent_summary`, and for local edits (EC-01 through EC-09) a `patch` array (RFC 6902 format). "
        "For generative edits (EC-10, EC-11, EC-12), return `edit_class`, `intent_summary`, `beat_index`, "
        "`regeneration_mode`, and `revision_note` — do NOT return a patch. "
        "Validate frame math: start_frame values must be cumulative sums of previous durations."
    )

    # In production: call configured LLM (OpenAI/Gemini/local)
    # response = await llm_client.chat(system_prompt, request.message, request.manifest, request.conversation_history)

    # Placeholder response — in production this is replaced by actual LLM call
    return {
        "edit_class": "EC-13",
        "intent_summary": "LLM integration pending — configure CMF_LLM_API_KEY",
        "patch": [],
        "summary": "LLM backend not yet configured. Set CMF_LLM_API_KEY environment variable.",
    }


# ════════════════════════════════════════════
# Health Check
# ════════════════════════════════════════════

@app.get("/api/editor/health")
async def health_check():
    """Health check endpoint for Gate M question 6 (backend connectivity)."""
    return {"status": "ok", "service": "cmf-editor-api", "version": "1.0.0"}
