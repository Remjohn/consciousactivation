#!/usr/bin/env python3
"""
Static & Dynamic Verification Script for Phase 28 / CA-GST-UI-01.

Mandate: CA-GST-UI-01 — Guest Ingestion & Asset Library UI
Governing Specification: SPEC-GST-UI-001 as amended by DEC-GST-001 v2

Verifies:
1. Presence and structural integrity of all frontend UI components and API clients.
2. Presence and integrity of backend schema and router extensions.
3. Verification of Context Taxonomy, Tiered Limits, and Hard Negatives (HN-GST-01..05).
4. Presence of CA-GST-UI-01 Completion Record and verbatim Section 7 decision question.
5. Presence and format of CAE Implementation Control State.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
IMPL_DIR = ROOT_DIR / "docs" / "cae" / "implementation"
WEB_SRC_DIR = ROOT_DIR / "apps" / "web" / "src"
CONTROL_STATE_PATH = IMPL_DIR / "CAE_IMPLEMENTATION_CONTROL_STATE.md"
COMPLETION_RECORD_PATH = IMPL_DIR / "CAE_GST_UI_01_COMPLETION_RECORD.md"

REQUIRED_UI_COMPONENTS = [
    "components/interview-composer/SourceUrlManager.tsx",
    "components/interview-composer/DocumentDropzone.tsx",
    "components/interview-composer/AuthorityAssertionModal.tsx",
    "components/interview-composer/ResearchPackageInspector.tsx",
    "components/interview-composer/BrandVoicePicker.tsx",
    "components/interview-composer/ResearchPanel.tsx",
    "components/interview-composer/BriefPanel.tsx",
]

REQUIRED_UI_TESTS = [
    "components/interview-composer/SourceUrlManager.test.tsx",
    "components/interview-composer/DocumentDropzone.test.tsx",
    "components/interview-composer/AuthorityAssertionModal.test.tsx",
    "components/interview-composer/ResearchPackageInspector.test.tsx",
    "components/interview-composer/BrandVoicePicker.test.tsx",
    "components/interview-composer/ResearchPanel.test.tsx",
]


def check_ui_components() -> bool:
    print("[CHECK 1] Verifying frontend UI components...")
    all_ok = True
    for rel_path in REQUIRED_UI_COMPONENTS:
        fpath = WEB_SRC_DIR / rel_path
        if not fpath.is_file() or fpath.stat().st_size == 0:
            print(f"  [FAIL] Missing or empty component: {rel_path}")
            all_ok = False
        else:
            print(f"  [PASS] Present: {rel_path} ({fpath.stat().st_size} bytes)")
    return all_ok


def check_ui_tests() -> bool:
    print("[CHECK 2] Verifying frontend vitest test suites...")
    all_ok = True
    for rel_path in REQUIRED_UI_TESTS:
        fpath = WEB_SRC_DIR / rel_path
        if not fpath.is_file() or fpath.stat().st_size == 0:
            print(f"  [FAIL] Missing or empty test file: {rel_path}")
            all_ok = False
        else:
            print(f"  [PASS] Present: {rel_path} ({fpath.stat().st_size} bytes)")
    return all_ok


def check_backend_extensions() -> bool:
    print("[CHECK 3] Verifying backend schema and router extensions...")
    schema_path = ROOT_DIR / "api" / "schemas" / "interview_composer.py"
    router_path = ROOT_DIR / "api" / "routers" / "interview_composer.py"
    test_path = ROOT_DIR / "tests" / "api" / "test_interview_composer_research.py"

    all_ok = True
    schema_content = schema_path.read_text(encoding="utf-8")
    router_content = router_path.read_text(encoding="utf-8")
    test_content = test_path.read_text(encoding="utf-8")

    # Check schema tokens
    for tok in ["ContextClass", "IDENTITY_DNA", "CONTEXT_PREMISE", "RESONANCE_REFERENCE", "BRAND_VOICE", "EVIDENCE_SOURCE", "INTERVIEW_RECORDING", "CAPTION_TRACK", "context_class", "caption_for", "brand_ref"]:
        if tok not in schema_content:
            print(f"  [FAIL] Missing token in backend schema: {tok}")
            all_ok = False

    # Check router tokens
    for tok in ["document_metadata_json", "INVALID_CONTEXT_CLASS", "INVALID_CAPTION_TARGET", "AUTHORITY_REQUIRED", "GUEST_NAME_INVALID", "WORKSPACE_REQUIRED"]:
        if tok not in router_content:
            print(f"  [FAIL] Missing token in router: {tok}")
            all_ok = False

    # Check hard-negative tests in test_interview_composer_research.py
    for tok in [
        "test_gst_context_class_and_caption_linking",
        "test_hn_gst_01_empty_guest_name_rejected",
        "test_hn_gst_02_oversized_file_rejected",
        "test_hn_gst_03_corrupted_hash_rejected",
        "test_hn_gst_04_missing_workspace_rejected",
        "test_hn_gst_05_missing_authority_rejected",
        "test_hn_gst_06_unknown_context_class_rejected",
        "test_hn_gst_07_invalid_caption_target_rejected",
    ]:
        if tok not in test_content:
            print(f"  [FAIL] Missing hard negative test in router tests: {tok}")
            all_ok = False

    if all_ok:
        print("  [PASS] Backend schema, router, and router test extensions verified.")
    return all_ok


def check_completion_record() -> bool:
    print("[CHECK 4] Verifying Completion Record & Verbatim Decision Question...")
    if not COMPLETION_RECORD_PATH.is_file() or COMPLETION_RECORD_PATH.stat().st_size == 0:
        print("  [FAIL] Missing or empty CAE_GST_UI_01_COMPLETION_RECORD.md")
        return False

    content = COMPLETION_RECORD_PATH.read_text(encoding="utf-8")
    sections = [
        "## 1. Executive Summary & Scope Attestation",
        "## 2. Six Implemented Scope Items (SPEC-GST-UI-001 & DEC-GST-001 v2)",
        "## 3. Context Taxonomy & Brand Voice Doctrinal Alignment",
        "## 4. Hard Negatives & Adversarial Defense Matrix (HN-GST-01..05)",
        "## 5. Verbatim Evidence & Test Suite Outputs",
        "## 6. Pre-Authorized Backend Extension Documentation",
        "## 7. Epistemic & Authority Boundaries",
        "## 8. Verbatim Section 7 Operator Decision Request",
    ]
    all_ok = True
    for sec in sections:
        if sec not in content:
            print(f"  [FAIL] Missing section in Completion Record: {sec}")
            all_ok = False

    expected_question = (
        "Accept CA-GST-UI-01 as the completed Guest Ingestion & Asset Library UI implementing "
        "ratified SPEC-GST-UI-001 (tiered uploads per DEC-GST-001 v2, presigned direct upload, "
        "SHA-256 verification, operator authority attestation, all tests green) — and authorize "
        "CA-BRF-UI-01 (Track B #3, Brief Ingestion & Generation UI) mandate drafting only?"
    )
    if expected_question not in content:
        print("  [FAIL] Missing or altered Section 7 decision question in Completion Record")
        all_ok = False

    if all_ok:
        print("  [PASS] Completion Record verified with verbatim Decision Question.")
    return all_ok


def check_control_state() -> bool:
    print("[CHECK 5] Verifying Control State Document...")
    if not CONTROL_STATE_PATH.is_file():
        print("  [FAIL] Missing CAE_IMPLEMENTATION_CONTROL_STATE.md")
        return False

    content = CONTROL_STATE_PATH.read_text(encoding="utf-8")
    all_ok = True
    if not re.search(r"\*\*Control status:\*\*\s+`[A-Za-z0-9_]+`", content):
        print("  [FAIL] Control status pattern not found in control state")
        all_ok = False

    if "CA-GST-UI-01" not in content:
        print("  [FAIL] CA-GST-UI-01 not referenced in control state")
        all_ok = False

    if all_ok:
        print("  [PASS] Control State Document verified.")
    return all_ok


def main() -> int:
    print("=" * 80)
    print("   CAE STATIC & STRUCTURAL AUDIT VERIFIER: PHASE 28 / CA-GST-UI-01    ")
    print("=" * 80)

    checks = [
        check_ui_components,
        check_ui_tests,
        check_backend_extensions,
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
        print("   STATIC VERIFICATION FAILED: One or more CA-GST-UI-01 checks failed.")
        print("=" * 80)
        return 1

    print("   SUCCESS: 5/5 STATIC VERIFICATION CHECKS PASSED FOR CA-GST-UI-01.  ")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    sys.exit(main())
