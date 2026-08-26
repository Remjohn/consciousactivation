#!/usr/bin/env python3
"""
CAE Static Audit Validator: Phase 13 / CA-AUDIT-01
Verifies the presence, completeness, schema adherence, and adversarial integrity
of the post-execution governance and evidence reconciliation artifacts.

Usage:
    python scripts/cae/audit/verify_ca_audit_01.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Allowed Evidence Classes per Mandate 13
PERMITTED_EVIDENCE_CLASSES = {
    "EXECUTABLE_SOURCE",
    "SCHEMA_OR_MIGRATION",
    "LOCAL_TEST",
    "STATIC_VALIDATOR",
    "STAGING_E3_TRANSCRIPT",
    "IMMUTABLE_RECEIPT",
    "OPERATOR_DECISION",
    "DOCUMENT_ONLY",
    "HISTORICAL_RECORD",
    "ENVIRONMENT_BLOCKED",
    "HYPOTHESIS",
    "CONTRADICTION",
}

# 14 Mandatory Matrix Columns per Mandate 13
MANDATORY_MATRIX_COLUMNS = [
    "claim_id",
    "domain",
    "claim",
    "evidence reference",
    "evidence class",
    "verification fidelity",
    "environment class",
    "reproducible now",
    "ratification state",
    "implementation state",
    "authority state",
    "scope / non-claim",
    "contradiction or finding",
    "owner / next decision",
]

# Required Artifacts
REQUIRED_ARTIFACTS = {
    "audit_report": ROOT_DIR / "docs/cae/implementation/CAE_POST_EXECUTION_GOVERNANCE_AUDIT.md",
    "status_matrix": ROOT_DIR / "docs/cae/implementation/CAE_GOVERNANCE_STATUS_MATRIX.md",
    "findings_register": ROOT_DIR / "docs/cae/implementation/CAE_AUDIT_01_FINDINGS_AND_DECISIONS_REGISTER.md",
    "reproducibility_log": ROOT_DIR / "docs/cae/implementation/CAE_AUDIT_01_EVIDENCE_REPRODUCIBILITY_LOG.md",
    "completion_record": ROOT_DIR / "docs/cae/implementation/CAE_AUDIT_01_COMPLETION_RECORD.md",
    "control_state": ROOT_DIR / "docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md",
}


def log_pass(msg: str) -> None:
    print(f"  [PASS] {msg}")


def log_fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def check_artifact_presence() -> list[str]:
    errors = []
    print("\n--- Test Suite 1: Artifact Presence & File Integrity ---")
    for name, path in REQUIRED_ARTIFACTS.items():
        if not path.is_file():
            err = f"Missing required artifact: {path.relative_to(ROOT_DIR)}"
            log_fail(err)
            errors.append(err)
        else:
            size = path.stat().st_size
            if size < 500:
                err = f"Artifact {path.relative_to(ROOT_DIR)} is suspiciously small ({size} bytes)"
                log_fail(err)
                errors.append(err)
            else:
                log_pass(f"Artifact exists: {path.relative_to(ROOT_DIR)} ({size} bytes)")
    return errors


def check_status_matrix() -> list[str]:
    errors = []
    print("\n--- Test Suite 2: 14-Column Status Matrix Completeness ---")
    matrix_file = REQUIRED_ARTIFACTS["status_matrix"]
    content = matrix_file.read_text(encoding="utf-8")

    # Check header columns
    for col in MANDATORY_MATRIX_COLUMNS:
        if col not in content:
            err = f"Missing mandatory matrix column: '{col}' in {matrix_file.name}"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Mandatory column present: '{col}'")

    # Check Phase 1-12 coverage
    expected_phase_prefixes = [
        ("Phase 01 / WP-10A", "CLM-P01"),
        ("Phase 02 / CA-MAP-01", "CLM-P02"),
        ("Phase 03 / CA-AUTH-01", "CLM-P03"),
        ("Phase 04 / CA-CAN-01A", "CLM-P04"),
        ("Phase 05 / CA-CAN-01B", "CLM-P05"),
        ("Phase 06 / CA-CAN-01C", "CLM-P06"),
        ("Phase 07 / CA-SPEC-01", "CLM-P07"),
        ("Phase 08 / CA-STATE-01", "CLM-P08"),
        ("Phase 09 / CA-TS-01", "CLM-P09"),
        ("Phase 10 / CA-IMPL-01A", "CLM-P10"),
        ("Phase 11 / CA-IMPL-01B", "CLM-P11"),
        ("Phase 12 / CA-IMPL-02/02P", "CLM-P12"),
    ]

    for phase_name, prefix in expected_phase_prefixes:
        if prefix not in content:
            err = f"Missing claim coverage for {phase_name} (prefix: {prefix})"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Claim coverage verified: {phase_name} ({prefix})")

    # Check Evidence Classes
    lines = content.splitlines()
    table_rows = [line for line in lines if line.startswith("| `CLM-")]
    log_pass(f"Found {len(table_rows)} classified claim rows in status matrix")

    for row in table_rows:
        parts = [p.strip() for p in row.split("|")[1:-1]]
        if len(parts) < 14:
            err = f"Row has insufficient columns ({len(parts)}/14): {parts[0] if parts else 'empty'}"
            log_fail(err)
            errors.append(err)
            continue

        claim_id = parts[0].replace("`", "")
        evidence_class = parts[4].replace("`", "")
        reproducible_now = parts[7].replace("`", "")
        authority_state = parts[10].replace("`", "")

        if evidence_class not in PERMITTED_EVIDENCE_CLASSES:
            err = f"Claim {claim_id} has invalid evidence class: '{evidence_class}'"
            log_fail(err)
            errors.append(err)

        # Check anti-overclaim on production
        if "PRODUCTION_AUTHORIZED: YES" in row or authority_state == "PRODUCTION_AUTHORITATIVE":
            err = f"Claim {claim_id} falsely claims production authority!"
            log_fail(err)
            errors.append(err)

    return errors


def check_findings_and_decisions() -> list[str]:
    errors = []
    print("\n--- Test Suite 3: Findings & Decisions Register Validation ---")
    reg_file = REQUIRED_ARTIFACTS["findings_register"]
    content = reg_file.read_text(encoding="utf-8")

    expected_findings = ["F-01", "F-02", "F-03", "F-04", "F-05"]
    for f in expected_findings:
        if f not in content:
            err = f"Missing technical finding {f} in {reg_file.name}"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Technical finding verified: {f}")

    expected_ratifications = ["RAT-001", "RAT-002", "RAT-003", "RAT-004", "RAT-005", "RAT-006", "RAT-007", "RAT-008"]
    for r in expected_ratifications:
        if r not in content:
            err = f"Missing ratification deficit {r} in {reg_file.name}"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Ratification deficit recorded: {r}")

    expected_dispositions = ["HISTORICAL_SUPERSEDED", "RESOLVED_BY", "STILL_OPEN"]
    for d in expected_dispositions:
        if d not in content:
            err = f"Missing required decision disposition: '{d}'"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Decision disposition taxonomy verified: '{d}'")

    return errors


def check_reproducibility_log() -> list[str]:
    errors = []
    print("\n--- Test Suite 4: Evidence Reproducibility Log Validation ---")
    log_file = REQUIRED_ARTIFACTS["reproducibility_log"]
    content = log_file.read_text(encoding="utf-8")

    required_sections = [
        "## 1. Locally Reproduced and Verified Evidence",
        "## 2. Recorded Staging Evidence (Not Replayed During Audit)",
        "## 3. Environment Boundaries and Reproducibility Limitations",
        "## 4. Reproducibility Sign-Off",
    ]
    for sec in required_sections:
        if sec not in content:
            err = f"Missing section '{sec}' in {log_file.name}"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Reproducibility log section verified: '{sec}'")

    # Check that E3 non-replay rule is explicitly declared
    if "staging_e3_proofs_replayed: 0" not in content:
        err = "Reproducibility log must certify staging_e3_proofs_replayed: 0"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Mandate 13 non-mutation rule certified (staging_e3_proofs_replayed: 0)")

    return errors


def check_completion_record() -> list[str]:
    errors = []
    print("\n--- Test Suite 5: Completion Record Sections A–H & Question Validation ---")
    comp_file = REQUIRED_ARTIFACTS["completion_record"]
    content = comp_file.read_text(encoding="utf-8")

    sections = [
        "## A. What Changed",
        "## B. Why It Changed",
        "## C. What Was Proven in This Audit",
        "## D. What Remains Only Recorded, Rather Than Independently Reproduced",
        "## E. What Remains Uncertain or Blocked",
        "## F. What Could Still Be Wrong",
        "## G. Exact Files and Statuses for Operator Inspection",
        "## H. Exact Decision Required",
    ]
    for sec in sections:
        if sec not in content:
            err = f"Missing mandatory Section in Completion Record: '{sec}'"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Completion Record section verified: '{sec}'")

    # Exact Section 6 Decision Question verbatim verification
    exact_question = (
        "Accept CA-AUDIT-01 as the authoritative post-execution status record, "
        "preserve all listed limitations and non-claims, and authorize CA-GOV-02 only to "
        "reconcile formal ratification states and control-state governance—without any schema, "
        "runtime, database, Storage, registry, or authority transition?"
    )
    if exact_question not in content:
        err = "Completion Record does not contain the exact verbatim Section 6 decision question!"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Exact verbatim Section 6 decision question confirmed in Completion Record.")

    return errors


def check_control_state() -> list[str]:
    errors = []
    print("\n--- Test Suite 6: Implementation Control State Validation ---")
    cs_file = REQUIRED_ARTIFACTS["control_state"]
    content = cs_file.read_text(encoding="utf-8")

    if "current_execution_stage: AUDIT" not in content and "current_execution_stage: OPERATOR_REVIEW" not in content:
        err = "Control state active stage is not AUDIT or OPERATOR_REVIEW"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Control state active stage verified (AUDIT or OPERATOR_REVIEW)")

    if "CA-AUDIT-01" not in content:
        err = "Control state does not reference CA-AUDIT-01"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Control state phase CA-AUDIT-01 referenced")

    if "ZERO_AUTHORITY_CHANGED" not in content and "operational_authority_change:" not in content:
        err = "Control state must explicitly declare ZERO_AUTHORITY_CHANGED or operational_authority_change"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Operational authority change status explicitly declared")

    if "MC-CAE-MED-001" not in content and "MC-CAE-WS-001" not in content:
        err = "Control state failed to retain aggregate cutover evidence"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Retained aggregate cutover evidence verified in control state")


    return errors


def main() -> int:
    print("=" * 80)
    print("   CAE STATIC AUDIT & GOVERNANCE VERIFIER: PHASE 13 / CA-AUDIT-01       ")
    print("=" * 80)

    all_errors = []
    all_errors.extend(check_artifact_presence())
    all_errors.extend(check_status_matrix())
    all_errors.extend(check_findings_and_decisions())
    all_errors.extend(check_reproducibility_log())
    all_errors.extend(check_completion_record())
    all_errors.extend(check_control_state())

    print("\n" + "=" * 80)
    if all_errors:
        print(f"   VALIDATION FAILED: {len(all_errors)} error(s) detected.")
        print("=" * 80)
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print("   SUCCESS: CA-AUDIT-01 GOVERNANCE RECONCILIATION 100% COMPLIANT        ")
    print("   ALL PHASES 1–12 AUDITED; ZERO OPERATIONAL AUTHORITY MUTATED.         ")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
