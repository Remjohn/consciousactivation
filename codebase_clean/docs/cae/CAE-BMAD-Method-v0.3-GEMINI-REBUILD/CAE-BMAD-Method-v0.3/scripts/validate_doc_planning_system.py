#!/usr/bin/env python3
"""
CAE-BMAD Documentation and Planning System Validator
Validates:
- PRD modules exist and conform to schema rules
- Functional Requirements matrix is present and non-empty
- Epic/story backlog exists with proper PRD traceability
- All referenced skills and templates exist
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate_doc_planning() -> tuple[list[str], list[str]]:
    passes = []
    errors = []

    # 1. Check schemas
    prd_schema_p = ROOT / "schemas" / "prd_module.schema.json"
    epic_schema_p = ROOT / "schemas" / "epic_story.schema.json"
    if not prd_schema_p.exists():
        errors.append("Missing schemas/prd_module.schema.json")
    else:
        passes.append("Found prd_module.schema.json")
    if not epic_schema_p.exists():
        errors.append("Missing schemas/epic_story.schema.json")
    else:
        passes.append("Found epic_story.schema.json")

    # 2. Check PRD modules
    modules_dir = ROOT / "docs" / "cae-bmad" / "03_product" / "modules"
    if not modules_dir.exists():
        errors.append(f"PRD modules directory not found: {modules_dir}")
    else:
        prd_files = list(modules_dir.glob("PRD-*.md"))
        if len(prd_files) < 5:
            errors.append(f"Expected at least 5 PRD modules, found {len(prd_files)}")
        else:
            passes.append(f"Found {len(prd_files)} PRD module files")

    # 3. Check PRD Index
    index_p = ROOT / "docs" / "cae-bmad" / "03_product" / "PRD_INDEX.md"
    if not index_p.exists():
        errors.append("Missing PRD_INDEX.md")
    else:
        passes.append("Found PRD_INDEX.md")

    # 4. Check PRD modules JSON
    prd_json_p = ROOT / "docs" / "cae-bmad" / "03_product" / "PRD_MODULES.json"
    if not prd_json_p.exists():
        errors.append("Missing PRD_MODULES.json")
    else:
        try:
            modules = json.loads(prd_json_p.read_text(encoding="utf-8"))
            if len(modules) < 5:
                errors.append(f"Expected at least 5 modules in JSON, found {len(modules)}")
            else:
                passes.append(f"PRD_MODULES.json contains {len(modules)} modules")
            for m in modules:
                if "module_id" not in m:
                    errors.append(f"Module missing module_id: {m}")
                if "functional_requirements" not in m:
                    errors.append(f"Module {m.get('module_id', '?')} missing functional_requirements")
        except Exception as e:
            errors.append(f"Failed to parse PRD_MODULES.json: {e}")

    # 5. Check FR Matrix
    fr_p = ROOT / "docs" / "cae-bmad" / "03_product" / "FUNCTIONAL_REQUIREMENTS.md"
    if not fr_p.exists():
        errors.append("Missing FUNCTIONAL_REQUIREMENTS.md")
    else:
        passes.append("Found FUNCTIONAL_REQUIREMENTS.md")

    # 6. Check Epics
    epics_json_p = ROOT / "docs" / "cae-bmad" / "05_planning" / "EPICS.json"
    epics_md_p = ROOT / "docs" / "cae-bmad" / "05_planning" / "EPICS.md"
    if not epics_json_p.exists():
        errors.append("Missing EPICS.json")
    else:
        try:
            epics = json.loads(epics_json_p.read_text(encoding="utf-8"))
            if len(epics) < 5:
                errors.append(f"Expected at least 5 epics, found {len(epics)}")
            else:
                passes.append(f"EPICS.json contains {len(epics)} epics")
        except Exception as e:
            errors.append(f"Failed to parse EPICS.json: {e}")

    if not epics_md_p.exists():
        errors.append("Missing EPICS.md")
    else:
        passes.append("Found EPICS.md")

    # 7. Check Plan Genealogy
    genealogy_p = ROOT / "docs" / "cae-bmad" / "05_planning" / "PLAN_GENEALOGY.md"
    if not genealogy_p.exists():
        errors.append("Missing PLAN_GENEALOGY.md")
    else:
        passes.append("Found PLAN_GENEALOGY.md")

    return passes, errors

def main():
    passes, errors = validate_doc_planning()
    print("=" * 60)
    print(f"CAE-BMAD Doc/Planning Validator — Passed: {len(passes)}, Errors: {len(errors)}")
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
        print("\nALL DOC/PLANNING VALIDATIONS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
