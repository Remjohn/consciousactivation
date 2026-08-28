"""
test_attribution_adversarial_cases.py
-------------------------------------
Adversarial tests for quote mislabeled as story, speculative statement marked fact, and invariant inflation.
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "attribution-intelligence" / "src"))

import pytest

from cae_attribution_intelligence.classifier import SemanticEvidenceClassifier
from cae_attribution_intelligence.domain import (
    EvidenceEpistemicStatus,
    SemanticRole,
)
from cae_attribution_intelligence.errors import (
    EvidenceStatusInflationError,
    InvariantInflationError,
    PrematurePublishabilityError,
    StoryLabelingViolationError,
)


def test_quote_mislabeled_as_story_rejection():
    # Short punchy quote mislabeled as a full STORY
    text = "Fail fast and break things."
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()

    with pytest.raises(StoryLabelingViolationError, match="Story labeling violation"):
        SemanticEvidenceClassifier.classify(
            workspace_id="ws-client-99",
            session_id="SES-001",
            segment_id="SEG-1",
            speaker="Guest",
            start_time_ms=0,
            end_time_ms=2000,
            verbatim_text=text,
            text_sha256=h,
            semantic_role=SemanticRole.STORY,  # VIOLATION! Only 5 words, no narrative arc
            epistemic_status=EvidenceEpistemicStatus.ABSTRACT_OPINION,
        )


def test_speculative_statement_marked_as_fact_rejection():
    # Speculative hedge marked as empirical FIRST_PARTY_FACT
    text = "I think maybe the market could collapse next year if interest rates stay high."
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()

    with pytest.raises(EvidenceStatusInflationError, match="Evidence status inflation"):
        SemanticEvidenceClassifier.classify(
            workspace_id="ws-client-99",
            session_id="SES-001",
            segment_id="SEG-2",
            speaker="Guest",
            start_time_ms=0,
            end_time_ms=5000,
            verbatim_text=text,
            text_sha256=h,
            semantic_role=SemanticRole.CLAIM,
            epistemic_status=EvidenceEpistemicStatus.FIRST_PARTY_FACT,  # VIOLATION! Speculative
        )


def test_generic_phrase_assigned_deep_invariant_rejection():
    # Generic phrase with no mechanism assigned a structural SDA invariant
    text = "It felt really good."
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()

    with pytest.raises(InvariantInflationError, match="Invariant inflation"):
        SemanticEvidenceClassifier.classify(
            workspace_id="ws-client-99",
            session_id="SES-001",
            segment_id="SEG-3",
            speaker="Guest",
            start_time_ms=0,
            end_time_ms=2000,
            verbatim_text=text,
            text_sha256=h,
            semantic_role=SemanticRole.BEAT,
            epistemic_status=EvidenceEpistemicStatus.LIVED_EXPERIENCE,
            invariant_ref="SDA-INV-FEEDBACK-ASYMMETRY",  # VIOLATION! No causal mechanism
        )


def test_premature_publishability_rejection():
    text = "A valid complete sentence explaining our core engineering principle."
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()

    with pytest.raises(PrematurePublishabilityError, match="Cannot mark annotation as publishable"):
        SemanticEvidenceClassifier.classify(
            workspace_id="ws-client-99",
            session_id="SES-001",
            segment_id="SEG-4",
            speaker="Guest",
            start_time_ms=0,
            end_time_ms=4000,
            verbatim_text=text,
            text_sha256=h,
            semantic_role=SemanticRole.CLAIM,
            epistemic_status=EvidenceEpistemicStatus.ABSTRACT_OPINION,
            is_publishable=True,  # VIOLATION!
        )
