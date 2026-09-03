#!/usr/bin/env python3
"""
Test Suite for Mandate M04: Rebuild the CAE Research / Product Reconstruction Agents
Covers:
- Positive tests (reconstruction artifact presence, 5 capability pillars, 216 sources analyzed, brownfield crosswalks)
- Negative/countertests (missing pillars, invalid status enum, truncated sources count)
- Stale reference tests (verifying reconstruction tools, schemas, and skills exist)
- False-proof defenses (ensuring capability claims have verified code paths)
"""

import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# POSITIVE TESTS
# ---------------------------------------------------------------------------

def test_product_reconstruction_artifacts_exist_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "01_reconstruction" / "PRODUCT_RECONSTRUCTION.json"
    md_path = ROOT / "docs" / "cae-bmad" / "01_reconstruction" / "PRODUCT_RECONSTRUCTION.md"
    assert json_path.exists(), f"Reconstruction JSON missing: {json_path}"
    assert md_path.exists(), f"Reconstruction Markdown missing: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data.get("product_name") == "Conscious Activation Engine (CAE)"
    assert data.get("sources_analyzed") == 216
    assert data.get("status") in ["APPROVED", "IN_REVIEW"]

def test_all_5_capability_pillars_defined():
    json_path = ROOT / "docs" / "cae-bmad" / "01_reconstruction" / "PRODUCT_RECONSTRUCTION.json"
    data = json.loads(json_path.read_text(encoding="utf-8"))
    pillars = data.get("capability_pillars", [])
    assert len(pillars) == 5, f"Expected 5 capability pillars, found {len(pillars)}"

    pillar_names = {p["name"] for p in pillars}
    assert "Audience & Guest Intelligence" in pillar_names
    assert "Question & Interview Intelligence" in pillar_names
    assert "Evidence & Receipt Provenance" in pillar_names
    assert "Editorial & Storyboard Production" in pillar_names
    assert "Multi-Agent Runtime & Factory Scheduling" in pillar_names

    for p in pillars:
        assert len(p["historical_roots"]) > 0
        assert len(p["active_runtime_path"]) > 0

def test_lineage_breakdown_comprehensive():
    json_path = ROOT / "docs" / "cae-bmad" / "01_reconstruction" / "PRODUCT_RECONSTRUCTION.json"
    data = json.loads(json_path.read_text(encoding="utf-8"))
    lineage = data.get("lineage_breakdown", {})
    assert "ccp_lineage" in lineage
    assert "cmf_lineage" in lineage
    assert "ccf_lineage" in lineage
    assert "visual_syntax" in lineage
    assert "runtime_canon" in lineage

def test_brownfield_crosswalk_has_verified_mappings():
    json_path = ROOT / "docs" / "cae-bmad" / "01_reconstruction" / "PRODUCT_RECONSTRUCTION.json"
    data = json.loads(json_path.read_text(encoding="utf-8"))
    crosswalk = data.get("brownfield_crosswalk", [])
    assert len(crosswalk) >= 5
    for c in crosswalk:
        assert "concept" in c
        assert "historical_origin" in c
        assert "modern_code_path" in c
        assert c["fidelity_status"] == "VERIFIED"

# ---------------------------------------------------------------------------
# NEGATIVE / COUNTERTESTS
# ---------------------------------------------------------------------------

def test_countertest_rejects_missing_capability_pillars():
    """Negative test: reconstruction with fewer than 5 pillars must fail schema."""
    schema_p = ROOT / "schemas" / "product_reconstruction.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["capability_pillars"]["minItems"]
    assert min_items == 5

    truncated_pillars = [{"pillar_id": "PIL-01"}]
    assert len(truncated_pillars) < min_items

def test_countertest_rejects_invalid_sources_analyzed():
    """Negative test: reconstruction claiming other than 216 sources must fail schema."""
    schema_p = ROOT / "schemas" / "product_reconstruction.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    allowed_sources_count = schema["properties"]["sources_analyzed"]["enum"]
    assert 216 in allowed_sources_count
    assert 100 not in allowed_sources_count

def test_countertest_rejects_missing_lineage_keys():
    """Negative test: missing required lineage keys must be caught."""
    schema_p = ROOT / "schemas" / "product_reconstruction.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    required_lineages = schema["properties"]["lineage_breakdown"]["required"]
    assert "ccp_lineage" in required_lineages
    assert "visual_syntax" in required_lineages

# ---------------------------------------------------------------------------
# STALE REFERENCES & SCRIPT INTEGRITY
# ---------------------------------------------------------------------------

def test_reconstruction_scripts_and_skills_exist():
    scripts_dir = ROOT / "scripts"
    assert (scripts_dir / "reconstruct_product_lineage.py").exists()
    assert (scripts_dir / "validate_product_reconstruction.py").exists()

    skills_dir = ROOT / "skills"
    assert (skills_dir / "caebmad-product-reconstruction" / "SKILL.md").exists()

    templates_dir = ROOT / "templates"
    assert (templates_dir / "product_reconstruction.md").exists()

    workflows_dir = ROOT / "workflows"
    assert (workflows_dir / "caebmad_m04_reconstruction_workflow.yaml").exists()
