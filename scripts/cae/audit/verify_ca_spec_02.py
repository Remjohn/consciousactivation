#!/usr/bin/env python3
"""
verify_ca_spec_02.py — Verification tool for Mandate CA-SPEC-02.
Audits the presence, structural integrity, 14-section schema conformance,
code anchor validity, hard negative count, and ledger coverage for all
six CA-SPEC-02 implementation specifications.
"""

import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SPECS_DIR = REPO_ROOT / "docs" / "cae" / "specs" / "current"
LEDGER_FILE = REPO_ROOT / "docs" / "cae" / "implementation" / "CAE_APP_COMPLETION_LEDGER.md"
PRD_FILE = REPO_ROOT / "docs" / "PRD" / "CURRENT.md"

REQUIRED_SPECS = [
    "SPEC-TWC-UI-001.md",
    "SPEC-GST-UI-001.md",
    "SPEC-BRF-001.md",
    "SPEC-STU-001.md",
    "SPEC-CMP-002.md",
    "SPEC-HAR-001.md",
]

REQUIRED_SECTIONS = [
    r"## 1\. Files and Evidence Read",
    r"## 2\. Architectural Role and Boundaries",
    r"## 3\. Brownfield Reality & Component Disposition",
    r"## 4\. Functional Requirement Traceability",
    r"## 5\. Canonical Object & Schema Contract",
    r"## 6\. API Contracts & Endpoint Shapes",
    r"## 7\. State Machines & Transition Grammar",
    r"## 8\. Error Taxonomy & Hard Failures",
    r"## 9\. Implementation File Allowlist & Scope Boundary",
    r"## 10\. Test Plan with Hard Negatives",
    r"## 11\. Evidence & Verification Protocol",
    r"## 12\. Risk Register & Failure Modes",
    r"## 13\. Rollback & Backout Procedure",
    r"## 14\. Open Decisions & Human Review Prompts",
]


def audit_prd_reconciliation() -> dict:
    if not PRD_FILE.exists():
        return {"ok": False, "error": f"PRD file missing: {PRD_FILE}"}
    content = PRD_FILE.read_text(encoding="utf-8")
    has_changelog = "2026-08-26 (Mandate Phase 26: CA-SPEC-02)" in content
    has_tenancy_update = "MC-CAE-WS-001/MEM-001/OPR-001 POSTGRES_AUTHORITATIVE_STAGING_ONLY" in content
    has_model_engine = "ModelReasoningEngine" in content
    has_debt_ref = "KNOWN_LEGACY_TEST_DEBT.md" in content

    ok = has_changelog and has_tenancy_update and has_model_engine and has_debt_ref
    return {
        "ok": ok,
        "has_changelog": has_changelog,
        "has_tenancy_update": has_tenancy_update,
        "has_model_engine": has_model_engine,
        "has_debt_ref": has_debt_ref,
    }


def audit_completion_ledger() -> dict:
    if not LEDGER_FILE.exists():
        return {"ok": False, "error": f"Completion ledger missing: {LEDGER_FILE}"}
    content = LEDGER_FILE.read_text(encoding="utf-8")
    
    # Check that all 6 specs are cross-referenced in the ledger
    missing_spec_refs = [spec for spec in REQUIRED_SPECS if spec not in content]
    # Check for capabilities
    has_caps = "CAP-TWC-01" in content and "CAP-HAR-02" in content
    
    ok = (len(missing_spec_refs) == 0) and has_caps
    return {
        "ok": ok,
        "missing_spec_refs": missing_spec_refs,
        "has_capabilities": has_caps,
    }


