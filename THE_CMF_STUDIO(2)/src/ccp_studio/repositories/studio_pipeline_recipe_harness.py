from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass
class InMemoryPipelineRecipeHarnessRepository:
    recipes: dict[str, Any] = field(default_factory=dict)
    runs: dict[str, Any] = field(default_factory=dict)
    receipts: dict[str, Any] = field(default_factory=dict)
    artifacts: dict[str, Any] = field(default_factory=dict)
    summaries: dict[str, Any] = field(default_factory=dict)
    def upsert(self, store_name: str, key: str, value: Any) -> Any:
        getattr(self, store_name)[key] = value
        return value
    def get(self, store_name: str, key: str) -> Any:
        return getattr(self, store_name)[key]
