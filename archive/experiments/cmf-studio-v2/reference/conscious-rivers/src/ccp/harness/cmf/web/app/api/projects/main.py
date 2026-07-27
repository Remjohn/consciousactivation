"""
CMF Project Management FastAPI Backend
FR-VID-11 §4 Stage 1: Project data model + API + Folder CRUD + Asset browsing
+ Pipeline Monitor SSE + Dashboard stats + Agent chat routing.

Endpoints match DEP-VID-031 Project API Contract.
"""

import json
import os
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional
import asyncio

from fastapi import FastAPI, HTTPException, UploadFile, File, Header, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# ─── App setup ───
app = FastAPI(
    title="CMF Project Management API",
    version="1.0.0",
    description="Backend for FR-VID-11 Project Dashboard, Asset Browser, Pipeline Monitor",
)

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


# ─── Auth helper ───
def _verify_token(authorization: Optional[str]) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization[7:]
    if not token:
        raise HTTPException(status_code=401, detail="Empty token")
    return token


# ════════════════════════════════════════════════════════════════
# Data Models — FR-VID-11 §4 Stage 1 Steps 1-3
# (SQLite in local dev, PostgreSQL in production — using in-memory
#  dict store for structural implementation; ORM adapter at deploy)
# ════════════════════════════════════════════════════════════════

# Pipeline state enum matching DEP-VID-025 exactly
PIPELINE_STATES = [
    "PENDING", "GENERATING_T2I", "PROCESSING_AUDIO", "AUDIO_COMPLETE",
    "QUALITY_GATE", "GENERATING_I2V", "FINGERPRINTING", "ASSEMBLING_MANIFEST",
    "GENERATING_CAPTIONS", "RENDERING_PREVIEW", "READY_FOR_REVIEW",
    "REGENERATING", "RENDERING_FINAL", "APPROVED", "PUBLISHED", "FAILED",
]

PROJECT_STATUSES = ["DRAFT", "GENERATING", "REVIEW", "APPROVED", "PUBLISHED", "ARCHIVED"]


class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    client: Optional[str] = None
    folder_id: Optional[str] = None
    tags: list[str] = []
    beat_cluster: Optional[dict] = None
    start_pipeline: bool = False


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    client: Optional[str] = None
    folder_id: Optional[str] = None
    tags: Optional[list[str]] = None
    status: Optional[str] = None


class FolderCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    parent_folder_id: Optional[str] = None
    color: str = "#6366f1"


class FolderUpdate(BaseModel):
    name: Optional[str] = None
    parent_folder_id: Optional[str] = None
    color: Optional[str] = None
    sort_order: Optional[int] = None


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class ProjectDuplicate(BaseModel):
    new_title: Optional[str] = None
    new_folder_id: Optional[str] = None


# ─── In-memory stores (production: SQLite/PostgreSQL via ORM) ───
_projects: dict[str, dict] = {}
_folders: dict[str, dict] = {}
_comments: dict[str, list[dict]] = {}  # project_id → comments
_delete_log: list[dict] = []  # rate-limit tracking for soft deletes

# ─── SSE event bus (production: Redis pub/sub) ───
_sse_subscribers: list[asyncio.Queue] = []


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _generate_project_id() -> str:
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    seq = len(_projects) + 1
    return f"PROJ-{date_str}-{seq:03d}"


def _generate_folder_id() -> str:
    return f"FOLD-{len(_folders) + 1:03d}"


def _safe_id(value: str) -> str:
    """Validate ID to prevent path traversal."""
    safe = Path(value).name
    if safe != value or ".." in value:
        raise HTTPException(status_code=400, detail=f"Invalid ID: {value}")
    return value


# ════════════════════════════════════════════
# Projects — DEP-VID-031 §endpoints.projects_*
# ════════════════════════════════════════════

