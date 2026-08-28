"""
test_searxng_adapter.py
-----------------------
Tests SearXNG multi-engine parser, SERP feature extraction, and signal synthesis.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "world-intelligence" / "src"))

from cae_world_intelligence.adapters.searxng_adapter import SearXNGAdapter
from cae_world_intelligence.normalization import SignalNormalizer
from cae_world_intelligence.verifier import ResearchSignalVerifier


def test_searxng_payload_parsing_and_synthesis():
    adapter = SearXNGAdapter()
    
    mock_payload = {
        "query": "Universal Geometry Embeddings",
        "number_of_results": 2,
        "results": [
            {
                "url": "https://arxiv.org/abs/2501.9999",
                "title": "Harnessing the Universal Geometry of Embeddings",
                "content": "A rigorous foundation showing that deep learning models converge to shared universal geometry.",
                "engines": ["google", "duckduckgo"],
                "author": "Cornell",
                "publishedDate": "2026-08-20T10:00:00Z"
            },
            {
                "url": "https://venturebeat.com/ai/universal-embeddings",
                "title": "Why Universal Latent Spaces Change Multimodal AI",
                "content": "Industry analysis of the Platonic Representation Hypothesis and cross-model alignment.",
                "engines": ["brave", "bing"],
                "author": "VentureBeat",
                "publishedDate": "2026-08-22T14:30:00Z"
            }
        ]
    }

    observations = adapter.fetch_observations("Universal Geometry", fixture_payload=mock_payload)
    assert len(observations) == 2
    assert observations[0].source_platform == "searxng"
    assert observations[0].author_outlet == "Cornell"

    signal = SignalNormalizer.synthesize_signal(
        topic="Universal Geometry Embeddings",
        observations=observations,
        entities=["Cornell", "Platonic Representation"],
        velocity_score=0.75,
        confidence_base=0.85,
    )

    assert signal.topic == "Universal Geometry Embeddings"
    assert signal.source_multiplicity.unique_root_domain_count == 2
    assert signal.source_multiplicity.independent_source_count == 2
    assert ResearchSignalVerifier.verify(signal) is True
