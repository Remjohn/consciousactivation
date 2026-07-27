from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

EXPECTED_VERSION = "1.1.0-rc.4"
EXPECTED_DIGEST = "sha256:e616d3f9f24633174658e02a29806eb13c2ce8df6419eeb70a3e6413fb69c281"


class ContractSetError(ValueError):
    pass


def _sha(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


class ContractSet:
    """Exact non-forking reader for the Delegation RC4 release."""

    def __init__(self, release_root: str | Path):
        self.root = Path(release_root).resolve()
        self.contracts_root = self.root / "contracts"
        self.receipt_path = self.root / "RELEASE_RECEIPT.json"
        if not self.receipt_path.is_file():
            raise ContractSetError(f"Delegation release receipt missing: {self.receipt_path}")
        self.receipt = json.loads(self.receipt_path.read_text(encoding="utf-8"))
        self.registry = json.loads((self.contracts_root / "registry.json").read_text(encoding="utf-8"))
        self._entries = {item["message_type"]: item for item in self.registry["messages"]}

    @property
    def version(self) -> str:
        return str(self.receipt["package_version"])

    @property
    def digest(self) -> str:
        return str(self.receipt["release_digest"])

    def verify_release(self) -> dict[str, Any]:
        if self.receipt.get("package_version") != EXPECTED_VERSION:
            raise ContractSetError("unexpected Delegation release version")
        if self.receipt.get("release_digest") != EXPECTED_DIGEST:
            raise ContractSetError("unexpected Delegation release digest")
        normalized: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in self.receipt.get("files", []):
            rel = item["path"]
            if rel in seen or rel.startswith("/") or ".." in Path(rel).parts:
                raise ContractSetError(f"unsafe or duplicate release path: {rel}")
            seen.add(rel)
            path = self.root / rel
            if not path.is_file():
                raise ContractSetError(f"missing Delegation release file: {rel}")
            if path.stat().st_size != item["bytes"] or _sha(path) != item["sha256"]:
                raise ContractSetError(f"Delegation release file mismatch: {rel}")
            normalized.append(item)
        actual_paths = {
            path.relative_to(self.root).as_posix()
            for path in self.root.rglob("*")
            if path.is_file()
            and path.relative_to(self.root).as_posix() != "RELEASE_RECEIPT.json"
            and not any(part in {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"} for part in path.relative_to(self.root).parts)
            and path.suffix not in {".pyc", ".pyo"}
        }
        if seen != actual_paths:
            raise ContractSetError("Delegation release inventory differs from receipt")
        digest_input = json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode("utf-8")
        digest = "sha256:" + hashlib.sha256(digest_input).hexdigest()
        if digest != self.receipt["release_digest"]:
            raise ContractSetError("Delegation release digest recomputation failed")
        manifest = self.contracts_root / "release-manifest.json"
        if _sha(manifest) != self.receipt["release_manifest_sha256"]:
            raise ContractSetError("Delegation release-manifest hash mismatch")
        return {
            "result": "PASS",
            "package": self.receipt["package"],
            "version": self.version,
            "release_digest": self.digest,
            "file_count": len(seen),
            "signature_status": self.receipt["signature_status"],
            "production_authorized": bool(self.receipt["production_authorized"]),
        }

    def entry(self, message_type: str) -> dict[str, Any]:
        try:
            return dict(self._entries[message_type])
        except KeyError as exc:
            raise ContractSetError(f"unknown Delegation message type: {message_type}") from exc

    def schema(self, message_type: str) -> dict[str, Any]:
        entry = self.entry(message_type)
        path = self.root / entry["schema_path"]
        schema = json.loads(path.read_text(encoding="utf-8"))
        observed = _sha(path)
        if observed != entry["schema_hash"]:
            raise ContractSetError(f"schema hash mismatch for {message_type}")
        return schema

    def example(self, message_type: str) -> dict[str, Any]:
        entry = self.entry(message_type)
        path = self.root / entry["example_path"]
        observed = _sha(path)
        if observed != entry["example_hash"]:
            raise ContractSetError(f"example hash mismatch for {message_type}")
        return json.loads(path.read_text(encoding="utf-8"))

    def validate(self, message_type: str, payload: Any) -> None:
        Draft202012Validator(
            self.schema(message_type),
            format_checker=FormatChecker(),
        ).validate(payload)

    def validate_examples(self) -> int:
        count = 0
        for message_type in sorted(self._entries):
            self.validate(message_type, self.example(message_type))
            count += 1
        return count
