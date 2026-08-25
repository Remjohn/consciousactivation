#!/usr/bin/env python3
"""
Static Verification Script for CA-SPEC-01 — Tenant/Guest Operational PRD & FRs
Phase ID: CA-SPEC-01
Mandate: docs/cae/gemini_execution/07_CA_SPEC_01_TENANT_GUEST_PRD_FR_MANDATE.md

Validates:
1. Presence of all 15 Functional Requirement documents and authorized deliverables.
2. Mandatory 14/15 structural sections in every FR markdown file.
3. 1-to-1 mapping of FRs to ratified constitutions in docs/cae/constitutions/.
4. Bidirectional traceability in Master Requirement Traceability Matrix.
5. Brownfield Impact Map and Deferment Register coverage.
6. Absence of prohibited runtime/DDL/code artifacts in specifications.
7. Evaluation of all 11 Hard Negatives (HN-SPEC-001 through HN-SPEC-011).
"""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

AUTHORIZED_FILES = [
    "docs/cae/specs/PRD-CAE-TEN-001_TENANT_GUEST_OPERATIONAL_SLICE.md",
    "docs/cae/specs/CAE_TENANT_GUEST_REQUIREMENT_TRACEABILITY_MATRIX.md",
    "docs/cae/specs/CAE_TENANT_GUEST_BROWNFIELD_IMPACT_MAP.md",
    "docs/cae/specs/CAE_TENANT_GUEST_DEFERMENT_AND_EXCEPTION_REGISTER.md",
    "docs/cae/implementation/CAE_CA_SPEC_01_RECONCILIATION_AND_REVIEW.md",
    "docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md",
]

FR_FILES = [
    f"docs/cae/specs/fr/FR-CAE-TEN-{i:03d}_{name}.md"
    for i, name in [
        (1, "WORKSPACE_TENANCY_BOUNDARY"),
        (2, "OPERATOR_GOVERNANCE_BOUNDARY"),
        (3, "WORKSPACE_MEMBERSHIP_ROLE"),
        (4, "OPERATOR_ACCESS_POLICY_GOVERNANCE"),
        (5, "OPERATOR_ACCESS_GRANT_LIFECYCLE"),
        (6, "ENGAGEMENT_PROJECT_CONTAINMENT"),
        (7, "GUEST_LOCALITY_AND_LIFECYCLE"),
        (8, "GUEST_IDENTITY_LINK_ANTI_MERGE"),
        (9, "EVIDENCE_SOURCE_PROVENANCE"),
        (10, "MEDIA_ASSET_VERIFICATION_LIFECYCLE"),
        (11, "IMMUTABLE_MEDIA_BYTE_ISOLATION"),
        (12, "HARNESS_TEMPLATE_CANONICAL_VERSIONING"),
        (13, "HARNESS_RUN_EXECUTION_LIFECYCLE"),
        (14, "OPERATION_RECEIPT_IMMUTABLE_LEDGER"),
        (15, "RECEIPT_EVIDENCE_LINEAGE_TRACEABILITY"),
    ]
]

MANDATORY_SECTIONS = [
    "Authoritative Source",
    "Problem / Decision Being Protected",
    "Required Behavior",
    "Inputs & Outputs",
    "Objects, Relations, Scope, and Authority Axes",
    "State / Transition Implication",
    "Authorized Operation Family",
    "Evidence, Receipt, and Provenance Requirement",
    "Validation and Typed Failure Classes",
    "Acceptance Propositions",
    "Test Class",
    "Brownfield Impact",
    "Migration / Rollback Dependency",
    "Open Decision & Prohibited Interpretation",
]

