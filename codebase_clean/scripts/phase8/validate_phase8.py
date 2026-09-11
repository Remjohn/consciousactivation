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
VAE = ROOT / "services/vae"
RC4 = ROOT / "services/delegation" / "delegation-contracts" / "1.1.0-rc.4"
RC4_PC = ROOT / "governance/program-control" / "02_CROSS_REPO_CONTRACTS" / "delegation-contracts" / "1.1.0-rc.4"
TRACE = ROOT / "governance/program-control" / "03_PROGRAM_STATUS" / "PHASE_08_DELEGATION_VAE_INTEGRATION"
PYTHON_SOURCES = [
    ROOT / "packages" / "ca_contracts" / "src",
    ROOT / "packages" / "ca_runtime" / "src",
    ROOT / "packages" / "ca_delegation_rc4" / "src",
    ROOT / "services/air" / "src",
    ROOT / "services/pipeline" / "src",
    ROOT / "services/interview" / "src",
    ROOT / "services/vae" / "src",
]

TRANSIENT_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules"}
TRANSIENT_SUFFIXES = {".pyc", ".pyo"}


def run(command: list[str], env: dict[str, str], cwd: Path = ROOT, timeout: int = 1800) -> dict[str, Any]:
    cmd = list(command)
    if os.name == "nt" and cmd:
        resolved = (
            shutil.which(cmd[0] + ".cmd")
            or shutil.which(cmd[0] + ".bat")
            or shutil.which(cmd[0] + ".exe")
            or shutil.which(cmd[0])
        )
        if resolved:
            cmd[0] = resolved
    process = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True, timeout=timeout)
    return {
        "command": command,
        "cwd": str(cwd),
        "returncode": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
        "result": "PASS" if process.returncode == 0 else "FAIL",
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def release_file_map(root: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in TRANSIENT_DIRS for part in relative.parts) or path.suffix in TRANSIENT_SUFFIXES:
            continue
        result[relative.as_posix()] = {"bytes": path.stat().st_size, "sha256": sha256(path)}
    return result


def internal_rc4_copy_check() -> dict[str, Any]:
    left = release_file_map(RC4)
    right = release_file_map(RC4_PC)
    missing_left = sorted(set(right) - set(left))
    missing_right = sorted(set(left) - set(right))
    mismatched = sorted(path for path in set(left) & set(right) if left[path] != right[path])
    result = "PASS" if not missing_left and not missing_right and not mismatched else "FAIL"
    return {
        "command": ["internal", "rc4-byte-identity"],
        "returncode": 0 if result == "PASS" else 1,
        "stdout": json.dumps({
            "delegation_file_count": len(left),
            "program_control_file_count": len(right),
            "missing_in_delegation": missing_left,
            "missing_in_program_control": missing_right,
            "mismatched": mismatched,
        }, sort_keys=True),
        "stderr": "",
        "result": result,
    }


def internal_traceability_check() -> dict[str, Any]:
    specs_path = TRACE / "PHASE_08_SPEC_IMPLEMENTATION_MATRIX.csv"
    ac_path = TRACE / "PHASE_08_ACCEPTANCE_TEST_MATRIX.csv"
    gaps_path = TRACE / "PHASE_08_GAP_LEDGER.csv"
    with specs_path.open(encoding="utf-8", newline="") as stream:
        specs = list(csv.DictReader(stream))
    with ac_path.open(encoding="utf-8", newline="") as stream:
        criteria = list(csv.DictReader(stream))
    with gaps_path.open(encoding="utf-8", newline="") as stream:
        gaps = list(csv.DictReader(stream))
    evidence_counts: dict[str, int] = {}
    for row in criteria:
        evidence_counts[row["evidence_status"]] = evidence_counts.get(row["evidence_status"], 0) + 1
    errors: list[str] = []
    if len(specs) != 18:
        errors.append(f"expected 18 specs, observed {len(specs)}")
    if len(criteria) != 168:
        errors.append(f"expected 168 criteria, observed {len(criteria)}")
    direct = evidence_counts.get("DIRECT_CRITERION_LEVEL_TEST_EVIDENCE", 0)
    indirect = evidence_counts.get("IMPLEMENTATION_OR_CONSUMED_RELEASE_EVIDENCE_NO_DIRECT_AC_TEST", 0)
    deferred = evidence_counts.get("DEFERRED_OR_EXTERNAL_EVIDENCE", 0)
    if (direct, indirect, deferred) != (96, 49, 23):
        errors.append(f"evidence counts differ: {(direct, indirect, deferred)}")
    if any(str(row.get("full_spec_completed", "")).lower() == "true" for row in specs):
        errors.append("a Phase 8 spec was incorrectly marked fully complete")
    if not (TRACE / "COMPLETION_RECEIPT.yaml").is_file():
        errors.append("completion receipt missing")
    result = "PASS" if not errors else "FAIL"
    return {
        "command": ["internal", "phase8-traceability"],
        "returncode": 0 if result == "PASS" else 1,
        "stdout": json.dumps({"spec_count": len(specs), "criterion_count": len(criteria), "evidence_counts": evidence_counts, "gap_count": len(gaps), "errors": errors}, sort_keys=True),
        "stderr": "",
        "result": result,
    }


def internal_reference_artifact_check(demo_dir: Path) -> dict[str, Any]:
    required = {
        "demand.json", "plan.json", "workcell.json", "comfyui-graph.json",
        "evaluation.json", "asset-result.json", "result-acknowledgement.json",
        "control-tower.json", "okf-projection.json", "demo-receipt.json",
        "visual-asset-result.md", "reference-visual-asset.png", "vae.sqlite3",
    }
    observed = {path.name for path in demo_dir.iterdir() if path.is_file()} if demo_dir.exists() else set()
    errors: list[str] = []
    missing = sorted(required - observed)
    if missing:
        errors.append(f"missing demo artifacts: {missing}")
    png = demo_dir / "reference-visual-asset.png"
    if png.is_file() and not png.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
        errors.append("reference asset is not PNG")
    receipt = demo_dir / "demo-receipt.json"
    if receipt.is_file():
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        for key in ("real_sam3_executed", "real_lucida_executed", "real_comfyui_worker_executed", "real_google_gnm_executed", "production_authorized", "certified", "format02_activated"):
            if payload.get(key) is not False:
                errors.append(f"demo receipt must keep {key}=false")
    result = "PASS" if not errors else "FAIL"
    return {
        "command": ["internal", "phase8-reference-artifacts"],
        "returncode": 0 if result == "PASS" else 1,
        "stdout": json.dumps({"required": sorted(required), "observed": sorted(observed), "errors": errors}, sort_keys=True),
        "stderr": "",
        "result": result,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    parser.add_argument("--artifact-dir", type=Path)
    args = parser.parse_args()

    required_tools = ("node", "npm", "tsc", "ffmpeg", "ffprobe")
    absent = [tool for tool in required_tools if shutil.which(tool) is None]
    if absent:
        raise SystemExit(f"Phase 8 validation requires tools on PATH: {', '.join(absent)}")

    with tempfile.TemporaryDirectory(prefix="ca-phase8-") as td:
        temp = Path(td)
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join(str(path) for path in PYTHON_SOURCES)
        env["CA_DATA_ROOT"] = str(temp / "data")
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONWARNINGS"] = "error::ResourceWarning"
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        checks: list[dict[str, Any]] = []

        checks.append(run([
            sys.executable, "-m", "compileall", "-q",
            "services/vae/src",
            "services/air/src",
            "services/pipeline/src",
            "services/interview/src",
            "packages/ca_contracts/src",
            "packages/ca_runtime/src",
            "packages/ca_delegation_rc4/src",
        ], env))

        phase7_report = temp / "phase7-regression.json"
        checks.append(run([sys.executable, "scripts/phase7/validate_phase7.py", "--report", str(phase7_report)], env, timeout=1800))

        phase8_env = dict(env)
        phase8_env["PYTHONPATH"] = os.pathsep.join([str(ROOT / "tests" / "phase8"), *(str(path) for path in PYTHON_SOURCES)])
        phase8_env["CA_DATA_ROOT"] = str(temp / "tests" / "phase8")
        checks.append(run([sys.executable, "-m", "pytest", "tests/phase8", "-q", "--basetemp", str(temp / "pytest-phase8")], phase8_env))

        validator_env = dict(env)
        validator_env["PYTHONPATH"] = os.pathsep.join([str(RC4 / "contracts"), str(RC4 / "validators")])
        checks.append(run([sys.executable, "-m", "pytest", "validators/tests", "-q", "--basetemp", str(temp / "pytest-delegation-validators")], validator_env, cwd=RC4))
        protocol_env = dict(env)
        protocol_env["PYTHONPATH"] = os.pathsep.join([str(RC4 / "contracts"), str(RC4 / "validators"), str(RC4 / "protocol")])
        checks.append(run([sys.executable, "-m", "pytest", "protocol/tests", "-q", "--basetemp", str(temp / "pytest-delegation-protocol")], protocol_env, cwd=RC4))

        checks.append(internal_rc4_copy_check())
        checks.append(internal_traceability_check())

        product_schemas = VAE / "contracts" / "schemas"
        packaged_schemas = VAE / "src" / "cmf_vae" / "schemas"
        product_map = {path.name: sha256(path) for path in product_schemas.glob("*.json")}
        packaged_map = {path.name: sha256(path) for path in packaged_schemas.glob("*.json")}
        schema_sync_result = "PASS" if product_map == packaged_map and len(product_map) == 17 else "FAIL"
        checks.append({
            "command": ["internal", "vae-schema-package-sync"],
            "returncode": 0 if schema_sync_result == "PASS" else 1,
            "stdout": json.dumps({"product_count": len(product_map), "packaged_count": len(packaged_map), "mismatched": sorted(name for name in set(product_map) | set(packaged_map) if product_map.get(name) != packaged_map.get(name))}, sort_keys=True),
            "stderr": "",
            "result": schema_sync_result,
        })

        schema_dir = temp / "schemas"
        schema_code = "from cmf_vae.schema_export import export_schemas; import json,sys; print(json.dumps(export_schemas(sys.argv[1]),sort_keys=True))"
        checks.append(run([sys.executable, "-c", schema_code, str(schema_dir)], env))
        schema_files = sorted(path.name for path in schema_dir.glob("*.json")) if schema_dir.exists() else []
        schema_result = "PASS" if len(schema_files) == 17 else "FAIL"
        checks.append({
            "command": ["internal", "phase8-schema-export"],
            "returncode": 0 if schema_result == "PASS" else 1,
            "stdout": json.dumps({"file_count": len(schema_files), "files": schema_files}, sort_keys=True),
            "stderr": "",
            "result": schema_result,
        })

        demo_dir = args.artifact_dir.resolve() if args.artifact_dir else temp / "demo"
        demo_dir.mkdir(parents=True, exist_ok=True)
        demo_code = "from cmf_vae.phase8_demo import run_phase8_demo; import json,sys; print(json.dumps(run_phase8_demo(sys.argv[1],sys.argv[2]),sort_keys=True))"
        checks.append(run([sys.executable, "-c", demo_code, str(demo_dir), str(RC4)], env))
        checks.append(internal_reference_artifact_check(demo_dir))

        result = "PASS" if all(check["result"] == "PASS" for check in checks) else "FAIL"
        report = {
            "schema_version": "ca-phase08-validation-report/v1",
            "validated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "phase": "PHASE_08_DELEGATION_VAE_INTEGRATION",
            "result": result,
            "checks": checks,
            "metadata": {
                "phase8_pytest_count": 24,
                "delegation_validator_test_count": 83,
                "delegation_validator_subtest_count": 16,
                "delegation_protocol_test_count": 35,
                "vae_schema_file_count": len(schema_files),
                "reference_demo_file_count": len([path for path in demo_dir.iterdir() if path.is_file()]),
                "real_sam3_executed": False,
                "real_lucida_executed": False,
                "real_comfyui_worker_executed": False,
                "real_google_gnm_executed": False,
            },
            "spec_scope": [
                "TS-DEL-001", "TS-VAE-BOUND-001",
                *[f"TS-VAE-{index:02d}" for index in range(1, 10)],
                "TS-DLG-01", "TS-DLG-03", "TS-DLG-05", "TS-DLG-06", "TS-DLG-08", "TS-DLG-09", "TS-REL-002",
            ],
            "claim_ceiling": "PHASE_08_DELEGATION_VAE_INTEGRATION_DEVELOPMENT_EVIDENCE",
            "full_spec_completion_claimed": False,
            "production_authorized": False,
            "certified": False,
            "format02_activated": False,
            "vae_stage5_started": False,
        }
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
        print(rendered, end="")
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(rendered, encoding="utf-8")
        return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
