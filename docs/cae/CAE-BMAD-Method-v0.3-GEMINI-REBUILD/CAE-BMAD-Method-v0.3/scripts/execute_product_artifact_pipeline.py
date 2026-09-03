#!/usr/bin/env python3
"""
CAE-BMAD Product Artifact Production Pipeline Executor
Assembles the complete set of core product specifications:
- Product Brief (Level 01)
- Technical Architecture (Level 02/07)
- UI/UX Specification (Level 01/07)
Emits deliverables to docs/cae-bmad/03_product/, docs/cae-bmad/04_architecture/, and docs/cae-bmad/06_ui_ux/
"""

import sys
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

def build_product_brief() -> dict:
    brief = {
        "artifact_id": "CAE-ART-PB-001",
        "product_name": "Conscious Activation Engine (CAE)",
        "status": "APPROVED",
        "vision_statement": "Conscious Activation Engine transforms high-velocity global intelligence, guest interviews, and editorial collision hypotheses into verified, broadcast-grade narrative activations with cryptographic proof and human operator governance.",
        "target_audience": [
            "Media & Narrative Strategists",
            "Editorial Content Producers",
            "Enterprise Brand Intelligence Directors",
            "Autonomous Studio Operators"
        ],
        "capability_pillars": [
            "Audience & Guest Intelligence",
            "Question & Interview Intelligence",
            "Evidence & Receipt Provenance",
            "Editorial & Storyboard Production",
            "Multi-Agent Runtime & Factory Scheduling"
        ],
        "non_goals": [
            "Will NOT execute un-sandboxed autonomous public broadcast without operator sign-off.",
            "Will NOT store unverified or hallucinated claims without explicit PROPOSED status tags.",
            "Will NOT act as a generic chatbot; all executions must be structured multi-agent workflows."
        ],
        "success_metrics": [
            "100% cryptographic provenance traceability on all emitted storyboards",
            "Zero unhandled state transitions during multi-agent pipeline execution",
            "Sub-second JIT context capsule assembly across all 19 specialized agents"
        ]
    }
    return brief

def build_architecture() -> dict:
    subsystems = [
        {
            "subsystem_id": "SUB-WORLD-INTEL",
            "name": "World Signal Ingestion Subsystem",
            "responsibility": "Ingests raw media signals, verifies source provenance hashes, checks wire inflation, and normalizes telemetry.",
            "bound_services": ["services/world-intelligence/"]
        },
        {
            "subsystem_id": "SUB-PIPELINE-ENGINE",
            "name": "Deterministic Workflow & Compiler Subsystem",
            "responsibility": "Compiles multi-agent DAGs, validates step schemas, and orchestrates deterministic state transitions.",
            "bound_services": ["services/pipeline/"]
        },
        {
            "subsystem_id": "SUB-RUNTIME-CORE",
            "name": "Conscious Activation Runtime Core",
            "responsibility": "Provides JIT context capsules, CAS state machine runtimes, and typed agent invocation harnesses.",
            "bound_services": ["packages/ca_runtime/"]
        },
        {
            "subsystem_id": "SUB-STUDIO-UI",
            "name": "Operator Studio & Visual Telemetry Subsystem",
            "responsibility": "Renders operator dashboards, telemetry monitors, and Atomic Harness visual syntax tokens.",
            "bound_services": ["atomic_harnesses_visual_syntax/"]
        }
    ]

    interfaces = [
        {
            "interface_name": "ResearchSignalIngestionAPI",
            "type": "REST_API",
            "contract_schema": "schemas/research_source.schema.json"
        },
        {
            "interface_name": "WorkflowExecutionPlanInterface",
            "type": "INTERNAL_PYTHON_API",
            "contract_schema": "schemas/workflow_factory_map.schema.json"
        },
        {
            "interface_name": "ProgramStateCASInterface",
            "type": "INTERNAL_PYTHON_API",
            "contract_schema": "docs/cae/constitutions/CA-CAN-02_STATE_AGGREGATE.yaml"
        }
    ]

    protocols = ["HTTP/2 REST", "Internal Asynchronous Python Callables", "CAS Optimistic Locking"]

    arch = {
        "artifact_id": "CAE-ART-ARCH-001",
        "status": "APPROVED",
        "system_name": "Conscious Activation Engine Core Architecture",
        "subsystems": subsystems,
        "interfaces": interfaces,
        "communication_protocols": protocols,
        "brownfield_integration_strategy": "The architecture directly incorporates existing Python packages (ca_runtime) and microservices (world-intelligence, pipeline), wrapping them in typed schema boundaries rather than rewriting them.",
        "security_and_governance": "All state transitions guarded by Compare-And-Swap version checks; all operator promotions require explicit gate ratification."
    }
    return arch