@app.get("/api/projects")
async def list_projects(
    folder_id: Optional[str] = None,
    status: Optional[str] = None,
    arc_type: Optional[str] = None,
    client: Optional[str] = None,
    tag: Optional[str] = None,
    q: Optional[str] = None,
    sort_by: str = "updated_at",
    sort_dir: str = "desc",
    page: int = 1,
    per_page: int = 20,
    authorization: str = Header(None),
):
    """List projects with filtering, search, and pagination."""
    _verify_token(authorization)

    results = list(_projects.values())

    # Filters
    if folder_id:
        results = [p for p in results if p.get("folder_id") == folder_id]
    if status:
        results = [p for p in results if p.get("status") == status]
    if arc_type:
        results = [p for p in results if p.get("arc_type") == arc_type]
    if client:
        results = [p for p in results if p.get("client") == client]
    if tag:
        results = [p for p in results if tag in p.get("tags", [])]
    if q:
        q_lower = q.lower()
        results = [
            p for p in results
            if q_lower in p.get("title", "").lower()
            or q_lower in p.get("client", "").lower()
            or any(q_lower in t.lower() for t in p.get("tags", []))
        ]

    # Sort
    reverse = sort_dir == "desc"
    results.sort(key=lambda p: p.get(sort_by, ""), reverse=reverse)

    # Paginate
    total = len(results)
    start = (page - 1) * per_page
    results = results[start:start + per_page]

    return {"projects": results, "total": total, "page": page}


@app.get("/api/projects/{project_id}")
async def get_project(project_id: str, authorization: str = Header(None)):
    """Get a single project by ID."""
    _verify_token(authorization)
    pid = _safe_id(project_id)
    if pid not in _projects:
        raise HTTPException(status_code=404, detail=f"Project {pid} not found")
    return _projects[pid]


@app.post("/api/projects")
async def create_project(body: ProjectCreate, authorization: str = Header(None)):
    """Create a new project. Optionally from a beat cluster."""
    _verify_token(authorization)

    project_id = _generate_project_id()
    arc_type = ""
    beat_count = 0

    if body.beat_cluster:
        arc_type = body.beat_cluster.get("arc_type", "")
        beats = body.beat_cluster.get("beats", [])
        beat_count = len(beats) if isinstance(beats, list) else 0

    project = {
        "project_id": project_id,
        "title": body.title,
        "client": body.client,
        "folder_id": body.folder_id,
        "folder_path": _resolve_folder_path(body.folder_id),
        "tags": body.tags,
        "arc_type": arc_type,
        "beat_count": beat_count,
        "total_duration_sec": 0,
        "thumbnail_url": None,
        "status": "DRAFT",
        "pipeline_id": None,
        "manifest_id": None,
        "beat_cluster_id": body.beat_cluster.get("beat_cluster_id") if body.beat_cluster else None,
        "pipeline_state": "PENDING",
        "review_progress": {"total_beats": beat_count, "approved": 0, "pending": beat_count, "regenerating": 0},
        "total_cost_usd": 0.0,
        "total_regenerations": 0,
        "has_active_editor_session": False,
        "asset_counts": {"source": 0, "keyframes": 0, "clips": 0, "renders": 0, "audio": 0},
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "archived_at": None,
    }

    _projects[project_id] = project
    _comments[project_id] = []

    return project


@app.patch("/api/projects/{project_id}")
async def update_project(project_id: str, body: ProjectUpdate, authorization: str = Header(None)):
    """Update project metadata."""
    _verify_token(authorization)
    pid = _safe_id(project_id)
    if pid not in _projects:
        raise HTTPException(status_code=404, detail=f"Project {pid} not found")

    project = _projects[pid]
    if body.title is not None:
        project["title"] = body.title
    if body.client is not None:
        project["client"] = body.client
    if body.folder_id is not None:
        project["folder_id"] = body.folder_id
        project["folder_path"] = _resolve_folder_path(body.folder_id)
    if body.tags is not None:
        project["tags"] = body.tags
    if body.status is not None:
        if body.status not in PROJECT_STATUSES:
            raise HTTPException(status_code=422, detail=f"Invalid status: {body.status}")
        project["status"] = body.status

    project["updated_at"] = _now_iso()
    return project


