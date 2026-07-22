from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryVideoEditingEngineRepository:
    projects: dict[str, Any] = field(default_factory=dict)
    variants: dict[str, Any] = field(default_factory=dict)
    source_asset_sets: dict[str, Any] = field(default_factory=dict)
    media_probe_receipts: dict[str, Any] = field(default_factory=dict)
    scene_realization_plans: dict[str, Any] = field(default_factory=dict)
    timeline_programs: dict[str, Any] = field(default_factory=dict)
    render_contracts: dict[str, Any] = field(default_factory=dict)
    render_receipts: dict[str, Any] = field(default_factory=dict)
    eval_receipts: dict[str, Any] = field(default_factory=dict)
    revision_receipts: dict[str, Any] = field(default_factory=dict)
    export_packs: dict[str, Any] = field(default_factory=dict)
    approval_packets: dict[str, Any] = field(default_factory=dict)

    def upsert(self, store_name: str, key: str, value: Any) -> Any:
        getattr(self, store_name)[key] = value
        return value

    def get(self, store_name: str, key: str) -> Any:
        return getattr(self, store_name)[key]
