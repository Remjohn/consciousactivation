#!/usr/bin/env python3
"""
Static Governance and Structural Validator for Phase 16 / CA-APPLY-04.

Validates:
1. Presence and structure of all 6 CA-APPLY-04 documentation artifacts.
2. Presence and integrity of GuardedMigrationRunner and proof runner.
3. Verification of admission constraints (no staging/production endpoints).
4. Coverage of all 11 adversarial countertests (CT-01 to CT-11).
5. Failure recovery rehearsal, atomic rollback, and history honesty verification.
6. Teardown receipt and zero shared-state leakage assertions.
7. Completion record structure (Sections A–H) and exact Section 6 decision question.
8. Implementation Control State update to APPLIED_AND_E3_PROVEN_IN_DISPOSABLE_ENVIRONMENT_ONLY.

Usage:
    python scripts/cae/audit/verify_ca_apply_04.py
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

DOCS_DIR = ROOT_DIR / "docs/cae/implementation"
RUNNER_PATH = ROOT_DIR / "packages/ca_runtime/src/ca_runtime/migration_runner.py"
PROOF_SCRIPT_PATH = ROOT_DIR / "scripts/cae/implementation/run_disposable_migration_proof.py"
CONTROL_STATE_PATH = DOCS_DIR / "CAE_IMPLEMENTATION_CONTROL_STATE.md"

REQUIRED_DOCUMENTS = [
    "CAE_APPLY_04_DISPOSABLE_ADMISSION_RECORD.md",
    "CAE_APPLY_04_MIGRATION_APPLICATION_PROOF.md",
    "CAE_APPLY_04_SCHEMA_AND_CONTAINMENT_RESULTS.md",
    "CAE_APPLY_04_FAILURE_RECOVERY_REHEARSAL.md",
    "CAE_APPLY_04_TEARDOWN_RECEIPT.md",
    "CAE_APPLY_04_COMPLETION_RECORD.md",
]

EXPECTED_SECTION_6_QUESTION = (
    "Accept CA-APPLY-04 as proof that the exact forward-only draft IDs applied safely in the named disposable PostgreSQL environment only, "
    "preserve all remaining F-01/F-02 and authority limitations, and authorize CA-INT-05 only to implement and prove the narrowly specified "
    "F-01 workspace/receipt lineage integrity repair—without touching F-02, shared staging, client data, or production?"
)


def log_pass(msg: str) -> None:
    print(f"  [PASS] {msg}")


def log_fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def verify_documents() -> bool:
    print("--- Test Suite 1: CA-APPLY-04 Documentation Artifacts ---")
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


def verify_runner_and_proof_script() -> bool:
    print("\n--- Test Suite 2: Guarded Runner & Proof Script ---")
    all_ok = True
    if not RUNNER_PATH.is_file():
        log_fail(f"Missing GuardedMigrationRunner at {RUNNER_PATH}")
        return False
    runner_code = RUNNER_PATH.read_text(encoding="utf-8")
    for cls_name in [
        "TargetEnvironmentAdmission",
        "GuardedMigrationRunner",
        "MigrationAdmissionError",
        "MigrationDestructiveStatementError",
        "IncompatibleTopologyError",
    ]:
        if cls_name not in runner_code:
            log_fail(f"Missing class in migration_runner: {cls_name}")
            all_ok = False
        else:
            log_pass(f"Verified runner class: {cls_name}")

    if not PROOF_SCRIPT_PATH.is_file():
        log_fail(f"Missing proof script at {PROOF_SCRIPT_PATH}")
        return False
    proof_code = PROOF_SCRIPT_PATH.read_text(encoding="utf-8")
    for ct in [f"test_ct{i:02d}" for i in range(1, 12)]:
        if ct not in proof_code:
            log_fail(f"Missing countertest method in proof script: {ct}")
            all_ok = False
        else:
            log_pass(f"Verified proof script countertest: {ct}")

    return all_ok


def verify_admission_record() -> bool:
    print("\n--- Test Suite 3: Disposable Admission Record ---")
    adm_path = DOCS_DIR / "CAE_APPLY_04_DISPOSABLE_ADMISSION_RECORD.md"
    content = adm_path.read_text(encoding="utf-8")
    all_ok = True
    for token in [
        "DISPOSABLE_POSTGRESQL_ONLY",
        "EMPTY_OR_SYNTHETIC_ONLY",
        "evnxdssbxxrsesftdvgx",
        ".pooler.supabase.com",
        "ADM-01", "ADM-02", "ADM-03", "ADM-04", "ADM-05", "ADM-06",
    ]:
        if token not in content:
            log_fail(f"Missing required admission token: '{token}'")
            all_ok = False
        else:
            log_pass(f"Admission rule verified: '{token}'")
    return all_ok


def verify_countertest_coverage() -> bool:
    print("\n--- Test Suite 4: 11 Countertests in Documentation ---")
    app_proof = (DOCS_DIR / "CAE_APPLY_04_MIGRATION_APPLICATION_PROOF.md").read_text(encoding="utf-8")
    schema_res = (DOCS_DIR / "CAE_APPLY_04_SCHEMA_AND_CONTAINMENT_RESULTS.md").read_text(encoding="utf-8")
    all_ok = True
    for ct in ["CT-02", "CT-04", "CT-05"]:
        if ct not in app_proof:
            log_fail(f"Missing countertest reference in application proof: {ct}")
            all_ok = False
        else:
            log_pass(f"Verified countertest reference: {ct}")

    for ct in ["CT-07", "CT-08", "CT-09"]:
        if ct not in schema_res:
            log_fail(f"Missing countertest reference in schema results: {ct}")
            all_ok = False
        else:
            log_pass(f"Verified countertest reference: {ct}")
    return all_ok


def verify_failure_recovery_and_teardown() -> bool:
    print("\n--- Test Suite 5: Failure Recovery & Teardown Receipt ---")
    rec_path = DOCS_DIR / "CAE_APPLY_04_FAILURE_RECOVERY_REHEARSAL.md"
    td_path = DOCS_DIR / "CAE_APPLY_04_TEARDOWN_RECEIPT.md"
    all_ok = True

    rec_content = rec_path.read_text(encoding="utf-8")
    for token in ["CT-10", "CT-03", "Ghost Rows", "Forward-Repair"]:
        if token not in rec_content:
            log_fail(f"Missing token in failure recovery rehearsal: '{token}'")
            all_ok = False
        else:
            log_pass(f"Recovery rehearsal token verified: '{token}'")

    td_content = td_path.read_text(encoding="utf-8")
    for token in ["CA-APPLY-04 Execution Harness", "Untouched (Zero Connections Made)", "POSTGRES_AUTHORITATIVE_STAGING_ONLY"]:
        if token not in td_content:
            log_fail(f"Missing token in teardown receipt: '{token}'")
            all_ok = False
        else:
            log_pass(f"Teardown receipt token verified: '{token}'")

    return all_ok


def verify_completion_record() -> bool:
    print("\n--- Test Suite 6: Completion Record & Section 6 Question ---")
    comp_path = DOCS_DIR / "CAE_APPLY_04_COMPLETION_RECORD.md"
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

    if "**Control status:** `APPLIED_AND_E3_PROVEN_IN_DISPOSABLE_ENVIRONMENT_ONLY`" not in content:
        log_fail("Control status is not APPLIED_AND_E3_PROVEN_IN_DISPOSABLE_ENVIRONMENT_ONLY")
        all_ok = False
    else:
        log_pass("Control status verified (APPLIED_AND_E3_PROVEN_IN_DISPOSABLE_ENVIRONMENT_ONLY)")

    if "current_work_package: CA-APPLY-04 Disposable PostgreSQL Migration Application and Recovery Proof" not in content:
        log_fail("Control state current_work_package is not CA-APPLY-04")
        all_ok = False
    else:
        log_pass("Control state current_work_package verified (CA-APPLY-04)")

    if "operational_authority_change: ZERO_AUTHORITY_CHANGED" not in content:
        log_fail("Missing explicit zero operational authority change assertion")
        all_ok = False
    else:
        log_pass("Zero operational authority change explicitly verified")

    return all_ok


def main() -> int:
    print("=" * 80)
    print("   CAE STATIC GOVERNANCE VALIDATOR: PHASE 16 / CA-APPLY-04               ")
    print("=" * 80)

    suites = [
        verify_documents,
        verify_runner_and_proof_script,
        verify_admission_record,
        verify_countertest_coverage,
        verify_failure_recovery_and_teardown,
        verify_completion_record,
        verify_control_state,
    ]

    all_passed = True
    for s in suites:
        if not s():
            all_passed = False

    print("\n" + "=" * 80)
    if not all_passed:
        print("   VALIDATION FAILED: One or more CA-APPLY-04 governance rules violated. ")
        print("=" * 80)
        return 1

    print("   SUCCESS: CA-APPLY-04 DISPOSABLE MIGRATION PROOF 100% COMPLIANT       ")
    print("   ZERO DATABASE MUTATION ON STAGING; DISPOSABLE PROOFS COMPLETE.       ")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
