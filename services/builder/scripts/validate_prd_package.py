from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "CMF_ATOMIC_HARNESS_BUILDER_NEXT_SHARDED_PRD_V1_2_ALIGNED"
MANIFEST_ROOTS = ["addendum", "governance", "handoff", "prd", "scripts", "sources", "templates", "validation", "docs/contracts", "docs/product-authority"]


def norm(value: str) -> str:
    return " ".join(str(value).split())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_state() -> dict:
    return {
        "requirements": yaml.safe_load((ROOT / "governance/REQUIREMENTS_REGISTRY.yaml").read_text(encoding="utf-8")),
        "decisions": json.loads((ROOT / "governance/DECISION_REGISTER.json").read_text(encoding="utf-8")),
        "categories": yaml.safe_load((ROOT / "governance/CANONICAL_CATEGORY_REGISTRY.yaml").read_text(encoding="utf-8")),
        "profiles": yaml.safe_load((ROOT / "governance/CONVERSATIONAL_PROFILE_REGISTRY.yaml").read_text(encoding="utf-8")),
        "targets": yaml.safe_load((ROOT / "governance/COMPILATION_TARGET_REGISTRY.yaml").read_text(encoding="utf-8")),
        "gates": yaml.safe_load((ROOT / "governance/READINESS_HARD_GATES.yaml").read_text(encoding="utf-8")),
        "sources": json.loads((ROOT / "governance/SOURCE_REGISTER.json").read_text(encoding="utf-8")),
        "contracts": yaml.safe_load((ROOT / "docs/contracts/CONTRACT_REGISTRY.yaml").read_text(encoding="utf-8")),
    }


def find_links() -> tuple[int, list[str]]:
    errors: list[str] = []
    checked = 0
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        for target in link_re.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            checked += 1
            if not (path.parent / target).resolve().exists():
                errors.append(f"broken_link:{path.relative_to(ROOT)}:{target}")
    return checked, errors


