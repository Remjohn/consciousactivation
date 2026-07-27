from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
STATUS = ROOT / "CMF_PROGRAM_CONTROL" / "03_PROGRAM_STATUS" / "PHASE_07_STUDIO_SUPERVISION"
STUDIO = ROOT / "07_CONSCIOUS_ACTIVATIONS_STUDIO"

EXPECTED_SPEC_HASHES = {
    "TS-CAS-001": "66afd1423145e6cb050ebcf188181649a35dfc2b0a1c4e01859cbf648ecfb7dc",
    "TS-CAS-002": "ae8458a925319fcf5fe416c5539b26aaa0852c2f497b78220d7180e480ff1e27",
    "TS-CAS-003": "2d8642d1b8e7f170732fbd293bc2d86997b3568756c5e686857e9c790f3f5841",
    "TS-CAS-004": "72cece250ffb7e6de8d14012145bba8fc2ed18b917e0ddd99c527159ab215435",
    "TS-CAS-005": "c69d45485d611d8fdd20d098dd99fbaa30c38d8d9915ac79bc9d4b3cf0337fc2",
    "TS-CAS-006": "02c053eceb3d71d564fbd20381211252d2476a42bf3f8ffd41055f45616100d3",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_exact_audited_spec_hashes_are_preserved() -> None:
    for spec_id, expected in EXPECTED_SPEC_HASHES.items():
        path = STUDIO / "docs" / "tech-specs" / f"{spec_id}.md"
        assert path.is_file(), spec_id
        assert sha256(path) == expected, spec_id


def test_phase7_spec_and_fr_traceability_is_complete() -> None:
    specs = read_csv(STATUS / "PHASE_07_SPEC_IMPLEMENTATION_MATRIX.csv")
    frs = read_csv(STATUS / "PHASE_07_FR_TEST_MATRIX.csv")
    acceptance = read_csv(STATUS / "PHASE_07_ACCEPTANCE_TEST_MATRIX.csv")
    assert {row["spec_id"] for row in specs} == set(EXPECTED_SPEC_HASHES)
    assert len(specs) == 6
    assert len(frs) == 17
    assert len(acceptance) == 36
    assert all(row["per_spec_status"] == "PARTIALLY_IMPLEMENTED" for row in specs)
    assert all(row["full_spec_completed"].lower() == "false" for row in specs)
    assert all(row["claim_ceiling"] == "PHASE_07_STUDIO_SUPERVISION_DEVELOPMENT_EVIDENCE" for row in specs)


def test_phase7_gap_and_completion_boundaries_are_truthful() -> None:
    gaps = yaml.safe_load((STATUS / "PHASE_07_GAP_LEDGER.yaml").read_text(encoding="utf-8"))
    receipt = yaml.safe_load((STATUS / "COMPLETION_RECEIPT.yaml").read_text(encoding="utf-8"))
    per_spec = yaml.safe_load((STATUS / "PER_SPEC_BUILD_STATUS.yaml").read_text(encoding="utf-8"))
    assert len(gaps["gaps"]) == 14
    assert sum(item["status"] == "DEFERRED" for item in gaps["gaps"]) == 1
    assert any("Format 02" in item["description"] for item in gaps["gaps"])
    assert receipt["claim_ceiling"] == "PHASE_07_STUDIO_SUPERVISION_DEVELOPMENT_EVIDENCE"
    assert receipt["production_authorized"] is False
    assert receipt["certified"] is False
    assert receipt["format02_active"] is False
    assert all(item["full_spec_completed"] is False for item in per_spec["specs"].values())


def test_contract_registry_is_closed_and_complete() -> None:
    registry = json.loads((STUDIO / "contracts" / "schemas" / "CONTRACT_REGISTRY.json").read_text(encoding="utf-8"))
    assert registry["version"] == "0.7.0-dev.1"
    assert len(registry["schemas"]) == 16
    for entry in registry["schemas"]:
        path = STUDIO / "contracts" / "schemas" / entry["path"]
        assert path.is_file()
        assert sha256(path) == entry["sha256"]
        schema = json.loads(path.read_text(encoding="utf-8"))
        assert schema.get("additionalProperties") is False