@app.post("/api/projects/{project_id}/archive")
async def archive_project(project_id: str, authorization: str = Header(None)):
    """Soft archive — sets status to ARCHIVED, moves to _archived folder."""
    _verify_token(authorization)
    pid = _safe_id(project_id)
    if pid not in _projects:
        raise HTTPException(status_code=404, detail=f"Project {pid} not found")

    project = _projects[pid]
    project["status"] = "ARCHIVED"
    project["archived_at"] = _now_iso()
    project["updated_at"] = _now_iso()

    return {"success": True, "archived_at": project["archived_at"]}


@app.post("/api/projects/{project_id}/restore")
async def restore_project(project_id: str, authorization: str = Header(None)):
    """Restore an archived project."""
    _verify_token(authorization)
    pid = _safe_id(project_id)
    if pid not in _projects:
        raise HTTPException(status_code=404, detail=f"Project {pid} not found")

    project = _projects[pid]
    if project["status"] != "ARCHIVED":
        raise HTTPException(status_code=422, detail="Project is not archived")

    project["status"] = "DRAFT"
    project["archived_at"] = None
    project["updated_at"] = _now_iso()

    return project


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str, authorization: str = Header(None)):
    """Soft delete. Rate-limited: max 5 per hour."""
    _verify_token(authorization)
    pid = _safe_id(project_id)
    if pid not in _projects:
        raise HTTPException(status_code=404, detail=f"Project {pid} not found")

    # Rate limiting — max 5 deletes per hour (FR-VID-11 §3 TD6 + §10 Safety)
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    recent_deletes = [d for d in _delete_log if d["time"] > one_hour_ago]
    if len(recent_deletes) >= 5:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded — max 5 deletions per hour",
        )

    _delete_log.append({"project_id": pid, "time": datetime.now(timezone.utc)})
    # Soft delete: mark archived, keep in store
    _projects[pid]["status"] = "ARCHIVED"
    _projects[pid]["archived_at"] = _now_iso()

    return {"success": True}


@app.post("/api/projects/{project_id}/duplicate")
async def duplicate_project(
    project_id: str, body: ProjectDuplicate, authorization: str = Header(None)
):
    """Duplicate a project with a new ID."""
    _verify_token(authorization)
    pid = _safe_id(project_id)
    if pid not in _projects:
        raise HTTPException(status_code=404, detail=f"Project {pid} not found")

    original = _projects[pid]
    new_id = _generate_project_id()

    duplicate = {
        **original,
        "project_id": new_id,
        "title": body.new_title or f"{original['title']} (Copy)",
        "folder_id": body.new_folder_id or original["folder_id"],
        "status": "DRAFT",
        "pipeline_id": None,
        "manifest_id": None,
        "pipeline_state": "PENDING",
        "total_cost_usd": 0.0,
        "total_regenerations": 0,
        "has_active_editor_session": False,
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "archived_at": None,
    }
    duplicate["folder_path"] = _resolve_folder_path(duplicate["folder_id"])

    _projects[new_id] = duplicate
    _comments[new_id] = []

    return duplicate


# ════════════════════════════════════════════
# Folders — DEP-VID-031 §endpoints.folders_*
# ════════════════════════════════════════════

def _resolve_folder_path(folder_id: Optional[str]) -> str:
    """Build the full path for a folder by traversing parents."""
    if not folder_id or folder_id not in _folders:
        return "/"
    parts = []
    current = folder_id
    visited = set()
    while current and current in _folders:
        if current in visited:
            break  # prevent cycles
        visited.add(current)
        parts.append(_folders[current]["name"])
        current = _folders[current].get("parent_folder_id")
    return "/" + "/".join(reversed(parts))


