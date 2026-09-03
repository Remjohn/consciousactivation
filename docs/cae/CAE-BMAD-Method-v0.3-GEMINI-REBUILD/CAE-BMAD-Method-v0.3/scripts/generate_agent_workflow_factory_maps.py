#!/usr/bin/env python3
"""
CAE-BMAD Agent, Workflow, and Factory Map Generator
Generates:
- AGENT_ARCHITECTURE_MAP.json and .md (mapping all 19 governed agents)
- WORKFLOW_FACTORY_MAP.json and .md (mapping factory primitives, pipelines, ADWs, rollback policies)
Emits to docs/cae-bmad/02_investigation/
"""

import sys
import json
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("[ERROR] PyYAML is required.")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]

def build_agent_map() -> dict:
    agents_dir = ROOT / "gemini_execution" / "agents"
    agent_files = sorted(agents_dir.glob("cae-*.md"))

    agents = []
    for af in agent_files:
        aid = af.stem
        content = af.read_text(encoding="utf-8")
        lines = content.splitlines()

        # Parse basic fields
        name = aid.replace("cae-", "").replace("-", " ").title()
        level = "PRODUCT / INTENT"
        skills = ["caebmad-operating-level"]
        boundary = "Must NOT exceed delegated authority or assume operator constitutional control."

        for line in lines:
            if line.startswith("# "):
                name = line.replace("# ", "").strip()
            elif "Level " in line and ("Primary Operating Level" in line or line.startswith("`Level ")):
                level = line.strip("` ").replace("## Primary Operating Level", "").strip()
            elif line.strip().startswith("- `caebmad-"):
                s = line.strip().strip("- `").strip("`")
                if s not in skills:
                    skills.append(s)
            elif "Must NOT " in line:
                boundary = line.strip("- ").strip()

        agents.append({
            "agent_id": aid,
            "name": name,
            "primary_operating_level": level,
            "assigned_skills": skills,
            "input_contract": ["Governed markdown and YAML artifacts", "Operating level context"],
            "output_contract": ["Typed JSON and markdown deliverables", "Investigation/audit traces"],
            "boundary_statement": boundary
        })

    boundary_rules = [
        "No autonomous agent may promote an artifact to PROMOTED status without explicit Operator Gate ratification.",
        "Every agent must execute within its assigned operating level and record descent/ascent steps when crossing boundaries.",
        "Tool permissions are strictly bounded; destructive operations require human-in-the-loop authorization."
    ]

    comm_matrix = [
        {
            "source_agent": "cae-method-orchestrator",
            "target_agent": "cae-product-reconstructor",
            "protocol": "WORKFLOW_INVOCATION",
            "validation_contract": "schemas/product_reconstruction.schema.json"
        },
        {
            "source_agent": "cae-product-reconstructor",
            "target_agent": "cae-prd-agent",
            "protocol": "ARTIFACT_HANDOFF",
            "validation_contract": "schemas/prd_module.schema.json"
        },
        {
            "source_agent": "cae-prd-agent",
            "target_agent": "cae-delivery-agent",
            "protocol": "ARTIFACT_HANDOFF",
            "validation_contract": "schemas/epic_story.schema.json"
        },
        {
            "source_agent": "cae-method-orchestrator",
            "target_agent": "cae-adversarial-reviewer",
            "protocol": "REVIEW_REQUEST",
            "validation_contract": "schemas/constitution.schema.json"
        }
    ]

    agent_map = {
        "artifact_id": "CAE-ART-AAM-001",
        "status": "APPROVED",
        "generated_date": datetime.now().isoformat(),
        "total_agents": len(agents),
        "agents": agents,
        "boundary_rules": boundary_rules,
        "communication_matrix": comm_matrix
    }
    return agent_map

