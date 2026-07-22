from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryFormatIntelligenceRepository:
    contexts: dict[str, Any] = field(default_factory=dict)
    extraction_packets: dict[str, Any] = field(default_factory=dict)
    activation_decisions: dict[str, Any] = field(default_factory=dict)
    sub_format_routes: dict[str, Any] = field(default_factory=dict)
    programs: dict[str, Any] = field(default_factory=dict)
    verdicts: dict[str, Any] = field(default_factory=dict)
    adapter_payloads: dict[str, Any] = field(default_factory=dict)

    def upsert(self, store_name: str, key: str, value: Any) -> Any:
        getattr(self, store_name)[key] = value
        return value

    def get(self, store_name: str, key: str) -> Any:
        return getattr(self, store_name)[key]
