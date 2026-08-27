"""
test_ca_spec_02_structure.py — Structural tests for CA-SPEC-02 deliverables.
Validates that all six implementation specifications, the App Completion Ledger,
and PRD reconciliations conform to mandated 14-section standards and contain
required hard negatives, code anchors, and decision markers.
"""

import pytest
from pathlib import Path
from scripts.cae.audit.verify_ca_spec_02 import (
    REQUIRED_SPECS,
    audit_prd_reconciliation,
    audit_completion_ledger,
    audit_spec_file,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_prd_reconciliation_structure():
    result = audit_prd_reconciliation()
    assert result["ok"] is True, f"PRD Reconciliation failed: {result}"
    assert result["has_changelog"] is True
    assert result["has_tenancy_update"] is True
    assert result["has_model_engine"] is True
    assert result["has_debt_ref"] is True


def test_app_completion_ledger_structure():
    result = audit_completion_ledger()
    assert result["ok"] is True, f"Completion ledger failed: {result}"
    assert len(result["missing_spec_refs"]) == 0
    assert result["has_capabilities"] is True


@pytest.mark.parametrize("spec_filename", REQUIRED_SPECS)
def test_spec_14_sections_and_quality_gates(spec_filename):
    result = audit_spec_file(spec_filename)
    assert result["ok"] is True, f"Spec {spec_filename} failed quality gate: {result}"
    assert result["section_count"] == 14, f"{spec_filename} has missing sections: {result.get('missing_sections')}"
    assert result["hard_negatives_count"] >= 5, f"{spec_filename} has only {result.get('hard_negatives_count')} hard negatives"
    assert result["has_open_decision"] is True, f"{spec_filename} missing OPEN_DECISION marker"
    assert result["has_code_anchors"] is True, f"{spec_filename} missing verified code anchors"
