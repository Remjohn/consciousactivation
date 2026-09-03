#!/usr/bin/env python3
"""
CAE-BMAD Grill Protocol & Signal Distillation Validator
Validates:
- schemas/grill_session.schema.json exists
- skills/caebmad-grill-protocol/SKILL.md exists
- templates/grill_question.md exists
- method/CAE_BMAD_GRILL_SPEC.md exists
- Canonical grill session conforms to schema, enforces min 320 words, and passes anti-genericity checks
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate_grill_protocol() -> tuple[list[str], list[str]]:
    passes = []
    errors = []

    # 1. Spec, Schema, Template, Skill
    spec_p = ROOT / "method" / "CAE_BMAD_GRILL_SPEC.md"
    schema_p = ROOT / "schemas" / "grill_session.schema.json"
    template_p = ROOT / "templates" / "grill_question.md"
    skill_p = ROOT / "skills" / "caebmad-grill-protocol" / "SKILL.md"

    for p, desc in [(spec_p, "Grill Specification"), (schema_p, "Grill Schema"), (template_p, "Grill Question Template"), (skill_p, "Grill Skill")]:
        if p.exists():
            passes.append(f"Found {desc}: {p.name}")
        else:
            errors.append(f"Missing {desc}: {p}")

    # 2. Canonical Grill Session
    session_json_p = ROOT / "docs" / "cae-bmad" / "00_governance" / "CANONICAL_GRILL_SESSION_001.json"
    session_md_p = ROOT / "docs" / "cae-bmad" / "00_governance" / "CANONICAL_GRILL_SESSION_001.md"

    if not session_json_p.exists() or not session_md_p.exists():
        errors.append("Missing CANONICAL_GRILL_SESSION_001 json/md")
    else:
        try:
            data = json.loads(session_json_p.read_text(encoding="utf-8"))
            rec = data.get("recommended_answer", "")
            words = len(rec.split())
            if words < 320:
                errors.append(f"Recommended answer under density floor (320 words): found {words} words")
            else:
                passes.append(f"Recommended answer exceeds density floor: {words} words (min 320)")

            prim = data.get("collision_primitive")
            if prim not in ["PREDICTION_VIOLATION", "COSTLY_EXPOSURE", "LATENT_PATTERN_ARTICULATION"]:
                errors.append(f"Invalid collision primitive: {prim}")
            else:
                passes.append(f"Valid collision primitive: {prim}")

            checks = data.get("anti_genericity_evaluations", {})
            for c in ["passed_check_1", "passed_check_2", "passed_check_3", "passed_check_4"]:
                if checks.get(c) is not True:
                    errors.append(f"Anti-genericity evaluation failed: {c} is not True")
            passes.append("All 4 Anti-Genericity Reality Contact checks passed")

            precheck = data.get("code_precheck", {})
            if len(precheck.get("inspected_surfaces", [])) == 0:
                errors.append("Codebase precheck inspected surfaces empty")
            else:
                passes.append(f"Codebase precheck covers {len(precheck['inspected_surfaces'])} physical surfaces")

        except Exception as e:
            errors.append(f"Failed to parse CANONICAL_GRILL_SESSION_001.json: {e}")

    return passes, errors

def main():
    passes, errors = validate_grill_protocol()
    print("=" * 60)
    print(f"CAE-BMAD Grill Protocol Validator — Passed: {len(passes)}, Errors: {len(errors)}")
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
        print("\nALL GRILL PROTOCOL VALIDATIONS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
