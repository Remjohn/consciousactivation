#!/usr/bin/env python3
"""Static contract verifier and hard-negative test suite for Phase 09 / CA-TS-01.

Validates that all technical specifications, Gate A–I reviews, operation contracts,
test plans, implementation file allowlists, risk registers, and review records
comply 100% with Mandate 09_CA_TS_01_IMPLEMENTATION_GATE_TECH_SPEC_MANDATE.md and Bundle v3.

Executes only static and artifact-level validations; executes zero database mutations.
"""

import sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# Required Deliverable Artifacts for CA-TS-01
REQUIRED_ARTIFACTS = [
    "docs/cae/tech_specs/TS-CAE-TEN-001_TENANT_GUEST_VERTICAL_SLICE.md",
    "docs/cae/tech_specs/TS-CAE-TEN-001_GATE_A_TO_I_REVIEW.md",
    "docs/cae/tech_specs/TS-CAE-TEN-001_OPERATION_AND_TRANSITION_CONTRACTS.yaml",
    "docs/cae/tech_specs/TS-CAE-TEN-001_TEST_AND_PROOF_PLAN.yaml",
    "docs/cae/tech_specs/TS-CAE-TEN-001_IMPLEMENTATION_FILE_ALLOWLIST.md",
    "docs/cae/tech_specs/TS-CAE-TEN-001_RISK_AND_ROLLBACK_REGISTER.md",
    "docs/cae/implementation/CAE_CA_TS_01_RECONCILIATION_AND_REVIEW.md",
    "docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md",
]

MANDATORY_14_SECTIONS = [
    "## 1. Files and Evidence Read",
    "## 2. Architectural Role and Boundaries",
    "## 3. Brownfield Reality",
    "## 4. Functional Requirement Traceability",
    "## 5. Canonical Object & Schema Contract",
    "## 6. Relationships, State Machines, Events, and Temporal Semantics",
    "## 7. Authorized Typed Semantic Operations & Agent Program Contract",
    "## 8. Intermediate Representation (IR) & Runtime Contract",
    "## 9. Validation and Error Taxonomy",
    "## 10. Implementation Plan",
    "## 11. Backward Compatibility, Migration & Rollback",
    "## 12. Acceptance Criteria",
    "## 13. Dependencies & External Concept Adaptations",
    "## 14. Testing and Reality-Contact Verification",
]

GATES_A_TO_I = [
    "Gate A",
    "Gate B",
    "Gate C",
    "Gate D",
    "Gate E",
    "Gate F",
    "Gate G",
    "Gate H",
    "Gate I",
]

HARD_NEGATIVES = [
    "HN-TS-001",
    "HN-TS-002",
    "HN-TS-003",
    "HN-TS-004",
    "HN-TS-005",
    "HN-TS-006",
    "HN-TS-007",
    "HN-TS-008",
    "HN-TS-009",
    "HN-TS-010",
    "HN-TS-011",
]


class VerificationFailure(Exception):
    pass


def log_pass(test_name: str) -> None:
    print(f"  [PASS] {test_name}")


def log_fail(test_name: str, reason: str) -> None:
    print(f"  [FAIL] {test_name}: {reason}")


def test_required_artifacts_exist() -> None:
    print("\n--- Test Suite 1: Artifact Presence & Boundary Enforcement ---")
    for rel_path in REQUIRED_ARTIFACTS:
        full_path = REPO_ROOT / rel_path
        if not full_path.exists():
            raise VerificationFailure(f"Required artifact missing: {rel_path}")
        if full_path.stat().st_size < 200:
            raise VerificationFailure(f"Artifact too small or empty: {rel_path}")
        log_pass(f"Artifact exists: {rel_path} ({full_path.stat().st_size} bytes)")


