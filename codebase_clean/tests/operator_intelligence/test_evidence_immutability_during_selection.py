"""
test_evidence_immutability_during_selection.py
----------------------------------------------
Tests that operator modifications can refine title and hook framing without altering underlying evidence text or hashes.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "operator-intelligence" / "src"))

import pytest

from cae_operator_intelligence.domain import OperatorActionType
from cae_operator_intelligence.errors import EvidenceMutationViolationError
from cae_operator_intelligence.manager import OperatorSelectionManager


def test_valid_framing_modification_preserves_evidence():
    session = OperatorSelectionManager.create_session(
        workspace_id="ws-client-99",
        operator_id="OP-LEAD-01",
    )

    orig_evidence = [
        {"segment_id": "SEG-001", "verbatim_text": "Our database crashed at 3 AM.", "text_sha256": "hash_3am"}
    ]
    mod_evidence = [
        {"segment_id": "SEG-001", "verbatim_text": "Our database crashed at 3 AM.", "text_sha256": "hash_3am"}
    ]

    receipt = OperatorSelectionManager.modify_framing(
        session=session,
        candidate_id="CND-001",
        new_title="Refined Title: Midnight Database Crash",
        new_hook="What happens when your primary replica fails in the dead of night?",
        original_evidence_links=orig_evidence,
        modified_evidence_links=mod_evidence,
        rationale="Sharpened hook to emphasize high stakes.",
    )

    assert receipt.action_type == OperatorActionType.MODIFY
    assert receipt.metadata["new_title"] == "Refined Title: Midnight Database Crash"


def test_tampered_evidence_text_raises_error():
    session = OperatorSelectionManager.create_session(
        workspace_id="ws-client-99",
        operator_id="OP-LEAD-01",
    )

    orig_evidence = [
        {"segment_id": "SEG-001", "verbatim_text": "Our database crashed at 3 AM.", "text_sha256": "hash_3am"}
    ]
    # Tampering with verbatim text
    tampered_evidence = [
        {"segment_id": "SEG-001", "verbatim_text": "Our database ran smoothly all night.", "text_sha256": "hash_smooth"}
    ]

    with pytest.raises(EvidenceMutationViolationError, match="Evidence mutation detected"):
        OperatorSelectionManager.modify_framing(
            session=session,
            candidate_id="CND-001",
            new_title="Tampered Title",
            new_hook="Tampered Hook",
            original_evidence_links=orig_evidence,
            modified_evidence_links=tampered_evidence,
            rationale="Attempting to rewrite evidence history.",
        )
