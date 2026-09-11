from __future__ import annotations

from pathlib import Path

from .application import InterviewComposerApplication


def status(database_path: str | Path | None = None) -> dict[str, object]:
    return InterviewComposerApplication(database_path).repository.health()
