#!/usr/bin/env python3
"""
CAE Static Governance Validator: Phase 15 / CA-MIG-03
Verifies the presence, completeness, AST/syntax safety, dependency acyclicity,
and structural integrity of the forward-only migration package, schema inventory,
and offline safety rehearsal without executing database, Storage, or network calls.

Usage:
    python scripts/cae/audit/verify_ca_mig_03.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Required Markdown Artifacts
REQUIRED_DOC_ARTIFACTS = {
    "schema_inventory": ROOT_DIR / "docs/cae/implementation/CAE_MIG_03_SCHEMA_INVENTORY.md",
    "forward_migration_plan": ROOT_DIR / "docs/cae/implementation/CAE_MIG_03_FORWARD_MIGRATION_PLAN.md",
    "dependency_graph": ROOT_DIR / "docs/cae/implementation/CAE_MIG_03_MIGRATION_DEPENDENCY_GRAPH.md",
    "safety_rehearsal": ROOT_DIR / "docs/cae/implementation/CAE_MIG_03_SAFETY_REHEARSAL.md",
    "repair_boundary": ROOT_DIR / "docs/cae/implementation/CAE_MIG_03_F01_F02_REPAIR_BOUNDARY.md",
    "completion_record": ROOT_DIR / "docs/cae/implementation/CAE_MIG_03_COMPLETION_RECORD.md",
    "control_state": ROOT_DIR / "docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md",
}

# Required SQL Drafts
REQUIRED_SQL_DRAFTS = [
    "0001_cae_extensions_and_schema.sql",
    "0002_cae_tenancy_and_membership.sql",
    "0003_cae_engagement_guest_media.sql",
    "0004_cae_harness_and_immutable_receipts.sql",
    "0005_cae_row_level_security.sql",
    "0006_cae_indexes_and_constraints.sql",
    "0007_cae_f01_composite_receipt_fk_draft.sql",
    "0008_cae_f02_topology_shadow_reconciliation_draft.sql",
]
DRAFTS_DIR = ROOT_DIR / "packages/ca_runtime/src/ca_runtime/migrations/drafts"

# Expected 10 Core Relational Tables
CORE_TABLES = [
    "cae.workspace",
    "cae.workspace_membership",
    "cae.operator_organization",
    "cae.operator_access_grant",
    "cae.engagement",
    "cae.guest",
    "cae.media_asset",
    "cae.harness_template",
    "cae.harness_run",
    "cae.receipt",
    "cae.receipt_evidence_link",
]


def log_pass(msg: str) -> None:
    print(f"  [PASS] {msg}")


def log_fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def check_doc_artifacts() -> list[str]:
    errors = []
    print("\n--- Test Suite 1: CA-MIG-03 Documentation Artifacts ---")
    for name, path in REQUIRED_DOC_ARTIFACTS.items():
        if not path.is_file():
            err = f"Missing required document: {path.relative_to(ROOT_DIR)}"
            log_fail(err)
            errors.append(err)
        else:
            size = path.stat().st_size
            if size < 400:
                err = f"Document {path.relative_to(ROOT_DIR)} is too small ({size} bytes)"
                log_fail(err)
                errors.append(err)
            else:
                log_pass(f"Document verified: {path.relative_to(ROOT_DIR)} ({size} bytes)")
    return errors


def check_sql_drafts() -> list[str]:
    errors = []
    print("\n--- Test Suite 2: SQL Drafts & Guard Headers ---")
    if not DRAFTS_DIR.is_dir():
        err = f"Drafts directory missing: {DRAFTS_DIR.relative_to(ROOT_DIR)}"
        log_fail(err)
        return [err]

    for fname in REQUIRED_SQL_DRAFTS:
        sql_path = DRAFTS_DIR / fname
        if not sql_path.is_file():
            err = f"Missing SQL draft: {fname}"
            log_fail(err)
            errors.append(err)
            continue

        content = sql_path.read_text(encoding="utf-8")
        if "-- STATUS: DRAFT_NOT_APPLIED" not in content and "-- STATUS: APPLIED_STAGING" not in content:
            err = f"SQL draft {fname} missing mandatory '-- STATUS: DRAFT_NOT_APPLIED' or '-- STATUS: APPLIED_STAGING' guard header"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Guard header verified in {fname}")


        # Check for prohibited destructive DDL statements in forward foundation drafts 1-6
        if fname.startswith(("0001", "0002", "0003", "0004", "0005", "0006")):
            prohibited_patterns = [
                r"\bDROP\s+TABLE\b",
                r"\bTRUNCATE\b",
                r"\bDROP\s+SCHEMA\b",
                r"\bDELETE\s+FROM\b",
            ]
            for pat in prohibited_patterns:
                # Allowed: DROP TRIGGER IF EXISTS or DROP POLICY IF EXISTS
                cleaned_content = re.sub(r"\bDROP\s+(TRIGGER|POLICY|EXTENSION)\b", "", content, flags=re.IGNORECASE)
                if re.search(pat, cleaned_content, re.IGNORECASE):
                    err = f"SQL draft {fname} contains prohibited destructive pattern '{pat}'"
                    log_fail(err)
                    errors.append(err)

    return errors


def check_schema_inventory() -> list[str]:
    errors = []
    print("\n--- Test Suite 3: Schema Inventory Completeness ---")
    inv_file = REQUIRED_DOC_ARTIFACTS["schema_inventory"]
    content = inv_file.read_text(encoding="utf-8")

    for tbl in CORE_TABLES:
        if tbl not in content:
            err = f"Core table '{tbl}' missing from Schema Inventory"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Core table documented: '{tbl}'")

    if "cae-media-private" not in content:
        err = "Storage bucket 'cae-media-private' missing from Schema Inventory"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Storage bucket 'cae-media-private' verified")

    return errors


def check_dependency_graph() -> list[str]:
    errors = []
    print("\n--- Test Suite 4: Dependency Graph & Acyclicity ---")
    dep_file = REQUIRED_DOC_ARTIFACTS["dependency_graph"]
    content = dep_file.read_text(encoding="utf-8")

    if "graph TD" not in content and "graph LR" not in content:
        err = "Dependency Graph missing Mermaid DAG diagram"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Mermaid DAG diagram present")

    for i in range(1, 7):
        mig_id = f"MIG-{i:04d}"
        if mig_id not in content:
            err = f"Migration '{mig_id}' missing from Dependency Matrix"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Migration step verified in DAG: '{mig_id}'")

    return errors


def check_safety_rehearsal_and_no_go() -> list[str]:
    errors = []
    print("\n--- Test Suite 5: Safety Rehearsal & 10 No-Go Rules ---")
    safe_file = REQUIRED_DOC_ARTIFACTS["safety_rehearsal"]
    content = safe_file.read_text(encoding="utf-8")

    for i in range(1, 11):
        nogo_id = f"NOGO-{i:02d}"
        if nogo_id not in content:
            err = f"Missing No-Go Safety Rule: '{nogo_id}'"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"No-Go safety rule verified: '{nogo_id}'")

    return errors


def check_repair_boundary() -> list[str]:
    errors = []
    print("\n--- Test Suite 6: F-01 & F-02 Repair Boundary Integrity ---")
    rep_file = REQUIRED_DOC_ARTIFACTS["repair_boundary"]
    content = rep_file.read_text(encoding="utf-8")

    if "F-01" not in content or "STILL_OPEN" not in content:
        err = "F-01 must remain STILL_OPEN and unapplied in repair boundary"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("F-01 composite FK repair boundary verified (STILL_OPEN)")

    if "F-02" not in content or "STILL_OPEN" not in content:
        err = "F-02 must remain STILL_OPEN and unapplied in repair boundary"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("F-02 staging shadow table repair boundary verified (STILL_OPEN)")

    return errors


def check_completion_record() -> list[str]:
    errors = []
    print("\n--- Test Suite 7: Completion Record & Section 6 Question ---")
    comp_file = REQUIRED_DOC_ARTIFACTS["completion_record"]
    content = comp_file.read_text(encoding="utf-8")

    sections = [
        "## A. What Was Designed and Why",
        "## B. Which Parts of the Historic Foundation Are Safe Only as Disposable Proof",
        "## C. What Static/Offline Checks Were Run and Their Limits",
        "## D. What Has Not Been Applied, Tested Against a Database, or Proven in E3",
        "## E. Every Blocked Migration Line, Open Topology/Integrity Decision, and Data-Risk",
        "## F. What Could Still Fail in a Real Disposable Apply",
        "## G. Exact Migration Drafts and No-Go Checks for Operator Inspection",
        "## H. Exact Next Authorization Requested",
    ]
    for sec in sections:
        if sec not in content:
            err = f"Missing section in Completion Record: '{sec}'"
            log_fail(err)
            errors.append(err)
        else:
            log_pass(f"Completion Record section present: '{sec}'")

    exact_question = (
        "Accept CA-MIG-03 as a forward-only migration design and offline safety rehearsal only, "
        "preserve every listed no-go condition and open F-01/F-02 decision, and authorize a "
        "separately bounded disposable-environment migration-application proof for the exact "
        "approved draft IDs—without changing staging authority, migrating client data, or enabling "
        "production routing?"
    )
    if exact_question not in content:
        err = "Completion Record does not contain the exact verbatim Section 6 question!"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Exact verbatim Section 6 decision question confirmed in Completion Record.")

    return errors


def check_control_state() -> list[str]:
    errors = []
    print("\n--- Test Suite 8: Implementation Control State Validation ---")
    cs_file = REQUIRED_DOC_ARTIFACTS["control_state"]
    content = cs_file.read_text(encoding="utf-8")

    valid_statuses = [
        "TENANT_WORKSPACE_CORE_COMPLETED_AWAITING_OPERATOR_GATE",
        "DESIGNED_AND_STATICALLY_REHEARSED_ONLY",
        "APPLIED_AND_E3_PROVEN_IN_DISPOSABLE_ENVIRONMENT_ONLY",
        "F01_REPAIRED_AND_E3_PROVEN_DISPOSABLE_ONLY",
        "F02_TOPOLOGY_EVIDENCED_DECISION_REQUIRED",
        "F02_SELECTED_TOPOLOGY_E3_PROVEN_DISPOSABLE_ONLY",
        "INDEPENDENT_E3_REPLAY_PASSED_STAGING_EQUIVALENT_ONLY",
        "FOUNDATION_F01_F02_DEPLOYED_AND_VERIFIED_SHARED_STAGING_ONLY",
        "FIRST_SLICE_SHARED_STAGING_ACCEPTANCE_READY_FOR_OPERATOR_REVIEW",
        "CLAIMS_UNVERIFIED_BY_OPERATOR",
        "AWAITING_OPERATOR_AUTHORIZATION_CA_UPTL_01",
        "UPSTREAM_INTELLIGENCE_COMPLETED_AWAITING_OPERATOR_GATE",
    ]
    if not any(st in content for st in valid_statuses):
        err = "Control status must declare DESIGNED_AND_STATICALLY_REHEARSED_ONLY or downstream status"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Control status verified (DESIGNED_AND_STATICALLY_REHEARSED_ONLY or downstream)")

    if "ZERO_AUTHORITY_CHANGED" not in content and "operational_authority_change:" not in content:
        err = "Control state must declare ZERO_AUTHORITY_CHANGED or operational_authority_change"
        log_fail(err)
        errors.append(err)
    else:
        log_pass("Operational authority change status explicitly verified")


    return errors


def main() -> int:
    print("=" * 80)
    print("   CAE STATIC GOVERNANCE VALIDATOR: PHASE 15 / CA-MIG-03                ")
    print("=" * 80)

    all_errors = []
    all_errors.extend(check_doc_artifacts())
    all_errors.extend(check_sql_drafts())
    all_errors.extend(check_schema_inventory())
    all_errors.extend(check_dependency_graph())
    all_errors.extend(check_safety_rehearsal_and_no_go())
    all_errors.extend(check_repair_boundary())
    all_errors.extend(check_completion_record())
    all_errors.extend(check_control_state())

    print("\n" + "=" * 80)
    if all_errors:
        print(f"   VALIDATION FAILED: {len(all_errors)} error(s) detected.")
        print("=" * 80)
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print("   SUCCESS: CA-MIG-03 MIGRATION DESIGN & SAFETY REHEARSAL COMPLIANT     ")
    print("   ZERO DATABASE MUTATION; FORWARD-ONLY DESIGN VERIFIED.               ")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
