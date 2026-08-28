"""
test_last30days_adapter.py
--------------------------
Tests the multi-platform fan-out adapter (Reddit, X, YouTube, HN, Polymarket).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "world-intelligence" / "src"))

from cae_world_intelligence.adapters.last30days_adapter import Last30DaysAdapter
from cae_world_intelligence.normalization import SignalNormalizer
from cae_world_intelligence.verifier import ResearchSignalVerifier


def test_last30days_fanout_parsing():
    adapter = Last30DaysAdapter()

    mock_payload = {
        "items": [
            {
                "platform": "reddit",
                "id": "abc1234",
                "subreddit": "MachineLearning",
                "title": "Discussion on Latent Space Preservation",
                "text": "Detailed community breakdown of how vector spaces preserve metric structures across models.",
                "created_at": "2026-08-25T12:00:00Z"
            },
            {
                "platform": "hackernews",
                "id": "hn9988",
                "author": "hn_hacker",
                "title": "Harnessing the Universal Geometry of Embeddings",
                "text": "Hacker News discussion regarding the mathematical underpinnings of universal representations.",
                "created_at": "2026-08-26T08:00:00Z"
            },
            {
                "platform": "polymarket",
                "id": "pm5544",
                "title": "Will universal embedding alignment reach consensus in 2026?",
                "snippet": "Prediction market volume reaches 2.4M on model interoperability standards.",
                "created_at": "2026-08-27T09:30:00Z"
            }
        ]
    }

    observations = adapter.fetch_observations("Universal Geometry", fixture_payload=mock_payload)
    assert len(observations) == 3
    platforms = {obs.source_platform for obs in observations}
    assert platforms == {"reddit", "hackernews", "polymarket"}

    signal = SignalNormalizer.synthesize_signal(
        topic="Cross-Platform Consensus on Universal Geometry",
        observations=observations,
        velocity_score=0.90,
        acceleration_score=0.80,
    )

    assert signal.source_multiplicity.unique_root_domain_count == 3
    assert signal.source_multiplicity.independent_source_count == 3
    assert ResearchSignalVerifier.verify(signal) is True
