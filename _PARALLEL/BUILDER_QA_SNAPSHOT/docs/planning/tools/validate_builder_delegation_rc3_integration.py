from __future__ import annotations

import copy
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[3]
INTEGRATION = ROOT / "contracts" / "integration"
PLANNING = ROOT / "docs" / "planning"
RC3 = Path(
    r"D:\Work\CONSCIOUS_ACTIVATIONS\CMF_PROGRAM_CONTROL\02_CROSS_REPO_CONTRACTS"
    r"\delegation-contracts\1.1.0-rc.3"
)

EXPECTED_VERSION = "1.1.0-rc.3"
EXPECTED_RELEASE_DIGEST = "sha256:e3100f9b3ec5db4077def2861128795451085bb8993f1fe318f5aaf6a6653cdf"
EXPECTED_RECEIPT_HASH = "sha256:bb5c5c236fd77b4715bb279f378e72881a05943527e1b88ad4845bb71f0f7c4d"
EXPECTED_MANIFEST_HASH = "sha256:e7501488be54221da3ab437a32d57f80a74cabf3347b6b6b874922b1019ff51f"
EXPECTED_PROFILE = "cmf-delegation-compatibility-profile-1-0"
EXPECTED_SOURCE_KINDS = {
    "interview_expression",
    "public_comment",
    "direct_message_reply",
    "authored_source",
    "live_premise",
    "research_synthesis",
    "operator_supplied",
    "legacy_migrated",
}
EXPECTED_CATEGORIES = {
    "short_form_edited_video",
    "2d_character_animation",
    "carousels",
    "supervisuals",
    "conversational_activation_expression",
}
EXPECTED_CONVERSATIONAL_PROFILES = {
    "public_comment",
    "reply_dm",
    "reelcast_expression",
    "interview_expression",
}
EXPECTED_LINEAGE = {
    "Activative Intelligence Pack": "/activative_semantic_lineage/activative_intelligence_pack_ref",
    "Identity DNA": "/activative_semantic_lineage/identity_dna_ref",
    "Context Premise": "/activative_semantic_lineage/context_premise_ref",
    "Resonance Map": "/activative_semantic_lineage/resonance_map_ref",
    "Matrix of Edging": "/activative_semantic_lineage/matrix_edge_product_ref",
    "Activative Call": "/activative_semantic_lineage/activative_call_refs",
    "Reaction Receipt": "/activative_semantic_lineage/reaction_receipt_refs",
    "Expression Moment": "/activative_semantic_lineage/expression_moment_refs",
    "Activation Contract": "/activation_contract",
    "Visual Semantic Pack": "/visual_semantic_pack",
    "Visual Narrative Program": "/visual_narrative_program",
    "Feature Contracts": "/feature_contracts",
    "T/V route": "/somatic_route_request",
    "Composition Intent": "/composition_intent",
}