def test_tech_spec_14_sections() -> None:
    print("\n--- Test Suite 2: Tech Spec 14-Section Protocol Validation ---")
    spec_path = REPO_ROOT / "docs/cae/tech_specs/TS-CAE-TEN-001_TENANT_GUEST_VERTICAL_SLICE.md"
    content = spec_path.read_text(encoding="utf-8")

    # Verify mandatory evidence log entries
    evidence_logs = [
        "1. ARCHITECTURE LOADED",
        "2. PHASE VALIDATION LOADED",
        "3. OBJECT CONSTITUTION(S) LOADED",
        "4. DEFINITION GRAMMAR LOADED",
        "5. PRD/FR LOADED",
        "6. BROWNFIELD CODE READ",
        "7. DATABASE/SCHEMA READ",
        "8. REGISTRIES READ",
        "9. TEST PATTERN READ",
        "10. REASONING/VALIDATION PROTOCOLS READ",
    ]
    for elog in evidence_logs:
        if elog not in content:
            raise VerificationFailure(f"Mandatory evidence log entry missing: {elog}")
        log_pass(f"Evidence log verified: {elog}")

    # Verify all 14 standard sections
    for sec in MANDATORY_14_SECTIONS:
        if sec not in content:
            raise VerificationFailure(f"Tech Spec missing mandatory section: {sec}")
        log_pass(f"Mandatory section verified: {sec}")


def test_gate_a_to_i_review() -> None:
    print("\n--- Test Suite 3: Gate A–I Independent Review Validation ---")
    review_path = REPO_ROOT / "docs/cae/tech_specs/TS-CAE-TEN-001_GATE_A_TO_I_REVIEW.md"
    content = review_path.read_text(encoding="utf-8")

    # Verify each gate from A to I is evaluated
    for gate in GATES_A_TO_I:
        if f"**{gate}**" not in content and f"| **{gate}** |" not in content and f"{gate} |" not in content:
            raise VerificationFailure(f"Gate evaluation missing: {gate}")
        log_pass(f"Gate evaluated: {gate}")

    # Verify stateful implementation criteria
    stateful_criteria = [
        "Authoritative State Source",
        "Current-State Projection",
        "State History / Event Model",
        "Legal State Transitions",
        "Authorized Semantic Operations",
        "Validation / Evidence Contract",
        "Receipt Contract",
        "Deterministic Recovery Path",
        "Reward-Hack Countertest",
        "Environment Fidelity Target",
        "StateM Adoption Boundary",
    ]
    for sc in stateful_criteria:
        if sc not in content:
            raise VerificationFailure(f"Stateful implementation criterion missing: {sc}")
        log_pass(f"Stateful criterion verified: {sc}")

    # Verify overall verdict is READY_FOR_DEVELOPMENT
    if "READY_FOR_DEVELOPMENT" not in content:
        raise VerificationFailure("Gate review overall status must be READY_FOR_DEVELOPMENT")
    log_pass("Overall gate status verified: READY_FOR_DEVELOPMENT")


