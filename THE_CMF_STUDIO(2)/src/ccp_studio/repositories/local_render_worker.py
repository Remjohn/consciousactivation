from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryLocalRenderWorkerRepository:
    workers: dict[str, Any] = field(default_factory=dict)
    queues: dict[str, Any] = field(default_factory=dict)
    jobs: dict[str, Any] = field(default_factory=dict)
    leases: dict[str, Any] = field(default_factory=dict)
    heartbeats: dict[str, Any] = field(default_factory=dict)
    results: dict[str, Any] = field(default_factory=dict)
    health_receipts: dict[str, Any] = field(default_factory=dict)

    def upsert(self, store_name: str, key: str, value: Any) -> Any:
        getattr(self, store_name)[key] = value
        return value

    def get(self, store_name: str, key: str) -> Any:
        return getattr(self, store_name)[key]
