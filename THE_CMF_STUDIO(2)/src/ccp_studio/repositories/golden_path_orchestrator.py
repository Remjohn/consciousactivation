from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryGoldenPathOrchestratorRepository:
    runs: dict[str, Any] = field(default_factory=dict)
    receipts: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)

    def upsert(self, store_name: str, key: str, value: Any) -> Any:
        getattr(self, store_name)[key] = value
        return value

    def get(self, store_name: str, key: str) -> Any:
        return getattr(self, store_name)[key]
