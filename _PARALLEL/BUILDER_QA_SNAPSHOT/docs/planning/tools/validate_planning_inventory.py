from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
PLANNING = ROOT / "docs" / "planning"
GOV = ROOT / "governance"
TECH = ROOT / "docs" / "tech-specs"
ARCH = ROOT / "docs" / "architecture"
UX = ROOT / "docs" / "ux"

INVENTORY = PLANNING / "PLANNING_REQUIREMENTS_INVENTORY.csv"
BASELINE = PLANNING / "REQUIREMENTS_EXTRACTION_BASELINE.md"
REPORT = PLANNING / "REQUIREMENTS_EXTRACTION_VALIDATION_REPORT.json"
PRESERVATION_RECEIPT = PLANNING / "V1_1_BASELINE_PRESERVATION_RECEIPT.json"
CHANGED_REPORT = PLANNING / "V1_2_CHANGED_OBLIGATIONS.csv"
CONFIRMATION_PACKAGE = PLANNING / "V1_2_INVENTORY_CONFIRMATION_PACKAGE.md"
CONFIRMATION_RECEIPT = PLANNING / "V1_2_INVENTORY_CONFIRMATION_RECEIPT.yaml"
EPIC_STEP_2_AUTHORIZATION = PLANNING / "EPIC_STEP_2_AUTHORIZATION_RECEIPT.yaml"
EPIC_INVENTORY_CONFIRMATION = PLANNING / "EPIC_INVENTORY_CONFIRMATION_RECEIPT.yaml"

ALLOWED_VERDICTS = {
    "IMPLEMENTED_AND_KEEP",
    "IMPLEMENTED_BUT_ALIGN",
    "PARTIALLY_IMPLEMENTED",
    "NEW_IMPLEMENTATION",
    "REPLACE_EXISTING_BEHAVIOR",
    "NEEDS_EMPIRICAL_PROTOTYPE",
    "DEFERRED",
    "NOT_APPLICABLE",
}

EXPECTED_COUNTS = {
    "FUNCTIONAL_REQUIREMENT": 210,
    "NON_FUNCTIONAL_REQUIREMENT": 53,
    "LOCKED_DECISION": 33,
    "ARCHITECTURE_DECISION": 18,
    "UX_CONTRACT_CLAUSE": 51,
    "READINESS_HARD_GATE": 15,
    "BINDING_ANTI_GOAL": 22,
    "CONSTITUTIONAL_AMENDMENT": 8,
}

REQUIRED_COLUMNS = {
    "inventory_id",
    "authority_type",
    "title",
    "normative_text",
    "acceptance_or_enforcement",
    "release_scope",
    "coverage_verdict",
    "planning_disposition",
    "feature_or_domain",
    "primary_specs",
    "architecture_components",
    "requirement_refs",
    "adr_refs",
    "decision_refs",
    "ux_refs",
    "verification_refs",
    "source_evidence",
    "repository_coverage_basis",
    "blocking_decisions",
    "active_blockers",
    "planning_owner",
    "epic_ids",
    "story_ids",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def refs(value: str | None) -> set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(";") if item.strip()}


def source_ids() -> dict[str, set[str]]:
    requirements = json.loads((GOV / "REQUIREMENTS_REGISTRY.json").read_text(encoding="utf-8"))
    decisions = json.loads((GOV / "DECISION_REGISTER.json").read_text(encoding="utf-8"))
    anti_goals = json.loads((GOV / "ARCHITECTURAL_PROHIBITIONS.json").read_text(encoding="utf-8"))
    hard_gates = yaml.safe_load((GOV / "READINESS_HARD_GATES.yaml").read_text(encoding="utf-8"))
    adr_register = yaml.safe_load((ARCH / "ADR_REGISTER.yaml").read_text(encoding="utf-8"))
    ux_contract = (UX / "HARNESS_CONTROL_TOWER_UX_CONTRACT.md").read_text(encoding="utf-8")
    delta_rows = read_csv(ROOT / "docs/constitutional-alignment/REQUIREMENT_DELTA.csv")
    return {
        "FUNCTIONAL_REQUIREMENT": {item["id"] for item in requirements["functional_requirements"]},
        "NON_FUNCTIONAL_REQUIREMENT": {item["id"] for item in requirements["non_functional_requirements"]},
        "LOCKED_DECISION": {item["id"] for item in decisions["decisions"]},
        "ARCHITECTURE_DECISION": {item["id"] for item in adr_register["records"] if item["status"] == "ACCEPTED"},
        "UX_CONTRACT_CLAUSE": set(re.findall(r"\bUXC-\d{3}\b", ux_contract)),
        "READINESS_HARD_GATE": {item["id"] for item in hard_gates["gates"]},
        "BINDING_ANTI_GOAL": {item["id"] for item in anti_goals["anti_goals"]},
        "CONSTITUTIONAL_AMENDMENT": {item["requirement_id"] for item in delta_rows if re.fullmatch(r"CONST-00[1-8]", item["requirement_id"])},
    }


