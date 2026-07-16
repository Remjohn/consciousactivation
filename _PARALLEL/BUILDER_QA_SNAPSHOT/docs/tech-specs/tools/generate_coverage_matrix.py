"""Generate the technical-specification FR/NFR coverage matrix.

Documentation tooling only; this is not Builder runtime code.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "docs/tech-specs/REQUIREMENT_COVERAGE_MATRIX.csv"

ALLOWED = {
    "IMPLEMENTED_AND_KEEP",
    "IMPLEMENTED_BUT_ALIGN",
    "PARTIALLY_IMPLEMENTED",
    "NEW_IMPLEMENTATION",
    "REPLACE_EXISTING_BEHAVIOR",
    "NEEDS_EMPIRICAL_PROTOTYPE",
    "DEFERRED",
    "NOT_APPLICABLE",
}

FEATURE_SPEC = {
    "F01": "TS-01", "F02": "TS-02", "F03": "TS-03", "F04": "TS-04",
    "F05": "TS-05", "F06": "TS-06", "F07": "TS-07", "F08": "TS-07",
    "F09": "TS-08", "F10": "TS-09", "F11": "TS-10", "F12": "TS-12",
    "F13": "TS-13", "F14": "TS-11", "F15": "TS-13", "F16": "TS-15",
    "F17": "TS-11", "F18": "TS-14",
}

EMPIRICAL_FR = {
    *(f"FR-{i:03d}" for i in range(19, 32)),
    "FR-032", "FR-034", "FR-035", "FR-037", "FR-039",
    "FR-103", "FR-104", "FR-105", "FR-106", "FR-109", "FR-110",
    "FR-111", "FR-113", "FR-115", "FR-145", "FR-146", "FR-147", "FR-167",
}
NOT_APPLICABLE_FR = {f"FR-{i:03d}" for i in range(160, 167)}
DEFERRED_FR = {"FR-169"}

NFR_SPEC = {
    "REL": "TS-06", "PERF": "TS-14", "TRACE": "TS-06", "OBS": "TS-12",
    "SEC": "TS-02", "COMPAT": "TS-06", "PORT": "TS-02", "UX": "TS-12",
    "EVAL": "TS-10", "MAINT": "TS-06", "SCALE": "TS-02", "ARCH": "TS-07",
    "TEST": "TS-14", "CAT": "TS-11", "WORKFLOW": "TS-14",
}
NFR_SPEC_OVERRIDES = {
    "NFR-REL-002": "TS-01", "NFR-REL-004": "TS-14",
    "NFR-PERF-001": "TS-12", "NFR-TRACE-002": "TS-12",
    "NFR-TRACE-003": "TS-10", "NFR-TRACE-004": "TS-02",
    "NFR-SEC-003": "TS-01", "NFR-SEC-004": "TS-14",
    "NFR-COMPAT-001": "IMPLEMENTATION_BASELINE", "NFR-PORT-002": "TS-14",
    "NFR-MAINT-002": "TS-08", "NFR-MAINT-003": "TS-11",
    "NFR-ARCH-002": "TS-14", "NFR-TEST-001": "TS-14",
}
EMPIRICAL_NFR = {
    "NFR-PERF-001", "NFR-PERF-002", "NFR-PERF-003", "NFR-EVAL-002",
    "NFR-EVAL-004", "NFR-SCALE-001", "NFR-CAT-003",
}

FEATURE_BLOCKERS = {
    "F01": "BD-001;BD-005", "F02": "BD-004;BD-005", "F03": "BD-004;BD-007",
    "F04": "BD-004;BD-007", "F05": "BD-005", "F06": "BD-001;BD-005",
    "F07": "BD-001", "F08": "BD-001", "F09": "BD-010", "F10": "BD-010",
    "F11": "BD-004;BD-008", "F12": "BD-005;BD-009", "F13": "BD-008",
    "F14": "BD-004;BD-007;BD-008;BD-010;BD-014", "F15": "BD-008", "F16": "BD-003",
    "F17": "BD-014", "F18": "BD-005;BD-006;BD-012;BD-013",
}


def fr_classification(item: dict) -> str:
    item_id = item["id"]
    if item_id in NOT_APPLICABLE_FR:
        return "NOT_APPLICABLE"
    if item_id in DEFERRED_FR:
        return "DEFERRED"
    if item_id in EMPIRICAL_FR:
        return "NEEDS_EMPIRICAL_PROTOTYPE"
    return "NEW_IMPLEMENTATION"


def fr_release(item: dict) -> str:
    number = int(item["id"].split("-")[1])
    if item["id"] in NOT_APPLICABLE_FR:
        return "N/A_NO_LOCAL_V2_1"
    if item["id"] == "FR-169":
        return "RELEASE_5_GENERAL_CERTIFICATION"
    if 137 <= number <= 150:
        return "R1_FORMAT02_PRODUCTION_OTHER_CATEGORIES_STRUCTURAL"
    if item["id"] in {"FR-172", "FR-173"}:
        return "R1_STRUCTURAL_EXTERNAL_TARGET_UNCERTIFIED"
    return "RELEASE_1"


def nfr_classification(item: dict) -> str:
    if item["id"] == "NFR-COMPAT-001":
        return "NOT_APPLICABLE"
    if item["id"] in EMPIRICAL_NFR:
        return "NEEDS_EMPIRICAL_PROTOTYPE"
    return "NEW_IMPLEMENTATION"


def evidence(item: dict, classification: str) -> str:
    if classification == "NOT_APPLICABLE":
        return "docs/tech-specs/REPOSITORY_INVENTORY.md#v21-determination;governance/SOURCE_REGISTER.json"
    return f"docs/tech-specs/REPOSITORY_INVENTORY.md#implementation-search;{item['source_file']}"


def basis(classification: str) -> str:
    if classification == "NOT_APPLICABLE":
        return "No V2.1 source, schema, package, workflow, or test exists inside the repository; migration coverage cannot be inferred from PRD history."
    if classification == "DEFERRED":
        return "The PRD schedules general Builder certification after the Release 1 reference and transfer portfolio."
    if classification == "NEEDS_EMPIRICAL_PROTOTYPE":
        return "No product implementation exists, and the required algorithm, quality, threshold, or scale behavior must be calibrated with authoritative evidence before production authorization."
    return "No product implementation, product schema, workflow, or production test exists in the repository; this behavior requires new implementation."


def main() -> None:
    registry = json.loads((ROOT / "governance/REQUIREMENTS_REGISTRY.json").read_text(encoding="utf-8"))
    rows = []
    for item in registry["functional_requirements"]:
        classification = fr_classification(item)
        primary_spec = "IMPLEMENTATION_BASELINE" if item["id"] in NOT_APPLICABLE_FR else FEATURE_SPEC[item["feature_id"]]
        rows.append({
            "id": item["id"], "type": "FR", "title": item["title"],
            "feature_or_domain": item["feature_id"], "classification": classification,
            "release_scope": fr_release(item), "primary_spec": primary_spec,
            "requirement_text": item["requirement"], "repository_evidence": evidence(item, classification),
            "coverage_basis": basis(classification),
            "blocking_decisions": "BD-004;BD-007;BD-008;BD-010;BD-014" if item["id"] == "FR-169" else FEATURE_BLOCKERS[item["feature_id"]],
        })
    for item in registry["non_functional_requirements"]:
        domain = item["id"].split("-")[1]
        classification = nfr_classification(item)
        rows.append({
            "id": item["id"], "type": "NFR", "title": item["title"],
            "feature_or_domain": domain, "classification": classification,
            "release_scope": "N/A_NO_LOCAL_V2_1" if classification == "NOT_APPLICABLE" else "RELEASE_1",
            "primary_spec": NFR_SPEC_OVERRIDES.get(item["id"], NFR_SPEC[domain]),
            "requirement_text": item["requirement"], "repository_evidence": evidence(item, classification),
            "coverage_basis": basis(classification),
            "blocking_decisions": "BD-003" if classification == "NOT_APPLICABLE" else "BD-001",
        })

    assert len(rows) == 263
    assert len({row["id"] for row in rows}) == 263
    assert {row["classification"] for row in rows} <= ALLOWED
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
