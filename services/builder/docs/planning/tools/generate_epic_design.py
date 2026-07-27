from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
PLANNING = ROOT / "docs" / "planning"
INVENTORY = PLANNING / "PLANNING_REQUIREMENTS_INVENTORY.csv"
EPIC_SOURCE = PLANNING / "EPIC_INVENTORY.yaml"
COVERAGE = PLANNING / "EPIC_REQUIREMENT_COVERAGE.csv"
PROPOSAL = PLANNING / "EPIC_DESIGN_PROPOSAL.md"

COVERAGE_COLUMNS = [
    "inventory_id",
    "authority_type",
    "title",
    "primary_epic_id",
    "primary_epic_title",
    "secondary_epic_ids",
    "source_release_scope",
    "epic_release_disposition",
    "active_blockers",
    "carried_gate_refs",
    "assignment_basis",
]

FEATURE_EPIC = {
    "F01": "EP-01",
    "F02": "EP-01",
    "F03": "EP-02",
    "F04": "EP-02",
    "F05": "EP-03",
    "F06": "EP-03",
    "F07": "EP-04",
    "F08": "EP-04",
    "F09": "EP-05",
    "F10": "EP-05",
    "F11": "EP-08",
    "F12": "EP-10",
    "F13": "EP-08",
    "F14": "EP-06",
    "F15": "EP-11",
    "F16": "EP-12",
    "F17": "EP-07",
    "F18": "EP-09",
}

SPEC_EPIC = {
    "TS-01": "EP-01",
    "TS-02": "EP-01",
    "TS-03": "EP-02",
    "TS-04": "EP-02",
    "TS-05": "EP-03",
    "TS-06": "EP-03",
    "TS-07": "EP-04",
    "TS-08": "EP-05",
    "TS-09": "EP-05",
    "TS-10": "EP-08",
    "TS-11": "EP-06",
    "TS-12": "EP-10",
    "TS-13": "EP-08",
    "TS-14": "EP-09",
    "TS-15": "EP-12",
    "IMPLEMENTATION_BASELINE": "EP-12",
}

DECISION_EPIC = {
    "D001": "EP-01", "D002": "EP-03", "D003": "EP-12", "D004": "EP-07",
    "D005": "EP-01", "D006": "EP-01", "D007": "EP-02", "D008": "EP-02",
    "D009": "EP-03", "D010": "EP-03", "D011": "EP-03", "D012": "EP-04",
    "D013": "EP-04", "D014": "EP-04", "D015": "EP-04", "D016": "EP-04",
    "D017": "EP-05", "D018": "EP-05", "D019": "EP-05", "D020": "EP-04",
    "D021": "EP-05", "D022": "EP-08", "D023": "EP-08", "D024": "EP-08",
    "D025": "EP-10", "D026": "EP-08", "D027": "EP-08", "D028": "EP-12",
    "D029": "EP-11", "D030": "EP-06", "D031": "EP-06", "D032": "EP-12",
    "D033": "EP-08",
}

ADR_EPIC = {
    "ADR-001": "EP-01", "ADR-002": "EP-03", "ADR-003": "EP-10",
    "ADR-004": "EP-03", "ADR-005": "EP-03", "ADR-006": "EP-09",
    "ADR-007": "EP-01", "ADR-008": "EP-02", "ADR-009": "EP-05",
    "ADR-010": "EP-08", "ADR-011": "EP-10", "ADR-012": "EP-09",
    "ADR-013": "EP-07", "ADR-014": "EP-12", "ADR-015": "EP-12",
    "ADR-016": "EP-09", "ADR-017": "EP-09", "ADR-018": "EP-07",
}

HARD_GATE_EPIC = {
    "HG-001": "EP-03", "HG-002": "EP-01", "HG-003": "EP-02",
    "HG-004": "EP-04", "HG-005": "EP-04", "HG-006": "EP-05",
    "HG-007": "EP-04", "HG-008": "EP-08", "HG-009": "EP-08",
    "HG-010": "EP-08", "HG-011": "EP-09", "HG-012": "EP-09",
    "HG-013": "EP-09", "HG-014": "EP-09", "HG-015": "EP-06",
}

ANTI_GOAL_EPIC = {
    "AG-001": "EP-01", "AG-002": "EP-01", "AG-003": "EP-06",
    "AG-004": "EP-06", "AG-005": "EP-06", "AG-006": "EP-02",
    "AG-007": "EP-02", "AG-008": "EP-05", "AG-009": "EP-05",
    "AG-010": "EP-05", "AG-011": "EP-09", "AG-012": "EP-04",
    "AG-013": "EP-04", "AG-014": "EP-08", "AG-015": "EP-08",
    "AG-016": "EP-10", "AG-017": "EP-12", "AG-018": "EP-03",
    "AG-019": "EP-09", "AG-020": "EP-09", "AG-021": "EP-09",
    "AG-022": "EP-08",
}

