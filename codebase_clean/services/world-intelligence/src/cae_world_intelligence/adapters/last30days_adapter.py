"""
last30days_adapter.py
---------------------
Multi-Source Fan-Out Adapter based on the last30days-skill methodology.
Aggregates discussions across Reddit, X, YouTube, HN, and Polymarket.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from ..domain import RawObservation
from .base import BaseResearchAdapter


class Last30DaysAdapter(BaseResearchAdapter):
    """
    Adapter implementing multi-source fan-out aggregation across community platforms.
    """

    SUPPORTED_PLATFORMS = {"reddit", "x", "youtube", "hackernews", "polymarket", "web"}

    def parse_platform_payload(self, payload: Dict[str, Any], query: str) -> List[RawObservation]:
        """Parse structured items from last30days multi-platform responses."""
        items = payload.get("items", [])
        observations: List[RawObservation] = []
        now = datetime.now(timezone.utc)

        for item in items:
            platform = item.get("platform", "web").lower()
            url = item.get("url") or f"https://{platform}.com/item/{item.get('id', 'unknown')}"
            text = item.get("text") or item.get("title") or item.get("snippet") or ""
            if not text:
                continue

            created_at_raw = item.get("created_at") or item.get("timestamp")
            obs_time = now
            if created_at_raw:
                try:
                    obs_time = datetime.fromisoformat(str(created_at_raw).replace("Z", "+00:00"))
                except Exception:
                    obs_time = now

            obs = RawObservation(
                source_platform=platform,
                query_context=query,
                raw_payload=item,
                retrieved_at=obs_time,
                raw_text_snippet=text,
                source_url=url,
                author_outlet=item.get("author") or item.get("subreddit") or platform,
            )
            observations.append(obs)

        return observations

    def fetch_observations(self, query: str, **kwargs: Any) -> List[RawObservation]:
        """Parse from fixture or payload."""
        if "fixture_payload" in kwargs:
            return self.parse_platform_payload(kwargs["fixture_payload"], query)
            
        raise NotImplementedError("Live last30days skill calls require registered agent credentials. Use fixture_payload for offline/test verification.")
