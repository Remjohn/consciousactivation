"""
test_candidate_formation_types.py
---------------------------------
Tests composition across multiple candidate types including Story, Mechanism, and Transformation.
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "candidate-intelligence" / "src"))

from cae_candidate_intelligence.composer import EditorialCandidateComposer
from cae_candidate_intelligence.domain import (
    CandidateEvidenceLink,
    CandidateType,
    HeritageCMFScore,
    NarrativeCompleteness,
)


def test_story_and_mechanism_candidates():
    # 1. Story Candidate with explicit turn
    story_text = (
        "In 2021 we thought our growth was unstoppable, but then the supply chain collapsed in May. "
        "We realized that our reliance on single-source vendors was a fatal design flaw."
    )
    h1 = hashlib.sha256(story_text.encode("utf-8")).hexdigest()

    link1 = CandidateEvidenceLink(
        segment_id="SEG-STORY-1",
        annotation_id="ANN-STORY-1",
        speaker="Guest",
        start_time_ms=0,
        end_time_ms=25000,
        verbatim_text=story_text,
        text_sha256=h1,
    )

    cmf = HeritageCMFScore.calculate(
        emotional_resonance=0.90,
        cognitive_novelty=0.85,
        authority_evidence=0.95,
        narrative_velocity=0.80,
    )

    story_cand = EditorialCandidateComposer.compose_candidate(
        workspace_id="ws-client-99",
        candidate_type=CandidateType.STORY_CANDIDATE,
        title="The Supply Chain Crucible",
        hook_statement="How a single supply chain failure forced us to rebuild from zero.",
        narrative_completeness=NarrativeCompleteness.COMPLETE,
        story_arc="THE_WITNESS",
        evidence_links=[link1],
        cmf_score=cmf,
    )

    assert story_cand.candidate_type == CandidateType.STORY_CANDIDATE
    assert story_cand.story_arc == "THE_WITNESS"

    # 2. Mechanism Candidate
    mech_text = "When feedback loops exceed 48 hours, team velocity drops exponentially because anxiety fills the information vacuum."
    h2 = hashlib.sha256(mech_text.encode("utf-8")).hexdigest()

    link2 = CandidateEvidenceLink(
        segment_id="SEG-MECH-1",
        annotation_id="ANN-MECH-1",
        speaker="Guest",
        start_time_ms=30000,
        end_time_ms=42000,
        verbatim_text=mech_text,
        text_sha256=h2,
    )

    mech_cand = EditorialCandidateComposer.compose_candidate(
        workspace_id="ws-client-99",
        candidate_type=CandidateType.MECHANISM_CANDIDATE,
        title="The Feedback Latency Trap",
        hook_statement="Why slow feedback kills team velocity.",
        narrative_completeness=NarrativeCompleteness.COMPLETE,
        invariant_ref="SDA-INV-FEEDBACK-LATENCY",
        evidence_links=[link2],
        cmf_score=cmf,
    )

    assert mech_cand.candidate_type == CandidateType.MECHANISM_CANDIDATE
    assert mech_cand.invariant_ref == "SDA-INV-FEEDBACK-LATENCY"
