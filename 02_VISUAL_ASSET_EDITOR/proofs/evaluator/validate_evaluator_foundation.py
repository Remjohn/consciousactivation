"""non_production_readiness_proof: validate evaluator evidence shapes and seed coverage."""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
import yaml

CLASSIFICATION = "non_production_readiness_proof"
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def load(path: Path):
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate(schema_name: str, instance_name: str) -> None:
    schema = load(HERE / schema_name)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(load(HERE / instance_name))


validate("EVALUATOR_PROGRAM_VERSION_PIN_CONTRACT.schema.json", "evaluator-program-pin.candidate.yaml")
validate("LABELED_CALIBRATION_CORPUS.schema.json", "labeled-calibration-seed.yaml")
validate("PROTECTED_REGRESSION_SET.schema.json", "protected-regression-set.seed.yaml")
validate("ROLLBACK_BASELINE_CONTRACT.schema.json", "evaluator-rollback-baseline.candidate.yaml")

seed = load(HERE / "labeled-calibration-seed.yaml")
required_tags = {
    "accepted_format02_asset", "wrong_visible_action", "identity_drift",
    "composition_failure", "technical_defect", "beneficial_recurrence",
    "redundant_recurrence", "wrong_reading_lock_violation", "no_text_failure",
    "repairable", "non_repairable",
}
observed_tags = {tag for case in seed["cases"] for tag in case["coverage_tags"]}
missing_tags = sorted(required_tags - observed_tags)
required_dimensions = {
    "zero_second_hook", "pattern_match_strength", "pattern_interrupt_strength",
    "viewer_role_clarity", "activation_direction_fidelity", "prediction_gap",
    "payoff", "affinity", "anticipation_residue", "anti_cliche_strength",
    "wrong_reading_risk", "feature_contract_compliance",
    "delete_caption_no_text_survival",
}
observed_dimensions = {
    key for case in seed["cases"] for key in case["labels"]["dimension_labels"]
}
missing_dimensions = sorted(required_dimensions - observed_dimensions)
pin = load(HERE / "evaluator-program-pin.candidate.yaml")
protected = load(HERE / "protected-regression-set.seed.yaml")
status = "insufficient_evidence"
errors = missing_tags + missing_dimensions
result = {
    "classification": CLASSIFICATION,
    "validator_status": "PASS" if not errors else "FAIL",
    "evaluator_certification_status": status,
    "seed_cases": len(seed["cases"]),
    "coverage_tags": sorted(observed_tags),
    "dimension_coverage": sorted(observed_dimensions),
    "evaluator_pin_status": pin["status"],
    "protected_set_status": protected["status"],
    "final_thresholds_defined": False,
    "errors": errors,
}
print(json.dumps(result, indent=2))
raise SystemExit(0 if not errors else 1)
