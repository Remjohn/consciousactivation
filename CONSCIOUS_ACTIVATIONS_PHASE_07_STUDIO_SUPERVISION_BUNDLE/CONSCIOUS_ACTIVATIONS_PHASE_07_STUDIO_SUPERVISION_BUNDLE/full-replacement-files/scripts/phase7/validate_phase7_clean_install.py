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
STUDIO = ROOT / "07_CONSCIOUS_ACTIVATIONS_STUDIO"


def run(command: list[str], env: dict[str, str], cwd: Path, timeout: int = 900) -> dict[str, Any]:
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
    if shutil.which("node") is None or shutil.which("npm") is None:
        raise SystemExit("Phase 7 clean-install proof requires node and npm")

    with tempfile.TemporaryDirectory(prefix="ca-phase7-install-") as td:
        temp = Path(td)
        studio_copy = temp / "studio"
        shutil.copytree(
            STUDIO,
            studio_copy,
            ignore=shutil.ignore_patterns("dist", "node_modules", "phase7-demo-output", ".DS_Store"),
        )
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONWARNINGS"] = "error::ResourceWarning"
        phase6_report = temp / "phase6-clean-install.json"
        checks = [
            run([sys.executable, str(ROOT / "scripts" / "phase6" / "validate_phase6_clean_install.py"), "--report", str(phase6_report)], env, ROOT),
            run(["npm", "run", "build"], env, studio_copy),
            run(["npm", "test"], env, studio_copy),
            run(["node", "dist/index.js", "health", "--json"], env, studio_copy),
            run(["node", "dist/index.js", "demo", "--output-dir", str(temp / "demo"), "--json"], env, studio_copy),
        ]
        result = "PASS" if all(check["result"] == "PASS" for check in checks) else "FAIL"
        report = {
            "schema_version": "ca-phase07-clean-install-report/v1",
            "validated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "result": result,
            "checks": checks,
            "claim_ceiling": "PHASE_07_STUDIO_SUPERVISION_DEVELOPMENT_EVIDENCE",
        }
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
        print(rendered, end="")
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(rendered, encoding="utf-8")
        return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
