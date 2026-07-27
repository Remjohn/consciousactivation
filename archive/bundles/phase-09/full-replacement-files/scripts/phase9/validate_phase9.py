from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TRACE = ROOT / "CMF_PROGRAM_CONTROL" / "03_PROGRAM_STATUS" / "PHASE_09_FINAL_APPLICATION"
PYTHON_SOURCES = [
    ROOT / "packages" / "ca_contracts" / "src",
    ROOT / "packages" / "ca_runtime" / "src",
    ROOT / "packages" / "ca_delegation_rc4" / "src",
    ROOT / "packages" / "ca_release" / "src",
    ROOT / "04_ACTIVATIVE_INTELLIGENCE_RUNTIME" / "src",
    ROOT / "05_ATOMIC_HARNESS_PIPELINE" / "src",
    ROOT / "06_INTERVIEW_EXPRESSION" / "src",
    ROOT / "02_VISUAL_ASSET_EDITOR" / "src",
]


def run(command: list[str], env: dict[str, str], *, cwd: Path = ROOT, timeout: int = 2400) -> dict[str, Any]:
    process = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, timeout=timeout)
    return {
        "command": command,
        "cwd": str(cwd),
        "returncode": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
        "result": "PASS" if process.returncode == 0 else "FAIL",
    }


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def internal_traceability() -> dict[str, Any]:
    specs = list(csv.DictReader((TRACE / "PHASE_09_SPEC_IMPLEMENTATION_MATRIX.csv").open(encoding="utf-8", newline="")))
    criteria = list(csv.DictReader((TRACE / "PHASE_09_ACCEPTANCE_TEST_MATRIX.csv").open(encoding="utf-8", newline="")))
    gaps = list(csv.DictReader((TRACE / "PHASE_09_GAP_LEDGER.csv").open(encoding="utf-8", newline="")))
    errors=[]
    if len(specs) != 13: errors.append(f"expected 13 specs, observed {len(specs)}")
    if not criteria: errors.append("acceptance criteria missing")
    if any(str(row.get("full_spec_completed", "")).lower() == "true" for row in specs): errors.append("a spec is incorrectly marked complete")
    for row in specs:
        path=ROOT/row["path"]
        if not path.is_file(): errors.append(f"missing spec {row['path']}")
        elif sha(path) != row["spec_sha256"]: errors.append(f"spec hash drift {row['spec_id']}")
    result="PASS" if not errors else "FAIL"
    return {"command":["internal","phase9-traceability"],"returncode":0 if result=="PASS" else 1,"stdout":json.dumps({"spec_count":len(specs),"criterion_count":len(criteria),"gap_count":len(gaps),"errors":errors},sort_keys=True),"stderr":"","result":result}


def internal_release_schemas() -> dict[str, Any]:
    root=ROOT/"packages/ca_release/src/ca_release/schemas"
    errors=[]; files=[]
    for path in sorted(root.glob("*.json")):
        files.append(path.name)
        try: json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc: errors.append(f"{path.name}: {exc}")
    if len(files) != 4: errors.append(f"expected 4 release schema files including registry, observed {len(files)}")
    result="PASS" if not errors else "FAIL"
    return {"command":["internal","release-schemas"],"returncode":0 if result=="PASS" else 1,"stdout":json.dumps({"files":files,"errors":errors},sort_keys=True),"stderr":"","result":result}


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--report",type=Path)
    parser.add_argument("--artifact-dir",type=Path)
    args=parser.parse_args()
    missing=[tool for tool in ("node","npm","tsc","ffmpeg","ffprobe","git") if shutil.which(tool) is None]
    if missing: raise SystemExit(f"Phase 9 validation requires: {', '.join(missing)}")
    with tempfile.TemporaryDirectory(prefix="ca-phase9-") as td:
        temp=Path(td)
        env=dict(os.environ)
        env["PYTHONPATH"]=os.pathsep.join(str(path) for path in PYTHON_SOURCES)
        env["CA_DATA_ROOT"]=str(temp/"data")
        env["PYTHONDONTWRITEBYTECODE"]="1"
        env["PYTHONWARNINGS"]="error::ResourceWarning"
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"]="1"
        checks=[]
        checks.append(run([sys.executable,"-m","compileall","-q","packages/ca_release/src","04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src","05_ATOMIC_HARNESS_PIPELINE/src","06_INTERVIEW_EXPRESSION/src","02_VISUAL_ASSET_EDITOR/src","packages/ca_contracts/src","packages/ca_runtime/src","packages/ca_delegation_rc4/src"],env))
        phase8_report=temp/"phase8.json"
        checks.append(run([sys.executable,"scripts/phase8/validate_phase8.py","--report",str(phase8_report)],env,timeout=2400))
        checks.append(run([sys.executable,"-m","pytest","tests/phase9","-q","--basetemp",str(temp/"pytest-phase9")],env,timeout=1200))
        checks.append(internal_traceability())
        checks.append(internal_release_schemas())
        artifact_dir=args.artifact_dir.resolve() if args.artifact_dir else temp/"pilot"
        pilot_code="from ca_release.pilot import run_phase9_pilot; import json,sys; print(json.dumps(run_phase9_pilot(sys.argv[1],sys.argv[2]),sort_keys=True))"
        checks.append(run([sys.executable,"-c",pilot_code,str(ROOT),str(artifact_dir)],env,timeout=1200))
        required=[artifact_dir/"PILOT_RECEIPT.json",artifact_dir/"PHASE_09_COMPLETION_RECEIPT.json",artifact_dir/"PHASE_09_REFERENCE_EVIDENCE.zip",artifact_dir/"release/RELEASE_MANIFEST.json",artifact_dir/"core/media/source-led-short.mp4",artifact_dir/"core/media/supervisual.png",artifact_dir/"core/media/carousel.pdf",artifact_dir/"core/media/animation/scene.mp4",artifact_dir/"core/vae/reference-visual-asset.png"]
        errs=[str(p) for p in required if not p.is_file()]
        if not errs:
            receipt=json.loads((artifact_dir/"PILOT_RECEIPT.json").read_text(encoding="utf-8"))
            for field in ("production_authorized","certified","format02_activated","vae_stage5_authorized"):
                if receipt.get(field) is not False: errs.append(f"{field} not false")
        checks.append({"command":["internal","phase9-reference-artifacts"],"returncode":0 if not errs else 1,"stdout":json.dumps({"required_count":len(required),"errors":errs},sort_keys=True),"stderr":"","result":"PASS" if not errs else "FAIL"})
        result="PASS" if all(c["result"]=="PASS" for c in checks) else "FAIL"
        trace=json.loads((TRACE/"TRACEABILITY_DATA.json").read_text(encoding="utf-8"))
        report={"schema_version":"ca-phase09-validation-report/v1","validated_at_utc":datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),"phase":"PHASE_09_FINAL_APPLICATION","result":result,"checks":checks,"metadata":{"phase9_test_count":11,"spec_count":trace["spec_count"],"acceptance_criterion_count":trace["acceptance_criterion_count"],"reference_artifact_count":5},"claim_ceiling":"PHASE_09_FINAL_INTEGRATED_DEVELOPMENT_CANDIDATE","full_spec_completion_claimed":False,"real_imported_human_interview_executed":False,"external_model_execution_proven":False,"production_authorized":False,"certified":False,"format02_activated":False,"vae_stage5_authorized":False}
        rendered=json.dumps(report,indent=2,sort_keys=True)+"\n"
        print(rendered,end="")
        if args.report:
            args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(rendered,encoding="utf-8")
        return 0 if result=="PASS" else 1

if __name__=="__main__": raise SystemExit(main())