def build_ui_ux_spec() -> dict:
    views = [
        {
            "view_id": "VIEW-OPERATOR-STUDIO",
            "title": "Master Operator Studio Dashboard",
            "purpose": "Central command interface for initiating programs, reviewing evidence, and managing operator gates.",
            "primary_components": ["ProgramNavigator", "GateApprovalModal", "TelemetryHUD"]
        },
        {
            "view_id": "VIEW-INTERVIEW-TELEMETRY",
            "title": "Dynamic Interview Telemetry Monitor",
            "purpose": "Live visual tracking of guest psychological stance, question tension, and turn-by-turn hypothesis testing.",
            "primary_components": ["GuestVectorVisualizer", "HypothesisHeatmap", "TurnSequenceController"]
        },
        {
            "view_id": "VIEW-EVIDENCE-INSPECTOR",
            "title": "Evidence & Provenance Inspector",
            "purpose": "Cryptographic receipt inspection, source hash verification, and wire-copy de-inflation inspector.",
            "primary_components": ["ReceiptVerificationBadge", "SourceLineageViewer", "RawBytesInspector"]
        }
    ]

    tokens = {
        "color_tokens": [
            "color-bg-primary: #0A0D14",
            "color-surface-card: #121824",
            "color-accent-amber: #F59E0B",
            "color-status-verified: #10B981",
            "color-status-contradicted: #EF4444"
        ],
        "typography_tokens": [
            "font-family-mono: 'JetBrains Mono', monospace",
            "font-family-sans: 'Inter', -apple-system, sans-serif",
            "font-size-telemetry: 11px"
        ],
        "telemetry_monitors": [
            "Monitor-Guest-Stance: 60Hz vector refresh",
            "Monitor-CAS-Version: Optimistic lock state indicator",
            "Monitor-Gate-Status: Pulse warning on unratified promotion"
        ]
    }

    flows = [
        {
            "flow_name": "Operator Gate Promotion Flow",
            "trigger": "Agent completes mandate step and requests promotion.",
            "steps": [
                "Agent emits gate packet (OPERATOR_GATE_Mxx.md)",
                "UI alerts operator with pulse warning badge",
                "Operator reviews automated test output and diff matrix",
                "Operator clicks Ratify or Rejects with feedback"
            ],
            "error_handling": "If validation fails, promotion button is disabled and failure log is presented in modal."
        }
    ]

    ui_ux = {
        "artifact_id": "CAE-ART-UIUX-001",
        "status": "APPROVED",
        "product_name": "Conscious Activation Engine UI/UX",
        "operator_views": views,
        "atomic_harness_tokens": tokens,
        "interaction_flows": flows,
        "accessibility_standards": "WCAG 2.1 AA compliant, full keyboard shortcut navigation, high-contrast dark telemetry theme."
    }
    return ui_ux

