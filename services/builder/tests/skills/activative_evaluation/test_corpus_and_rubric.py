from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).parents[3]
EVALUATION_ROOT = ROOT / "evaluation" / "skills" / "activative_intelligence_pack_compiler"
sys.path.insert(0, str(EVALUATION_ROOT))

from evaluator import evaluate_case, load_case, read_json  # noqa: E402


def _sha256(path: Path) -> str:
    return f"sha256:{sha256(path.read_bytes()).hexdigest()}"


def _manifest() -> dict[str, object]:
    return read_json(EVALUATION_ROOT / "CORPUS_MANIFEST.yaml")


def _rubric() -> dict[str, object]:
    return read_json(EVALUATION_ROOT / "RUBRIC.yaml")


def _cases():
    manifest = _manifest()
    base = EVALUATION_ROOT / manifest["base_fixture"]["path"]
    for item in manifest["cases"]:
        yield item, load_case(base, EVALUATION_ROOT / item["path"])


def test_manifest_pins_every_public_development_asset() -> None:
    manifest = _manifest()
    assert manifest["protected"] is False
    assert manifest["production_certification_eligible"] is False
    assert manifest["campaign_ceiling"] == "development_validated"
    assert manifest["production_thresholds"] == "NOT_DEFINED_HUMAN_GOVERNANCE_REQUIRED"
    assert manifest["case_count"] == len(manifest["cases"]) == 14
    for key in ("base_fixture", "rubric", "evaluator"):
        item = manifest[key]
        assert _sha256(EVALUATION_ROOT / item["path"]) == item["sha256"]
    for item in manifest["cases"]:
        assert _sha256(EVALUATION_ROOT / item["path"]) == item["sha256"]


def test_rubric_has_exact_independent_dimensions_and_no_production_threshold() -> None:
    rubric = _rubric()
    assert rubric["dimensions"] == [
        "identity_fidelity",
        "audience_reality_fidelity",
        "edge_preservation",
        "specificity",
        "non_generic_pressure",
        "correct_human_role",
        "desired_reaction",
        "micro_commitment_integrity",
        "wrong_reading_resistance",
        "lineage_completeness",
        "non_invention_of_human_truth",
    ]
    assert rubric["allowed_statuses"] == [
        "development_validated",
        "insufficient_evidence",
        "shadow_ready",
        "certified",
    ]
    assert rubric["campaign_ceiling"] == "development_validated"
    assert rubric["production_thresholds"] == "NOT_DEFINED_HUMAN_GOVERNANCE_REQUIRED"
    assert rubric["claims"] == {
        "production_ready": False,
        "shadow_ready": False,
        "certified": False,
    }


def test_every_case_matches_independent_expected_outcome() -> None:
    rubric = _rubric()
    ids: set[str] = set()
    classes: list[str] = []
    for item, case in _cases():
        assert case["case_id"] == item["case_id"]
        assert case["case_id"] not in ids
        ids.add(case["case_id"])
        classes.append(case["case_class"])
        assert case["protected"] is False
        receipt = evaluate_case(case, rubric)
        expected = case["expected"]
        assert receipt.status == expected["status"]
        assert list(receipt.hard_gate_failures) == expected["hard_gate_failures"]
        assert receipt.status in {"development_validated", "insufficient_evidence"}
        assert receipt.receipt_hash.startswith("sha256:")
        assert asdict(receipt)["evaluation_subject_hash"].startswith("sha256:")

    assert classes.count("strong_golden") == 2
    assert "weak_acceptable" in classes
    assert set(classes) >= {
        "adversarial",
        "missing_evidence",
        "semantic_flattening",
        "invented_human_truth",
        "invented_human_reaction",
        "wrong_reading_lock_violation",
        "identity_drift",
        "audience_context_drift",
        "generic_motivational_language",
        "false_activative_call",
        "no_guidance_control",
    }

