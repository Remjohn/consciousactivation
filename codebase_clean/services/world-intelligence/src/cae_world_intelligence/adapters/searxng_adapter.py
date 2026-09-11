"""
searxng_adapter.py
------------------
SearXNG Metasearch Ingestion Adapter.
Parses multi-engine SERP responses without vendor bias.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..domain import RawObservation
from .base import BaseResearchAdapter


class SearXNGAdapter(BaseResearchAdapter):
    """
    Adapter for SearXNG metasearch JSON payloads.
    Translates multi-engine SERP aggregations into typed RawObservations.
    """

    def __init__(self, endpoint_url: Optional[str] = None):
        self.endpoint_url = endpoint_url or "http://localhost:8888"

    def parse_searxng_response(self, payload: Dict[str, Any], query: str) -> List[RawObservation]:
        """Parse raw SearXNG JSON dictionary into RawObservation instances."""
        results = payload.get("results", [])
        observations: List[RawObservation] = []

        now = datetime.now(timezone.utc)
        for item in results:
            url = item.get("url")
            content = item.get("content") or item.get("title") or ""
            if not url or not content:
                continue

            engines = item.get("engines", ["searxng"])
            author = item.get("author") or engines[0] if engines else "searxng"
            
            # Extract published date if present
            pub_date_raw = item.get("publishedDate")
            obs_time = now
            if pub_date_raw:
                try:
                    obs_time = datetime.fromisoformat(pub_date_raw.replace("Z", "+00:00"))
                except Exception:
                    obs_time = now

            obs = RawObservation(
                source_platform="searxng",
                query_context=query,
                raw_payload=item,
                retrieved_at=obs_time,
                raw_text_snippet=content,
                source_url=url,
                author_outlet=author,
            )
            observations.append(obs)

        return observations

    def fetch_observations(self, query: str, **kwargs: Any) -> List[RawObservation]:
        """
        In production, executes HTTP GET to SearXNG JSON endpoint.
        If 'fixture_payload' is passed in kwargs, parses that payload directly.
        """
        if "fixture_payload" in kwargs:
            return self.parse_searxng_response(kwargs["fixture_payload"], query)
            
        # In bounded local environments without active SearXNG container, raises or returns empty
        raise NotImplementedError("Live HTTP SearXNG retrieval requires active SEARXNG_ENDPOINT. Use fixture_payload for offline/test execution.")
