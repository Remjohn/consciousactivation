"""Validate Builder Next architecture and ADR traceability."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
ARCH = ROOT / "docs/architecture"
TECH = ROOT / "docs/tech-specs"
REQUIRED_ARCH_SECTIONS = (
    "Authority And Purpose", "Non-Goals And Frozen Boundaries", "System Context",
    "Architecture Style", "Logical Components", "Canonical State And Identity",
    "Persistence And Consistency", "Harness IR And Compilation", "Builder Workflow Runtime",
    "Security And Isolation", "Observability And Operations", "Deployment Topology",
    "Reliability And Performance", "Testing Architecture", "Architecture Completion Gate",
)
REQUIRED_ADR_SECTIONS = (
    "Context", "Decision", "Alternatives", "Interfaces", "Authority", "Security",
    "Determinism", "Consequences", "Observability", "Performance", "Migration", "Verification",
)


def main() -> None:
    errors: list[str] = []
    registry = json.loads((ROOT / "governance/REQUIREMENTS_REGISTRY.json").read_text(encoding="utf-8"))
    expected_ids = {item["id"] for item in registry["functional_requirements"] + registry["non_functional_requirements"]}
    trace_rows = list(csv.DictReader((ARCH / "ARCHITECTURE_TRACEABILITY_MATRIX.csv").open(encoding="utf-8")))
    observed_ids = {row["id"] for row in trace_rows}
    if len(trace_rows) != 263 or len(observed_ids) != 263 or observed_ids != expected_ids:
        errors.append(f"requirement trace closure failed: rows={len(trace_rows)} unique={len(observed_ids)}")
    for row in trace_rows:
        for field in ("tech_spec", "component_id", "architecture_component", "adr_ids", "architecture_mechanism", "verification_strategy", "requirement_source"):
            if not row[field]:
                errors.append(f"{row['id']} missing {field}")

    register = yaml.safe_load((ARCH / "ADR_REGISTER.yaml").read_text(encoding="utf-8"))
    records = register.get("records", [])
    if len(records) != 18 or len({record["id"] for record in records}) != 18:
        errors.append(f"expected 18 unique ADR records, found {len(records)}")
    allowed = set(register.get("allowed_statuses", []))
    registered_ids = {record["id"] for record in records}
    mapped_ids = {adr for row in trace_rows for adr in row["adr_ids"].split(";") if adr}
    if mapped_ids != registered_ids:
        errors.append(f"ADR trace mismatch missing={sorted(registered_ids-mapped_ids)} extra={sorted(mapped_ids-registered_ids)}")

    decision_ids = {decision for record in records for decision in record.get("decisions", [])}
    expected_decisions = {f"D{number:03d}" for number in range(1, 34)}
    if decision_ids != expected_decisions:
        errors.append(f"decision coverage mismatch missing={sorted(expected_decisions-decision_ids)} extra={sorted(decision_ids-expected_decisions)}")

    for record in records:
        if record["status"] not in allowed:
            errors.append(f"{record['id']} invalid status {record['status']}")
        path = ARCH / record["file"]
        if not path.is_file():
            errors.append(f"{record['id']} file missing: {record['file']}")
            continue
        text = path.read_text(encoding="utf-8")
        if f"Status: `{record['status']}`" not in text:
            errors.append(f"{record['id']} status differs from register")
        missing = [term for term in REQUIRED_ADR_SECTIONS if term.lower() not in text.lower()]
        if missing:
            errors.append(f"{record['id']} missing ADR terms: {missing}")
        if not any(record["id"] in row["adr_ids"].split(";") for row in trace_rows):
            errors.append(f"{record['id']} has no mapped FR/NFR")

    aligned_adrs = {"ADR-007", "ADR-008", "ADR-010", "ADR-011", "ADR-013", "ADR-018"}
    for record in records:
        if record["id"] in aligned_adrs:
            if record.get("constitutional_alignment") != "V1_2_PATCHED_2026_07_14":
                errors.append(f"{record['id']} missing V1.2 register marker")
            text = (ARCH / record["file"]).read_text(encoding="utf-8")
            for term in ("V1.2 Constitutional Alignment Amendment", "Implementation owner", "Component boundary", "Data / contract", "Failure behavior", "Test seam", "Acceptance criteria", "Migration / compatibility"):
                if term.lower() not in text.lower():
                    errors.append(f"{record['id']} missing V1.2 term: {term}")

    architecture = (ARCH / "ARCHITECTURE.md").read_text(encoding="utf-8")
    missing_sections = [term for term in REQUIRED_ARCH_SECTIONS if term.lower() not in architecture.lower()]
    if missing_sections:
        errors.append(f"architecture missing sections: {missing_sections}")
    for boundary in ("No Visual Asset Editor production behavior", "No shared Delegation Protocol implementation", "No V2.1 migration"):
        if boundary not in architecture:
            errors.append(f"frozen boundary missing: {boundary}")
    for term in ("Activative Intelligence Constitution V1.1", "Builder PRD V1.2", "HG-015", "five-category", "three-target"):
        if term.lower() not in architecture.lower() and term.lower() not in "\n".join((ARCH / record["file"]).read_text(encoding="utf-8") for record in records).lower():
            errors.append(f"architecture alignment term missing: {term}")

    proposed = [record["id"] for record in records if record["status"] == "PROPOSED"]
    if proposed and register.get("completion_gate") != "FAIL":
        errors.append("completion gate must be FAIL while proposed ADRs remain")
    blockers = yaml.safe_load((TECH / "BLOCKING_DECISIONS.yaml").read_text(encoding="utf-8"))
    active_blockers = [item["id"] for item in blockers.get("decisions", []) if str(item.get("status", "")).startswith("BLOCKING_")]
    if not active_blockers:
        errors.append("expected unresolved blockers for proposed architecture")

    ballot = yaml.safe_load((ARCH / "ARCHITECTURE_RATIFICATION_BALLOT.yaml").read_text(encoding="utf-8"))
    ballot_items = ballot.get("adr_ratifications", [])
    ballot_adr_ids = {item.get("adr_id") for item in ballot_items}
    unknown_ballot_adrs = ballot_adr_ids - registered_ids
    if unknown_ballot_adrs:
        errors.append(f"ratification ballot references unknown ADRs: {sorted(unknown_ballot_adrs)}")
    ballot_blockers = {item.get("blocker_id") for item in ballot.get("blocker_dispositions", [])}
    all_blocker_ids = {item["id"] for item in blockers.get("decisions", [])}
    unknown_ballot_blockers = ballot_blockers - all_blocker_ids
    if unknown_ballot_blockers:
        errors.append(f"ratification ballot references unknown blockers: {sorted(unknown_ballot_blockers)}")
    missing_active_blockers = set(active_blockers) - ballot_blockers
    if missing_active_blockers:
        errors.append(f"active blockers are missing from ratification ballot: {sorted(missing_active_blockers)}")
    if ballot.get("contract_ratification", {}).get("blocker_ids") != ["BD-001"]:
        errors.append("preservation-contract ratification must own BD-001")
    allowed_options = set(ballot.get("decision_options", []))
    expected_options = {"APPROVE_RECOMMENDATION", "APPROVE_WITH_AMENDMENTS", "REJECT_AND_REPLACE", "DEFER"}
    if allowed_options != expected_options:
        errors.append("ratification decision options are incomplete")
    selections = [ballot.get("contract_ratification", {}).get("selection")] + [item.get("selection") for item in ballot_items]
    invalid_selections = [selection for selection in selections if selection is not None and selection not in allowed_options]
    if invalid_selections:
        errors.append(f"invalid ratification selections: {invalid_selections}")
    if all(selection is not None for selection in selections) and ballot.get("architecture_completion_gate") == "FAIL":
        pass  # Evidence blockers can still hold the gate after all decision selections.
    if any(selection is None for selection in selections) and ballot.get("architecture_completion_gate") != "FAIL":
        errors.append("architecture gate must remain FAIL while ratification selections are pending")
    if all(selection is not None for selection in selections):
        non_accepted_ratified_adrs = [record["id"] for record in records if record["id"] in ballot_adr_ids and record["status"] != "ACCEPTED"]
        if non_accepted_ratified_adrs:
            errors.append(f"ratified ADRs are not accepted in register: {non_accepted_ratified_adrs}")
    blocker_states = {item.get("state") for item in ballot.get("blocker_dispositions", [])}
    if not blocker_states <= set(ballot.get("allowed_blocker_states", [])):
        errors.append("ratification ballot contains invalid blocker state")
    if not (ARCH / "ARCHITECTURE_RATIFICATION_PACKET.md").is_file():
        errors.append("human-readable architecture ratification packet is missing")
    open_ballot_blockers = {item["blocker_id"] for item in ballot.get("blocker_dispositions", []) if item.get("state") == "OPEN"}
    if open_ballot_blockers != set(active_blockers):
        errors.append(f"open ballot blockers differ from active blocker register: ballot={sorted(open_ballot_blockers)} register={sorted(active_blockers)}")
    if active_blockers and ballot.get("architecture_completion_gate") != "FAIL":
        errors.append("architecture completion gate must remain FAIL while active evidence blockers remain")

    receipt_path = ARCH / "ARCHITECTURE_RATIFICATION_RECEIPT.yaml"
    if not receipt_path.is_file():
        errors.append("architecture ratification receipt is missing")
        receipt = {}
    else:
        receipt = yaml.safe_load(receipt_path.read_text(encoding="utf-8"))
        expected_items = {ballot.get("contract_ratification", {}).get("item_id")} | {item.get("item_id") for item in ballot_items}
        if set(receipt.get("ratified_items", [])) != expected_items:
            errors.append("ratification receipt item coverage differs from ballot")
        if set(receipt.get("accepted_adrs", [])) != ballot_adr_ids:
            errors.append("ratification receipt ADR coverage differs from ballot")
        if set(receipt.get("open_external_or_empirical_blockers", [])) != set(active_blockers):
            errors.append("ratification receipt open blockers differ from active register")

    if any((ROOT / name).exists() for name in ("src", "tests", "apps", "packages")):
        errors.append("production implementation directory exists during architecture-only phase")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "architecture_completion_gate": register.get("completion_gate"),
        "requirements": len(trace_rows),
        "functional_requirements": sum(row["type"] == "FR" for row in trace_rows),
        "non_functional_requirements": sum(row["type"] == "NFR" for row in trace_rows),
        "adrs": len(records),
        "accepted_adrs": sum(record["status"] == "ACCEPTED" for record in records),
        "v1_2_aligned_adrs": len(aligned_adrs),
        "proposed_adrs": len(proposed),
        "locked_decisions_covered": len(decision_ids),
        "ratification_items": len(ballot_items) + 1,
        "pending_ratification_selections": sum(selection is None for selection in selections),
        "blocker_dispositions": len(ballot.get("blocker_dispositions", [])),
        "open_blocker_dispositions": len(open_ballot_blockers),
        "active_blocking_decisions": active_blockers,
        "errors": errors,
    }
    rendered = json.dumps(result, indent=2) + "\n"
    (ARCH / "ARCHITECTURE_VALIDATION_REPORT.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
