"""
test_attribution_domain_contracts.py
------------------------------------
Validates SemanticAnnotation and EvidenceClassification serialization and schema typing.
"""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "attribution-intelligence" / "src"))

from cae_attribution_intelligence.classifier import SemanticEvidenceClassifier
from cae_attribution_intelligence.domain import (
    EmotionalRegister,
    EvidenceEpistemicStatus,
    SemanticRole,
    StoryArcGeometry,
)
from cae_attribution_intelligence.verifier import SemanticAttributionVerifier


def test_semantic_annotation_creation_and_serialization():
    text = (
        "In October 2022, when the server farm melted down in Dublin, "
        "I was standing in the cold hallway knowing that fifty thousand customer databases were offline."
    )
    text_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

    ann = SemanticEvidenceClassifier.classify(
        workspace_id="ws-client-99",
        session_id="SES-100",
        segment_id="SEG-101",
        speaker="Guest",
        start_time_ms=10000,
        end_time_ms=22000,
        verbatim_text=text,
        text_sha256=text_hash,
        semantic_role=SemanticRole.STORY,
        epistemic_status=EvidenceEpistemicStatus.LIVED_EXPERIENCE,
        confidence_score=0.92,
        tension_ref="AET-CRISIS-LEADERSHIP",
        emotional_register=EmotionalRegister.VULNERABILITY,
        story_arc_geometry=StoryArcGeometry.THE_WITNESS,
    )

    assert ann.annotation_id.startswith("ANN-")
    assert ann.observable_evidence.speaker == "Guest"
    assert ann.semantic_inference.semantic_role == SemanticRole.STORY
    assert ann.semantic_inference.is_publishable is False
    assert SemanticAttributionVerifier.verify_annotation(ann) is True

    record = SemanticEvidenceClassifier.create_classification_record(ann)
    assert record.primary_role == SemanticRole.STORY
    assert record.epistemic_tier == EvidenceEpistemicStatus.LIVED_EXPERIENCE
