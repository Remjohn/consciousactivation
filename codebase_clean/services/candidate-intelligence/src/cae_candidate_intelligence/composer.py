"""
composer.py
-----------
Editorial Candidate Composer turning evidence links into structured ContentCandidate units.
"""

from __future__ import annotations

from typing import List, Optional

from .domain import (
    CandidateEvidenceLink,
    CandidateType,
    ContentCandidate,
    HeritageCMFScore,
    NarrativeCompleteness,
    ProductionStatus,
)
from .errors import (
    MissingStoryTurnError,
    NarrativeIncompletenessError,
    PrematureProductionApprovalError,
    UngroundedCandidateError,
)


class EditorialCandidateComposer:
    """Compiles grounded evidence segments into structured ContentCandidates."""

    TURN_INDICATORS = [
        "until", "but", "however", "then suddenly", "realized", "shattered", "turned out",
        "the truth was", "what changed", "in reality", "pivoted", "breakthrough", "catastrophe"
    ]

    @classmethod
    def compose_candidate(
        cls,
        *,
        workspace_id: str,
        candidate_type: CandidateType,
        title: str,
        hook_statement: str,
        narrative_completeness: NarrativeCompleteness,
        evidence_links: List[CandidateEvidenceLink],
        cmf_score: HeritageCMFScore,
        story_arc: Optional[str] = None,
        tension_ref: Optional[str] = None,
        invariant_ref: Optional[str] = None,
        archetypal_container: Optional[str] = None,
        production_status: ProductionStatus = ProductionStatus.DRAFT_CANDIDATE,
        standalone_context_notes: Optional[str] = None,
    ) -> ContentCandidate:
        """Assembles a ContentCandidate with strict structural gating."""
        # 1. Reject Premature Production Approval
        if production_status == ProductionStatus.APPROVED_FOR_PRODUCTION:
            raise PrematureProductionApprovalError(
                "Cannot mark candidate as APPROVED_FOR_PRODUCTION during candidate formation. "
                "Approval belongs exclusively to Operator selection gates."
            )

        # 2. Check Grounding Lineage
        if not evidence_links:
            raise UngroundedCandidateError(
                f"Candidate '{title}' is completely ungrounded: evidence_links list cannot be empty."
            )

        # 3. Check Standalone Completeness for Incomplete Segments
        if narrative_completeness == NarrativeCompleteness.INCOMPLETE:
            raise NarrativeIncompletenessError(
                f"Candidate '{title}' is marked INCOMPLETE. Candidates must achieve COMPLETE or INTENTIONALLY_OPEN_ENDED status."
            )

        combined_text = " ".join(link.verbatim_text.lower() for link in evidence_links)

        # 4. Check Story Candidate for Narrative Turn / Resolution
        if candidate_type == CandidateType.STORY_CANDIDATE:
            has_turn = any(indicator in combined_text for indicator in cls.TURN_INDICATORS)
            if not has_turn:
                raise MissingStoryTurnError(
                    f"Story candidate '{title}' lacks a decisive narrative turn or resolution indicator in its evidence text."
                )

        return ContentCandidate(
            workspace_id=workspace_id,
            candidate_type=candidate_type,
            title=title,
            hook_statement=hook_statement,
            narrative_completeness=narrative_completeness,
            story_arc=story_arc,
            tension_ref=tension_ref,
            invariant_ref=invariant_ref,
            archetypal_container=archetypal_container,
            evidence_links=evidence_links,
            cmf_score=cmf_score,
            production_status=production_status,
            standalone_context_notes=standalone_context_notes,
        )
