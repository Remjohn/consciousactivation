"""
verifier.py
-----------
Verification and gating logic for Content Candidates (CAE-M07).
"""

from __future__ import annotations

from .domain import (
    CandidateType,
    ContentCandidate,
    NarrativeCompleteness,
    ProductionStatus,
)
from .errors import (
    MissingStoryTurnError,
    NarrativeIncompletenessError,
    PrematureProductionApprovalError,
    UngroundedCandidateError,
)


class ContentCandidateVerifier:
    """Enforces constitutional validity on ContentCandidates."""

    TURN_INDICATORS = [
        "until", "but", "however", "then suddenly", "realized", "shattered", "turned out",
        "the truth was", "what changed", "in reality", "pivoted", "breakthrough", "catastrophe"
    ]

    @classmethod
    def verify_candidate(cls, candidate: ContentCandidate) -> bool:
        """Validates a ContentCandidate against constitutional rules."""
        # 1. Reject Premature Production Approval
        if candidate.production_status == ProductionStatus.APPROVED_FOR_PRODUCTION:
            raise PrematureProductionApprovalError(
                f"Candidate '{candidate.candidate_id}' violates constitutional boundary: "
                f"production_status cannot be APPROVED_FOR_PRODUCTION in M07."
            )

        # 2. Check Grounding Lineage
        if not candidate.evidence_links:
            raise UngroundedCandidateError(
                f"Candidate '{candidate.candidate_id}' has empty evidence lineage."
            )

        # 3. Check Standalone Completeness
        if candidate.narrative_completeness == NarrativeCompleteness.INCOMPLETE:
            raise NarrativeIncompletenessError(
                f"Candidate '{candidate.candidate_id}' is marked INCOMPLETE."
            )

        # 4. Check Story Turn
        if candidate.candidate_type == CandidateType.STORY_CANDIDATE:
            combined_text = " ".join(link.verbatim_text.lower() for link in candidate.evidence_links)
            if not any(indicator in combined_text for indicator in cls.TURN_INDICATORS):
                raise MissingStoryTurnError(
                    f"Story candidate '{candidate.candidate_id}' lacks a narrative turn in its evidence."
                )

        return True
