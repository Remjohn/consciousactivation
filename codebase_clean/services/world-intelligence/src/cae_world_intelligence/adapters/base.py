"""
base.py
-------
Abstract Base Adapter for World Intelligence.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ..domain import RawObservation


class BaseResearchAdapter(ABC):
    """Abstract interface for all research ingestion adapters."""

    @abstractmethod
    def fetch_observations(self, query: str, **kwargs: Any) -> List[RawObservation]:
        """Query external engine or fixture and return normalized RawObservation objects."""
        pass
