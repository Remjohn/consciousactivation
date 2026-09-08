"""Wave 05 test support — path bootstrap for CA-M036 tests."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for path in reversed([
    ROOT / "tests" / "wave05",
    ROOT / "tests" / "phase3",
    ROOT / "tests" / "phase2",
    ROOT / "tests" / "phase1",
    ROOT / "packages" / "ca_contracts" / "src",
    ROOT / "packages" / "ca_runtime" / "src",
    ROOT / "services" / "world-intelligence" / "src",
    ROOT / "services" / "pipeline" / "src",
    ROOT / "services" / "interview" / "src",
]):
    value = str(path)
    if value not in sys.path:
        sys.path.insert(0, value)
