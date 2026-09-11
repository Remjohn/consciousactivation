"""
Pure offline structural and governance unit tests for Phase 17 / CA-INT-05.

Validates:
1. All CA-INT-05 documentation artifacts exist and are non-empty.
2. F-01 composite FK repair draft (MIG-0007) is well-formed with RESTRICT.
3. Automated proof runner executes all 11 adversarial countertests (F01-CT-01 to CT-11).
4. Completion record contains required sections A through G and exact Section 6 decision question.
5. Implementation Control State correctly records F01_REPAIRED_AND_E3_PROVEN_DISPOSABLE_ONLY.
"""

from __future__ import annotations

from pathlib import Path
import pytest

from scripts.cae.audit.verify_ca_int_05 import (
    DOCS_DIR,
    EXPECTED_SECTION_6_QUESTION,
    REQUIRED_DOCUMENTS,
    verify_admission_record,
    verify_completion_record,
    verify_control_state,
    verify_countertest_coverage,
    verify_documents,
    verify_draft_and_proof_script,
    verify_recovery_and_teardown,
)
from scripts.cae.implementation.run_f01_repair_proof import (
    test_f01_ct01_cross_workspace_link_constraint_rejection as ct01,
    test_f01_ct02_valid_local_link_success as ct02,
    test_f01_ct03_parent_candidate_key_inspection as ct03,
    test_f01_ct04_composite_child_fk_inspection as ct04,
    test_f01_ct05_preflight_cross_workspace_data_rejection as ct05,
    test_f01_ct06_preflight_missing_parent_key_rejection as ct06,
    test_f01_ct07_append_only_trigger_retention as ct07,
    test_f01_ct08_rls_isolation_retention as ct08,
    test_f01_ct09_altered_draft_and_predecessor_rejection as ct09,
    test_f01_ct10_atomic_rollback_and_honest_history as ct10,
    test_f01_ct11_scoped_teardown_verification as ct11,
)


def test_ca_int_05_documentation_suite():
    assert verify_documents() is True
    assert verify_draft_and_proof_script() is True
    assert verify_admission_record() is True
    assert verify_countertest_coverage() is True
    assert verify_recovery_and_teardown() is True
    assert verify_completion_record() is True
    assert verify_control_state() is True


def test_ca_int_05_11_countertests_execution():
    assert ct01() is True
    assert ct02() is True
    assert ct03() is True
    assert ct04() is True
    assert ct05() is True
    assert ct06() is True
    assert ct07() is True
    assert ct08() is True
    assert ct09() is True
    assert ct10() is True
    assert ct11() is True


def test_ca_int_05_verbatim_question():
    comp_file = DOCS_DIR / "CAE_INT_05_COMPLETION_RECORD.md"
    content = comp_file.read_text(encoding="utf-8")
    clean_content = " ".join(content.split())
    clean_expected = " ".join(EXPECTED_SECTION_6_QUESTION.split())
    assert clean_expected in clean_content
