from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STUDIO = ROOT / "07_CONSCIOUS_ACTIVATIONS_STUDIO"
SCHEMAS = STUDIO / "contracts" / "schemas"
PYTHON_SOURCES = [
    ROOT / "packages" / "ca_contracts" / "src",
    ROOT / "packages" / "ca_runtime" / "src",
    ROOT / "04_ACTIVATIVE_INTELLIGENCE_RUNTIME" / "src",
    ROOT / "05_ATOMIC_HARNESS_PIPELINE" / "src",
    ROOT / "06_INTERVIEW_EXPRESSION" / "src",
]


def run(command: list[str], env: dict[str, str], cwd: Path = ROOT, timeout: int = 900) -> dict[str, Any]:
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


def schema_validation(demo_dir: Path, env: dict[str, str]) -> dict[str, Any]:
    code = r'''
import copy, json, sys
from pathlib import Path
from ca_contracts.validation import ContractValidationError, SchemaRegistry

schema_dir = Path(sys.argv[1])
demo = Path(sys.argv[2])
registry = SchemaRegistry(schema_dir=schema_dir)
control = json.loads((demo / "control-tower.json").read_text(encoding="utf-8"))
change = json.loads((demo / "change-request-program.json").read_text(encoding="utf-8"))
rerun = json.loads((demo / "selective-rerun-request.json").read_text(encoding="utf-8"))
episode = json.loads((demo / "human-resolution-episode.json").read_text(encoding="utf-8"))
programming = json.loads((demo / "programming-material-record.json").read_text(encoding="utf-8"))
ship = json.loads((demo / "ship-decision.json").read_text(encoding="utf-8"))
audit = json.loads((demo / "audit-export.json").read_text(encoding="utf-8"))

payloads = {
    "control_tower_projection": control,
    "campaign_order": control["order"],
    "campaign_state": control["campaign"],
    "studio_surface_binding": control["studio_binding"],
    "timeline_projection": control["timeline"],
    "autonomy_policy": control["order"]["autonomy_policy"],
    "change_request_program": change,
    "selective_rerun_request": rerun,
    "human_resolution_episode": episode,
    "programming_material_record": programming,
    "ship_decision": ship,
    "audit_export_manifest": audit,
}
for name, payload in payloads.items():
    registry.validate(name, payload)

# The remaining four contract families receive exact bounded fixtures.
ref = control["source_package_ref"]
actor = control["order"]["operator_actor"]
operator_request = {
    "request_id": "request:schema-proof",
    "run_ref": ref,
    "target_refs": [ref],
    "target_node_ids": ["node:supervisual-render"],
    "category_id": "static_composition",
    "natural_language_request": "move the title left by 5%",
    "current_state_ref": ref,
    "evaluation_ref": ref,
    "jit_capsule_ref": ref,
    "permitted_tool_registry_ref": ref,
    "operator_actor": actor,
    "expected_state_version": 1,
}
direct = {
    "delta_id": "delta:schema-proof",
    "run_ref": ref,
    "target_ref": ref,
    "target_node_id": "node:supervisual-render",
    "manipulation_type": "MOVE_BBOX",
    "arguments": {"axis": "x", "delta_micros": -50000, "mode": "NORMALIZED_MICROS"},
    "current_state_ref": ref,
    "operator_actor": actor,
    "expected_state_version": 1,
}
exception = {
    "package_id": "exception:schema-proof",
    "campaign_ref": ref,
    "exception_code": "TASTE_BOUNDARY",
    "responsible_product": "conscious-activations-studio",
    "summary": "Operator decision required",
    "evidence_refs": [ref],
    "candidate_refs": [ref],
    "allowed_decisions": ["APPROVE", "REQUEST_REVISION"],
    "recommended_next_actions": ["review candidates"],
}
ship_request = {
    "ship_request_id": "ship-request:schema-proof",
    "campaign_ref": ref,
    "autonomy_mode": control["campaign"]["autonomy_mode"],
    "target_channel": "development-export",
    "artifact_refs": control["artifacts"],
    "evaluation_refs": control["evaluations"],
    "unresolved_exception_ids": [],
    "operator_actor": actor,
    "publication_authority_ref": ref,
    "publication_policy_ref": ref,
}
for name, payload in {
    "operator_revision_request": operator_request,
    "direct_manipulation_delta": direct,
    "exception_review_package": exception,
    "ship_request": ship_request,
}.items():
    registry.validate(name, payload)

invalid = copy.deepcopy(change)
invalid["unexpected_governed_field"] = True
try:
    registry.validate("change_request_program", invalid)
except ContractValidationError:
    pass
else:
    raise SystemExit("closed schema accepted an unknown field")

print(json.dumps({"result": "PASS", "schema_count": len(registry.schema_names), "validated_payloads": 16, "unknown_field_rejected": True}, sort_keys=True))
'''
    return run([sys.executable, "-c", code, str(SCHEMAS), str(demo_dir)], env)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if shutil.which("node") is None or shutil.which("npm") is None:
        raise SystemExit("Phase 7 validation requires node and npm on PATH")

    with tempfile.TemporaryDirectory(prefix="ca-phase7-") as td:
        temp = Path(td)
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join(str(path) for path in PYTHON_SOURCES)
        env["CA_DATA_ROOT"] = str(temp / "data")
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONWARNINGS"] = "error::ResourceWarning"
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        checks: list[dict[str, Any]] = []

        checks.append(run([
            sys.executable,
            "-m",
            "compileall",
            "-q",
            "04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src",
            "05_ATOMIC_HARNESS_PIPELINE/src",
            "06_INTERVIEW_EXPRESSION/src",
            "packages/ca_contracts/src",
            "packages/ca_runtime/src",
        ], env))

        checks.append(run(["npm", "run", "build"], env, cwd=STUDIO))

        phase6_report = temp / "phase6-regression.json"
        checks.append(run([sys.executable, "scripts/phase6/validate_phase6.py", "--report", str(phase6_report)], env, timeout=1200))

        phase7_env = dict(env)
        phase7_env["PYTHONPATH"] = os.pathsep.join([str(ROOT / "tests/phase7"), *(str(item) for item in PYTHON_SOURCES)])
        phase7_env["CA_DATA_ROOT"] = str(temp / "tests" / "phase7")
        checks.append(run([sys.executable, "-m", "pytest", "tests/phase7", "-q", "--basetemp", str(temp / "pytest-phase7")], phase7_env))

        checks.append(run(["npm", "test"], env, cwd=STUDIO))
        demo_dir = temp / "demo"
        checks.append(run(["node", "dist/index.js", "demo", "--output-dir", str(demo_dir), "--json"], env, cwd=STUDIO))
        checks.append(schema_validation(demo_dir, env))

        required_demo_files = {
            "control-tower.json",
            "studio-control-tower.html",
            "change-request-program.json",
            "selective-rerun-request.json",
            "human-resolution-episode.json",
            "human-resolution-ledger.ndjson",
            "programming-material-record.json",
            "ship-decision.json",
            "audit-export.json",
        }
        observed_demo_files = {path.name for path in demo_dir.iterdir() if path.is_file()} if demo_dir.exists() else set()
        demo_result = "PASS" if required_demo_files <= observed_demo_files else "FAIL"
        checks.append({
            "command": ["internal", "reference-demo-artifact-check"],
            "returncode": 0 if demo_result == "PASS" else 1,
            "stdout": json.dumps({"required": sorted(required_demo_files), "observed": sorted(observed_demo_files)}),
            "stderr": "",
            "result": demo_result,
        })

        result = "PASS" if all(check["result"] == "PASS" for check in checks) else "FAIL"
        report = {
            "schema_version": "ca-phase07-validation-report/v1",
            "validated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "phase": "PHASE_07_STUDIO_SUPERVISION",
            "result": result,
            "checks": checks,
            "metadata": {
                "studio_contract_schema_count": 16,
                "studio_node_test_count": 20,
                "reference_demo_file_count": len(observed_demo_files),
                "external_model_calls": 0,
                "live_pipeline_calls": 0,
                "live_publication_calls": 0,
            },
            "spec_scope": ["TS-CAS-001", "TS-CAS-002", "TS-CAS-003", "TS-CAS-004", "TS-CAS-005", "TS-CAS-006"],
            "claim_ceiling": "PHASE_07_STUDIO_SUPERVISION_DEVELOPMENT_EVIDENCE",
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
