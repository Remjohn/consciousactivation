"""
test_candidate_adversarial_cases.py
-----------------------------------
Adversarial tests for ungrounded hooks, story missing turn, incomplete narrative, and premature approval.
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "candidate-intelligence" / "src"))

import pytest

from cae_candidate_intelligence.composer import EditorialCandidateComposer
from cae_candidate_intelligence.domain import (
    CandidateEvidenceLink,
    CandidateType,
    HeritageCMFScore,
    NarrativeCompleteness,
    ProductionStatus,
)
from cae_candidate_intelligence.errors import (
    MissingStoryTurnError,
    NarrativeIncompletenessError,
    PrematureProductionApprovalError,
    UngroundedCandidateError,
)


def test_ungrounded_viral_hook_rejection():
    # Attempting to form a candidate with empty evidence links
    cmf = HeritageCMFScore.calculate(
        emotional_resonance=0.95,
        cognitive_novelty=0.95,
        authority_evidence=0.0,
        narrative_velocity=0.99,
    )

    with pytest.raises(UngroundedCandidateError, match="completely ungrounded"):
        EditorialCandidateComposer.compose_candidate(
            workspace_id="ws-client-99",
            candidate_type=CandidateType.QUOTE_CANDIDATE,
            title="Pure Clickbait",
            hook_statement="This one trick changed everything forever!",
            narrative_completeness=NarrativeCompleteness.COMPLETE,
            evidence_links=[],  # VIOLATION! Empty lineage
            cmf_score=cmf,
        )


def test_story_missing_turn_rejection():
    # Story text that has context and setup but no turn or breakthrough
    flat_text = "In 2019 we worked from 9am to 5pm in the office and had daily standup meetings every single day."
    h = hashlib.sha256(flat_text.encode("utf-8")).hexdigest()

    link = CandidateEvidenceLink(
        segment_id="SEG-FLAT-1",
        annotation_id="ANN-FLAT-1",
        speaker="Guest",
        start_time_ms=0,
        end_time_ms=10000,
        verbatim_text=flat_text,
        text_sha256=h,
    )

    cmf = HeritageCMFScore.calculate(
        emotional_resonance=0.3,
        cognitive_novelty=0.2,
        authority_evidence=0.5,
        narrative_velocity=0.4,
    )

    with pytest.raises(MissingStoryTurnError, match="lacks a decisive narrative turn"):
        EditorialCandidateComposer.compose_candidate(
            workspace_id="ws-client-99",
            candidate_type=CandidateType.STORY_CANDIDATE,
            title="Flat Story",
            hook_statement="Our daily routine in 2019.",
            narrative_completeness=NarrativeCompleteness.COMPLETE,
            evidence_links=[link],
            cmf_score=cmf,
        )


def test_incomplete_narrative_rejection():
    text = "We walked into the conference room and..."
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()

    link = CandidateEvidenceLink(
        segment_id="SEG-INC-1",
        annotation_id="ANN-INC-1",
        speaker="Guest",
        start_time_ms=0,
        end_time_ms=3000,
        verbatim_text=text,
        text_sha256=h,
    )

    cmf = HeritageCMFScore.calculate(
        emotional_resonance=0.5,
        cognitive_novelty=0.5,
        authority_evidence=0.5,
        narrative_velocity=0.5,
    )

    with pytest.raises(NarrativeIncompletenessError, match="marked INCOMPLETE"):
        EditorialCandidateComposer.compose_candidate(
            workspace_id="ws-client-99",
            candidate_type=CandidateType.BEAT_CANDIDATE,
            title="Incomplete Beat",
            hook_statement="Entering the room...",
            narrative_completeness=NarrativeCompleteness.INCOMPLETE,  # VIOLATION!
            evidence_links=[link],
            cmf_score=cmf,
        )


def test_premature_production_approval_rejection():
    text = "Valid verified evidence text with complete narrative and insight."
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()

    link = CandidateEvidenceLink(
        segment_id="SEG-VAL-1",
        annotation_id="ANN-VAL-1",
        speaker="Guest",
        start_time_ms=0,
        end_time_ms=8000,
        verbatim_text=text,
        text_sha256=h,
    )

    cmf = HeritageCMFScore.calculate(
        emotional_resonance=0.8,
        cognitive_novelty=0.8,
        authority_evidence=0.8,
        narrative_velocity=0.8,
    )

    with pytest.raises(PrematureProductionApprovalError, match="APPROVED_FOR_PRODUCTION"):
        EditorialCandidateComposer.compose_candidate(
            workspace_id="ws-client-99",
            candidate_type=CandidateType.QUOTE_CANDIDATE,
            title="Premature Candidate",
            hook_statement="Insight statement.",
            narrative_completeness=NarrativeCompleteness.COMPLETE,
            evidence_links=[link],
            cmf_score=cmf,
            production_status=ProductionStatus.APPROVED_FOR_PRODUCTION,  # VIOLATION!
        )
