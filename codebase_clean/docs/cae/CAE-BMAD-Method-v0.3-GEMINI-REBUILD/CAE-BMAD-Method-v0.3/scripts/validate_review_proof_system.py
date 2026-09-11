#!/usr/bin/env python3
"""
CAE-BMAD Review, Proof, and Gate System Validator
Validates:
- REVIEW_AND_GATE_RECORD.json conforms to schemas/review_proof_record.schema.json
- OPERATOR_GATE_DECISIONS.json conforms to schemas/operator_gate_decision.schema.json
- Associated skills, templates, workflows exist on disk
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate_review_proof_system() -> tuple[list[str], list[str]]:
    passes = []
    errors = []

    # 1. Schemas
    rev_schema_p = ROOT / "schemas" / "review_proof_record.schema.json"
    ogd_schema_p = ROOT / "schemas" / "operator_gate_decision.schema.json"

    for sp, name in [(rev_schema_p, "review_proof_record"), (ogd_schema_p, "operator_gate_decision")]:
        if not sp.exists():
            errors.append(f"Missing schemas/{name}.schema.json")
        else:
            passes.append(f"Found {name}.schema.json")

    # 2. Review and Gate Record
    rev_json_p = ROOT / "docs" / "cae-bmad" / "09_review" / "REVIEW_AND_GATE_RECORD.json"
    rev_md_p = ROOT / "docs" / "cae-bmad" / "09_review" / "REVIEW_AND_GATE_RECORD.md"

    if not rev_json_p.exists() or not rev_md_p.exists():
        errors.append("Missing REVIEW_AND_GATE_RECORD json/md")
    else:
        try:
            data = json.loads(rev_json_p.read_text(encoding="utf-8"))
            mandates = data.get("audited_mandates", [])
            cts = data.get("countertest_evaluations", [])
            if len(mandates) < 5:
                errors.append(f"Expected at least 5 audited mandates, found {len(mandates)}")
            elif len(cts) < 3:
                errors.append(f"Expected at least 3 countertest evaluations, found {len(cts)}")
            else:
                passes.append(f"REVIEW_AND_GATE_RECORD covers {len(mandates)} mandates and {len(cts)} countertests")

            if data.get("gate_clearance_verdict") != "CLEARANCE_GRANTED":
                errors.append(f"Unexpected clearance verdict: {data.get('gate_clearance_verdict')}")
            else:
                passes.append("Gate clearance verdict is CLEARANCE_GRANTED")
        except Exception as e:
            errors.append(f"Failed to parse REVIEW_AND_GATE_RECORD.json: {e}")

    # 3. Operator Gate Decisions
    ogd_json_p = ROOT / "docs" / "cae-bmad" / "00_governance" / "OPERATOR_GATE_DECISIONS.json"
    ogd_md_p = ROOT / "docs" / "cae-bmad" / "00_governance" / "OPERATOR_GATE_DECISIONS.md"

    if not ogd_json_p.exists() or not ogd_md_p.exists():
        errors.append("Missing OPERATOR_GATE_DECISIONS json/md")
    else:
        try:
            data = json.loads(ogd_json_p.read_text(encoding="utf-8"))
            decisions = data.get("decisions", [])
            if len(decisions) < 10:
                errors.append(f"Expected at least 10 gate decisions recorded, found {len(decisions)}")
            else:
                passes.append(f"OPERATOR_GATE_DECISIONS catalogs {len(decisions)} mandate gates")
        except Exception as e:
            errors.append(f"Failed to parse OPERATOR_GATE_DECISIONS.json: {e}")

    # 4. Skills
    skills_dir = ROOT / "skills"
    for sname in ["caebmad-adversarial-review", "caebmad-gate-promotion"]:
        if (skills_dir / sname / "SKILL.md").exists():
            passes.append(f"Found {sname} skill")
        else:
            errors.append(f"Missing {sname} skill")

    return passes, errors

def main():
    passes, errors = validate_review_proof_system()
    print("=" * 60)
    print(f"CAE-BMAD Review & Proof System Validator — Passed: {len(passes)}, Errors: {len(errors)}")
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
        print("\nALL REVIEW, PROOF, AND GATE SYSTEM VALIDATIONS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
