from __future__ import annotations

import sys
from pathlib import Path


def repo_root(start: Path | None = None) -> Path:
    cursor = (start or Path(__file__)).resolve()
    for candidate in [cursor, *cursor.parents]:
        if (candidate / "CMF_PROGRAM_CONTROL").is_dir() and (candidate / "01_ATOMIC_HARNESS_BUILDER").is_dir():
            return candidate
    raise RuntimeError("unable to locate Conscious Activations repository root")


def add_phase1_python_paths(root: Path) -> None:
    paths = [
        root / "packages" / "ca_contracts" / "src",
        root / "packages" / "ca_runtime" / "src",
        root / "04_ACTIVATIVE_INTELLIGENCE_RUNTIME" / "src",
        root / "05_ATOMIC_HARNESS_PIPELINE" / "src",
        root / "06_INTERVIEW_EXPRESSION" / "src",
    ]
    for path in reversed(paths):
        value = str(path)
        if value not in sys.path:
            sys.path.insert(0, value)
