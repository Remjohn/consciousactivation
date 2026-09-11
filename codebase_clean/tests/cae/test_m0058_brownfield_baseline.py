"""CAE-M0058 executable brownfield reconciliation and product-run baseline tests."""
from __future__ import annotations

import sys
import types
from pathlib import Path
from typing import Any

# The sandbox image does not ship psycopg. M0058 must still exercise the SQLite
# product path without pretending that PostgreSQL is reachable.
try:
    import psycopg  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover - environment guard
    mod = types.ModuleType("psycopg")
    mod.Connection = Any
    mod.Cursor = Any
    mod.connect = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("psycopg unavailable in M0058 sandbox"))
    types_mod = types.ModuleType("psycopg.types")
    json_mod = types.ModuleType("psycopg.types.json")
    json_mod.Jsonb = lambda value: value
    types_mod.json = json_mod
    mod.types = types_mod
    sys.modules.update({"psycopg": mod, "psycopg.types": types_mod, "psycopg.types.json": json_mod})

import json


from ca_runtime.brownfield_baseline import (
    INVARIANT,
    MANDATE_ID,
    PathStatus,
    build_ledger,
    inventory_programs,
    run_minimal_product_probe,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_PROGRAM_COUNT = 17


def test_m0058_inventory_covers_all_programs_and_classifies_boundaries() -> None:
    rows = inventory_programs(REPO_ROOT)
    assert len(rows) == EXPECTED_PROGRAM_COUNT

    research = next(row for row in rows if row.program_id == "research_canonicalization_program")
    assert research.runtime_state_machine_registered is True
    assert research.harness == "RESEARCH_CANONICALIZATION_HARNESS_V1"
    assert research.classification is PathStatus.PARTIAL
    assert "no separate executable binding/package" in research.limitation


def test_m0058_probe_performs_real_operator_runtime_and_persistent_state_transition() -> None:
    probe = run_minimal_product_probe(REPO_ROOT, workspace_id="m0058-test-workspace")

    assert probe["run"]["success"] is True
    assert probe["run"]["current_state"] == "INITIAL"
    assert probe["run"]["lifecycle"] == "RUNNING"
    assert probe["dispatch_persistence"]["lease_present"] is True
    assert probe["dispatch_persistence"]["workflow_dispatch_present"] is True
    assert probe["gate"]["gate_id"] == "canonical_knowledge_commit_gate"
    assert probe["gate"]["current_state"] == "INITIAL"
    assert probe["gate"]["lifecycle"] == "AWAITING_APPROVAL"
    assert probe["gate"]["suspension_present"] is True
    assert probe["trace"]["trace_node_count"] >= 1
    assert probe["release"]["success"] is False
    assert probe["release"]["blocked_after_gate"] is True
    assert probe["persistence_recheck"]["aggregate_present"] is True
    assert probe["persistence_recheck"]["same_state_hash"] is True


def test_m0058_ledger_contains_required_status_classes_and_executable_proof() -> None:
    ledger = build_ledger(REPO_ROOT, source_git_commit="c41b68394ba8d1435c3cbb62b08f38908bbd3737")

    assert ledger.mandate_id == MANDATE_ID
    assert ledger.invariant == INVARIANT
    assert len(ledger.paths) >= 11
    statuses = {path.status for path in ledger.paths}
    assert {PathStatus.WORKING, PathStatus.PARTIAL, PathStatus.MOCKED, PathStatus.UNREACHABLE, PathStatus.CONFLICTING} <= statuses

    by_id = {path.path_id: path for path in ledger.paths}
    assert by_id["P01"].evidence_class.value == "EXECUTABLE"
    assert by_id["P03"].status is PathStatus.UNREACHABLE
    assert by_id["P11"].status is PathStatus.MOCKED
    assert by_id["P05"].status is PathStatus.CONFLICTING
    assert by_id["P09"].status is PathStatus.CONFLICTING

    assert ledger.probe["run"]["lifecycle"] == "RUNNING"
    assert ledger.probe["gate"]["lifecycle"] == "AWAITING_APPROVAL"
    assert ledger.probe["release"]["blocked_after_gate"] is True
    blocker_ids = {item["id"] for item in ledger.blockers}
    assert {"B-M0058-RUNTIME-001", "B-M0058-HARNESS-001", "B-M0058-AUTH-001", "B-M0058-PROOF-001"} <= blocker_ids


def test_m0058_false_proof_countercase_names_existing_dispatch_only_benchmark() -> None:
    ledger = build_ledger(REPO_ROOT, source_git_commit="c41b68394ba8d1435c3cbb62b08f38908bbd3737")
    countercase = ledger.false_proof_countercase
    assert "M71 benchmark" in countercase
    assert "successful command dispatch" in countercase
    assert "never executing the intended" in countercase


def test_m0058_markdown_and_json_are_self_consistent() -> None:
    ledger = build_ledger(REPO_ROOT, source_git_commit="c41b68394ba8d1435c3cbb62b08f38908bbd3737")
    payload = ledger.to_dict()
    markdown = ledger.to_markdown()

    assert payload["mandate_id"] == MANDATE_ID
    assert payload["invariant"] == INVARIANT
    assert payload["source_git_commit"] == "c41b68394ba8d1435c3cbb62b08f38908bbd3737"
    assert "## Reachable-call-path ledger" in markdown
    assert "## Stateful behavior evidence" in markdown
    assert "## Verification boundary" in markdown
    assert "**WORKING**" in markdown
    assert "**MOCKED**" in markdown
    assert "**UNREACHABLE**" in markdown
    assert "**CONFLICTING**" in markdown
    assert json.loads(json.dumps(payload))["probe"]["gate"]["lifecycle"] == "AWAITING_APPROVAL"


def test_m0058_probe_is_durable_across_two_independent_runs() -> None:
    first = run_minimal_product_probe(REPO_ROOT, workspace_id="m0058-durable-1")
    second = run_minimal_product_probe(REPO_ROOT, workspace_id="m0058-durable-2")

    assert first["aggregate_id"] != second["aggregate_id"]
    for probe in (first, second):
        assert probe["persistence_recheck"]["aggregate_present"] is True
        assert probe["persistence_recheck"]["transition_count"] >= probe["dispatch_persistence"]["transition_count_after_dispatch"]
        assert probe["gate"]["receipt_id"]
        assert probe["gate"]["audit_digest"]

def test_m0058_control_state_and_evidence_artifacts_are_present() -> None:
    control = REPO_ROOT / "docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md"
    baseline_md = REPO_ROOT / "docs/cae/implementation/CAE_M0058_BROWNFIELD_BASELINE.md"
    baseline_json = REPO_ROOT / "docs/cae/implementation/CAE_M0058_BROWNFIELD_BASELINE.json"

    control_text = control.read_text(encoding="utf-8")
    payload = json.loads(baseline_json.read_text(encoding="utf-8"))

    assert "mandate_id: CAE-M0058" in control_text
    assert "control_status: PENDING_OPERATOR_DECISION" in control_text
    assert "Do you accept M0058 and authorize M0059/M0060?" in control_text
    assert baseline_md.exists()
    assert payload["mandate_id"] == "CAE-M0058"
    assert len(payload["program_inventory"]) == EXPECTED_PROGRAM_COUNT

