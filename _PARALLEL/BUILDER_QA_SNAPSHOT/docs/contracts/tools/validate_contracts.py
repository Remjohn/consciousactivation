from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[3]
CONTRACTS = ROOT / "docs" / "contracts"
REPORT = CONTRACTS / "VALIDATION_REPORT.json"

EXAMPLE_SCHEMAS = {
    "shared-activative-pack.json": "shared-activative-core.schema.json",
    "reelcast-expression.json": "conversational-expression.schema.json",
    "interview-expression.json": "conversational-expression.schema.json",
    "visual-delegation-handoff.json": "visual-semantic-handoff.schema.json",
    "constitutional-evaluation.json": "constitutional-evaluation.schema.json",
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    schemas: dict[str, dict] = {}
    for path in sorted((CONTRACTS / "schemas").glob("*.schema.json")):
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
            schemas[path.name] = schema
        except Exception as exc:
            errors.append(f"schema:{path.name}:{exc}")

    for example_name, schema_name in EXAMPLE_SCHEMAS.items():
        try:
            instance = json.loads((CONTRACTS / "examples" / example_name).read_text(encoding="utf-8"))
            validator = Draft202012Validator(schemas[schema_name], format_checker=FormatChecker())
            for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
                errors.append(f"example:{example_name}:{'/'.join(map(str, error.path))}:{error.message}")
        except Exception as exc:
            errors.append(f"example:{example_name}:{exc}")

    registry = load_yaml(CONTRACTS / "CONTRACT_REGISTRY.yaml")
    required_contract_fields = {"contract_id", "implementation_owner", "component_boundary", "schema", "failure_behavior", "test_seam", "acceptance_criteria", "compatibility_effect"}
    contract_ids: list[str] = []
    for contract in registry.get("contracts", []):
        contract_ids.append(contract.get("contract_id", ""))
        missing = required_contract_fields - set(contract)
        if missing:
            errors.append(f"contract:{contract.get('contract_id')}:missing:{sorted(missing)}")
        schema_path = str(contract.get("schema", "")).split("#", 1)[0]
        if schema_path and not (ROOT / schema_path).exists():
            errors.append(f"contract:{contract.get('contract_id')}:missing_schema:{schema_path}")
    if len(contract_ids) != len(set(contract_ids)):
        errors.append("contract_registry:duplicate_contract_id")

    categories = load_yaml(ROOT / "governance" / "CANONICAL_CATEGORY_REGISTRY.yaml")
    category_ids = [item["category_id"] for item in categories["categories"]]
    if category_ids != ["short_form_edited_video", "2d_character_animation", "carousels", "supervisuals", "conversational_activation_expression"]:
        errors.append(f"categories:unexpected:{category_ids}")
    fifth = categories["categories"][-1]
    expected_profiles = ["public_comment", "reply_dm", "reelcast_expression", "interview_expression"]
    if fifth.get("current_profiles") != expected_profiles:
        errors.append("categories:fifth_profile_list_mismatch")

    profiles = load_yaml(ROOT / "governance" / "CONVERSATIONAL_PROFILE_REGISTRY.yaml")
    if [item["profile_id"] for item in profiles["profiles"]] != expected_profiles:
        errors.append("profiles:registry_mismatch")
    if any(item.get("release_1_certification") != "UNCERTIFIED" for item in profiles["profiles"]):
        errors.append("profiles:release_1_must_be_uncertified")

    targets = load_yaml(ROOT / "governance" / "COMPILATION_TARGET_REGISTRY.yaml")
    if len(targets.get("targets", [])) != 3:
        errors.append("targets:expected_three_compilation_targets")

    precedence = load_yaml(ROOT / "governance" / "CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml")
    constitution = ROOT / precedence["authority"]["constitution"]["path"]
    if not constitution.exists():
        errors.append("authority:pinned_constitution_missing")
    elif hashlib.sha256(constitution.read_bytes()).hexdigest() != precedence["authority"]["constitution"]["sha256"]:
        errors.append("authority:pinned_constitution_hash_mismatch")

    report = {
        "schema_version": "cmf-builder-contract-validation/v1",
        "status": "PASS" if not errors else "FAIL",
        "validated_schemas": sorted(schemas),
        "validated_examples": sorted(EXAMPLE_SCHEMAS),
        "contract_count": len(contract_ids),
        "canonical_category_count": len(category_ids),
        "conversational_profile_count": len(profiles.get("profiles", [])),
        "compilation_target_count": len(targets.get("targets", [])),
        "errors": errors,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