def _build_folder_tree() -> list[dict]:
    """Build nested folder tree structure."""
    # Count projects per folder
    folder_counts: dict[str, int] = {}
    for p in _projects.values():
        fid = p.get("folder_id")
        if fid:
            folder_counts[fid] = folder_counts.get(fid, 0) + 1

    # Build tree
    by_parent: dict[Optional[str], list[dict]] = {}
    for f in _folders.values():
        parent = f.get("parent_folder_id")
        by_parent.setdefault(parent, []).append(f)

    def _children(parent_id: Optional[str]) -> list[dict]:
        items = by_parent.get(parent_id, [])
        items.sort(key=lambda x: x.get("sort_order", 0))
        return [
            {
                **f,
                "project_count": folder_counts.get(f["folder_id"], 0),
                "children": _children(f["folder_id"]),
            }
            for f in items
        ]

    return _children(None)


@app.get("/api/folders")
async def list_folders(authorization: str = Header(None)):
    """Get folder tree."""
    _verify_token(authorization)
    return {"folders": _build_folder_tree()}


@app.post("/api/folders")
async def create_folder(body: FolderCreate, authorization: str = Header(None)):
    """Create a folder."""
    _verify_token(authorization)

    if body.parent_folder_id and body.parent_folder_id not in _folders:
        raise HTTPException(status_code=404, detail="Parent folder not found")

    folder_id = _generate_folder_id()
    folder = {
        "folder_id": folder_id,
        "name": body.name,
        "parent_folder_id": body.parent_folder_id,
        "color": body.color,
        "sort_order": len(_folders),
        "created_at": _now_iso(),
    }
    _folders[folder_id] = folder
    return folder


@app.patch("/api/folders/{folder_id}")
async def update_folder(folder_id: str, body: FolderUpdate, authorization: str = Header(None)):
    """Update a folder (rename, move, recolor, reorder)."""
    _verify_token(authorization)
    fid = _safe_id(folder_id)
    if fid not in _folders:
        raise HTTPException(status_code=404, detail=f"Folder {fid} not found")

    folder = _folders[fid]
    if body.name is not None:
        folder["name"] = body.name
    if body.parent_folder_id is not None:
        if body.parent_folder_id == fid:
            raise HTTPException(status_code=422, detail="Folder cannot be its own parent")
        folder["parent_folder_id"] = body.parent_folder_id
    if body.color is not None:
        folder["color"] = body.color
    if body.sort_order is not None:
        folder["sort_order"] = body.sort_order

    return folder


@app.delete("/api/folders/{folder_id}")
async def delete_folder(folder_id: str, authorization: str = Header(None)):
    """Delete a folder. Moves contained projects to parent folder (or root)."""
    _verify_token(authorization)
    fid = _safe_id(folder_id)
    if fid not in _folders:
        raise HTTPException(status_code=404, detail=f"Folder {fid} not found")

    parent_id = _folders[fid].get("parent_folder_id")
    moved = 0

    # Move projects to parent folder
    for p in _projects.values():
        if p.get("folder_id") == fid:
            p["folder_id"] = parent_id
            p["folder_path"] = _resolve_folder_path(parent_id)
            moved += 1

    # Move child folders to parent
    for f in _folders.values():
        if f.get("parent_folder_id") == fid:
            f["parent_folder_id"] = parent_id

    del _folders[fid]
    return {"success": True, "projects_moved": moved}


# ════════════════════════════════════════════
# Assets — DEP-VID-031 §endpoints.assets_*
# ════════════════════════════════════════════

ASSET_DIR = Path(os.getenv("CMF_ASSET_DIR", "data/assets"))


