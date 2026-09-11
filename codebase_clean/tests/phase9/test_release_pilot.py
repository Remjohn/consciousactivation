from __future__ import annotations

from pathlib import Path

from ca_release.guards import evaluate_format02_gate
from ca_release.pilot import run_phase9_pilot


def test_format02_remains_deferred():
    result = evaluate_format02_gate()
    assert result["decision"] == "DENIED_DEFERRED"
    assert result["format02_activated"] is False


def test_final_release_pilot(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    result = run_phase9_pilot(repo, tmp_path / "phase9")
    assert result["artifact_count"] == 5
    assert result["production_authorized"] is False
    assert result["certified"] is False
    assert result["format02_activated"] is False
    assert Path(result["release_evidence_zip"]).is_file()
    assert (tmp_path / "phase9" / "release" / "RELEASE_MANIFEST.json").is_file()
    assert (tmp_path / "phase9" / "PILOT_RECEIPT.json").is_file()
