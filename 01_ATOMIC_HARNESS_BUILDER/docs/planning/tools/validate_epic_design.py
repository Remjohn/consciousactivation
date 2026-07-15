from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
PLANNING = ROOT / "docs" / "planning"
GOV = ROOT / "governance"

INVENTORY = PLANNING / "PLANNING_REQUIREMENTS_INVENTORY.csv"
CONFIRMATION = PLANNING / "V1_2_INVENTORY_CONFIRMATION_RECEIPT.yaml"
AUTHORIZATION = PLANNING / "EPIC_STEP_2_AUTHORIZATION_RECEIPT.yaml"
EPIC_SOURCE = PLANNING / "EPIC_INVENTORY.yaml"
COVERAGE = PLANNING / "EPIC_REQUIREMENT_COVERAGE.csv"
PROPOSAL = PLANNING / "EPIC_DESIGN_PROPOSAL.md"
REPORT = PLANNING / "EPIC_DESIGN_VALIDATION_REPORT.json"
PROGRAM_STATUS = ROOT / "PROGRAM_STATUS_EXPORT.yaml"

REQUIRED_GATES = {"HD-006", "HD-007", "BD-004", "BD-007", "BD-008", "BD-010", "BD-014"}
EXPECTED_FEATURE_EPICS = {
    "F01": "EP-01", "F02": "EP-01", "F03": "EP-02", "F04": "EP-02",
    "F05": "EP-03", "F06": "EP-03", "F07": "EP-04", "F08": "EP-04",
    "F09": "EP-05", "F10": "EP-05", "F11": "EP-08", "F12": "EP-10",
    "F13": "EP-08", "F14": "EP-06", "F15": "EP-11", "F16": "EP-12",
    "F17": "EP-07", "F18": "EP-09",
}
EXPECTED_CONSTITUTION_EPICS = {
    "CONST-001": "EP-03", "CONST-002": "EP-06", "CONST-003": "EP-06",
    "CONST-004": "EP-06", "CONST-005": "EP-07", "CONST-006": "EP-06",
    "CONST-007": "EP-08", "CONST-008": "EP-08",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def refs(value: str | None) -> set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(";") if item.strip()}