def build_workflow_map() -> dict:
    primitives = [
        {
            "primitive_id": "PRIM-01",
            "name": "JIT Context Capsule Assembler",
            "description": "Assembles minimal token-efficient context packets containing only active schemas, lineage cards, and upstream inputs.",
            "runtime_binding": "packages/ca_runtime/src/ca_runtime/agent_invocation.py"
        },
        {
            "primitive_id": "PRIM-02",
            "name": "Deterministic Step Scheduler",
            "description": "Advances workflow state machines sequentially only upon schema verification of output artifacts.",
            "runtime_binding": "services/pipeline/src/cmf_pipeline/workflow/application/compiler.py"
        },
        {
            "primitive_id": "PRIM-03",
            "name": "Compare-And-Swap State CAS Runtime",
            "description": "Guarantees atomic, optimistic locking state mutations preventing race conditions across multi-agent execution.",
            "runtime_binding": "packages/ca_runtime/src/ca_runtime/program_state_runtime.py"
        }
    ]

    pipelines = [
        {
            "pipeline_id": "PIPE-M01",
            "name": "Constitution and Method Contract Rebuild",
            "trigger": "Gemini Activation Prompt M01",
            "steps": [
                {"step_number": 1, "agent": "cae-method-orchestrator", "action": "Author Constitution & Governance", "output_artifact": "CAE_BMAD_CONSTITUTION.md"},
                {"step_number": 2, "agent": "cae-adversarial-reviewer", "action": "Run Countertests & Boundary Checks", "output_artifact": "OPERATOR_GATE_M01.md"}
            ],
            "terminal_condition": "All 10 M01 tests pass and operator approves gate.",
            "rollback_strategy": "Quarantine generated schemas and revert to baseline constitution stubs."
        },
        {
            "pipeline_id": "PIPE-M02",
            "name": "216-Source Research Library Intake",
            "trigger": "Gemini Activation Prompt M02",
            "steps": [
                {"step_number": 1, "agent": "cae-product-reconstructor", "action": "Ingest 216 Sources and Score Relevance", "output_artifact": "CAE_RESEARCH_LIBRARY.yaml"},
                {"step_number": 2, "agent": "cae-adversarial-reviewer", "action": "Verify Anti-Flattening Invariants", "output_artifact": "OPERATOR_GATE_M02.md"}
            ],
            "terminal_condition": "Exact 216 sources validated against schema with zero unclassified sources.",
            "rollback_strategy": "Purge .caebmad/research/ output and reload 144-source baseline catalog."
        },
        {
            "pipeline_id": "PIPE-M03",
            "name": "Multi-Level Engineering Investigation",
            "trigger": "Gemini Activation Prompt M03",
            "steps": [
                {"step_number": 1, "agent": "cae-documentation-analyst", "action": "Scan 13 Operating Levels", "output_artifact": "OPERATING_LEVEL_ASSESSMENT.json"},
                {"step_number": 2, "agent": "cae-brownfield-auditor", "action": "Identify Code Drift and Broken References", "output_artifact": "OPERATOR_GATE_M03.md"}
            ],
            "terminal_condition": "All 13 levels evaluated with concrete filesystem evidence paths.",
            "rollback_strategy": "Revert assessment deliverables to DRAFT status and log investigation errors."
        },
        {
            "pipeline_id": "PIPE-M04",
            "name": "Product Intent and Lineage Reconstruction",
            "trigger": "Gemini Activation Prompt M04",
            "steps": [
                {"step_number": 1, "agent": "cae-product-reconstructor", "action": "Synthesize 5 Capability Pillars", "output_artifact": "PRODUCT_RECONSTRUCTION.json"},
                {"step_number": 2, "agent": "cae-brownfield-auditor", "action": "Map Brownfield Code Crosswalks", "output_artifact": "OPERATOR_GATE_M04.md"}
            ],
            "terminal_condition": "All 5 Capability Pillars defined with verified code paths and 216 sources analyzed.",
            "rollback_strategy": "Revert reconstruction record and re-evaluate capability pillar extraction."
        }
    ]

    adw_patterns = [
        {
            "pattern_id": "ADW-SSSF",
            "name": "Single-Step Software Factory (SSSF)",
            "description": "Deterministic step execution pattern where an agent receives a strictly typed context capsule and produces an audited artifact.",
            "jit_capsule_strategy": "Inject only target schema, input artifact, and specific operating level boundaries."
        },
        {
            "pattern_id": "ADW-ADV-LOOP",
            "name": "Adversarial Review Loop",
            "description": "Two-agent pattern where a generator agent's output is subjected to countertests and false-proof defenses by cae-adversarial-reviewer.",
            "jit_capsule_strategy": "Inject generated artifact, countertest rules, and constitutional boundary checks."
        }
    ]

    recovery_matrix = [
        {
            "error_type": "SCHEMA_VALIDATION_ERROR",
            "detection_agent": "cae-method-orchestrator",
            "recovery_action": "Reject artifact, emit error diagnostics, retry with corrected parameters.",
            "operator_escalation": False
        },
        {
            "error_type": "CONTRADICTION_UNRESOLVED",
            "detection_agent": "cae-adversarial-reviewer",
            "recovery_action": "Log in Decision Ledger, halt pipeline, generate Operator Gate packet.",
            "operator_escalation": True
        },
        {
            "error_type": "INFINITE_DESCENT_LOOP",
            "detection_agent": "cae-brownfield-auditor",
            "recovery_action": "Circuit-breaker abort, log WORKFLOW_UNDER_SPECIFIED, return to parent level.",
            "operator_escalation": False
        }
    ]

    wf_map = {
        "artifact_id": "CAE-ART-WFM-001",
        "status": "APPROVED",
        "generated_date": datetime.now().isoformat(),
        "factory_primitives": primitives,
        "pipelines": pipelines,
        "adw_patterns": adw_patterns,
        "error_recovery_matrix": recovery_matrix
    }
    return wf_map

