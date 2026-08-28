"""
verifier.py
-----------
Verification logic for human-in-the-loop operator selection and evidence immutability (CAE-M09).
"""

from __future__ import annotations

from .domain import (
    OperatorActionType,
    OperatorSelectionSession,
    SelectedCandidateSnapshot,
)
from .errors import (
    SilentSelectionViolationError,
    UnapprovedExecutionError,
)


class OperatorSelectionVerifier:
    """Enforces human-in-the-loop selection gates and verifies audit integrity."""

    @classmethod
    def verify_candidate_approval(
        cls,
        session: OperatorSelectionSession,
        candidate_id: str,
    ) -> SelectedCandidateSnapshot:
        """Verifies that a candidate was explicitly approved by the human operator."""
        # Find matching SELECT receipt
        select_receipts = [
            r for r in session.receipts
            if r.candidate_id == candidate_id and r.action_type == OperatorActionType.SELECT
        ]

        if not select_receipts:
            raise UnapprovedExecutionError(
                f"Candidate '{candidate_id}' cannot proceed to production: no explicit Operator SELECT receipt found."
            )

        matching_snapshots = [
            s for s in session.approved_snapshots
            if s.candidate_id == candidate_id
        ]

        if not matching_snapshots:
            raise SilentSelectionViolationError(
                f"Candidate '{candidate_id}' has a receipt but no verified SelectedCandidateSnapshot in session."
            )

        return matching_snapshots[0]
