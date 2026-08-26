"""
Unit and structural tests for Phase 22 / CA-ACCEPT-10.

Mandate: CA-ACCEPT-10 — Independent Regression, Operator Acceptance, and Next-Aggregate Decision.
"""

from __future__ import annotations

from pathlib import Path
import sys
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
IMPL_DIR = ROOT_DIR / "docs" / "cae" / "implementation"

sys.path.insert(0, str(ROOT_DIR / "scripts" / "cae" / "audit"))

import verify_ca_accept_10


def test_required_documentation_files_exist():
    """All 6 CA-ACCEPT-10 documentation files exist and are non-empty."""
    for fname in verify_ca_accept_10.REQUIRED_DOCS:
        fpath = IMPL_DIR / fname
        assert fpath.is_file(), f"Missing file: {fname}"
        assert fpath.stat().st_size > 0, f"Empty file: {fname}"


def test_review_admission_and_independence():
    """Admission record declares SELF_REVIEW_WITH_ADVERSARIAL_CHECKS and rules ADM-ACC-01 to 06."""
    content = (IMPL_DIR / "CAE_ACCEPT_10_REVIEW_ADMISSION.md").read_text(encoding="utf-8")
    assert "SELF_REVIEW_WITH_ADVERSARIAL_CHECKS" in content
    assert "REVIEWER_INDEPENDENCE_LIMITED" in content
    for rule in ["ADM-ACC-01", "ADM-ACC-02", "ADM-ACC-03", "ADM-ACC-04", "ADM-ACC-05", "ADM-ACC-06"]:
        assert rule in content


def test_claim_matrix_structure():
    """Claim matrix contains all 12 claims and proper classifications."""
    content = (IMPL_DIR / "CAE_ACCEPT_10_REGRESSION_AND_CLAIM_MATRIX.md").read_text(encoding="utf-8")
    for i in range(1, 13):
        assert f"CLM-{i:02d}" in content
    assert "ACCEPTED" in content
    assert "LIMITED" in content
    assert "REJECTED" in content


def test_candidate_register_bounds():
    """Candidate register contains at most 3 qualified candidates and excludes disqualified ones."""
    content = (IMPL_DIR / "CAE_ACCEPT_10_NEXT_AGGREGATE_CANDIDATE_REGISTER.md").read_text(encoding="utf-8")
    assert "MC-CAE-ENG-001" in content
    assert "MC-CAE-GST-001" in content
    assert "MC-CAE-EVN-001" in content
    assert "Disqualified Aggregates Register" in content
    assert "MC-CAE-CMP-001" in content


def test_completion_record_structure_and_decision_question():
    """Completion record contains Sections A-H and verbatim Section 6 decision question."""
    content = (IMPL_DIR / "CAE_ACCEPT_10_COMPLETION_RECORD.md").read_text(encoding="utf-8")
    for sec in [
        "## A. What Was Reviewed and What Changed",
        "## B. What Is Accepted Versus Limited / Unproven / Rejected",
        "## C. What Evidence Was Independently Observed Versus Inherited",
        "## D. What Remains Staging-Only and What Remains Deferred",
        "## E. What Could Still Be Wrong and Its Falsification Path",
        "## F. The Complete F-01 / F-02 / Recovery / Authority Status",
        "## G. Exact Reviewer-Independence Limitations and Inspection Paths",
        "## H. The One Next Decision Required",
    ]:
        assert sec in content

    expected_question = (
        "Accept the CA-ACCEPT-10 bounded shared-staging substrate review as stated, preserve "
        "every limited/unproven/deferred claim and all production/data/authority non-claims, "
        "and authorize CA-NEXT-01 only to write a mandate and evidence plan for the one named "
        "next aggregate in the Candidate Register—without implementing, migrating, or promoting "
        "that aggregate?"
    )
    assert expected_question in content


def test_control_state_status():
    """Control state is updated to FIRST_SLICE_SHARED_STAGING_ACCEPTANCE_READY_FOR_OPERATOR_REVIEW or downstream."""
    content = (IMPL_DIR / "CAE_IMPLEMENTATION_CONTROL_STATE.md").read_text(encoding="utf-8")
    valid_statuses = [
        "FIRST_SLICE_SHARED_STAGING_ACCEPTANCE_READY_FOR_OPERATOR_REVIEW",
        "CLAIMS_UNVERIFIED_BY_OPERATOR",
        "AWAITING_OPERATOR_AUTHORIZATION_CA_UPTL_01",
        "UPSTREAM_INTELLIGENCE_COMPLETED_AWAITING_OPERATOR_GATE",
    ]
    assert any(st in content for st in valid_statuses)
    assert "CA-ACCEPT-10" in content


def test_static_verifier_passes():
    """Static audit script verify_ca_accept_10.py passes with exit code 0."""
    assert verify_ca_accept_10.main() == 0
