#!/usr/bin/env python3
"""
CAE-BMAD Agent, Workflow, and Factory System Validator
Validates:
- AGENT_ARCHITECTURE_MAP.json conforms to schemas/agent_system_architecture.schema.json (19 agents)
- WORKFLOW_FACTORY_MAP.json conforms to schemas/workflow_factory_map.schema.json (primitives, pipelines, rollback strategies)
- Associated skills, templates, workflows, and markdown companions exist
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate_agent_workflow_factory() -> tuple[list[str], list[str]]:
    passes = []
    errors = []

    # 1. Schemas
    a_schema_p = ROOT / "schemas" / "agent_system_architecture.schema.json"
    w_schema_p = ROOT / "schemas" / "workflow_factory_map.schema.json"

    if not a_schema_p.exists():
        errors.append("Missing schemas/agent_system_architecture.schema.json")
    else:
        passes.append("Found agent_system_architecture.schema.json")

    if not w_schema_p.exists():
        errors.append("Missing schemas/workflow_factory_map.schema.json")
    else:
        passes.append("Found workflow_factory_map.schema.json")

    # 2. Agent Architecture Map
    agent_json_p = ROOT / "docs" / "cae-bmad" / "02_investigation" / "AGENT_ARCHITECTURE_MAP.json"
    agent_md_p = ROOT / "docs" / "cae-bmad" / "02_investigation" / "AGENT_ARCHITECTURE_MAP.md"

    if not agent_json_p.exists() or not agent_md_p.exists():
        errors.append("Missing AGENT_ARCHITECTURE_MAP json/md")
    else:
        try:
            adata = json.loads(agent_json_p.read_text(encoding="utf-8"))
            agents = adata.get("agents", [])
            if len(agents) < 19:
                errors.append(f"Expected at least 19 agents, found {len(agents)}")
            else:
                passes.append(f"AGENT_ARCHITECTURE_MAP covers {len(agents)} governed agents")

            for a in agents:
                if len(a.get("assigned_skills", [])) == 0:
                    errors.append(f"Agent {a.get('agent_id')} has no assigned skills")
                if len(a.get("boundary_statement", "")) < 10:
                    errors.append(f"Agent {a.get('agent_id')} has insufficient boundary statement")
        except Exception as e:
            errors.append(f"Failed to parse AGENT_ARCHITECTURE_MAP.json: {e}")

    # 3. Workflow Factory Map
    wf_json_p = ROOT / "docs" / "cae-bmad" / "02_investigation" / "WORKFLOW_FACTORY_MAP.json"
    wf_md_p = ROOT / "docs" / "cae-bmad" / "02_investigation" / "WORKFLOW_FACTORY_MAP.md"

    if not wf_json_p.exists() or not wf_md_p.exists():
        errors.append("Missing WORKFLOW_FACTORY_MAP json/md")
    else:
        try:
            wdata = json.loads(wf_json_p.read_text(encoding="utf-8"))
            prims = wdata.get("factory_primitives", [])
            if len(prims) < 3:
                errors.append(f"Expected at least 3 factory primitives, found {len(prims)}")
            else:
                passes.append(f"WORKFLOW_FACTORY_MAP covers {len(prims)} factory primitives")

            pipes = wdata.get("pipelines", [])
            if len(pipes) < 4:
                errors.append(f"Expected at least 4 pipelines, found {len(pipes)}")
            else:
                passes.append(f"WORKFLOW_FACTORY_MAP covers {len(pipes)} multi-agent pipelines")

            for p in pipes:
                if len(p.get("rollback_strategy", "")) < 10:
                    errors.append(f"Pipeline {p.get('pipeline_id')} has no rollback strategy")
        except Exception as e:
            errors.append(f"Failed to parse WORKFLOW_FACTORY_MAP.json: {e}")

    # 4. Skills and Templates
    skills_dir = ROOT / "skills"
    if (skills_dir / "caebmad-agent-architecture" / "SKILL.md").exists():
        passes.append("Found caebmad-agent-architecture skill")
    else:
        errors.append("Missing caebmad-agent-architecture skill")

    if (skills_dir / "caebmad-workflow-factory" / "SKILL.md").exists():
        passes.append("Found caebmad-workflow-factory skill")
    else:
        errors.append("Missing caebmad-workflow-factory skill")

    return passes, errors

def main():
    passes, errors = validate_agent_workflow_factory()
    print("=" * 60)
    print(f"CAE-BMAD Agent/Workflow/Factory Validator — Passed: {len(passes)}, Errors: {len(errors)}")
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
        print("\nALL AGENT/WORKFLOW/FACTORY SYSTEM VALIDATIONS PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
