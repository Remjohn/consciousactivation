"""
test_operator_selection_actions.py
----------------------------------
Tests execution of operator actions (SELECT, REJECT, MODIFY) and session state tracking.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "operator-intelligence" / "src"))

from cae_operator_intelligence.domain import OperatorActionType
from cae_operator_intelligence.manager import OperatorSelectionManager
from cae_operator_intelligence.verifier import OperatorSelectionVerifier


def test_operator_select_and_verify():
    session = OperatorSelectionManager.create_session(
        workspace_id="ws-client-99",
        operator_id="OP-LEAD-01",
    )

    evidence_links = [
        {"segment_id": "SEG-001", "verbatim_text": "We built replication.", "text_sha256": "hash123"}
    ]

    snapshot = OperatorSelectionManager.select_candidate(
        session=session,
        candidate_id="CND-001",
        title="Building Database Replication",
        hook_statement="Why traditional failover falls short in distributed clusters.",
        priority_rank=8,
        evidence_links=evidence_links,
        rationale="Strong technical authority and concrete lived experience.",
    )

    assert len(session.receipts) == 1
    assert len(session.approved_snapshots) == 1

    verified_snapshot = OperatorSelectionVerifier.verify_candidate_approval(
        session=session,
        candidate_id="CND-001",
    )
    assert verified_snapshot.candidate_id == snapshot.candidate_id


def test_operator_reject_candidate():
    session = OperatorSelectionManager.create_session(
        workspace_id="ws-client-99",
        operator_id="OP-LEAD-01",
    )

    receipt = OperatorSelectionManager.reject_candidate(
        session=session,
        candidate_id="CND-002",
        rationale="Too generic and reads like marketing PR rather than vulnerable insight.",
        taste_delta="Model scored 0.78, but operator rejects due to lack of authentic tension.",
    )

    assert receipt.action_type == OperatorActionType.REJECT
    assert len(session.approved_snapshots) == 0
    assert len(session.receipts) == 1
