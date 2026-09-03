#!/usr/bin/env python3
"""
CAE-BMAD Workspace Initializer
Initializes the .caebmad/ working area without altering application runtime code.
"""

import sys
import shutil
from pathlib import Path

def init_caebmad(root_dir: Path) -> int:
    caebmad_dir = root_dir / ".caebmad"
    dirs_to_create = [
        caebmad_dir / "config",
        caebmad_dir / "research",
        caebmad_dir / "state",
        caebmad_dir / "templates",
        caebmad_dir / "workflows",
        root_dir / "docs" / "cae-bmad" / "00_governance",
        root_dir / "docs" / "cae-bmad" / "01_reconstruction",
        root_dir / "docs" / "cae-bmad" / "02_investigation",
        root_dir / "docs" / "cae-bmad" / "03_product" / "modules",
        root_dir / "docs" / "cae-bmad" / "04_architecture",
        root_dir / "docs" / "cae-bmad" / "05_planning",
        root_dir / "docs" / "cae-bmad" / "06_ui_ux",
        root_dir / "docs" / "cae-bmad" / "07_brownfield",
        root_dir / "docs" / "cae-bmad" / "08_handoff",
        root_dir / "docs" / "cae-bmad" / "09_review",
    ]

    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)
        print(f"[INIT] Created directory: {d.relative_to(root_dir)}")

    # Initialize default project state
    state_file = caebmad_dir / "state" / "project-state.yaml"
    if not state_file.exists():
        state_file.write_text(
            "method: cae-bmad\nversion: 0.3.0-rebuild\nstate: NOT_STARTED\nactive_mandate: M01\nratified_milestones: []\n",
            encoding="utf-8"
        )
        print(f"[INIT] Initialized state file: {state_file.relative_to(root_dir)}")

    print("[INIT] CAE-BMAD workspace initialization complete.")
    return 0

if __name__ == "__main__":
    target = Path(__file__).resolve().parents[1]
    sys.exit(init_caebmad(target))
