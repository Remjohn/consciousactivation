from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from cmf_delegation_validators.lifecycle import validate_sequence
from cmf_delegation_validators.paths import FIXTURES_ROOT, ROOT


SCENARIOS = FIXTURES_ROOT / "format02" / "scenarios"


@pytest.mark.parametrize("scenario_path", sorted(SCENARIOS.glob("SCN-*.json")))
def test_format02_scenario_evidence_is_executable(scenario_path: Path) -> None:
    scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
    assert scenario["scenario_id"] == scenario_path.stem
    assert scenario["fixture_profile"] == "FORMAT02_REFERENCE"
    if scenario["lifecycle_sequence"]:
        assert validate_sequence(scenario["lifecycle_sequence"]) == scenario["expected_terminal_state"]
    else:
        assert scenario["expected_terminal_state"] == scenario["expected_initial_state"]
    for item in scenario["message_sequence"]:
        fixture = ROOT / item["fixture_ref"]
        actual = "sha256:" + hashlib.sha256(fixture.read_bytes()).hexdigest()
        assert actual == item["fixture_hash"]
    expected = scenario["assertions"]["audit"]["expected_sequence"]
    committed = [
        item["audit_sequence"] for item in expected if item["receipt_mode"] != "REUSED"
    ]
    assert committed == list(range(1, len(committed) + 1))
    for item in expected:
        if item["receipt_mode"] == "REUSED":
            originals = [
                candidate
                for candidate in expected
                if candidate["message_id"] == item["message_id"]
                and candidate["receipt_mode"] == "ORIGINAL"
            ]
            assert len(originals) == 1
            assert item["audit_sequence"] == originals[0]["audit_sequence"]
    assert all(item["duplicate_domain_effect_allowed"] is False for item in scenario["assertions"]["outbox"]["expected_deliveries"])
    constitutional_scenarios = {"SCN-01", "SCN-02", "SCN-05", "SCN-08", "SCN-09", "SCN-10"}
    if scenario["scenario_id"] in constitutional_scenarios:
        assert scenario["assertions"]["constitutional"]
    else:
        assert "constitutional" not in scenario["assertions"]
