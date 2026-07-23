from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from _paths import add_phase1_python_paths, repo_root

ROOT = repo_root()
add_phase1_python_paths(ROOT)


def run(command: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=cwd or ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    return {
        "command": command,
        "cwd": str(cwd or ROOT),
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    results: list[dict[str, object]] = []
    contract_root = ROOT / "CMF_PROGRAM_CONTROL" / "02_CROSS_REPO_CONTRACTS" / "activative-production-spine" / "0.1.0-dev.1"
    results.append(run([sys.executable, str(contract_root / "scripts" / "validate_contracts.py")]))

    results.append(run([sys.executable, "-m", "unittest", "discover", "-s", "tests/phase1", "-v"]))

    with tempfile.TemporaryDirectory(prefix="ca-phase1-install-") as install_temp:
        venv_path = Path(install_temp) / "venv"
        results.append(run([
            sys.executable,
            str(ROOT / "scripts" / "phase1" / "install_workspace.py"),
            "--venv",
            str(venv_path),
        ]))
        venv_python = venv_path / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        if venv_python.exists():
            results.append(run([
                str(venv_python),
                "-c",
                "import ca_contracts,ca_runtime,cmf_activative_intelligence,cmf_pipeline,conscious_activations_interview_expression;print('clean workspace import: PASS')",
            ]))

    studio = ROOT / "07_CONSCIOUS_ACTIVATIONS_STUDIO"
    tsc = shutil.which("tsc")
    if tsc:
        results.append(run([tsc, "-p", "tsconfig.json"], cwd=studio))
    else:
        results.append({
            "command": ["tsc", "-p", "tsconfig.json"],
            "cwd": str(studio),
            "returncode": 0,
            "stdout": "",
            "stderr": "typescript compiler unavailable; committed dist artifact smoke-tested instead",
            "classification": "TOOL_NOT_AVAILABLE_NONBLOCKING_FOR_APPLY",
        })
    node = shutil.which("node")
    if not node:
        results.append({
            "command": ["node"],
            "cwd": str(studio),
            "returncode": 1,
            "stdout": "",
            "stderr": "Node.js is required for the Studio Phase 1 shell",
        })
    else:
        results.append(run([node, "tests/health.test.mjs"], cwd=studio))
        results.append(run([node, "dist/index.js", "health", "--json"], cwd=studio))

    with tempfile.TemporaryDirectory(prefix="ca-phase1-bootstrap-") as temp_dir:
        results.append(run([
            sys.executable,
            str(ROOT / "scripts" / "phase1" / "bootstrap_products.py"),
            "--data-root",
            temp_dir,
            "--json",
        ]))

    failed = [item for item in results if item["returncode"] != 0]
    report = {
        "schema_version": "ca-phase1-validation/v1",
        "result": "PASS" if not failed else "FAIL",
        "checks": results,
        "failed_check_count": len(failed),
        "production_authorized": False,
        "certified": False,
        "format02_activated": False,
        "vae_stage5_started": False,
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        target = args.report if args.report.is_absolute() else ROOT / args.report
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