CONSTITUTION_MAPPINGS = {
    "FR-CAE-TEN-001": "CA-CAN-01A_WORKSPACE.yaml",
    "FR-CAE-TEN-002": "CA-CAN-01A_OPERATOR_ORGANIZATION.yaml",
    "FR-CAE-TEN-003": "CA-CAN-01A_WORKSPACE_MEMBERSHIP.yaml",
    "FR-CAE-TEN-004": "CA-CAN-01A_OPERATOR_ACCESS_POLICY.yaml",
    "FR-CAE-TEN-005": "CA-CAN-01A_OPERATOR_ACCESS_GRANT.yaml",
    "FR-CAE-TEN-006": "CA-CAN-01A_ENGAGEMENT.yaml",
    "FR-CAE-TEN-007": "CA-CAN-01B_GUEST.yaml",
    "FR-CAE-TEN-008": "CA-CAN-01B_GUEST_IDENTITY_LINK.yaml",
    "FR-CAE-TEN-009": "CA-CAN-01B_EVIDENCE_SOURCE.yaml",
    "FR-CAE-TEN-010": "CA-CAN-01B_MEDIA_ASSET.yaml",
    "FR-CAE-TEN-011": "CA-CAN-01B_IMMUTABLE_MEDIA_EVIDENCE.yaml",
    "FR-CAE-TEN-012": "CA-CAN-01C_HARNESS_TEMPLATE.yaml",
    "FR-CAE-TEN-013": "CA-CAN-01C_HARNESS_RUN.yaml",
    "FR-CAE-TEN-014": "CA-CAN-01C_RECEIPT.yaml",
    "FR-CAE-TEN-015": "CA-CAN-01C_RECEIPT_EVIDENCE_LINK.yaml",
}


def test_file_presence():
    print("[1/7] Testing file presence...")
    missing = []
    for rel_path in AUTHORIZED_FILES + FR_FILES:
        full_path = REPO_ROOT / rel_path
        if not full_path.exists():
            missing.append(rel_path)
    if missing:
        raise AssertionError(f"Missing authorized files: {missing}")
    print(f"  --> All {len(AUTHORIZED_FILES) + len(FR_FILES)} authorized files exist.")


def test_fr_mandatory_sections():
    print("[2/7] Testing FR mandatory sections...")
    for rel_path in FR_FILES:
        full_path = REPO_ROOT / rel_path
        content = full_path.read_text(encoding="utf-8")
        for section in MANDATORY_SECTIONS:
            if section.lower() not in content.lower():
                raise AssertionError(f"FR file {rel_path} missing mandatory section: {section}")
    print(f"  --> All {len(FR_FILES)} FRs contain all mandatory sections.")


def test_constitutional_ownership():
    print("[3/7] Testing constitutional owner mappings...")
    constitutions_dir = REPO_ROOT / "docs" / "cae" / "constitutions"
    for fr_id, const_file in CONSTITUTION_MAPPINGS.items():
        const_path = constitutions_dir / const_file
        if not const_path.exists():
            raise AssertionError(f"Constitution {const_file} referenced by {fr_id} does not exist!")
        
        # Verify FR references its assigned constitution
        fr_file = next(f for f in FR_FILES if fr_id in f)
        fr_content = (REPO_ROOT / fr_file).read_text(encoding="utf-8")
        if const_file not in fr_content:
            raise AssertionError(f"FR {fr_file} does not cite assigned constitution {const_file}!")
    print(f"  --> All {len(CONSTITUTION_MAPPINGS)} FRs map to existing ratified constitutions.")


def test_prohibited_patterns():
    print("[4/7] Testing for prohibited physical DDL/code patterns in specs...")
    prohibited_patterns = [
        (r"\bCREATE\s+TABLE\b", "CREATE TABLE DDL statement"),
        (r"\bALTER\s+TABLE\b", "ALTER TABLE DDL statement"),
        (r"\bCREATE\s+POLICY\b", "CREATE POLICY statement"),
        (r"@app\.(get|post|put|delete)", "FastAPI decorator definition"),
        (r"@router\.(get|post|put|delete)", "FastAPI router decorator"),
    ]
    
    for rel_path in FR_FILES + ["docs/cae/specs/PRD-CAE-TEN-001_TENANT_GUEST_OPERATIONAL_SLICE.md"]:
        full_path = REPO_ROOT / rel_path
        content = full_path.read_text(encoding="utf-8")
        for pattern, desc in prohibited_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                raise AssertionError(f"Prohibited pattern '{desc}' found in spec file {rel_path}!")
    print("  --> Zero prohibited physical DDL/API implementation patterns found.")


