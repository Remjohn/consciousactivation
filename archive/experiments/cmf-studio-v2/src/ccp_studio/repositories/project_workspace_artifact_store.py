from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryProjectWorkspaceArtifactStoreRepository:
    workspaces: dict[str, Any] = field(default_factory=dict)
    folder_maps: dict[str, Any] = field(default_factory=dict)
    run_directories: dict[str, Any] = field(default_factory=dict)
    artifact_refs: dict[str, Any] = field(default_factory=dict)
    artifact_versions: dict[str, Any] = field(default_factory=dict)
    manifests: dict[str, Any] = field(default_factory=dict)
    lineages: dict[str, Any] = field(default_factory=dict)
    receipts: dict[str, Any] = field(default_factory=dict)
    materialization_receipts: dict[str, Any] = field(default_factory=dict)

    def upsert(self, store_name: str, key: str, value: Any) -> Any:
        getattr(self, store_name)[key] = value
        return value

    def get(self, store_name: str, key: str) -> Any:
        return getattr(self, store_name)[key]
