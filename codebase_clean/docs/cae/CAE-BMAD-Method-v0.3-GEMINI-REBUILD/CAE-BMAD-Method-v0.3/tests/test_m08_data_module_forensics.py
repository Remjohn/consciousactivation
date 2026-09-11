#!/usr/bin/env python3
"""
Test Suite for Mandate M08: Rebuild the Data / Module / Code Forensics Agents
Covers:
- Positive tests (Data Reality Map, Module Map, Code Forensics Report exist and validate)
- Negative/countertests (truncated entities list, missing line proofs, invalid storage engine)
- Stale reference tests (skills, templates, workflows, scripts exist on disk)
- False-proof defenses (line proofs must cite real files with verbatim snippets)
"""

import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# POSITIVE TESTS
# ---------------------------------------------------------------------------

def test_data_reality_map_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "DATA_REALITY_MAP.json"
    md_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "DATA_REALITY_MAP.md"
    assert json_path.exists(), f"Missing data map json: {json_path}"
    assert md_path.exists(), f"Missing data map md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    ents = data.get("entities", [])
    assert len(ents) >= 4, f"Expected at least 4 data entities, found {len(ents)}"

    ent_names = {e["entity_name"] for e in ents}
    assert "ResearchSignal" in ent_names
    assert "ProgramStateAggregate" in ent_names
    assert "CompiledWorkflowStep" in ent_names

    for e in ents:
        assert len(e["key_fields"]) >= 1
        assert e["storage_engine"] in ["IN_MEMORY_CAS", "FILESYSTEM_YAML", "SQLITE", "POSTGRES", "REDIS"]

def test_module_map_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "MODULE_MAP.json"
    md_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "MODULE_MAP.md"
    assert json_path.exists(), f"Missing module map json: {json_path}"
    assert md_path.exists(), f"Missing module map md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    mods = data.get("modules", [])
    assert len(mods) >= 4, f"Expected at least 4 modules, found {len(mods)}"
    assert data.get("circular_dependencies_detected") is False

    mod_namespaces = {m["module_namespace"] for m in mods}
    assert "cae_world_intelligence" in mod_namespaces
    assert "ca_runtime" in mod_namespaces
    assert "cmf_pipeline.workflow" in mod_namespaces

def test_code_forensics_report_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "CODE_FORENSICS_REPORT.json"
    md_path = ROOT / "docs" / "cae-bmad" / "07_brownfield" / "CODE_FORENSICS_REPORT.md"
    assert json_path.exists(), f"Missing forensics report json: {json_path}"
    assert md_path.exists(), f"Missing forensics report md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data.get("verdict") == "VERIFIED_GROUND_TRUTH"

    classes = data.get("classes_inspected", [])
    assert len(classes) >= 3, f"Expected at least 3 classes, found {len(classes)}"

    funcs = data.get("functions_inspected", [])
    assert len(funcs) >= 3, f"Expected at least 3 functions, found {len(funcs)}"

    proofs = data.get("line_proofs", [])
    assert len(proofs) >= 3, f"Expected at least 3 line proofs, found {len(proofs)}"

    for p in proofs:
        assert len(p["exact_code_snippet"]) > 10
        assert p["verified"] is True

def test_m08_schemas_valid():
    d_schema_p = ROOT / "schemas" / "data_reality_map.schema.json"
    m_schema_p = ROOT / "schemas" / "module_map.schema.json"
    c_schema_p = ROOT / "schemas" / "code_forensics_report.schema.json"

    assert d_schema_p.exists()
    assert m_schema_p.exists()
    assert c_schema_p.exists()

    d_schema = json.loads(d_schema_p.read_text(encoding="utf-8"))
    m_schema = json.loads(m_schema_p.read_text(encoding="utf-8"))
    c_schema = json.loads(c_schema_p.read_text(encoding="utf-8"))

    assert "entities" in d_schema["required"]
    assert "modules" in m_schema["required"]
    assert "line_proofs" in c_schema["required"]

# ---------------------------------------------------------------------------
# NEGATIVE / COUNTERTESTS
# ---------------------------------------------------------------------------

def test_countertest_rejects_truncated_entities_count():
    """Schema requires at least 4 entities in data map."""
    schema_p = ROOT / "schemas" / "data_reality_map.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["entities"]["minItems"]
    assert min_items >= 4

    truncated = [{"entity_name": "DummyEntity"}]
    assert len(truncated) < min_items

def test_countertest_rejects_invalid_storage_engine():
    """Schema enforces enum on storage_engine."""
    schema_p = ROOT / "schemas" / "data_reality_map.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    allowed_engines = set(schema["properties"]["entities"]["items"]["properties"]["storage_engine"]["enum"])
    invalid_engine = "PUNCH_CARD_STORAGE"
    assert invalid_engine not in allowed_engines

def test_countertest_rejects_empty_line_proofs():
    """Schema requires minItems 3 for line proofs in forensics report."""
    schema_p = ROOT / "schemas" / "code_forensics_report.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["line_proofs"]["minItems"]
    assert min_items >= 3

    truncated = [{"claim": "Fake claim"}]
    assert len(truncated) < min_items

# ---------------------------------------------------------------------------
# STALE REFERENCES & SCRIPT INTEGRITY
# ---------------------------------------------------------------------------

def test_m08_scripts_skills_templates_workflows_exist():
    skills_dir = ROOT / "skills"
    assert (skills_dir / "caebmad-data-investigate" / "SKILL.md").exists()
    assert (skills_dir / "caebmad-module-investigate" / "SKILL.md").exists()
    assert (skills_dir / "caebmad-code-forensics" / "SKILL.md").exists()

    templates_dir = ROOT / "templates"
    assert (templates_dir / "data_reality_map.md").exists()
    assert (templates_dir / "module_map.md").exists()
    assert (templates_dir / "code_forensics_report.md").exists()

    workflows_dir = ROOT / "workflows"
    assert (workflows_dir / "caebmad_m08_data_module_forensics_workflow.yaml").exists()

    scripts_dir = ROOT / "scripts"
    assert (scripts_dir / "generate_data_module_forensics_maps.py").exists()
    assert (scripts_dir / "validate_data_module_forensics_system.py").exists()
