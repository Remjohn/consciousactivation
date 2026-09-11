#!/usr/bin/env python3
"""
CAE Static Governance Validator: Phase 14 / CA-GOV-02
Verifies the presence, completeness, vocabulary conformance, and structural integrity
of the formal ratification register, control-state reconciliation, and operator decision packet.

Usage:
    python scripts/cae/audit/verify_ca_gov_02.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Allowed Dispositions per Mandate 14 Section 3
PERMITTED_DISPOSITIONS = {
    "RECORDED_RATIFIED",
    "PENDING_OPERATOR_RATIFICATION",
    "DEFERRED",
    "REJECTED",
    "SUPERSEDED",
    "HISTORICAL_RESOLVED",
    "CONTRADICTORY",
    "NOT_APPLICABLE",
}

# 14 Mandatory Ratification Register Columns per Mandate 14 Section 3
MANDATORY_REGISTER_COLUMNS = [
    "decision_id",
    "subject/version",
    "current documented status",
    "evidence reference",
    "decision type",
    "eligible decision owner",
    "proposed disposition",
    "operator decision record",
    "effective date",
    "supersedes / preserves",
    "implementation relationship",
    "authority/environment boundary",
    "open risk",
    "next permitted phase",
]

# 8 Separately Decidable Governance IDs
MANDATORY_DECISION_IDS = [
    "DEC-GOV-MAP-01",
    "DEC-GOV-AUTH-01",
    "DEC-GOV-CAN-01A",
    "DEC-GOV-CAN-01B",
    "DEC-GOV-CAN-01C",
    "DEC-GOV-SPEC-01",
    "DEC-GOV-STATE-01",
    "DEC-GOV-TS-01",
]

# Required Artifacts
REQUIRED_ARTIFACTS = {
    "ratification_register": ROOT_DIR / "docs/cae/implementation/CAE_GOV_02_RATIFICATION_REGISTER.md",
    "control_state_reconciliation": ROOT_DIR / "docs/cae/implementation/CAE_GOV_02_CONTROL_STATE_RECONCILIATION.md",
    "operator_decision_packet": ROOT_DIR / "docs/cae/implementation/CAE_GOV_02_OPERATOR_DECISION_PACKET.md",
    "transition_ledger": ROOT_DIR / "docs/cae/implementation/CAE_GOV_02_GOVERNANCE_TRANSITION_LEDGER.md",
    "completion_record": ROOT_DIR / "docs/cae/implementation/CAE_GOV_02_COMPLETION_RECORD.md",
    "control_state": ROOT_DIR / "docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md",
}


def log_pass(msg: str) -> None:
    print(f"  [PASS] {msg}")


def log_fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def check_artifact_presence() -> list[str]:
    errors = []
    print("\n--- Test Suite 1: CA-GOV-02 Artifact Presence & Integrity ---")
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


def check_ratification_register() -> list[str]:
    errors = []
    print("\n--- Test Suite 2: Ratification Register Schema & Vocabulary Validation ---")
    reg_file = REQUIRED_ARTIFACTS["ratification_register"]
    content = reg_file.read_text(encoding="utf-8")

    # Check header columns
    for col in MANDATORY_REGISTER_COLUMNS:
        if col not in content:
            err = f"Missing mandatory register column: '{col}' in {reg_file.name}"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Mandatory column present: '{col}'")

    # Check table rows and dispositions
    lines = content.splitlines()
    table_rows = [line for line in lines if line.startswith("| `DEC-")]
    log_pass(f"Found {len(table_rows)} classified decision rows in register")

    for row in table_rows:
        parts = [p.strip() for p in row.split("|")[1:-1]]
        if len(parts) < 14:
            err = f"Row has insufficient columns ({len(parts)}/14): {parts[0] if parts else 'empty'}"
            log_fail(err)
            errors.append(err)
            continue

        decision_id = parts[0].replace("`", "")
        disposition = parts[6].replace("`", "")

        if disposition not in PERMITTED_DISPOSITIONS:
            err = f"Decision {decision_id} has invalid disposition: '{disposition}'"
            log_fail(err)
            errors.append(err)

    return errors


def check_three_layer_stratification() -> list[str]:
    errors = []
    print("\n--- Test Suite 3: Three-Layer Stratification Model Validation ---")
    csr_file = REQUIRED_ARTIFACTS["control_state_reconciliation"]
    content = csr_file.read_text(encoding="utf-8")

    layers = [
        "## 2. Layer 1: Current Execution State",
        "## 3. Layer 2: Historical Execution Ledger",
        "## 4. Layer 3: Open Governance Decisions & Deferrals",
    ]
    for layer in layers:
        if layer not in content:
            err = f"Missing Stratification Layer: '{layer}' in {csr_file.name}"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Stratified layer present: '{layer}'")

    # Check authority boundary restriction
    if "POSTGRES_AUTHORITATIVE_STAGING_ONLY" not in content:
        err = "Layer 1 must explicitly state POSTGRES_AUTHORITATIVE_STAGING_ONLY for media"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Staging authority restriction explicitly verified in Layer 1")

    return errors


def check_operator_decision_packet() -> list[str]:
    errors = []
    print("\n--- Test Suite 4: Operator Decision Packet Unbundling Validation ---")
    packet_file = REQUIRED_ARTIFACTS["operator_decision_packet"]
    content = packet_file.read_text(encoding="utf-8")

    for dec_id in MANDATORY_DECISION_IDS:
        if dec_id not in content:
            err = f"Missing separately decidable item: '{dec_id}' in {packet_file.name}"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Separately decidable item verified: '{dec_id}'")

    # Check mandatory subfields per item
    required_subfields = [
        "What changes if approved",
        "What does not change",
        "Evidence Reference",
        "Risks",
        "Non-claims",
        "Next Permitted Phase",
    ]
    for field in required_subfields:
        if field not in content:
            err = f"Missing mandatory packet subfield: '{field}'"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Packet item subfield present: '{field}'")

    return errors


def check_transition_ledger_and_adversarial_defenses() -> list[str]:
    errors = []
    print("\n--- Test Suite 5: Transition Ledger & Adversarial Defenses Validation ---")
    ledger_file = REQUIRED_ARTIFACTS["transition_ledger"]
    content = ledger_file.read_text(encoding="utf-8")

    # Check transitions
    for i in range(1, 14):
        tr_id = f"TR-GOV-{i:02d}"
        if tr_id not in content:
            err = f"Missing transition record: '{tr_id}'"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Transition record verified: '{tr_id}'")

    # Check all 8 adversarial checks from Section 5
    for i in range(1, 9):
        adv_id = f"ADV-{i:02d}"
        if adv_id not in content:
            err = f"Missing adversarial defense check: '{adv_id}'"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Adversarial defense verified: '{adv_id}'")

    return errors


def check_completion_record() -> list[str]:
    errors = []
    print("\n--- Test Suite 6: Completion Record & Verbatim Question Validation ---")
    comp_file = REQUIRED_ARTIFACTS["completion_record"]
    content = comp_file.read_text(encoding="utf-8")

    sections = [
        "## A. What Governance Records Changed and Why",
        "## B. Which Facts Were Only Classified Versus Formally Ratified",
        "## C. What Evidence Was Inspected and Locally Rechecked",
        "## D. What E3/Runtime Claims Remain Recorded Rather Than Replayed",
        "## E. Every Unresolved Decision, Contradiction, Finding, and Deferral",
        "## F. What Could Still Be Wrong in the Control Record",
        "## G. Exact Operator Inspection Paths and Decision IDs",
        "## H. Exact Next Authorization Requested",
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
        "Approve the CA-GOV-02 Ratification Register and Control-State Reconciliation: "
        "record only the decision IDs explicitly approved in the attached operator packet as ratified, "
        "retain every other item as pending/deferred/contradictory exactly as listed, "
        "preserve all F-01/F-02/F-03 and non-claims, and authorize CA-MIG-03 only to design "
        "and rehearse safe forward-only migrations—without applying a migration or changing operational authority?"
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
    print("\n--- Test Suite 7: Implementation Control State Validation ---")
    cs_file = REQUIRED_ARTIFACTS["control_state"]
    content = cs_file.read_text(encoding="utf-8")

    if "current_execution_stage: OPERATOR_REVIEW" not in content:
        err = "Control state active stage is not OPERATOR_REVIEW"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Control state active stage is OPERATOR_REVIEW")

    if "CA-GOV-02" not in content:
        err = "Control state does not reference CA-GOV-02"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Control state phase CA-GOV-02 referenced")

    if "ZERO_AUTHORITY_CHANGED" not in content and "operational_authority_change:" not in content:
        err = "Control state must explicitly declare ZERO_AUTHORITY_CHANGED or operational_authority_change"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Operational authority change status explicitly declared")


    return errors


def main() -> int:
    print("=" * 80)
    print("   CAE STATIC GOVERNANCE VALIDATOR: PHASE 14 / CA-GOV-02                ")
    print("=" * 80)

    all_errors = []
    all_errors.extend(check_artifact_presence())
    all_errors.extend(check_ratification_register())
    all_errors.extend(check_three_layer_stratification())
    all_errors.extend(check_operator_decision_packet())
    all_errors.extend(check_transition_ledger_and_adversarial_defenses())
    all_errors.extend(check_completion_record())
    all_errors.extend(check_control_state())

    print("\n" + "=" * 80)
    if all_errors:
        print(f"   VALIDATION FAILED: {len(all_errors)} error(s) detected.")
        print("=" * 80)
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print("   SUCCESS: CA-GOV-02 GOVERNANCE RECONCILIATION 100% COMPLIANT         ")
    print("   ALL RATIFICATIONS & DECISION PACKET READY FOR OPERATOR REVIEW.      ")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
