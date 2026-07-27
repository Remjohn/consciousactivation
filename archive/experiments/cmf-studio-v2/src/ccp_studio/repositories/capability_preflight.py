from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryCapabilityPreflightRepository:
    reports: dict[str, Any] = field(default_factory=dict)
    provider_menus: dict[str, Any] = field(default_factory=dict)
    runtime_reports: dict[str, Any] = field(default_factory=dict)
    setup_offers: dict[str, Any] = field(default_factory=dict)

    def upsert(self, store_name: str, key: str, value: Any) -> Any:
        getattr(self, store_name)[key] = value
        return value

    def get(self, store_name: str, key: str) -> Any:
        return getattr(self, store_name)[key]