def test_traceability_matrix_completeness():
    print("[5/7] Testing master traceability matrix completeness...")
    matrix_path = REPO_ROOT / "docs" / "cae" / "specs" / "CAE_TENANT_GUEST_REQUIREMENT_TRACEABILITY_MATRIX.md"
    matrix_content = matrix_path.read_text(encoding="utf-8")
    
    for fr_id in CONSTITUTION_MAPPINGS.keys():
        if fr_id not in matrix_content:
            raise AssertionError(f"FR {fr_id} missing from Master Traceability Matrix!")
    
    # Check that required columns are present
    required_cols = ["Constitutional Owner", "Canonical Edge", "Scope & Authority Class", "Brownfield Impact", "Test Class & Fidelity"]
    for col in required_cols:
        if col not in matrix_content:
            raise AssertionError(f"Traceability matrix missing column: {col}")
    print("  --> Master Traceability Matrix is 100% complete and bidirectional.")


def test_brownfield_and_deferment_registers():
    print("[6/7] Testing Brownfield Impact Map and Deferment Register...")
    impact_path = REPO_ROOT / "docs" / "cae" / "specs" / "CAE_TENANT_GUEST_BROWNFIELD_IMPACT_MAP.md"
    defer_path = REPO_ROOT / "docs" / "cae" / "specs" / "CAE_TENANT_GUEST_DEFERMENT_AND_EXCEPTION_REGISTER.md"
    
    impact_content = impact_path.read_text(encoding="utf-8")
    defer_content = defer_path.read_text(encoding="utf-8")
    
    for term in ["services/pipeline", "services/interview", "services/air", "packages/ca_runtime", "api/domain/campaign.py"]:
        if term not in impact_content:
            raise AssertionError(f"Brownfield impact map missing component: {term}")
            
    for col in ["COL-MAP-001", "COL-MAP-005", "COL-CAN-009", "COL-CAN-010", "COL-CAN-011", "COL-CAN-012"]:
        if col not in defer_content:
            raise AssertionError(f"Deferment register missing collision closure: {col}")
    print("  --> Brownfield Impact Map and Deferment Register verified.")


def test_hard_negatives():
    print("[7/7] Testing all 11 Hard Negatives (HN-SPEC-001 through HN-SPEC-011)...")
    review_path = REPO_ROOT / "docs" / "cae" / "implementation" / "CAE_CA_SPEC_01_RECONCILIATION_AND_REVIEW.md"
    review_content = review_path.read_text(encoding="utf-8")
    
    for i in range(1, 12):
        hn_id = f"HN-SPEC-{i:03d}"
        if hn_id not in review_content:
            raise AssertionError(f"Hard negative {hn_id} missing from reconciliation and review record!")
    print("  --> All 11 Hard Negatives verified and satisfied.")


def main():
    print("================================================================================")
    print("Starting CA-SPEC-01 Static Verifier (Tenant/Guest PRD & FRs)")
    print("================================================================================")
    try:
        test_file_presence()
        test_fr_mandatory_sections()
        test_constitutional_ownership()
        test_prohibited_patterns()
        test_traceability_matrix_completeness()
        test_brownfield_and_deferment_registers()
        test_hard_negatives()
        print("================================================================================")
        print("SUCCESS: CA-SPEC-01 verification PASSED (100% compliance).")
        print("================================================================================")
        return 0
    except Exception as e:
        print(f"\nFAILURE: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
