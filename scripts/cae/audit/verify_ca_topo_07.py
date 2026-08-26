#!/usr/bin/env python3
"""
Static Verification Script for Phase 19 / CA-TOPO-07.

Mandate: CA-TOPO-07 — Selected F-02 Canonical Topology Implementation and Disposable Proof.
Option: DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET.

Verifies:
1. Presence and structural integrity of 6 CA-TOPO-07 documentation artifacts.
2. Target Admission Record rules (ADM-TOPO-01 to ADM-TOPO-06).
3. Selected Option A implementation records, MIG-0008 draft, and adapter specifications.
4. Canonical route execution proof and idempotent replay trace.
5. 12 Adversarial countertests record (TOPO07-CT-01 to TOPO07-CT-12).
6. Teardown receipt and isolation invariants.
7. Completion record Sections A through G and Section 6 decision question.
8. Control state transition to F02_SELECTED_TOPOLOGY_E3_PROVEN_DISPOSABLE_ONLY.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
IMPL_DIR = ROOT_DIR / "docs" / "cae" / "implementation"
CONTROL_STATE_PATH = IMPL_DIR / "CAE_IMPLEMENTATION_CONTROL_STATE.md"
DRAFTS_DIR = ROOT_DIR / "packages" / "ca_runtime" / "src" / "ca_runtime" / "migrations" / "drafts"

REQUIRED_DOCS = [
    "CAE_TOPO_07_ADMISSION_RECORD.md",
    "CAE_TOPO_07_SELECTED_OPTION_IMPLEMENTATION.md",
    "CAE_TOPO_07_CANONICAL_ROUTE_PROOF.md",
    "CAE_TOPO_07_ADVERSARIAL_AND_RECOVERY_RESULTS.md",
    "CAE_TOPO_07_TEARDOWN_RECEIPT.md",
    "CAE_TOPO_07_COMPLETION_RECORD.md",
]


def check_required_artifacts() -> bool:
    print("[CHECK 1] Checking presence of CA-TOPO-07 documentation artifacts...")
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
    content = (IMPL_DIR / "CAE_TOPO_07_ADMISSION_RECORD.md").read_text(encoding="utf-8")
    required_tokens = [
        "ADM-TOPO-01", "ADM-TOPO-02", "ADM-TOPO-03", "ADM-TOPO-04", "ADM-TOPO-05", "ADM-TOPO-06",
        "DISPOSABLE_POSTGRESQL_ONLY", "disposable_topo07_pg", "EMPTY_OR_SYNTHETIC_ONLY",
        "DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET", "evnxdssbxxrsesftdvgx",
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


def check_option_implementation() -> bool:
    print("[CHECK 3] Verifying Option A Implementation Record...")
    content = (IMPL_DIR / "CAE_TOPO_07_SELECTED_OPTION_IMPLEMENTATION.md").read_text(encoding="utf-8")
    required_tokens = [
        "DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET",
        "CA_IMPL_UUID_FAMILY",
        "MIG-0008",
        "0008_cae_f02_topology_shadow_reconciliation_draft.sql",
        "legacy_wp03_workspace",
        "legacy_wp03_media_asset",
        "legacy_wp03_execution_receipt",
        "CanonicalInterviewSourceAdapter",
        "register_verified_interview_source",
        "fk_workspace_receipt",
    ]
    all_ok = True
    for tok in required_tokens:
        if tok not in content:
            print(f"  [FAIL] Missing token in Implementation Record: {tok}")
            all_ok = False
    if all_ok:
        print("  [PASS] Option A Implementation Record verified.")
    return all_ok


def check_canonical_route_proof() -> bool:
    print("[CHECK 4] Verifying Canonical Route Execution Proof...")
    content = (IMPL_DIR / "CAE_TOPO_07_CANONICAL_ROUTE_PROOF.md").read_text(encoding="utf-8")
    required_tokens = [
        "register_verified_interview_source",
        "SET LOCAL cae.current_workspace_id",
        "cae.media_asset",
        "cae.receipt",
        "cae.receipt_evidence_link",
        "fk_workspace_receipt",
        "IDEMPOTENT_REPLAY",
    ]
    all_ok = True
    for tok in required_tokens:
        if tok not in content:
            print(f"  [FAIL] Missing token in Canonical Route Proof: {tok}")
            all_ok = False
    if all_ok:
        print("  [PASS] Canonical Route Proof verified.")
    return all_ok


def check_adversarial_results() -> bool:
    print("[CHECK 5] Verifying Adversarial Countertest Results...")
    content = (IMPL_DIR / "CAE_TOPO_07_ADVERSARIAL_AND_RECOVERY_RESULTS.md").read_text(encoding="utf-8")
    all_ok = True
    for i in range(1, 13):
        ct_id = f"TOPO07-CT-{i:02d}"
        if ct_id not in content:
            print(f"  [FAIL] Missing countertest result: {ct_id}")
            all_ok = False
    if "12/12 PASSED" not in content:
        print("  [FAIL] Missing '12/12 PASSED' summary")
        all_ok = False
    if all_ok:
        print("  [PASS] All 12 Adversarial Countertests verified.")
    return all_ok


def check_teardown_receipt() -> bool:
    print("[CHECK 6] Verifying Scoped Teardown Receipt...")
    content = (IMPL_DIR / "CAE_TOPO_07_TEARDOWN_RECEIPT.md").read_text(encoding="utf-8")
    required_tokens = [
        "PURGED AND VERIFIED ISOLATED",
        "evnxdssbxxrsesftdvgx",
        "POSTGRES_AUTHORITATIVE_STAGING_ONLY",
        "MC-CAE-MED-001",
    ]
    all_ok = True
    for tok in required_tokens:
        if tok not in content:
            print(f"  [FAIL] Missing token in Teardown Receipt: {tok}")
            all_ok = False
    if all_ok:
        print("  [PASS] Scoped Teardown Receipt verified.")
    return all_ok


def check_completion_record() -> bool:
    print("[CHECK 7] Verifying Completion Record Sections A through G...")
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
    all_ok = True
    for s in sections:
        if s not in content:
            print(f"  [FAIL] Missing section: {s}")
            all_ok = False

    decision_q = (
        "Accept CA-TOPO-07 as disposable proof of the operator-selected F-02 canonical topology and route only, "
        "preserve all shared-staging/production and data-migration limitations, and authorize CA-E3-08 only to "
        "independently replay the bounded foundation, F-01, and selected F-02 proof chain in a network-permitted "
        "staging-equivalent environment—without promoting any new authority?"
    )
    if decision_q not in content:
        print("  [FAIL] Exact Section 6 Decision Question missing from Completion Record")
        all_ok = False

    if all_ok:
        print("  [PASS] Completion Record verified with verbatim Decision Question.")
    return all_ok


def check_control_state() -> bool:
    print("[CHECK 8] Verifying Control State Document...")
    content = CONTROL_STATE_PATH.read_text(encoding="utf-8")
    all_ok = True
    valid_statuses = [
        "TENANT_WORKSPACE_CORE_COMPLETED_AWAITING_OPERATOR_GATE",
        "F02_SELECTED_TOPOLOGY_E3_PROVEN_DISPOSABLE_ONLY",
        "INDEPENDENT_E3_REPLAY_PASSED_STAGING_EQUIVALENT_ONLY",
        "FOUNDATION_F01_F02_DEPLOYED_AND_VERIFIED_SHARED_STAGING_ONLY",
        "FIRST_SLICE_SHARED_STAGING_ACCEPTANCE_READY_FOR_OPERATOR_REVIEW",
        "CLAIMS_UNVERIFIED_BY_OPERATOR",
        "AWAITING_OPERATOR_AUTHORIZATION_CA_UPTL_01",
        "UPSTREAM_INTELLIGENCE_COMPLETED_AWAITING_OPERATOR_GATE",
    ]
    if not any(st in content for st in valid_statuses):
        print("  [FAIL] Control status is not F02_SELECTED_TOPOLOGY_E3_PROVEN_DISPOSABLE_ONLY or downstream")
        all_ok = False
    if "CA-TOPO-07" not in content:
        print("  [FAIL] Control state does not reference CA-TOPO-07")
        all_ok = False
    if all_ok:
        print("  [PASS] Control State Document verified.")
    return all_ok


def main() -> int:
    print("=" * 80)
    print("   CAE STATIC AUDIT & INTEGRITY VERIFIER: PHASE 19 / CA-TOPO-07       ")
    print("=" * 80)

    checks = [
        check_required_artifacts,
        check_admission_record,
        check_option_implementation,
        check_canonical_route_proof,
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
        print("   STATIC VERIFICATION FAILED: One or more CA-TOPO-07 checks failed. ")
        print("=" * 80)
        return 1

    print("   SUCCESS: 8/8 STATIC VERIFICATION CHECKS PASSED FOR CA-TOPO-07.     ")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
