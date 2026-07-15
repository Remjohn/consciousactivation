#!/usr/bin/env python3
"""Copy a release candidate to an isolated directory and run every shipped gate."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path


def run(command: list[str], cwd: Path, env: dict[str, str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": " ".join(command),
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def transient_paths(root: Path) -> list[str]:
    result: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if (
            bool({".pytest_cache", "__pycache__"}.intersection(relative.parts))
            or relative.name in {".DS_Store", "Thumbs.db", "desktop.ini"}
            or relative.suffix.lower() in {".pyc", ".pyo", ".tmp", ".temp", ".swp", ".swo"}
            or relative.name.endswith("~")
        ):
            result.append(relative.as_posix())
    return sorted(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    candidate = args.candidate.resolve()
    if not (candidate / "RELEASE_RECEIPT.json").is_file():
        raise SystemExit(f"Not a sealed release candidate: {candidate}")

    with tempfile.TemporaryDirectory(prefix="delegation-rc4-clean-room-") as temp:
        clean_root = Path(temp) / candidate.name
        shutil.copytree(candidate, clean_root)
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONPATH"] = os.pathsep.join(
            [
                str(clean_root / "validators"),
                str(clean_root / "protocol"),
                str(clean_root / "contracts/generated/python"),
            ]
        )
        commands = [
            [sys.executable, "-B", "validators/run_release_validation.py"],
            [
                sys.executable,
                "-B",
                "-m",
                "unittest",
                "discover",
                "-s",
                "validators/tests",
                "-q",
            ],
            [
                sys.executable,
                "-B",
                "-m",
                "pytest",
                "protocol/tests",
                "-q",
                "-p",
                "no:cacheprovider",
            ],
        ]
        results = [run(command, clean_root, env) for command in commands]
        transients = transient_paths(clean_root)
        status = "PASS" if all(item["exit_code"] == 0 for item in results) and not transients else "FAIL"
        validator_text = results[1]["stdout"] + results[1]["stderr"]
        protocol_text = results[2]["stdout"] + results[2]["stderr"]
        validator_match = re.search(r"Ran (\d+) tests", validator_text)
        protocol_match = re.search(r"(\d+) passed", protocol_text)
        report = {
            "validated_at": date.today().isoformat(),
            "candidate_source": str(candidate),
            "validation_environment": "temporary clean release-only copy",
            "source_repository_available_to_tests": False,
            "status": status,
            "validator_tests": int(validator_match.group(1)) if validator_match else None,
            "protocol_tests": int(protocol_match.group(1)) if protocol_match else None,
            "transient_files_after_validation": transients,
            "gates": [
                {
                    "command": item["command"],
                    "exit_code": item["exit_code"],
                    "stdout_tail": item["stdout"][-4000:],
                    "stderr_tail": item["stderr"][-4000:],
                }
                for item in results
            ],
        }
        print(json.dumps(report, indent=2))
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
