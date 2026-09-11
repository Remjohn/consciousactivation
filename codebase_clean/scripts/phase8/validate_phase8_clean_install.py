from __future__ import annotations

import argparse
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
SOURCE_PACKAGES = [
    (ROOT / "packages" / "ca_contracts", "ca_contracts"),
    (ROOT / "packages" / "ca_runtime", "ca_runtime"),
    (ROOT / "packages" / "ca_delegation_rc4", "ca_delegation_rc4"),
    (ROOT / "services/air", "air"),
    (ROOT / "services/pipeline", "pipeline"),
    (ROOT / "services/interview", "interview"),
    (ROOT / "services/vae", "vae"),
]


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if shutil.which("node") is None or shutil.which("npm") is None or shutil.which("tsc") is None:
        raise SystemExit("Phase 8 clean-install proof requires node, npm and tsc")

    with tempfile.TemporaryDirectory(prefix="ca-phase8-install-") as td:
        temp = Path(td)
        install = temp / "install"
        build = temp / "build"
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONWARNINGS"] = "error::ResourceWarning"
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
        checks: list[dict[str, Any]] = []

        phase7_report = temp / "phase7-clean-install.json"
        checks.append(run([sys.executable, str(ROOT / "scripts" / "phase7" / "validate_phase7_clean_install.py"), "--report", str(phase7_report)], env, ROOT))

        copied: list[Path] = []
        for source, name in SOURCE_PACKAGES:
            destination = build / name
            shutil.copytree(source, destination, ignore=shutil.ignore_patterns("build", "dist", "*.egg-info", "__pycache__", "*.pyc", ".pytest_cache", "node_modules"))
            copied.append(destination)
        checks.append(run([
            sys.executable, "-m", "pip", "install", "--quiet", "--no-deps", "--no-build-isolation", "--target", str(install),
            *(str(path) for path in copied),
        ], env, ROOT))

        demo = temp / "demo"
        schemas = temp / "schemas"
        data_root = temp / "runtime-data"
        clean_env = dict(env)
        clean_env["PYTHONPATH"] = str(install)
        clean_env["CA_REPO_ROOT"] = str(ROOT)
        clean_env["CA_DATA_ROOT"] = str(data_root)
        checks.append(run([sys.executable, "-m", "cmf_vae", "--repo", str(ROOT), "health", "--db", str(data_root / "vae.sqlite3"), "--storage", str(data_root / "storage")], clean_env, ROOT))
        checks.append(run([sys.executable, "-m", "cmf_vae", "--repo", str(ROOT), "export-schemas", "--output-dir", str(schemas)], clean_env, ROOT))
        checks.append(run([sys.executable, "-m", "cmf_vae", "--repo", str(ROOT), "demo", "--output-dir", str(demo)], clean_env, ROOT))

        expected_demo = {"reference-visual-asset.png", "asset-result.json", "result-acknowledgement.json", "demo-receipt.json"}
        demo_files = {path.name for path in demo.iterdir() if path.is_file()} if demo.exists() else set()
        schema_files = {path.name for path in schemas.glob("*.json")} if schemas.exists() else set()
        internal_pass = expected_demo <= demo_files and len(schema_files) == 17
        checks.append({
            "command": ["internal", "clean-install-artifacts"],
            "returncode": 0 if internal_pass else 1,
            "stdout": json.dumps({"demo_files": sorted(demo_files), "schema_count": len(schema_files)}, sort_keys=True),
            "stderr": "",
            "result": "PASS" if internal_pass else "FAIL",
        })

        result = "PASS" if all(check["result"] == "PASS" for check in checks) else "FAIL"
        report = {
            "schema_version": "ca-phase08-clean-install-report/v1",
            "validated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "result": result,
            "checks": checks,
            "installed_packages": [name for _, name in SOURCE_PACKAGES],
            "claim_ceiling": "PHASE_08_DELEGATION_VAE_INTEGRATION_DEVELOPMENT_EVIDENCE",
            "production_authorized": False,
            "certified": False,
        }
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
        print(rendered, end="")
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(rendered, encoding="utf-8")
        return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
