import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

harnesses = [
    'CAR-LST-Olympics-4-5-10',
    'MEM-REL-Relatable',
    'RCT-SEED-Reaction',
    'SPV-CON-Contrast',
    'SPV-PRM-Premium',
    'SPV-SYM-Symbolic',
    'TWQ-IMG-Portrait',
    'TWQ-STD-Assertion',
    'VPL-WYR-Quizcard'
]

source_root = Path("d:/Work/consciousactivation/atomic_harnesses_visual_syntax")
temp_zip_dir = Path("d:/Work/consciousactivation/temp_zips")
temp_zip_dir.mkdir(parents=True, exist_ok=True)

stage1_out = Path("d:/Work/consciousactivation/stage1_output")
specs_out = stage1_out / "specs"
specs_out.mkdir(parents=True, exist_ok=True)

success_s1 = 0
success_s2 = 0

for h in harnesses:
    print(f"\n==========================================")
    print(f"Processing Harness: {h}")
    print(f"==========================================")
    
    # 1. Locate harness directory
    found_dirs = list(source_root.rglob(h))
    if not found_dirs or not found_dirs[0].is_dir():
        print(f"[ERROR] Harness directory not found for {h}")
        continue
    
    h_dir = found_dirs[0]
    zip_path = temp_zip_dir / f"{h}.zip"
    
    # Create zip file from directory
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(h_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, h_dir)
                zipf.write(full_path, arcname)
                
    print(f"[ZIP] Created {zip_path.name}")
    
    # 2. Run Stage 1 CLI
    cmd_s1 = [
        sys.executable,
        "-m", "cmf_builder.stage1.stage1_cli",
        "--harness-id", h,
        "--source-zip", str(zip_path),
        "--output-dir", str(stage1_out)
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    
    proc_s1 = subprocess.run(cmd_s1, cwd=r"d:\Work\consciousactivation\services\builder", env=env, capture_output=True, text=True)
    
    s1_report = stage1_out / f"{h}_STAGE1_REPORT.json"
    if proc_s1.returncode != 0 or not s1_report.exists():
        print(f"[FAIL Stage 1] {h}")
        print("STDERR:", proc_s1.stderr)
        continue
        
    success_s1 += 1
    print(f"[PASS Stage 1] Report generated: {s1_report.name}")
    
    # 3. Run Stage 2 CLI
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
        success_s2 += 1
        print(f"[PASS Stage 2] Spec generated: {s2_spec.name}")
    else:
        print(f"[FAIL Stage 2] {h}")
        print("STDOUT:", proc_s2.stdout)
        print("STDERR:", proc_s2.stderr)

print("\n" + "="*60)
print(f"SUMMARY: Stage 1 = {success_s1}/{len(harnesses)} | Stage 2 = {success_s2}/{len(harnesses)} PASS")
print("="*60)
