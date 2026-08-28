"""
adapters
--------
Adapters for external search, social, and research fixtures.
"""

from .base import BaseResearchAdapter
from .searxng_adapter import SearXNGAdapter
from .last30days_adapter import Last30DaysAdapter
from .fixture_adapter import FixtureResearchAdapter

__all__ = [
    "BaseResearchAdapter",
    "SearXNGAdapter",
    "Last30DaysAdapter",
    "FixtureResearchAdapter",
]
