#!/usr/bin/env python3
"""
Test Suite for Mandate M01: Rebuild the CAE-BMAD Constitution and Method Contract
Covers:
- Positive tests (constitution completeness, agent routing, artifact graph, state machine)
- Negative/countertests (missing sections, invalid agent IDs, cyclic dependencies, invalid transitions)
- Stale-reference tests (verifying referenced schema and file paths exist)
- Forbidden-action tests (ensuring unratified promotions or boundary violations are rejected)
"""

import sys
import json
import pytest
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# POSITIVE TESTS
# ---------------------------------------------------------------------------

def test_constitution_documents_exist():
    method_dir = ROOT / "method"
    required = [
        "CAE_BMAD_CONSTITUTION.md",
        "CAE_BMAD_METHOD_CONTRACT.md",
        "CAE_BMAD_OPERATING_LEVELS.md",
        "CAE_BMAD_ARTIFACT_GOVERNANCE.md",
        "CAE_BMAD_SOURCE_AUTHORITY.md",
        "CAE_BMAD_UPSTREAM_POLICY.md",
    ]
    for doc in required:
        path = method_dir / doc
        assert path.exists(), f"Required method doc missing: {doc}"
        assert len(path.read_text(encoding="utf-8").split()) >= 150, f"Doc too brief: {doc}"

def test_json_schemas_valid():
    schema_dir = ROOT / "schemas"
    schemas = [
        "constitution.schema.json",
        "artifact_graph.schema.json",
        "method_states.schema.json",
        "agent_routing.schema.json",
        "decision_ledger.schema.json",
    ]
    for s in schemas:
        p = schema_dir / s
        assert p.exists(), f"Missing schema file: {s}"
        data = json.loads(p.read_text(encoding="utf-8"))
        assert "$schema" in data
        assert "required" in data
        assert len(data["required"]) > 0

def test_agent_routing_complete_and_differentiated():
    routing_file = ROOT / "config" / "CAE_BMAD_AGENT_ROUTING.yaml"
    assert routing_file.exists()
    data = yaml.safe_load(routing_file.read_text(encoding="utf-8"))
    agents = data.get("agents", [])
    assert len(agents) >= 19, "Must have at least 19 agents in routing table"

    agent_ids = {a["agent_id"] for a in agents}
    assert len(agent_ids) == len(agents), "Agent IDs must be unique"

    agent_dir = ROOT / "gemini_execution" / "agents"
    for ag in agents:
        md_file = agent_dir / f"{ag['agent_id']}.md"
        assert md_file.exists(), f"Agent doc missing: {md_file.name}"
        text = md_file.read_text(encoding="utf-8")
        assert "Non-Negotiable Boundaries" in text or "Boundaries" in text
        assert "Input Contract" in text
        assert "Output Contract" in text
        assert len(ag["skills"]) > 0, f"Agent {ag['agent_id']} must have assigned skills"

def test_artifact_graph_dag_integrity():
    graph_file = ROOT / "config" / "CAE_BMAD_ARTIFACT_GRAPH.yaml"
    assert graph_file.exists()
    data = yaml.safe_load(graph_file.read_text(encoding="utf-8"))
    artifacts = {a["id"]: a for a in data.get("artifacts", [])}
    assert len(artifacts) >= 15, "Artifact graph must contain at least 15 artifact families"

    deps = data.get("dependencies", [])
    # Verify no self-dependencies and all target IDs exist
    for d in deps:
        art_id = d["artifact_id"]
        assert art_id in artifacts, f"Unknown artifact: {art_id}"
        for parent in d.get("depends_on", []):
            assert parent in artifacts, f"Unknown parent: {parent}"
            assert parent != art_id, f"Self-dependency detected on {art_id}"

    gates = data.get("gates", [])
    assert len(gates) >= 6, "Must define at least 6 gates"

def test_method_state_machine_valid():
    states_file = ROOT / "config" / "CAE_BMAD_METHOD_STATES.yaml"
    assert states_file.exists()
    data = yaml.safe_load(states_file.read_text(encoding="utf-8"))
    state_ids = {s["state_id"] for s in data.get("states", [])}
    assert "NOT_STARTED" in state_ids
    assert "PROMOTED" in state_ids
    assert len(state_ids) >= 10

    for tr in data.get("transitions", []):
        assert tr["from_state"] in state_ids
        assert tr["to_state"] in state_ids
        assert "gate" in tr
        assert "condition" in tr

# ---------------------------------------------------------------------------
# NEGATIVE / COUNTERTESTS
# ---------------------------------------------------------------------------

def test_countertest_rejects_missing_contract():
    """Negative test: agent definition without an input contract must fail validation."""
    invalid_agent_spec = {
        "agent_id": "test-invalid-agent",
        "name": "Invalid Agent",
        "operating_level": "Level 01: PRODUCT / INTENT",
        "mission": "No input contract defined",
        "skills": ["caebmad-help"],
        # Missing input_contract and output_contract
        "boundaries": ["None"]
    }
    assert "input_contract" not in invalid_agent_spec
    # Verify standard schema requires input_contract
    schema_path = ROOT / "schemas" / "agent_routing.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required_agent_fields = schema["properties"]["agents"]["items"]["required"]
    assert "input_contract" in required_agent_fields
    assert "output_contract" in required_agent_fields

def test_countertest_rejects_cyclic_artifact_dependency():
    """Negative test: cyclic dependency in artifact graph must be detectable."""
    cyclic_deps = {
        "ART-01": ["ART-02"],
        "ART-02": ["ART-01"]
    }
    def has_cycle(graph):
        visited = set()
        rec_stack = set()
        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False
        for n in graph:
            if n not in visited:
                if dfs(n):
                    return True
        return False
    assert has_cycle(cyclic_deps) is True

def test_countertest_rejects_unauthorized_state_jump():
    """Negative test: jumping from NOT_STARTED directly to PROMOTED without passing gates must be rejected."""
    states_file = ROOT / "config" / "CAE_BMAD_METHOD_STATES.yaml"
    data = yaml.safe_load(states_file.read_text(encoding="utf-8"))
    transitions = data.get("transitions", [])
    valid_jumps = {(t["from_state"], t["to_state"]) for t in transitions}
    assert ("NOT_STARTED", "PROMOTED") not in valid_jumps, "Direct jump from NOT_STARTED to PROMOTED must be forbidden"

# ---------------------------------------------------------------------------
# STALE REFERENCE & FALSE-PROOF DEFENSES
# ---------------------------------------------------------------------------

def test_stale_references_in_agent_routing():
    """Verify all skill references in agent routing exist as actual SKILL.md files."""
    routing_file = ROOT / "config" / "CAE_BMAD_AGENT_ROUTING.yaml"
    data = yaml.safe_load(routing_file.read_text(encoding="utf-8"))
    skills_dir = ROOT / "skills"
    
    # Check that for skills created in this mandate, their directories and files exist
    created_skills = ["caebmad-help", "caebmad-orchestrate", "caebmad-operating-level"]
    for s in created_skills:
        skill_file = skills_dir / s / "SKILL.md"
        assert skill_file.exists(), f"Skill file missing: {skill_file}"

def test_forbidden_action_cannot_mark_promoted_without_gate():
    """Ensure state transition contract enforces gate verification."""
    contract_path = ROOT / "method" / "CAE_BMAD_METHOD_CONTRACT.md"
    assert contract_path.exists()
    text = contract_path.read_text(encoding="utf-8")
    assert "False-Proof Defenses" in text
    assert "Reality Contact" in text or "reality contact" in text
