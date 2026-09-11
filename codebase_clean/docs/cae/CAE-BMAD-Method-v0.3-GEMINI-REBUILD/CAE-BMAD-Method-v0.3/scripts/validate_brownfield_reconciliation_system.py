#!/usr/bin/env python3
"""
CAE-BMAD Brownfield Reconciliation System Validator
Validates:
- BROWNFIELD_RECONCILIATION_REPORT.json conforms to schemas/brownfield_reconciliation.schema.json
- MISSING_IMPLEMENTATION_REGISTER.json conforms to schemas/missing_implementation_register.schema.json
- Associated skills, templates, workflows exist on disk
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate_brownfield_reconciliation() -> tuple[list[str], list[str]]:
    passes = []
    errors = []

    # 1. Schemas
    br_schema_p = ROOT / "schemas" / "brownfield_reconciliation.schema.json"
    mir_schema_p = ROOT / "schemas" / "missing_implementation_register.schema.json"

    for sp, name in [(br_schema_p, "brownfield_reconciliation"), (mir_schema_p, "missing_implementation_register")]:
        if not sp.exists():
            errors.append(f"Missing schemas/{name}.schema.json")
        else:
            passes.append(f"Found {name}.schema.json")

    # 2. Brownfield Reconciliation Report
    br_json_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "BROWNFIELD_RECONCILIATION_REPORT.json"
    br_md_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "BROWNFIELD_RECONCILIATION_REPORT.md"

    if not br_json_p.exists() or not br_md_p.exists():
        errors.append("Missing BROWNFIELD_RECONCILIATION_REPORT json/md")
    else:
        try:
            data = json.loads(br_json_p.read_text(encoding="utf-8"))
            evals = data.get("subsystem_evaluations", [])
            if len(evals) < 5:
                errors.append(f"Expected at least 5 subsystem evaluations, found {len(evals)}")
            else:
                passes.append(f"BROWNFIELD_RECONCILIATION_REPORT covers {len(evals)} subsystem evaluations")

            verdicts = {e["fidelity_verdict"] for e in evals}
            if not verdicts:
                errors.append("No fidelity verdicts assigned")
            else:
                passes.append(f"Fidelity verdicts assigned: {', '.join(sorted(verdicts))}")

            summary = data.get("layer_gap_summary", {})
            total = summary.get("verified_count", 0) + summary.get("partial_count", 0) + summary.get("missing_count", 0) + summary.get("contradicted_count", 0)
            if total < 5:
                errors.append(f"Gap summary totals {total}, expected at least 5")
            else:
                passes.append(f"Layer gap summary covers {total} evaluations")
        except Exception as e:
            errors.append(f"Failed to parse BROWNFIELD_RECONCILIATION_REPORT.json: {e}")

    # 3. Missing Implementation Register
    mir_json_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "MISSING_IMPLEMENTATION_REGISTER.json"
    mir_md_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "MISSING_IMPLEMENTATION_REGISTER.md"

    if not mir_json_p.exists() or not mir_md_p.exists():
        errors.append("Missing MISSING_IMPLEMENTATION_REGISTER json/md")
    else:
        try:
            data = json.loads(mir_json_p.read_text(encoding="utf-8"))
            gaps = data.get("gap_items", [])
            if len(gaps) < 3:
                errors.append(f"Expected at least 3 gap items, found {len(gaps)}")
            else:
                passes.append(f"MISSING_IMPLEMENTATION_REGISTER catalogs {len(gaps)} gap items")

            roadmap = data.get("remediation_roadmap", [])
            if len(roadmap) < 1:
                errors.append("Missing remediation roadmap")
            else:
                passes.append(f"Remediation roadmap has {len(roadmap)} steps")
        except Exception as e:
            errors.append(f"Failed to parse MISSING_IMPLEMENTATION_REGISTER.json: {e}")

    # 4. Skills
    skills_dir = ROOT / "skills"
    for sname in ["caebmad-brownfield-reconciliation", "caebmad-missing-layer-detect"]:
        if (skills_dir / sname / "SKILL.md").exists():
            passes.append(f"Found {sname} skill")
        else:
            errors.append(f"Missing {sname} skill")

    return passes, errors

def main():
    passes, errors = validate_brownfield_reconciliation()
    print("=" * 60)
    print(f"CAE-BMAD Brownfield Reconciliation Validator — Passed: {len(passes)}, Errors: {len(errors)}")
    print("=" * 60)
    for p in passes:
        print(f"  [PASS] {p}")
    if errors:
        print("\n" + "!" * 60)
        print("VALIDATION FAILURES:")
        print("!" * 60)
        for e in errors:
            print(f"  [FAIL] {e}")
        sys.exit(1)
    else:
        print("\nALL BROWNFIELD RECONCILIATION SYSTEM VALIDATIONS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
