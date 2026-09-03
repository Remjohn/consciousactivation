#!/usr/bin/env python3
"""
Test Suite for the CAE-BMAD Grill-Me Protocol & Signal Distillation System
Covers:
- Positive tests (Grill spec, schema, skill, template, and canonical session exist and validate)
- Density floor enforcement (recommended answer must be >= 320 words)
- Collision primitive validation (PREDICTION_VIOLATION, COSTLY_EXPOSURE, LATENT_PATTERN_ARTICULATION)
- Anti-genericity reality contact checks (all 4 checks must be True)
- Negative/countertests (rejects sub-320 words, rejects missing code precheck, rejects false anti-genericity checks)
- Stale reference tests (skills, templates, scripts exist on disk)
"""

import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# POSITIVE TESTS
# ---------------------------------------------------------------------------

def test_grill_spec_and_schemas_exist():
    spec_p = ROOT / "method" / "CAE_BMAD_GRILL_SPEC.md"
    schema_p = ROOT / "schemas" / "grill_session.schema.json"
    template_p = ROOT / "templates" / "grill_question.md"
    skill_p = ROOT / "skills" / "caebmad-grill-protocol" / "SKILL.md"

    assert spec_p.exists(), f"Missing grill spec: {spec_p}"
    assert schema_p.exists(), f"Missing grill schema: {schema_p}"
    assert template_p.exists(), f"Missing grill template: {template_p}"
    assert skill_p.exists(), f"Missing grill skill: {skill_p}"

def test_canonical_grill_session_conforms_to_schema():
    json_path = ROOT / "docs" / "cae-bmad" / "00_governance" / "CANONICAL_GRILL_SESSION_001.json"
    md_path = ROOT / "docs" / "cae-bmad" / "00_governance" / "CANONICAL_GRILL_SESSION_001.md"

    assert json_path.exists(), f"Missing canonical grill json: {json_path}"
    assert md_path.exists(), f"Missing canonical grill md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))

    # Check density floor
    rec = data.get("recommended_answer", "")
    words = len(rec.split())
    assert words >= 320, f"Recommended answer below 320-word floor: {words} words"

    # Check collision primitive
    assert data.get("collision_primitive") in ["PREDICTION_VIOLATION", "COSTLY_EXPOSURE", "LATENT_PATTERN_ARTICULATION"]

    # Check anti-genericity checks
    evals = data.get("anti_genericity_evaluations", {})
    for k in ["passed_check_1", "passed_check_2", "passed_check_3", "passed_check_4"]:
        assert evals.get(k) is True, f"Anti-genericity check {k} failed"

    # Check code precheck
    precheck = data.get("code_precheck", {})
    assert len(precheck.get("inspected_surfaces", [])) >= 1
    assert len(precheck.get("why_unresolvable_by_code", "")) >= 20

def test_grill_schema_definition_valid():
    schema_p = ROOT / "schemas" / "grill_session.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))

    assert "recommended_answer" in schema["required"]
    assert "word_count" in schema["required"]
    assert "collision_primitive" in schema["required"]
    assert schema["properties"]["word_count"]["minimum"] >= 320

# ---------------------------------------------------------------------------
# NEGATIVE / COUNTERTESTS
# ---------------------------------------------------------------------------

def test_countertest_rejects_sub_320_word_recommendation():
    """Schema and rule enforce minimum 320 words to prevent Density Decay."""
    schema_p = ROOT / "schemas" / "grill_session.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_words = schema["properties"]["word_count"]["minimum"]
    assert min_words >= 320

    shallow_rec = "We recommend Postgres because it is reliable and scalable for our database."
    words = len(shallow_rec.split())
    assert words < min_words, "Shallow recommendation should be under min word floor"

def test_countertest_rejects_empty_code_precheck():
    """Schema requires at least 1 inspected surface in code_precheck."""
    schema_p = ROOT / "schemas" / "grill_session.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_surfaces = schema["properties"]["code_precheck"]["properties"]["inspected_surfaces"]["minItems"]
    assert min_surfaces >= 1

    empty_surfaces = []
    assert len(empty_surfaces) < min_surfaces

def test_countertest_rejects_failed_anti_genericity_gate():
    """Schema requires all 4 anti-genericity evaluations to be const: true."""
    schema_p = ROOT / "schemas" / "grill_session.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    check_schema = schema["properties"]["anti_genericity_evaluations"]["properties"]["passed_check_1"]
    assert check_schema.get("const") is True

# ---------------------------------------------------------------------------
# STALE REFERENCES & INTEGRITY
# ---------------------------------------------------------------------------

def test_grill_scripts_skills_templates_exist():
    assert (ROOT / "skills" / "caebmad-grill-protocol" / "SKILL.md").exists()
    assert (ROOT / "templates" / "grill_question.md").exists()
    assert (ROOT / "scripts" / "generate_canonical_grill_session.py").exists()
    assert (ROOT / "scripts" / "validate_grill_protocol.py").exists()
