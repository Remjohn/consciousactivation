"""
Pure local structure test for CA-GOV-02 Formal Ratification & Control State Artifacts.
Validates ratification fields, decision IDs, and three-layer stratification without network or DB mutation.
"""

from __future__ import annotations

from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def test_ca_gov_02_artifacts_exist_and_non_empty():
    required_files = [
        "docs/cae/implementation/CAE_GOV_02_RATIFICATION_REGISTER.md",
        "docs/cae/implementation/CAE_GOV_02_CONTROL_STATE_RECONCILIATION.md",
        "docs/cae/implementation/CAE_GOV_02_OPERATOR_DECISION_PACKET.md",
        "docs/cae/implementation/CAE_GOV_02_GOVERNANCE_TRANSITION_LEDGER.md",
        "docs/cae/implementation/CAE_GOV_02_COMPLETION_RECORD.md",
        "docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md",
    ]
    for rel_path in required_files:
        full_path = ROOT_DIR / rel_path
        assert full_path.is_file(), f"Artifact missing: {rel_path}"
        assert full_path.stat().st_size > 500, f"Artifact empty or too small: {rel_path}"


def test_ratification_register_14_columns():
    reg_path = ROOT_DIR / "docs/cae/implementation/CAE_GOV_02_RATIFICATION_REGISTER.md"
    content = reg_path.read_text(encoding="utf-8")
    mandatory_cols = [
        "decision_id",
        "subject/version",
        "current documented status",
        "evidence reference",
        "decision type",
        "eligible decision owner",
        "proposed disposition",
        "operator decision record",
        "effective date",
        "supersedes / preserves",
        "implementation relationship",
        "authority/environment boundary",
        "open risk",
        "next permitted phase",
    ]
    for col in mandatory_cols:
        assert col in content, f"Mandatory column '{col}' missing from register"


def test_operator_decision_packet_unbundled():
    packet_path = ROOT_DIR / "docs/cae/implementation/CAE_GOV_02_OPERATOR_DECISION_PACKET.md"
    content = packet_path.read_text(encoding="utf-8")
    expected_ids = [
        "DEC-GOV-MAP-01",
        "DEC-GOV-AUTH-01",
        "DEC-GOV-CAN-01A",
        "DEC-GOV-CAN-01B",
        "DEC-GOV-CAN-01C",
        "DEC-GOV-SPEC-01",
        "DEC-GOV-STATE-01",
        "DEC-GOV-TS-01",
    ]
    for dec_id in expected_ids:
        assert dec_id in content, f"Decision ID '{dec_id}' missing from decision packet"


def test_three_layer_stratification():
    csr_path = ROOT_DIR / "docs/cae/implementation/CAE_GOV_02_CONTROL_STATE_RECONCILIATION.md"
    content = csr_path.read_text(encoding="utf-8")
    assert "Layer 1: Current Execution State" in content
    assert "Layer 2: Historical Execution Ledger" in content
    assert "Layer 3: Open Governance Decisions & Deferrals" in content
    assert "POSTGRES_AUTHORITATIVE_STAGING_ONLY" in content


def test_completion_record_verbatim_question():
    comp_path = ROOT_DIR / "docs/cae/implementation/CAE_GOV_02_COMPLETION_RECORD.md"
    content = comp_path.read_text(encoding="utf-8")
    exact_question = (
        "Approve the CA-GOV-02 Ratification Register and Control-State Reconciliation: "
        "record only the decision IDs explicitly approved in the attached operator packet as ratified, "
        "retain every other item as pending/deferred/contradictory exactly as listed, "
        "preserve all F-01/F-02/F-03 and non-claims, and authorize CA-MIG-03 only to design "
        "and rehearse safe forward-only migrations—without applying a migration or changing operational authority?"
    )
    assert exact_question in content
