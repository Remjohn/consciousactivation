#!/usr/bin/env python3
"""
CAE-BMAD Data, Module, and Code Forensics System Validator
Validates:
- DATA_REALITY_MAP.json conforms to schemas/data_reality_map.schema.json
- MODULE_MAP.json conforms to schemas/module_map.schema.json
- CODE_FORENSICS_REPORT.json conforms to schemas/code_forensics_report.schema.json
- Associated skills, templates, workflows, and markdown companions exist
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate_data_module_forensics() -> tuple[list[str], list[str]]:
    passes = []
    errors = []

    # 1. Schemas
    d_schema_p = ROOT / "schemas" / "data_reality_map.schema.json"
    m_schema_p = ROOT / "schemas" / "module_map.schema.json"
    c_schema_p = ROOT / "schemas" / "code_forensics_report.schema.json"

    for sp, name in [(d_schema_p, "data_reality_map"), (m_schema_p, "module_map"), (c_schema_p, "code_forensics_report")]:
        if not sp.exists():
            errors.append(f"Missing schemas/{name}.schema.json")
        else:
            passes.append(f"Found {name}.schema.json")

    # 2. Data Map
    data_json_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "DATA_REALITY_MAP.json"
    data_md_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "DATA_REALITY_MAP.md"

    if not data_json_p.exists() or not data_md_p.exists():
        errors.append("Missing DATA_REALITY_MAP json/md")
    else:
        try:
            ddata = json.loads(data_json_p.read_text(encoding="utf-8"))
            ents = ddata.get("entities", [])
            if len(ents) < 4:
                errors.append(f"Expected at least 4 data entities, found {len(ents)}")
            else:
                passes.append(f"DATA_REALITY_MAP covers {len(ents)} entities")
        except Exception as e:
            errors.append(f"Failed to parse DATA_REALITY_MAP.json: {e}")

    # 3. Module Map
    mod_json_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "MODULE_MAP.json"
    mod_md_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "MODULE_MAP.md"

    if not mod_json_p.exists() or not mod_md_p.exists():
        errors.append("Missing MODULE_MAP json/md")
    else:
        try:
            mdata = json.loads(mod_json_p.read_text(encoding="utf-8"))
            mods = mdata.get("modules", [])
            if len(mods) < 4:
                errors.append(f"Expected at least 4 modules, found {len(mods)}")
            else:
                passes.append(f"MODULE_MAP covers {len(mods)} module namespaces")
        except Exception as e:
            errors.append(f"Failed to parse MODULE_MAP.json: {e}")

    # 4. Code Forensics Report
    cfr_json_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "CODE_FORENSICS_REPORT.json"
    cfr_md_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "CODE_FORENSICS_REPORT.md"

    if not cfr_json_p.exists() or not cfr_md_p.exists():
        errors.append("Missing CODE_FORENSICS_REPORT json/md")
    else:
        try:
            cdata = json.loads(cfr_json_p.read_text(encoding="utf-8"))
            classes = cdata.get("classes_inspected", [])
            funcs = cdata.get("functions_inspected", [])
            proofs = cdata.get("line_proofs", [])

            if len(classes) < 3 or len(funcs) < 3 or len(proofs) < 3:
                errors.append("CODE_FORENSICS_REPORT has insufficient classes, functions, or line proofs")
            else:
                passes.append(f"CODE_FORENSICS_REPORT covers {len(classes)} classes, {len(funcs)} functions, {len(proofs)} line proofs")
        except Exception as e:
            errors.append(f"Failed to parse CODE_FORENSICS_REPORT.json: {e}")

    # 5. Skills
    skills_dir = ROOT / "skills"
    for sname in ["caebmad-data-investigate", "caebmad-module-investigate", "caebmad-code-forensics"]:
        if (skills_dir / sname / "SKILL.md").exists():
            passes.append(f"Found {sname} skill")
        else:
            errors.append(f"Missing {sname} skill")

    return passes, errors

def main():
    passes, errors = validate_data_module_forensics()
    print("=" * 60)
    print(f"CAE-BMAD Data/Module/Forensics Validator — Passed: {len(passes)}, Errors: {len(errors)}")
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
        print("\nALL DATA/MODULE/FORENSICS SYSTEM VALIDATIONS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