def audit_spec_file(spec_filename: str) -> dict:
    spec_path = SPECS_DIR / spec_filename
    if not spec_path.exists():
        return {"filename": spec_filename, "ok": False, "error": "File does not exist"}

    content = spec_path.read_text(encoding="utf-8")
    
    # Verify 14 sections
    missing_sections = []
    for idx, pattern in enumerate(REQUIRED_SECTIONS, 1):
        if not re.search(pattern, content):
            missing_sections.append(f"Section {idx} ({pattern})")

    # Verify Hard Negatives count (minimum 5)
    hn_matches = re.findall(r"HN-[A-Z]+-\d+", content)
    unique_hns = list(set(hn_matches))
    hn_count = len(unique_hns)

    # Verify OPEN_DECISION marker in section 14
    has_open_decision = "OPEN_DECISION" in content

    # Verify code anchors in section 1
    has_code_anchors = bool(
        re.search(r"(\.py|\.ts|\.tsx|\.json):\d+", content) or 
        re.search(r"(\.py|\.ts|\.tsx|\.json)[`]?\s*\((lines|line)?\s*\d+", content)
    )

    ok = (len(missing_sections) == 0) and (hn_count >= 5) and has_open_decision and has_code_anchors

    return {
        "filename": spec_filename,
        "ok": ok,
        "section_count": 14 - len(missing_sections),
        "missing_sections": missing_sections,
        "hard_negatives_count": hn_count,
        "hard_negatives": unique_hns,
        "has_open_decision": has_open_decision,
        "has_code_anchors": has_code_anchors,
    }


def run_full_audit():
    print("=" * 70)
    print("CA-SPEC-02 IMPLEMENTATION SPECIFICATION & PRD AUDIT")
    print(f"Timestamp: 2026-08-26 | Repo Root: {REPO_ROOT}")
    print("=" * 70)

    # 1. PRD Audit
    prd_res = audit_prd_reconciliation()
    print(f"\n[1/3] PRD Reconciliation (CURRENT.md): {'PASS' if prd_res['ok'] else 'FAIL'}")
    print(f"  - 2026-08-26 Changelog Entry: {'YES' if prd_res['has_changelog'] else 'NO'}")
    print(f"  - Tenancy Staging Update:    {'YES' if prd_res['has_tenancy_update'] else 'NO'}")
    print(f"  - ModelReasoningEngine Ref:  {'YES' if prd_res['has_model_engine'] else 'NO'}")
    print(f"  - Legacy Debt Reference:     {'YES' if prd_res['has_debt_ref'] else 'NO'}")

    # 2. Completion Ledger Audit
    ledger_res = audit_completion_ledger()
    print(f"\n[2/3] App-Completion Ledger: {'PASS' if ledger_res['ok'] else 'FAIL'}")
    print(f"  - All 6 Specs Cross-Referenced: {'YES' if not ledger_res.get('missing_spec_refs') else 'NO'}")
    print(f"  - Capabilities Matrix Included: {'YES' if ledger_res.get('has_capabilities') else 'NO'}")

    # 3. Specs Audit
    print("\n[3/3] 6-Spec Conformance Matrix (14-Section Depth, >=5 Hard Negatives):")
    all_specs_ok = True
    spec_results = []
    for spec_name in REQUIRED_SPECS:
        res = audit_spec_file(spec_name)
        spec_results.append(res)
        status = "PASS" if res["ok"] else "FAIL"
        if not res["ok"]:
            all_specs_ok = False
        print(f"  - {spec_name:<20} : {status} (Sections: {res.get('section_count', 0)}/14, Hard Negatives: {res.get('hard_negatives_count', 0)}, Open Decisions: {'YES' if res.get('has_open_decision') else 'NO'})")
        if not res["ok"] and res.get("missing_sections"):
            for ms in res["missing_sections"]:
                print(f"      * Missing: {ms}")

    overall_ok = prd_res["ok"] and ledger_res["ok"] and all_specs_ok
    print("\n" + "=" * 70)
    print(f"OVERALL MANDATE CA-SPEC-02 AUDIT RESULT: {'PASS (100%)' if overall_ok else 'FAIL'}")
    print("=" * 70)

    if not overall_ok:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    run_full_audit()
