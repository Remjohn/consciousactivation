"""
test_observable_vs_inference_separation.py
------------------------------------------
Tests strict partitioning between immutable observable evidence and model inference.
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


def test_strict_partition_separation():
    raw_text = "We lost three major enterprise clients within two weeks because of our outage."
    text_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()

    ann = SemanticEvidenceClassifier.classify(
        workspace_id="ws-client-99",
        session_id="SES-001",
        segment_id="SEG-100",
        speaker="Guest",
        start_time_ms=5000,
        end_time_ms=12000,
        verbatim_text=raw_text,
        text_sha256=text_hash,
        semantic_role=SemanticRole.PROOF,
        epistemic_status=EvidenceEpistemicStatus.FIRST_PARTY_FACT,
        confidence_score=0.95,
        tension_ref="AET-RELIABILITY-TRUST",
        invariant_ref="SDA-INV-FEEDBACK-LATENCY",
        emotional_register=EmotionalRegister.RESOLVE,
        story_arc_geometry=StoryArcGeometry.CRUCIBLE_AND_REBIRTH,
    )

    # Observable evidence cannot contain inference fields
    obs = ann.observable_evidence
    assert hasattr(obs, "verbatim_text")
    assert hasattr(obs, "start_time_ms")
    assert hasattr(obs, "text_sha256")
    assert not hasattr(obs, "semantic_role")
    assert not hasattr(obs, "tension_ref")

    # Semantic inference contains model interpretations
    inf = ann.semantic_inference
    assert inf.semantic_role == SemanticRole.PROOF
    assert inf.epistemic_status == EvidenceEpistemicStatus.FIRST_PARTY_FACT
    assert inf.tension_ref == "AET-RELIABILITY-TRUST"
    assert inf.is_publishable is False
