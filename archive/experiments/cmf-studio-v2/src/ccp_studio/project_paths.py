"""Project-root path helpers for CMF Studio."""

from __future__ import annotations

from pathlib import Path


PROJECT_DIR_NAME = "THE CMF STUDIO"
PROJECT_SENTINELS = (
    "05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md",
    "product-brief-CMF_STUDIO-2026-06-19.md",
)


def discover_project_root(anchor: Path | None = None) -> Path:
    """Return the CMF Studio project root from parent or project cwd."""

    start = (anchor or Path.cwd()).resolve()
    if start.is_file():
        start = start.parent

    for candidate in (start, *start.parents):
        if _has_project_sentinels(candidate):
            return candidate
        child = candidate / PROJECT_DIR_NAME
        if _has_project_sentinels(child):
            return child

    package_root = Path(__file__).resolve().parents[2]
    if _has_project_sentinels(package_root):
        return package_root
    return start


def resolve_project_path(path: str | Path, project_root: Path | None = None) -> Path:
    """Resolve project-relative paths and legacy THE CMF STUDIO-prefixed refs."""

    candidate = Path(path)
    if candidate.is_absolute():
        return candidate

    root = (project_root or discover_project_root()).resolve()
    parts = candidate.parts
    if parts and parts[0] == PROJECT_DIR_NAME:
        candidate = Path(*parts[1:]) if len(parts) > 1 else Path()
    return root / candidate


def _has_project_sentinels(candidate: Path) -> bool:
    return candidate.exists() and all((candidate / sentinel).exists() for sentinel in PROJECT_SENTINELS)
