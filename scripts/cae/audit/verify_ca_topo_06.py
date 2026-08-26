#!/usr/bin/env python3
"""
Static Governance and Structural Validator for Phase 18 / CA-TOPO-06.

Validates:
1. Presence and structure of all 6 CA-TOPO-06 documentation artifacts.
2. Topology inventory completeness (11 entities, WP03_TEXT_FAMILY vs CA_IMPL_UUID_FAMILY).
3. Contract-route matrix analysis (bridge failure analysis & typed workaround bounding).
4. Collision & option analysis (Option A, Option B, Option C).
5. Read-only staging inspection record (ENVIRONMENT_BLOCKED declaration).
6. Operator decision packet structure & option tokens.
7. Completion record structure (Sections A–G) and exact Section 6 decision question.
8. Implementation Control State update to F02_TOPOLOGY_EVIDENCED_DECISION_REQUIRED.

Usage:
    python scripts/cae/audit/verify_ca_topo_06.py
"""

from __future__ import annotations

import os
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
DOCS_DIR = ROOT_DIR / "docs/cae/implementation"
CONTROL_STATE_PATH = DOCS_DIR / "CAE_IMPLEMENTATION_CONTROL_STATE.md"

REQUIRED_DOCUMENTS = [
    "CAE_TOPO_06_F02_TOPOLOGY_INVENTORY.md",
    "CAE_TOPO_06_F02_CONTRACT_ROUTE_MATRIX.md",
    "CAE_TOPO_06_F02_COLLISION_AND_OPTION_ANALYSIS.md",
    "CAE_TOPO_06_F02_READ_ONLY_STAGING_INSPECTION.md",
    "CAE_TOPO_06_OPERATOR_DECISION_PACKET.md",
    "CAE_TOPO_06_COMPLETION_RECORD.md",
]

EXPECTED_SECTION_6_QUESTION = (
    "Select one CA-TOPO-06 topology option and its named canonical route/identity boundary for the "
    "F-02-affected relations, preserve all other options and non-claims as rejected or deferred, and "
    "authorize CA-TOPO-07 only to implement and prove that selected topology in a new disposable "
    "environment—without moving client data, altering shared staging, or changing operational authority?"
)


def log_pass(msg: str) -> None:
    print(f"  [PASS] {msg}")


def log_fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def verify_documents() -> bool:
    print("--- Test Suite 1: CA-TOPO-06 Documentation Artifacts ---")
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


def verify_topology_inventory() -> bool:
    print("\n--- Test Suite 2: Topology Inventory Completeness ---")
    inv_path = DOCS_DIR / "CAE_TOPO_06_F02_TOPOLOGY_INVENTORY.md"
    content = inv_path.read_text(encoding="utf-8")
    all_ok = True
    for token in [
        "WP03_TEXT_FAMILY",
        "CA_IMPL_UUID_FAMILY",
        "TOPO-01", "TOPO-02", "TOPO-03", "TOPO-04", "TOPO-05",
        "TOPO-06", "TOPO-07", "TOPO-08", "TOPO-09", "TOPO-10", "TOPO-11",
        "TOPOLOGY_EVIDENCED_DECISION_REQUIRED",
    ]:
        if token not in content:
            log_fail(f"Missing required inventory token: '{token}'")
            all_ok = False
        else:
            log_pass(f"Inventory token verified: '{token}'")
    return all_ok


def verify_contract_route_matrix() -> bool:
    print("\n--- Test Suite 3: Contract-Route Matrix & Root Cause ---")
    crm_path = DOCS_DIR / "CAE_TOPO_06_F02_CONTRACT_ROUTE_MATRIX.md"
    content = crm_path.read_text(encoding="utf-8")
    all_ok = True
    for token in [
        "CAE-BRIDGE-001.verified-interview-source-registration",
        "CAE-MEDIA-001.media-verification",
        "cae.project",
        "cae.media_asset",
        "register_verified_interview_source",
        "verify_media_asset",
        "BLOCKED_SCHEMA_MISMATCH",
        "BOUNDED_TYPED_ROUTE_ACTIVE",
    ]:
        if token not in content:
            log_fail(f"Missing required route token: '{token}'")
            all_ok = False
        else:
            log_pass(f"Route token verified: '{token}'")
    return all_ok


