"""Validate technical-specification traceability and document shape."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
TECH = ROOT / "docs/tech-specs"
ALLOWED = {
    "IMPLEMENTED_AND_KEEP", "IMPLEMENTED_BUT_ALIGN", "PARTIALLY_IMPLEMENTED",
    "NEW_IMPLEMENTATION", "REPLACE_EXISTING_BEHAVIOR", "NEEDS_EMPIRICAL_PROTOTYPE",
    "DEFERRED", "NOT_APPLICABLE",
}
REQUIRED_TERMS = (
    "Traceability", "Responsibility", "Modules", "Canonical Data Structures",
    "Commands", "Events", "Persistence", "Dependency", "Invalidation", "Idempotency",
    "Security", "Isolation", "Observability", "Cost", "Performance", "Failures",
    "Recovery", "Acceptance Tests", "Implementation Tasks", "Non-Goals", "Migration",
)
ALIGNMENT_TERMS = (
    "V1.2 Constitutional Alignment Patch", "Implementation owner", "Component boundary",
    "Data or contract", "Failure behavior", "Test seam", "Acceptance criteria", "Migration / compatibility",
)


def extract_requirement_ids(text: str) -> set[str]:
    found = set(re.findall(r"\bFR-\d{3}\b|\bNFR-[A-Z]+-\d{3}\b", text))
    for start, end in re.findall(r"\bFR-(\d{3})\s+through\s+FR-(\d{3})\b", text, flags=re.IGNORECASE):
        found.update(f"FR-{number:03d}" for number in range(int(start), int(end) + 1))
    for domain, start, end in re.findall(
        r"\bNFR-([A-Z]+)-(\d{3})\s+through\s+NFR-\1-(\d{3})\b", text, flags=re.IGNORECASE
    ):
        found.update(f"NFR-{domain.upper()}-{number:03d}" for number in range(int(start), int(end) + 1))
    return found


def main() -> None:
    errors: list[str] = []
    registry = json.loads((ROOT / "governance/REQUIREMENTS_REGISTRY.json").read_text(encoding="utf-8"))
    expected = {item["id"] for item in registry["functional_requirements"] + registry["non_functional_requirements"]}
    rows = list(csv.DictReader((TECH / "REQUIREMENT_COVERAGE_MATRIX.csv").open(encoding="utf-8")))
    observed = {row["id"] for row in rows}
    if len(rows) != 263 or len(observed) != 263 or observed != expected:
        errors.append(f"matrix ID closure failed: rows={len(rows)} unique={len(observed)} missing={sorted(expected-observed)} extra={sorted(observed-expected)}")
    for row in rows:
        if row["classification"] not in ALLOWED:
            errors.append(f"{row['id']} invalid classification {row['classification']}")
        if not row["repository_evidence"] or not row["primary_spec"] or not row["coverage_basis"]:
            errors.append(f"{row['id']} has incomplete coverage evidence")

    spec_paths = sorted((TECH / "specs").glob("TS-*.md"))
    if len(spec_paths) != 15:
        errors.append(f"expected 15 subsystem specs, found {len(spec_paths)}")
    for path in spec_paths:
        text = path.read_text(encoding="utf-8")
        missing = [term for term in REQUIRED_TERMS if term.lower() not in text.lower()]
        if missing:
            errors.append(f"{path.name} missing required terms: {missing}")
        alignment_missing = [term for term in ALIGNMENT_TERMS if term.lower() not in text.lower()]
        if alignment_missing:
            errors.append(f"{path.name} missing V1.2 alignment terms: {alignment_missing}")

    spec_by_id = {path.name.split("-", 2)[0] + "-" + path.name.split("-", 2)[1]: path for path in spec_paths}
    owner_text = {
        spec_id: extract_requirement_ids(path.read_text(encoding="utf-8"))
        for spec_id, path in spec_by_id.items()
    }
    owner_text["IMPLEMENTATION_BASELINE"] = extract_requirement_ids(
        (TECH / "IMPLEMENTATION_BASELINE.md").read_text(encoding="utf-8")
    )
    for row in rows:
        owner = row["primary_spec"]
        if owner not in owner_text:
            errors.append(f"{row['id']} references unknown primary spec {owner}")
        elif row["id"] not in owner_text[owner]:
            errors.append(f"{row['id']} is not claimed in primary spec {owner}")

    all_spec_text = (TECH / "ARCHITECTURE_PRESERVATION_CONTRACT.md").read_text(encoding="utf-8")
    all_spec_text += "\n" + "\n".join(path.read_text(encoding="utf-8") for path in spec_paths)
    covered_decisions = {int(value) for value in re.findall(r"\bD(\d{3})\b", all_spec_text)}
    for start, end in re.findall(r"\bD(\d{3})-D(\d{3})\b", all_spec_text):
        covered_decisions.update(range(int(start), int(end) + 1))
    for number in range(1, 34):
        if number not in covered_decisions:
            errors.append(f"decision coverage not found for D{number:03d}")
    if "HG-001-HG-015" not in all_spec_text:
        errors.append("hard-gate range HG-001-HG-015 not found")
    if "AG-001-AG-022" not in all_spec_text:
        errors.append("anti-goal range AG-001-AG-022 not found")
    for term in ALIGNMENT_TERMS:
        if term.lower() not in (TECH / "ARCHITECTURE_PRESERVATION_CONTRACT.md").read_text(encoding="utf-8").lower():
            errors.append(f"TS-00 missing V1.2 alignment term: {term}")
    contract_report = json.loads((ROOT / "docs/contracts/VALIDATION_REPORT.json").read_text(encoding="utf-8"))
    if contract_report.get("status") != "PASS":
        errors.append("Builder contract schemas/examples are not validated PASS")
    required_constitutional_terms = ["Activation First", "Visual Syntax First", "Reaction Receipt", "Expression Moment", "HG-015", "all five"]
    for term in required_constitutional_terms:
        if term.lower() not in all_spec_text.lower():
            errors.append(f"technical specification set missing constitutional term: {term}")

    blockers = yaml.safe_load((TECH / "BLOCKING_DECISIONS.yaml").read_text(encoding="utf-8"))
    if blockers.get("implementation_gate") != "FAIL":
        errors.append("implementation gate must remain FAIL while blockers exist")
    if not any(str(item.get("status", "")).startswith("BLOCKING_") for item in blockers.get("decisions", [])):
        errors.append("blocking decision register has no active blocker")

    prohibited_runtime_dirs = [ROOT / name for name in ("src", "tests", "apps", "packages")]
    if any(path.exists() for path in prohibited_runtime_dirs):
        errors.append("production implementation directory was created during specification work")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "matrix_rows": len(rows),
        "fr_rows": sum(row["type"] == "FR" for row in rows),
        "nfr_rows": sum(row["type"] == "NFR" for row in rows),
        "spec_files": len(spec_paths) + 1,
        "constitutional_alignment": "V1_2_PATCHED",
        "contract_validation": contract_report.get("status"),
        "errors": errors,
    }
    rendered = json.dumps(result, indent=2) + "\n"
    (TECH / "TECH_SPEC_VALIDATION_REPORT.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
