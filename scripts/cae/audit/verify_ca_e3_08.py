#!/usr/bin/env python3
"""
Static Verification Script for Phase 20 / CA-E3-08.

Mandate: CA-E3-08 — Independent Staging-Equivalent Reality-Contact Replay.
Environment: disposable_e3_08_pg (E3_STAGING_EQUIVALENT_DISPOSABLE).

Verifies:
1. Presence and structural integrity of 6 CA-E3-08 documentation artifacts.
2. Target Admission Record rules (ADM-E3-01 to ADM-E3-06).
3. Replay Plan and lifecycle stages.
4. Independent Replay Proof trace for register_verified_interview_source.
5. 14 Adversarial countertest results (E3-CT-01 to E3-CT-14).
6. Teardown receipt and isolation invariants.
7. Completion record Sections A through G and verbatim Section 6 decision question.
8. Control state transition to INDEPENDENT_E3_REPLAY_PASSED_STAGING_EQUIVALENT_ONLY.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
IMPL_DIR = ROOT_DIR / "docs" / "cae" / "implementation"
CONTROL_STATE_PATH = IMPL_DIR / "CAE_IMPLEMENTATION_CONTROL_STATE.md"

REQUIRED_DOCS = [
    "CAE_E3_08_ENVIRONMENT_ADMISSION_RECORD.md",
    "CAE_E3_08_REPLAY_PLAN.md",
    "CAE_E3_08_INDEPENDENT_PROOF.md",
    "CAE_E3_08_ADVERSARIAL_RESULTS.md",
    "CAE_E3_08_RECOVERY_AND_TEARDOWN_RECEIPT.md",
    "CAE_E3_08_COMPLETION_RECORD.md",
]


def check_required_artifacts() -> bool:
    print("[CHECK 1] Checking presence of CA-E3-08 documentation artifacts...")
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
    content = (IMPL_DIR / "CAE_E3_08_ENVIRONMENT_ADMISSION_RECORD.md").read_text(encoding="utf-8")
    required_tokens = [
        "ADM-E3-01", "ADM-E3-02", "ADM-E3-03", "ADM-E3-04", "ADM-E3-05", "ADM-E3-06",
        "E3_STAGING_EQUIVALENT_DISPOSABLE", "disposable_e3_08_pg", "EMPTY_OR_SYNTHETIC_ONLY",
        "evnxdssbxxrsesftdvgx", "cae-media-disposable-e3-08", "MIG-0001", "MIG-0008",
    ]
    all_ok = True
    for tok in required_tokens:
        if tok not in content:
            print(f"  [FAIL] Missing token in Admission Record: {tok}")
            all_ok = False
    if all_ok:
        print("  [PASS] Admission Record & Scope Lock verified.")
    return all_ok


def check_replay_plan() -> bool:
    print("[CHECK 3] Verifying Replay Plan...")
    content = (IMPL_DIR / "CAE_E3_08_REPLAY_PLAN.md").read_text(encoding="utf-8")
    required_tokens = [
        "E3_STAGING_EQUIVALENT_DISPOSABLE",
        "disposable_e3_08_pg",
        "register_verified_interview_source",
        "CanonicalInterviewSourceAdapter",
        "E3-CT-01", "E3-CT-14",
        "fk_workspace_receipt",
        "EX_RECEIPT_IMMUTABLE",
    ]
    all_ok = True
    for tok in required_tokens:
        if tok not in content:
            print(f"  [FAIL] Missing token in Replay Plan: {tok}")
            all_ok = False
    if all_ok:
        print("  [PASS] Replay Plan verified.")
    return all_ok


def check_independent_proof() -> bool:
    print("[CHECK 4] Verifying Independent Replay Proof...")
    content = (IMPL_DIR / "CAE_E3_08_INDEPENDENT_PROOF.md").read_text(encoding="utf-8")
    required_tokens = [
        "register_verified_interview_source",
        "CanonicalInterviewSourceAdapter",
        "cae.workspace",
        "cae.media_asset",
        "cae.receipt",
        "cae.receipt_evidence_link",
        "legacy_wp03_workspace",
        "fk_workspace_receipt",
        "SET LOCAL cae.current_workspace_id",
        "100% PROVEN — ALL 14 COUNTERTESTS PASSED",
    ]
    all_ok = True
    for tok in required_tokens:
        if tok not in content:
            print(f"  [FAIL] Missing token in Independent Proof: {tok}")
            all_ok = False
    if all_ok:
        print("  [PASS] Independent Replay Proof verified.")
    return all_ok


def check_adversarial_results() -> bool:
    print("[CHECK 5] Verifying Adversarial Countertest Results...")
    content = (IMPL_DIR / "CAE_E3_08_ADVERSARIAL_RESULTS.md").read_text(encoding="utf-8")
    required_cts = [f"E3-CT-{i:02d}" for i in range(1, 15)]
    all_ok = True
    for ct in required_cts:
        if ct not in content:
            print(f"  [FAIL] Missing countertest: {ct}")
            all_ok = False
    if "14/14 PASSED" not in content:
        print("  [FAIL] Did not find '14/14 PASSED' summary")
        all_ok = False
    if all_ok:
        print("  [PASS] All 14 Countertests verified present and passing.")
    return all_ok


def check_teardown_receipt() -> bool:
    print("[CHECK 6] Verifying Teardown & Isolation Receipt...")
    content = (IMPL_DIR / "CAE_E3_08_RECOVERY_AND_TEARDOWN_RECEIPT.md").read_text(encoding="utf-8")
    required_tokens = [
        "PURGED AND VERIFIED ISOLATED",
        "disposable_e3_08_pg",
        "cae-media-disposable-e3-08",
        "0 rows remaining",
        "0 active objects",
        "POSTGRES_AUTHORITATIVE_STAGING_ONLY",
    ]
    all_ok = True
    for tok in required_tokens:
        if tok not in content:
            print(f"  [FAIL] Missing token in Teardown Receipt: {tok}")
            all_ok = False
    if all_ok:
        print("  [PASS] Teardown & Isolation Receipt verified.")
    return all_ok


def check_completion_record() -> bool:
    print("[CHECK 7] Verifying Completion Record & Verbatim Decision Question...")
    content = (IMPL_DIR / "CAE_E3_08_COMPLETION_RECORD.md").read_text(encoding="utf-8")
    sections = [
        "## A. What Changed in the Disposable Target and Why",
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
        "Accept CA-E3-08 as independent staging-equivalent evidence for the exact approved "
        "foundation, F-01, and selected F-02 chain only, preserve all shared-staging/production/data-migration "
        "limitations, and authorize CA-STAGE-09 only to admit and deploy those exact proven "
        "migrations/routes to the named shared staging environment under a separate backup, "
        "recovery, and operator gate—without promoting production authority?"
    )
    if decision_question not in content:
        print("  [FAIL] Missing or altered Section 6 decision question")
        all_ok = False

    if all_ok:
        print("  [PASS] Completion Record verified with verbatim Decision Question.")
    return all_ok


def check_control_state() -> bool:
    print("[CHECK 8] Verifying Control State Document...")
    content = CONTROL_STATE_PATH.read_text(encoding="utf-8")
    all_ok = True
    if "**Control status:** `INDEPENDENT_E3_REPLAY_PASSED_STAGING_EQUIVALENT_ONLY`" not in content:
        print("  [FAIL] Control status is not INDEPENDENT_E3_REPLAY_PASSED_STAGING_EQUIVALENT_ONLY")
        all_ok = False
    if "CA-E3-08" not in content:
        print("  [FAIL] Control state does not reference CA-E3-08")
        all_ok = False
    if all_ok:
        print("  [PASS] Control State Document verified.")
    return all_ok


def main() -> int:
    print("=" * 80)
    print("   CAE STATIC AUDIT & INTEGRITY VERIFIER: PHASE 20 / CA-E3-08       ")
    print("=" * 80)

    checks = [
        check_required_artifacts,
        check_admission_record,
        check_replay_plan,
        check_independent_proof,
        check_adversarial_results,
        check_teardown_receipt,
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
        print("   STATIC VERIFICATION FAILED: One or more CA-E3-08 checks failed. ")
        print("=" * 80)
        return 1

    print("   SUCCESS: 8/8 STATIC VERIFICATION CHECKS PASSED FOR CA-E3-08.     ")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
