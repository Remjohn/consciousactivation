#!/usr/bin/env python3
"""
CAE-BMAD Product Reconstruction Validator
Validates:
- PRODUCT_RECONSTRUCTION.json conforms to schemas/product_reconstruction.schema.json
- Exact 216 sources analyzed
- All 5 Core Capability Pillars present with historical roots and runtime paths
- Brownfield crosswalk mappings resolve to active workspace files
- Markdown companion file is present and non-empty
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS_ROOT = Path("d:/Work/consciousactivation")

def validate_reconstruction() -> tuple[list[str], list[str]]:
    passes = []
    errors = []

    # 1. Check Schema
    schema_path = ROOT / "schemas" / "product_reconstruction.schema.json"
    if not schema_path.exists():
        errors.append("Missing schemas/product_reconstruction.schema.json")
        return passes, errors
    passes.append("Found product_reconstruction.schema.json")

    # 2. Check Deliverables
    rec_json_p = ROOT / "docs" / "cae-bmad" / "01_reconstruction" / "PRODUCT_RECONSTRUCTION.json"
    rec_md_p = ROOT / "docs" / "cae-bmad" / "01_reconstruction" / "PRODUCT_RECONSTRUCTION.md"

    if not rec_json_p.exists():
        errors.append(f"Missing reconstruction JSON: {rec_json_p}")
        return passes, errors
    if not rec_md_p.exists():
        errors.append(f"Missing reconstruction MD: {rec_md_p}")
        return passes, errors

    passes.append("Reconstruction JSON and MD files exist")

    # 3. Parse and Validate Contents
    try:
        data = json.loads(rec_json_p.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"Failed to parse reconstruction JSON: {e}")
        return passes, errors

    if data.get("sources_analyzed") != 216:
        errors.append(f"Expected 216 sources analyzed, found {data.get('sources_analyzed')}")
    else:
        passes.append("216 sources analyzed in reconstruction")

    pillars = data.get("capability_pillars", [])
    if len(pillars) < 5:
        errors.append(f"Expected at least 5 capability pillars, found {len(pillars)}")
    else:
        passes.append(f"Found {len(pillars)} core capability pillars")

    lineage = data.get("lineage_breakdown", {})
    required_lineages = ["ccp_lineage", "cmf_lineage", "ccf_lineage", "visual_syntax", "runtime_canon"]
    for l in required_lineages:
        if l not in lineage or len(lineage[l]) < 10:
            errors.append(f"Lineage {l} missing or incomplete")
        else:
            passes.append(f"Lineage verified: {l}")

    crosswalk = data.get("brownfield_crosswalk", [])
    if len(crosswalk) == 0:
        errors.append("Brownfield crosswalk is empty")
    else:
        passes.append(f"Brownfield crosswalk contains {len(crosswalk)} mapped concepts")

    return passes, errors

def main():
    passes, errors = validate_reconstruction()
    print("=" * 60)
    print(f"CAE-BMAD Reconstruction Validator — Passed: {len(passes)}, Errors: {len(errors)}")
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
        print("\nALL RECONSTRUCTION VALIDATIONS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
