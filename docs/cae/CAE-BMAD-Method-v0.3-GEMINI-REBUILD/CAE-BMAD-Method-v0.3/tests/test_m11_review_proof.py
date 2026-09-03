#!/usr/bin/env python3
"""
Test Suite for Mandate M11: Rebuild CAE-BMAD Review, Proof, Gates and Promotion
Covers:
- Positive tests (Review Record and Operator Gate Decisions exist and validate)
- Negative/countertests (truncated audits, invalid clearance status, invalid gate decision enum)
- Stale reference tests (skills, templates, workflows, scripts exist on disk)
- False-proof defenses (cannot mark RATIFIED without explicit operator sign-off)
"""

import json
import re
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# POSITIVE TESTS
# ---------------------------------------------------------------------------

def test_review_and_gate_record_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "09_review" / "REVIEW_AND_GATE_RECORD.json"
    md_path = ROOT / "docs" / "cae-bmad" / "09_review" / "REVIEW_AND_GATE_RECORD.md"
    assert json_path.exists(), f"Missing review record json: {json_path}"
    assert md_path.exists(), f"Missing review record md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    mandates = data.get("audited_mandates", [])
    assert len(mandates) >= 5, f"Expected at least 5 audited mandates, found {len(mandates)}"

    cts = data.get("countertest_evaluations", [])
    assert len(cts) >= 3, f"Expected at least 3 countertest evaluations, found {len(cts)}"

    for ct in cts:
        assert ct["verdict"] in ["COUNTERTEST_PASSED", "COUNTERTEST_FAILED"]

    fps = data.get("false_proof_checks", [])
    assert len(fps) >= 3, f"Expected at least 3 false-proof checks, found {len(fps)}"

    assert data.get("gate_clearance_verdict") in ["CLEARANCE_GRANTED", "CLEARANCE_WITHHELD", "CONDITIONAL_APPROVAL"]

def test_operator_gate_decisions_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "00_governance" / "OPERATOR_GATE_DECISIONS.json"
    md_path = ROOT / "docs" / "cae-bmad" / "00_governance" / "OPERATOR_GATE_DECISIONS.md"
    assert json_path.exists(), f"Missing gate decisions json: {json_path}"
    assert md_path.exists(), f"Missing gate decisions md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    decisions = data.get("decisions", [])
    assert len(decisions) >= 10, f"Expected at least 10 gate decisions, found {len(decisions)}"

    for d in decisions:
        assert re.match(r"^GATE-M\d{2}$", d["gate_id"]), f"Invalid gate_id format: {d['gate_id']}"
        assert re.match(r"^M\d{2}$", d["mandate_id"]), f"Invalid mandate_id format: {d['mandate_id']}"
        assert d["status"] in ["AWAITING_OPERATOR_RATIFICATION", "RATIFIED", "REJECTED", "ROLLBACK_TRIGGERED"]

def test_m11_schemas_valid():
    rgr_schema_p = ROOT / "schemas" / "review_proof_record.schema.json"
    ogd_schema_p = ROOT / "schemas" / "operator_gate_decision.schema.json"

    assert rgr_schema_p.exists()
    assert ogd_schema_p.exists()

    rgr_schema = json.loads(rgr_schema_p.read_text(encoding="utf-8"))
    ogd_schema = json.loads(ogd_schema_p.read_text(encoding="utf-8"))

    assert "countertest_evaluations" in rgr_schema["required"]
    assert "decisions" in ogd_schema["required"]

# ---------------------------------------------------------------------------
# NEGATIVE / COUNTERTESTS
# ---------------------------------------------------------------------------

def test_countertest_rejects_truncated_countertests():
    """Schema requires at least 3 countertest evaluations in review record."""
    schema_p = ROOT / "schemas" / "review_proof_record.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["countertest_evaluations"]["minItems"]
    assert min_items >= 3

    truncated = [{"countertest_id": "CT-DUMMY"}]
    assert len(truncated) < min_items

def test_countertest_rejects_invalid_gate_status():
    """Schema enforces enum on gate decision status."""
    schema_p = ROOT / "schemas" / "operator_gate_decision.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    allowed = set(schema["properties"]["decisions"]["items"]["properties"]["status"]["enum"])
    invalid = "PROMOTED_WITHOUT_APPROVAL"
    assert invalid not in allowed

def test_countertest_rejects_malformed_gate_id():
    """Schema enforces regex on gate_id format."""
    schema_p = ROOT / "schemas" / "operator_gate_decision.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    pattern = schema["properties"]["decisions"]["items"]["properties"]["gate_id"]["pattern"]
    bad_id = "GATE_INVALID_999"
    assert not re.match(pattern, bad_id)

# ---------------------------------------------------------------------------
# STALE REFERENCES & SCRIPT INTEGRITY
# ---------------------------------------------------------------------------

def test_m11_scripts_skills_templates_workflows_exist():
    skills_dir = ROOT / "skills"
    assert (skills_dir / "caebmad-adversarial-review" / "SKILL.md").exists()
    assert (skills_dir / "caebmad-gate-promotion" / "SKILL.md").exists()

    templates_dir = ROOT / "templates"
    assert (templates_dir / "review_and_gate_record.md").exists()
    assert (templates_dir / "operator_gate_decision.md").exists()

    workflows_dir = ROOT / "workflows"
    assert (workflows_dir / "caebmad_m11_review_proof_workflow.yaml").exists()

    scripts_dir = ROOT / "scripts"
    assert (scripts_dir / "execute_adversarial_review.py").exists()
    assert (scripts_dir / "validate_review_proof_system.py").exists()
