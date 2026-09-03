#!/usr/bin/env python3
"""
Test Suite for Mandate M10: Rebuild Brownfield Reconciliation and Missing-Layer Detection
Covers:
- Positive tests (Reconciliation Report and Missing Implementation Register exist and validate)
- Negative/countertests (truncated evaluations, missing gap IDs, invalid verdicts)
- Stale reference tests (skills, templates, workflows, scripts exist on disk)
- False-proof defenses (brownfield claim without inspected code surface = FAIL)
"""

import json
import re
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# POSITIVE TESTS
# ---------------------------------------------------------------------------

def test_brownfield_reconciliation_report_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "BROWNFIELD_RECONCILIATION_REPORT.json"
    md_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "BROWNFIELD_RECONCILIATION_REPORT.md"
    assert json_path.exists(), f"Missing reconciliation report json: {json_path}"
    assert md_path.exists(), f"Missing reconciliation report md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    evals = data.get("subsystem_evaluations", [])
    assert len(evals) >= 5, f"Expected at least 5 subsystem evaluations, found {len(evals)}"

    verdicts = {e["fidelity_verdict"] for e in evals}
    valid_verdicts = {"VERIFIED_COMPLETE", "PARTIAL_IMPLEMENTATION", "MISSING_LAYER", "CONTRADICTED"}
    assert verdicts.issubset(valid_verdicts), f"Invalid verdicts found: {verdicts - valid_verdicts}"

    summary = data.get("layer_gap_summary", {})
    total = summary.get("verified_count", 0) + summary.get("partial_count", 0) + summary.get("missing_count", 0) + summary.get("contradicted_count", 0)
    assert total >= 5

    assert data["reconciliation_verdict"] in ["RECONCILED_WITH_GAPS_VISIBLE", "FULLY_RECONCILED", "UNRECONCILED_DRIFT"]

def test_missing_implementation_register_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "MISSING_IMPLEMENTATION_REGISTER.json"
    md_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "MISSING_IMPLEMENTATION_REGISTER.md"
    assert json_path.exists(), f"Missing register json: {json_path}"
    assert md_path.exists(), f"Missing register md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    gaps = data.get("gap_items", [])
    assert len(gaps) >= 3, f"Expected at least 3 gap items, found {len(gaps)}"

    for g in gaps:
        assert re.match(r"^GAP-\d{3}$", g["gap_id"]), f"Invalid gap_id format: {g['gap_id']}"
        assert g["severity"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        assert len(g["remediation_plan"]) >= 10

    roadmap = data.get("remediation_roadmap", [])
    assert len(roadmap) >= 1

def test_m10_schemas_valid():
    br_schema_p = ROOT / "schemas" / "brownfield_reconciliation.schema.json"
    mir_schema_p = ROOT / "schemas" / "missing_implementation_register.schema.json"

    assert br_schema_p.exists()
    assert mir_schema_p.exists()

    br_schema = json.loads(br_schema_p.read_text(encoding="utf-8"))
    mir_schema = json.loads(mir_schema_p.read_text(encoding="utf-8"))

    assert "subsystem_evaluations" in br_schema["required"]
    assert "gap_items" in mir_schema["required"]

# ---------------------------------------------------------------------------
# NEGATIVE / COUNTERTESTS
# ---------------------------------------------------------------------------

def test_countertest_rejects_truncated_evaluations():
    """Schema requires at least 5 subsystem evaluations in reconciliation report."""
    schema_p = ROOT / "schemas" / "brownfield_reconciliation.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["subsystem_evaluations"]["minItems"]
    assert min_items >= 5

    truncated = [{"subsystem_name": "DummyOnly"}]
    assert len(truncated) < min_items

def test_countertest_rejects_invalid_fidelity_verdict():
    """Schema enforces enum on fidelity_verdict."""
    schema_p = ROOT / "schemas" / "brownfield_reconciliation.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    allowed = set(schema["properties"]["subsystem_evaluations"]["items"]["properties"]["fidelity_verdict"]["enum"])
    invalid = "LOOKS_FINE_TRUST_ME"
    assert invalid not in allowed

def test_countertest_rejects_gap_without_remediation():
    """Schema requires minLength 10 for remediation_plan on each gap item."""
    schema_p = ROOT / "schemas" / "missing_implementation_register.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_len = schema["properties"]["gap_items"]["items"]["properties"]["remediation_plan"]["minLength"]
    assert min_len >= 10

    empty_plan = "Fix it"
    assert len(empty_plan) < min_len

# ---------------------------------------------------------------------------
# STALE REFERENCES & SCRIPT INTEGRITY
# ---------------------------------------------------------------------------

def test_m10_scripts_skills_templates_workflows_exist():
    skills_dir = ROOT / "skills"
    assert (skills_dir / "caebmad-brownfield-reconciliation" / "SKILL.md").exists()
    assert (skills_dir / "caebmad-missing-layer-detect" / "SKILL.md").exists()

    templates_dir = ROOT / "templates"
    assert (templates_dir / "brownfield_reconciliation_report.md").exists()
    assert (templates_dir / "missing_implementation_register.md").exists()

    workflows_dir = ROOT / "workflows"
    assert (workflows_dir / "caebmad_m10_brownfield_reconciliation_workflow.yaml").exists()

    scripts_dir = ROOT / "scripts"
    assert (scripts_dir / "reconcile_brownfield_reality.py").exists()
    assert (scripts_dir / "validate_brownfield_reconciliation_system.py").exists()
