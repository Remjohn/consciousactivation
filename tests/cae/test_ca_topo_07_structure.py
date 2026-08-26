"""
Unit and structural tests for Phase 19 / CA-TOPO-07.

Mandate: CA-TOPO-07 — Selected F-02 Canonical Topology Implementation and Disposable Proof.
Option: DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET.
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
    F01_REPAIR_DRAFT,
    F02_TOPOLOGY_DRAFT,
)
import verify_ca_topo_07
import run_topo07_selected_proof


def test_required_documentation_files_exist():
    """All 6 CA-TOPO-07 documentation files exist and are non-empty."""
    for fname in verify_ca_topo_07.REQUIRED_DOCS:
        fpath = IMPL_DIR / fname
        assert fpath.is_file(), f"Missing file: {fname}"
        assert fpath.stat().st_size > 0, f"Empty file: {fname}"


def test_admission_record_rules():
    """Admission record contains rules ADM-TOPO-01 to ADM-TOPO-06 and scope lock."""
    content = (IMPL_DIR / "CAE_TOPO_07_ADMISSION_RECORD.md").read_text(encoding="utf-8")
    for rule in ["ADM-TOPO-01", "ADM-TOPO-02", "ADM-TOPO-03", "ADM-TOPO-04", "ADM-TOPO-05", "ADM-TOPO-06"]:
        assert rule in content
    assert "DISPOSABLE_POSTGRESQL_ONLY" in content
    assert "disposable_topo07_pg" in content
    assert "EMPTY_OR_SYNTHETIC_ONLY" in content
    assert "DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET" in content
    assert "evnxdssbxxrsesftdvgx" in content


def test_option_a_implementation_specifications():
    """Option A implementation record contains required entities, MIG-0008, and adapter details."""
    content = (IMPL_DIR / "CAE_TOPO_07_SELECTED_OPTION_IMPLEMENTATION.md").read_text(encoding="utf-8")
    assert "DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET" in content
    assert "CA_IMPL_UUID_FAMILY" in content
    assert "MIG-0008" in content
    assert "0008_cae_f02_topology_shadow_reconciliation_draft.sql" in content
    assert "legacy_wp03_workspace" in content
    assert "legacy_wp03_media_asset" in content
    assert "legacy_wp03_execution_receipt" in content
    assert "CanonicalInterviewSourceAdapter" in content
    assert "register_verified_interview_source" in content
    assert "fk_workspace_receipt" in content


def test_canonical_route_proof_details():
    """Canonical route proof record contains execution steps, RLS context, and composite FK linkage."""
    content = (IMPL_DIR / "CAE_TOPO_07_CANONICAL_ROUTE_PROOF.md").read_text(encoding="utf-8")
    assert "register_verified_interview_source" in content
    assert "SET LOCAL cae.current_workspace_id" in content
    assert "cae.media_asset" in content
    assert "cae.receipt" in content
    assert "cae.receipt_evidence_link" in content
    assert "fk_workspace_receipt" in content
    assert "IDEMPOTENT_REPLAY" in content


def test_adversarial_results_completeness():
    """Adversarial results record contains all 12 countertests passing."""
    content = (IMPL_DIR / "CAE_TOPO_07_ADVERSARIAL_AND_RECOVERY_RESULTS.md").read_text(encoding="utf-8")
    for i in range(1, 13):
        assert f"TOPO07-CT-{i:02d}" in content
    assert "12/12 PASSED" in content


def test_teardown_receipt_invariants():
    """Teardown receipt verifies isolated purge and zero operational authority change."""
    content = (IMPL_DIR / "CAE_TOPO_07_TEARDOWN_RECEIPT.md").read_text(encoding="utf-8")
    assert "PURGED AND VERIFIED ISOLATED" in content
    assert "evnxdssbxxrsesftdvgx" in content
    assert "POSTGRES_AUTHORITATIVE_STAGING_ONLY" in content
    assert "MC-CAE-MED-001" in content


def test_completion_record_structure_and_decision_question():
    """Completion record contains Sections A-G and exact verbatim Section 6 decision question."""
    content = (IMPL_DIR / "CAE_TOPO_07_COMPLETION_RECORD.md").read_text(encoding="utf-8")
    sections = [
        "## A. What Changed in the Disposable Target and Why",
        "## B. Tests, Environment, and Evidence Captured",
        "## C. What Failed or Remained Unproven",
        "## D. Cleanup and Teardown Result",
        "## E. F-01 and F-02 Status",
        "## F. Risks and Non-Claims",
        "## G. Exact Next Authorization Requested",
    ]
    for s in sections:
        assert s in content

    decision_q = (
        "Accept CA-TOPO-07 as disposable proof of the operator-selected F-02 canonical topology and route only, "
        "preserve all shared-staging/production and data-migration limitations, and authorize CA-E3-08 only to "
        "independently replay the bounded foundation, F-01, and selected F-02 proof chain in a network-permitted "
        "staging-equivalent environment—without promoting any new authority?"
    )
    clean_content = " ".join(content.split())
    clean_decision_q = " ".join(decision_q.split())
    assert clean_decision_q in clean_content


def test_migration_runner_option_a_manifest():
    """GuardedMigrationRunner loads 8 drafts including MIG-0007 and MIG-0008 when include_f02_topology=True."""
    adm = TargetEnvironmentAdmission(
        target_label="disposable_topo07_pg",
        target_url="postgresql://runner:pass@127.0.0.1:5432/disposable_topo07_pg",
        environment_class="DISPOSABLE_POSTGRESQL_ONLY",
        is_disposable_declared=True,
        data_classification="EMPTY_OR_SYNTHETIC_ONLY",
        teardown_owner="CA-TOPO-07-Test",
    )
    runner = GuardedMigrationRunner(adm, DRAFTS_DIR, include_f02_topology=True)
    assert len(runner.manifest) == 8
    ids = [e.migration_id for e in runner.manifest]
    assert ids == [
        "MIG-0001", "MIG-0002", "MIG-0003", "MIG-0004",
        "MIG-0005", "MIG-0006", "MIG-0007", "MIG-0008",
    ]
    assert runner.manifest[-1].migration_id == "MIG-0008"
    assert runner.manifest[-1].predecessor == "MIG-0007"
    assert runner.manifest[-1].filename == "0008_cae_f02_topology_shadow_reconciliation_draft.sql"


def test_target_admission_staging_signature_rejection():
    """TargetEnvironmentAdmission strictly rejects staging/production endpoints."""
    adm = TargetEnvironmentAdmission(
        target_label="forbidden_staging",
        target_url="postgresql://runner:pass@evnxdssbxxrsesftdvgx.pooler.supabase.com:6543/postgres",
        environment_class="DISPOSABLE_POSTGRESQL_ONLY",
        is_disposable_declared=True,
        data_classification="EMPTY_OR_SYNTHETIC_ONLY",
        teardown_owner="CA-TOPO-07-Test",
    )
    with pytest.raises(MigrationAdmissionError) as exc_info:
        adm.validate()
    assert "forbidden staging/production signature" in str(exc_info.value)


def test_run_topo07_selected_proof_all_countertests_pass():
    """Execute all 12 CA-TOPO-07 countertests via run_topo07_selected_proof."""
    assert run_topo07_selected_proof.main() == 0


def test_verify_ca_topo_07_static_verifier():
    """Static verifier verify_ca_topo_07 passes with returncode 0."""
    assert verify_ca_topo_07.main() == 0
