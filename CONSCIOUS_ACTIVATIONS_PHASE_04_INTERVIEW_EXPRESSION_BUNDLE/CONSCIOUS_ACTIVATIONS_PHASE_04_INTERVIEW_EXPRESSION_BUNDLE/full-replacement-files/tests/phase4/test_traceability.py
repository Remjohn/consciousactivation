from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRACE = ROOT / "CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/PHASE_04_INTERVIEW_EXPRESSION"


def rows(name: str) -> list[dict[str, str]]:
    with (TRACE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_phase4_spec_matrix_matches_exact_seven_specs() -> None:
    specs = rows("PHASE_04_SPEC_IMPLEMENTATION_MATRIX.csv")
    assert [row["spec_id"] for row in specs] == [f"TS-INT-{index:03d}" for index in range(1, 8)]
    assert all(row["full_spec_completed"].lower() == "false" for row in specs)
    for row in specs:
        path = ROOT / row["spec_path"]
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["spec_sha256"]
        assert (ROOT / row["test_path"]).is_file()


def test_phase4_acceptance_matrix_is_complete_and_conservative() -> None:
    criteria = rows("PHASE_04_ACCEPTANCE_TEST_MATRIX.csv")
    assert len(criteria) == 201
    allowed = {
        "DIRECT_ACCEPTANCE_TEST_EVIDENCE",
        "IMPLEMENTATION_PRESENT_NO_DIRECT_AC_TEST",
        "DEFERRED_NOT_IMPLEMENTED",
        "NOT_PROVEN_IN_PHASE_04",
    }
    assert {row["evidence_status"] for row in criteria} <= allowed
    assert all(row["spec_id"].startswith("TS-INT-") for row in criteria)
    assert all(row["criterion_id"] for row in criteria)
    for row in criteria:
        if row["evidence_status"] == "DIRECT_ACCEPTANCE_TEST_EVIDENCE":
            assert row["test_evidence"]


def test_phase4_completion_receipt_has_no_full_spec_or_production_claim() -> None:
    import yaml

    receipt = yaml.safe_load((TRACE / "COMPLETION_RECEIPT.yaml").read_text(encoding="utf-8"))
    assert receipt["specs_fully_completed"] == 0
    assert receipt["specs_partially_implemented"] == 7
    assert receipt["acceptance_criteria_total"] == 201
    assert receipt["production_authorized"] is False
    assert receipt["certified"] is False
    assert receipt["format02_activated"] is False
