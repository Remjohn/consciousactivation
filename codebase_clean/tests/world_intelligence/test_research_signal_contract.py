"""
test_research_signal_contract.py
--------------------------------
Validates ResearchSignal domain model serialization, fields, and immutability invariants.
"""

import sys
from pathlib import Path

# Add world-intelligence src to sys.path
sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "world-intelligence" / "src"))

import pytest
from datetime import datetime, timezone
from cae_world_intelligence.domain import (
    ResearchSignal,
    ProvenanceRecord,
    SourceMultiplicity,
)
from cae_world_intelligence.verifier import ResearchSignalVerifier


def test_research_signal_instantiation_and_serialization():
    now = datetime.now(timezone.utc)
    snippet = "Large multimodal models demonstrate unified latent representations across vision and language."
    content_hash = ProvenanceRecord.compute_content_hash(snippet)

    prov = ProvenanceRecord(
        origin_url="https://arxiv.org/abs/2501.9999",
        root_domain="arxiv.org",
        platform="searxng",
        observed_at=now,
        content_hash_sha256=content_hash,
        author_outlet="Cornell Researchers",
    )

    multiplicity = SourceMultiplicity(
        raw_mention_count=3,
        unique_root_domain_count=3,
        independent_source_count=3,
        syndication_ratio=0.0,
    )

    signal = ResearchSignal(
        topic="Universal Multimodal Geometry",
        entities=["Cornell", "LMM", "Platonic Representation"],
        observation_time=now,
        velocity_score=0.85,
        acceleration_score=0.60,
        cross_source_divergence=0.25,
        novelty_score=0.90,
        confidence_score=0.95,
        evidence_excerpt=snippet,
        source_multiplicity=multiplicity,
        primary_provenance=prov,
    )

    assert signal.signal_id.startswith("SIG-")
    assert signal.topic == "Universal Multimodal Geometry"
    assert len(signal.entities) == 3
    assert ResearchSignalVerifier.verify(signal) is True

    # Test serialization to JSON/dict
    signal_dict = signal.model_dump()
    assert signal_dict["primary_provenance"]["root_domain"] == "arxiv.org"
    assert signal_dict["source_multiplicity"]["independent_source_count"] == 3


def test_invalid_score_ranges():
    now = datetime.now(timezone.utc)
    snippet = "Test snippet exceeding 10 characters."
    prov = ProvenanceRecord(
        origin_url="https://example.com/test",
        root_domain="example.com",
        platform="searxng",
        observed_at=now,
        content_hash_sha256=ProvenanceRecord.compute_content_hash(snippet),
    )
    multiplicity = SourceMultiplicity(
        raw_mention_count=1,
        unique_root_domain_count=1,
        independent_source_count=1,
    )

    # velocity_score out of range (> 1.0)
    with pytest.raises(ValueError):
        ResearchSignal(
            topic="Invalid Score",
            observation_time=now,
            velocity_score=1.5,
            confidence_score=0.5,
            evidence_excerpt=snippet,
            source_multiplicity=multiplicity,
            primary_provenance=prov,
        )
