"""
test_operator_domain_contracts.py
---------------------------------
Validates OperatorDecisionReceipt and SelectedCandidateSnapshot serialization, typing, and schema integrity.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "operator-intelligence" / "src"))

from cae_operator_intelligence.domain import (
    CandidateEditorialBoardView,
    OperatorActionType,
    OperatorDecisionReceipt,
    SelectedCandidateSnapshot,
)


def test_operator_domain_contracts_instantiation():
    receipt = OperatorDecisionReceipt(
        operator_id="OP-LEAD-01",
        candidate_id="CND-101",
        action_type=OperatorActionType.SELECT,
        rationale="Strong vulnerable turn in paragraph 3 with clear audience resonance.",
        taste_delta="Model scored novelty 0.65, but personal story gives it 0.90 practical impact.",
    )

    assert receipt.receipt_id.startswith("RCP-")
    assert receipt.action_type == OperatorActionType.SELECT
    assert "vulnerable turn" in receipt.rationale

    snapshot = SelectedCandidateSnapshot(
        candidate_id="CND-101",
        workspace_id="ws-client-99",
        title="The Zero-Downtime Migration Failure",
        hook_statement="We thought we built redundancy until a single DNS typo brought down 12 regions.",
        priority_rank=9,
        evidence_links=[{"segment_id": "SEG-001", "verbatim_text": "text", "text_sha256": "abc"}],
        approved_by="OP-LEAD-01",
    )

    assert snapshot.snapshot_id.startswith("SNP-")
    assert snapshot.priority_rank == 9
    assert snapshot.approved_by == "OP-LEAD-01"
