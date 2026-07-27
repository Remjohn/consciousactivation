"""Static safety guards for the CMF command spine."""

from __future__ import annotations

from pathlib import Path


FORBIDDEN_RUNTIME_COUPLING_MARKERS = [
    "legacy_runtime.",
    "old_bmad_runtime.",
    "ccp_legacy_runtime.",
]


def scan_for_legacy_runtime_coupling(paths: list[Path]) -> list[str]:
    """Return files that reference forbidden legacy runtime packages."""

    violations: list[str] = []
    for path in paths:
        if not path.exists() or not path.is_file() or path.suffix != ".py":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if any(marker in text for marker in FORBIDDEN_RUNTIME_COUPLING_MARKERS):
            violations.append(str(path))
    return violations

