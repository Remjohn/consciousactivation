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
PYTHONPATH_PARTS = (
    ROOT / "tests" / "phase2",
    ROOT / "tests" / "phase1",
    ROOT / "packages" / "ca_contracts" / "src",
    ROOT / "packages" / "ca_runtime" / "src",
    ROOT / "04_ACTIVATIVE_INTELLIGENCE_RUNTIME" / "src",
    ROOT / "05_ATOMIC_HARNESS_PIPELINE" / "src",
    ROOT / "06_INTERVIEW_EXPRESSION" / "src",
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run(command: list[str], *, env: dict[str, str], cwd: Path = ROOT) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "result": "PASS" if completed.returncode == 0 else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="ca-phase2-") as temp_dir:
        temp = Path(temp_dir)
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join(str(path) for path in PYTHONPATH_PARTS)
        env["CA_DATA_ROOT"] = str(temp / "data")
        checks: list[dict[str, Any]] = []

        checks.append(run([sys.executable, "-m", "compileall", "-q", "04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src"], env=env))
        checks.append(run([sys.executable, "-m", "pytest", "tests/phase1", "tests/phase2", "-q"], env=env))
        checks.append(run([sys.executable, "-m", "cmf_activative_intelligence", "bootstrap", "--json"], env=env))
        checks.append(run([sys.executable, "-m", "cmf_activative_intelligence", "load-registries", "--json"], env=env))
        checks.append(run([sys.executable, "-m", "cmf_activative_intelligence", "demo", "--json"], env=env))
        schema_dir = temp / "schemas"
        checks.append(run([sys.executable, "-m", "cmf_activative_intelligence", "export-schemas", str(schema_dir), "--json"], env=env))

        install_root = temp / "install"
        build_sources = temp / "build-sources"
        source_specs = (
            (ROOT / "packages" / "ca_contracts", build_sources / "ca_contracts"),
            (ROOT / "packages" / "ca_runtime", build_sources / "ca_runtime"),
            (ROOT / "04_ACTIVATIVE_INTELLIGENCE_RUNTIME", build_sources / "air"),
        )
        for source, target in source_specs:
            shutil.copytree(
                source,
                target,
                ignore=shutil.ignore_patterns("build", "dist", "*.egg-info", "__pycache__", "*.pyc", "*.pyo"),
            )
        checks.append(
            run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--quiet",
                    "--no-deps",
                    "--no-build-isolation",
                    "--target",
                    str(install_root),
                    str(build_sources / "ca_contracts"),
                    str(build_sources / "ca_runtime"),
                    str(build_sources / "air"),
                ],
                env=env,
            )
        )
        clean_env = dict(env)
        clean_env["PYTHONPATH"] = str(install_root)
        clean_env["CA_DATA_ROOT"] = str(temp / "clean-data")
        checks.append(run([sys.executable, "-m", "cmf_activative_intelligence", "demo", "--json"], env=clean_env))

        schema_count = len(list(schema_dir.glob("*.schema.json"))) if schema_dir.exists() else 0
        metadata = {
            "schema_count": schema_count,
            "expected_schema_count": 17,
            "schema_result": "PASS" if schema_count == 17 else "FAIL",
        }
        transient = [
            str(path.relative_to(ROOT)).replace("\\", "/")
            for path in ROOT.rglob("*")
            if path.name in {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
            or (path.is_file() and path.suffix in {".pyc", ".pyo"})
        ]
        # Existing caches are reported but not treated as code validation failures; bundle creation removes them.
        result = "PASS" if all(item["result"] == "PASS" for item in checks) and metadata["schema_result"] == "PASS" else "FAIL"
        report = {
            "schema_version": "ca-phase02-validation-report/v1",
            "validated_at_utc": now(),
            "phase": "PHASE_02_DETERMINISTIC_SEMANTIC_CORE",
            "result": result,
            "checks": checks,
            "metadata": metadata,
            "transient_paths_observed_before_bundle_cleanup": transient,
            "claim_ceiling": "AIR_PHASE_02_CORE_IMPLEMENTED_DEVELOPMENT_PASS",
            "external_model_calls": 0,
            "real_human_evidence_claimed": False,
            "production_authorized": False,
            "certified": False,
            "format02_activated": False,
        }
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
