"""
test_operator_adversarial_cases.py
----------------------------------
Adversarial tests for silent auto-selection prevention, missing rationale rejection, and unapproved execution blocks.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "operator-intelligence" / "src"))

import pytest

from cae_operator_intelligence.errors import (
    EvidenceMutationViolationError,
    MissingRationaleError,
    UnapprovedExecutionError,
)
from cae_operator_intelligence.manager import OperatorSelectionManager
from cae_operator_intelligence.verifier import OperatorSelectionVerifier


def test_unapproved_candidate_cannot_execute():
    session = OperatorSelectionManager.create_session(
        workspace_id="ws-client-99",
        operator_id="OP-LEAD-01",
    )

    # Candidate was evaluated with 0.99 score in M08 but Operator has NOT selected it
    with pytest.raises(UnapprovedExecutionError, match="no explicit Operator SELECT receipt found"):
        OperatorSelectionVerifier.verify_candidate_approval(
            session=session,
            candidate_id="CND-TOP-SCORING-BUT-UNSELECTED",
        )


def test_selection_without_rationale_rejected():
    session = OperatorSelectionManager.create_session(
        workspace_id="ws-client-99",
        operator_id="OP-LEAD-01",
    )

    with pytest.raises(MissingRationaleError, match="requires an explanatory rationale"):
        OperatorSelectionManager.select_candidate(
            session=session,
            candidate_id="CND-001",
            title="Title",
            hook_statement="Hook Statement",
            priority_rank=5,
            evidence_links=[{"segment_id": "SEG-001"}],
            rationale="",  # VIOLATION: Empty rationale
        )


def test_rejection_without_rationale_rejected():
    session = OperatorSelectionManager.create_session(
        workspace_id="ws-client-99",
        operator_id="OP-LEAD-01",
    )

    with pytest.raises(MissingRationaleError, match="requires an explanatory rationale"):
        OperatorSelectionManager.reject_candidate(
            session=session,
            candidate_id="CND-001",
            rationale="   ",  # VIOLATION: Whitespace rationale
        )
