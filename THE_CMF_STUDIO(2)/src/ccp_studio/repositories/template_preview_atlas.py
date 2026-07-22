from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryTemplatePreviewAtlasRepository:
    atlases: dict[str, Any] = field(default_factory=dict)
    slot_maps: dict[str, Any] = field(default_factory=dict)
    sample_payloads: dict[str, Any] = field(default_factory=dict)
    preview_results: dict[str, Any] = field(default_factory=dict)
    template_versions: dict[str, Any] = field(default_factory=dict)
    approval_receipts: dict[str, Any] = field(default_factory=dict)

    def upsert(self, store_name: str, key: str, value: Any) -> Any:
        getattr(self, store_name)[key] = value
        return value

    def get(self, store_name: str, key: str) -> Any:
        return getattr(self, store_name)[key]
