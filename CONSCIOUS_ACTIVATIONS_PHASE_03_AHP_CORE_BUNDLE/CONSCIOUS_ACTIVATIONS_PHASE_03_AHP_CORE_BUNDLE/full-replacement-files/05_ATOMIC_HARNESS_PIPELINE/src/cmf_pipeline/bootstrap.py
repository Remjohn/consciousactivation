from __future__ import annotations

from pathlib import Path
from typing import Any

from .application import PipelineApplication


def status(database_path: str | Path | None = None) -> dict[str, Any]:
    return PipelineApplication(database_path).status()
