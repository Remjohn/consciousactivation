"""
fixture_adapter.py
------------------
Deterministic fixture adapter for offline testing, CI, and false-proof verification.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from ..domain import RawObservation
from .base import BaseResearchAdapter


class FixtureResearchAdapter(BaseResearchAdapter):
    """Provides deterministic test observations for automated verification suites."""

    @classmethod
    def get_valid_multi_source_fixture(cls, topic: str = "Universal Latent Geometry") -> List[RawObservation]:
        """Returns 3 independent observations from 3 distinct platforms and root domains."""
        now = datetime.now(timezone.utc) - timedelta(hours=3)
        return [
            RawObservation(
                source_platform="hackernews",
                query_context=topic,
                raw_payload={"points": 450, "comments": 120},
                retrieved_at=now,
                raw_text_snippet="Universal latent geometry preserves relational distance across disparate transformer embedding models.",
                source_url="https://news.ycombinator.com/item?id=38912401",
                author_outlet="hn_user_42",
            ),
            RawObservation(
                source_platform="reddit",
                query_context=topic,
                raw_payload={"score": 380, "subreddit": "MachineLearning"},
                retrieved_at=now,
                raw_text_snippet="New Cornell paper demonstrates that vector spaces preserve geometry across separate training runs.",
                source_url="https://reddit.com/r/MachineLearning/comments/1abc234/universal_geometry",
                author_outlet="r/MachineLearning",
            ),
            RawObservation(
                source_platform="searxng",
                query_context=topic,
                raw_payload={"engines": ["google", "duckduckgo", "brave"]},
                retrieved_at=now,
                raw_text_snippet="Vector Space Preservation (VSP) proves that disparate foundation models map onto the same Platonic representation.",
                source_url="https://arxiv.org/abs/2501.12345",
                author_outlet="arxiv.org",
            ),
        ]

    @classmethod
    def get_syndicated_mirror_fixture(cls, topic: str = "Fed Rate Decision") -> List[RawObservation]:
        """Returns 5 copies of the same Reuters wire syndicated across 5 different blog/scraper domains."""
        now = datetime.now(timezone.utc) - timedelta(hours=1)
        wire_text = "(Reuters) - The Federal Reserve held benchmark interest rates steady at 5.25% today, signaling no immediate cuts."
        return [
            RawObservation(
                source_platform="searxng",
                query_context=topic,
                raw_payload={},
                retrieved_at=now,
                raw_text_snippet=wire_text,
                source_url="https://www.reuters.com/markets/rates-decision-2026",
                author_outlet="Reuters",
            ),
            RawObservation(
                source_platform="searxng",
                query_context=topic,
                raw_payload={},
                retrieved_at=now,
                raw_text_snippet=wire_text,
                source_url="https://finance-mirror1.com/news/reuters-rates-2026",
                author_outlet="FinanceMirror1",
            ),
            RawObservation(
                source_platform="searxng",
                query_context=topic,
                raw_payload={},
                retrieved_at=now,
                raw_text_snippet=wire_text,
                source_url="https://market-scraper-blog.net/fed-holds-rates",
                author_outlet="ScraperBot",
            ),
            RawObservation(
                source_platform="searxng",
                query_context=topic,
                raw_payload={},
                retrieved_at=now,
                raw_text_snippet=wire_text,
                source_url="https://crypto-news-daily.org/macro-fed-update",
                author_outlet="CryptoDaily",
            ),
            RawObservation(
                source_platform="searxng",
                query_context=topic,
                raw_payload={},
                retrieved_at=now,
                raw_text_snippet=wire_text,
                source_url="https://daily-feed-aggregator.io/story/9912",
                author_outlet="AggregatorIO",
            ),
        ]

    @classmethod
    def get_stale_observation_fixture(cls) -> List[RawObservation]:
        """Returns an observation from 90 days ago (exceeding default 30-day TTL)."""
        stale_time = datetime.now(timezone.utc) - timedelta(days=95)
        return [
            RawObservation(
                source_platform="searxng",
                query_context="Old event",
                raw_payload={},
                retrieved_at=stale_time,
                raw_text_snippet="Historical press release from earlier this year discussing past quarter projections.",
                source_url="https://example.com/archive/2026/01/press-release",
                author_outlet="ArchiveNews",
            )
        ]

    def fetch_observations(self, query: str, **kwargs: Any) -> List[RawObservation]:
        fixture_type = kwargs.get("fixture_type", "valid")
        if fixture_type == "valid":
            return self.get_valid_multi_source_fixture(query)
        elif fixture_type == "syndicated":
            return self.get_syndicated_mirror_fixture(query)
        elif fixture_type == "stale":
            return self.get_stale_observation_fixture()
        else:
            raise ValueError(f"Unknown fixture type: {fixture_type}")
