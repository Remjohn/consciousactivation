from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
PLANNING = ROOT / "docs" / "planning"

INVENTORY = PLANNING / "PLANNING_REQUIREMENTS_INVENTORY.csv"
EPIC_COVERAGE = PLANNING / "EPIC_REQUIREMENT_COVERAGE.csv"
STORY_INVENTORY = PLANNING / "STORY_INVENTORY.yaml"
STORY_COVERAGE = PLANNING / "STORY_REQUIREMENT_COVERAGE.csv"
STORY_DEPENDENCIES = PLANNING / "STORY_DEPENDENCY_GRAPH.csv"
STORY_CONFIRMATION = PLANNING / "STORY_INVENTORY_CONFIRMATION_RECEIPT.yaml"
SPEC_ASSIGNMENTS = PLANNING / "FEATURE_TECH_SPEC_ASSIGNMENTS.csv"
RISK_REVIEW = PLANNING / "FILE_CHURN_RISK_BOUNDARY_REVIEW.md"
READINESS_REPORT = PLANNING / "IMPLEMENTATION_READINESS_REPORT.md"
PROGRAM_STATUS = ROOT / "PROGRAM_STATUS_EXPORT.yaml"
BLOCKING_DECISIONS = ROOT / "docs" / "tech-specs" / "BLOCKING_DECISIONS.yaml"

