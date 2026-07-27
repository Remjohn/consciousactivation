from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
PIN_PATH = REPO_ROOT / "contracts/integration/DELEGATION_CONTRACT_PIN.yaml"
ALIAS_PATH = REPO_ROOT.parent / "CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/FORMAT02_PROFILE_ALIAS_REGISTRY.yaml"
EXPECTED_VERSION = "1.1.0-rc.4"
EXPECTED_DIGEST = "sha256:c614a4d9b705e382456f4d6cd1cd6b7bcbc892517a22b358950db7404e3b4c44"
EXPECTED_RECEIPT = "sha256:042ab1ad99a4e5a4f8ff3a08c559b410db9c17cbade48ef05e92d6170dddc25f"
EXPECTED_MANIFEST = "sha256:7a23c0896f215c008bd2f9f0f7079cb97c23d05d100ac5a4b60691bb8abb9882"
EXPECTED_ALIAS_HASH = "sha256:21ad1a618361a14ec62576ce4e1d7ce3c7267e3bd77a1004aa8b996d51c87d57"


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    results: list[dict[str, object]] = []

    def check(check_id: str, condition: bool, evidence: object) -> None:
        results.append({"id": check_id, "status": "PASS" if condition else "FAIL", "evidence": evidence})

    pin = load_yaml(PIN_PATH)
    release = Path(pin["source"]["path"])
    receipt_path = release / pin["identity"]["release_receipt_path"]
    manifest_path = release / pin["identity"]["release_manifest_path"]
    receipt = load_json(receipt_path)

    check("BRC4-01", pin["source"]["package_version"] == EXPECTED_VERSION, pin["source"]["package_version"])
    check("BRC4-02", receipt["release_digest"] == EXPECTED_DIGEST == pin["identity"]["release_digest"], receipt["release_digest"])
    check("BRC4-03", sha256(receipt_path) == EXPECTED_RECEIPT == pin["identity"]["release_receipt_sha256"], sha256(receipt_path))
    check("BRC4-04", sha256(manifest_path) == EXPECTED_MANIFEST == pin["identity"]["release_manifest_sha256"], sha256(manifest_path))

    mismatches = []
    for item in receipt["files"]:
        path = release / item["path"]
        if path.stat().st_size != item["bytes"] or sha256(path) != item["sha256"]:
            mismatches.append(item["path"])
    check("BRC4-05", not mismatches and len(receipt["files"]) == 163, {"entries": len(receipt["files"]), "mismatches": mismatches})

    sys.path.insert(0, str(release / "validators"))
    from cmf_delegation_validators.derivative_locks import validate_derivative_lock_inheritance

    derivative_root = release / "fixtures/compatibility/derivative-locks"
    expected = {
        "exact-inheritance.valid.json": "LOCK_INHERITANCE_VALID",
        "stricter-addition.valid.json": "LOCK_INHERITANCE_VALID",
        "lock-removal.invalid.json": "PARENT_LOCK_REMOVED",
        "lock-weakening.invalid.json": "PARENT_LOCK_WEAKENED",
        "missing-parent-evidence.invalid.json": "PARENT_LOCK_EVIDENCE_REQUIRED",
        "ambiguous-derivation.invalid.json": "DERIVATION_CLASSIFICATION_REQUIRED",
        "semantic-shortcut.invalid.json": "UNAUTHORIZED_LOCK_RELAXATION",
        "authorized-new-demand-relaxation.valid.json": "LOCK_INHERITANCE_VALID",
    }
    observed = {name: validate_derivative_lock_inheritance(load_json(derivative_root / name))["status"] for name in expected}
    check("BRC4-06", observed == expected, observed)

    source = load_yaml(REPO_ROOT / "contracts/integration/SOURCE_PROVENANCE_MAPPING.yaml")
    expected_source_kinds = {"interview_expression", "public_comment", "direct_message_reply", "authored_source", "live_premise", "research_synthesis", "operator_supplied", "legacy_migrated"}
    check("BRC4-07", set(source["governed_source_kinds"]) == expected_source_kinds, sorted(source["governed_source_kinds"]))
    provenance_fields = {path.rsplit("/", 1)[-1] for path in source["interview_provenance"]["required_non_empty_fields"]}
    check("BRC4-08", provenance_fields == {"reaction_receipt_refs", "expression_moment_refs"}, sorted(provenance_fields))

    lineage = load_yaml(REPO_ROOT / "contracts/integration/ACTIVATIVE_LINEAGE_MAPPING.yaml")
    mapped = {item["builder_artifact"] for item in lineage["mappings"]}
    required = {"Activative Intelligence Pack", "Identity DNA", "Context Premise", "Resonance Map", "Matrix of Edging", "Activative Call", "Reaction Receipt", "Expression Moment", "Activation Contract", "Visual Semantic Pack", "Visual Narrative Program", "Feature Contracts", "T/V route", "Composition Intent"}
    check("BRC4-09", required == mapped, sorted(mapped))

    locks = load_yaml(REPO_ROOT / "contracts/integration/WRONG_READING_LOCK_INHERITANCE.yaml")
    required_fields = {"inheritance_id", "authoritative_parent_ref", "parent_contract_version", "governing_authoritative_demand_ref", "parent_lock_evidence", "derivative_ref", "derivative_wrong_reading_locks", "derivation_type", "derivative_semantics", "authoritative_lock_authorization", "declared_at"}
    check("BRC4-10", set(locks["compiled_relationship_fields"]) == required_fields, sorted(locks["compiled_relationship_fields"]))
    check("BRC4-11", locks["builder_boundary"]["realizes_visual_behavior"] is False, locks["builder_boundary"])

    alias = load_yaml(ALIAS_PATH)
    check("BRC4-12", sha256(ALIAS_PATH) == EXPECTED_ALIAS_HASH and alias["canonical_profile_id"] == "format02_minimal_coach_theatre", {"hash": sha256(ALIAS_PATH), "canonical": alias["canonical_profile_id"]})
    category = load_yaml(REPO_ROOT / "contracts/integration/CATEGORY_PROFILE_COMPATIBILITY.yaml")
    profile = next(item for item in category["profiles"] if item["profile_id"] == alias["canonical_profile_id"])
    state = profile["compatibility"]
    check("BRC4-13", state == {"reference_profile": True, "structurally_supported": True, "contract_compatible": True, "benchmarked": False, "limited_production_certified": False, "production_certified": False}, state)

    story = load_yaml(REPO_ROOT / "docs/planning/STORY_CROSS_REPOSITORY_DEPENDENCIES.yaml")
    subset = load_yaml(REPO_ROOT / "docs/planning/RELEASE_1_STORY_SUBSET.yaml")
    check("BRC4-14", story["active_contract_pins"]["XDEP-003"].endswith(EXPECTED_VERSION) and subset["delegation_contract_baseline"]["package_version"] == EXPECTED_VERSION, {"story_pin": story["active_contract_pins"]["XDEP-003"], "subset": subset["delegation_contract_baseline"]["package_version"]})

    active_files = [PIN_PATH, REPO_ROOT / "contracts/integration/BUILDER_TO_DELEGATION_WIRE_MAPPING.yaml", REPO_ROOT / "contracts/integration/WRONG_READING_LOCK_INHERITANCE.yaml", REPO_ROOT / "contracts/integration/CATEGORY_PROFILE_COMPATIBILITY.yaml", REPO_ROOT / "contracts/integration/SOURCE_PROVENANCE_MAPPING.yaml", REPO_ROOT / "contracts/integration/ACTIVATIVE_LINEAGE_MAPPING.yaml", REPO_ROOT / "docs/planning/STORY_CROSS_REPOSITORY_DEPENDENCIES.yaml", REPO_ROOT / "docs/planning/RELEASE_1_STORY_SUBSET.yaml"]
    stale = [str(path.relative_to(REPO_ROOT)) for path in active_files if any(version in path.read_text(encoding="utf-8") for version in ("1.1.0-rc.1", "1.1.0-rc.2", "1.1.0-rc.3")) and path != PIN_PATH]
    check("BRC4-15", not stale, stale)
    check("BRC4-16", pin["trust"]["status"] == "local_unsigned_release_candidate" and pin["trust"]["production_eligibility"] is False and pin["trust"]["production_authorized"] is False, pin["trust"])

    failed = [item for item in results if item["status"] != "PASS"]
    output = {"validator": "builder-delegation-rc4-integration", "status": "PASS" if not failed else "FAIL", "checks_total": len(results), "checks_passed": len(results) - len(failed), "results": results}
    print(json.dumps(output, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
