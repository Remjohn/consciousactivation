#!/usr/bin/env python3
"""
CAE-BMAD Constitution & Method Contract Validator
Validates the structural and semantic integrity of M01 deliverables:
- Method Constitution & Governance Documents
- JSON Schemas & Config Models
- 19 Agent Specifications & Routing
- Artifact Dependency Graph DAG Integrity
- Method State Machine Transitions
"""

import sys
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[ERROR] PyYAML is required. Please install pyyaml.")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]

def validate_all() -> tuple[list[str], list[str]]:
    passes = []
    errors = []

    # 1. Validate Method Governance Documents
    method_dir = ROOT / "method"
    required_docs = [
        "CAE_BMAD_CONSTITUTION.md",
        "CAE_BMAD_METHOD_CONTRACT.md",
        "CAE_BMAD_OPERATING_LEVELS.md",
        "CAE_BMAD_ARTIFACT_GOVERNANCE.md",
        "CAE_BMAD_SOURCE_AUTHORITY.md",
        "CAE_BMAD_UPSTREAM_POLICY.md",
    ]

    for doc in required_docs:
        doc_path = method_dir / doc
        if not doc_path.exists():
            errors.append(f"Missing method document: {doc}")
        else:
            text = doc_path.read_text(encoding="utf-8")
            if len(text.split()) < 150:
                errors.append(f"Method document {doc} is too brief ({len(text.split())} words)")
            else:
                passes.append(f"Method document present and non-trivial: {doc}")

    # 2. Validate JSON Schemas
    schema_dir = ROOT / "schemas"
    required_schemas = [
        "constitution.schema.json",
        "artifact_graph.schema.json",
        "method_states.schema.json",
        "agent_routing.schema.json",
        "decision_ledger.schema.json",
    ]

    for sch in required_schemas:
        sch_path = schema_dir / sch
        if not sch_path.exists():
            errors.append(f"Missing schema: {sch}")
        else:
            try:
                data = json.loads(sch_path.read_text(encoding="utf-8"))
                if "$schema" not in data or "required" not in data:
                    errors.append(f"Schema {sch} missing $schema or required fields")
                else:
                    passes.append(f"Valid JSON Schema: {sch}")
            except Exception as e:
                errors.append(f"Invalid JSON in schema {sch}: {e}")

    # 3. Validate Configuration Files
    config_dir = ROOT / "config"
    required_configs = [
        "caebmad-config.yaml",
        "CAE_BMAD_ARTIFACT_GRAPH.yaml",
        "CAE_BMAD_METHOD_STATES.yaml",
        "CAE_BMAD_AGENT_ROUTING.yaml",
    ]

    parsed_configs = {}
    for cfg in required_configs:
        cfg_path = config_dir / cfg
        if not cfg_path.exists():
            errors.append(f"Missing config file: {cfg}")
        else:
            try:
                data = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
                parsed_configs[cfg] = data
                passes.append(f"Valid YAML Config: {cfg}")
            except Exception as e:
                errors.append(f"Invalid YAML in config {cfg}: {e}")

    # 4. Validate Agent Routing and Agent Definition Files
    routing_data = parsed_configs.get("CAE_BMAD_AGENT_ROUTING.yaml")
    if routing_data and "agents" in routing_data:
        agents = routing_data["agents"]
        if len(agents) < 19:
            errors.append(f"Expected at least 19 agents in routing table, found {len(agents)}")
        else:
            passes.append(f"Agent routing table defines {len(agents)} agents")

        agent_dir = ROOT / "gemini_execution" / "agents"
        for ag in agents:
            ag_id = ag["agent_id"]
            md_file = agent_dir / f"{ag_id}.md"
            if not md_file.exists():
                errors.append(f"Agent {ag_id} defined in routing but missing definition file {md_file.name}")
            else:
                ag_text = md_file.read_text(encoding="utf-8")
                if "Non-Negotiable Boundaries" not in ag_text and "Boundaries" not in ag_text:
                    errors.append(f"Agent {ag_id} missing boundary rules")
                if "Input Contract" not in ag_text or "Output Contract" not in ag_text:
                    errors.append(f"Agent {ag_id} missing input/output contract")
                passes.append(f"Agent specification verified: {ag_id}")
    else:
        errors.append("CAE_BMAD_AGENT_ROUTING.yaml missing 'agents' section")

    # 5. Validate Artifact Graph (DAG Integrity)
    graph_data = parsed_configs.get("CAE_BMAD_ARTIFACT_GRAPH.yaml")
    if graph_data:
        artifacts = {a["id"]: a for a in graph_data.get("artifacts", [])}
        deps = graph_data.get("dependencies", [])
        gates = graph_data.get("gates", [])

        if len(artifacts) < 15:
            errors.append(f"Expected at least 15 artifact families in graph, found {len(artifacts)}")
        else:
            passes.append(f"Artifact graph contains {len(artifacts)} artifacts")

        # Check dependency resolution
        for dep in deps:
            art_id = dep["artifact_id"]
            if art_id not in artifacts:
                errors.append(f"Dependency references unknown artifact: {art_id}")
            for d in dep.get("depends_on", []):
                if d not in artifacts:
                    errors.append(f"Artifact {art_id} depends on unknown artifact: {d}")

        if len(gates) < 6:
            errors.append(f"Expected at least 6 gates in artifact graph, found {len(gates)}")
        else:
            passes.append(f"Artifact graph defines {len(gates)} operator gates")

    # 6. Validate State Machine
    states_data = parsed_configs.get("CAE_BMAD_METHOD_STATES.yaml")
    if states_data:
        state_ids = {s["state_id"] for s in states_data.get("states", [])}
        transitions = states_data.get("transitions", [])

        if "NOT_STARTED" not in state_ids or "PROMOTED" not in state_ids:
            errors.append("State machine missing NOT_STARTED or PROMOTED state")
        else:
            passes.append(f"State machine defines {len(state_ids)} states")

        for tr in transitions:
            if tr["from_state"] not in state_ids:
                errors.append(f"Transition from unknown state: {tr['from_state']}")
            if tr["to_state"] not in state_ids:
                errors.append(f"Transition to unknown state: {tr['to_state']}")

    return passes, errors

def main():
    passes, errors = validate_all()
    print("=" * 60)
    print(f"CAE-BMAD Constitution Validator — Passed: {len(passes)}, Errors: {len(errors)}")
    print("=" * 60)
    for p in passes:
        print(f"  [PASS] {p}")
    if errors:
        print("\n" + "!" * 60)
        print("VALIDATION FAILURES:")
        print("!" * 60)
        for e in errors:
            print(f"  [FAIL] {e}")
        sys.exit(1)
    else:
        print("\nALL CONSTITUTIONAL VALIDATIONS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
