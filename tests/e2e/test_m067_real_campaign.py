"""Automated proof-contract tests for CAE-M067.

These tests never replace the OpenChatCut runtime. They validate the evidence
contract, fail-closed environment behavior, and M0064 lineage false-proof cases.
The decisive live campaign is executed only when a real OpenChatCut endpoint and
real source/program/evidence inputs are supplied by the environment.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from tests.e2e.m067_real_campaign_harness import (
    EXPECTED_STATE_SEQUENCE,
    INVARIANT,
    MANDATE_ID,
    REQUIRED_CHECKPOINTS,
    EvidenceLedger,
    assert_no_mock_runtime,
    environment_fidelity,
    run_local_adversarial_proof,
    write_blocked_live_evidence,
)


def test_m067_manifest_defines_required_real_campaign_checkpoints(tmp_path: Path) -> None:
    ledger = EvidenceLedger(tmp_path, "m067-test")
    ledger.add(
        checkpoint="semantic_intent",
        status="PASS",
        evidence_class="TEST",
        actor="test",
        state_before="CAMPAIGN_READY",
        state_after="EXECUTING",
        command="test",
        inputs={"intent": "proof"},
        outputs={"accepted": True},
    )
    manifest = ledger.finalize(terminal_state="EXECUTING", status="TEST_ONLY", limitations=["live runtime not exercised"])
    assert manifest["mandate_id"] == MANDATE_ID
    assert manifest["invariant"] == INVARIANT
    assert manifest["required_checkpoints"] == list(REQUIRED_CHECKPOINTS)
    assert manifest["captured_checkpoints"] == ["semantic_intent"]
    assert manifest["manifest_sha256"]
    assert (tmp_path / "evidence-ledger.jsonl").read_text(encoding="utf-8").count("\n") == 1


def test_m067_state_sequence_matches_mandate() -> None:
    assert EXPECTED_STATE_SEQUENCE == (
        "CAMPAIGN_READY",
        "EXECUTING",
        "OPERATOR_GATE",
        "RELEASE_READY",
    )


def test_m067_no_mock_runtime_endpoint_is_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENCHATCUT_MCP_URL", "http://localhost:5199/api/external-mcp/mcp")
    assert_no_mock_runtime()
    monkeypatch.setenv("OPENCHATCUT_MCP_URL", "http://mock-host:5199/api/external-mcp/mcp")
    with pytest.raises(Exception, match="non-native OpenChatCut"):
        assert_no_mock_runtime()


def test_m067_environment_fidelity_records_missing_live_runtime(tmp_path: Path) -> None:
    result = environment_fidelity()
    assert "python" in result
    assert "git" in result
    assert "openchatcut" in result
    assert result["openchatcut"]["endpoint"].endswith("/api/external-mcp/mcp")
    assert result["source_media"]["present"] is False or isinstance(result["source_media"]["sha256"], str)


def test_m067_adversarial_false_proofs_are_rejected(tmp_path: Path) -> None:
    result = run_local_adversarial_proof(tmp_path)
    assert result["status"] == "ADVERSARIAL_PASS"
    assert "asset_lineage_false_proof" in result["captured_checkpoints"]
    assert "selection_lineage_false_proof" in result["captured_checkpoints"]


def test_m067_adversarial_manifest_is_hash_addressed(tmp_path: Path) -> None:
    run_local_adversarial_proof(tmp_path)
    manifest = json.loads((tmp_path / "adversarial" / "evidence-manifest.json").read_text(encoding="utf-8"))
    assert len(manifest["manifest_sha256"]) == 64
    assert all(row["evidence_class"] in {"EXECUTABLE", "TEST"} for row in manifest["rows"])


def test_m067_live_mode_is_not_satisfied_by_local_fixture_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CAE_M067_SOURCE_MEDIA", raising=False)
    monkeypatch.delenv("CAE_M067_VIDEO_PROGRAM_JSON", raising=False)
    monkeypatch.delenv("CAE_M067_OPERATOR_EVIDENCE_JSON", raising=False)
    monkeypatch.delenv("CAE_M067_RELEASE_EVIDENCE_JSON", raising=False)
    fidelity = environment_fidelity()
    assert fidelity["source_media"]["present"] is False


def test_m067_blocked_live_run_preserves_every_required_checkpoint(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENCHATCUT_MCP_URL", "http://127.0.0.1:1/api/external-mcp/mcp")
    manifest = write_blocked_live_evidence(tmp_path, "native runtime unavailable")
    assert manifest["status"] == "REAL_CAMPAIGN_BLOCKED"
    assert manifest["terminal_state"] == "BLOCKED"
    assert manifest["captured_checkpoints"] == list(REQUIRED_CHECKPOINTS)
    rows = {row["checkpoint"]: row for row in manifest["rows"]}
    assert rows["native_openchatcut"]["status"] == "BLOCKED"
    assert rows["operator_intervention"]["status"] == "NOT_REACHED"
    assert rows["qa_release_evidence"]["status"] == "NOT_REACHED"
    assert rows["terminal_state"]["state_after"] == "BLOCKED"