def load_yaml(name: str) -> dict[str, Any]:
    return yaml.safe_load((INTEGRATION / name).read_text(encoding="utf-8"))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def released_hash_errors(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for entry in document.get("files", []):
        path = RC3 / entry["path"]
        if not path.is_file():
            errors.append(f"missing:{entry['path']}")
        elif digest(path) != entry["sha256"]:
            errors.append(f"hash:{entry['path']}")
    return errors


def find_enum(node: Any, property_name: str) -> set[str] | None:
    if isinstance(node, dict):
        properties = node.get("properties", {})
        if property_name in properties and isinstance(properties[property_name], dict):
            enum = properties[property_name].get("enum")
            if enum:
                return set(enum)
        for value in node.values():
            found = find_enum(value, property_name)
            if found is not None:
                return found
    elif isinstance(node, list):
        for value in node:
            found = find_enum(value, property_name)
            if found is not None:
                return found
    return None


def is_valid(validator: jsonschema.Validator, instance: dict[str, Any]) -> bool:
    return not list(validator.iter_errors(instance))


def main() -> int:
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, evidence: Any) -> None:
        checks.append({"name": name, "verdict": "PASS" if passed else "FAIL", "evidence": evidence})

    mapping_names = [
        "DELEGATION_CONTRACT_PIN.yaml",
        "BUILDER_TO_DELEGATION_WIRE_MAPPING.yaml",
        "CATEGORY_PROFILE_COMPATIBILITY.yaml",
        "SOURCE_PROVENANCE_MAPPING.yaml",
        "WRONG_READING_LOCK_INHERITANCE.yaml",
        "ACTIVATIVE_LINEAGE_MAPPING.yaml",
    ]
    mappings = {name: load_yaml(name) for name in mapping_names}
    pin = mappings["DELEGATION_CONTRACT_PIN.yaml"]
    wire = mappings["BUILDER_TO_DELEGATION_WIRE_MAPPING.yaml"]
    category = mappings["CATEGORY_PROFILE_COMPATIBILITY.yaml"]
    provenance = mappings["SOURCE_PROVENANCE_MAPPING.yaml"]
    locks = mappings["WRONG_READING_LOCK_INHERITANCE.yaml"]
    lineage = mappings["ACTIVATIVE_LINEAGE_MAPPING.yaml"]

    receipt_path = RC3 / "RELEASE_RECEIPT.json"
    manifest_path = RC3 / "contracts" / "release-manifest.json"
    receipt = load_json(receipt_path)
    manifest = load_json(manifest_path)
    profile = load_json(RC3 / "compatibility" / "profile.json")
    schema = load_json(RC3 / "contracts" / "schemas" / "visual-asset-demand.schema.json")
    example = load_json(RC3 / "contracts" / "examples" / "visual-asset-demand.example.json")
    validator = jsonschema.Draft202012Validator(schema)

    exact_pin = (
        pin["source"]["package_version"] == EXPECTED_VERSION
        and pin["identity"]["release_digest"] == EXPECTED_RELEASE_DIGEST
        and pin["identity"]["release_receipt_sha256"] == EXPECTED_RECEIPT_HASH
        and pin["identity"]["release_manifest_sha256"] == EXPECTED_MANIFEST_HASH
        and pin["compatibility"]["profile_id"] == EXPECTED_PROFILE
        and pin["trust"]["status"] == "local_unsigned_release_candidate"
        and pin["trust"]["production_eligibility"] is False
    )
    check("exact_rc3_pin", exact_pin, pin["identity"])

    identity_matches = (
        receipt["package_version"] == EXPECTED_VERSION
        and receipt["release_digest"] == EXPECTED_RELEASE_DIGEST
        and digest(receipt_path) == EXPECTED_RECEIPT_HASH
        and digest(manifest_path) == EXPECTED_MANIFEST_HASH
        and profile["profile_id"] == EXPECTED_PROFILE
        and receipt["signature_status"] == "UNSIGNED"
        and receipt["production_authorized"] is False
    )
    check("release_receipt_manifest_and_profile_identity", identity_matches, {
        "receipt_sha256": digest(receipt_path),
        "manifest_sha256": digest(manifest_path),
        "profile_id": profile["profile_id"],
    })

    receipt_errors = released_hash_errors(receipt)
    manifest_errors = released_hash_errors(manifest)
    check("all_released_hashes", not receipt_errors and not manifest_errors, {
        "receipt_entries": len(receipt.get("files", [])),
        "manifest_entries": len(manifest.get("files", [])),
        "errors": sorted(set(receipt_errors + manifest_errors)),
    })

    check("generated_types_released", all(
        token in (RC3 / path).read_text(encoding="utf-8")
        for path, token in [
            ("contracts/generated/python/cmf_delegation_contracts/types.py", "interview_expression"),
            ("contracts/generated/typescript/index.ts", "interview_expression"),
        ]
    ), "Python and TypeScript generated types include interview_expression")

    schema_source_kinds = find_enum(schema, "source_kind")
    check("source_kind_schema_enforcement", schema_source_kinds == EXPECTED_SOURCE_KINDS, sorted(schema_source_kinds or []))
    check("source_kind_mapping", set(provenance["governed_source_kinds"]) == EXPECTED_SOURCE_KINDS, provenance["mappings"])
    check("ambiguous_source_kind_fails_closed", provenance["global_rules"]["guess_when_ambiguous"] == "prohibited" and any(
        row.get("ambiguity_behavior") == "reject_and_request_authoritative_classification"
        for row in provenance["mappings"]
    ), provenance["global_rules"])

    base_valid = is_valid(validator, example)
    interview_missing = copy.deepcopy(example)
    interview_missing["source_provenance"]["source_kind"] = "interview_expression"
    interview_missing["activative_semantic_lineage"]["reaction_receipt_refs"] = []
    interview_missing["activative_semantic_lineage"]["expression_moment_refs"] = []
    non_interview = copy.deepcopy(example)
    non_interview["source_provenance"]["source_kind"] = "public_comment"
    non_interview["activative_semantic_lineage"].pop("reaction_receipt_refs", None)
    non_interview["activative_semantic_lineage"].pop("expression_moment_refs", None)
    check("mandatory_interview_provenance", base_valid and not is_valid(validator, interview_missing), {
        "valid_interview_fixture": base_valid,
        "empty_interview_refs_rejected": not is_valid(validator, interview_missing),
    })
    check("optional_non_interview_provenance", is_valid(validator, non_interview), "public_comment validates without interview-only refs")

    category_ids = {row["category_id"] for row in category["categories"]}
    profile_rows = {row["profile_id"]: row for row in category["profiles"]}
    dimensions = set(category["compatibility_dimensions"])
    all_dimensions = all(dimensions == set(row["compatibility"]) for row in category["categories"] + category["profiles"])
    conversational_uncertified = all(
        profile_rows[name]["compatibility"]["structurally_compilable"]
        and profile_rows[name]["compatibility"]["contract_compatible"]
        and not profile_rows[name]["compatibility"]["benchmarked"]
        and not profile_rows[name]["compatibility"]["limited_production_certified"]
        and not profile_rows[name]["compatibility"]["production_certified"]
        for name in EXPECTED_CONVERSATIONAL_PROFILES
    )
    format_02 = profile_rows["minimal_coach_theatre"]
    check("category_profile_compatibility", category_ids == EXPECTED_CATEGORIES and EXPECTED_CONVERSATIONAL_PROFILES <= set(profile_rows) and all_dimensions, {
        "categories": sorted(category_ids), "profiles": sorted(profile_rows), "dimensions": sorted(dimensions)
    })
    check("format02_certification_without_conversational_inheritance", (
        format_02["canonical_path"] == "2d_character_animation/minimal_coach_theatre"
        and format_02["compatibility"]["production_certified"]
        and conversational_uncertified
        and category["certification_rules"]["format_02_certification_inheritance_allowed"] is False
    ), category["certification_rules"])

    empty_locks = copy.deepcopy(example)
    empty_locks["wrong_reading_locks"] = []
    lock_rule_ids = {row["id"] for row in locks["rules"]}
    lock_mapping_ok = (
        lock_rule_ids == {"WRL-001", "WRL-002", "WRL-003", "WRL-004", "WRL-005"}
        and locks["set_semantics"]["parent_lock_set_must_be_subset_of_derivative_lock_set"] is True
        and locks["builder_boundary"]["realizes_visual_behavior"] is False
        and locks["vae_boundary"]["enforces_realization_behavior"] is True
        and not is_valid(validator, empty_locks)
    )
    check("wrong_reading_lock_inheritance", lock_mapping_ok, {"rules": sorted(lock_rule_ids), "empty_locks_rejected": not is_valid(validator, empty_locks)})

    actual_lineage = {row["builder_artifact"]: row["delegation_field"] for row in lineage["mappings"]}
    lineage_ok = (
        actual_lineage == EXPECTED_LINEAGE
        and lineage["preservation_policy"]["flatten_into_generic_notes"] == "prohibited"
        and lineage["validation_rules"]["structured_field_count"] == 14
        and lineage["validation_rules"]["generic_notes_target_count"] == 0
    )
    check("semantic_lineage_preservation", lineage_ok, actual_lineage)

    no_schema_fork = not list(INTEGRATION.rglob("*.schema.json")) and wire["ownership_boundary"]["builder_must_not"][0] == "copy or modify Delegation schemas as local truth"
    check("no_local_schema_fork", no_schema_fork, [str(path.relative_to(ROOT)) for path in INTEGRATION.rglob("*.schema.json")])
    external_ownership = (
        pin["external_owner"] == "CMF_DELEGATION_PROTOCOL"
        and wire["external_contract_owner"] == "CMF_DELEGATION_PROTOCOL"
        and locks["owners"]["shared_contract_owner"] == "CMF_DELEGATION_PROTOCOL"
    )
    check("external_ownership_of_delegation_contracts", external_ownership, {
        "pin": pin["external_owner"], "wire": wire["external_contract_owner"], "locks": locks["owners"]
    })

    cross_repo = yaml.safe_load((PLANNING / "STORY_CROSS_REPOSITORY_DEPENDENCIES.yaml").read_text(encoding="utf-8"))
    xdep3 = next(row for row in cross_repo["dependencies"] if row["id"] == "XDEP-003")
    active_text = json.dumps({
        "active_contract_pins": cross_repo.get("active_contract_pins", {}),
        "xdep3": xdep3,
    }, sort_keys=True)
    no_prior_active = (
        "1.1.0-rc.1" not in active_text
        and "1.1.0-rc.2" not in active_text
        and "1.1.0-rc.3" in active_text
        and xdep3["production_eligibility"] is False
    )
    check("no_active_rc1_or_rc2_dependency", no_prior_active, xdep3["active_contract_pin"])

    release_subset = yaml.safe_load((PLANNING / "RELEASE_1_STORY_SUBSET.yaml").read_text(encoding="utf-8"))
    check("release_1_subset_reference", (
        release_subset["release_1_story_count"] == 69
        and len(release_subset["release_1_story_ids"]) == 69
        and release_subset["delegation_contract_baseline"]["package_version"] == EXPECTED_VERSION
        and release_subset["delegation_contract_baseline"]["production_eligibility"] is False
    ), release_subset["delegation_contract_baseline"])

    with (PLANNING / "PLANNING_REQUIREMENTS_INVENTORY.csv").open(newline="", encoding="utf-8-sig") as handle:
        inventory = list(csv.DictReader(handle))
    epic_doc = yaml.safe_load((PLANNING / "EPIC_INVENTORY.yaml").read_text(encoding="utf-8"))
    story_doc = yaml.safe_load((PLANNING / "STORY_INVENTORY.yaml").read_text(encoding="utf-8"))
    obligation_ids = {row["inventory_id"] for row in inventory}
    story_ids = {row["story_id"] for row in story_doc["stories"]}
    invalid_obligations: set[str] = set()
    invalid_stories: set[str] = set()
    for document in mappings.values():
        trace = document.get("planning_traceability", {})
        invalid_obligations.update(set(trace.get("obligations", [])) - obligation_ids)
        invalid_stories.update(set(trace.get("stories", [])) - story_ids)
    check("existing_obligation_and_story_traceability", not invalid_obligations and not invalid_stories, {
        "invalid_obligations": sorted(invalid_obligations), "invalid_stories": sorted(invalid_stories)
    })
    check("confirmed_baseline_not_regenerated", len(inventory) == 410 and len(epic_doc["epics"]) == 12 and len(story_doc["stories"]) == 69, {
        "obligations": len(inventory), "epics": len(epic_doc["epics"]), "stories": len(story_doc["stories"])
    })

    historical_files = [
        "docs/planning/EPIC_INVENTORY.yaml",
        "docs/planning/EPIC_DESIGN_PROPOSAL.md",
        "docs/planning/STEP4_CROSS_REPO_DEPENDENCY_VALIDATION.yaml",
        "docs/planning/STEP4_VALIDATION_REPORT.json",
        "docs/planning/STEP4_PLANNING_COVERAGE_REPORT.md",
        "docs/planning/STEP4_BLOCKER_IMPACT_REPORT.md",
        "docs/planning/IMPLEMENTATION_READINESS_FINAL.md",
    ]
    check("historical_prior_candidate_records_preserved", all((ROOT / path).is_file() for path in historical_files), historical_files)

    failures = [row["name"] for row in checks if row["verdict"] != "PASS"]
    output = {
        "schema_version": "cmf-builder-delegation-rc3-validation/v1",
        "validated_on": "2026-07-14",
        "verdict": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "passed": len(checks) - len(failures),
        "failed": len(failures),
        "failures": failures,
        "checks": checks,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