def main() -> int:
    errors: list[str] = []

    if not INVENTORY.is_file():
        errors.append("planning requirements inventory is missing")
        rows: list[dict[str, str]] = []
    else:
        rows = read_csv(INVENTORY)

    if rows and set(rows[0]) != REQUIRED_COLUMNS:
        errors.append(f"inventory columns differ: {sorted(set(rows[0]) ^ REQUIRED_COLUMNS)}")

    expected_ids_by_type = source_ids()
    expected_all_ids = set().union(*expected_ids_by_type.values())
    inventory_ids = [row.get("inventory_id", "") for row in rows]
    if len(inventory_ids) != len(set(inventory_ids)):
        errors.append("inventory contains duplicate IDs")
    actual_all_ids = set(inventory_ids)
    if actual_all_ids != expected_all_ids:
        errors.append(
            "inventory IDs differ from authority sources "
            f"missing={sorted(expected_all_ids - actual_all_ids)} "
            f"extra={sorted(actual_all_ids - expected_all_ids)}"
        )

    type_counts = Counter(row.get("authority_type", "") for row in rows)
    if dict(type_counts) != EXPECTED_COUNTS:
        errors.append(f"authority-type counts differ: {dict(sorted(type_counts.items()))}")

    for authority_type, expected_ids in expected_ids_by_type.items():
        actual_ids = {
            row["inventory_id"]
            for row in rows
            if row.get("authority_type") == authority_type
        }
        if actual_ids != expected_ids:
            errors.append(
                f"{authority_type} IDs differ "
                f"missing={sorted(expected_ids - actual_ids)} extra={sorted(actual_ids - expected_ids)}"
            )

    coverage_rows = read_csv(TECH / "REQUIREMENT_COVERAGE_MATRIX.csv")
    verdict_by_id = {row["id"]: row["classification"] for row in coverage_rows}
    blocker_register = yaml.safe_load((TECH / "BLOCKING_DECISIONS.yaml").read_text(encoding="utf-8"))
    known_blockers = {item["id"] for item in blocker_register["decisions"]}
    active_blockers = {
        item["id"]
        for item in blocker_register["decisions"]
        if str(item.get("status", "")).startswith("BLOCKING_")
    }

    valid_spec_refs = {f"TS-{number:02d}" for number in range(16)} | {"IMPLEMENTATION_BASELINE"}

    for row in rows:
        inventory_id = row.get("inventory_id", "<unknown>")
        authority_type = row.get("authority_type", "")
        for field in (
            "title",
            "normative_text",
            "acceptance_or_enforcement",
            "release_scope",
            "planning_disposition",
            "feature_or_domain",
            "primary_specs",
            "verification_refs",
            "source_evidence",
            "repository_coverage_basis",
            "planning_owner",
        ):
            if not row.get(field, "").strip():
                errors.append(f"{inventory_id}: empty {field}")

        verdict = row.get("coverage_verdict", "")
        if authority_type in {"FUNCTIONAL_REQUIREMENT", "NON_FUNCTIONAL_REQUIREMENT"}:
            if verdict not in ALLOWED_VERDICTS:
                errors.append(f"{inventory_id}: invalid coverage verdict {verdict!r}")
            if verdict != verdict_by_id.get(inventory_id):
                errors.append(f"{inventory_id}: coverage verdict differs from Stage 1 matrix")
        elif verdict:
            errors.append(f"{inventory_id}: non-FR/NFR row has a coverage verdict")

        unknown_specs = refs(row.get("primary_specs")) - valid_spec_refs
        if unknown_specs:
            errors.append(f"{inventory_id}: unknown primary specs {sorted(unknown_specs)}")

        blocker_refs = refs(row.get("blocking_decisions"))
        if blocker_refs - known_blockers:
            errors.append(f"{inventory_id}: unknown blockers {sorted(blocker_refs - known_blockers)}")
        expected_active = blocker_refs & active_blockers
        actual_active = refs(row.get("active_blockers"))
        if actual_active != expected_active:
            errors.append(
                f"{inventory_id}: active blockers differ "
                f"expected={sorted(expected_active)} actual={sorted(actual_active)}"
            )

        for source in refs(row.get("source_evidence")):
            source_path = source.split("#", 1)[0]
            if source_path and not (ROOT / source_path).is_file():
                errors.append(f"{inventory_id}: source does not exist: {source_path}")

        if row.get("epic_ids") or row.get("story_ids"):
            errors.append(f"{inventory_id}: Epic/Story assignment exists before Epic Step 2 authorization")

    represented_active = {
        blocker
        for row in rows
        for blocker in refs(row.get("active_blockers"))
    }
    if represented_active != active_blockers:
        errors.append(
            "active blocker coverage differs "
            f"missing={sorted(active_blockers - represented_active)} "
            f"extra={sorted(represented_active - active_blockers)}"
        )

    if not PRESERVATION_RECEIPT.is_file():
        errors.append("V1.1 preservation receipt is missing")
        preservation = {}
    else:
        preservation = json.loads(PRESERVATION_RECEIPT.read_text(encoding="utf-8"))
        if preservation.get("original_inventory_sha256") != "3892c33a00f769b4704603f0067c565355bd57a7127e7b9433724fbb4ac197fa":
            errors.append("V1.1 preservation receipt hash differs from frozen Batch A baseline")
        if preservation.get("original_inventory_rows") != 401:
            errors.append("V1.1 preservation receipt row count is not 401")
        original_ids = set(preservation.get("original_inventory_ids", []))
        if len(original_ids) != 401 or not original_ids <= actual_all_ids:
            errors.append("not all 401 original inventory IDs are retained")
        expected_additions = {f"CONST-{number:03d}" for number in range(1, 9)} | {"HG-015"}
        if actual_all_ids - original_ids != expected_additions:
            errors.append(f"V1.2 additions differ: {sorted(actual_all_ids-original_ids)}")

    if not CHANGED_REPORT.is_file():
        errors.append("V1.2 changed-obligation report is missing")
        changed_rows = []
    else:
        changed_rows = read_csv(CHANGED_REPORT)
        if len({row["inventory_id"] for row in changed_rows}) != len(changed_rows):
            errors.append("changed-obligation report has duplicate IDs")
        if any(row["change_kind"] == "REMOVED" for row in changed_rows):
            errors.append("changed-obligation report removes an existing obligation")
        added_ids = {row["inventory_id"] for row in changed_rows if row["change_kind"] == "ADDED"}
        if added_ids != {f"CONST-{number:03d}" for number in range(1, 9)} | {"HG-015"}:
            errors.append(f"changed-obligation additions differ: {sorted(added_ids)}")

    if not CONFIRMATION_PACKAGE.is_file():
        errors.append("human-confirmation package is missing")
    else:
        confirmation_text = CONFIRMATION_PACKAGE.read_text(encoding="utf-8")
        for term in ("410-row", "CONFIRM V1.2 INVENTORY", "Epic Step 2", "implementation readiness remains `FAIL`"):
            if term not in confirmation_text:
                errors.append(f"confirmation package missing term: {term}")

    confirmation_error_count = len(errors)
    if not CONFIRMATION_RECEIPT.is_file():
        errors.append("V1.2 inventory confirmation receipt is missing")
        confirmation_receipt = {}
    else:
        confirmation_receipt = yaml.safe_load(CONFIRMATION_RECEIPT.read_text(encoding="utf-8"))
        receipt_inventory = confirmation_receipt.get("inventory", {})
        receipt_boundary = confirmation_receipt.get("authorization_boundary", {})
        inventory_hash = hashlib.sha256(INVENTORY.read_bytes()).hexdigest() if INVENTORY.is_file() else ""
        if confirmation_receipt.get("status") != "CONFIRMED":
            errors.append("inventory confirmation receipt status is not CONFIRMED")
        if confirmation_receipt.get("confirmation_text") != "CONFIRM V1.2 INVENTORY":
            errors.append("inventory confirmation receipt does not preserve the exact human response")
        if receipt_inventory.get("rows") != 410:
            errors.append("inventory confirmation receipt row count is not 410")
        if receipt_inventory.get("sha256") != inventory_hash:
            errors.append("confirmed inventory hash differs from the current inventory")
        if receipt_inventory.get("epic_assignments") != 0 or receipt_inventory.get("story_assignments") != 0:
            errors.append("inventory confirmation receipt records Epic/Story assignments")
        if receipt_boundary.get("planning_inventory_confirmed") is not True:
            errors.append("inventory confirmation receipt does not confirm the planning inventory")
        if receipt_boundary.get("epic_step_2_authorized") is not False:
            errors.append("inventory confirmation receipt improperly authorizes Epic Step 2")
        if receipt_boundary.get("production_implementation_authorized") is not False:
            errors.append("inventory confirmation receipt improperly authorizes production implementation")
    confirmation_valid = len(errors) == confirmation_error_count

    epic_step_2_authorized = False
    if not EPIC_STEP_2_AUTHORIZATION.is_file():
        errors.append("Epic Step 2 authorization receipt is missing")
    else:
        epic_authorization = yaml.safe_load(EPIC_STEP_2_AUTHORIZATION.read_text(encoding="utf-8"))
        epic_step_2_authorized = epic_authorization.get("status") == "AUTHORIZED"
        if not epic_step_2_authorized:
            errors.append("Epic Step 2 authorization receipt is not AUTHORIZED")
        if epic_authorization.get("scope", {}).get("vertical_story_authoring") != "prohibited_pending_human_epic_confirmation":
            errors.append("Epic Step 2 authorization does not preserve the Story-authoring stop gate")

    by_id = {row["inventory_id"]: row for row in rows}
    required_current_terms = {
        "FR-137": "Activative Intelligence Pack",
        "FR-139": "Conversational Activation / Human Expression",
        "FR-145": "Expression Moment",
        "FR-146": "silence",
        "FR-147": "participant roles",
        "FR-169": "all five category constitutions",
        "D031": "Current V1.2 effect",
        "AG-004": "five canonical categories",
        "HG-015": "constitutional semantic stack or conversational category missing",
    }
    for inventory_id, term in required_current_terms.items():
        body = f"{by_id.get(inventory_id, {}).get('title', '')} {by_id.get(inventory_id, {}).get('normative_text', '')}".lower()
        if term.lower() not in body:
            errors.append(f"{inventory_id}: current-effect term missing: {term}")

    baseline_text = BASELINE.read_text(encoding="utf-8") if BASELINE.is_file() else ""
    if "Status: `CONFIRMED`" not in baseline_text:
        errors.append("planning baseline status is not CONFIRMED")
    expected_epic_gate = "SATISFIED_STEP_2_AUTHORIZED" if epic_step_2_authorized else "BLOCKED_PENDING_EXPLICIT_EPIC_STEP_2_AUTHORIZATION"
    if f"Epic-design gate: `{expected_epic_gate}`" not in baseline_text:
        errors.append(f"epic-design gate does not match {expected_epic_gate}")

    story_step_3_authorized = False
    if EPIC_INVENTORY_CONFIRMATION.is_file():
        epic_confirmation = yaml.safe_load(EPIC_INVENTORY_CONFIRMATION.read_text(encoding="utf-8"))
        story_step_3_authorized = (
            epic_confirmation.get("status") == "CONFIRMED_STEP_3_AUTHORIZED"
            and epic_confirmation.get("authorization_boundary", {}).get("vertical_story_authoring_step_3") == "authorized"
        )

    status = "PASS" if not errors else "FAIL"
    report = {
        "status": status,
        "inventory_confirmation_gate": "CONFIRMED" if confirmation_valid else "INVALID",
        "epic_design_gate": expected_epic_gate,
        "vertical_story_authoring_gate": (
            "SATISFIED_STEP_3_AUTHORIZED" if story_step_3_authorized else "NOT_AUTHORIZED"
        ),
        "step_4_gate": "NOT_AUTHORIZED",
        "implementation_readiness_gate": "FAIL",
        "inventory_rows": len(rows),
        "v1_1_rows_preserved": preservation.get("original_inventory_rows", 0),
        "changed_obligation_rows": len(changed_rows),
        "v1_2_added_rows": sum(row.get("change_kind") == "ADDED" for row in changed_rows),
        "v1_2_removed_rows": sum(row.get("change_kind") == "REMOVED" for row in changed_rows),
        "authority_type_counts": dict(sorted(type_counts.items())),
        "fr_nfr_verdict_counts": dict(
            sorted(Counter(row["coverage_verdict"] for row in rows if row.get("coverage_verdict")).items())
        ),
        "active_blockers": sorted(active_blockers),
        "epic_assignments": sum(bool(row.get("epic_ids")) for row in rows),
        "story_assignments": sum(bool(row.get("story_ids")) for row in rows),
        "errors": errors,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
