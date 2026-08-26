"""
Unit and structural tests for Phase 21 / CA-STAGE-09.

Mandate: CA-STAGE-09 — Controlled Shared-Staging Deployment of the Proven Foundation Repairs.
Target: evnxdssbxxrsesftdvgx.pooler.supabase.com:6543/postgres (E3_STAGING_SUPABASE_POOLER_PRIVATE_STORAGE).
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
    SharedStagingEnvironmentAdmission,
    TargetEnvironmentAdmission,
    MigrationAdmissionError,
)
import verify_ca_stage_09
import run_stage_09_deployment_proof


def test_required_documentation_files_exist():
    """All 5 CA-STAGE-09 documentation files exist and are non-empty."""
    for fname in verify_ca_stage_09.REQUIRED_DOCS:
        fpath = IMPL_DIR / fname
        assert fpath.is_file(), f"Missing file: {fname}"
        assert fpath.stat().st_size > 0, f"Empty file: {fname}"


def test_admission_record_rules():
    """Admission record contains rules ADM-STAGE-01 to ADM-STAGE-06 and scope lock."""
    content = (IMPL_DIR / "CAE_STAGE_09_ADMISSION_AND_BACKUP_RECORD.md").read_text(encoding="utf-8")
    for rule in ["ADM-STAGE-01", "ADM-STAGE-02", "ADM-STAGE-03", "ADM-STAGE-04", "ADM-STAGE-05", "ADM-STAGE-06"]:
        assert rule in content
    assert "E3_STAGING_SUPABASE_POOLER_PRIVATE_STORAGE" in content
    assert "evnxdssbxxrsesftdvgx" in content
    assert "CW-2026-08-26-STAGE09-01" in content
    assert "snapshot_pre_stage09_20260826T051500Z" in content


def test_preflight_and_deployment_record():
    """Preflight and deployment record contains execution trace and manifest."""
    content = (IMPL_DIR / "CAE_STAGE_09_PREFLIGHT_AND_DEPLOYMENT_RECORD.md").read_text(encoding="utf-8")
    assert "evnxdssbxxrsesftdvgx" in content
    assert "GuardedMigrationRunner" in content
    for m in ["MIG-0001", "MIG-0002", "MIG-0003", "MIG-0004", "MIG-0005", "MIG-0006", "MIG-0007", "MIG-0008"]:
        assert m in content
    assert "fk_workspace_receipt" in content
    assert "legacy_wp03_workspace" in content


def test_post_deployment_proof_details():
    """Post-deployment proof record contains execution steps, storage check, RLS context, and composite FK."""
    content = (IMPL_DIR / "CAE_STAGE_09_POST_DEPLOYMENT_PROOF.md").read_text(encoding="utf-8")
    assert "register_verified_interview_source" in content
    assert "SET LOCAL cae.current_workspace_id" in content
    assert "cae.media_asset" in content
    assert "cae.receipt" in content
    assert "cae.receipt_evidence_link" in content
    assert "fk_workspace_receipt" in content
    assert "100% PROVEN — ALL 14 COUNTERTESTS PASSED" in content
    for i in range(1, 15):
        assert f"STAGE09-CT-{i:02d}" in content


def test_recovery_readiness_and_cleanup_receipt():
    """Recovery and cleanup receipt verifies isolated purge and zero authority escalation."""
    content = (IMPL_DIR / "CAE_STAGE_09_RECOVERY_READINESS_AND_CLEANUP.md").read_text(encoding="utf-8")
    assert "PURGED AND VERIFIED ISOLATED" in content
    assert "evnxdssbxxrsesftdvgx" in content
    assert "cae-media-staging-synthetic" in content
    assert "0 rows remaining" in content
    assert "0 active objects" in content
    assert "POSTGRES_AUTHORITATIVE_STAGING_ONLY" in content


def test_completion_record_structure_and_decision_question():
    """Completion record contains Sections A-G and exact verbatim Section 6 decision question."""
    content = (IMPL_DIR / "CAE_STAGE_09_COMPLETION_RECORD.md").read_text(encoding="utf-8")
    for sec in [
        "## A. What Changed in Shared Staging and Why",
        "## B. Tests, Environment, and Evidence Captured",
        "## C. What Failed or Remained Unproven",
        "## D. Cleanup and Teardown Result",
        "## E. F-01 and F-02 Status",
        "## F. Risks and Non-Claims",
        "## G. Exact Next Authorization Requested",
    ]:
        assert sec in content

    expected_question = (
        "Accept CA-STAGE-09 as controlled shared-staging deployment and verification of the exact "
        "proven foundation, F-01, and selected F-02 chain only; preserve every production, "
        "authority, client-data, and deferred-domain limitation; and authorize CA-ACCEPT-10 "
        "only for independent regression review, operator acceptance, and selection of at most "
        "one next aggregate—without beginning that aggregate or promoting production authority?"
    )
    assert expected_question in content


def test_control_state_status():
    """Control state is updated to FOUNDATION_F01_F02_DEPLOYED_AND_VERIFIED_SHARED_STAGING_ONLY."""
    content = (IMPL_DIR / "CAE_IMPLEMENTATION_CONTROL_STATE.md").read_text(encoding="utf-8")
    assert "**Control status:** `FOUNDATION_F01_F02_DEPLOYED_AND_VERIFIED_SHARED_STAGING_ONLY`" in content
    assert "CA-STAGE-09" in content


def test_staging_admission_guard_rejections():
    """SharedStagingEnvironmentAdmission validates staging rules and rejects invalid endpoints."""
    # Production endpoint rejection
    prod_adm = SharedStagingEnvironmentAdmission(
        target_label="forbidden_prod",
        target_url="postgresql://runner:pass@prod-db.pooler.supabase.com:6543/postgres",
        environment_class="E3_STAGING_SUPABASE_POOLER_PRIVATE_STORAGE",
        change_window="CW-2026-08-26-STAGE09-01",
        backup_snapshot_id="snapshot_pre_stage09_20260826T051500Z",
        recovery_owner="CAE Release Operations",
        data_classification="EMPTY_OR_SYNTHETIC_ONLY",
    )
    with pytest.raises(MigrationAdmissionError) as exc_info:
        prod_adm.validate()
    assert "forbidden production signature" in str(exc_info.value)

    # Valid staging admission
    valid_adm = SharedStagingEnvironmentAdmission(
        target_label="staging_valid",
        target_url="postgresql://runner:pass@evnxdssbxxrsesftdvgx.pooler.supabase.com:6543/postgres",
        environment_class="E3_STAGING_SUPABASE_POOLER_PRIVATE_STORAGE",
        change_window="CW-2026-08-26-STAGE09-01",
        backup_snapshot_id="snapshot_pre_stage09_20260826T051500Z",
        recovery_owner="CAE Release Operations",
        data_classification="EMPTY_OR_SYNTHETIC_ONLY",
    )
    valid_adm.validate()


def test_static_verifier_passes():
    """Static audit script verify_ca_stage_09.py passes with exit code 0."""
    assert verify_ca_stage_09.main() == 0


def test_live_stage_09_deployment_harness():
    """All 14 countertests in run_stage_09_deployment_proof pass."""
    results = run_stage_09_deployment_proof.run_stage_09_countertests()
    assert len(results) == 14
    assert all(results.values()), f"Failed countertests: {[k for k, v in results.items() if not v]}"
