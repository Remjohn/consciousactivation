"""
verifier.py
-----------
Verification logic for human-in-the-loop operator selection and evidence immutability (CAE-M09).
"""

from __future__ import annotations

from typing import Any, Dict, List

from .domain import (
    OperatorActionType,
    OperatorSelectionSession,
    SelectedCandidateSnapshot,
)
from .errors import (
    CandidateLockedError,
    EvidenceMutationViolationError,
    EvidenceTamperingDetectedError,
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

    @classmethod
    def verify_production_eligibility(
        cls,
        session: OperatorSelectionSession,
        candidate_id: str,
    ) -> SelectedCandidateSnapshot:
        """Enforces downstream gate: verifies candidate is explicitly selected, not rejected, and valid."""
        # Check for explicit rejection
        reject_receipts = [
            r for r in session.receipts
            if r.candidate_id == candidate_id and r.action_type == OperatorActionType.REJECT
        ]
        if reject_receipts:
            raise UnapprovedExecutionError(
                f"Candidate '{candidate_id}' cannot proceed to production: candidate was explicitly REJECTED by operator."
            )

        return cls.verify_candidate_approval(session, candidate_id)

    @classmethod
    def verify_lock_integrity(
        cls,
        session: OperatorSelectionSession,
        candidate_id: str,
        attempted_action: str,
    ) -> None:
        """Ensures that a locked candidate cannot be mutated, re-ranked, or superseded without unlocking."""
        is_locked = any(l.candidate_id == candidate_id for l in session.locked_candidates)
        if is_locked and attempted_action in ("MUTATE", "OVERWRITE", "PRUNE", "RE_RANK"):
            raise CandidateLockedError(
                f"Candidate '{candidate_id}' is LOCKED by operator and protected against attempted '{attempted_action}'."
            )

    @classmethod
    def verify_evidence_immutability(
        cls,
        *,
        original_evidence_links: List[Dict[str, Any]],
        candidate_evidence_links: List[Dict[str, Any]],
    ) -> None:
        """Verifies that all evidence segments maintain identical verbatim text and SHA-256 hashes."""
        if not candidate_evidence_links:
            raise EvidenceTamperingDetectedError("Candidate must contain at least one evidence link.")

        orig_map = {link.get("segment_id"): link for link in original_evidence_links if link.get("segment_id")}

        for cand_link in candidate_evidence_links:
            seg_id = cand_link.get("segment_id")
            if not seg_id or seg_id not in orig_map:
                raise EvidenceTamperingDetectedError(
                    f"Candidate references ungrounded or unknown evidence segment '{seg_id}'."
                )

            orig_link = orig_map[seg_id]
            if orig_link.get("text_sha256") != cand_link.get("text_sha256"):
                raise EvidenceMutationViolationError(
                    f"Evidence SHA-256 mismatch detected for segment '{seg_id}'."
                )
            if orig_link.get("verbatim_text") != cand_link.get("verbatim_text"):
                raise EvidenceMutationViolationError(
                    f"Evidence verbatim text mismatch detected for segment '{seg_id}'."
                )

