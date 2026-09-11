#!/usr/bin/env python3
"""
Test Suite for Mandate M06: Rebuild the CAE Agent / Workflow / Factory Intelligence
Covers:
- Positive tests (Agent Architecture Map covers 19 agents, Workflow Factory Map covers primitives & pipelines)
- Negative/countertests (truncated agent count, missing rollback strategy, missing communication matrix)
- Stale reference tests (skills, templates, workflows, and scripts exist on disk)
- False-proof defenses (agent boundaries must be non-empty, pipelines must have rollback policies)
"""

import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# POSITIVE TESTS
# ---------------------------------------------------------------------------

def test_agent_architecture_map_exists_and_covers_all_19_agents():
    json_path = ROOT / "docs" / "cae-bmad" / "02_investigation" / "AGENT_ARCHITECTURE_MAP.json"
    md_path = ROOT / "docs" / "cae-bmad" / "02_investigation" / "AGENT_ARCHITECTURE_MAP.md"
    assert json_path.exists(), f"Missing agent map json: {json_path}"
    assert md_path.exists(), f"Missing agent map md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    agents = data.get("agents", [])
    assert len(agents) >= 19, f"Expected at least 19 agents, found {len(agents)}"

    agent_ids = {a["agent_id"] for a in agents}
    assert "cae-method-orchestrator" in agent_ids
    assert "cae-agent-systems-analyst" in agent_ids
    assert "cae-workflow-factory-analyst" in agent_ids
    assert "cae-adversarial-reviewer" in agent_ids

    for a in agents:
        assert len(a["assigned_skills"]) >= 1
        assert len(a["boundary_statement"]) >= 10

def test_workflow_factory_map_exists_and_valid():
    json_path = ROOT / "docs" / "cae-bmad" / "02_investigation" / "WORKFLOW_FACTORY_MAP.json"
    md_path = ROOT / "docs" / "cae-bmad" / "02_investigation" / "WORKFLOW_FACTORY_MAP.md"
    assert json_path.exists(), f"Missing workflow map json: {json_path}"
    assert md_path.exists(), f"Missing workflow map md: {md_path}"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    prims = data.get("factory_primitives", [])
    assert len(prims) >= 3, f"Expected at least 3 primitives, found {len(prims)}"

    pipes = data.get("pipelines", [])
    assert len(pipes) >= 4, f"Expected at least 4 pipelines, found {len(pipes)}"

    for p in pipes:
        assert "pipeline_id" in p
        assert len(p["steps"]) >= 1
        assert len(p["rollback_strategy"]) >= 10

def test_m06_schemas_valid():
    a_schema_p = ROOT / "schemas" / "agent_system_architecture.schema.json"
    w_schema_p = ROOT / "schemas" / "workflow_factory_map.schema.json"
    assert a_schema_p.exists()
    assert w_schema_p.exists()

    a_schema = json.loads(a_schema_p.read_text(encoding="utf-8"))
    w_schema = json.loads(w_schema_p.read_text(encoding="utf-8"))

    assert "agents" in a_schema["required"]
    assert "pipelines" in w_schema["required"]
    assert "factory_primitives" in w_schema["required"]

# ---------------------------------------------------------------------------
# NEGATIVE / COUNTERTESTS
# ---------------------------------------------------------------------------

def test_countertest_rejects_truncated_agent_count():
    """Schema requires at least 19 agents."""
    schema_p = ROOT / "schemas" / "agent_system_architecture.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["agents"]["minItems"]
    assert min_items >= 19

    truncated = [{"agent_id": "cae-dummy"}]
    assert len(truncated) < min_items

def test_countertest_rejects_pipeline_without_rollback():
    """Schema requires rollback_strategy with minLength 10."""
    schema_p = ROOT / "schemas" / "workflow_factory_map.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    pipe_props = schema["properties"]["pipelines"]["items"]["properties"]
    assert pipe_props["rollback_strategy"]["minLength"] >= 10

def test_countertest_rejects_empty_communication_matrix():
    """Schema requires communication_matrix with minItems 1."""
    schema_p = ROOT / "schemas" / "agent_system_architecture.schema.json"
    schema = json.loads(schema_p.read_text(encoding="utf-8"))
    min_items = schema["properties"]["communication_matrix"]["minItems"]
    assert min_items >= 1

# ---------------------------------------------------------------------------
# STALE REFERENCES & SCRIPT INTEGRITY
# ---------------------------------------------------------------------------

def test_m06_scripts_skills_templates_workflows_exist():
    skills_dir = ROOT / "skills"
    assert (skills_dir / "caebmad-agent-architecture" / "SKILL.md").exists()
    assert (skills_dir / "caebmad-workflow-factory" / "SKILL.md").exists()

    templates_dir = ROOT / "templates"
    assert (templates_dir / "agent_architecture_map.md").exists()
    assert (templates_dir / "workflow_factory_map.md").exists()

    workflows_dir = ROOT / "workflows"
    assert (workflows_dir / "caebmad_m06_agent_workflow_factory_workflow.yaml").exists()

    scripts_dir = ROOT / "scripts"
    assert (scripts_dir / "generate_agent_workflow_factory_maps.py").exists()
    assert (scripts_dir / "validate_agent_workflow_factory_system.py").exists()
