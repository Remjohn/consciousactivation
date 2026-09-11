"""
verifier.py
-----------
Verification and audit logic for EditorialBoard and candidate scoring (CAE-M08).
"""

from __future__ import annotations

from .domain import EditorialBoard, GateStatus
from .errors import NonCompensableGateFailureError


class EditorialBoardVerifier:
    """Enforces constitutional validity on the EditorialBoard."""

    @classmethod
    def verify_board(cls, board: EditorialBoard) -> bool:
        """Validates an EditorialBoard against constitutional rules."""
        evaluated_ids = {p.candidate_id for p in board.evaluated_candidates}

        # 1. Verify Non-Compensable Gate Enforcement
        for profile in board.evaluated_candidates:
            if profile.gate_status != GateStatus.PASSED and profile.is_eligible_for_board:
                raise NonCompensableGateFailureError(
                    f"Candidate '{profile.candidate_id}' failed gate with status {profile.gate_status} "
                    f"but was incorrectly marked is_eligible_for_board=True."
                )

        # 2. Verify Cluster Lineage Integrity
        for cluster in board.clusters:
            for cand_id in cluster.candidate_ids:
                if cand_id not in evaluated_ids:
                    raise KeyError(
                        f"Cluster '{cluster.cluster_id}' references unknown candidate '{cand_id}'."
                    )

        return True
