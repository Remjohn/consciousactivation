#!/usr/bin/env python3
"""
Test Suite for Mandate M05: Rebuild the CAE Documentation and Planning Agents
Covers:
- Positive tests (PRD modules, FR matrix, epics/stories, plan genealogy, schema validation)
- Negative/countertests (untestable FRs, missing lineage, vague acceptance criteria)
- Stale reference tests (skills, templates, workflows exist)
- False-proof defenses (PRD without source lineage must fail)
"""

import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# POSITIVE TESTS
# ---------------------------------------------------------------------------

def test_prd_modules_exist_and_cover_all_5_pillars():
    modules_dir = ROOT / "docs" / "cae-bmad" / "03_product" / "modules"
    assert modules_dir.exists(), f"PRD modules directory missing: {modules_dir}"
    prd_files = sorted(modules_dir.glob("PRD-*.md"))
    assert len(prd_files) >= 5, f"Expected at least 5 PRD modules, found {len(prd_files)}"

    prd_json_p = ROOT / "docs" / "cae-bmad" / "03_product" / "PRD_MODULES.json"
    assert prd_json_p.exists()
    modules = json.loads(prd_json_p.read_text(encoding="utf-8"))
    assert len(modules) == 5

    pillar_ids = {m["capability_pillar"].split(":")[0].strip() for m in modules}
    for pid in ["PIL-01", "PIL-02", "PIL-03", "PIL-04", "PIL-05"]:
        assert pid in pillar_ids, f"Missing pillar {pid} in PRD modules"

def test_functional_requirements_matrix_present_and_valid():
    fr_p = ROOT / "docs" / "cae-bmad" / "03_product" / "FUNCTIONAL_REQUIREMENTS.md"
    assert fr_p.exists(), "FUNCTIONAL_REQUIREMENTS.md missing"
    content = fr_p.read_text(encoding="utf-8")
    assert "FR-001" in content
    assert "FR-005" in content

def test_epics_exist_with_prd_traceability():
    epics_json_p = ROOT / "docs" / "cae-bmad" / "05_planning" / "EPICS.json"
    epics_md_p = ROOT / "docs" / "cae-bmad" / "05_planning" / "EPICS.md"
    assert epics_json_p.exists()
    assert epics_md_p.exists()

    epics = json.loads(epics_json_p.read_text(encoding="utf-8"))
    assert len(epics) == 5

    for e in epics:
        assert "epic_id" in e
        assert len(e["prd_modules"]) >= 1, f"Epic {e['epic_id']} has no PRD module references"
        assert len(e["functional_requirements"]) >= 1
        assert len(e["stories"]) >= 1
        for s in e["stories"]:
            assert "as_a" in s
            assert "i_want" in s
            assert "so_that" in s
            assert len(s["acceptance_criteria"]) >= 1

def test_plan_genealogy_exists():
    genealogy_p = ROOT / "docs" / "cae-bmad" / "05_planning" / "PLAN_GENEALOGY.md"
    assert genealogy_p.exists()
    content = genealogy_p.read_text(encoding="utf-8")
    assert "M01-M12" in content
    assert "CAE-BMAD Method Rebuild" in content

def test_prd_and_epic_schemas_valid():
    prd_schema_p = ROOT / "schemas" / "prd_module.schema.json"
    epic_schema_p = ROOT / "schemas" / "epic_story.schema.json"
    assert prd_schema_p.exists()
    assert epic_schema_p.exists()

    prd_schema = json.loads(prd_schema_p.read_text(encoding="utf-8"))
    epic_schema = json.loads(epic_schema_p.read_text(encoding="utf-8"))

    assert "module_id" in prd_schema["required"]
    assert "functional_requirements" in prd_schema["required"]
    assert "source_lineage" in prd_schema["required"]
    assert "epic_id" in epic_schema["required"]
    assert "stories" in epic_schema["required"]

# ---------------------------------------------------------------------------
# NEGATIVE / COUNTERTESTS
# ---------------------------------------------------------------------------

def test_countertest_rejects_untestable_fr():
    """Schema enforces testable: true as const."""
    prd_schema_p = ROOT / "schemas" / "prd_module.schema.json"
    schema = json.loads(prd_schema_p.read_text(encoding="utf-8"))
    fr_props = schema["properties"]["functional_requirements"]["items"]["properties"]
    assert fr_props["testable"]["const"] is True

def test_countertest_rejects_prd_without_source_lineage():
    """Schema enforces at least 1 source lineage entry."""
    prd_schema_p = ROOT / "schemas" / "prd_module.schema.json"
    schema = json.loads(prd_schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["source_lineage"]["minItems"]
    assert min_items >= 1

def test_countertest_rejects_epic_without_stories():
    """Schema enforces at least 1 story per epic."""
    epic_schema_p = ROOT / "schemas" / "epic_story.schema.json"
    schema = json.loads(epic_schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["stories"]["minItems"]
    assert min_items >= 1

# ---------------------------------------------------------------------------
# STALE REFERENCES & SKILL INTEGRITY
# ---------------------------------------------------------------------------

def test_doc_planning_skills_templates_workflows_exist():
    skills_dir = ROOT / "skills"
    assert (skills_dir / "caebmad-prd" / "SKILL.md").exists()
    assert (skills_dir / "caebmad-epics-stories" / "SKILL.md").exists()
    assert (skills_dir / "caebmad-fr" / "SKILL.md").exists()

    templates_dir = ROOT / "templates"
    assert (templates_dir / "prd_module.md").exists()
    assert (templates_dir / "epic_story.md").exists()

    workflows_dir = ROOT / "workflows"
    assert (workflows_dir / "caebmad_m05_doc_planning_workflow.yaml").exists()

    scripts_dir = ROOT / "scripts"
    assert (scripts_dir / "generate_doc_planning.py").exists()
    assert (scripts_dir / "validate_doc_planning_system.py").exists()