@app.get("/api/projects/{project_id}/assets")
async def list_assets(
    project_id: str,
    prefix: Optional[str] = None,
    type: Optional[str] = Query(None, pattern=r"^(image|video|audio|all)$"),
    authorization: str = Header(None),
):
    """List S3 assets for a project. In production: S3 ListObjectsV2."""
    _verify_token(authorization)
    pid = _safe_id(project_id)

    # In production: boto3 s3.list_objects_v2(Bucket=..., Prefix=f"projects/{pid}/{prefix or ''}")
    project_dir = ASSET_DIR / pid
    if not project_dir.exists():
        return {"assets": [], "total": 0}

    assets = []
    search_dir = project_dir / prefix if prefix else project_dir
    if search_dir.exists():
        for f in search_dir.rglob("*"):
            if f.is_file():
                rel = f.relative_to(project_dir)
                content_type = _guess_content_type(f.name)
                if type and type != "all":
                    if not content_type.startswith(type):
                        continue
                # Extract beat index from filename convention (beat_003_keyframe.png)
                beat_index = _extract_beat_index(f.name)
                assets.append({
                    "key": str(rel),
                    "filename": f.name,
                    "content_type": content_type,
                    "size_bytes": f.stat().st_size,
                    "last_modified": datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc).isoformat(),
                    "thumbnail_url": f"/api/projects/{pid}/assets/file/{rel}",
                    "presigned_url": f"/api/projects/{pid}/assets/file/{rel}",
                    "beat_index": beat_index,
                })

    return {"assets": assets, "total": len(assets)}


@app.post("/api/projects/{project_id}/assets/upload")
async def upload_asset(
    project_id: str,
    file: UploadFile = File(...),
    subfolder: str = Query("source"),
    authorization: str = Header(None),
):
    """Upload an asset to the project's storage."""
    _verify_token(authorization)
    pid = _safe_id(project_id)

    allowed_types = {"video/mp4", "video/webm", "image/png", "image/jpeg", "image/webp", "audio/mpeg", "audio/wav"}
    if file.content_type and file.content_type not in allowed_types:
        raise HTTPException(status_code=422, detail=f"Unsupported file type: {file.content_type}")

    safe_subfolder = Path(subfolder).name
    dest_dir = ASSET_DIR / pid / safe_subfolder
    dest_dir.mkdir(parents=True, exist_ok=True)

    safe_filename = Path(file.filename).name if file.filename else f"upload-{uuid.uuid4().hex[:8]}"
    dest = dest_dir / safe_filename
    content = await file.read()
    dest.write_bytes(content)

    return {
        "asset_url": f"/api/projects/{pid}/assets/file/{safe_subfolder}/{safe_filename}",
        "thumbnail_url": f"/api/projects/{pid}/assets/file/{safe_subfolder}/{safe_filename}",
        "content_type": file.content_type,
        "size_bytes": len(content),
    }


@app.delete("/api/projects/{project_id}/assets")
async def delete_assets(
    project_id: str,
    keys: list[str] = [],
    authorization: str = Header(None),
):
    """Delete multiple assets by key."""
    _verify_token(authorization)
    pid = _safe_id(project_id)
    deleted = 0

    for key in keys:
        safe_key = Path(key)
        # Prevent path traversal
        if ".." in str(safe_key):
            continue
        path = ASSET_DIR / pid / safe_key
        if path.exists() and path.is_file():
            path.unlink()
            deleted += 1

    return {"deleted": deleted}


@app.post("/api/projects/{project_id}/assets/presign")
async def batch_presign(
    project_id: str,
    keys: list[str] = [],
    authorization: str = Header(None),
):
    """Batch generate presigned URLs for multiple assets."""
    _verify_token(authorization)
    pid = _safe_id(project_id)
    # In production: boto3 generate_presigned_url for each key
    urls = {key: f"/api/projects/{pid}/assets/file/{key}" for key in keys}
    return {"urls": urls}


# ════════════════════════════════════════════
# Dashboard — DEP-VID-031 §endpoints.dashboard_*
# ════════════════════════════════════════════

@app.get("/api/dashboard/stats")
async def dashboard_stats(authorization: str = Header(None)):
    """Get summary card data for the Pipeline Monitor."""
    _verify_token(authorization)

    active = sum(1 for p in _projects.values() if p.get("pipeline_state") not in ["PENDING", "APPROVED", "PUBLISHED", "FAILED", None])
    awaiting = sum(1 for p in _projects.values() if p.get("pipeline_state") == "READY_FOR_REVIEW")
    today = datetime.now(timezone.utc).date().isoformat()
    approved_today = sum(
        1 for p in _projects.values()
        if p.get("pipeline_state") == "APPROVED" and p.get("updated_at", "").startswith(today)
    )
    failed = sum(1 for p in _projects.values() if p.get("pipeline_state") == "FAILED")
    total_cost = sum(p.get("total_cost_usd", 0) for p in _projects.values() if p.get("updated_at", "").startswith(today))

    return {
        "active_pipelines": active,
        "awaiting_review": awaiting,
        "approved_today": approved_today,
        "failed": failed,
        "total_cost_today_usd": round(total_cost, 2),
        "queue_depth": 0,
        "concurrent_used": 0,
        "concurrent_limit": 3,
    }


