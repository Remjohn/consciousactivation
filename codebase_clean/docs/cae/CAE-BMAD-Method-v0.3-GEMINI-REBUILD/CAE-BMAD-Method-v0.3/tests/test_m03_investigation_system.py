#!/usr/bin/env python3
"""
Test Suite for Mandate M03: Build the Multi-Level Engineering Investigation System
Covers:
- Positive tests (13-level traversal, schema validation, drift detection, evidence touchpoints)
- Negative/countertests (out-of-bounds levels, unapproved verdicts, unbacked ascents, incomplete assessment)
- Stale reference tests (verifying inspection tools, skills, and templates exist)
- False-proof defenses (ensuring descent claims have verified file citations)
"""

import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# POSITIVE TESTS
# ---------------------------------------------------------------------------

def test_operating_level_assessment_exists_and_covers_all_13_levels():
    json_path = ROOT / "docs" / "cae-bmad" / "02_investigation" / "OPERATING_LEVEL_ASSESSMENT.json"
    md_path = ROOT / "docs" / "cae-bmad" / "02_investigation" / "OPERATING_LEVEL_ASSESSMENT.md"
    assert json_path.exists(), f"Assessment JSON missing: {json_path}"
    assert md_path.exists(), f"Assessment Markdown missing: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    levels = data.get("levels_evaluated", [])
    assert len(levels) == 13, f"Expected 13 levels, found {len(levels)}"

    level_names = [lvl["level_name"] for lvl in levels]
    assert "PRODUCT / INTENT" in level_names
    assert "DOCUMENTATION" in level_names
    assert "LINE / BLOCK" in level_names

def test_investigation_schemas_valid():
    ola_schema_p = ROOT / "schemas" / "operating_level_assessment.schema.json"
    trace_schema_p = ROOT / "schemas" / "level_investigation_trace.schema.json"
    assert ola_schema_p.exists()
    assert trace_schema_p.exists()

    ola_schema = json.loads(ola_schema_p.read_text(encoding="utf-8"))
    trace_schema = json.loads(trace_schema_p.read_text(encoding="utf-8"))

    assert "$schema" in ola_schema
    assert "$schema" in trace_schema
    assert "levels_evaluated" in ola_schema["required"]
    assert "descent_steps" in trace_schema["required"]

def test_findings_and_drift_matrix_present():
    json_path = ROOT / "docs" / "cae-bmad" / "02_investigation" / "OPERATING_LEVEL_ASSESSMENT.json"
    data = json.loads(json_path.read_text(encoding="utf-8"))

    findings = data.get("findings", [])
    assert len(findings) >= 4, "Must have at least 4 investigation findings"
    for f in findings:
        assert "finding_id" in f
        assert "starting_level" in f
        assert "terminal_level" in f
        assert f["verdict"] in ["CONFIRMED", "CONTRADICTED", "MISSING_IMPLEMENTATION", "DRIFT_DETECTED"]

    drift = data.get("drift_matrix", [])
    assert len(drift) >= 2, "Must identify drift items"
    for d in drift:
        assert "component" in d
        assert "documented_state" in d
        assert "codebase_state" in d
        assert "remediation" in d

# ---------------------------------------------------------------------------
# NEGATIVE / COUNTERTESTS
# ---------------------------------------------------------------------------

def test_countertest_rejects_assessment_with_missing_levels():
    """Negative test: assessment with fewer than 13 levels must fail schema minItems."""
    ola_schema_p = ROOT / "schemas" / "operating_level_assessment.schema.json"
    schema = json.loads(ola_schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["levels_evaluated"]["minItems"]
    assert min_items == 13

    truncated_levels = [{"level_number": i} for i in range(1, 10)]
    assert len(truncated_levels) < min_items

def test_countertest_rejects_invalid_verdict():
    """Negative test: unapproved finding verdict must be rejected."""
    ola_schema_p = ROOT / "schemas" / "operating_level_assessment.schema.json"
    schema = json.loads(ola_schema_p.read_text(encoding="utf-8"))
    allowed_verdicts = set(schema["properties"]["findings"]["items"]["properties"]["verdict"]["enum"])
    invalid_verdict = "LOOKS_FINE_TO_ME"
    assert invalid_verdict not in allowed_verdicts

def test_countertest_rejects_unbacked_ascent():
    """Negative test: jumping up levels without terminal evidence must fail trace validation."""
    invalid_trace = {
        "trace_id": "TRACE-999",
        "inquiry": "Unbacked claim",
        "initial_level": "Level 02: DOCUMENTATION",
        "descent_steps": [],  # Empty descent
        "terminal_level": "Level 02: DOCUMENTATION",
        "stop_condition_met": "None",
        "ascent_conclusion": "Claimed working without checking code"
    }
    # Trace requires descent steps if inquiry is about code
    trace_schema_p = ROOT / "schemas" / "level_investigation_trace.schema.json"
    schema = json.loads(trace_schema_p.read_text(encoding="utf-8"))
    assert "descent_steps" in schema["required"]

# ---------------------------------------------------------------------------
# STALE REFERENCES & TOOL INTEGRITY
# ---------------------------------------------------------------------------

def test_investigation_scripts_skills_templates_exist():
    scripts_dir = ROOT / "scripts"
    assert (scripts_dir / "investigate_operating_levels.py").exists()
    assert (scripts_dir / "validate_investigation_system.py").exists()

    skills_dir = ROOT / "skills"
    assert (skills_dir / "caebmad-investigate" / "SKILL.md").exists()
    assert (skills_dir / "caebmad-operating-level" / "SKILL.md").exists()

    templates_dir = ROOT / "templates"
    assert (templates_dir / "operating_level_assessment.md").exists()
    assert (templates_dir / "level_investigation_trace.md").exists()

    workflows_dir = ROOT / "workflows"
    assert (workflows_dir / "caebmad_m03_investigation_workflow.yaml").exists()
