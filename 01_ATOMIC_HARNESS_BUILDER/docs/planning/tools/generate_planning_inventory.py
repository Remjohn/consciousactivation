from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "docs"
PLANNING = DOCS / "planning"
ARCH = DOCS / "architecture"
TECH = DOCS / "tech-specs"
UX = DOCS / "ux"
GOV = ROOT / "governance"

OUTPUT = PLANNING / "PLANNING_REQUIREMENTS_INVENTORY.csv"
BASELINE = PLANNING / "REQUIREMENTS_EXTRACTION_BASELINE.md"
PRESERVATION_RECEIPT = PLANNING / "V1_1_BASELINE_PRESERVATION_RECEIPT.json"
CHANGED_CSV = PLANNING / "V1_2_CHANGED_OBLIGATIONS.csv"
CHANGED_MD = PLANNING / "V1_2_CHANGED_OBLIGATIONS.md"
CONFIRMATION = PLANNING / "V1_2_INVENTORY_CONFIRMATION_PACKAGE.md"
CONFIRMATION_RECEIPT = PLANNING / "V1_2_INVENTORY_CONFIRMATION_RECEIPT.yaml"
EPIC_STEP_2_AUTHORIZATION = PLANNING / "EPIC_STEP_2_AUTHORIZATION_RECEIPT.yaml"

COLUMNS = [
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
]

HARD_GATE_SPEC_MAP = {
    "HG-001": ["TS-01", "TS-05", "TS-13"],
    "HG-002": ["TS-02", "TS-03", "TS-10", "TS-13"],
    "HG-003": ["TS-04", "TS-11", "TS-15"],
    "HG-004": ["TS-06", "TS-07", "TS-13", "TS-14"],
    "HG-005": ["TS-06", "TS-07", "TS-13"],
    "HG-006": ["TS-08", "TS-10", "TS-13"],
    "HG-007": ["TS-01", "TS-05", "TS-07", "TS-13", "TS-14"],
    "HG-008": ["TS-10", "TS-14"],
    "HG-009": ["TS-10", "TS-13"],
    "HG-010": ["TS-00"],
    "HG-011": ["TS-07", "TS-14"],
    "HG-012": ["TS-14"],
    "HG-013": ["TS-14"],
    "HG-014": ["TS-10", "TS-14"],
    "HG-015": ["TS-00", "TS-03", "TS-06", "TS-10", "TS-11", "TS-13", "TS-15"],
}

CONSTITUTIONAL_PLANNING_MAP = {
    "CONST-001": {"specs": ["TS-00", "TS-01", "TS-06", "TS-13"], "components": ["Architecture Policy", "Run Governance", "Harness IR And Compilers", "Repair, Authorization, Handoff"], "refs": ["FR-137", "FR-139", "FR-145", "FR-146", "FR-147"], "adrs": ["ADR-005", "ADR-013"], "blockers": []},
    "CONST-002": {"specs": ["TS-01", "TS-04", "TS-11", "TS-12"], "components": ["Run Governance", "Atomicity", "Category And Target Compilers", "Control Tower"], "refs": ["FR-139", "FR-169"], "adrs": ["ADR-011", "ADR-013", "ADR-014"], "blockers": ["BD-004", "BD-007", "BD-008", "BD-010", "BD-014"]},
    "CONST-003": {"specs": ["TS-05", "TS-06", "TS-07", "TS-09", "TS-11"], "components": ["Genesis", "Harness IR And Compilers", "Architecture Graphs", "JIT Capsule Compiler", "Category And Target Compilers"], "refs": ["FR-137"], "adrs": ["ADR-004", "ADR-005", "ADR-013"], "blockers": ["BD-004"]},
    "CONST-004": {"specs": ["TS-02", "TS-06", "TS-07", "TS-10", "TS-11", "TS-12", "TS-14"], "components": ["Evidence Workspace", "Harness IR And Compilers", "Architecture Graphs", "Evaluation", "Category And Target Compilers", "Control Tower", "Workflow Runtime"], "refs": ["FR-145", "FR-146", "FR-147"], "adrs": ["ADR-007", "ADR-010", "ADR-011", "ADR-013"], "blockers": ["BD-004", "BD-008", "BD-010"]},
    "CONST-005": {"specs": ["TS-03", "TS-06", "TS-07", "TS-10", "TS-11", "TS-13", "TS-14", "TS-15"], "components": ["Visual Understanding", "Harness IR And Compilers", "Architecture Graphs", "Evaluation", "Category And Target Compilers", "Repair, Authorization, Handoff", "Workflow Runtime", "Format 02 Reference Slice"], "refs": ["FR-137", "FR-145", "FR-147"], "adrs": ["ADR-008", "ADR-010", "ADR-013", "ADR-018"], "blockers": ["BD-007", "BD-008", "BD-014"]},
    "CONST-006": {"specs": ["TS-00", "TS-03", "TS-05", "TS-11", "TS-14", "TS-15"], "components": ["Architecture Policy", "Visual Understanding", "Genesis", "Category And Target Compilers", "Workflow Runtime", "Format 02 Reference Slice"], "refs": ["FR-137", "FR-145", "FR-146", "FR-147"], "adrs": ["ADR-008", "ADR-013"], "blockers": ["BD-007"]},
    "CONST-007": {"specs": ["TS-03", "TS-06", "TS-10", "TS-11", "TS-13", "TS-15"], "components": ["Visual Understanding", "Harness IR And Compilers", "Evaluation", "Category And Target Compilers", "Repair, Authorization, Handoff", "Format 02 Reference Slice"], "refs": ["FR-137", "FR-145", "FR-147", "HG-015"], "adrs": ["ADR-008", "ADR-010", "ADR-013", "ADR-018"], "blockers": ["BD-008"]},
    "CONST-008": {"specs": ["TS-10", "TS-11", "TS-12", "TS-13", "TS-15"], "components": ["Evaluation", "Category And Target Compilers", "Control Tower", "Repair, Authorization, Handoff", "Format 02 Reference Slice"], "refs": ["FR-169", "HG-015"], "adrs": ["ADR-010", "ADR-011", "ADR-013"], "blockers": ["BD-008"]},
}

