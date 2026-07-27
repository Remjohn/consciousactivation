from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for path in reversed([
    ROOT / "tests" / "phase3",
    ROOT / "tests" / "phase2",
    ROOT / "tests" / "phase1",
    ROOT / "packages" / "ca_contracts" / "src",
    ROOT / "packages" / "ca_runtime" / "src",
    ROOT / "04_ACTIVATIVE_INTELLIGENCE_RUNTIME" / "src",
    ROOT / "05_ATOMIC_HARNESS_PIPELINE" / "src",
    ROOT / "06_INTERVIEW_EXPRESSION" / "src",
]):
    value = str(path)
    if value not in sys.path:
        sys.path.insert(0, value)

AUTHORITY = {
    "authority_id": "ca-program-control-v2.1-candidate",
    "authority_version": "2.1.0-candidate",
    "authority_sha256": "a" * 64,
    "authority_state": "candidate_not_current",
}


def ref(object_id: str, sha: str | None = None, version: str = "1.0.0") -> dict[str, str]:
    return {"object_id": object_id, "version": version, "sha256": sha or "b" * 64}


def base(object_id_field: str, object_id: str, *, epistemic: bool = True, lifecycle: bool = True) -> dict[str, object]:
    value: dict[str, object] = {
        object_id_field: object_id,
        "version": "1.0.0",
        "authority": dict(AUTHORITY),
    }
    if lifecycle:
        value["lifecycle_state"] = "approved"
    if epistemic:
        value["epistemic_state"] = "operator_confirmed"
    return value