def verify_collision_and_options() -> bool:
    print("\n--- Test Suite 4: Collision & Option Analysis ---")
    opt_path = DOCS_DIR / "CAE_TOPO_06_F02_COLLISION_AND_OPTION_ANALYSIS.md"
    content = opt_path.read_text(encoding="utf-8")
    all_ok = True
    for token in [
        "Option A: Canonical CA-IMPL UUID Target",
        "Option B: Canonical WP-03 Text-Keyed Topology",
        "Option C: Namespaced Dual Coexistence",
        "TS-CAE-TEN-001",
    ]:
        if token not in content:
            log_fail(f"Missing required option token: '{token}'")
            all_ok = False
        else:
            log_pass(f"Option token verified: '{token}'")
    return all_ok


def verify_staging_inspection() -> bool:
    print("\n--- Test Suite 5: Read-Only Staging Inspection Record ---")
    stg_path = DOCS_DIR / "CAE_TOPO_06_F02_READ_ONLY_STAGING_INSPECTION.md"
    content = stg_path.read_text(encoding="utf-8")
    all_ok = True
    for token in [
        "ENVIRONMENT_BLOCKED",
        "evnxdssbxxrsesftdvgx",
        "No Negative Inference",
        "Source Truth Rigor",
    ]:
        if token not in content:
            log_fail(f"Missing required inspection token: '{token}'")
            all_ok = False
        else:
            log_pass(f"Inspection token verified: '{token}'")
    return all_ok


def verify_decision_packet() -> bool:
    print("\n--- Test Suite 6: Operator Decision Packet & Tokens ---")
    dp_path = DOCS_DIR / "CAE_TOPO_06_OPERATOR_DECISION_PACKET.md"
    content = dp_path.read_text(encoding="utf-8")
    all_ok = True
    for token in [
        "DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET",
        "DECISION_TOPO_OPTION_B_RETAIN_WP03_TEXT_BASELINE",
        "DECISION_TOPO_OPTION_C_NAMESPACED_DUAL_COEXISTENCE",
    ]:
        if token not in content:
            log_fail(f"Missing decision token: '{token}'")
            all_ok = False
        else:
            log_pass(f"Decision token verified: '{token}'")
    return all_ok


def verify_completion_record() -> bool:
    print("\n--- Test Suite 7: Completion Record & Section 6 Question ---")
    comp_path = DOCS_DIR / "CAE_TOPO_06_COMPLETION_RECORD.md"
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
    print("\n--- Test Suite 8: Implementation Control State Validation ---")
    content = CONTROL_STATE_PATH.read_text(encoding="utf-8")
    all_ok = True

    valid_statuses = [
        "F02_TOPOLOGY_EVIDENCED_DECISION_REQUIRED",
        "F02_SELECTED_TOPOLOGY_E3_PROVEN_DISPOSABLE_ONLY",
    ]
    if not any(f"**Control status:** `{st}`" in content for st in valid_statuses):
        log_fail("Control status is not F02_TOPOLOGY_EVIDENCED_DECISION_REQUIRED or downstream")
        all_ok = False
    else:
        log_pass("Control status verified (F02_TOPOLOGY_EVIDENCED_DECISION_REQUIRED or downstream)")

    if "CA-TOPO-06" not in content:
        log_fail("Control state does not contain CA-TOPO-06")
        all_ok = False
    else:
        log_pass("Control state contains CA-TOPO-06")

    if "operational_authority_change: ZERO_AUTHORITY_CHANGED" not in content:
        log_fail("Missing explicit zero operational authority change assertion")
        all_ok = False
    else:
        log_pass("Zero operational authority change explicitly verified")

    return all_ok


def main() -> int:
    print("=" * 80)
    print("   CAE STATIC GOVERNANCE VALIDATOR: PHASE 18 / CA-TOPO-06               ")
    print("=" * 80)

    suites = [
        verify_documents,
        verify_topology_inventory,
        verify_contract_route_matrix,
        verify_collision_and_options,
        verify_staging_inspection,
        verify_decision_packet,
        verify_completion_record,
        verify_control_state,
    ]

    all_passed = True
    for s in suites:
        if not s():
            all_passed = False

    print("\n" + "=" * 80)
    if not all_passed:
        print("   VALIDATION FAILED: One or more CA-TOPO-06 governance rules violated.")
        print("=" * 80)
        return 1

    print("   SUCCESS: CA-TOPO-06 TOPOLOGY RECONCILIATION 100% COMPLIANT          ")
    print("   READ-LED INVENTORY COMPLETE; OPERATOR DECISION PACKET PREPARED.     ")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
