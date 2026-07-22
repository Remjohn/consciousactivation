from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryNarrativeStoryDoctorRepository:
    runs: dict[str, Any] = field(default_factory=dict)
    contexts: dict[str, Any] = field(default_factory=dict)
    source_packets: dict[str, Any] = field(default_factory=dict)
    brief_bindings: dict[str, Any] = field(default_factory=dict)
    expected_graphs: dict[str, Any] = field(default_factory=dict)
    beat_maps: dict[str, Any] = field(default_factory=dict)
    expression_inventories: dict[str, Any] = field(default_factory=dict)
    clusters: dict[str, Any] = field(default_factory=dict)
    cluster_graphs: dict[str, Any] = field(default_factory=dict)
    archetype_matrices: dict[str, Any] = field(default_factory=dict)
    archetype_programs: dict[str, Any] = field(default_factory=dict)
    primitive_sets: dict[str, Any] = field(default_factory=dict)
    delivery_recipes: dict[str, Any] = field(default_factory=dict)
    format_matrices: dict[str, Any] = field(default_factory=dict)
    packets: dict[str, Any] = field(default_factory=dict)
    receipts: dict[str, Any] = field(default_factory=dict)

    def upsert(self, store_name: str, key: str, value: Any) -> Any:
        getattr(self, store_name)[key] = value
        return value

    def get(self, store_name: str, key: str) -> Any:
        return getattr(self, store_name)[key]
