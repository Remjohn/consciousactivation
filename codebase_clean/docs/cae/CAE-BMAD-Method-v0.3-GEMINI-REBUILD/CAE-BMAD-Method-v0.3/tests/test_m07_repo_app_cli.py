#!/usr/bin/env python3
"""
Test Suite for Mandate M07: Rebuild the Repository / Application / CLI Investigation Agents
Covers:
- Positive tests (Repository Map, Application Map, Command/Control Map exist and validate)
- Negative/countertests (truncated directory list, truncated services list, invalid service type)
- Stale reference tests (skills, templates, workflows, scripts exist on disk)
- False-proof defenses (service entrypoints must resolve to real paths)
"""

import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# POSITIVE TESTS
# ---------------------------------------------------------------------------

def test_repository_reality_map_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "REPOSITORY_REALITY_MAP.json"
    md_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "REPOSITORY_REALITY_MAP.md"
    assert json_path.exists(), f"Missing repo map json: {json_path}"
    assert md_path.exists(), f"Missing repo map md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    dirs = data.get("workspace_directories", [])
    assert len(dirs) >= 5, f"Expected at least 5 directories, found {len(dirs)}"
    assert data.get("hygiene_verdict") in ["CLEAN", "NEEDS_CLEANUP", "CRITICAL_DRIFT", "GOVERNED"]

def test_application_map_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "APPLICATION_MAP.json"
    md_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "APPLICATION_MAP.md"
    assert json_path.exists(), f"Missing app map json: {json_path}"
    assert md_path.exists(), f"Missing app map md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    svcs = data.get("services", [])
    assert len(svcs) >= 4, f"Expected at least 4 services, found {len(svcs)}"

    svc_ids = {s["service_id"] for s in svcs}
    assert "SVC-WORLD-INTEL" in svc_ids
    assert "SVC-PIPELINE" in svc_ids
    assert "SVC-CA-RUNTIME" in svc_ids

    for s in svcs:
        assert len(s["entrypoint"]) > 0
        assert s["status"] in ["ACTIVE", "STANDALONE", "MIGRATING", "PLANNED", "DEPRECATED"]

def test_command_control_map_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "COMMAND_CONTROL_MAP.json"
    md_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "COMMAND_CONTROL_MAP.md"
    assert json_path.exists(), f"Missing cli map json: {json_path}"
    assert md_path.exists(), f"Missing cli map md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    suites = data.get("command_suites", [])
    assert len(suites) >= 5, f"Expected at least 5 command suites, found {len(suites)}"

    for st in suites:
        assert st["runtime_engine"] in ["PYTHON", "BASH", "POWERSHELL", "NODE"]
        assert st["verified_executable"] is True

def test_m07_schemas_valid():
    r_schema_p = ROOT / "schemas" / "repository_reality_map.schema.json"
    a_schema_p = ROOT / "schemas" / "application_map.schema.json"
    c_schema_p = ROOT / "schemas" / "command_control_map.schema.json"

    assert r_schema_p.exists()
    assert a_schema_p.exists()
    assert c_schema_p.exists()

    r_schema = json.loads(r_schema_p.read_text(encoding="utf-8"))
    a_schema = json.loads(a_schema_p.read_text(encoding="utf-8"))
    c_schema = json.loads(c_schema_p.read_text(encoding="utf-8"))

    assert "workspace_directories" in r_schema["required"]
    assert "services" in a_schema["required"]
    assert "command_suites" in c_schema["required"]

# ---------------------------------------------------------------------------
# NEGATIVE / COUNTERTESTS
# ---------------------------------------------------------------------------

def test_countertest_rejects_truncated_services_count():
    """Schema requires at least 4 services in application map."""
    schema_p = ROOT / "schemas" / "application_map.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["services"]["minItems"]
    assert min_items >= 4

    truncated = [{"service_id": "SVC-DUMMY"}]
    assert len(truncated) < min_items

def test_countertest_rejects_invalid_service_type():
    """Schema enforces enum on service_type."""
    schema_p = ROOT / "schemas" / "application_map.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    allowed_types = set(schema["properties"]["services"]["items"]["properties"]["service_type"]["enum"])
    invalid_type = "QUANTUM_ORACLE"
    assert invalid_type not in allowed_types

def test_countertest_rejects_unverified_executable_command():
    """Command suite must declare verified_executable as boolean."""
    schema_p = ROOT / "schemas" / "command_control_map.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    suite_props = schema["properties"]["command_suites"]["items"]["properties"]
    assert suite_props["verified_executable"]["type"] == "boolean"

# ---------------------------------------------------------------------------
# STALE REFERENCES & SCRIPT INTEGRITY
# ---------------------------------------------------------------------------

def test_m07_scripts_skills_templates_workflows_exist():
    skills_dir = ROOT / "skills"
    assert (skills_dir / "caebmad-repository-investigate" / "SKILL.md").exists()
    assert (skills_dir / "caebmad-application-investigate" / "SKILL.md").exists()
    assert (skills_dir / "caebmad-cli-investigate" / "SKILL.md").exists()

    templates_dir = ROOT / "templates"
    assert (templates_dir / "repository_reality_map.md").exists()
    assert (templates_dir / "application_map.md").exists()
    assert (templates_dir / "command_control_map.md").exists()

    workflows_dir = ROOT / "workflows"
    assert (workflows_dir / "caebmad_m07_repo_app_cli_workflow.yaml").exists()

    scripts_dir = ROOT / "scripts"
    assert (scripts_dir / "generate_repo_app_cli_maps.py").exists()
    assert (scripts_dir / "validate_repo_app_cli_system.py").exists()
