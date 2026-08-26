#!/usr/bin/env python3
"""
Static Verification Script for Phase 21 / CA-STAGE-09.

Mandate: CA-STAGE-09 — Controlled Shared-Staging Deployment of the Proven Foundation Repairs.
Target: evnxdssbxxrsesftdvgx.pooler.supabase.com:6543/postgres (E3_STAGING_SUPABASE_POOLER_PRIVATE_STORAGE).

Verifies:
1. Presence and structural integrity of 5 CA-STAGE-09 documentation artifacts.
2. Target Admission Record rules (ADM-STAGE-01 to ADM-STAGE-06).
3. Preflight & Deployment Record and forward migration execution trace.
4. Post-Deployment Proof and 14 reality-contact countertests (STAGE09-CT-01 to STAGE09-CT-14).
5. Recovery Readiness and Scoped Cleanup Receipt.
6. Completion record Sections A through G and verbatim Section 6 decision question.
7. Control state transition to FOUNDATION_F01_F02_DEPLOYED_AND_VERIFIED_SHARED_STAGING_ONLY.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
IMPL_DIR = ROOT_DIR / "docs" / "cae" / "implementation"
CONTROL_STATE_PATH = IMPL_DIR / "CAE_IMPLEMENTATION_CONTROL_STATE.md"

REQUIRED_DOCS = [
    "CAE_STAGE_09_ADMISSION_AND_BACKUP_RECORD.md",
    "CAE_STAGE_09_PREFLIGHT_AND_DEPLOYMENT_RECORD.md",
    "CAE_STAGE_09_POST_DEPLOYMENT_PROOF.md",
    "CAE_STAGE_09_RECOVERY_READINESS_AND_CLEANUP.md",
    "CAE_STAGE_09_COMPLETION_RECORD.md",
]


def check_required_artifacts() -> bool:
    print("[CHECK 1] Checking presence of CA-STAGE-09 documentation artifacts...")
    all_ok = True
    for fname in REQUIRED_DOCS:
        fpath = IMPL_DIR / fname
        if not fpath.is_file() or fpath.stat().st_size == 0:
            print(f"  [FAIL] Missing or empty: {fname}")
            all_ok = False
        else:
            print(f"  [PASS] Present: {fname} ({fpath.stat().st_size} bytes)")
    return all_ok


def check_admission_record() -> bool:
    print("[CHECK 2] Verifying Admission Record & Scope Lock...")
    content = (IMPL_DIR / "CAE_STAGE_09_ADMISSION_AND_BACKUP_RECORD.md").read_text(encoding="utf-8")
    required_tokens = [
        "ADM-STAGE-01", "ADM-STAGE-02", "ADM-STAGE-03", "ADM-STAGE-04", "ADM-STAGE-05", "ADM-STAGE-06",
        "E3_STAGING_SUPABASE_POOLER_PRIVATE_STORAGE", "evnxdssbxxrsesftdvgx",
        "CW-2026-08-26-STAGE09-01", "snapshot_pre_stage09_20260826T051500Z",
        "MIG-0001", "MIG-0008",
    ]
    all_ok = True
    for tok in required_tokens:
        if tok not in content:
            print(f"  [FAIL] Missing token in Admission Record: {tok}")
            all_ok = False
    if all_ok:
        print("  [PASS] Admission Record & Scope Lock verified.")
    return all_ok


def check_deployment_record() -> bool:
    print("[CHECK 3] Verifying Preflight & Deployment Record...")
    content = (IMPL_DIR / "CAE_STAGE_09_PREFLIGHT_AND_DEPLOYMENT_RECORD.md").read_text(encoding="utf-8")
    required_tokens = [
        "evnxdssbxxrsesftdvgx",
        "GuardedMigrationRunner",
        "MIG-0001", "MIG-0002", "MIG-0003", "MIG-0004",
        "MIG-0005", "MIG-0006", "MIG-0007", "MIG-0008",
        "fk_workspace_receipt", "legacy_wp03_workspace",
    ]
    all_ok = True
    for tok in required_tokens:
        if tok not in content:
            print(f"  [FAIL] Missing token in Preflight/Deployment Record: {tok}")
            all_ok = False
    if all_ok:
        print("  [PASS] Preflight & Deployment Record verified.")
    return all_ok


def check_post_deployment_proof() -> bool:
    print("[CHECK 4] Verifying Post-Deployment Reality-Contact Proof...")
    content = (IMPL_DIR / "CAE_STAGE_09_POST_DEPLOYMENT_PROOF.md").read_text(encoding="utf-8")
    required_tokens = [
        "register_verified_interview_source",
        "StagingInterviewSourceAdapter",
        "cae.media_asset",
        "cae.receipt",
        "cae.receipt_evidence_link",
        "fk_workspace_receipt",
        "SET LOCAL cae.current_workspace_id",
        "100% PROVEN — ALL 14 COUNTERTESTS PASSED",
    ]
    all_ok = True
    for tok in required_tokens:
        if tok not in content:
            print(f"  [FAIL] Missing token in Post-Deployment Proof: {tok}")
            all_ok = False
    for i in range(1, 15):
        ct = f"STAGE09-CT-{i:02d}"
        if ct not in content:
            print(f"  [FAIL] Missing countertest token: {ct}")
            all_ok = False
    if all_ok:
        print("  [PASS] Post-Deployment Reality-Contact Proof verified.")
    return all_ok


def check_recovery_and_cleanup_receipt() -> bool:
    print("[CHECK 5] Verifying Recovery Readiness & Scoped Cleanup Receipt...")
    content = (IMPL_DIR / "CAE_STAGE_09_RECOVERY_READINESS_AND_CLEANUP.md").read_text(encoding="utf-8")
    required_tokens = [
        "PURGED AND VERIFIED ISOLATED",
        "evnxdssbxxrsesftdvgx",
        "cae-media-staging-synthetic",
        "0 rows remaining",
        "0 active objects",
        "POSTGRES_AUTHORITATIVE_STAGING_ONLY",
    ]
    all_ok = True
    for tok in required_tokens:
        if tok not in content:
            print(f"  [FAIL] Missing token in Recovery/Cleanup Receipt: {tok}")
            all_ok = False
    if all_ok:
        print("  [PASS] Recovery Readiness & Scoped Cleanup Receipt verified.")
    return all_ok


def check_completion_record() -> bool:
    print("[CHECK 6] Verifying Completion Record & Verbatim Decision Question...")
    content = (IMPL_DIR / "CAE_STAGE_09_COMPLETION_RECORD.md").read_text(encoding="utf-8")
    sections = [
        "## A. What Changed in Shared Staging and Why",
        "## B. Tests, Environment, and Evidence Captured",
        "## C. What Failed or Remained Unproven",
        "## D. Cleanup and Teardown Result",
        "## E. F-01 and F-02 Status",
        "## F. Risks and Non-Claims",
        "## G. Exact Next Authorization Requested",
    ]
    all_ok = True
    for sec in sections:
        if sec not in content:
            print(f"  [FAIL] Missing section in Completion Record: {sec}")
            all_ok = False

    decision_question = (
        "Accept CA-STAGE-09 as controlled shared-staging deployment and verification of the exact "
        "proven foundation, F-01, and selected F-02 chain only; preserve every production, "
        "authority, client-data, and deferred-domain limitation; and authorize CA-ACCEPT-10 "
        "only for independent regression review, operator acceptance, and selection of at most "
        "one next aggregate—without beginning that aggregate or promoting production authority?"
    )
    if decision_question not in content:
        print("  [FAIL] Missing or altered Section 6 decision question")
        all_ok = False

    if all_ok:
        print("  [PASS] Completion Record verified with verbatim Decision Question.")
    return all_ok


def check_control_state() -> bool:
    print("[CHECK 7] Verifying Control State Document...")
    content = CONTROL_STATE_PATH.read_text(encoding="utf-8")
    all_ok = True
    valid_statuses = [
        "FOUNDATION_F01_F02_DEPLOYED_AND_VERIFIED_SHARED_STAGING_ONLY",
        "FIRST_SLICE_SHARED_STAGING_ACCEPTANCE_READY_FOR_OPERATOR_REVIEW",
        "CLAIMS_UNVERIFIED_BY_OPERATOR",
        "AWAITING_OPERATOR_AUTHORIZATION_CA_UPTL_01",
        "UPSTREAM_INTELLIGENCE_COMPLETED_AWAITING_OPERATOR_GATE",
    ]
    if not any(st in content for st in valid_statuses):
        print("  [FAIL] Control status is not FOUNDATION_F01_F02_DEPLOYED_AND_VERIFIED_SHARED_STAGING_ONLY or downstream")
        all_ok = False
    if "CA-STAGE-09" not in content:
        print("  [FAIL] Control state does not reference CA-STAGE-09")
        all_ok = False
    if all_ok:
        print("  [PASS] Control State Document verified.")
    return all_ok


def main() -> int:
    print("=" * 80)
    print("   CAE STATIC AUDIT & INTEGRITY VERIFIER: PHASE 21 / CA-STAGE-09     ")
    print("=" * 80)

    checks = [
        check_required_artifacts,
        check_admission_record,
        check_deployment_record,
        check_post_deployment_proof,
        check_recovery_and_cleanup_receipt,
        check_completion_record,
        check_control_state,
    ]

    all_passed = True
    for chk in checks:
        if not chk():
            all_passed = False
        print()

    print("=" * 80)
    if not all_passed:
        print("   STATIC VERIFICATION FAILED: One or more CA-STAGE-09 checks failed. ")
        print("=" * 80)
        return 1

    print("   SUCCESS: 7/7 STATIC VERIFICATION CHECKS PASSED FOR CA-STAGE-09.   ")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
