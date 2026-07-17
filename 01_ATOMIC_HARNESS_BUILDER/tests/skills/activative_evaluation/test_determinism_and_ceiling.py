from __future__ import annotations

from dataclasses import asdict
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).parents[3]
EVALUATION_ROOT = ROOT / "evaluation" / "skills" / "activative_intelligence_pack_compiler"
sys.path.insert(0, str(EVALUATION_ROOT))

from evaluator import evaluate_case, load_case, read_json  # noqa: E402


def _golden():
    return load_case(
        EVALUATION_ROOT / "fixtures" / "BASE_CASE.json",
        EVALUATION_ROOT / "fixtures" / "strong_golden_truth_over_approval.json",
    )


def test_identical_inputs_produce_byte_identical_receipts() -> None:
    rubric = read_json(EVALUATION_ROOT / "RUBRIC.yaml")
    first = asdict(evaluate_case(_golden(), rubric))
    second = asdict(evaluate_case(_golden(), rubric))
    assert first == second
    assert json.dumps(first, sort_keys=True, separators=(",", ":")) == json.dumps(
        second, sort_keys=True, separators=(",", ":")
    )


def test_fresh_process_reproduces_receipt_hash() -> None:
    rubric = read_json(EVALUATION_ROOT / "RUBRIC.yaml")
    local = evaluate_case(_golden(), rubric)
    helper = Path(__file__).with_name("evaluate_fixture_process.py")
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join(
        item for item in (str(ROOT / "src"), str(ROOT), environment.get("PYTHONPATH", "")) if item
    )
    result = subprocess.run(
        [sys.executable, str(helper), str(EVALUATION_ROOT)],
        cwd=ROOT,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == local.receipt_hash


def test_shadow_and_certified_requests_fail_closed_at_campaign_ceiling() -> None:
    rubric = read_json(EVALUATION_ROOT / "RUBRIC.yaml")
    for requested in ("shadow_ready", "certified"):
        receipt = evaluate_case(_golden(), rubric, requested_status=requested)
        assert receipt.status == "insufficient_evidence"
        assert "MATURITY_CEILING_EXCEEDED" in receipt.hard_gate_failures
        assert receipt.status not in {"shadow_ready", "certified"}

