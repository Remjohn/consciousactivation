"""
test_source_multiplicity_and_anti_inflation.py
----------------------------------------------
Tests anti-inflation rules, ensuring syndication mirrors cannot masquerade as independent corroboration.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "world-intelligence" / "src"))

from cae_world_intelligence.adapters.fixture_adapter import FixtureResearchAdapter
from cae_world_intelligence.normalization import SignalNormalizer
from cae_world_intelligence.verifier import ResearchSignalVerifier


def test_syndication_de_inflation():
    adapter = FixtureResearchAdapter()
    syndicated_observations = adapter.get_syndicated_mirror_fixture("Fed Rate Decision")

    assert len(syndicated_observations) == 5

    multiplicity, provenance_records = SignalNormalizer.calculate_multiplicity(syndicated_observations)

    # All 5 have different URLs / domains, but identical text and explicit Reuters wire attribution
    assert multiplicity.raw_mention_count == 5
    assert multiplicity.unique_root_domain_count == 5
    # Crucial assertion: independent source count must be 1, NOT 5!
    assert multiplicity.independent_source_count == 1
    assert multiplicity.syndication_ratio >= 0.80

    signal = SignalNormalizer.synthesize_signal(
        topic="Federal Reserve Rate Decision",
        observations=syndicated_observations,
        confidence_base=0.95,
    )

    # Confidence must be capped because independent_source_count == 1
    assert signal.confidence_score <= 0.60
    assert ResearchSignalVerifier.verify(signal) is True
