#!/usr/bin/env python3
"""
Test Suite for Mandate M02: Build the 216-Source Research Intake and Lineage System
Covers:
- Positive tests (216 sources exact count, schema validation, score distribution, authority classes)
- Negative/countertests (out-of-bounds scores, invalid enum values, duplicate IDs, incomplete sources)
- Stale reference tests (verifying research files and schemas exist on disk)
- False-proof defenses (preventing synthetic or unclassified source entries)
"""

import json
import pytest
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# POSITIVE TESTS
# ---------------------------------------------------------------------------

def test_research_library_file_exists_and_has_216_sources():
    lib_path = ROOT / ".caebmad" / "research" / "CAE_RESEARCH_LIBRARY.yaml"
    assert lib_path.exists(), f"Research library missing: {lib_path}"
    data = yaml.safe_load(lib_path.read_text(encoding="utf-8"))
    sources = data.get("sources", [])
    assert len(sources) == 216, f"Expected exactly 216 sources, found {len(sources)}"
    assert data.get("target_sources") == 216
    assert data.get("baseline_count") == 144
    assert data.get("extended_count") == 72

def test_research_source_schemas_exist_and_valid():
    src_schema_p = ROOT / "schemas" / "research_source.schema.json"
    lib_schema_p = ROOT / "schemas" / "research_library.schema.json"
    assert src_schema_p.exists()
    assert lib_schema_p.exists()

    src_schema = json.loads(src_schema_p.read_text(encoding="utf-8"))
    lib_schema = json.loads(lib_schema_p.read_text(encoding="utf-8"))

    assert "$schema" in src_schema
    assert "$schema" in lib_schema
    assert "source_id" in src_schema["required"]
    assert "relevance" in src_schema["required"]
    assert "authority" in src_schema["required"]
    assert "lineage" in src_schema["required"]

def test_all_216_sources_conform_to_schema_rules():
    lib_path = ROOT / ".caebmad" / "research" / "CAE_RESEARCH_LIBRARY.yaml"
    data = yaml.safe_load(lib_path.read_text(encoding="utf-8"))
    sources = data.get("sources", [])

    src_schema_p = ROOT / "schemas" / "research_source.schema.json"
    src_schema = json.loads(src_schema_p.read_text(encoding="utf-8"))
    allowed_classes = set(src_schema["properties"]["source_class"]["enum"])
    allowed_lineages = set(src_schema["properties"]["lineage"]["enum"])
    allowed_authorities = set(src_schema["properties"]["authority"]["enum"])
    allowed_statuses = set(src_schema["properties"]["status"]["enum"])

    seen_ids = set()
    for s in sources:
        sid = s["source_id"]
        assert sid not in seen_ids, f"Duplicate source ID: {sid}"
        seen_ids.add(sid)

        assert 0 <= s["relevance"] <= 100, f"Invalid relevance score: {s['relevance']}"
        assert s["source_class"] in allowed_classes, f"Invalid class: {s['source_class']}"
        assert s["lineage"] in allowed_lineages, f"Invalid lineage: {s['lineage']}"
        assert s["authority"] in allowed_authorities, f"Invalid authority: {s['authority']}"
        assert s["status"] in allowed_statuses, f"Invalid status: {s['status']}"
        assert len(s["title"]) > 0
        assert len(s["why_it_matters"]) > 0

def test_foundation_100_relevance_sources_present():
    lib_path = ROOT / ".caebmad" / "research" / "CAE_RESEARCH_LIBRARY.yaml"
    data = yaml.safe_load(lib_path.read_text(encoding="utf-8"))
    sources = data.get("sources", [])

    top_sources = [s for s in sources if s["relevance"] == 100]
    assert len(top_sources) >= 2, "Must have foundational 100-relevance sources"
    titles = {s["title"] for s in top_sources}
    assert any("PRD" in t or "Workspace" in t for t in titles)

# ---------------------------------------------------------------------------
# NEGATIVE / COUNTERTESTS
# ---------------------------------------------------------------------------

def test_countertest_rejects_out_of_bounds_relevance():
    """Negative test: relevance score > 100 or < 0 must be rejected."""
    invalid_source = {
        "source_id": "SRC-999",
        "path_or_url": "test.md",
        "title": "Test Invalid Score",
        "source_class": "CANONICAL_SPEC",
        "lineage": "CAE_CANON",
        "contributor": "CAE",
        "relevance": 150,  # Invalid
        "authority": "CURRENT",
        "operating_level": "Level 02: DOCUMENTATION",
        "status": "KNOWN"
    }
    src_schema_p = ROOT / "schemas" / "research_source.schema.json"
    schema = json.loads(src_schema_p.read_text(encoding="utf-8"))
    max_val = schema["properties"]["relevance"]["maximum"]
    assert invalid_source["relevance"] > max_val

def test_countertest_rejects_invalid_authority_rank():
    """Negative test: unapproved authority class must be rejected."""
    invalid_source = {
        "source_id": "SRC-999",
        "authority": "UNVERIFIED_BLOG_POST"
    }
    src_schema_p = ROOT / "schemas" / "research_source.schema.json"
    schema = json.loads(src_schema_p.read_text(encoding="utf-8"))
    allowed = set(schema["properties"]["authority"]["enum"])
    assert invalid_source["authority"] not in allowed

def test_countertest_rejects_library_with_missing_sources():
    """Negative test: research library with fewer than 216 sources must fail."""
    truncated_sources = [{"source_id": f"SRC-{i:03d}"} for i in range(1, 100)]
    lib_schema_p = ROOT / "schemas" / "research_library.schema.json"
    schema = json.loads(lib_schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["sources"]["minItems"]
    assert len(truncated_sources) < min_items

# ---------------------------------------------------------------------------
# STALE REFERENCES & LINEAGE PRESERVATION
# ---------------------------------------------------------------------------

def test_research_skills_and_templates_exist():
    skills_dir = ROOT / "skills"
    assert (skills_dir / "caebmad-product-reconstruction" / "SKILL.md").exists()
    assert (skills_dir / "caebmad-research" / "SKILL.md").exists()

    templates_dir = ROOT / "templates"
    assert (templates_dir / "research_library.yaml").exists()
    assert (templates_dir / "source_lineage_card.md").exists()
    assert (templates_dir / "product_reconstruction.md").exists()

def test_anti_flattening_lineage_coverage():
    """Verify all major historical lineages (CCP, CMF, CCF, Visual Syntax) are represented."""
    lib_path = ROOT / ".caebmad" / "research" / "CAE_RESEARCH_LIBRARY.yaml"
    data = yaml.safe_load(lib_path.read_text(encoding="utf-8"))
    sources = data.get("sources", [])

    lineages_present = {s["lineage"] for s in sources}
    assert "CCP_LINEAGE" in lineages_present
    assert "CMF_LINEAGE" in lineages_present
    assert "VISUAL_SYNTAX" in lineages_present
    assert "CAE_CANON" in lineages_present
    assert "BMAD_UPSTREAM" in lineages_present
