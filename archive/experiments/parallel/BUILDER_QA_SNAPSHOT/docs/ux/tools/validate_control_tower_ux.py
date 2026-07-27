from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
UX = ROOT / "docs" / "ux"
CONTRACT = UX / "HARNESS_CONTROL_TOWER_UX_CONTRACT.md"
MATRIX = UX / "CONTROL_TOWER_UX_TRACEABILITY_MATRIX.csv"
REPORT = UX / "CONTROL_TOWER_UX_VALIDATION_REPORT.json"
RECEIPT = UX / "CONTROL_TOWER_UX_APPROVAL_RECEIPT.yaml"

REQUIRED_OWNED = {
    *(f"FR-{number}" for number in range(117, 127)),
    "NFR-PERF-001",
    "NFR-TRACE-002",
    "NFR-OBS-001",
    "NFR-OBS-002",
    "NFR-OBS-003",
    "NFR-OBS-004",
    "NFR-UX-001",
    "NFR-UX-002",
}

REQUIRED_DECISIONS = {
    "D002", "D007", "D010", "D011", "D013", "D014", "D015",
    "D017", "D018", "D020", "D021", "D024", "D025", "D026",
    "D027", "D029", "D033",
}

REQUIRED_SECTIONS = {
    "## 4. Information Architecture",
    "## 6. Truth, Freshness, And Status Semantics",
    "## 7. Surface Contracts",
    "## 8. Governed Action Contract",
    "## 9. Loading, Empty, Degraded, And Failure States",
    "## 10. Accessibility Contract",
    "## 11. Security, Privacy, And Disclosure",
    "## 12. Performance And Scale Budgets",
    "## 14. Acceptance Test Catalog",
    "## 15. Story-Slicing Constraints",
    "## 16. Explicit Non-Goals",
    "## 18. Approval Gate",
}


def split_refs(value: str) -> set[str]:
    return {item.strip() for item in value.split(";") if item.strip()}


def main() -> int:
    errors: list[str] = []

    if not CONTRACT.is_file():
        errors.append("UX contract is missing")
        contract_text = ""
    else:
        contract_text = CONTRACT.read_text(encoding="utf-8")

    if "Status: `APPROVED`" not in contract_text:
        errors.append("UX contract status is not APPROVED")

    if not RECEIPT.is_file():
        errors.append("UX approval receipt is missing")
        receipt_text = ""
    else:
        receipt_text = RECEIPT.read_text(encoding="utf-8")

    required_receipt_values = {
        "outcome: APPROVED",
        "approved_artifact: docs/ux/HARNESS_CONTROL_TOWER_UX_CONTRACT.md",
        "artifact_id: CTUX-001",
        "approved_version: 1.0.0",
        "authority: human_product_and_ux_authority",
    }
    for value in sorted(required_receipt_values):
        if value not in receipt_text:
            errors.append(f"UX approval receipt is missing: {value}")
    if not re.search(r"prior_pending_contract_sha256: [0-9a-f]{64}\b", receipt_text):
        errors.append("UX approval receipt lacks a valid pre-approval SHA-256")

    for section in sorted(REQUIRED_SECTIONS):
        if section not in contract_text:
            errors.append(f"required UX contract section is missing: {section}")

    clause_ids = set(re.findall(r"\bUXC-\d{3}\b", contract_text))
    acceptance_ids = set(re.findall(r"\bAT-UX-\d{3}\b", contract_text))
    decision_ids = set(re.findall(r"\bD\d{3}\b", contract_text))

    missing_decisions = REQUIRED_DECISIONS - decision_ids
    if missing_decisions:
        errors.append(f"locked decisions missing from UX contract: {sorted(missing_decisions)}")

    rows: list[dict[str, str]] = []
    if not MATRIX.is_file():
        errors.append("UX traceability matrix is missing")
    else:
        with MATRIX.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))

    required_columns = {
        "requirement_id", "relationship", "title", "contract_clauses",
        "surfaces", "acceptance_tests", "source",
    }
    if rows and set(rows[0]) != required_columns:
        errors.append(f"UX matrix columns differ: {sorted(set(rows[0]) ^ required_columns)}")

    requirement_ids = [row.get("requirement_id", "") for row in rows]
    if len(requirement_ids) != len(set(requirement_ids)):
        errors.append("UX matrix contains duplicate requirement IDs")

    owned = {
        row.get("requirement_id", "")
        for row in rows
        if row.get("relationship") == "OWNED"
    }
    missing_owned = REQUIRED_OWNED - owned
    unexpected_owned = owned - REQUIRED_OWNED
    if missing_owned or unexpected_owned:
        errors.append(
            "owned UX requirements differ "
            f"missing={sorted(missing_owned)} extra={sorted(unexpected_owned)}"
        )

    for row in rows:
        requirement_id = row.get("requirement_id", "<unknown>")
        if row.get("relationship") not in {"OWNED", "SUPPORTING"}:
            errors.append(f"{requirement_id}: invalid relationship")
        for field in ("title", "contract_clauses", "surfaces", "acceptance_tests", "source"):
            if not row.get(field, "").strip():
                errors.append(f"{requirement_id}: empty {field}")

        unknown_clauses = split_refs(row.get("contract_clauses", "")) - clause_ids
        if unknown_clauses:
            errors.append(f"{requirement_id}: unknown contract clauses {sorted(unknown_clauses)}")

        unknown_tests = split_refs(row.get("acceptance_tests", "")) - acceptance_ids
        if unknown_tests:
            errors.append(f"{requirement_id}: unknown acceptance tests {sorted(unknown_tests)}")

        source = row.get("source", "").split("#", 1)[0]
        if source and not (ROOT / source).is_file():
            errors.append(f"{requirement_id}: source does not exist: {source}")

    status = "PASS" if not errors else "FAIL"
    report = {
        "status": status,
        "adoption_gate": "SATISFIED",
        "implementation_readiness_gate": "FAIL",
        "matrix_rows": len(rows),
        "owned_requirements": len(owned),
        "supporting_requirements": len(rows) - len(owned),
        "contract_clauses": len(clause_ids),
        "acceptance_tests": len(acceptance_ids),
        "locked_decisions_covered": len(REQUIRED_DECISIONS & decision_ids),
        "errors": errors,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