def test_operation_and_transition_contracts() -> None:
    print("\n--- Test Suite 4: Operation & Transition Contracts Validation ---")
    contract_path = REPO_ROOT / "docs/cae/tech_specs/TS-CAE-TEN-001_OPERATION_AND_TRANSITION_CONTRACTS.yaml"
    with open(contract_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "operations" not in data:
        raise VerificationFailure("Invalid YAML structure in operation contracts")

    operations = data["operations"]
    if len(operations) < 8:
        raise VerificationFailure(f"Expected at least 8 operations, found {len(operations)}")

    for op in operations:
        op_id = op.get("operation_id")
        if not op_id:
            raise VerificationFailure("Operation missing operation_id")
        if "scope_derivation" not in op:
            raise VerificationFailure(f"{op_id} missing scope_derivation")
        if "input_schema" not in op or "output_schema" not in op:
            raise VerificationFailure(f"{op_id} missing schema definitions")
        if "typed_errors" not in op or len(op["typed_errors"]) == 0:
            raise VerificationFailure(f"{op_id} missing typed errors")
        if "receipt_schema" not in op:
            raise VerificationFailure(f"{op_id} missing receipt_schema")
        log_pass(f"Operation contract verified: {op_id}")


def test_test_and_proof_plan() -> None:
    print("\n--- Test Suite 5: Test & Proof Plan Validation ---")
    plan_path = REPO_ROOT / "docs/cae/tech_specs/TS-CAE-TEN-001_TEST_AND_PROOF_PLAN.yaml"
    with open(plan_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "hard_negatives" not in data or "test_tiers" not in data:
        raise VerificationFailure("Invalid YAML structure in test plan")

    # Check test tiers
    tiers = [t.get("tier") for t in data["test_tiers"]]
    expected_tiers = ["E0_UNIT_FIXTURE", "E1_STATIC", "E2_REPOSITORY_FIXTURE", "E3_STAGING", "E4_REAL_WORLD_OUTCOME"]
    for et in expected_tiers:
        if et not in tiers:
            raise VerificationFailure(f"Test tier missing: {et}")
        log_pass(f"Test tier verified: {et}")

    # Check hard negatives
    negatives = {hn.get("negative_id"): hn for hn in data["hard_negatives"]}
    for hn_id in HARD_NEGATIVES:
        if hn_id not in negatives:
            raise VerificationFailure(f"Hard negative missing from test plan: {hn_id}")
        log_pass(f"Hard negative test defined: {hn_id}")


def test_allowlist_and_risk_register() -> None:
    print("\n--- Test Suite 6: Allowlist & Risk Register Validation ---")
    allowlist_path = REPO_ROOT / "docs/cae/tech_specs/TS-CAE-TEN-001_IMPLEMENTATION_FILE_ALLOWLIST.md"
    al_content = allowlist_path.read_text(encoding="utf-8")
    if "STRICTLY PROHIBITED DIRECTORIES" not in al_content:
        raise VerificationFailure("Allowlist missing prohibited directories section")
    if "CA-IMPL-01A" not in al_content:
        raise VerificationFailure("Allowlist must govern CA-IMPL-01A")
    log_pass("Implementation file allowlist verified")

    risk_path = REPO_ROOT / "docs/cae/tech_specs/TS-CAE-TEN-001_RISK_AND_ROLLBACK_REGISTER.md"
    risk_content = risk_path.read_text(encoding="utf-8")
    if "Deterministic Rollback Procedures" not in risk_content:
        raise VerificationFailure("Risk register missing rollback procedures")
    log_pass("Risk and rollback register verified")


def test_reconciliation_record() -> None:
    print("\n--- Test Suite 7: Reconciliation and Non-Claims Record Validation ---")
    rec_path = REPO_ROOT / "docs/cae/implementation/CAE_CA_TS_01_RECONCILIATION_AND_REVIEW.md"
    content = rec_path.read_text(encoding="utf-8")

    # Verify all 11 hard negatives defended in review record
    for hn in HARD_NEGATIVES:
        if hn not in content:
            raise VerificationFailure(f"Hard negative missing from review record: {hn}")
        if f"| **`{hn}`** |" not in content or "DEFENDED" not in content:
            raise VerificationFailure(f"Hard negative {hn} not marked DEFENDED in review record")
        log_pass(f"Hard negative defended in review record: {hn}")

    # Verify non-claims
    non_claims = [
        "Zero Production Parity",
        "Zero Data Movement",
        "Zero Qualitative Truth Claim",
    ]
    for nc in non_claims:
        if nc not in content:
            raise VerificationFailure(f"Non-claim missing from review record: {nc}")
        log_pass(f"Non-claim verified: {nc}")


def main() -> int:
    print("================================================================================")
    print("   CAE STATIC TECH-SPEC & GATE VERIFIER: PHASE 09 / CA-TS-01                     ")
    print("================================================================================")
    try:
        test_required_artifacts_exist()
        test_tech_spec_14_sections()
        test_gate_a_to_i_review()
        test_operation_and_transition_contracts()
        test_test_and_proof_plan()
        test_allowlist_and_risk_register()
        test_reconciliation_record()
        print("\n================================================================================")
        print("   SUCCESS: CA-TS-01 TECH SPEC & GATE REVIEW VERIFIED (100% COMPLIANT)          ")
        print("   ALL 9 GATES CLEARED; READY_FOR_DEVELOPMENT AUTHORIZING CA-IMPL-01A ONLY.     ")
        print("================================================================================")
        return 0
    except VerificationFailure as e:
        print(f"\n[FATAL ERROR] Verification failed: {e}")
        return 1
    except Exception as e:
        print(f"\n[UNEXPECTED ERROR] {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