def main() -> int:
    errors: list[str] = []

    inventory_rows = read_csv(INVENTORY) if INVENTORY.is_file() else []
    coverage_rows = read_csv(COVERAGE) if COVERAGE.is_file() else []
    epic_doc = yaml.safe_load(EPIC_SOURCE.read_text(encoding="utf-8")) if EPIC_SOURCE.is_file() else {}
    confirmation = yaml.safe_load(CONFIRMATION.read_text(encoding="utf-8")) if CONFIRMATION.is_file() else {}
    authorization = yaml.safe_load(AUTHORIZATION.read_text(encoding="utf-8")) if AUTHORIZATION.is_file() else {}
    program_status = yaml.safe_load(PROGRAM_STATUS.read_text(encoding="utf-8")) if PROGRAM_STATUS.is_file() else {}

    inventory_hash = hashlib.sha256(INVENTORY.read_bytes()).hexdigest() if INVENTORY.is_file() else ""
    confirmed_hash = confirmation.get("inventory", {}).get("sha256")
    if len(inventory_rows) != 410:
        errors.append(f"confirmed inventory row count is {len(inventory_rows)}, expected 410")
    if inventory_hash != confirmed_hash:
        errors.append("confirmed inventory hash changed during Epic design")
    if any(row.get("epic_ids") or row.get("story_ids") for row in inventory_rows):
        errors.append("confirmed inventory baseline was mutated with Epic or Story assignments")

    if authorization.get("status") != "AUTHORIZED":
        errors.append("Epic Step 2 authorization receipt is not AUTHORIZED")
    auth_scope = authorization.get("scope", {})
    if auth_scope.get("vertical_story_authoring") != "prohibited_pending_human_epic_confirmation":
        errors.append("authorization receipt does not prohibit vertical Story authoring")
    if auth_scope.get("production_implementation") != "prohibited_readiness_fail":
        errors.append("authorization receipt does not preserve the implementation prohibition")

    epics = epic_doc.get("epics", [])
    epic_ids = [item.get("id") for item in epics]
    if len(epic_ids) != 12 or len(epic_ids) != len(set(epic_ids)):
        errors.append("Epic inventory must contain 12 unique Epics")
    epic_by_id = {item["id"]: item for item in epics if item.get("id")}
    epic_order = {item["id"]: item.get("order") for item in epics if item.get("id")}
    if sorted(epic_order.values()) != list(range(1, 13)):
        errors.append("Epic order must be exactly 1 through 12")

    dependency_edges = 0
    for epic in epics:
        epic_id = epic.get("id", "<missing>")
        for field in (
            "title", "primary_actor", "outcome", "release_1_disposition", "completion_evidence", "blocked_outcomes"
        ):
            if not str(epic.get(field, "")).strip():
                errors.append(f"{epic_id}: empty {field}")
        if not epic.get("scope_in") or not epic.get("scope_out"):
            errors.append(f"{epic_id}: outcome boundary is incomplete")
        for dependency in epic.get("dependencies", []):
            dependency_edges += 1
            if dependency not in epic_by_id:
                errors.append(f"{epic_id}: unknown dependency {dependency}")
            elif epic_order[dependency] >= epic_order[epic_id]:
                errors.append(f"{epic_id}: dependency {dependency} is not earlier in topological order")

    planning_boundary = epic_doc.get("planning_boundary", {})
    if planning_boundary.get("planning_may_continue") is not True:
        errors.append("Epic inventory does not explicitly allow planning to continue")
    if planning_boundary.get("vertical_story_authoring_authorized") is not False:
        errors.append("Epic inventory improperly authorizes Story authoring")
    if planning_boundary.get("production_implementation_authorized") is not False:
        errors.append("Epic inventory improperly authorizes production implementation")
    if planning_boundary.get("implementation_readiness") != "FAIL":
        errors.append("Epic inventory does not preserve implementation readiness FAIL")

    if program_status.get("current_stage") != "epic_step_2_complete_pending_human_confirmation":
        errors.append("program status does not report Step 2 complete pending human confirmation")
    if program_status.get("epic_step_2_authorized") is not True:
        errors.append("program status does not record Epic Step 2 authorization")
    if program_status.get("vertical_story_authoring_authorized") is not False:
        errors.append("program status improperly authorizes vertical Story authoring")
    if program_status.get("production_implementation_authorized") is not False:
        errors.append("program status improperly authorizes production implementation")
    if program_status.get("baseline", {}).get("proposed_epics") != 12:
        errors.append("program status proposed Epic count is not 12")
    if program_status.get("baseline", {}).get("epic_primary_assignments") != 410:
        errors.append("program status primary assignment count is not 410")

    category_registry = yaml.safe_load((GOV / "CANONICAL_CATEGORY_REGISTRY.yaml").read_text(encoding="utf-8"))
    expected_categories = {item["category_id"] for item in category_registry["categories"]}
    actual_categories = {item["category_id"] for item in epic_doc.get("canonical_categories", [])}
    if actual_categories != expected_categories or len(actual_categories) != 5:
        errors.append(f"canonical category set differs: {sorted(actual_categories)}")

    profile_registry = yaml.safe_load((GOV / "CONVERSATIONAL_PROFILE_REGISTRY.yaml").read_text(encoding="utf-8"))
    expected_profiles = {item["profile_id"] for item in profile_registry["profiles"]}
    actual_profiles = {item["profile_id"] for item in epic_doc.get("conversational_profiles", [])}
    if actual_profiles != expected_profiles or len(actual_profiles) != 4:
        errors.append(f"conversational profile set differs: {sorted(actual_profiles)}")
    for profile in epic_doc.get("conversational_profiles", []):
        if profile["profile_id"] in {"reelcast_expression", "interview_expression"} and "external_execution" not in profile["boundary"]:
            errors.append(f"{profile['profile_id']}: external execution boundary missing")

    target_registry = yaml.safe_load((GOV / "COMPILATION_TARGET_REGISTRY.yaml").read_text(encoding="utf-8"))
    expected_targets = {item["target_id"] for item in target_registry["targets"]}
    actual_targets = {item["target_id"] for item in epic_doc.get("compilation_targets", [])}
    if actual_targets != expected_targets or len(actual_targets) != 3:
        errors.append(f"compilation target set differs: {sorted(actual_targets)}")

    carried_gates = {
        gate
        for epic in epics
        for gate in epic.get("decision_and_blocker_obligations", [])
    }
    if not REQUIRED_GATES <= carried_gates:
        errors.append(f"required gates not carried: {sorted(REQUIRED_GATES - carried_gates)}")

    xdep_ids = {item["id"] for item in epic_doc.get("cross_repository_dependencies", [])}
    if len(xdep_ids) < 4:
        errors.append("cross-repository dependency inventory is incomplete")
    for epic in epics:
        unknown = set(epic.get("cross_repository_dependencies", [])) - xdep_ids
        if unknown:
            errors.append(f"{epic['id']}: unknown cross-repository dependencies {sorted(unknown)}")

    inventory_by_id = {row["inventory_id"]: row for row in inventory_rows}
    coverage_ids = [row.get("inventory_id", "") for row in coverage_rows]
    duplicate_coverage_ids = sorted(item for item, count in Counter(coverage_ids).items() if count > 1)
    if duplicate_coverage_ids:
        errors.append(f"duplicate primary coverage rows: {duplicate_coverage_ids}")
    missing_ids = sorted(set(inventory_by_id) - set(coverage_ids))
    extra_ids = sorted(set(coverage_ids) - set(inventory_by_id))
    if missing_ids or extra_ids:
        errors.append(f"coverage IDs differ missing={missing_ids} extra={extra_ids}")

    primary_counts = Counter()
    authority_counts_by_epic: dict[str, Counter[str]] = defaultdict(Counter)
    secondary_links = 0
    coverage_by_id = {row["inventory_id"]: row for row in coverage_rows if row.get("inventory_id")}
    for coverage_row in coverage_rows:
        inventory_id = coverage_row.get("inventory_id", "<missing>")
        primary_epic = coverage_row.get("primary_epic_id", "")
        if primary_epic not in epic_by_id:
            errors.append(f"{inventory_id}: unknown or empty primary Epic {primary_epic!r}")
            continue
        primary_counts[primary_epic] += 1
        authority_counts_by_epic[primary_epic][coverage_row.get("authority_type", "")] += 1
        secondary = refs(coverage_row.get("secondary_epic_ids"))
        secondary_links += len(secondary)
        if primary_epic in secondary:
            errors.append(f"{inventory_id}: primary Epic repeated as secondary")
        if secondary - set(epic_ids):
            errors.append(f"{inventory_id}: unknown secondary Epics {sorted(secondary - set(epic_ids))}")
        source_row = inventory_by_id.get(inventory_id, {})
        if coverage_row.get("authority_type") != source_row.get("authority_type"):
            errors.append(f"{inventory_id}: authority type differs from confirmed inventory")
        if coverage_row.get("source_release_scope") != source_row.get("release_scope"):
            errors.append(f"{inventory_id}: release scope differs from confirmed inventory")
        if not refs(source_row.get("active_blockers")) <= refs(coverage_row.get("carried_gate_refs")):
            errors.append(f"{inventory_id}: active blocker is not carried into Epic coverage")
        if coverage_row.get("epic_release_disposition") != epic_by_id[primary_epic].get("release_1_disposition"):
            errors.append(f"{inventory_id}: Epic release disposition differs from Epic inventory")

    for epic_id in epic_ids:
        if primary_counts[epic_id] == 0:
            errors.append(f"{epic_id}: has no primary obligations")

    for inventory_id, source_row in inventory_by_id.items():
        if source_row["authority_type"] == "FUNCTIONAL_REQUIREMENT":
            expected_epic = EXPECTED_FEATURE_EPICS[source_row["feature_or_domain"]]
            if coverage_by_id.get(inventory_id, {}).get("primary_epic_id") != expected_epic:
                errors.append(f"{inventory_id}: functional outcome maps to wrong Epic")
    for inventory_id, expected_epic in EXPECTED_CONSTITUTION_EPICS.items():
        if coverage_by_id.get(inventory_id, {}).get("primary_epic_id") != expected_epic:
            errors.append(f"{inventory_id}: constitutional responsibility maps to wrong Epic")
    if any(
        row["authority_type"] == "UX_CONTRACT_CLAUSE" and row["primary_epic_id"] != "EP-10"
        for row in coverage_rows
    ):
        errors.append("approved UX clauses are not all owned by EP-10")

    proposal_text = PROPOSAL.read_text(encoding="utf-8") if PROPOSAL.is_file() else ""
    for term in (
        "Planning may continue. Implementation remains prohibited",
        "Conversational Activation / Human Expression",
        "reelcast_expression",
        "interview_expression",
        "Vertical Story authoring: `NOT_AUTHORIZED`",
    ):
        if term not in proposal_text:
            errors.append(f"Epic proposal missing required boundary term: {term}")

    status = "PASS" if not errors else "FAIL"
    report = {
        "status": status,
        "epic_proposal_gate": "PENDING_HUMAN_CONFIRMATION",
        "vertical_story_authoring_gate": "NOT_AUTHORIZED",
        "implementation_readiness_gate": "FAIL",
        "confirmed_inventory_sha256": inventory_hash,
        "confirmed_obligations": len(inventory_rows),
        "primary_assignments": len(coverage_rows),
        "unique_primary_assignments": len(set(coverage_ids)),
        "missing_primary_assignments": missing_ids,
        "duplicate_primary_assignments": duplicate_coverage_ids,
        "secondary_traceability_links": secondary_links,
        "epic_count": len(epics),
        "dependency_edges": dependency_edges,
        "dependency_order_validation": "PASS" if not any("dependency" in error for error in errors) else "FAIL",
        "primary_obligation_counts_by_epic": dict(sorted(primary_counts.items())),
        "authority_type_counts_by_epic": {
            epic_id: dict(sorted(counter.items()))
            for epic_id, counter in sorted(authority_counts_by_epic.items())
        },
        "canonical_categories": sorted(actual_categories),
        "conversational_profiles": sorted(actual_profiles),
        "compilation_targets": sorted(actual_targets),
        "carried_decisions_and_blockers": sorted(carried_gates),
        "cross_repository_dependencies": sorted(xdep_ids),
        "errors": errors,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
