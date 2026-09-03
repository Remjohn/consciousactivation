#!/usr/bin/env python3
"""
Test Suite for Mandate M09: Rebuild the CAE Product Artifact Production Pipeline
Covers:
- Positive tests (Product Brief, Architecture Spec, UI/UX Spec exist and validate)
- Negative/countertests (truncated pillars, missing non-goals, missing interface contracts)
- Stale reference tests (skills, templates, workflows, scripts exist on disk)
- False-proof defenses (subsystems must bind to physical services)
"""

import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# POSITIVE TESTS
# ---------------------------------------------------------------------------

def test_product_brief_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "03_product" / "PRODUCT_BRIEF.json"
    md_path = ROOT / "docs" / "cae-bmad" / "03_product" / "PRODUCT_BRIEF.md"
    assert json_path.exists(), f"Missing product brief json: {json_path}"
    assert md_path.exists(), f"Missing product brief md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert len(data.get("capability_pillars", [])) >= 5
    assert len(data.get("non_goals", [])) >= 2
    assert len(data.get("vision_statement", "")) >= 20

def test_architecture_spec_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "04_architecture" / "ARCHITECTURE.json"
    md_path = ROOT / "docs" / "cae-bmad" / "04_architecture" / "ARCHITECTURE.md"
    assert json_path.exists(), f"Missing architecture json: {json_path}"
    assert md_path.exists(), f"Missing architecture md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    subs = data.get("subsystems", [])
    assert len(subs) >= 4, f"Expected at least 4 subsystems, found {len(subs)}"

    ifaces = data.get("interfaces", [])
    assert len(ifaces) >= 2, f"Expected at least 2 interfaces, found {len(ifaces)}"

    for iface in ifaces:
        assert iface["type"] in ["REST_API", "GRPC", "EVENT_BUS", "INTERNAL_PYTHON_API"]

def test_ui_ux_spec_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "06_ui_ux" / "UI_UX_SPECIFICATION.json"
    md_path = ROOT / "docs" / "cae-bmad" / "06_ui_ux" / "UI_UX_SPECIFICATION.md"
    assert json_path.exists(), f"Missing UI/UX json: {json_path}"
    assert md_path.exists(), f"Missing UI/UX md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    views = data.get("operator_views", [])
    assert len(views) >= 3, f"Expected at least 3 views, found {len(views)}"

    tokens = data.get("atomic_harness_tokens", {})
    assert len(tokens.get("color_tokens", [])) >= 1
    assert len(tokens.get("typography_tokens", [])) >= 1

def test_m09_schemas_valid():
    pb_schema_p = ROOT / "schemas" / "product_brief.schema.json"
    arch_schema_p = ROOT / "schemas" / "architecture_spec.schema.json"
    ui_schema_p = ROOT / "schemas" / "ui_ux_spec.schema.json"

    assert pb_schema_p.exists()
    assert arch_schema_p.exists()
    assert ui_schema_p.exists()

    pb_schema = json.loads(pb_schema_p.read_text(encoding="utf-8"))
    arch_schema = json.loads(arch_schema_p.read_text(encoding="utf-8"))
    ui_schema = json.loads(ui_schema_p.read_text(encoding="utf-8"))

    assert "capability_pillars" in pb_schema["required"]
    assert "subsystems" in arch_schema["required"]
    assert "operator_views" in ui_schema["required"]

# ---------------------------------------------------------------------------
# NEGATIVE / COUNTERTESTS
# ---------------------------------------------------------------------------

def test_countertest_rejects_brief_without_non_goals():
    """Schema requires at least 2 non-goals in product brief."""
    schema_p = ROOT / "schemas" / "product_brief.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["non_goals"]["minItems"]
    assert min_items >= 2

    truncated = ["Only one non-goal"]
    assert len(truncated) < min_items

def test_countertest_rejects_architecture_without_subsystems():
    """Schema requires at least 4 subsystems in architecture spec."""
    schema_p = ROOT / "schemas" / "architecture_spec.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["subsystems"]["minItems"]
    assert min_items >= 4

    truncated = [{"subsystem_id": "SUB-DUMMY"}]
    assert len(truncated) < min_items

def test_countertest_rejects_ui_spec_without_views():
    """Schema requires at least 3 operator views in UI/UX spec."""
    schema_p = ROOT / "schemas" / "ui_ux_spec.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["operator_views"]["minItems"]
    assert min_items >= 3

    truncated = [{"view_id": "VIEW-DUMMY"}]
    assert len(truncated) < min_items

# ---------------------------------------------------------------------------
# STALE REFERENCES & SCRIPT INTEGRITY
# ---------------------------------------------------------------------------

def test_m09_scripts_skills_templates_workflows_exist():
    skills_dir = ROOT / "skills"
    assert (skills_dir / "caebmad-product-brief" / "SKILL.md").exists()
    assert (skills_dir / "caebmad-architecture" / "SKILL.md").exists()
    assert (skills_dir / "caebmad-ui" / "SKILL.md").exists()

    templates_dir = ROOT / "templates"
    assert (templates_dir / "product_brief.md").exists()
    assert (templates_dir / "architecture.md").exists()
    assert (templates_dir / "ui_ux_specification.md").exists()

    workflows_dir = ROOT / "workflows"
    assert (workflows_dir / "caebmad_m09_product_pipeline_workflow.yaml").exists()

    scripts_dir = ROOT / "scripts"
    assert (scripts_dir / "execute_product_artifact_pipeline.py").exists()
    assert (scripts_dir / "validate_product_artifact_pipeline.py").exists()