def main():
    out_dir = ROOT / "docs" / "cae-bmad" / "02_investigation"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Agent Map
    agent_map = build_agent_map()
    agent_json_p = out_dir / "AGENT_ARCHITECTURE_MAP.json"
    with open(agent_json_p, "w", encoding="utf-8") as f:
        json.dump(agent_map, f, indent=2)

    agent_md_p = out_dir / "AGENT_ARCHITECTURE_MAP.md"
    with open(agent_md_p, "w", encoding="utf-8") as f:
        f.write("# Agent System Architecture Map\n\n")
        f.write(f"**Artifact ID:** {agent_map['artifact_id']}  \n")
        f.write(f"**Status:** {agent_map['status']}  \n")
        f.write(f"**Total Governed Agents:** {agent_map['total_agents']}  \n")
        f.write(f"**Generated Date:** {agent_map['generated_date']}  \n\n")
        f.write("---\n\n## 1. Governed Agent Inventory\n\n")
        f.write("| # | Agent ID | Role Name | Primary Level | Assigned Skills | Boundaries |\n")
        f.write("|---|---|---|---|---|---|\n")
        for idx, a in enumerate(agent_map["agents"], start=1):
            skills_str = ", ".join(f"`{s}`" for s in a["assigned_skills"])
            f.write(f"| {idx:02d} | `{a['agent_id']}` | {a['name']} | `{a['primary_operating_level']}` | {skills_str} | {a['boundary_statement'][:60]}... |\n")

        f.write("\n---\n\n## 2. Global Boundary Rules\n\n")
        for r in agent_map["boundary_rules"]:
            f.write(f"- {r}\n")

        f.write("\n---\n\n## 3. Communication & Delegation Topology\n\n")
        f.write("| Source Agent | Target Agent | Protocol | Validation Contract |\n")
        f.write("|---|---|---|---|\n")
        for c in agent_map["communication_matrix"]:
            f.write(f"| `{c['source_agent']}` | `{c['target_agent']}` | `{c['protocol']}` | `{c['validation_contract']}` |\n")

    # 2. Workflow Map
    wf_map = build_workflow_map()
    wf_json_p = out_dir / "WORKFLOW_FACTORY_MAP.json"
    with open(wf_json_p, "w", encoding="utf-8") as f:
        json.dump(wf_map, f, indent=2)

    wf_md_p = out_dir / "WORKFLOW_FACTORY_MAP.md"
    with open(wf_md_p, "w", encoding="utf-8") as f:
        f.write("# Workflow and Factory Map\n\n")
        f.write(f"**Artifact ID:** {wf_map['artifact_id']}  \n")
        f.write(f"**Status:** {wf_map['status']}  \n")
        f.write(f"**Generated Date:** {wf_map['generated_date']}  \n\n")
        f.write("---\n\n## 1. AI Factory Primitives\n\n")
        f.write("| Primitive ID | Name | Description | Runtime Binding |\n")
        f.write("|---|---|---|---|\n")
        for p in wf_map["factory_primitives"]:
            f.write(f"| `{p['primitive_id']}` | {p['name']} | {p['description']} | `{p['runtime_binding']}` |\n")

        f.write("\n---\n\n## 2. Multi-Agent Workflow Pipelines\n\n")
        for pipe in wf_map["pipelines"]:
            f.write(f"### {pipe['pipeline_id']}: {pipe['name']}\n")
            f.write(f"- **Trigger:** `{pipe['trigger']}`\n")
            f.write(f"- **Terminal Condition:** {pipe['terminal_condition']}\n")
            f.write(f"- **Rollback Strategy:** {pipe['rollback_strategy']}\n\n")
            f.write("| Step # | Agent | Action | Output Artifact |\n")
            f.write("|---|---|---|---|\n")
            for s in pipe["steps"]:
                f.write(f"| {s['step_number']} | `{s['agent']}` | {s['action']} | `{s['output_artifact']}` |\n")
            f.write("\n")

        f.write("---\n\n## 3. Agentic Development Workflow (ADW) Patterns\n\n")
        for pat in wf_map["adw_patterns"]:
            f.write(f"### {pat['pattern_id']}: {pat['name']}\n")
            f.write(f"{pat['description']}\n\n")
            f.write(f"- **JIT Capsule Strategy:** {pat['jit_capsule_strategy']}\n\n")

        f.write("---\n\n## 4. Error Recovery & Rollback Matrix\n\n")
        f.write("| Error Type | Detection Agent | Recovery Action | Operator Escalation |\n")
        f.write("|---|---|---|---|\n")
        for err in wf_map["error_recovery_matrix"]:
            esc = "YES" if err["operator_escalation"] else "NO"
            f.write(f"| `{err['error_type']}` | `{err['detection_agent']}` | {err['recovery_action']} | {esc} |\n")

    print("[SUCCESS] Generated Agent Architecture and Workflow/Factory Maps:")
    print(f"  - {agent_json_p}")
    print(f"  - {agent_md_p}")
    print(f"  - {wf_json_p}")
    print(f"  - {wf_md_p}")

if __name__ == "__main__":
    main()
