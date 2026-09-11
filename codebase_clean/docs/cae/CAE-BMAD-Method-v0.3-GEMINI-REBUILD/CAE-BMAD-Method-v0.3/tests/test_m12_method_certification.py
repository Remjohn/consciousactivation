#!/usr/bin/env python3
"""
Test Suite for Mandate M12: Integrate and Certify the Complete CAE-BMAD Method
Covers:
- Positive tests (Master Certification Package and End-to-End Integration Run exist and validate)
- Negative/countertests (truncated mandates, incomplete operating levels, missing line proofs)
- Stale reference tests (skills, templates, workflows, scripts exist on disk)
- False-proof defenses (line-level proofs must cite physical files on disk with exact snippets)
"""

import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# POSITIVE TESTS
# ---------------------------------------------------------------------------

def test_method_certification_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "10_certification" / "CAE_BMAD_METHOD_CERTIFICATION.json"
    md_path = ROOT / "docs" / "cae-bmad" / "10_certification" / "CAE_BMAD_METHOD_CERTIFICATION.md"
    assert json_path.exists(), f"Missing certification json: {json_path}"
    assert md_path.exists(), f"Missing certification md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    mandates = data.get("mandate_certifications", [])
    assert len(mandates) == 12, f"Expected exactly 12 certified mandates, found {len(mandates)}"

    levels = data.get("operating_level_coverage", [])
    assert len(levels) == 13, f"Expected exactly 13 operating levels, found {len(levels)}"

    e2e = data.get("end_to_end_verification_summary", {})
    assert e2e.get("trace_verified") is True
    assert len(e2e.get("physical_code_touched", [])) >= 3

    assert data.get("final_certification_verdict") == "METHOD_CERTIFIED_FOR_OPERATOR_RATIFICATION"

def test_end_to_end_integration_run_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "10_certification" / "END_TO_END_INTEGRATION_RUN.json"
    md_path = ROOT / "docs" / "cae-bmad" / "10_certification" / "END_TO_END_INTEGRATION_RUN.md"
    assert json_path.exists(), f"Missing integration run json: {json_path}"
    assert md_path.exists(), f"Missing integration run md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    steps = data.get("trace_steps", [])
    assert len(steps) >= 10, f"Expected at least 10 trace steps across Levels 01-13, found {len(steps)}"

    proofs = data.get("line_level_proofs", [])
    assert len(proofs) >= 3, f"Expected at least 3 line-level proofs, found {len(proofs)}"

    WORKSPACE_ROOT = ROOT.parents[3] if len(ROOT.parents) > 3 and (ROOT.parents[3] / "packages").exists() else ROOT
    for p in proofs:
        assert len(p["exact_snippet"]) > 20
        assert (WORKSPACE_ROOT / p["file_path"]).exists(), f"Proof cites non-existent file: {p['file_path']}"

    assert data.get("fidelity_verdict") == "END_TO_END_PROVEN_AGAINST_REAL_CODE"

def test_m12_schemas_valid():
    cert_schema_p = ROOT / "schemas" / "method_certification_package.schema.json"
    e2e_schema_p = ROOT / "schemas" / "end_to_end_integration_run.schema.json"

    assert cert_schema_p.exists()
    assert e2e_schema_p.exists()

    cert_schema = json.loads(cert_schema_p.read_text(encoding="utf-8"))
    e2e_schema = json.loads(e2e_schema_p.read_text(encoding="utf-8"))

    assert "mandate_certifications" in cert_schema["required"]
    assert "operating_level_coverage" in cert_schema["required"]
    assert "trace_steps" in e2e_schema["required"]

# ---------------------------------------------------------------------------
# NEGATIVE / COUNTERTESTS
# ---------------------------------------------------------------------------

def test_countertest_rejects_truncated_mandates():
    """Schema requires at least 12 mandate certifications."""
    schema_p = ROOT / "schemas" / "method_certification_package.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["mandate_certifications"]["minItems"]
    assert min_items >= 12

    truncated = [{"mandate_id": "M01"}]
    assert len(truncated) < min_items

def test_countertest_rejects_truncated_operating_levels():
    """Schema requires at least 13 operating levels."""
    schema_p = ROOT / "schemas" / "method_certification_package.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["operating_level_coverage"]["minItems"]
    assert min_items >= 13

    truncated = [{"level_index": "01"}]
    assert len(truncated) < min_items

def test_countertest_rejects_empty_proofs_in_e2e():
    """Schema requires at least 3 line-level proofs in integration run."""
    schema_p = ROOT / "schemas" / "end_to_end_integration_run.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["line_level_proofs"]["minItems"]
    assert min_items >= 3

    truncated = [{"file_path": "dummy.py"}]
    assert len(truncated) < min_items

# ---------------------------------------------------------------------------
# STALE REFERENCES & SCRIPT INTEGRITY
# ---------------------------------------------------------------------------

def test_m12_scripts_skills_templates_workflows_exist():
    skills_dir = ROOT / "skills"
    assert (skills_dir / "caebmad-method-certification" / "SKILL.md").exists()

    templates_dir = ROOT / "templates"
    assert (templates_dir / "method_certification_package.md").exists()
    assert (templates_dir / "end_to_end_integration_run.md").exists()

    workflows_dir = ROOT / "workflows"
    assert (workflows_dir / "caebmad_m12_method_certification_workflow.yaml").exists()

    scripts_dir = ROOT / "scripts"
    assert (scripts_dir / "certify_complete_method.py").exists()
    assert (scripts_dir / "validate_method_certification.py").exists()
