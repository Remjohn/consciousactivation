"""
Pure offline structural and governance unit tests for Phase 16 / CA-APPLY-04.

Validates:
1. All CA-APPLY-04 documentation artifacts exist and are non-empty.
2. GuardedMigrationRunner admission, predecessor, and static guard checks pass.
3. Automated proof runner executes all 11 adversarial countertests (CT-01 to CT-11).
4. Completion record contains required sections A through H and exact Section 6 decision question.
5. Implementation Control State correctly records APPLIED_AND_E3_PROVEN_IN_DISPOSABLE_ENVIRONMENT_ONLY.
"""

from __future__ import annotations

from pathlib import Path
import pytest

from ca_runtime.migration_runner import (
    APPROVED_DRAFTS,
    GuardedMigrationRunner,
    IncompatibleTopologyError,
    MigrationAdmissionError,
    MigrationDestructiveStatementError,
    MigrationPredecessorError,
    TargetEnvironmentAdmission,
)
from scripts.cae.audit.verify_ca_apply_04 import (
    DOCS_DIR,
    EXPECTED_SECTION_6_QUESTION,
    REQUIRED_DOCUMENTS,
    verify_admission_record,
    verify_completion_record,
    verify_control_state,
    verify_countertest_coverage,
    verify_documents,
    verify_failure_recovery_and_teardown,
    verify_runner_and_proof_script,
)
from scripts.cae.implementation.run_disposable_migration_proof import (
    test_ct01_wrong_target_rejection as ct01,
    test_ct02_altered_draft_checksum_rejection as ct02,
    test_ct03_incompatible_topology_rejection as ct03,
    test_ct04_destructive_statement_rejection as ct04,
    test_ct05_predecessor_ordering_enforcement as ct05,
    test_ct06_idempotent_no_op_re_run as ct06,
    test_ct07_rls_unscoped_denial as ct07,
    test_ct08_cross_workspace_parent_rejection as ct08,
    test_ct09_receipt_immutability_trigger as ct09,
    test_ct10_failure_rollback_and_history_honesty as ct10,
    test_ct11_scoped_synthetic_teardown as ct11,
)


def test_ca_apply_04_documentation_suite():
    assert verify_documents() is True
    assert verify_runner_and_proof_script() is True
    assert verify_admission_record() is True
    assert verify_countertest_coverage() is True
    assert verify_failure_recovery_and_teardown() is True
    assert verify_completion_record() is True
    assert verify_control_state() is True


def test_ca_apply_04_11_countertests_execution():
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


def test_ca_apply_04_verbatim_question():
    comp_file = DOCS_DIR / "CAE_APPLY_04_COMPLETION_RECORD.md"
    content = comp_file.read_text(encoding="utf-8")
    clean_content = " ".join(content.split())
    clean_expected = " ".join(EXPECTED_SECTION_6_QUESTION.split())
    assert clean_expected in clean_content
