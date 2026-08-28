"""
test_candidate_domain_contracts.py
----------------------------------
Validates ContentCandidate serialization, typing, and schema integrity.
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
    ProductionStatus,
)
from cae_candidate_intelligence.verifier import ContentCandidateVerifier


def test_content_candidate_creation_and_verification():
    quote_text = "The hardest leadership lesson is learning that clarity without compassion is brutality."
    h = hashlib.sha256(quote_text.encode("utf-8")).hexdigest()

    link = CandidateEvidenceLink(
        segment_id="SEG-001",
        annotation_id="ANN-001",
        speaker="Guest",
        start_time_ms=10000,
        end_time_ms=15000,
        verbatim_text=quote_text,
        text_sha256=h,
    )

    cmf = HeritageCMFScore.calculate(
        emotional_resonance=0.88,
        cognitive_novelty=0.91,
        authority_evidence=0.85,
        narrative_velocity=0.90,
    )

    candidate = EditorialCandidateComposer.compose_candidate(
        workspace_id="ws-client-99",
        candidate_type=CandidateType.QUOTE_CANDIDATE,
        title="Clarity vs Compassion",
        hook_statement="Clarity without compassion is brutality.",
        narrative_completeness=NarrativeCompleteness.COMPLETE,
        evidence_links=[link],
        cmf_score=cmf,
        tension_ref="AET-RADICAL-CANDOR",
        production_status=ProductionStatus.DRAFT_CANDIDATE,
    )

    assert candidate.candidate_id.startswith("CND-")
    assert candidate.production_status == ProductionStatus.DRAFT_CANDIDATE
    assert candidate.cmf_score.composite_score > 0.8
    assert ContentCandidateVerifier.verify_candidate(candidate) is True
