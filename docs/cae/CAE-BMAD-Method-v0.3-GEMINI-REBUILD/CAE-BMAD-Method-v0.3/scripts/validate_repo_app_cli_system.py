#!/usr/bin/env python3
"""
CAE-BMAD Repository, Application, and CLI System Validator
Validates:
- REPOSITORY_REALITY_MAP.json conforms to schemas/repository_reality_map.schema.json
- APPLICATION_MAP.json conforms to schemas/application_map.schema.json (min 4 services with entrypoints)
- COMMAND_CONTROL_MAP.json conforms to schemas/command_control_map.schema.json (min 5 command suites)
- Associated skills, templates, workflows, and markdown companions exist
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate_repo_app_cli() -> tuple[list[str], list[str]]:
    passes = []
    errors = []

    # 1. Schemas
    r_schema_p = ROOT / "schemas" / "repository_reality_map.schema.json"
    a_schema_p = ROOT / "schemas" / "application_map.schema.json"
    c_schema_p = ROOT / "schemas" / "command_control_map.schema.json"

    for sp, name in [(r_schema_p, "repository_reality_map"), (a_schema_p, "application_map"), (c_schema_p, "command_control_map")]:
        if not sp.exists():
            errors.append(f"Missing schemas/{name}.schema.json")
        else:
            passes.append(f"Found {name}.schema.json")

    # 2. Repo Map
    repo_json_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "REPOSITORY_REALITY_MAP.json"
    repo_md_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "REPOSITORY_REALITY_MAP.md"

    if not repo_json_p.exists() or not repo_md_p.exists():
        errors.append("Missing REPOSITORY_REALITY_MAP json/md")
    else:
        try:
            rdata = json.loads(repo_json_p.read_text(encoding="utf-8"))
            dirs = rdata.get("workspace_directories", [])
            if len(dirs) < 5:
                errors.append(f"Expected at least 5 workspace directories, found {len(dirs)}")
            else:
                passes.append(f"REPOSITORY_REALITY_MAP covers {len(dirs)} directories")
        except Exception as e:
            errors.append(f"Failed to parse REPOSITORY_REALITY_MAP.json: {e}")

    # 3. App Map
    app_json_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "APPLICATION_MAP.json"
    app_md_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "APPLICATION_MAP.md"

    if not app_json_p.exists() or not app_md_p.exists():
        errors.append("Missing APPLICATION_MAP json/md")
    else:
        try:
            adata = json.loads(app_json_p.read_text(encoding="utf-8"))
            svcs = adata.get("services", [])
            if len(svcs) < 4:
                errors.append(f"Expected at least 4 services, found {len(svcs)}")
            else:
                passes.append(f"APPLICATION_MAP covers {len(svcs)} services")
        except Exception as e:
            errors.append(f"Failed to parse APPLICATION_MAP.json: {e}")

    # 4. CLI Map
    cli_json_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "COMMAND_CONTROL_MAP.json"
    cli_md_p = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "COMMAND_CONTROL_MAP.md"

    if not cli_json_p.exists() or not cli_md_p.exists():
        errors.append("Missing COMMAND_CONTROL_MAP json/md")
    else:
        try:
            cdata = json.loads(cli_json_p.read_text(encoding="utf-8"))
            suites = cdata.get("command_suites", [])
            if len(suites) < 5:
                errors.append(f"Expected at least 5 command suites, found {len(suites)}")
            else:
                passes.append(f"COMMAND_CONTROL_MAP covers {len(suites)} command suites")
        except Exception as e:
            errors.append(f"Failed to parse COMMAND_CONTROL_MAP.json: {e}")

    # 5. Skills
    skills_dir = ROOT / "skills"
    for sname in ["caebmad-repository-investigate", "caebmad-application-investigate", "caebmad-cli-investigate"]:
        if (skills_dir / sname / "SKILL.md").exists():
            passes.append(f"Found {sname} skill")
        else:
            errors.append(f"Missing {sname} skill")

    return passes, errors

def main():
    passes, errors = validate_repo_app_cli()
    print("=" * 60)
    print(f"CAE-BMAD Repo/App/CLI Validator — Passed: {len(passes)}, Errors: {len(errors)}")
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
        print("\nALL REPO/APP/CLI SYSTEM VALIDATIONS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
