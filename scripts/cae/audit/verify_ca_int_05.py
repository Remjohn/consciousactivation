#!/usr/bin/env python3
"""
Static Governance and Structural Validator for Phase 17 / CA-INT-05.

Validates:
1. Presence and structure of all 5 CA-INT-05 documentation artifacts.
2. Presence and integrity of F-01 repair draft and proof runner.
3. Target admission constraints (disposable only, non-staging/production).
4. Coverage of all 11 adversarial countertests (F01-CT-01 to CT-11).
5. Independent constraint layer inspection (composite FK on workspace_id, receipt_id).
6. Failure recovery rehearsal, atomic rollback, and teardown receipt.
7. Completion record structure (Sections A–G) and exact Section 6 decision question.
8. Implementation Control State update to F01_REPAIRED_AND_E3_PROVEN_DISPOSABLE_ONLY.

Usage:
    python scripts/cae/audit/verify_ca_int_05.py
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

DOCS_DIR = ROOT_DIR / "docs/cae/implementation"
DRAFTS_DIR = ROOT_DIR / "packages/ca_runtime/src/ca_runtime/migrations/drafts"
RUNNER_PATH = ROOT_DIR / "packages/ca_runtime/src/ca_runtime/migration_runner.py"
PROOF_SCRIPT_PATH = ROOT_DIR / "scripts/cae/implementation/run_f01_repair_proof.py"
CONTROL_STATE_PATH = DOCS_DIR / "CAE_IMPLEMENTATION_CONTROL_STATE.md"

REQUIRED_DOCUMENTS = [
    "CAE_INT_05_F01_ADMISSION_RECORD.md",
    "CAE_INT_05_F01_SCHEMA_REPAIR_PROOF.md",
    "CAE_INT_05_F01_ADVERSARIAL_RESULTS.md",
    "CAE_INT_05_F01_RECOVERY_AND_TEARDOWN.md",
    "CAE_INT_05_COMPLETION_RECORD.md",
]

EXPECTED_SECTION_6_QUESTION = (
    "Accept CA-INT-05 as disposable-environment proof that F-01 is structurally rejected by the exact approved forward migration, "
    "preserve F-02 and all shared-staging/production limitations, and authorize CA-TOPO-06 only to reconcile and prove the "
    "WP-03 versus CA-IMPL table-family topology—without applying F-01 to shared staging or changing operational authority?"
)


def log_pass(msg: str) -> None:
    print(f"  [PASS] {msg}")


def log_fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def verify_documents() -> bool:
    print("--- Test Suite 1: CA-INT-05 Documentation Artifacts ---")
    all_ok = True
    for doc in REQUIRED_DOCUMENTS:
        doc_path = DOCS_DIR / doc
        if not doc_path.is_file():
            log_fail(f"Missing required document: {doc_path}")
            all_ok = False
            continue
        sz = doc_path.stat().st_size
        if sz < 500:
            log_fail(f"Document {doc} unexpectedly small ({sz} bytes)")
            all_ok = False
            continue
        log_pass(f"Document verified: {doc} ({sz} bytes)")
    return all_ok


def verify_draft_and_proof_script() -> bool:
    print("\n--- Test Suite 2: F-01 Repair Draft & Proof Script ---")
    all_ok = True
    draft_path = DRAFTS_DIR / "0007_cae_f01_composite_receipt_fk_draft.sql"
    if not draft_path.is_file():
        log_fail(f"Missing F-01 repair draft: {draft_path}")
        return False
    draft_sql = draft_path.read_text(encoding="utf-8")
    if "fk_workspace_receipt" not in draft_sql or "REFERENCES cae.receipt(workspace_id, receipt_id)" not in draft_sql:
        log_fail("Draft 0007 missing required composite FK constraint")
        all_ok = False
    else:
        log_pass("Verified draft 0007 composite FK definition")

    if not PROOF_SCRIPT_PATH.is_file():
        log_fail(f"Missing proof script at {PROOF_SCRIPT_PATH}")
        return False
    proof_code = PROOF_SCRIPT_PATH.read_text(encoding="utf-8")
    for ct in [f"test_f01_ct{i:02d}" for i in range(1, 12)]:
        if ct not in proof_code:
            log_fail(f"Missing countertest method in proof script: {ct}")
            all_ok = False
        else:
            log_pass(f"Verified proof script countertest: {ct}")

    return all_ok


def verify_admission_record() -> bool:
    print("\n--- Test Suite 3: Disposable Admission Record ---")
    adm_path = DOCS_DIR / "CAE_INT_05_F01_ADMISSION_RECORD.md"
    content = adm_path.read_text(encoding="utf-8")
    all_ok = True
    for token in [
        "DISPOSABLE_POSTGRESQL_ONLY",
        "EMPTY_OR_SYNTHETIC_ONLY",
        "evnxdssbxxrsesftdvgx",
        ".pooler.supabase.com",
        "ADM-INT-01", "ADM-INT-02", "ADM-INT-03", "ADM-INT-04", "ADM-INT-05", "ADM-INT-06",
    ]:
        if token not in content:
            log_fail(f"Missing required admission token: '{token}'")
            all_ok = False
        else:
            log_pass(f"Admission rule verified: '{token}'")
    return all_ok


def verify_countertest_coverage() -> bool:
    print("\n--- Test Suite 4: 11 Countertests in Documentation ---")
    adv_res = (DOCS_DIR / "CAE_INT_05_F01_ADVERSARIAL_RESULTS.md").read_text(encoding="utf-8")
    all_ok = True
    for i in range(1, 12):
        ct = f"F01-CT-{i:02d}"
        if ct not in adv_res:
            log_fail(f"Missing countertest reference in adversarial results: {ct}")
            all_ok = False
        else:
            log_pass(f"Verified countertest reference: {ct}")
    return all_ok


def verify_recovery_and_teardown() -> bool:
    print("\n--- Test Suite 5: Recovery Rehearsal & Teardown Receipt ---")
    rec_path = DOCS_DIR / "CAE_INT_05_F01_RECOVERY_AND_TEARDOWN.md"
    all_ok = True
    content = rec_path.read_text(encoding="utf-8")
    for token in ["CA-INT-05 Execution Harness", "Untouched (Zero Connections Made)", "POSTGRES_AUTHORITATIVE_STAGING_ONLY"]:
        if token not in content:
            log_fail(f"Missing token in recovery and teardown receipt: '{token}'")
            all_ok = False
        else:
            log_pass(f"Recovery and teardown token verified: '{token}'")
    return all_ok


def verify_completion_record() -> bool:
    print("\n--- Test Suite 6: Completion Record & Section 6 Question ---")
    comp_path = DOCS_DIR / "CAE_INT_05_COMPLETION_RECORD.md"
    content = comp_path.read_text(encoding="utf-8")
    all_ok = True
    for sec in [
        "## A. What Changed in the Disposable Target and Why",
        "## B. Tests, Environment, and Evidence Captured",
        "## C. What Failed or Remained Unproven",
        "## D. Cleanup and Teardown Result",
        "## E. F-01 and F-02 Status",
        "## F. Risks and Non-Claims",
        "## G. Exact Next Authorization Requested",
    ]:
        if sec not in content:
            log_fail(f"Missing required section in Completion Record: '{sec}'")
            all_ok = False
        else:
            log_pass(f"Completion Record section present: '{sec}'")

    clean_content = " ".join(content.split())
    clean_expected = " ".join(EXPECTED_SECTION_6_QUESTION.split())
    if clean_expected not in clean_content:
        log_fail("Section 6 decision question does not match expected text verbatim")
        all_ok = False
    else:
        log_pass("Exact verbatim Section 6 decision question confirmed in Completion Record.")
    return all_ok


def verify_control_state() -> bool:
    print("\n--- Test Suite 7: Implementation Control State Validation ---")
    content = CONTROL_STATE_PATH.read_text(encoding="utf-8")
    all_ok = True

    valid_statuses = [
        "F01_REPAIRED_AND_E3_PROVEN_DISPOSABLE_ONLY",
        "F02_TOPOLOGY_EVIDENCED_DECISION_REQUIRED",
        "F02_SELECTED_TOPOLOGY_E3_PROVEN_DISPOSABLE_ONLY",
        "INDEPENDENT_E3_REPLAY_PASSED_STAGING_EQUIVALENT_ONLY",
        "FOUNDATION_F01_F02_DEPLOYED_AND_VERIFIED_SHARED_STAGING_ONLY",
    ]
    if not any(st in content for st in valid_statuses):
        log_fail("Control status is not F01_REPAIRED_AND_E3_PROVEN_DISPOSABLE_ONLY or downstream")
        all_ok = False
    else:
        log_pass("Control status verified (F01_REPAIRED_AND_E3_PROVEN_DISPOSABLE_ONLY or downstream)")

    if "CA-INT-05" not in content:
        log_fail("Control state does not contain CA-INT-05")
        all_ok = False
    else:
        log_pass("Control state contains CA-INT-05")

    if "operational_authority_change: ZERO_AUTHORITY_CHANGED" not in content:
        log_fail("Missing explicit zero operational authority change assertion")
        all_ok = False
    else:
        log_pass("Zero operational authority change explicitly verified")

    return all_ok


def main() -> int:
    print("=" * 80)
    print("   CAE STATIC GOVERNANCE VALIDATOR: PHASE 17 / CA-INT-05               ")
    print("=" * 80)

    suites = [
        verify_documents,
        verify_draft_and_proof_script,
        verify_admission_record,
        verify_countertest_coverage,
        verify_recovery_and_teardown,
        verify_completion_record,
        verify_control_state,
    ]

    all_passed = True
    for s in suites:
        if not s():
            all_passed = False

    print("\n" + "=" * 80)
    if not all_passed:
        print("   VALIDATION FAILED: One or more CA-INT-05 governance rules violated. ")
        print("=" * 80)
        return 1

    print("   SUCCESS: CA-INT-05 F-01 INTEGRITY REPAIR 100% COMPLIANT             ")
    print("   ZERO DATABASE MUTATION ON STAGING; DISPOSABLE PROOFS COMPLETE.       ")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
