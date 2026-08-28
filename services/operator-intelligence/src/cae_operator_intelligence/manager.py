"""
manager.py
----------
Operator Selection Manager executing typed editorial actions and emitting decision receipts.
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional

from .domain import (
    OperatorActionType,
    OperatorDecisionReceipt,
    OperatorSelectionSession,
    SelectedCandidateSnapshot,
)
from .errors import (
    EvidenceMutationViolationError,
    MissingRationaleError,
)


class OperatorSelectionManager:
    """Manages human operator editorial decisions with full auditability and learning receipt emission."""

    @classmethod
    def create_session(cls, *, workspace_id: str, operator_id: str) -> OperatorSelectionSession:
        return OperatorSelectionSession(workspace_id=workspace_id, operator_id=operator_id)

    @classmethod
    def select_candidate(
        cls,
        session: OperatorSelectionSession,
        *,
        candidate_id: str,
        title: str,
        hook_statement: str,
        priority_rank: int,
        evidence_links: List[Dict[str, Any]],
        rationale: str,
        taste_delta: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> SelectedCandidateSnapshot:
        """Selects a candidate for production, emitting an audit receipt and creating an immutable snapshot."""
        if not rationale or len(rationale.strip()) < 5:
            raise MissingRationaleError("Operator selection requires an explanatory rationale of at least 5 characters.")

        receipt = OperatorDecisionReceipt(
            operator_id=session.operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.SELECT,
            rationale=rationale,
            taste_delta=taste_delta,
        )
        session.receipts.append(receipt)

        snapshot = SelectedCandidateSnapshot(
            candidate_id=candidate_id,
            workspace_id=session.workspace_id,
            title=title,
            hook_statement=hook_statement,
            priority_rank=priority_rank,
            evidence_links=evidence_links,
            approved_by=session.operator_id,
            notes=notes,
        )
        session.approved_snapshots.append(snapshot)
        return snapshot

    @classmethod
    def reject_candidate(
        cls,
        session: OperatorSelectionSession,
        *,
        candidate_id: str,
        rationale: str,
        taste_delta: Optional[str] = None,
    ) -> OperatorDecisionReceipt:
        """Rejects a candidate, recording the rejection as a permanent learning event."""
        if not rationale or len(rationale.strip()) < 5:
            raise MissingRationaleError("Operator rejection requires an explanatory rationale.")

        receipt = OperatorDecisionReceipt(
            operator_id=session.operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.REJECT,
            rationale=rationale,
            taste_delta=taste_delta,
        )
        session.receipts.append(receipt)
        return receipt

    @classmethod
    def modify_framing(
        cls,
        session: OperatorSelectionSession,
        *,
        candidate_id: str,
        new_title: str,
        new_hook: str,
        original_evidence_links: List[Dict[str, Any]],
        modified_evidence_links: List[Dict[str, Any]],
        rationale: str,
    ) -> OperatorDecisionReceipt:
        """Modifies title/hook framing while strictly verifying that evidence text and hashes are unchanged."""
        if not rationale or len(rationale.strip()) < 5:
            raise MissingRationaleError("Operator modification requires an explanatory rationale.")

        # Check evidence immutability
        if len(original_evidence_links) != len(modified_evidence_links):
            raise EvidenceMutationViolationError("Cannot add or remove evidence segments during framing modification.")

        for orig, mod in zip(original_evidence_links, modified_evidence_links):
            if orig["text_sha256"] != mod["text_sha256"] or orig["verbatim_text"] != mod["verbatim_text"]:
                raise EvidenceMutationViolationError(
                    f"Evidence mutation detected: verbatim text or hash was altered for segment '{orig.get('segment_id')}'."
                )

        receipt = OperatorDecisionReceipt(
            operator_id=session.operator_id,
            candidate_id=candidate_id,
            action_type=OperatorActionType.MODIFY,
            rationale=rationale,
            metadata={"new_title": new_title, "new_hook": new_hook},
        )
        session.receipts.append(receipt)
        return receipt