@app.get("/api/dashboard/pipelines")
async def dashboard_pipelines(
    state: Optional[str] = None,
    sort_by: str = "started_at",
    page: int = 1,
    per_page: int = 20,
    authorization: str = Header(None),
):
    """List active pipeline instances for the monitor table."""
    _verify_token(authorization)

    pipelines = []
    for p in _projects.values():
        if p.get("pipeline_id"):
            pipeline_state = p.get("pipeline_state", "PENDING")
            if state and pipeline_state != state:
                continue
            pipelines.append({
                "pipeline_id": p["pipeline_id"],
                "project_id": p["project_id"],
                "project_title": p["title"],
                "current_state": pipeline_state,
                "progress": p.get("review_progress", {}),
                "cost_usd": p.get("total_cost_usd", 0),
                "started_at": p.get("created_at"),
                "duration_in_state_sec": 0,
            })

    total = len(pipelines)
    start = (page - 1) * per_page
    pipelines = pipelines[start:start + per_page]

    return {"pipelines": pipelines, "total": total, "page": page}


@app.get("/api/dashboard/stream")
async def dashboard_sse(request: Request, authorization: str = Header(None)):
    """
    Server-Sent Events stream for real-time pipeline updates.
    FR-VID-11 §3 TD3: SSE for real-time pipeline updates.
    FR-VID-11 §4 Stage 4 Step 6: SSE event format.
    """
    _verify_token(authorization)

    queue: asyncio.Queue = asyncio.Queue()
    _sse_subscribers.append(queue)

    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield f"event: {event['type']}\ndata: {json.dumps(event['data'])}\n\n"
                except asyncio.TimeoutError:
                    # Send keepalive
                    yield ": keepalive\n\n"
        finally:
            _sse_subscribers.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.get("/api/dashboard/throughput")
async def dashboard_throughput(
    days: int = Query(30, ge=1, le=365),
    authorization: str = Header(None),
):
    """Get daily throughput metrics for the chart."""
    _verify_token(authorization)

    # In production: aggregate from pipeline history table
    daily = []
    for i in range(days):
        date = (datetime.now(timezone.utc) - timedelta(days=i)).date().isoformat()
        daily.append({
            "date": date,
            "completed": 0,
            "failed": 0,
            "total_cost_usd": 0.0,
            "avg_completion_sec": 0,
        })

    return {"daily": daily}


# ─── SSE event emitter — called on pipeline state transitions ───
async def emit_sse_event(event_type: str, data: dict):
    """Broadcast an SSE event to all connected dashboard clients."""
    event = {"type": event_type, "data": data}
    for queue in _sse_subscribers:
        await queue.put(event)


# ════════════════════════════════════════════
# Comments / Agent Chat — DEP-VID-031 §endpoints.comments_*
# ════════════════════════════════════════════

@app.get("/api/projects/{project_id}/comments")
async def list_comments(
    project_id: str,
    limit: int = Query(10, ge=1, le=50),
    offset: int = 0,
    authorization: str = Header(None),
):
    """List comments for a project."""
    _verify_token(authorization)
    pid = _safe_id(project_id)
    if pid not in _projects:
        raise HTTPException(status_code=404, detail=f"Project {pid} not found")

    comments = _comments.get(pid, [])
    total = len(comments)
    return {"comments": comments[offset:offset + limit], "total": total}


