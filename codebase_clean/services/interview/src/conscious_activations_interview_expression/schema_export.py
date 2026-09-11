from __future__ import annotations
import json
from pathlib import Path
from .schemas import SCHEMA_NAMES, schema_for

def export_schemas(output: str | Path) -> list[str]:
    target = Path(output)
    target.mkdir(parents=True, exist_ok=True)
    files: list[str] = []
    for name in SCHEMA_NAMES:
        path = target / f"{name}.schema.json"
        path.write_text(json.dumps(schema_for(name), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        files.append(path.name)
    registry = {
        "schema_version": "ca-interview-expression-contract-registry/v1",
        "product": "interview-expression",
        "version": "0.4.0-dev.1",
        "schemas": sorted(files),
        "production_authorized": False,
    }
    registry_path = target / "CONTRACT_REGISTRY.json"
    registry_path.write_text(json.dumps(registry, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    files.append(registry_path.name)
    return sorted(files)