ANTI_GOAL_SPEC_MAP = {
    "AG-001": ["TS-00", "TS-01", "TS-13", "TS-15"],
    "AG-002": ["TS-00", "TS-01", "TS-11"],
    "AG-003": ["TS-00", "TS-04", "TS-11"],
    "AG-004": ["TS-00", "TS-11"],
    "AG-005": ["TS-00", "TS-11", "TS-15"],
    "AG-006": ["TS-00", "TS-03"],
    "AG-007": ["TS-00", "TS-03", "TS-05"],
    "AG-008": ["TS-00", "TS-07", "TS-08"],
    "AG-009": ["TS-00", "TS-08", "TS-09"],
    "AG-010": ["TS-00", "TS-08", "TS-10"],
    "AG-011": ["TS-00", "TS-07", "TS-14"],
    "AG-012": ["TS-00", "TS-07", "TS-14"],
    "AG-013": ["TS-00", "TS-09", "TS-14"],
    "AG-014": ["TS-00", "TS-07", "TS-13"],
    "AG-015": ["TS-00", "TS-10", "TS-13"],
    "AG-016": ["TS-00", "TS-12", "TS-14"],
    "AG-017": ["TS-00", "TS-10", "TS-15"],
    "AG-018": ["TS-00", "TS-06"],
    "AG-019": ["TS-00", "TS-14"],
    "AG-020": ["TS-00", "TS-14"],
    "AG-021": ["TS-00", "TS-14"],
    "AG-022": ["TS-00", "TS-01", "TS-05", "TS-13", "TS-14"],
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def refs(value: str | None) -> set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(";") if item.strip()}


def joined(values: set[str] | list[str]) -> str:
    return ";".join(sorted(set(values)))


