from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for path in reversed([
    ROOT / "packages" / "ca_contracts" / "src",
    ROOT / "packages" / "ca_runtime" / "src",
    ROOT / "04_ACTIVATIVE_INTELLIGENCE_RUNTIME" / "src",
    ROOT / "05_ATOMIC_HARNESS_PIPELINE" / "src",
    ROOT / "06_INTERVIEW_EXPRESSION" / "src",
]):
    value = str(path)
    if value not in sys.path:
        sys.path.insert(0, value)