CONSTITUTION_EPIC = {
    "CONST-001": "EP-03",
    "CONST-002": "EP-06",
    "CONST-003": "EP-06",
    "CONST-004": "EP-06",
    "CONST-005": "EP-07",
    "CONST-006": "EP-06",
    "CONST-007": "EP-08",
    "CONST-008": "EP-08",
}

EXPLICIT_MAPS = {
    "LOCKED_DECISION": DECISION_EPIC,
    "ARCHITECTURE_DECISION": ADR_EPIC,
    "READINESS_HARD_GATE": HARD_GATE_EPIC,
    "BINDING_ANTI_GOAL": ANTI_GOAL_EPIC,
    "CONSTITUTIONAL_AMENDMENT": CONSTITUTION_EPIC,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def refs(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(";") if item.strip()]


def assign_primary(row: dict[str, str]) -> tuple[str, str]:
    authority_type = row["authority_type"]
    inventory_id = row["inventory_id"]
    if authority_type == "FUNCTIONAL_REQUIREMENT":
        feature = row["feature_or_domain"]
        return FEATURE_EPIC[feature], f"feature outcome {feature}"
    if authority_type == "NON_FUNCTIONAL_REQUIREMENT":
        candidates = {SPEC_EPIC[spec] for spec in refs(row["primary_specs"]) if spec in SPEC_EPIC}
        if len(candidates) != 1:
            raise ValueError(f"{inventory_id}: NFR primary spec does not resolve to one Epic: {sorted(candidates)}")
        epic_id = next(iter(candidates))
        return epic_id, f"primary specification {row['primary_specs']}"
    if authority_type == "UX_CONTRACT_CLAUSE":
        return "EP-10", "approved Control Tower user outcome"
    mapping = EXPLICIT_MAPS.get(authority_type)
    if mapping is None or inventory_id not in mapping:
        raise ValueError(f"{inventory_id}: no primary Epic mapping for {authority_type}")
    return mapping[inventory_id], f"explicit {authority_type.lower().replace('_', ' ')} ownership"


def secondary_epics(row: dict[str, str], primary_epic: str, epic_order: dict[str, int]) -> list[str]:
    secondary = {
        SPEC_EPIC[spec]
        for spec in refs(row.get("primary_specs"))
        if spec in SPEC_EPIC and SPEC_EPIC[spec] != primary_epic
    }
    if row.get("active_blockers") and primary_epic != "EP-08":
        secondary.add("EP-08")
    return sorted(secondary, key=epic_order.__getitem__)


def bullet_lines(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def main() -> None:
    rows = read_csv(INVENTORY)
    epic_doc = yaml.safe_load(EPIC_SOURCE.read_text(encoding="utf-8"))
    epics = epic_doc["epics"]
    epic_by_id = {epic["id"]: epic for epic in epics}
    epic_order = {epic["id"]: epic["order"] for epic in epics}
    xdep_by_id = {item["id"]: item for item in epic_doc["cross_repository_dependencies"]}

    coverage_rows: list[dict[str, str]] = []
    primary_ids_by_epic: dict[str, list[str]] = defaultdict(list)
    primary_type_counts: dict[str, Counter[str]] = defaultdict(Counter)

    for row in rows:
        primary_epic, basis = assign_primary(row)
        epic = epic_by_id[primary_epic]
        secondary = secondary_epics(row, primary_epic, epic_order)
        carried_gates = sorted(
            set(refs(row.get("active_blockers"))) | set(epic["decision_and_blocker_obligations"])
        )
        coverage_rows.append({
            "inventory_id": row["inventory_id"],
            "authority_type": row["authority_type"],
            "title": row["title"],
            "primary_epic_id": primary_epic,
            "primary_epic_title": epic["title"],
            "secondary_epic_ids": ";".join(secondary),
            "source_release_scope": row["release_scope"],
            "epic_release_disposition": epic["release_1_disposition"],
            "active_blockers": row["active_blockers"],
            "carried_gate_refs": ";".join(carried_gates),
            "assignment_basis": basis,
        })
        primary_ids_by_epic[primary_epic].append(row["inventory_id"])
        primary_type_counts[primary_epic][row["authority_type"]] += 1

    with COVERAGE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COVERAGE_COLUMNS)
        writer.writeheader()
        writer.writerows(coverage_rows)

    sections: list[str] = []
    for epic in epics:
        epic_id = epic["id"]
        xdeps = [xdep_by_id[item] for item in epic["cross_repository_dependencies"]]
        covered_by_type: dict[str, list[str]] = defaultdict(list)
        for coverage_row in coverage_rows:
            if coverage_row["primary_epic_id"] == epic_id:
                covered_by_type[coverage_row["authority_type"]].append(coverage_row["inventory_id"])
        coverage_lines = []
        for authority_type, ids in sorted(covered_by_type.items()):
            coverage_lines.append(f"- `{authority_type}` ({len(ids)}): " + ", ".join(f"`{item}`" for item in ids))
        xdep_lines = [
            f"- `{item['id']}` — **{item['repository_or_product']}**: {item['relationship']} Constraint: {item['current_constraint']}"
            for item in xdeps
        ]
        sections.append(f"""## {epic_id} — {epic['title']}

**Outcome:** {epic['outcome']}

**Primary actor:** {epic['primary_actor']}

**Release 1 disposition:** `{epic['release_1_disposition']}`

**Depends on:** {', '.join(f'`{item}`' for item in epic['dependencies']) if epic['dependencies'] else 'None'}

**Decision and blocker obligations:** {', '.join(f'`{item}`' for item in epic['decision_and_blocker_obligations'])}

**Primary coverage ({len(primary_ids_by_epic[epic_id])} obligations):**

{chr(10).join(coverage_lines)}

**Cross-repository dependencies:**

{chr(10).join(xdep_lines)}

**Included outcome boundary:**

{bullet_lines(epic['scope_in'])}

**Excluded boundary:**

{bullet_lines(epic['scope_out'])}

**Completion evidence:** {epic['completion_evidence']}

**Blocked outcomes and risk:** {epic['blocked_outcomes']}
""")

    overview_rows = []
    for epic in epics:
        overview_rows.append(
            f"| {epic['id']} | {epic['title']} | {len(primary_ids_by_epic[epic['id']])} | "
            f"{', '.join(epic['dependencies']) or 'None'} | `{epic['release_1_disposition']}` |"
        )

    gate_usage: dict[str, list[str]] = defaultdict(list)
    for epic in epics:
        for gate in epic["decision_and_blocker_obligations"]:
            gate_usage[gate].append(epic["id"])
    gate_rows = [
        f"| `{gate}` | {', '.join(epic_ids)} | OPEN — planning may continue; affected implementation or certification outcomes remain blocked |"
        for gate, epic_ids in sorted(gate_usage.items())
    ]

    category_rows = [
        f"| `{item['category_id']}` | {item['canonical_name']} | EP-06 |"
        for item in epic_doc["canonical_categories"]
    ]
    target_rows = [
        f"| `{item['target_id']}` | {item['canonical_name']} | EP-07 |"
        for item in epic_doc["compilation_targets"]
    ]
    profile_rows = [
        f"| `{item['profile_id']}` | `{item['boundary']}` | EP-06 |"
        for item in epic_doc["conversational_profiles"]
    ]

    proposal = f"""# Builder V1.2 Outcome-Centered Epic Design Proposal

Status: `PROPOSED_AWAITING_HUMAN_CONFIRMATION`

Step: `2 — Outcome-centered Epic design`

Authority: Builder PRD V1.2 under Activative Intelligence Constitution V1.1.

Confirmed planning baseline: 410 obligations, SHA-256 `d3db32a78f4acce25e5448ff7c6ecb765ba814c0bdbf1bb44d6b49de00c55923`.

This proposal assigns every confirmed obligation exactly once as a primary Epic responsibility in `EPIC_REQUIREMENT_COVERAGE.csv`. Secondary traceability is non-owning. The confirmed baseline CSV is not mutated. No vertical Stories or production implementation are included.

Planning may continue. Implementation remains prohibited while readiness is `FAIL`.

## Proposed Epic inventory

| Epic | Outcome-centered title | Primary obligations | Dependencies | Release 1 disposition |
| --- | --- | ---: | --- | --- |
{chr(10).join(overview_rows)}

## Canonical category preservation

| Category ID | Canonical category | Primary Epic |
| --- | --- | --- |
{chr(10).join(category_rows)}

## Conversational profile boundary

| Profile ID | Builder boundary | Primary Epic |
| --- | --- | --- |
{chr(10).join(profile_rows)}

`reelcast_expression` and `interview_expression` are structurally compiled, validated, and handed off by Builder. Their live execution and final product PRDs remain outside this repository.

## Compilation target preservation

| Target ID | Compilation target | Primary Epic |
| --- | --- | --- |
{chr(10).join(target_rows)}

## Dependency ordering

The Epic IDs are a topological execution proposal: every dependency has a lower order number. This does not require horizontal implementation. Each Epic must deliver its stated end-to-end actor or system outcome, and Release 1 must demonstrate a complete Format 02 path through the needed portions of the sequence.

## Unresolved decisions, blockers, and gates

| Gate | Carried by | Effect |
| --- | --- | --- |
{chr(10).join(gate_rows)}

## Exact Epic proposals and primary requirement coverage

{chr(10).join(sections)}

## Step boundary

- Epic proposal status: `AWAITING_HUMAN_CONFIRMATION`.
- Vertical Story authoring: `NOT_AUTHORIZED`.
- Production implementation: `PROHIBITED_READINESS_FAIL`.
- Visual Asset Editor and Delegation Protocol implementation: outside Builder ownership.
- Next action: human confirms or corrects the Epic inventory and primary coverage before Step 3 begins.
"""
    PROPOSAL.write_text(proposal, encoding="utf-8")


if __name__ == "__main__":
    main()
