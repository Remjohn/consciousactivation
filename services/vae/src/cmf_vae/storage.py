from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from ca_contracts import bytes_sha256, canonical_json_text, utc_now_rfc3339

from .errors import VAEError
from .validation import safe_relative


class ContentAddressedStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.objects = self.root / "objects"
        self.metadata = self.root / "metadata"

    def put(self, data: bytes, *, logical_uri: str, media_type: str, metadata: Mapping[str, Any] | None = None) -> dict[str, Any]:
        digest = bytes_sha256(data)
        object_path = self.objects / digest[:2] / digest
        meta_path = self.metadata / f"{digest}.json"
        object_path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata.mkdir(parents=True, exist_ok=True)
        if object_path.exists() and bytes_sha256(object_path.read_bytes()) != digest:
            raise VAEError("content-addressed object tamper detected")
        if not object_path.exists():
            temp = object_path.with_suffix(".tmp")
            temp.write_bytes(data)
            temp.replace(object_path)
        logical = safe_relative(logical_uri, "logical_uri")
        record = {
            "artifact_id": f"artifact:{digest}",
            "artifact_version": "1.0.0",
            "sha256": digest,
            "byte_count": len(data),
            "media_type": media_type,
            "logical_uri": logical,
            "metadata": dict(metadata or {}),
            "created_at_utc": utc_now_rfc3339(),
        }
        if meta_path.exists():
            existing = json.loads(meta_path.read_text(encoding="utf-8"))
            stable_existing = {k:v for k,v in existing.items() if k!="created_at_utc"}
            stable_record = {k:v for k,v in record.items() if k!="created_at_utc"}
            if stable_existing != stable_record:
                raise VAEError("artifact metadata conflict for content digest")
            record = existing
        else:
            meta_path.write_text(canonical_json_text(record)+"\n", encoding="utf-8")
        return {**record, "resource_ref": self.resource_ref(record)}

    def get(self, sha256: str) -> tuple[bytes, dict[str, Any]]:
        object_path = self.objects / sha256[:2] / sha256
        meta_path = self.metadata / f"{sha256}.json"
        if not object_path.is_file() or not meta_path.is_file():
            raise VAEError(f"unknown stored artifact: {sha256}")
        data = object_path.read_bytes()
        if bytes_sha256(data) != sha256:
            raise VAEError("stored artifact byte tamper detected")
        record = json.loads(meta_path.read_text(encoding="utf-8"))
        if record["sha256"] != sha256 or record["byte_count"] != len(data):
            raise VAEError("stored artifact metadata tamper detected")
        return data, record

    @staticmethod
    def resource_ref(record: Mapping[str, Any]) -> dict[str, str]:
        return {
            "resource_id": str(record["artifact_id"]),
            "version": str(record["artifact_version"]),
            "payload_hash": "sha256:" + str(record["sha256"]),
            "canonical_ref": f"cmf-contract://resources/{record['artifact_id']}/{record['artifact_version']}",
        }
