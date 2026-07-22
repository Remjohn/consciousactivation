from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class InMemoryProviderRuntimeRepository:
    capability_profiles: dict[str, Any] = field(default_factory=dict)
    jobs: dict[str, Any] = field(default_factory=dict)
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    receipts: dict[str, Any] = field(default_factory=dict)
    decisions: dict[str, Any] = field(default_factory=dict)
    sample_gates: dict[str, Any] = field(default_factory=dict)
    asset_refs: dict[str, Any] = field(default_factory=dict)
    attempts: dict[str, Any] = field(default_factory=dict)

    def upsert(self, store_name: str, key: str, value: Any) -> Any:
        getattr(self, store_name)[key] = value
        return value
