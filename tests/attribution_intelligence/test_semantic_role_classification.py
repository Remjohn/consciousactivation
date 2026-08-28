"""
test_semantic_role_classification.py
------------------------------------
Tests classification across multiple semantic roles and epistemic tiers.
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "attribution-intelligence" / "src"))

from cae_attribution_intelligence.classifier import SemanticEvidenceClassifier
from cae_attribution_intelligence.domain import (
    EvidenceEpistemicStatus,
    SemanticRole,
)
from cae_attribution_intelligence.verifier import SemanticAttributionVerifier


def test_multiple_semantic_roles():
    cases = [
        (
            SemanticRole.QUOTE,
            "Culture is not what you preach on slides; culture is what you tolerate in private.",
            EvidenceEpistemicStatus.ABSTRACT_OPINION,
        ),
        (
            SemanticRole.MECHANISM,
            "When latency exceeds 300 milliseconds, users drop off because their cognitive dopamine prediction loop breaks.",
            EvidenceEpistemicStatus.FIRST_PARTY_FACT,
        ),
        (
            SemanticRole.CONTRADICTION,
            "We were told that hiring more engineers would speed up the delivery, but our cycle time doubled.",
            EvidenceEpistemicStatus.LIVED_EXPERIENCE,
        ),
        (
            SemanticRole.REVEAL,
            "The truth is that I approved that acquisition without reading the audit report.",
            EvidenceEpistemicStatus.LIVED_EXPERIENCE,
        ),
        (
            SemanticRole.PROOF,
            "In Q3 2024, our customer retention rate rose from 42% to 89% after deploying automated onboarding.",
            EvidenceEpistemicStatus.FIRST_PARTY_FACT,
        ),
    ]

    for role, text, epistemic in cases:
        h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        ann = SemanticEvidenceClassifier.classify(
            workspace_id="ws-client-99",
            session_id="SES-001",
            segment_id="SEG-1",
            speaker="Guest",
            start_time_ms=0,
            end_time_ms=10000,
            verbatim_text=text,
            text_sha256=h,
            semantic_role=role,
            epistemic_status=epistemic,
        )

        assert ann.semantic_inference.semantic_role == role
        assert SemanticAttributionVerifier.verify_annotation(ann) is True