def flattened(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def markdown_section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return flattened(match.group(1)) if match else ""


def disposition_for(verdict: str) -> str:
    return {
        "DEFERRED": "DEFERRED_FROM_RELEASE_1",
        "NOT_APPLICABLE": "EXCLUDED_UNLESS_INVALIDATED",
        "NEEDS_EMPIRICAL_PROTOTYPE": "PROTOTYPE_OR_EVIDENCE_STORY_REQUIRED",
    }.get(verdict, "IMPLEMENTATION_STORY_REQUIRED")


def blank_row(**values: str) -> dict[str, str]:
    row = {column: "" for column in COLUMNS}
    row.update(values)
    return row


def main() -> None:
    previous_bytes = OUTPUT.read_bytes() if OUTPUT.is_file() else b""
    previous_rows = read_csv(OUTPUT) if OUTPUT.is_file() else []
    previous_by_id = {row["inventory_id"]: row for row in previous_rows}
    inventory_confirmed = CONFIRMATION_RECEIPT.is_file()
    epic_step_2_authorized = EPIC_STEP_2_AUTHORIZATION.is_file()
    requirements = json.loads((GOV / "REQUIREMENTS_REGISTRY.json").read_text(encoding="utf-8"))
    decisions = json.loads((GOV / "DECISION_REGISTER.json").read_text(encoding="utf-8"))
    anti_goals = json.loads((GOV / "ARCHITECTURAL_PROHIBITIONS.json").read_text(encoding="utf-8"))
    hard_gates = yaml.safe_load((GOV / "READINESS_HARD_GATES.yaml").read_text(encoding="utf-8"))
    adr_register = yaml.safe_load((ARCH / "ADR_REGISTER.yaml").read_text(encoding="utf-8"))
    blockers = yaml.safe_load((TECH / "BLOCKING_DECISIONS.yaml").read_text(encoding="utf-8"))

    tech_rows = read_csv(TECH / "REQUIREMENT_COVERAGE_MATRIX.csv")
    arch_rows = read_csv(ARCH / "ARCHITECTURE_TRACEABILITY_MATRIX.csv")
    ux_rows = read_csv(UX / "CONTROL_TOWER_UX_TRACEABILITY_MATRIX.csv")

    tech_by_id = {row["id"]: row for row in tech_rows}
    arch_by_id = {row["id"]: row for row in arch_rows}
    ux_by_requirement = {row["requirement_id"]: row for row in ux_rows}

    active_blockers = {
        record["id"]
        for record in blockers["decisions"]
        if str(record.get("status", "")).startswith("BLOCKING_")
    }

    adr_by_id = {record["id"]: record for record in adr_register["records"]}
    adrs_by_decision: dict[str, set[str]] = defaultdict(set)
    for record in adr_register["records"]:
        for decision_id in record.get("decisions", []):
            adrs_by_decision[decision_id].add(record["id"])

    rows: list[dict[str, str]] = []
    requirement_records = requirements["functional_requirements"] + requirements["non_functional_requirements"]

    for requirement in requirement_records:
        requirement_id = requirement["id"]
        tech = tech_by_id[requirement_id]
        arch = arch_by_id[requirement_id]
        ux = ux_by_requirement.get(requirement_id, {})
        blocker_refs = refs(tech["blocking_decisions"]) | refs(arch["blocking_decisions"])
        consequences = requirement.get("testable_consequences", [])
        acceptance = " | ".join(consequences) if consequences else arch["verification_strategy"]
        source_refs = refs(tech["repository_evidence"]) | {requirement["source_file"]}
        decision_refs = set(requirement.get("decisions", [])) | refs(arch["locked_decisions"])
        rows.append(
            blank_row(
                inventory_id=requirement_id,
                authority_type="FUNCTIONAL_REQUIREMENT" if requirement_id.startswith("FR-") else "NON_FUNCTIONAL_REQUIREMENT",
                title=requirement["title"],
                normative_text=requirement["requirement"],
                acceptance_or_enforcement=acceptance,
                release_scope=tech["release_scope"],
                coverage_verdict=tech["classification"],
                planning_disposition=disposition_for(tech["classification"]),
                feature_or_domain=tech["feature_or_domain"],
                primary_specs=tech["primary_spec"],
                architecture_components=arch["architecture_component"],
                requirement_refs=requirement_id,
                adr_refs=arch["adr_ids"],
                decision_refs=joined(decision_refs),
                ux_refs=ux.get("contract_clauses", ""),
                verification_refs=arch["verification_strategy"],
                source_evidence=joined(source_refs),
                repository_coverage_basis=tech["coverage_basis"],
                blocking_decisions=joined(blocker_refs),
                active_blockers=joined(blocker_refs & active_blockers),
                planning_owner=tech["primary_spec"],
            )
        )

    for decision in decisions["decisions"]:
        decision_id = decision["id"]
        mapped_arch = [row for row in arch_rows if decision_id in refs(row["locked_decisions"])]
        adr_ids = adrs_by_decision[decision_id]
        blocker_refs = {
            blocker
            for adr_id in adr_ids
            for blocker in adr_by_id[adr_id].get("blockers", [])
        }
        current_effect = ""
        decision_sources = {"governance/DECISION_REGISTER.json", "governance/PRODUCT_CONSTITUTION.yaml"}
        if decision_id == "D031":
            current_effect = " Current V1.2 effect: the constitutional amendment expands this historical four-category decision to five categories, including Conversational Activation / Human Expression."
            decision_sources.add("docs/product-authority/BUILDER_V1_2_CONSTITUTIONAL_ALIGNMENT_AMENDMENT.md")
        rows.append(
            blank_row(
                inventory_id=decision_id,
                authority_type="LOCKED_DECISION",
                title=decision["title"],
                normative_text=decision["decision"] + current_effect,
                acceptance_or_enforcement=decision["rationale"],
                release_scope="CROSS_CUTTING",
                planning_disposition="MANDATORY_PLANNING_CONSTRAINT",
                feature_or_domain="PRODUCT_CONSTITUTION",
                primary_specs=joined({row["tech_spec"] for row in mapped_arch}),
                architecture_components=joined({row["architecture_component"] for row in mapped_arch}),
                requirement_refs=joined(set(decision.get("mapped_functional_requirements", []))),
                adr_refs=joined(adr_ids),
                decision_refs=decision_id,
                verification_refs=joined({item for row in mapped_arch for item in refs(row["verification_strategy"])}),
                source_evidence=joined(decision_sources),
                repository_coverage_basis="Locked product authority mapped to requirements and ratified architecture; production implementation is absent.",
                blocking_decisions=joined(blocker_refs),
                active_blockers=joined(blocker_refs & active_blockers),
                planning_owner="product_constitution",
            )
        )

    for adr in adr_register["records"]:
        adr_id = adr["id"]
        adr_path = ARCH / adr["file"]
        text = adr_path.read_text(encoding="utf-8")
        mapped_arch = [row for row in arch_rows if adr_id in refs(row["adr_ids"])]
        owner_match = re.search(r"^Owners:\s*(.*?)(?:\. Trace:|$)", text, flags=re.MULTILINE)
        owner = owner_match.group(1).strip() if owner_match else "architecture"
        requirement_refs = {row["id"] for row in mapped_arch}
        blocker_refs = set(adr.get("blockers", []))
        alignment_amendment = markdown_section(text, "V1.2 Constitutional Alignment Amendment")
        rows.append(
            blank_row(
                inventory_id=adr_id,
                authority_type="ARCHITECTURE_DECISION",
                title=adr["title"],
                normative_text=markdown_section(text, "Decision"),
                acceptance_or_enforcement=flattened(" ".join(filter(None, [markdown_section(text, "Verification"), alignment_amendment]))),
                release_scope="CROSS_CUTTING",
                planning_disposition="ACCEPTED_ARCHITECTURE_CONSTRAINT",
                feature_or_domain="ARCHITECTURE",
                primary_specs=joined({row["tech_spec"] for row in mapped_arch}),
                architecture_components=joined({row["architecture_component"] for row in mapped_arch}),
                requirement_refs=joined(requirement_refs),
                adr_refs=adr_id,
                decision_refs=joined(set(adr.get("decisions", []))),
                verification_refs=joined({item for row in mapped_arch for item in refs(row["verification_strategy"])}),
                source_evidence=f"docs/architecture/{adr['file']};docs/architecture/ADR_REGISTER.yaml",
                repository_coverage_basis="Accepted architecture decision with mapped verification obligations; production implementation is absent.",
                blocking_decisions=joined(blocker_refs),
                active_blockers=joined(blocker_refs & active_blockers),
                planning_owner=owner,
            )
        )

    ux_contract = (UX / "HARNESS_CONTROL_TOWER_UX_CONTRACT.md").read_text(encoding="utf-8")
    inline_clauses = re.findall(
        r"^- \*\*(UXC-\d{3}) - (.*?):\*\* (.*)$",
        ux_contract,
        flags=re.MULTILINE,
    )
    surface_clauses = [
        (clause_id, title, flattened(body))
        for clause_id, title, body in re.findall(
            r"^### (UXC-\d{3}) - (.*?)\s*$\n(.*?)(?=^### |^## |\Z)",
            ux_contract,
            flags=re.MULTILINE | re.DOTALL,
        )
    ]
    ux_clauses = inline_clauses + surface_clauses
    ux_requirements_by_clause: dict[str, set[str]] = defaultdict(set)
    ux_tests_by_clause: dict[str, set[str]] = defaultdict(set)
    for ux_row in ux_rows:
        for clause_id in refs(ux_row["contract_clauses"]):
            ux_requirements_by_clause[clause_id].add(ux_row["requirement_id"])
            ux_tests_by_clause[clause_id] |= refs(ux_row["acceptance_tests"])

    for clause_id, title, normative_text in ux_clauses:
        requirement_ids = ux_requirements_by_clause[clause_id]
        mapped_arch = [arch_by_id[item] for item in requirement_ids if item in arch_by_id]
        blocker_refs = {item for row in mapped_arch for item in refs(row["blocking_decisions"])}
        rows.append(
            blank_row(
                inventory_id=clause_id,
                authority_type="UX_CONTRACT_CLAUSE",
                title=title,
                normative_text=normative_text,
                acceptance_or_enforcement=joined(ux_tests_by_clause[clause_id]) or "Contract review and story acceptance coverage required.",
                release_scope="RELEASE_1",
                planning_disposition="APPROVED_UX_CONSTRAINT",
                feature_or_domain="CONTROL_TOWER_UX",
                primary_specs=joined({"TS-12"} | {row["tech_spec"] for row in mapped_arch}),
                architecture_components=joined({"Control Tower"} | {row["architecture_component"] for row in mapped_arch}),
                requirement_refs=joined(requirement_ids),
                adr_refs=joined({"ADR-011", "ADR-016"} | {item for row in mapped_arch for item in refs(row["adr_ids"])}),
                decision_refs=joined({"D025", "D033"} | {item for row in mapped_arch for item in refs(row["locked_decisions"])}),
                ux_refs=clause_id,
                verification_refs=joined(ux_tests_by_clause[clause_id]),
                source_evidence="docs/ux/HARNESS_CONTROL_TOWER_UX_CONTRACT.md;docs/ux/CONTROL_TOWER_UX_APPROVAL_RECEIPT.yaml",
                repository_coverage_basis="Approved UX planning authority; production UI implementation is absent.",
                blocking_decisions=joined(blocker_refs),
                active_blockers=joined(blocker_refs & active_blockers),
                planning_owner="ux_architecture",
            )
        )

    for gate in hard_gates["gates"]:
        gate_id = gate["id"]
        human_name = gate["name"].replace("_", " ")
        rows.append(
            blank_row(
                inventory_id=gate_id,
                authority_type="READINESS_HARD_GATE",
                title=human_name.title(),
                normative_text=f"Readiness and release result must be {gate['result']} when {human_name} is present.",
                acceptance_or_enforcement="A passing receipt is invalid unless this gate is explicitly evaluated and absent or resolved by authorized evidence.",
                release_scope="CROSS_CUTTING",
                planning_disposition="MANDATORY_FAIL_GATE",
                feature_or_domain="READINESS_GOVERNANCE",
                primary_specs=joined(HARD_GATE_SPEC_MAP[gate_id]),
                decision_refs="D027;D033",
                verification_refs="hard-gate;negative;authority;receipt",
                source_evidence="governance/READINESS_HARD_GATES.yaml;docs/tech-specs/ARCHITECTURE_PRESERVATION_CONTRACT.md",
                repository_coverage_basis="Binding readiness gate; every assigned story must preserve fail-closed behavior.",
                planning_owner="evaluation_governance",
            )
        )

    delta_rows = read_csv(ROOT / "docs/constitutional-alignment/REQUIREMENT_DELTA.csv")
    for delta in delta_rows:
        amendment_id = delta["requirement_id"]
        if amendment_id not in CONSTITUTIONAL_PLANNING_MAP:
            continue
        mapping = CONSTITUTIONAL_PLANNING_MAP[amendment_id]
        blocker_refs = set(mapping["blockers"])
        rows.append(
            blank_row(
                inventory_id=amendment_id,
                authority_type="CONSTITUTIONAL_AMENDMENT",
                title=delta["change_type"].replace("_", " ").title(),
                normative_text=delta["summary"],
                acceptance_or_enforcement="The mapped contract schemas, technical specifications, ADR amendments, and HG-015 checks must validate without lower-authority override or semantic-lineage loss.",
                release_scope="CROSS_CUTTING_V1_2",
                planning_disposition="MANDATORY_CONSTITUTIONAL_CONSTRAINT",
                feature_or_domain="CONSTITUTIONAL_ALIGNMENT",
                primary_specs=joined(mapping["specs"]),
                architecture_components=joined(mapping["components"]),
                requirement_refs=joined(mapping["refs"]),
                adr_refs=joined(mapping["adrs"]),
                decision_refs="D027;D031;D033",
                verification_refs="constitutional-precedence;contract-schema;dual-order;semantic-lineage;hard-gate;negative;boundary",
                source_evidence="docs/constitutional-alignment/REQUIREMENT_DELTA.csv;docs/product-authority/BUILDER_V1_2_CONSTITUTIONAL_ALIGNMENT_AMENDMENT.md;governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml;docs/contracts/CONTRACT_REGISTRY.yaml",
                repository_coverage_basis="New standalone V1.2 constitutional planning obligation; it supplements rather than duplicates the retained FR/NFR, ADR, UX, decision, gate, and anti-goal rows.",
                blocking_decisions=joined(blocker_refs),
                active_blockers=joined(blocker_refs & active_blockers),
                planning_owner="constitutional_alignment_and_mapped_spec_owners",
            )
        )

    for anti_goal in anti_goals["anti_goals"]:
        anti_goal_id = anti_goal["id"]
        rows.append(
            blank_row(
                inventory_id=anti_goal_id,
                authority_type="BINDING_ANTI_GOAL",
                title=anti_goal["title"],
                normative_text=anti_goal["prohibition"],
                acceptance_or_enforcement="Architecture and readiness validation must fail when this prohibition is violated.",
                release_scope="CROSS_CUTTING",
                planning_disposition="BINDING_PROHIBITION",
                feature_or_domain="PRODUCT_BOUNDARY",
                primary_specs=joined(ANTI_GOAL_SPEC_MAP[anti_goal_id]),
                decision_refs="D033",
                verification_refs="anti-goal;boundary;negative;readiness",
                source_evidence="governance/ARCHITECTURAL_PROHIBITIONS.json;prd/09-non-goals-anti-goals.md",
                repository_coverage_basis="Binding product prohibition mapped to preservation and subsystem specifications.",
                planning_owner="product_constitution",
            )
        )

    rows.sort(key=lambda row: row["inventory_id"])
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    current_by_id = {row["inventory_id"]: row for row in rows}
    changed_records = []
    for inventory_id in sorted(set(previous_by_id) | set(current_by_id)):
        before = previous_by_id.get(inventory_id)
        after = current_by_id.get(inventory_id)
        if before == after:
            continue
        changed_fields = [column for column in COLUMNS if (before or {}).get(column, "") != (after or {}).get(column, "")]
        changed_records.append({
            "inventory_id": inventory_id,
            "change_kind": "ADDED" if before is None else "REMOVED" if after is None else "UPDATED",
            "changed_fields": ";".join(changed_fields),
            "previous_normative_text": (before or {}).get("normative_text", ""),
            "current_normative_text": (after or {}).get("normative_text", ""),
            "previous_active_blockers": (before or {}).get("active_blockers", ""),
            "current_active_blockers": (after or {}).get("active_blockers", ""),
            "previous_primary_specs": (before or {}).get("primary_specs", ""),
            "current_primary_specs": (after or {}).get("primary_specs", ""),
        })
    with CHANGED_CSV.open("w", newline="", encoding="utf-8") as handle:
        fields = list(changed_records[0])
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(changed_records)

    if previous_rows and not PRESERVATION_RECEIPT.exists():
        changed_original_rows = {item["inventory_id"]: previous_by_id[item["inventory_id"]] for item in changed_records if item["inventory_id"] in previous_by_id}
        receipt = {
            "schema_version": "cmf-builder-planning-v1-1-preservation/v1",
            "captured_on": "2026-07-14",
            "original_inventory_sha256": hashlib.sha256(previous_bytes).hexdigest(),
            "original_inventory_rows": len(previous_rows),
            "original_inventory_ids": sorted(previous_by_id),
            "original_row_hashes": {inventory_id: hashlib.sha256(json.dumps(previous_by_id[inventory_id], sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest() for inventory_id in sorted(previous_by_id)},
            "changed_original_rows": changed_original_rows,
            "reconstruction_rule": "Use changed_original_rows for updated rows and the V1.2 inventory for all unchanged original IDs.",
        }
        PRESERVATION_RECEIPT.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    preservation_metadata = (
        json.loads(PRESERVATION_RECEIPT.read_text(encoding="utf-8"))
        if PRESERVATION_RECEIPT.is_file()
        else {}
    )
    v1_1_row_count = preservation_metadata.get("original_inventory_rows", len(previous_rows))
    v1_1_inventory_hash = preservation_metadata.get(
        "original_inventory_sha256",
        hashlib.sha256(previous_bytes).hexdigest() if previous_bytes else "not-captured",
    )

    type_counts = Counter(row["authority_type"] for row in rows)
    verdict_counts = Counter(row["coverage_verdict"] for row in rows if row["coverage_verdict"])
    active_counts = Counter(
        blocker
        for row in rows
        for blocker in refs(row["active_blockers"])
    )
    baseline_status = "CONFIRMED" if inventory_confirmed else "COMPLETE_PENDING_HUMAN_CONFIRMATION"
    epic_design_gate = (
        "SATISFIED_STEP_2_AUTHORIZED"
        if epic_step_2_authorized
        else "BLOCKED_PENDING_EXPLICIT_EPIC_STEP_2_AUTHORIZATION"
        if inventory_confirmed
        else "BLOCKED_PENDING_HUMAN_CONFIRMATION"
    )
    confirmation_gate_text = (
        "Human product authority confirmed this inventory as the complete planning baseline on 2026-07-14. "
        "The receipt is `V1_2_INVENTORY_CONFIRMATION_RECEIPT.yaml`. Confirmation accepted coverage and extraction, "
        "not implementation readiness. Step 2 was subsequently authorized through "
        "`EPIC_STEP_2_AUTHORIZATION_RECEIPT.yaml` and completed as a proposed Epic design. Step 3 remains "
        "unauthorized, and the five external or empirical blockers remain open."
        if epic_step_2_authorized
        else
        "Human product authority confirmed this inventory as the complete planning baseline on 2026-07-14. "
        "The receipt is `V1_2_INVENTORY_CONFIRMATION_RECEIPT.yaml`. Confirmation accepts coverage and extraction, "
        "not implementation readiness, and does not authorize Epic Step 2. Epic design may begin only after "
        "separate explicit authorization. The five external or empirical blockers remain open."
        if inventory_confirmed
        else "Epic design may begin only after validation passes and human product authority confirms this inventory "
        "as the complete planning baseline. Confirmation accepts coverage and extraction, not implementation "
        "readiness. The five external or empirical blockers remain open."
    )
    baseline = f"""# Planning Requirements Extraction Baseline

Status: `{baseline_status}`

Extraction validation authority: `REQUIREMENTS_EXTRACTION_VALIDATION_REPORT.json`

Epic-design gate: `{epic_design_gate}`

## Scope

This is Step 1 of `handoff/EPICS_AND_STORIES_HANDOFF.md`. It normalizes every authoritative planning obligation before any epic or story is designed. It contains no production implementation and deliberately leaves `epic_ids` and `story_ids` empty.

## Inventory Counts

| Authority type | Count |
|---|---:|
| Functional requirements | {type_counts['FUNCTIONAL_REQUIREMENT']} |
| Non-functional requirements | {type_counts['NON_FUNCTIONAL_REQUIREMENT']} |
| Locked decisions | {type_counts['LOCKED_DECISION']} |
| Accepted ADR obligations | {type_counts['ARCHITECTURE_DECISION']} |
| Approved UX clauses | {type_counts['UX_CONTRACT_CLAUSE']} |
| Readiness hard gates | {type_counts['READINESS_HARD_GATE']} |
| Binding anti-goals | {type_counts['BINDING_ANTI_GOAL']} |
| Constitutional amendment obligations | {type_counts['CONSTITUTIONAL_AMENDMENT']} |
| **Total** | **{len(rows)}** |

## FR/NFR Coverage Verdicts

| Verdict | Count |
|---|---:|
""" + "\n".join(f"| `{name}` | {count} |" for name, count in sorted(verdict_counts.items())) + """

The verdicts are copied from `docs/tech-specs/REQUIREMENT_COVERAGE_MATRIX.csv`; this extraction does not reclassify requirements.

## Active Blocker Exposure

""" + ("\n".join(f"- `{name}` affects {count} inventory rows." for name, count in sorted(active_counts.items())) or "- No active blockers are referenced.") + """

Resolved blocker IDs remain in `blocking_decisions` for provenance. Only currently unresolved external or empirical blockers appear in `active_blockers`.

## Normalized Schema

Each inventory row includes full normative text, enforcement or acceptance evidence, release scope, the existing coverage verdict where applicable, planning disposition, feature/domain, specs and architecture owners, requirement/ADR/decision/UX links, verification strategy, concrete source evidence, repository coverage basis, blocker provenance, active blockers, and future Epic/Story assignment fields.

## Source Authority

- `governance/REQUIREMENTS_REGISTRY.json`
- `governance/DECISION_REGISTER.json`
- `governance/ARCHITECTURAL_PROHIBITIONS.json`
- `governance/READINESS_HARD_GATES.yaml`
- `sources/CCP_ACTIVATIVE_INTELLIGENCE_VISUAL_NARRATIVE_CONSTITUTION_V1_1.md`
- `docs/product-authority/BUILDER_V1_2_CONSTITUTIONAL_ALIGNMENT_AMENDMENT.md`
- `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`
- `docs/contracts/CONTRACT_REGISTRY.yaml`
- `docs/tech-specs/REQUIREMENT_COVERAGE_MATRIX.csv`
- `docs/architecture/ARCHITECTURE_TRACEABILITY_MATRIX.csv`
- `docs/architecture/ADR_REGISTER.yaml` and individual ADRs
- `docs/ux/HARNESS_CONTROL_TOWER_UX_CONTRACT.md`
- `docs/ux/CONTROL_TOWER_UX_TRACEABILITY_MATRIX.csv`

## Confirmation Gate

{confirmation_gate_text}
"""
    BASELINE.write_text(baseline, encoding="utf-8")

    changed_by_kind = Counter(item["change_kind"] for item in changed_records)
    changed_md = f"""# Builder V1.2 Changed-Obligation Report

Status: `COMPLETE`

- Original V1.1 inventory: {v1_1_row_count} rows, SHA-256 `{v1_1_inventory_hash}`.
- Revised V1.2 inventory: {len(rows)} rows.
- Added rows: {changed_by_kind.get('ADDED', 0)}.
- Updated existing rows: {changed_by_kind.get('UPDATED', 0)}.
- Removed rows: {changed_by_kind.get('REMOVED', 0)}.
- Every original inventory ID is retained: `{set(previous_by_id) <= set(current_by_id)}`.
- Epic assignments: 0. Story assignments: 0.

The nine planned additions are `CONST-001` through `CONST-008` and `HG-015`. Stable requirement IDs FR-137, FR-139, FR-145, FR-146, FR-147, and FR-169 are updated in place. D031 remains historical evidence with explicit V1.2 current effect; AG-004 applies to all five categories. Six accepted ADR rows acquire their additive alignment enforcement while all 18 ADR decisions remain accepted.

The complete field-level report is `V1_2_CHANGED_OBLIGATIONS.csv`. The original 401-row baseline hash, all original row hashes, and the complete prior payload of every changed original row are preserved in `V1_1_BASELINE_PRESERVATION_RECEIPT.json`.
"""
    CHANGED_MD.write_text(changed_md, encoding="utf-8")

    confirmation_status = "CONFIRMED" if inventory_confirmed else "AWAITING_HUMAN_CONFIRMATION"
    confirmation_heading = "Confirmation recorded" if inventory_confirmed else "Confirmation requested"
    confirmation_intro = (
        f"Human product authority confirmed the revised **{len(rows)}-row** Builder V1.2 planning inventory as the complete baseline for outcome-centered Epic design on 2026-07-14 with the exact response **CONFIRM V1.2 INVENTORY**."
        if inventory_confirmed
        else f"Please confirm that the revised **{len(rows)}-row** Builder V1.2 planning inventory is the complete baseline for outcome-centered Epic design."
    )
    confirmation_record = (
        "The machine-readable confirmation evidence is `V1_2_INVENTORY_CONFIRMATION_RECEIPT.yaml`. Inventory "
        "confirmation alone did not authorize Epic Step 2; subsequent bounded authorization is recorded separately "
        "in `EPIC_STEP_2_AUTHORIZATION_RECEIPT.yaml`."
        if epic_step_2_authorized
        else "The machine-readable confirmation evidence is `V1_2_INVENTORY_CONFIRMATION_RECEIPT.yaml`. Epic Step 2 remains not authorized."
        if inventory_confirmed
        else ""
    )
    confirmation_response = (
        "Recorded human response: **CONFIRM V1.2 INVENTORY**."
        if inventory_confirmed
        else "Requested human response: **CONFIRM V1.2 INVENTORY** or provide exact corrections by inventory ID."
    )
    confirmation = f"""# Builder V1.2 Inventory Human-Confirmation Package

Status: `{confirmation_status}`

## {confirmation_heading}

{confirmation_intro}

Confirmation means:

- all {v1_1_row_count} V1.1 planning obligations remain represented;
- eight standalone constitutional amendment obligations and HG-015 are added;
- changed stable requirements and affected decisions/ADRs/anti-goals are updated in place;
- all Epic and Story assignments remain empty;
- BD-004, BD-007, BD-008, BD-010, and BD-014 remain open;
- implementation readiness remains `FAIL`;
- the Visual Asset Editor and Delegation Protocol are not implemented here.

Confirmation does **not** authorize Epic Step 2 automatically, production implementation, conversational certification, the Visual Asset Editor runtime, or the Delegation Protocol runtime. Outcome-centered Epic design may begin only after an explicit confirmation and subsequent authorization.

{confirmation_record}

## Evidence to review

1. `PLANNING_REQUIREMENTS_INVENTORY.csv`
2. `V1_2_CHANGED_OBLIGATIONS.md` and `.csv`
3. `REQUIREMENTS_EXTRACTION_VALIDATION_REPORT.json`
4. `V1_1_BASELINE_PRESERVATION_RECEIPT.json`
5. `docs/constitutional-alignment/VALIDATION_REPORT.md`

{confirmation_response}
"""
    CONFIRMATION.write_text(confirmation, encoding="utf-8")


if __name__ == "__main__":
    main()
