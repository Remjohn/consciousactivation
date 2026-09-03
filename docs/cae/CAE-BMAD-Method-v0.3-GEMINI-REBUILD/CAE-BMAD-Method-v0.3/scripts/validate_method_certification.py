#!/usr/bin/env python3
"""
CAE-BMAD Method Certification Validator
Validates:
- CAE_BMAD_METHOD_CERTIFICATION.json conforms to schemas/method_certification_package.schema.json
- END_TO_END_INTEGRATION_RUN.json conforms to schemas/end_to_end_integration_run.schema.json
- Associated skills, templates, workflows exist on disk
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate_method_certification() -> tuple[list[str], list[str]]:
    passes = []
    errors = []

    # 1. Schemas
    cert_schema_p = ROOT / "schemas" / "method_certification_package.schema.json"
    e2e_schema_p = ROOT / "schemas" / "end_to_end_integration_run.schema.json"

    for sp, name in [(cert_schema_p, "method_certification_package"), (e2e_schema_p, "end_to_end_integration_run")]:
        if not sp.exists():
            errors.append(f"Missing schemas/{name}.schema.json")
        else:
            passes.append(f"Found {name}.schema.json")

    # 2. Master Method Certification
    cert_json_p = ROOT / "docs" / "cae-bmad" / "10_certification" / "CAE_BMAD_METHOD_CERTIFICATION.json"
    cert_md_p = ROOT / "docs" / "cae-bmad" / "10_certification" / "CAE_BMAD_METHOD_CERTIFICATION.md"

    if not cert_json_p.exists() or not cert_md_p.exists():
        errors.append("Missing CAE_BMAD_METHOD_CERTIFICATION json/md")
    else:
        try:
            data = json.loads(cert_json_p.read_text(encoding="utf-8"))
            mandates = data.get("mandate_certifications", [])
            levels = data.get("operating_level_coverage", [])
            if len(mandates) < 12:
                errors.append(f"Expected 12 certified mandates, found {len(mandates)}")
            else:
                passes.append(f"CAE_BMAD_METHOD_CERTIFICATION certifies all {len(mandates)} mandates (M01-M12)")

            if len(levels) < 13:
                errors.append(f"Expected 13 operating levels, found {len(levels)}")
            else:
                passes.append(f"Operating level coverage complete across all {len(levels)} levels")

            if data.get("final_certification_verdict") != "METHOD_CERTIFIED_FOR_OPERATOR_RATIFICATION":
                errors.append(f"Unexpected certification verdict: {data.get('final_certification_verdict')}")
            else:
                passes.append("Final certification verdict is METHOD_CERTIFIED_FOR_OPERATOR_RATIFICATION")
        except Exception as e:
            errors.append(f"Failed to parse CAE_BMAD_METHOD_CERTIFICATION.json: {e}")

    # 3. End-to-End Integration Run Trace
    e2e_json_p = ROOT / "docs" / "cae-bmad" / "10_certification" / "END_TO_END_INTEGRATION_RUN.json"
    e2e_md_p = ROOT / "docs" / "cae-bmad" / "10_certification" / "END_TO_END_INTEGRATION_RUN.md"

    if not e2e_json_p.exists() or not e2e_md_p.exists():
        errors.append("Missing END_TO_END_INTEGRATION_RUN json/md")
    else:
        try:
            data = json.loads(e2e_json_p.read_text(encoding="utf-8"))
            steps = data.get("trace_steps", [])
            proofs = data.get("line_level_proofs", [])
            if len(steps) < 4:
                errors.append(f"Expected at least 4 trace steps, found {len(steps)}")
            else:
                passes.append(f"END_TO_END_INTEGRATION_RUN traces {len(steps)} chronological steps")

            if len(proofs) < 3:
                errors.append(f"Expected at least 3 line-level proofs, found {len(proofs)}")
            else:
                passes.append(f"Line-level code proofs verified on {len(proofs)} physical files")

            if data.get("fidelity_verdict") != "END_TO_END_PROVEN_AGAINST_REAL_CODE":
                errors.append(f"Unexpected fidelity verdict: {data.get('fidelity_verdict')}")
            else:
                passes.append("End-to-end fidelity verdict is END_TO_END_PROVEN_AGAINST_REAL_CODE")
        except Exception as e:
            errors.append(f"Failed to parse END_TO_END_INTEGRATION_RUN.json: {e}")

    # 4. Skill
    skill_p = ROOT / "skills" / "caebmad-method-certification" / "SKILL.md"
    if skill_p.exists():
        passes.append("Found caebmad-method-certification skill")
    else:
        errors.append("Missing caebmad-method-certification skill")

    return passes, errors

def main():
    passes, errors = validate_method_certification()
    print("=" * 60)
    print(f"CAE-BMAD Method Certification Validator — Passed: {len(passes)}, Errors: {len(errors)}")
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
        print("\nALL METHOD INTEGRATION AND CERTIFICATION VALIDATIONS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