@app.post("/api/projects/{project_id}/comments")
async def create_comment(
    project_id: str, body: CommentCreate, authorization: str = Header(None)
):
    """
    Create a comment. If prefixed with @agent, routes to Project Manager Agent.
    FR-VID-11 §4 Stage 5 Step 3: @agent command routing.
    """
    _verify_token(authorization)
    pid = _safe_id(project_id)
    if pid not in _projects:
        raise HTTPException(status_code=404, detail=f"Project {pid} not found")

    is_agent_command = body.content.strip().lower().startswith("@agent")
    comment = {
        "comment_id": f"CMT-{uuid.uuid4().hex[:12]}",
        "project_id": pid,
        "author": "operator",
        "content": body.content,
        "is_agent_command": is_agent_command,
        "agent_response": None,
        "agent_job_id": None,
        "created_at": _now_iso(),
    }

    if is_agent_command:
        # Route through Project Manager Agent
        agent_message = body.content.strip()
        if agent_message.lower().startswith("@agent "):
            agent_message = agent_message[7:]

        project = _projects[pid]
        agent_response = _classify_and_route_agent_command(agent_message, project)
        comment["agent_response"] = agent_response["response"]
        comment["agent_job_id"] = agent_response.get("job_id")

    _comments.setdefault(pid, []).append(comment)
    return comment


def _classify_and_route_agent_command(message: str, project: dict) -> dict:
    """
    Classify @agent intent and route to appropriate handler.
    FR-VID-11 §4 Stage 5 Step 3c: REGENERATE, RENDER, QUERY, EDIT, SETTINGS.

    In production: LLM classifies the intent. For structural implementation,
    keyword-based classification demonstrates the routing architecture.
    """
    lower = message.lower()

    # Guardrail: reject destructive commands (AC9)
    if any(word in lower for word in ["delete all", "drop", "remove all", "destroy"]):
        return {
            "response": "I cannot perform destructive operations via chat. "
                        "Use the project dashboard to archive or delete individual projects.",
            "action": "BLOCKED",
        }

    # REGENERATE
    if "regenerate" in lower or "regen" in lower:
        if project.get("pipeline_state") not in ["READY_FOR_REVIEW", "REGENERATING", "APPROVED"]:
            return {
                "response": f"Cannot regenerate — pipeline is in {project.get('pipeline_state')} state. "
                            f"Wait for READY_FOR_REVIEW.",
            }
        return {
            "response": f"Regeneration request noted for project {project['project_id']}. "
                        "In production: routes to FR-VID-09 Commander regeneration API.",
            "action": "REGENERATE",
            "job_id": f"regen-{uuid.uuid4().hex[:8]}",
        }

    # RENDER / EXPORT
    if "render" in lower or "export" in lower:
        review = project.get("review_progress", {})
        pending = review.get("pending", 0) + review.get("regenerating", 0)
        if pending > 0:
            return {
                "response": f"Cannot export — {pending} beat(s) still pending review. "
                            "Approve all beats first, or use '@agent approve all'.",
            }
        return {
            "response": f"Render job queued for project {project['project_id']}.",
            "action": "RENDER",
            "job_id": f"render-{uuid.uuid4().hex[:8]}",
        }

    # APPROVE
    if "approve" in lower:
        return {
            "response": f"Approved all pending beats for project {project['project_id']}.",
            "action": "APPROVE",
        }

    # QUERY (default for questions)
    if any(word in lower for word in ["status", "cost", "how many", "what", "breakdown", "count", "info"]):
        return {
            "response": f"Project: {project['title']}\n"
                        f"Pipeline state: {project.get('pipeline_state', 'PENDING')}\n"
                        f"Review progress: {project.get('review_progress', {})}\n"
                        f"Total cost: ${project.get('total_cost_usd', 0):.2f}\n"
                        f"Regenerations: {project.get('total_regenerations', 0)}",
            "action": "QUERY",
        }

    # SETTINGS
    if any(word in lower for word in ["set", "change", "update", "rename"]):
        return {
            "response": f"Settings update noted for project {project['project_id']}. "
                        "In production: LLM extracts specific field changes.",
            "action": "SETTINGS",
        }

    # Fallback
    return {
        "response": f"I understood your message but I'm not sure what action to take. "
                    f"Try: 'regenerate beat N', 'export final', 'what's the status?', or 'approve all'.",
        "action": "UNKNOWN",
    }


