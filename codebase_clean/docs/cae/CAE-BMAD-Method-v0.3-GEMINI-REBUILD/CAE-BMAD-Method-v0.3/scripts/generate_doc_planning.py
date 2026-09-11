#!/usr/bin/env python3
"""
CAE-BMAD Documentation and Planning System Generator
Generates:
- Seed PRD modules from the Product Reconstruction 5 capability pillars
- PRD Index
- Functional Requirements matrix
- Epic/Story backlog
- Plan Genealogy stub
All emitted to docs/cae-bmad/03_product/ and docs/cae-bmad/05_planning/
"""

import sys
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

def generate_doc_planning():
    rec_json = ROOT / "docs" / "cae-bmad" / "01_reconstruction" / "PRODUCT_RECONSTRUCTION.json"
    if not rec_json.exists():
        print(f"[ERROR] Product Reconstruction not found: {rec_json}")
        sys.exit(1)

    rec = json.loads(rec_json.read_text(encoding="utf-8"))
    pillars = rec.get("capability_pillars", [])

    # Create directories
    product_dir = ROOT / "docs" / "cae-bmad" / "03_product"
    modules_dir = product_dir / "modules"
    planning_dir = ROOT / "docs" / "cae-bmad" / "05_planning"
    modules_dir.mkdir(parents=True, exist_ok=True)
    planning_dir.mkdir(parents=True, exist_ok=True)

    prd_modules = []
    all_frs = []
    epics = []

    for i, pillar in enumerate(pillars, start=1):
        mid = f"PRD-{i:03d}"
        fr_id = f"FR-{i:03d}"
        epic_id = f"EPIC-{i:03d}"
        story_id = f"STORY-{i:04d}"

        prd_module = {
            "module_id": mid,
            "title": pillar["name"],
            "status": "DRAFT",
            "capability_pillar": f"{pillar['pillar_id']}: {pillar['name']}",
            "source_lineage": [
                {"source_id": f"SRC-{i:03d}", "fidelity_status": "INHERITED"}
            ],
            "functional_requirements": [
                {
                    "fr_id": fr_id,
                    "description": f"The system shall implement {pillar['name']} capabilities as defined in {mid}.",
                    "testable": True,
                    "acceptance_criteria": [
                        f"Integration tests verify {pillar['name']} runtime contracts.",
                        f"Brownfield crosswalk confirms active code path at: {pillar['active_runtime_path']}"
                    ]
                }
            ],
            "acceptance_criteria": [
                f"Module {mid} traces to at least one SRC-xxx source.",
                f"All FRs in {mid} have concrete acceptance criteria."
            ]
        }
        prd_modules.append(prd_module)
        all_frs.append(prd_module["functional_requirements"][0])

        epic = {
            "epic_id": epic_id,
            "title": f"Implement {pillar['name']}",
            "status": "BACKLOG",
            "prd_modules": [mid],
            "functional_requirements": [fr_id],
            "stories": [
                {
                    "story_id": story_id,
                    "as_a": "CAE operator",
                    "i_want": f"the {pillar['name']} capability to be fully operational",
                    "so_that": f"the platform can execute {pillar['name'].lower()} workflows end-to-end",
                    "acceptance_criteria": [
                        f"Automated tests confirm {pillar['name']} contract satisfaction.",
                        "No MISSING or CONTRADICTED status in brownfield crosswalk."
                    ]
                }
            ]
        }
        epics.append(epic)

        # Write individual PRD module markdown
        md_content = f"# PRD Module — {mid}: {pillar['name']}\n\n"
        md_content += f"**Module ID:** `{mid}`  \n"
        md_content += f"**Status:** `DRAFT`  \n"
        md_content += f"**Capability Pillar:** `{pillar['pillar_id']}: {pillar['name']}`  \n\n"
        md_content += f"---\n\n## 1. Overview\n{pillar['description']}\n\n"
        md_content += f"## 2. Source Lineage\n- **Historical Roots:** {pillar['historical_roots']}\n"
        md_content += f"- **Active Runtime Path:** `{pillar['active_runtime_path']}`\n\n"
        md_content += f"## 3. Functional Requirements\n### {fr_id}\n"
        md_content += f"{prd_module['functional_requirements'][0]['description']}\n\n"
        md_content += "**Acceptance Criteria:**\n"
        for ac in prd_module['functional_requirements'][0]['acceptance_criteria']:
            md_content += f"- {ac}\n"

        (modules_dir / f"{mid}.md").write_text(md_content, encoding="utf-8")

    # Write PRD Index
    index_content = "# PRD Module Index\n\n"
    index_content += f"**Generated:** {datetime.now().isoformat()}  \n"
    index_content += f"**Total Modules:** {len(prd_modules)}  \n\n"
    index_content += "| Module ID | Title | Pillar | Status |\n"
    index_content += "|---|---|---|---|\n"
    for m in prd_modules:
        index_content += f"| `{m['module_id']}` | {m['title']} | `{m['capability_pillar']}` | `{m['status']}` |\n"
    (product_dir / "PRD_INDEX.md").write_text(index_content, encoding="utf-8")

    # Write PRD modules JSON
    (product_dir / "PRD_MODULES.json").write_text(
        json.dumps(prd_modules, indent=2), encoding="utf-8"
    )

    # Write FR matrix
    fr_content = "# Functional Requirements Matrix\n\n"
    fr_content += f"**Generated:** {datetime.now().isoformat()}  \n"
    fr_content += f"**Total FRs:** {len(all_frs)}  \n\n"
    fr_content += "| FR ID | Description | Testable | Acceptance Criteria |\n"
    fr_content += "|---|---|---|---|\n"
    for fr in all_frs:
        acs = "; ".join(fr["acceptance_criteria"])
        fr_content += f"| `{fr['fr_id']}` | {fr['description'][:80]}... | Yes | {acs[:100]}... |\n"
    (product_dir / "FUNCTIONAL_REQUIREMENTS.md").write_text(fr_content, encoding="utf-8")

    # Write Epics JSON
    (planning_dir / "EPICS.json").write_text(
        json.dumps(epics, indent=2), encoding="utf-8"
    )

    # Write Epics markdown
    epics_md = "# Delivery Epics\n\n"
    for e in epics:
        epics_md += f"## {e['epic_id']}: {e['title']}\n"
        epics_md += f"- **Status:** `{e['status']}`\n"
        epics_md += f"- **PRD Modules:** {', '.join(f'`{p}`' for p in e['prd_modules'])}\n"
        epics_md += f"- **FRs:** {', '.join(f'`{f}`' for f in e['functional_requirements'])}\n\n"
        for s in e['stories']:
            epics_md += f"### {s['story_id']}\n"
            epics_md += f"- **As a** {s['as_a']}\n"
            epics_md += f"- **I want** {s['i_want']}\n"
            epics_md += f"- **So that** {s['so_that']}\n\n"
    (planning_dir / "EPICS.md").write_text(epics_md, encoding="utf-8")

    # Write Plan Genealogy stub
    genealogy_md = "# Plan Genealogy\n\n"
    genealogy_md += f"**Generated:** {datetime.now().isoformat()}  \n\n"
    genealogy_md += "## Historical Milestone Register\n"
    genealogy_md += "| Milestone Range | Domain | Status |\n"
    genealogy_md += "|---|---|---|\n"
    genealogy_md += "| M01-M12 | CAE-BMAD Method Rebuild | IN_PROGRESS |\n"
    genealogy_md += "| M13-M40 | Platform Foundation & Runtime | HISTORICAL |\n"
    genealogy_md += "| M41-M55 | Pipeline & Workflow Compiler | HISTORICAL |\n"
    genealogy_md += "| M56-M72 | World Intelligence & Editorial | HISTORICAL |\n"
    (planning_dir / "PLAN_GENEALOGY.md").write_text(genealogy_md, encoding="utf-8")

    print(f"[SUCCESS] Generated Documentation & Planning artifacts:")
    print(f"  - {len(prd_modules)} PRD modules in {modules_dir}")
    print(f"  - PRD Index at {product_dir / 'PRD_INDEX.md'}")
    print(f"  - {len(all_frs)} FRs in {product_dir / 'FUNCTIONAL_REQUIREMENTS.md'}")
    print(f"  - {len(epics)} Epics in {planning_dir / 'EPICS.md'}")
    print(f"  - Plan Genealogy at {planning_dir / 'PLAN_GENEALOGY.md'}")

if __name__ == "__main__":
    generate_doc_planning()
