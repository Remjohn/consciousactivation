"""
test_world_signal_negative_cases.py
-----------------------------------
Validates rejection of fabricated text, stale observations, and invalid provenance.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "world-intelligence" / "src"))

import pytest
from datetime import datetime, timedelta, timezone

from cae_world_intelligence.domain import (
    ProvenanceRecord,
    ResearchSignal,
    SourceMultiplicity,
)
from cae_world_intelligence.errors import (
    DuplicateSourceInflationError,
    EvidenceError,
    ProvenanceError,
    StaleObservationError,
)
from cae_world_intelligence.verifier import ResearchSignalVerifier


def create_base_signal(
    *,
    snippet: str = "Authentic observation text from verified source.",
    observed_at: datetime | None = None,
    origin_url: str = "https://arxiv.org/abs/2501.1234",
    confidence: float = 0.80,
    indep_sources: int = 2,
    unique_domains: int = 2,
    hash_override: str | None = None,
) -> ResearchSignal:
    now = datetime.now(timezone.utc)
    obs_time = observed_at or (now - timedelta(days=2))
    content_hash = hash_override or ProvenanceRecord.compute_content_hash(snippet)

    prov = ProvenanceRecord(
        origin_url=origin_url,
        root_domain="arxiv.org",
        platform="searxng",
        observed_at=obs_time,
        content_hash_sha256=content_hash,
    )

    multiplicity = SourceMultiplicity(
        raw_mention_count=indep_sources,
        unique_root_domain_count=unique_domains,
        independent_source_count=indep_sources,
        syndication_ratio=0.0,
    )

    return ResearchSignal(
        topic="Test Signal Topic",
        observation_time=obs_time,
        velocity_score=0.7,
        confidence_score=confidence,
        evidence_excerpt=snippet,
        source_multiplicity=multiplicity,
        primary_provenance=prov,
    )


def test_fabricated_text_tamper_detection():
    # Signal where declared hash does not match actual snippet
    signal = create_base_signal(
        snippet="This snippet has been modified/tampered after hash computation.",
        hash_override="a" * 64,  # Fake hash
    )

    with pytest.raises(EvidenceError, match="Fabrication check failed"):
        ResearchSignalVerifier.verify(signal)


def test_stale_observation_rejection():
    # Observation from 60 days ago
    stale_time = datetime.now(timezone.utc) - timedelta(days=60)
    signal = create_base_signal(observed_at=stale_time)

    with pytest.raises(StaleObservationError, match="exceeds maximum freshness TTL"):
        ResearchSignalVerifier.verify(signal)


def test_invalid_provenance_url():
    signal = create_base_signal(origin_url="not_a_valid_url")

    with pytest.raises(ProvenanceError, match="Invalid provenance URL"):
        ResearchSignalVerifier.verify(signal)


def test_duplicate_source_inflation_rejection():
    # Attempting to claim confidence 0.95 with only 1 independent source
    signal = create_base_signal(confidence=0.95, indep_sources=1, unique_domains=1)

    with pytest.raises(DuplicateSourceInflationError, match="requires at least 2 independent sources"):
        ResearchSignalVerifier.verify(signal)