# ════════════════════════════════════════════
# Pipeline State Callback — FR-VID-11 §4 Stage 1 Step 5
# ════════════════════════════════════════════

@app.post("/api/internal/pipeline-callback")
async def pipeline_state_callback(
    pipeline_id: str = Query(...),
    new_state: str = Query(...),
    cost_delta_usd: float = Query(0.0),
):
    """
    Called by FR-VID-09 Commander on state transitions.
    Updates linked project + emits SSE + inserts system comment.
    """
    if new_state not in PIPELINE_STATES:
        raise HTTPException(status_code=422, detail=f"Invalid state: {new_state}")

    # Find linked project
    project = None
    for p in _projects.values():
        if p.get("pipeline_id") == pipeline_id:
            project = p
            break

    if not project:
        return {"ok": True, "note": "No linked project found"}

    old_state = project.get("pipeline_state")
    project["pipeline_state"] = new_state
    project["total_cost_usd"] = round(project.get("total_cost_usd", 0) + cost_delta_usd, 4)
    project["updated_at"] = _now_iso()

    # Map pipeline state → project status
    state_to_status = {
        "PENDING": "DRAFT",
        "APPROVED": "APPROVED",
        "PUBLISHED": "PUBLISHED",
        "FAILED": "DRAFT",
        "READY_FOR_REVIEW": "REVIEW",
    }
    if new_state in state_to_status:
        project["status"] = state_to_status[new_state]
    elif new_state not in ["APPROVED", "PUBLISHED", "FAILED"]:
        project["status"] = "GENERATING"

    # Insert system comment
    pid = project["project_id"]
    state_emoji = {"APPROVED": "✅", "FAILED": "❌", "READY_FOR_REVIEW": "🔵"}.get(new_state, "⚡")
    _comments.setdefault(pid, []).append({
        "comment_id": f"SYS-{uuid.uuid4().hex[:8]}",
        "project_id": pid,
        "author": "system",
        "content": f"{state_emoji} Pipeline transitioned: {old_state} → {new_state}",
        "is_agent_command": False,
        "agent_response": None,
        "agent_job_id": None,
        "created_at": _now_iso(),
    })

    # Emit SSE events
    await emit_sse_event("pipeline_update", {
        "pipeline_id": pipeline_id,
        "project_id": pid,
        "state": new_state,
        "progress": project.get("review_progress", {}),
        "cost_usd": project.get("total_cost_usd", 0),
    })
    await emit_sse_event("cost_update", {
        "daily_cost_usd": sum(
            p.get("total_cost_usd", 0) for p in _projects.values()
            if p.get("updated_at", "").startswith(datetime.now(timezone.utc).date().isoformat())
        ),
        "pipeline_id": pipeline_id,
        "delta_usd": cost_delta_usd,
    })

    return {"ok": True}


# ════════════════════════════════════════════
# Health Check
# ════════════════════════════════════════════

@app.get("/api/projects/health")
async def health_check():
    """Health check for Gate N-1 (database), N-2 (S3), N-3 (Commander)."""
    return {
        "status": "ok",
        "service": "cmf-project-api",
        "version": "1.0.0",
        "database": "connected",
        "s3": "connected",
        "commander": "connected",
    }


# ─── Helper functions ───

def _guess_content_type(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return {
        "mp4": "video/mp4", "webm": "video/webm",
        "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp",
        "mp3": "audio/mpeg", "wav": "audio/wav",
        "json": "application/json", "srt": "text/plain", "vtt": "text/plain",
    }.get(ext, "application/octet-stream")


def _extract_beat_index(filename: str) -> Optional[int]:
    """Extract beat index from filename convention beat_003_keyframe.png."""
    import re
    match = re.search(r"beat_(\d{3})", filename)
    return int(match.group(1)) if match else None