def validate(include_manifest: bool = True) -> tuple[list[str], dict]:
    errors: list[str] = []
    state = load_state()
    frs = state["requirements"]["functional_requirements"]
    nfrs = state["requirements"]["non_functional_requirements"]
    ids = [item["id"] for item in frs + nfrs]
    if len(ids) != len(set(ids)):
        errors.append("duplicate_requirement_ids")
    if len(frs) != 210 or len(nfrs) != 53:
        errors.append(f"requirement_counts:{len(frs)}:{len(nfrs)}")

    feature_files = sorted((ROOT / "prd/05-features").glob("F[0-9][0-9]-*.md"))
    if len(feature_files) != 18:
        errors.append(f"feature_count:{len(feature_files)}")
    parsed: dict[str, tuple[str, str]] = {}
    pattern = re.compile(r"^### (FR-[0-9]{3})\s+\S+\s+(.+?)\n\n\*\*Requirement:\*\*\s*(.+?)\n\n", re.MULTILINE | re.DOTALL)
    shard_order: list[str] = []
    for path in feature_files:
        text = path.read_text(encoding="utf-8")
        for requirement_id, title, requirement in pattern.findall(text):
            shard_order.append(requirement_id)
            parsed[requirement_id] = (norm(title), norm(requirement))
    expected_order = [item["id"] for item in frs]
    if shard_order != expected_order:
        errors.append("feature_shard_requirement_order_or_ids_mismatch")
    for item in frs:
        actual = parsed.get(item["id"])
        expected = (norm(item["title"]), norm(item["requirement"]))
        if actual != expected:
            errors.append(f"feature_registry_semantic_mismatch:{item['id']}")
        if not item.get("testable_consequences"):
            errors.append(f"missing_testable_consequences:{item['id']}")

    fr_by_id = {item["id"]: item for item in frs}
    required_terms = {
        "FR-137": ["Activative Intelligence Pack", "smallest useful commitment", "frozen Activative Intelligence"],
        "FR-139": ["five canonical categories", "Conversational Activation / Human Expression"],
        "FR-145": ["conversational", "Expression Moment"],
        "FR-146": ["turn", "silence"],
        "FR-147": ["participant roles", "smallest useful commitment"],
        "FR-169": ["all five category constitutions"],
    }
    for requirement_id, terms in required_terms.items():
        body = norm(fr_by_id[requirement_id]["title"] + " " + fr_by_id[requirement_id]["requirement"] + " " + " ".join(fr_by_id[requirement_id]["testable_consequences"]))
        for term in terms:
            if term not in body:
                errors.append(f"constitutional_term_missing:{requirement_id}:{term}")

    decision_ids = {item["id"] for item in state["decisions"]["decisions"]}
    if len(decision_ids) != 33:
        errors.append(f"decision_count:{len(decision_ids)}")
    covered = {decision for item in frs for decision in item.get("decisions", [])}
    for decision_id in sorted(decision_ids - covered):
        errors.append(f"decision_without_fr:{decision_id}")

    category_ids = [item["category_id"] for item in state["categories"]["categories"]]
    profile_ids = [item["profile_id"] for item in state["profiles"]["profiles"]]
    gate_ids = [item["id"] for item in state["gates"]["gates"]]
    source_ids = [item.get("source_id", item.get("id")) for item in state["sources"]["sources"]]
    if category_ids != ["short_form_edited_video", "2d_character_animation", "carousels", "supervisuals", "conversational_activation_expression"]:
        errors.append("canonical_category_registry_mismatch")
    if profile_ids != ["public_comment", "reply_dm", "reelcast_expression", "interview_expression"]:
        errors.append("conversational_profile_registry_mismatch")
    if len(state["targets"]["targets"]) != 3:
        errors.append("compilation_target_count_changed")
    if gate_ids != [f"HG-{number:03d}" for number in range(1, 16)]:
        errors.append("readiness_hard_gate_registry_mismatch")
    if "SRC-013-CONSTITUTION" not in source_ids:
        errors.append("constitution_source_not_registered")

    constitution = ROOT / "sources/CCP_ACTIVATIVE_INTELLIGENCE_VISUAL_NARRATIVE_CONSTITUTION_V1_1.md"
    if not constitution.exists() or sha(constitution) != "21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b":
        errors.append("constitution_source_hash_mismatch")
    contract_report = json.loads((ROOT / "docs/contracts/VALIDATION_REPORT.json").read_text(encoding="utf-8"))
    if contract_report.get("status") != "PASS":
        errors.append("contract_validation_not_pass")

    link_count, link_errors = find_links()
    errors.extend(link_errors)
    bad_tokens = ["{{", "TBD", "TODO", "[placeholder]"]
    for path in list((ROOT / "prd").rglob("*.md")) + list((ROOT / "governance").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for token in bad_tokens:
            if token in text:
                errors.append(f"placeholder:{path.relative_to(ROOT)}:{token}")

    if include_manifest:
        manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
        for item in manifest["files"]:
            path = ROOT / item["path"]
            if not path.exists():
                errors.append(f"manifest_missing:{item['path']}")
            elif sha(path) != item["sha256"]:
                errors.append(f"manifest_hash_mismatch:{item['path']}")

    stats = {
        "decisions": len(decision_ids),
        "features": len(feature_files),
        "functional_requirements": len(frs),
        "non_functional_requirements": len(nfrs),
        "user_journeys": len({journey for item in frs for journey in item.get("user_journeys", [])}),
        "canonical_categories": len(category_ids),
        "conversational_profiles": len(profile_ids),
        "compilation_targets": len(state["targets"]["targets"]),
        "readiness_hard_gates": len(gate_ids),
        "source_records": len(source_ids),
        "contracts": len(state["contracts"]["contracts"]),
        "relative_links_checked": link_count,
    }
    return errors, stats


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def refresh_derived(errors: list[str], stats: dict) -> None:
    state = load_state()
    frs = state["requirements"]["functional_requirements"]
    nfrs = state["requirements"]["non_functional_requirements"]
    (ROOT / "governance/REQUIREMENTS_REGISTRY.json").write_text(json.dumps(state["requirements"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    trace_rows = []
    for item in frs + nfrs:
        trace_rows.append({
            "requirement_id": item["id"],
            "type": "FR" if item["id"].startswith("FR-") else "NFR",
            "feature_id": item.get("feature_id", ""),
            "title": item["title"],
            "decisions": ";".join(item.get("decisions", [])),
            "user_journeys": ";".join(item.get("user_journeys", [])),
            "cross_cutting_nfrs": ";".join(item.get("cross_cutting_nfrs", [])),
            "source_file": item.get("source_file", ""),
        })
    write_csv(ROOT / "governance/TRACEABILITY_MATRIX.csv", list(trace_rows[0]), trace_rows)

    decision_to_frs: dict[str, list[str]] = defaultdict(list)
    for item in frs:
        for decision in item.get("decisions", []):
            decision_to_frs[decision].append(item["id"])
    decision_rows = [{"decision_id": decision, "functional_requirements": ";".join(decision_to_frs[decision]), "count": len(decision_to_frs[decision])} for decision in sorted(decision_to_frs)]
    write_csv(ROOT / "governance/DECISION_TO_REQUIREMENT_MAP.csv", ["decision_id", "functional_requirements", "count"], decision_rows)

    coverage_lines = ["# Requirements Coverage Map", "", "Current-effect note: D031 remains historical decision evidence; the V1.2 constitutional amendment expands its governed category effect from four to five.", "", "| Decision | Functional requirements | Count |", "| --- | --- | ---: |"]
    coverage_lines.extend(f"| {row['decision_id']} | {row['functional_requirements'].replace(';', ', ')} | {row['count']} |" for row in decision_rows)
    (ROOT / "governance/REQUIREMENTS_COVERAGE_MAP.md").write_text("\n".join(coverage_lines) + "\n", encoding="utf-8")

    status = "PASS" if not errors else "FAIL"
    local = {"package": PACKAGE_NAME, "status": status, "created": "2026-07-14", "counts": stats, "warnings": [], "constitutional_overlay": "docs/product-authority/BUILDER_V1_2_CONSTITUTIONAL_ALIGNMENT_AMENDMENT.md"}
    (ROOT / "LOCAL_VERIFICATION.json").write_text(json.dumps(local, indent=2) + "\n", encoding="utf-8")
    (ROOT / "validation/ID_COVERAGE_REPORT.json").write_text(json.dumps({"status": status, "counts": stats, "changed_stable_requirements": ["FR-137", "FR-139", "FR-145", "FR-146", "FR-147"], "constitutional_amendment_obligations": 8, "decision_coverage": {row["decision_id"]: row["count"] for row in decision_rows}}, indent=2) + "\n", encoding="utf-8")
    (ROOT / "validation/LINK_CHECK_REPORT.json").write_text(json.dumps({"status": status if not [item for item in errors if item.startswith('broken_link:')] else "FAIL", "relative_links_checked": stats["relative_links_checked"], "errors": [item for item in errors if item.startswith("broken_link:")]}, indent=2) + "\n", encoding="utf-8")
    (ROOT / "validation/SOURCE_INTEGRITY_REPORT.json").write_text(json.dumps({"status": "PASS" if "constitution_source_hash_mismatch" not in errors else "FAIL", "source_records": stats["source_records"], "constitution_sha256": "21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b"}, indent=2) + "\n", encoding="utf-8")
    (ROOT / "validation/EMBEDDED_VALIDATOR_RESULT.json").write_text(json.dumps({"status": status, "errors": errors}, indent=2) + "\n", encoding="utf-8")
    report = f"""---
title: PRD Package Validation Report
product: CMF Atomic Harness Builder Next
version: 1.2-aligned
status: {status}
updated: '2026-07-14'
---

# PRD Package Validation Report

**Result:** `{status}`

## Counts

| Item | Count |
| --- | ---: |
| Decisions | {stats['decisions']} |
| Features | {stats['features']} |
| Functional Requirements | {stats['functional_requirements']} |
| Non-Functional Requirements | {stats['non_functional_requirements']} |
| Canonical Categories | {stats['canonical_categories']} |
| Conversational Profiles | {stats['conversational_profiles']} |
| Compilation Targets | {stats['compilation_targets']} |
| Readiness Hard Gates | {stats['readiness_hard_gates']} |
| Source Records | {stats['source_records']} |
| Builder Contract Definitions | {stats['contracts']} |

## Constitutional checks

- Constitution source hash and precedence contract: {status}
- Five-category registry and four conversational profiles: {status}
- FR-137, FR-139, FR-145, FR-146, FR-147 and FR-169 semantic synchronization: {status}
- HG-015 and thirteen-source coverage: {status}
- Contract schemas and examples: {status}
- Three compilation targets preserved: {status}

This structural PASS does not authorize production implementation, conversational certification, the Visual Asset Editor runtime, or the Delegation Protocol runtime. HD-006 and HD-007 remain readiness blockers.
"""
    (ROOT / "validation/PRD_VALIDATION_REPORT.md").write_text(report, encoding="utf-8")

    files: list[Path] = [ROOT / "README.md", ROOT / "LOCAL_VERIFICATION.json"]
    for root_name in MANIFEST_ROOTS:
        base = ROOT / root_name
        if base.exists():
            files.extend(path for path in base.rglob("*") if path.is_file() and "__pycache__" not in path.parts)
    unique = sorted(set(files), key=lambda path: path.relative_to(ROOT).as_posix())
    manifest_files = [{"path": path.relative_to(ROOT).as_posix(), "size_bytes": path.stat().st_size, "sha256": sha(path)} for path in unique]
    manifest = {"package": PACKAGE_NAME, "product": "CMF Atomic Harness Builder Next", "version": "1.2-aligned", "status": status, "created": "2026-07-14", "file_count_excluding_manifest": len(manifest_files), "total_bytes_excluding_manifest": sum(item["size_bytes"] for item in manifest_files), "counts": stats, "files": manifest_files}
    (ROOT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-derived", action="store_true")
    args = parser.parse_args()
    if args.refresh_derived:
        pre_errors, pre_stats = validate(include_manifest=False)
        refresh_derived(pre_errors, pre_stats)
    errors, stats = validate(include_manifest=True)
    result = {"status": "PASS" if not errors else "FAIL", "counts": stats, "errors": errors}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
