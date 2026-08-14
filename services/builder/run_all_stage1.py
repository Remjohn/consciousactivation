import os
import sys
import subprocess
import json
from pathlib import Path

harnesses = [
    # SPV (4)
    'SPV-CON-Comparison',
    'SPV-CON-Contrast',
    'SPV-PRM-Premium',
    'SPV-SYM-Symbolic',
    # MEM (1)
    'MEM-REL-Relatable',
    # RCT (1)
    'RCT-SEED-Reaction',
    # TWQ (3)
    'TWQ-IMG-Portrait',
    'TWQ-IMG-Quotebox',
    'TWQ-STD-Assertion',
    # VPL (2)
    'VPL-WYR-Quizcard',
    'VPL-WYR-Vertical',
    # CAR-LST (18)
    'CAR-LST-Olympics-4-5-10',
    'CAR-LST-Peoplechg-4-5-11',
    'CAR-LST-Planetdat-1-1-8',
    'CAR-LST-Realconfid-4-5-4',
    'CAR-LST-Relatives-4-5-7',
    'CAR-LST-Resentmnt-4-5-10',
    'CAR-LST-Rightppl-4-5-3',
    'CAR-LST-Ronaldo-4-5-6',
    'CAR-LST-Ronweasly-4-5-9',
    'CAR-LST-Safespace-4-5-5',
    'CAR-LST-Screenstr-4-5-8',
    'CAR-LST-Selflove-4-5-4',
    'CAR-LST-Stayrare-4-5-4',
    'CAR-LST-Stopsave-1-1-10',
    'CAR-LST-Upgrades-4-5-3',
    'CAR-LST-Viralpost-3-4-8',
    'CAR-LST-Weekgoals-4-5-2',
    'CAR-LST-Yurchance-4-5-5'
]

zip_map = {}
for root, dirs, files in os.walk('d:/Work/consciousactivation/services/storage/harness-library'):
    for f in files:
        if f.endswith('.zip'):
            name = f[:-4]
            zip_map[name] = os.path.join(root, f)

results = []
success_count = 0

stage1_out = Path("d:/Work/consciousactivation/stage1_output")
specs_out = stage1_out / "specs"
specs_out.mkdir(parents=True, exist_ok=True)

for h in harnesses:
    source_zip = zip_map.get(h)
    if not source_zip:
        print(f"  [FAIL] ZIP NOT FOUND FOR: {h}")
        results.append({"harness": h, "status": "FAIL", "error": "Zip file not found"})
        continue
        
    print(f"--- Processing {h} ---")
    
    # 1. Run Stage 1 CLI
    cmd_s1 = [
        sys.executable,
        "-m", "cmf_builder.stage1.stage1_cli",
        "--harness-id", h,
        "--source-zip", source_zip,
        "--output-dir", str(stage1_out)
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    
    proc_s1 = subprocess.run(cmd_s1, cwd=r"d:\Work\consciousactivation\services\builder", env=env, capture_output=True, text=True)
    
    s1_report = stage1_out / f"{h}_STAGE1_REPORT.json"
    if proc_s1.returncode != 0 or not s1_report.exists():
        print(f"  [FAIL Stage 1] {h}")
        print("STDERR:", proc_s1.stderr[:300])
        results.append({"harness": h, "status": "FAIL_STAGE1", "error": proc_s1.stderr})
        continue

    # 2. Run Stage 2 CLI
    cmd_s2 = [
        sys.executable,
        "-m", "cmf_builder.stage2.stage2_cli",
        "--harness-id", h,
        "--stage1-report", str(s1_report),
        "--output-dir", str(specs_out)
    ]
    
    proc_s2 = subprocess.run(cmd_s2, cwd=r"d:\Work\consciousactivation\services\builder", env=env, capture_output=True, text=True)
    
    s2_spec = specs_out / f"{h}_STAGE2_SPEC.json"
    if proc_s2.returncode == 0:
        success_count += 1
        print(f"  [PASS] {h} -> Stage 1 & Stage 2 Complete!")
        results.append({
            "harness": h,
            "status": "PASS",
            "stage1_report": str(s1_report),
            "stage2_spec": str(s2_spec) if s2_spec.exists() else "created in output dir"
        })
    else:
        print(f"  [FAIL Stage 2] {h}")
        print("STDOUT:", proc_s2.stdout[:300])
        results.append({"harness": h, "status": "FAIL_STAGE2", "error": proc_s2.stdout})

print("\n" + "="*60)
print(f"COMPLETE: {success_count}/{len(harnesses)} Harnesses Compiled Stage 1 & Stage 2 Successfully")
print("="*60)

with open(stage1_out / "execution_summary.json", "w") as f:
    json.dump(results, f, indent=2)
