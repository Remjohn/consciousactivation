import os
import sys
import subprocess
import json
from pathlib import Path

stage1_out = Path("d:/Work/consciousactivation/stage1_output")
specs_out = stage1_out

success_count = 0
reports = list(stage1_out.glob("*_STAGE1_REPORT.json"))
total = len(reports)

for report in reports:
    h = report.name.replace("_STAGE1_REPORT.json", "")
    print(f"--- Processing {h} Stage 2 ---")
    
    cmd_s2 = [
        sys.executable,
        "-m", "cmf_builder.stage2.stage2_cli",
        "--harness-id", h,
        "--stage1-report", str(report),
        "--output-dir", str(specs_out)
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    
    proc_s2 = subprocess.run(cmd_s2, cwd=r"d:\Work\consciousactivation\services\builder", env=env, capture_output=True, text=True)
    
    if proc_s2.returncode == 0:
        success_count += 1
        print(f"  [PASS] {h} -> Stage 2 Complete!")
    else:
        print(f"  [FAIL Stage 2] {h}")
        print("STDOUT:", proc_s2.stdout[:300])
        print("STDERR:", proc_s2.stderr[:300])

print("\n" + "="*60)
print(f"COMPLETE: {success_count}/{total} Harnesses Compiled Stage 2 Successfully")
print("="*60)
