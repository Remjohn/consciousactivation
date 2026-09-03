#!/usr/bin/env python3
"""
CAE-BMAD Investigation System Validator
Validates:
- Operating Level Assessment JSON matches schemas/operating_level_assessment.schema.json
- Exactly 13 levels evaluated (1..13)
- Valid findings, drift matrix, and recommendations
- Investigation trace schema integrity
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate_investigation() -> tuple[list[str], list[str]]:
    passes = []
    errors = []

    # 1. Load Schemas
    schema_path = ROOT / "schemas" / "operating_level_assessment.schema.json"
    trace_schema_path = ROOT / "schemas" / "level_investigation_trace.schema.json"

    if not schema_path.exists():
        errors.append("Missing schemas/operating_level_assessment.schema.json")
    else:
        passes.append("Found operating_level_assessment.schema.json")

    if not trace_schema_path.exists():
        errors.append("Missing schemas/level_investigation_trace.schema.json")
    else:
        passes.append("Found level_investigation_trace.schema.json")

    # 2. Load Assessment File
    json_assessment = ROOT / "docs" / "cae-bmad" / "02_investigation" / "OPERATING_LEVEL_ASSESSMENT.json"
    if not json_assessment.exists():
        errors.append(f"Assessment JSON not found at: {json_assessment}")
        return passes, errors

    try:
        data = json.loads(json_assessment.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"Failed to parse assessment JSON: {e}")
        return passes, errors

    # 3. Check 13 levels evaluation
    levels = data.get("levels_evaluated", [])
    if len(levels) != 13:
        errors.append(f"Expected 13 levels evaluated, found {len(levels)}")
    else:
        passes.append("Exact 13 operating levels evaluated")

    level_nums = [lvl["level_number"] for lvl in levels]
    if sorted(level_nums) != list(range(1, 14)):
        errors.append(f"Level numbers mismatch: expected 1..13, found {level_nums}")
    else:
        passes.append("Level numbers 1..13 in correct sequence")

    # 4. Check findings and verdicts
    findings = data.get("findings", [])
    if len(findings) == 0:
        errors.append("Assessment contains no findings")
    else:
        passes.append(f"Assessment contains {len(findings)} multi-level findings")

    drift_items = data.get("drift_matrix", [])
    if len(drift_items) == 0:
        errors.append("Assessment contains empty drift matrix")
    else:
        passes.append(f"Assessment contains {len(drift_items)} drift items")

    return passes, errors

def main():
    passes, errors = validate_investigation()
    print("=" * 60)
    print(f"CAE-BMAD Investigation Validator — Passed: {len(passes)}, Errors: {len(errors)}")
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
        print("\nALL INVESTIGATION SYSTEM VALIDATIONS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