EXPECTED_CONFIRMATION = "CONFIRM BUILDER V1.2 STORY INVENTORY AND BEGIN STEP 4"
EXPECTED_ACTIVE_BLOCKERS = {"BD-004", "BD-007", "BD-008", "BD-010", "BD-014"}
EXPECTED_HUMAN_DECISIONS = {"HD-006", "HD-007"}
KNOWN_SPECS = {f"TS-{index:02d}" for index in range(16)} | {"IMPLEMENTATION_BASELINE"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def refs(value: str | None) -> set[str]:
    return {item.strip() for item in (value or "").split(";") if item.strip()}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate() -> dict[str, object]:
    errors: list[str] = []
    concerns: list[str] = []

    inventory_rows = read_csv(INVENTORY)
    epic_rows = read_csv(EPIC_COVERAGE)
    story_rows = read_csv(STORY_COVERAGE)
    dependency_rows = read_csv(STORY_DEPENDENCIES)
    spec_rows = read_csv(SPEC_ASSIGNMENTS) if SPEC_ASSIGNMENTS.is_file() else []
    story_doc = yaml.safe_load(STORY_INVENTORY.read_text(encoding="utf-8"))
    confirmation = yaml.safe_load(STORY_CONFIRMATION.read_text(encoding="utf-8"))
    program = yaml.safe_load(PROGRAM_STATUS.read_text(encoding="utf-8"))
    decisions = yaml.safe_load(BLOCKING_DECISIONS.read_text(encoding="utf-8"))

    inventory_ids = {row["inventory_id"] for row in inventory_rows}
    epic_primary = [row["inventory_id"] for row in epic_rows]
    story_primary = [row["inventory_id"] for row in story_rows]
    if len(inventory_rows) != 410 or len(inventory_ids) != 410:
        errors.append("Planning inventory is not 410 unique obligations")
    if Counter(epic_primary) != Counter(inventory_ids):
        errors.append("Epic primary coverage is not exactly once for all 410 obligations")
    if Counter(story_primary) != Counter(inventory_ids):
        errors.append("Story primary coverage is not exactly once for all 410 obligations")

    stories = story_doc.get("stories", [])
    story_by_id = {story["story_id"]: story for story in stories}
    if len(stories) != 69 or len(story_by_id) != 69:
        errors.append("Story inventory is not 69 unique Stories")
    order = {story["story_id"]: story["global_order"] for story in stories}
    forward_edges = []
    edge_count = 0
    for story in stories:
        for dependency in story.get("dependencies", []):
            edge_count += 1
            if dependency not in order or order[dependency] >= order[story["story_id"]]:
                forward_edges.append(f"{story['story_id']}->{dependency}")
    if forward_edges:
        errors.append(f"Future or unknown Story dependencies: {forward_edges}")
    if edge_count != 103:
        errors.append(f"Expected 103 Story dependency edges, found {edge_count}")
    if len(dependency_rows) != 69:
        errors.append("Dependency graph does not contain one row per Story")

    if confirmation.get("confirmation_text") != EXPECTED_CONFIRMATION:
        errors.append("Exact Story confirmation text is not preserved")
    if confirmation.get("status") != "CONFIRMED_STEP_4_AUTHORIZED":
        errors.append("Step 4 authorization receipt is not confirmed")
    confirmed = confirmation.get("confirmed_story_design", {})
    hash_checks = {
        "story_inventory": STORY_INVENTORY,
        "story_requirement_coverage": STORY_COVERAGE,
        "story_dependency_graph": STORY_DEPENDENCIES,
    }
    for key, path in hash_checks.items():
        if confirmed.get(key, {}).get("sha256") != sha256(path):
            errors.append(f"Confirmed Story artifact hash changed: {key}")

    assignment_by_story = {row.get("story_id"): row for row in spec_rows}
    if len(spec_rows) != 69 or len(assignment_by_story) != 69:
        errors.append("Feature technical-specification assignment matrix is not 69 unique Stories")
    for story_id, story in story_by_id.items():
        expected_specs = set(story["contracts_and_seams"]["primary_specs"])
        assigned_specs = refs(assignment_by_story.get(story_id, {}).get("technical_spec_ids"))
        if expected_specs != assigned_specs:
            errors.append(f"{story_id}: technical-specification assignment differs from confirmed Story")
        unknown = assigned_specs - KNOWN_SPECS
        if unknown:
            errors.append(f"{story_id}: unknown technical specifications {sorted(unknown)}")

    if not RISK_REVIEW.is_file():
        errors.append("File-churn and risk-boundary review is missing")
    if not READINESS_REPORT.is_file():
        errors.append("Implementation-readiness report is missing")

    active_blockers = {
        item["id"]
        for item in decisions.get("decisions", [])
        if str(item.get("status", "")).startswith("BLOCKING_")
    }
    if not EXPECTED_ACTIVE_BLOCKERS.issubset(active_blockers):
        errors.append("Expected blocking decisions are not preserved")
    if set(program.get("human_decisions_required", [])) != EXPECTED_HUMAN_DECISIONS:
        errors.append("HD-006 and HD-007 are not both preserved")
    if program.get("implementation_authorized") is not False:
        errors.append("Program status improperly authorizes implementation")
    if program.get("production_implementation_authorized") is not False:
        errors.append("Program status improperly authorizes production implementation")

    integrity = confirmation.get("preflight_integrity_observation", {})
    if integrity.get("status") != "CONCERNS":
        errors.append("Historical validation-artifact integrity concern is not recorded")
    else:
        concerns.append("Confirmed Epic validation artifact hash drift requires reconciliation")
    concerns.extend(sorted(active_blockers))
    concerns.extend(sorted(EXPECTED_HUMAN_DECISIONS))

    coverage_status = "PASS" if not errors else "FAIL"
    readiness_status = "FAIL"
    return {
        "status": coverage_status,
        "step_4_status": "COMPLETE" if not errors else "INCOMPLETE",
        "coverage_verdict": coverage_status,
        "artifact_integrity_verdict": "CONCERNS",
        "implementation_readiness_verdict": readiness_status,
        "production_implementation_authorized": False,
        "confirmed_obligations": len(inventory_rows),
        "confirmed_epics": 12,
        "confirmed_stories": len(stories),
        "epic_primary_assignments": len(epic_primary),
        "story_primary_assignments": len(story_primary),
        "feature_technical_spec_assignments": len(spec_rows),
        "dependency_edges": edge_count,
        "forward_dependency_edges": len(forward_edges),
        "active_blockers": sorted(active_blockers),
        "human_decisions_required": sorted(EXPECTED_HUMAN_DECISIONS),
        "concerns": concerns,
        "errors": errors,
    }


def main() -> int:
    result = validate()
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
