"""
Batch runner to re-execute Stage 1 CLI for all 29 alternative-schema harnesses.
Clears intermediate checkpoints to ensure clean execution from updated VisionClient observations.
"""

import os
import time
from pathlib import Path
from cmf_builder.stage1.stage1_cli import main as stage1_cli_main

BASE_DIR = Path(r"d:\Work\consciousactivation")
CAROUSELS_ZIP_DIR = BASE_DIR / "atomic_harnesses_visual_syntax" / "carousels"
SUPERVISUALS_ZIP_DIR = BASE_DIR / "atomic_harnesses_visual_syntax" / "supervisuals"
OUTPUT_DIR = BASE_DIR / "stage1_output"
CHECKPOINTS_DIR = OUTPUT_DIR / "checkpoints"

STUB_HARNESSES = [
    "CAR-LST-Olympics-4-5-10",
    "CAR-LST-Peoplechg-4-5-11",
    "CAR-LST-Planetdat-1-1-8",
    "CAR-LST-Realconfid-4-5-4",
    "CAR-LST-Relatives-4-5-7",
    "CAR-LST-Resentmnt-4-5-10",
    "CAR-LST-Rightppl-4-5-3",
    "CAR-LST-Ronaldo-4-5-6",
    "CAR-LST-Ronweasly-4-5-9",
    "CAR-LST-Safespace-4-5-5",
    "CAR-LST-Screenstr-4-5-8",
    "CAR-LST-Selflove-4-5-4",
    "CAR-LST-Stayrare-4-5-4",
    "CAR-LST-Stopsave-1-1-10",
    "CAR-LST-Upgrades-4-5-3",
    "CAR-LST-Viralpost-3-4-8",
    "CAR-LST-Weekgoals-4-5-2",
    "CAR-LST-Yurchance-4-5-5",
    "MEM-REL-Relatable",
    "RCT-SEED-Reaction",
    "SPV-CON-Comparison",
    "SPV-CON-Contrast",
    "SPV-PRM-Premium",
    "SPV-SYM-Symbolic",
    "TWQ-IMG-Portrait",
    "TWQ-IMG-Quotebox",
    "TWQ-STD-Assertion",
    "VPL-WYR-Quizcard",
    "VPL-WYR-Vertical"
]


def find_zip_file(harness_id: str) -> Path:
    if harness_id.startswith("CAR-"):
        zip_path = CAROUSELS_ZIP_DIR / f"{harness_id}.zip"
    else:
        zip_path = SUPERVISUALS_ZIP_DIR / f"{harness_id}.zip"
    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file not found: {zip_path}")
    return zip_path


def clear_checkpoints():
    if CHECKPOINTS_DIR.exists():
        for f in CHECKPOINTS_DIR.glob("*.json"):
            try:
                os.remove(f)
            except Exception:
                pass


def main():
    print(f"Starting Stage 1 re-run for {len(STUB_HARNESSES)} harnesses...")
    passed = 0
    failed = 0

    for idx, harness_id in enumerate(STUB_HARNESSES, 1):
        print(f"\n[{idx}/{len(STUB_HARNESSES)}] Processing {harness_id}...")
        
        clear_checkpoints()

        try:
            zip_path = find_zip_file(harness_id)
            cli_args = [
                "--harness-id", harness_id,
                "--source-zip", str(zip_path),
                "--output-dir", str(OUTPUT_DIR)
            ]
            exit_code = stage1_cli_main(cli_args)
            if exit_code == 0:
                passed += 1
                print(f"[PASS] {harness_id} Stage 1 report regenerated.")
            else:
                failed += 1
                print(f"[FAIL] {harness_id} Stage 1 exited with code {exit_code}")
        except Exception as e:
            failed += 1
            print(f"[ERROR] {harness_id}: {e}")

    print(f"\n==========================================")
    print(f"Stage 1 Re-run Complete: PASS={passed} | FAIL={failed}")
    print(f"==========================================")


if __name__ == "__main__":
    main()
