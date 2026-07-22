"""Canonical registry consolidation service."""

from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ccp_studio.contracts.registry_consolidation import (
    CanonicalRegistryEntry,
    CanonicalRegistryNamespace,
    RegistryConsolidationManifest,
    RegistryCrosswalkEntry,
)


class RegistryConsolidationServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True)
class RegistryConsolidationService:
    manifest_path: Path
    crosswalk_path: Path | None = None

    @classmethod
    def from_project_root(cls, project_root: Path) -> "RegistryConsolidationService":
        registry_root = project_root / "registries" / "canonical" / "registry"
        return cls(
            manifest_path=registry_root / "consolidation_manifest.v1.json",
            crosswalk_path=registry_root / "crosswalk.v1.csv",
        )

    def load_consolidation_manifest(self, manifest_path: Path | None = None) -> RegistryConsolidationManifest:
        path = manifest_path or self.manifest_path
        if not path.exists():
            raise RegistryConsolidationServiceError("CANONICAL_REGISTRY_MANIFEST_MISSING", str(path))
        payload = json.loads(path.read_text(encoding="utf-8"))
        return RegistryConsolidationManifest.model_validate(payload)

    def load_manifest(self) -> RegistryConsolidationManifest:
        return self.load_consolidation_manifest()

    def load_registry_crosswalk(self, crosswalk_path: Path | None = None) -> list[RegistryCrosswalkEntry]:
        path = crosswalk_path or self.crosswalk_path
        if path is not None and path.exists():
            rows = []
            with path.open("r", encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    rows.append(RegistryCrosswalkEntry.model_validate(row))
            return rows
        return list(self.load_consolidation_manifest().crosswalk)

    def entries(self, namespace: CanonicalRegistryNamespace | None = None) -> list[CanonicalRegistryEntry]:
        manifest = self.load_consolidation_manifest()
        if namespace is None:
            return list(manifest.canonical_entries)
        return [entry for entry in manifest.canonical_entries if entry.namespace == namespace]

    def entry_by_id(self, entry_id: str) -> CanonicalRegistryEntry:
        for entry in self.entries():
            if entry.entry_id == entry_id:
                return entry
        raise RegistryConsolidationServiceError("CANONICAL_REGISTRY_ENTRY_NOT_FOUND", entry_id)

    def resolve_canonical_registry_entry(self, source_path: str) -> RegistryCrosswalkEntry:
        for crosswalk in self.load_registry_crosswalk():
            if crosswalk.source_path == source_path:
                return crosswalk
        raise RegistryConsolidationServiceError("REGISTRY_CROSSWALK_NOT_FOUND", source_path)

    def crosswalk_for_source(self, source_path: str) -> RegistryCrosswalkEntry:
        return self.resolve_canonical_registry_entry(source_path)

    def detect_duplicate_registry_entries(self) -> list[str]:
        counts = Counter((entry.namespace.value, entry.entry_id) for entry in self.entries())
        return [f"{namespace}:{entry_id}" for (namespace, entry_id), count in counts.items() if count > 1]

    def validate_registry_namespace(self, namespace: CanonicalRegistryNamespace | str) -> CanonicalRegistryNamespace:
        if isinstance(namespace, CanonicalRegistryNamespace):
            return namespace
        try:
            return CanonicalRegistryNamespace(namespace)
        except ValueError as exc:
            raise RegistryConsolidationServiceError("REGISTRY_NAMESPACE_UNKNOWN", str(namespace)) from exc

    def namespaces_present(self) -> set[CanonicalRegistryNamespace]:
        return {entry.namespace for entry in self.entries()}

    def summarize_registry_consolidation_status(self) -> dict[str, Any]:
        manifest = self.load_consolidation_manifest()
        duplicates = self.detect_duplicate_registry_entries()
        return {
            "source_registry_root": manifest.source_registry_root,
            "canonical_registry_root": manifest.canonical_registry_root,
            "crosswalk_count": len(manifest.crosswalk),
            "canonical_entry_count": len(manifest.canonical_entries),
            "duplicate_entry_count": len(duplicates),
            "duplicates": duplicates,
        }
