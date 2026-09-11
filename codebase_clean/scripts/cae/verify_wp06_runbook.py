"""Verify WP-06 procedural doctrine against the registered staging contracts."""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urlsplit

import psycopg
import yaml


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs" / "cae" / "runbooks" / "evidence_to_air_first_slice_v1.yaml"
SKILL = ROOT / "docs" / "cae" / "skills" / "EVIDENCE_TO_AIR_FIRST_SLICE_SKILL.md"
ENVIRONMENT_VARIABLE = "CAE_SUPABASE_DATABASE_URL"
PROJECT_REF = "evnxdssbxxrsesftdvgx"


def load_local_environment() -> None:
    for line in (ROOT / ".env").read_text(encoding="utf-8-sig").splitlines():
        key, separator, value = line.partition("=")
        if separator and key and not key.lstrip().startswith("#"):
            os.environ.setdefault(key.strip(), value.strip())


def connection_url() -> str:
    url = os.environ.get(ENVIRONMENT_VARIABLE, "")
    parsed = urlsplit(url)
    if not (parsed.hostname and parsed.hostname.endswith(".pooler.supabase.com") and parsed.port == 5432 and parsed.username == f"postgres.{PROJECT_REF}"):
        raise RuntimeError("connection is not the approved CAE staging session pooler")
    return url


def main() -> int:
    runbook = yaml.safe_load(RUNBOOK.read_text(encoding="utf-8"))
    skill = SKILL.read_text(encoding="utf-8")
    states = {state["state_id"]: state for state in runbook["states"]}
    operation_bindings: set[str] = set()
    contract_bindings: set[str] = set()
    for state in states.values():
        operation_bindings.update(state.get("allowed_operations", []))
        contract = state.get("transition_contract")
        if contract:
            contract_bindings.add(contract)
        contract_bindings.update(state.get("transition_contracts", []))
    expected_operations = {
        "cae.evidence.capture@1.0.0", "cae.evidence.authenticate@1.0.0",
        "cae.air.propose-assessment@1.0.0", "cae.air.validate-assessment@1.0.0",
        "cae.air.confirm-assessment@1.0.0",
    }
    expected_contracts = {"STC-EVID-000@1.0.0", "STC-EVID-001@1.0.0", "STC-AIR-000@1.0.0", "STC-AIR-001@1.0.0", "STC-AIR-002@1.0.0"}
    load_local_environment()
    with psycopg.connect(connection_url(), connect_timeout=10) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT operation_id || '@' || operation_version FROM cae.semantic_operation ORDER BY operation_id")
            registered_operations = {row[0] for row in cursor.fetchall()}
            cursor.execute("SELECT contract_id || '@' || contract_version FROM cae.state_transition_contract WHERE active = true ORDER BY contract_id")
            registered_contracts = {row[0] for row in cursor.fetchall()}
    checks = {
        "runbook_identity": runbook["runbook_id"] == "cae.evidence_to_air_first_slice" and runbook["version"] == "1.0.0",
        "no_shadow_state": runbook["authority_boundary"]["prohibited_shadow_state"] == "local runbook state, prompt memory, or Harness IR",
        "operation_bindings": operation_bindings == expected_operations and expected_operations <= registered_operations,
        "contract_bindings": contract_bindings == expected_contracts and expected_contracts <= registered_contracts,
        "state_machine": runbook["initial_state"] == "RECON" and set(runbook["terminal_states"]) == {"COMPLETE", "BLOCKED", "REPAIR_REQUIRED", "FAILED"},
        "recovery_and_countertests": "stale expected version must create no event or receipt" in runbook["fidelity_and_reward_hack_checks"],
        "skill_boundary": "registry-neutral" in skill and "not turn a\n   missing decision into `COMPLETE`" in skill,
    }
    for name, passed in checks.items():
        print(f"{name}={'PASS' if passed else 'FAIL'}")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
