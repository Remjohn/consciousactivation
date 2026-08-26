"""
Unit and structural tests for Phase 20 / CA-E3-08.

Mandate: CA-E3-08 — Independent Staging-Equivalent Reality-Contact Replay.
Target: disposable_e3_08_pg (E3_STAGING_EQUIVALENT_DISPOSABLE).
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
IMPL_DIR = ROOT_DIR / "docs" / "cae" / "implementation"
DRAFTS_DIR = ROOT_DIR / "packages" / "ca_runtime" / "src" / "ca_runtime" / "migrations" / "drafts"

sys.path.insert(0, str(ROOT_DIR / "packages" / "ca_runtime" / "src"))
sys.path.insert(0, str(ROOT_DIR / "packages" / "ca_contracts" / "src"))
sys.path.insert(0, str(ROOT_DIR / "scripts" / "cae" / "audit"))
sys.path.insert(0, str(ROOT_DIR / "scripts" / "cae" / "implementation"))

from ca_runtime.migration_runner import (
    GuardedMigrationRunner,
    TargetEnvironmentAdmission,
    MigrationAdmissionError,
)
import verify_ca_e3_08
import run_e3_08_replay_proof


def test_required_documentation_files_exist():
    """All 6 CA-E3-08 documentation files exist and are non-empty."""
    for fname in verify_ca_e3_08.REQUIRED_DOCS:
        fpath = IMPL_DIR / fname
        assert fpath.is_file(), f"Missing file: {fname}"
        assert fpath.stat().st_size > 0, f"Empty file: {fname}"


def test_admission_record_rules():
    """Admission record contains rules ADM-E3-01 to ADM-E3-06 and scope lock."""
    content = (IMPL_DIR / "CAE_E3_08_ENVIRONMENT_ADMISSION_RECORD.md").read_text(encoding="utf-8")
    for rule in ["ADM-E3-01", "ADM-E3-02", "ADM-E3-03", "ADM-E3-04", "ADM-E3-05", "ADM-E3-06"]:
        assert rule in content
    assert "E3_STAGING_EQUIVALENT_DISPOSABLE" in content
    assert "disposable_e3_08_pg" in content
    assert "EMPTY_OR_SYNTHETIC_ONLY" in content
    assert "cae-media-disposable-e3-08" in content
    assert "evnxdssbxxrsesftdvgx" in content


def test_replay_plan_specifications():
    """Replay plan contains required entities, 14 countertests, and adapter details."""
    content = (IMPL_DIR / "CAE_E3_08_REPLAY_PLAN.md").read_text(encoding="utf-8")
    assert "E3_STAGING_EQUIVALENT_DISPOSABLE" in content
    assert "disposable_e3_08_pg" in content
    assert "CanonicalInterviewSourceAdapter" in content
    assert "register_verified_interview_source" in content
    assert "fk_workspace_receipt" in content
    assert "EX_RECEIPT_IMMUTABLE" in content
    for i in range(1, 15):
        assert f"E3-CT-{i:02d}" in content


def test_independent_proof_details():
    """Independent proof record contains execution steps, storage verification, RLS context, and composite FK linkage."""
    content = (IMPL_DIR / "CAE_E3_08_INDEPENDENT_PROOF.md").read_text(encoding="utf-8")
    assert "register_verified_interview_source" in content
    assert "SET LOCAL cae.current_workspace_id" in content
    assert "cae.media_asset" in content
    assert "cae.receipt" in content
    assert "cae.receipt_evidence_link" in content
    assert "legacy_wp03_workspace" in content
    assert "fk_workspace_receipt" in content
    assert "100% PROVEN — ALL 14 COUNTERTESTS PASSED" in content


def test_adversarial_results_completeness():
    """Adversarial results record contains all 14 countertests passing."""
    content = (IMPL_DIR / "CAE_E3_08_ADVERSARIAL_RESULTS.md").read_text(encoding="utf-8")
    for i in range(1, 15):
        assert f"E3-CT-{i:02d}" in content
    assert "14/14 PASSED" in content


def test_teardown_receipt_invariants():
    """Teardown receipt verifies isolated purge and zero operational authority change."""
    content = (IMPL_DIR / "CAE_E3_08_RECOVERY_AND_TEARDOWN_RECEIPT.md").read_text(encoding="utf-8")
    assert "PURGED AND VERIFIED ISOLATED" in content
    assert "disposable_e3_08_pg" in content
    assert "cae-media-disposable-e3-08" in content
    assert "0 rows remaining" in content
    assert "0 active objects" in content
    assert "POSTGRES_AUTHORITATIVE_STAGING_ONLY" in content
    assert "MC-CAE-MED-001" in content


def test_completion_record_structure_and_decision_question():
    """Completion record contains Sections A-G and exact verbatim Section 6 decision question."""
    content = (IMPL_DIR / "CAE_E3_08_COMPLETION_RECORD.md").read_text(encoding="utf-8")
    for sec in [
        "## A. What Changed in the Disposable Target and Why",
        "## B. Tests, Environment, and Evidence Captured",
        "## C. What Failed or Remained Unproven",
        "## D. Cleanup and Teardown Result",
        "## E. F-01 and F-02 Status",
        "## F. Risks and Non-Claims",
        "## G. Exact Next Authorization Requested",
    ]:
        assert sec in content

    expected_question = (
        "Accept CA-E3-08 as independent staging-equivalent evidence for the exact approved "
        "foundation, F-01, and selected F-02 chain only, preserve all shared-staging/production/data-migration "
        "limitations, and authorize CA-STAGE-09 only to admit and deploy those exact proven "
        "migrations/routes to the named shared staging environment under a separate backup, "
        "recovery, and operator gate—without promoting production authority?"
    )
    assert expected_question in content


def test_control_state_status():
    """Control state is updated to INDEPENDENT_E3_REPLAY_PASSED_STAGING_EQUIVALENT_ONLY or downstream."""
    content = (IMPL_DIR / "CAE_IMPLEMENTATION_CONTROL_STATE.md").read_text(encoding="utf-8")
    valid_statuses = [
        "TENANT_WORKSPACE_CORE_COMPLETED_AWAITING_OPERATOR_GATE",
        "INDEPENDENT_E3_REPLAY_PASSED_STAGING_EQUIVALENT_ONLY",
        "FOUNDATION_F01_F02_DEPLOYED_AND_VERIFIED_SHARED_STAGING_ONLY",
        "FIRST_SLICE_SHARED_STAGING_ACCEPTANCE_READY_FOR_OPERATOR_REVIEW",
        "CLAIMS_UNVERIFIED_BY_OPERATOR",
        "AWAITING_OPERATOR_AUTHORIZATION_CA_UPTL_01",
        "UPSTREAM_INTELLIGENCE_COMPLETED_AWAITING_OPERATOR_GATE",
    ]
    assert any(st in content for st in valid_statuses)
    assert "CA-E3-08" in content


def test_static_verifier_passes():
    """Static audit script verify_ca_e3_08.py passes with exit code 0."""
    assert verify_ca_e3_08.main() == 0


def test_live_e3_08_replay_harness():
    """All 14 countertests in run_e3_08_replay_proof pass."""
    results = run_e3_08_replay_proof.run_e3_08_replay_proof()
    assert len(results) == 14
    assert all(results.values()), f"Failed countertests: {[k for k, v in results.items() if not v]}"
