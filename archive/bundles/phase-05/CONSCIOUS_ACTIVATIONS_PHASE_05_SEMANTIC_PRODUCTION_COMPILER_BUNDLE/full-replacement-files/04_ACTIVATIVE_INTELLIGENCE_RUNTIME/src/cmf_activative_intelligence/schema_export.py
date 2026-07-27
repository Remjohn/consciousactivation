from __future__ import annotations

import json
from pathlib import Path

from ca_contracts import canonical_json_text, canonical_sha256

from .domain import schema_registry


def export_schemas(output_root: Path) -> dict[str, object]:
    output_root.mkdir(parents=True, exist_ok=True)
    registry = schema_registry()
    files: list[dict[str, object]] = []
    for object_type, schema in sorted(registry.items()):
        path = output_root / f"{object_type}.schema.json"
        text = json.dumps(schema, indent=2, sort_keys=True) + "\n"
        path.write_text(text, encoding="utf-8")
        files.append(
            {
                "object_type": object_type,
                "path": path.name,
                "sha256": canonical_sha256(schema),
                "bytes": len(text.encode("utf-8")),
            }
        )
    manifest = {
        "schema_version": "ca-air-semantic-production-schema-export/v1",
        "contract_family": "air-semantic-production",
        "contract_version": "0.3.0-dev.1",
        "authority_state": "candidate_not_current",
        "production_authorized": False,
        "schemas": files,
    }
    (output_root / "SCHEMA_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest
