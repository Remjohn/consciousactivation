from __future__ import annotations

import json
from pathlib import Path

REGISTRY_PATH = Path("docs/implementation/offline-development/SOURCE_BOUNDARY_REGISTRY.yaml")


def load_source_boundary_registry(root: Path) -> dict[str, object]:
    registry = json.loads((root / REGISTRY_PATH).read_text(encoding="utf-8"))
    if registry.get("schema_version") != "cmf-builder-source-boundary-registry/v1":
        raise AssertionError("unsupported source-boundary registry schema")
    sources = registry.get("sources")
    if not isinstance(sources, list) or not sources:
        raise AssertionError("source-boundary registry has no sources")
    paths: list[str] = []
    for item in sources:
        if not isinstance(item, dict):
            raise AssertionError("invalid source-boundary registry entry")
        path = item.get("path")
        owner = item.get("owner_package")
        if not isinstance(path, str) or not path.startswith("src/cmf_builder/"):
            raise AssertionError(f"invalid registered source path: {path!r}")
        expected_owner = (
            "cmf_builder"
            if path == "src/cmf_builder/__init__.py"
            else f"cmf_builder.{path.split('/')[2]}"
        )
        if owner != expected_owner:
            raise AssertionError(f"missing package ownership for {path}")
        paths.append(path)
    if len(paths) != len(set(paths)):
        raise AssertionError("duplicate registered source path")
    return registry


def registered_source_files(root: Path) -> set[str]:
    registry = load_source_boundary_registry(root)
    return {item["path"] for item in registry["sources"]}  # type: ignore[index]
