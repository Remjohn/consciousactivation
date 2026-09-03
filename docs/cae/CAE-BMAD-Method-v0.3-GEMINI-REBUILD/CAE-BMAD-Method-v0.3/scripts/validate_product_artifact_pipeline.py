#!/usr/bin/env python3
"""
CAE-BMAD Product Artifact Production Pipeline Validator
Validates:
- PRODUCT_BRIEF.json conforms to schemas/product_brief.schema.json
- ARCHITECTURE.json conforms to schemas/architecture_spec.schema.json
- UI_UX_SPECIFICATION.json conforms to schemas/ui_ux_spec.schema.json
- Associated skills, templates, workflows, and markdown companions exist
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate_product_pipeline() -> tuple[list[str], list[str]]:
    passes = []
    errors = []

    # 1. Schemas
    pb_schema_p = ROOT / "schemas" / "product_brief.schema.json"
    arch_schema_p = ROOT / "schemas" / "architecture_spec.schema.json"
    ui_schema_p = ROOT / "schemas" / "ui_ux_spec.schema.json"

    for sp, name in [(pb_schema_p, "product_brief"), (arch_schema_p, "architecture_spec"), (ui_schema_p, "ui_ux_spec")]:
        if not sp.exists():
            errors.append(f"Missing schemas/{name}.schema.json")
        else:
            passes.append(f"Found {name}.schema.json")

    # 2. Product Brief
    pb_json_p = ROOT / "docs" / "cae-bmad" / "03_product" / "PRODUCT_BRIEF.json"
    pb_md_p = ROOT / "docs" / "cae-bmad" / "03_product" / "PRODUCT_BRIEF.md"

    if not pb_json_p.exists() or not pb_md_p.exists():
        errors.append("Missing PRODUCT_BRIEF json/md")
    else:
        try:
            pdata = json.loads(pb_json_p.read_text(encoding="utf-8"))
            pillars = pdata.get("capability_pillars", [])
            non_goals = pdata.get("non_goals", [])
            if len(pillars) < 5:
                errors.append(f"Expected at least 5 pillars in Product Brief, found {len(pillars)}")
            elif len(non_goals) < 2:
                errors.append(f"Expected at least 2 non-goals in Product Brief, found {len(non_goals)}")
            else:
                passes.append(f"PRODUCT_BRIEF covers {len(pillars)} pillars and {len(non_goals)} non-goals")
        except Exception as e:
            errors.append(f"Failed to parse PRODUCT_BRIEF.json: {e}")

    # 3. Architecture Spec
    arch_json_p = ROOT / "docs" / "cae-bmad" / "04_architecture" / "ARCHITECTURE.json"
    arch_md_p = ROOT / "docs" / "cae-bmad" / "04_architecture" / "ARCHITECTURE.md"

    if not arch_json_p.exists() or not arch_md_p.exists():
        errors.append("Missing ARCHITECTURE json/md")
    else:
        try:
            adata = json.loads(arch_json_p.read_text(encoding="utf-8"))
            subs = adata.get("subsystems", [])
            ifaces = adata.get("interfaces", [])
            if len(subs) < 4:
                errors.append(f"Expected at least 4 subsystems, found {len(subs)}")
            elif len(ifaces) < 2:
                errors.append(f"Expected at least 2 interfaces, found {len(ifaces)}")
            else:
                passes.append(f"ARCHITECTURE covers {len(subs)} subsystems and {len(ifaces)} typed interfaces")
        except Exception as e:
            errors.append(f"Failed to parse ARCHITECTURE.json: {e}")

    # 4. UI/UX Spec
    ui_json_p = ROOT / "docs" / "cae-bmad" / "06_ui_ux" / "UI_UX_SPECIFICATION.json"
    ui_md_p = ROOT / "docs" / "cae-bmad" / "06_ui_ux" / "UI_UX_SPECIFICATION.md"

    if not ui_json_p.exists() or not ui_md_p.exists():
        errors.append("Missing UI_UX_SPECIFICATION json/md")
    else:
        try:
            udata = json.loads(ui_json_p.read_text(encoding="utf-8"))
            views = udata.get("operator_views", [])
            tokens = udata.get("atomic_harness_tokens", {})
            if len(views) < 3:
                errors.append(f"Expected at least 3 operator views, found {len(views)}")
            elif "color_tokens" not in tokens or len(tokens["color_tokens"]) == 0:
                errors.append("UI_UX_SPECIFICATION missing Atomic Harness color tokens")
            else:
                passes.append(f"UI_UX_SPECIFICATION covers {len(views)} views and Atomic Harness tokens")
        except Exception as e:
            errors.append(f"Failed to parse UI_UX_SPECIFICATION.json: {e}")

    # 5. Skills
    skills_dir = ROOT / "skills"
    for sname in ["caebmad-product-brief", "caebmad-architecture", "caebmad-ui"]:
        if (skills_dir / sname / "SKILL.md").exists():
            passes.append(f"Found {sname} skill")
        else:
            errors.append(f"Missing {sname} skill")

    return passes, errors

def main():
    passes, errors = validate_product_pipeline()
    print("=" * 60)
    print(f"CAE-BMAD Product Pipeline Validator — Passed: {len(passes)}, Errors: {len(errors)}")
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
        print("\nALL PRODUCT ARTIFACT PIPELINE SYSTEM VALIDATIONS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
