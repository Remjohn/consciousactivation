from __future__ import annotations
import re
import shutil
from pathlib import Path
from fastapi import UploadFile

_UNSAFE = re.compile(r"[^A-Za-z0-9_.-]+")


def _sanitize(filename: str) -> str:
    name = Path(filename).name
    cleaned = _UNSAFE.sub("_", name)
    return cleaned or "upload.bin"


def save_upload(upload: UploadFile, *, media_root: Path, workspace_id: str, project_id: str) -> tuple[Path, str]:
    safe_name = _sanitize(upload.filename or "upload.bin")
    dest_dir = media_root / "interviews" / workspace_id / project_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / safe_name
    with dest_path.open("wb") as out:
        shutil.copyfileobj(upload.file, out)
    logical_uri = f"workspace://{workspace_id}/{project_id}/{safe_name}"
    return dest_path, logical_uri