def main():
    # 1. Product Brief
    product_dir = ROOT / "docs" / "cae-bmad" / "03_product"
    product_dir.mkdir(parents=True, exist_ok=True)
    brief = build_product_brief()
    pb_json_p = product_dir / "PRODUCT_BRIEF.json"
    with open(pb_json_p, "w", encoding="utf-8") as f:
        json.dump(brief, f, indent=2)

    pb_md_p = product_dir / "PRODUCT_BRIEF.md"
    with open(pb_md_p, "w", encoding="utf-8") as f:
        f.write(f"# Product Brief — {brief['product_name']}\n\n")
        f.write(f"**Artifact ID:** {brief['artifact_id']}  \n")
        f.write(f"**Status:** {brief['status']}  \n\n")
        f.write(f"---\n\n## 1. Vision Statement\n{brief['vision_statement']}\n\n")
        f.write("---\n\n## 2. Target Audience\n")
        for a in brief["target_audience"]:
            f.write(f"- {a}\n")
        f.write("\n---\n\n## 3. Capability Pillars\n")
        for p in brief["capability_pillars"]:
            f.write(f"- {p}\n")
        f.write("\n---\n\n## 4. Explicit Non-Goals\n")
        for ng in brief["non_goals"]:
            f.write(f"- {ng}\n")
        f.write("\n---\n\n## 5. Success Metrics\n")
        for sm in brief["success_metrics"]:
            f.write(f"- {sm}\n")

    # 2. Architecture
    arch_dir = ROOT / "docs" / "cae-bmad" / "04_architecture"
    arch_dir.mkdir(parents=True, exist_ok=True)
    arch = build_architecture()
    arch_json_p = arch_dir / "ARCHITECTURE.json"
    with open(arch_json_p, "w", encoding="utf-8") as f:
        json.dump(arch, f, indent=2)

    arch_md_p = arch_dir / "ARCHITECTURE.md"
    with open(arch_md_p, "w", encoding="utf-8") as f:
        f.write(f"# Architecture Specification — {arch['system_name']}\n\n")
        f.write(f"**Artifact ID:** {arch['artifact_id']}  \n")
        f.write(f"**Status:** {arch['status']}  \n\n")
        f.write("---\n\n## 1. Subsystems\n\n")
        f.write("| Subsystem ID | Name | Responsibility | Bound Services |\n")
        f.write("|---|---|---|---|\n")
        for sub in arch["subsystems"]:
            svcs_str = ", ".join(f"`{s}`" for s in sub["bound_services"])
            f.write(f"| `{sub['subsystem_id']}` | {sub['name']} | {sub['responsibility']} | {svcs_str} |\n")

        f.write("\n---\n\n## 2. Interface Boundaries\n\n")
        f.write("| Interface Name | Type | Contract Schema |\n")
        f.write("|---|---|---|\n")
        for iface in arch["interfaces"]:
            f.write(f"| `{iface['interface_name']}` | `{iface['type']}` | `{iface['contract_schema']}` |\n")

        f.write("\n---\n\n## 3. Communication Protocols\n\n")
        for proto in arch["communication_protocols"]:
            f.write(f"- {proto}\n")

        f.write(f"\n---\n\n## 4. Brownfield Integration Strategy\n\n{arch['brownfield_integration_strategy']}\n")
        f.write(f"\n---\n\n## 5. Security & Governance Controls\n\n{arch['security_and_governance']}\n")

    # 3. UI/UX
    ui_dir = ROOT / "docs" / "cae-bmad" / "06_ui_ux"
    ui_dir.mkdir(parents=True, exist_ok=True)
    ui_ux = build_ui_ux_spec()
    ui_json_p = ui_dir / "UI_UX_SPECIFICATION.json"
    with open(ui_json_p, "w", encoding="utf-8") as f:
        json.dump(ui_ux, f, indent=2)

    ui_md_p = ui_dir / "UI_UX_SPECIFICATION.md"
    with open(ui_md_p, "w", encoding="utf-8") as f:
        f.write(f"# UI/UX Specification — {ui_ux['product_name']}\n\n")
        f.write(f"**Artifact ID:** {ui_ux['artifact_id']}  \n")
        f.write(f"**Status:** {ui_ux['status']}  \n\n")
        f.write("---\n\n## 1. Operator Studio Views\n\n")
        f.write("| View ID | Title | Purpose | Primary Components |\n")
        f.write("|---|---|---|---|\n")
        for v in ui_ux["operator_views"]:
            comps_str = ", ".join(v["primary_components"])
            f.write(f"| `{v['view_id']}` | {v['title']} | {v['purpose']} | {comps_str} |\n")

        f.write("\n---\n\n## 2. Atomic Harness Design Tokens\n\n")
        f.write("### Color Tokens\n")
        for c in ui_ux["atomic_harness_tokens"]["color_tokens"]:
            f.write(f"- `{c}`\n")
        f.write("\n### Typography Tokens\n")
        for t in ui_ux["atomic_harness_tokens"]["typography_tokens"]:
            f.write(f"- `{t}`\n")
        f.write("\n### Telemetry Monitors\n")
        for m in ui_ux["atomic_harness_tokens"]["telemetry_monitors"]:
            f.write(f"- `{m}`\n")

        f.write("\n---\n\n## 3. Interaction Flows\n\n")
        for flow in ui_ux["interaction_flows"]:
            f.write(f"### {flow['flow_name']}\n")
            f.write(f"- **Trigger:** `{flow['trigger']}`\n")
            f.write("- **Steps:**\n")
            for st in flow["steps"]:
                f.write(f"  1. {st}\n")
            f.write(f"- **Error Handling:** {flow['error_handling']}\n\n")

        f.write(f"---\n\n## 4. Accessibility Standards\n\n{ui_ux['accessibility_standards']}\n")

    print("[SUCCESS] Emitted Product Brief, Architecture, and UI/UX specifications:")
    print(f"  - {pb_json_p}")
    print(f"  - {arch_json_p}")
    print(f"  - {ui_json_p}")

if __name__ == "__main__":
    main()
