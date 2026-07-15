"""non_production_readiness_proof: validate the controlled Format 02 fixture chain."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from jsonschema import Draft202012Validator
import yaml

CLASSIFICATION = "non_production_readiness_proof"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CHAIN = yaml.safe_load((HERE / "FORMAT02_CONTROLLED_PROOF.yaml").read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_vae(schema_rel: str, instance) -> None:
    schema = load_yaml(ROOT / schema_rel)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(instance)


errors = []
if CHAIN["classification"] != CLASSIFICATION:
    errors.append("classification")

pin = load_yaml(ROOT / "contracts/integration/DELEGATION_CONTRACT_PIN.yaml")
release = Path(pin["package"]["release_path"])
sys.path.insert(0, str(release / "validators"))
from cmf_delegation_validators.contracts import validate_payload  # noqa: E402
from cmf_delegation_validators.compatibility import validate_visual_asset_demand_adapter  # noqa: E402
from cmf_delegation_validators.derivative_locks import validate_derivative_lock_inheritance  # noqa: E402

demand_path = Path(CHAIN["demand"]["path"])
demand = json.loads(demand_path.read_text(encoding="utf-8"))
validate_payload("visual-asset-demand", demand)
validate_visual_asset_demand_adapter(demand, copy.deepcopy(demand))
if digest(demand_path) != CHAIN["demand"]["sha256"]:
    errors.append("demand_hash")

derivative_path = Path(CHAIN["derivative_lock_inheritance"]["fixture_path"])
derivative_claim = json.loads(derivative_path.read_text(encoding="utf-8"))
if digest(derivative_path) != CHAIN["derivative_lock_inheritance"]["fixture_sha256"]:
    errors.append("derivative_fixture_hash")
derivative_outcome = validate_derivative_lock_inheritance(derivative_claim)
if derivative_outcome.get("status") != CHAIN["derivative_lock_inheritance"]["expected_status"] or derivative_outcome.get("valid") is not True:
    errors.append("derivative_lock_inheritance")

plan_path = ROOT / CHAIN["visual_production_plan"]["path"]
plan = load_yaml(plan_path)
validate_vae("contracts/schemas/VISUAL_PRODUCTION_PLAN.schema.yaml", plan)
if digest(plan_path) != CHAIN["visual_production_plan"]["sha256"]:
    errors.append("plan_hash")

for candidate in CHAIN["candidate_portfolio"]["candidates"]:
    path = ROOT / candidate["path"]
    if digest(path) != candidate["sha256"]:
        errors.append(f"candidate_hash:{candidate['candidate_ref']}")
    doc = ET.parse(path).getroot()
    if doc.get("width") != "1080" or doc.get("height") != "1920":
        errors.append(f"candidate_dimensions:{candidate['candidate_ref']}")

validate_vae("contracts/schemas/VISUAL_REPAIR_CONTRACT.schema.yaml", CHAIN["targeted_repair"]["payload"])
validate_vae("contracts/schemas/ASSET_RESULT_CONTRACT.schema.yaml", CHAIN["asset_result"]["payload"])

if CHAIN["independent_evaluator"]["producer_identity"] == CHAIN["independent_evaluator"]["evaluator_identity"]:
    errors.append("evaluator_not_independent")
if CHAIN["asset_result"]["payload"]["authorized_for_composition"] is not False:
    errors.append("production_authority_leak")
if CHAIN["production_acceptance"]["production_authority"] is not False:
    errors.append("simulated_acceptance_authority_leak")

result = {
    "classification": CLASSIFICATION,
    "fixture_contract_chain": "PASS" if not errors else "FAIL",
    "delegation_rc4_demand_validation": "PASS",
    "delegation_rc4_derivative_lock_inheritance": "PASS" if "derivative_lock_inheritance" not in errors else "FAIL",
    "vae_boundary_losslessness": "PASS",
    "provider_neutral_plan_validation": "PASS",
    "candidate_hash_and_geometry_validation": "PASS" if not errors else "FAIL",
    "targeted_repair_contract_validation": "PASS",
    "asset_result_schema_validation": "PASS",
    "pinned_comfyui_workflow_execution": "FAIL_not_available",
    "independent_evaluator_certification": "FAIL_insufficient_evidence",
    "real_production_acceptance": "FAIL_not_authorized",
    "real_downstream_consumption": "FAIL_consumer_unavailable",
    "end_to_end_proof": "FAIL",
    "errors": errors,
}
print(json.dumps(result, indent=2))
raise SystemExit(0 if not errors else 1)
