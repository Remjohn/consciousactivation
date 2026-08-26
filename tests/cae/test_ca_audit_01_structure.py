"""
Pure local structure test for CA-AUDIT-01 Post-Execution Governance Artifacts.
Validates matrix fields, phase coverage, and anti-overclaim rules without network or database interaction.
"""

from __future__ import annotations

from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def test_audit_artifacts_exist_and_non_empty():
    required_files = [
        "docs/cae/implementation/CAE_POST_EXECUTION_GOVERNANCE_AUDIT.md",
        "docs/cae/implementation/CAE_GOVERNANCE_STATUS_MATRIX.md",
        "docs/cae/implementation/CAE_AUDIT_01_FINDINGS_AND_DECISIONS_REGISTER.md",
        "docs/cae/implementation/CAE_AUDIT_01_EVIDENCE_REPRODUCIBILITY_LOG.md",
        "docs/cae/implementation/CAE_AUDIT_01_COMPLETION_RECORD.md",
        "docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md",
    ]
    for rel_path in required_files:
        full_path = ROOT_DIR / rel_path
        assert full_path.is_file(), f"Artifact missing: {rel_path}"
        assert full_path.stat().st_size > 500, f"Artifact empty or too small: {rel_path}"


def test_governance_matrix_14_columns():
    matrix_path = ROOT_DIR / "docs/cae/implementation/CAE_GOVERNANCE_STATUS_MATRIX.md"
    content = matrix_path.read_text(encoding="utf-8")
    mandatory_cols = [
        "claim_id",
        "domain",
        "claim",
        "evidence reference",
        "evidence class",
        "verification fidelity",
        "environment class",
        "reproducible now",
        "ratification state",
        "implementation state",
        "authority state",
        "scope / non-claim",
        "contradiction or finding",
        "owner / next decision",
    ]
    for col in mandatory_cols:
        assert col in content, f"Mandatory column '{col}' missing from matrix"


def test_no_false_production_authorization():
    matrix_path = ROOT_DIR / "docs/cae/implementation/CAE_GOVERNANCE_STATUS_MATRIX.md"
    content = matrix_path.read_text(encoding="utf-8")
    assert "PRODUCTION_AUTHORIZED: YES" not in content, "Falsely claiming production authority"
    assert "PRODUCTION_AUTHORITATIVE" not in content, "Falsely claiming production authority"


def test_control_state_audit_phase():
    cs_path = ROOT_DIR / "docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md"
    content = cs_path.read_text(encoding="utf-8")
    assert ("current_execution_stage: AUDIT" in content or "current_execution_stage: OPERATOR_REVIEW" in content)
    assert "CA-AUDIT-01" in content
    assert ("ZERO_AUTHORITY_CHANGED" in content or "operational_authority_change:" in content)
    assert ("MC-CAE-MED-001" in content or "MC-CAE-WS-001" in content)



def test_completion_record_verbatim_question():
    comp_path = ROOT_DIR / "docs/cae/implementation/CAE_AUDIT_01_COMPLETION_RECORD.md"
    content = comp_path.read_text(encoding="utf-8")
    exact_question = (
        "Accept CA-AUDIT-01 as the authoritative post-execution status record, "
        "preserve all listed limitations and non-claims, and authorize CA-GOV-02 only to "
        "reconcile formal ratification states and control-state governance—without any schema, "
        "runtime, database, Storage, registry, or authority transition?"
    )
    assert exact_question in content
