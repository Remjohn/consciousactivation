"""non_production_readiness_proof: validate CRC-401 and CRC-402 repository evidence."""
from __future__ import annotations

import hashlib
import json
from itertools import product
from pathlib import Path

import yaml

CLASSIFICATION = "non_production_readiness_proof"
ROOT = Path(__file__).resolve().parents[2]
PROGRAM = Path("D:/Work/CONSCIOUS_ACTIVATIONS/CMF_PROGRAM_CONTROL")


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


errors: list[str] = []

precedence_path = ROOT / "governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml"
precedence = load_yaml(precedence_path)
if precedence.get("contract_id") != "CMF-VISUAL-ASSET-EDITOR-CONSTITUTIONAL-PRECEDENCE-LOCAL":
    errors.append("crc401_contract_identity")
if precedence.get("non_fork_guarantee") != {
    "constitution_content_embedded": False,
    "local_constitution_copy_created": False,
    "canonical_hash_is_authoritative": True,
    "local_override_allowed": False,
}:
    errors.append("crc401_non_fork_guarantee")

authority_paths = {
    "constitution": PROGRAM / "00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md",
    "authority_record": PROGRAM / "00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md",
    "precedence_contract": PROGRAM / "00_CONSTITUTION/current-v1.1/governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml",
    "product_pointer": PROGRAM / "01_PRODUCT_AUTHORITIES/visual-asset-editor/AUTHORITY_POINTER.md",
    "product_contract": PROGRAM / "01_PRODUCT_AUTHORITIES/visual-asset-editor/current-unpacked/CMF_VISUAL_ASSET_EDITOR_SHARDED_PRD_V1_1/governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml",
    "authority_matrix": PROGRAM / "03_PROGRAM_STATUS/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml",
    "convergence_verdict": PROGRAM / "03_PROGRAM_STATUS/CONVERGENCE_VERDICT.yaml",
}
declared_hashes = {
    "constitution": precedence["canonical_authority"]["sha256"],
    "authority_record": precedence["canonical_authority"]["authority_record"]["sha256"],
    "precedence_contract": precedence["canonical_authority"]["precedence_contract"]["sha256"],
    "product_pointer": precedence["product_authority"]["pointer_sha256"],
    "product_contract": precedence["product_authority"]["package_precedence_contract_sha256"],
    "authority_matrix": precedence["program_control_validation_basis"]["cross_product_authority_matrix_sha256"],
    "convergence_verdict": precedence["program_control_validation_basis"]["convergence_verdict_sha256"],
}
for name, path in authority_paths.items():
    if not path.is_file() or sha256(path) != declared_hashes[name]:
        errors.append(f"crc401_hash:{name}")

program_matrix = load_yaml(authority_paths["authority_matrix"])
vae_evidence = program_matrix["constitutional_precedence_evidence"]["vae"]
if vae_evidence.get("concern_id") != "CRC-401" or vae_evidence.get("repository_local_contract") != "absent":
    errors.append("crc401_program_record_basis")

matrix_path = ROOT / "validation/fixtures/feature-contract/FEATURE_CONTRACT_CATEGORY_ASSET_FAMILY_MATRIX.yaml"
matrix = load_yaml(matrix_path)
category_record = load_yaml(PROGRAM / "03_PROGRAM_STATUS/CATEGORY_PROFILE_CONVERGENCE.yaml")
categories = category_record["canonical_categories"]["values"]
families = [item["id"] for item in load_yaml(ROOT / "governance/ASSET_FAMILY_REGISTRY.yaml")["families"]]
expected_pairs = set(product(categories, families))
observed_pairs = {(item["category"], item["asset_family"]) for item in matrix["matrix"]}
if len(matrix["matrix"]) != 40 or observed_pairs != expected_pairs:
    errors.append("crc402_pair_coverage")

allowed_statuses = {"supported", "structural_only", "deferred", "explicitly_rejected"}
for item in matrix["matrix"]:
    if item.get("status") not in allowed_statuses:
        errors.append(f"crc402_status:{item.get('category')}:{item.get('asset_family')}")
    if item.get("feature_contract_applicability") != "required":
        errors.append(f"crc402_applicability:{item.get('category')}:{item.get('asset_family')}")
if matrix["production_support_policy"].get("explicit_production_certification_claims_in_this_matrix") != 0:
    errors.append("crc402_production_claim")

fixture_dir = matrix_path.parent
positive_count = 0
negative_count = 0
for name in matrix["representative_fixtures"]["positive"]:
    fixture = json.loads((fixture_dir / name).read_text(encoding="utf-8"))
    positive_count += 1
    if fixture.get("classification") != CLASSIFICATION or fixture.get("production_certified") is not False:
        errors.append(f"crc402_positive_scope:{name}")
    if fixture.get("authoritative_owner") != "CONTENT_HARNESS":
        errors.append(f"crc402_positive_owner:{name}")
    ref = fixture.get("feature_contract", {}).get("contract_ref", {})
    if set(ref) != {"resource_id", "version", "payload_hash", "canonical_ref"}:
        errors.append(f"crc402_positive_ref:{name}")
    realization = fixture.get("vae_realization", {})
    if realization.get("authoritative_contract_mutated") is not False:
        errors.append(f"crc402_positive_mutation:{name}")

for name in matrix["representative_fixtures"]["negative"]:
    fixture = json.loads((fixture_dir / name).read_text(encoding="utf-8"))
    negative_count += 1
    if fixture.get("classification") != CLASSIFICATION or fixture.get("expected_result") != "explicitly_rejected":
        errors.append(f"crc402_negative_result:{name}")
    if not fixture.get("rejection_code"):
        errors.append(f"crc402_negative_code:{name}")

result = {
    "classification": CLASSIFICATION,
    "validator_status": "PASS" if not errors else "FAIL",
    "CRC-401": {
        "repository_local_evidence": "PASS" if not any(e.startswith("crc401") for e in errors) else "FAIL",
        "canonical_constitution_hash": declared_hashes["constitution"],
        "local_override_allowed": False,
        "constitution_duplicated_or_forked": False,
        "program_control_record_reconciliation": "PENDING_PROGRAM_CONTROL_UPDATE",
    },
    "CRC-402": {
        "repository_local_evidence": "PASS" if not any(e.startswith("crc402") for e in errors) else "FAIL",
        "canonical_categories": len(categories),
        "canonical_asset_families": len(families),
        "category_asset_family_pairs": len(observed_pairs),
        "positive_fixtures": positive_count,
        "negative_fixtures": negative_count,
        "production_certified_pairs": 0,
        "program_control_record_reconciliation": "PENDING_PROGRAM_CONTROL_UPDATE",
    },
    "authorization_effect": "none",
    "implementation_authorized": False,
    "stage5_allowed": False,
    "errors": errors,
}
print(json.dumps(result, indent=2))
raise SystemExit(0 if not errors else 1)
