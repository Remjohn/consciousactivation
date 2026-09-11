from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ca_contracts import canonical_sha256

from ..domain.errors import PipelineValidationError
from ..domain.validation import reject_noncanonical, require_sha, require_string, semantic_identity
from .archive_reader import PortableHarnessPackageReader


class HarnessPackageVerifier:
    REQUIRED_MEMBERS = ("definition.json", "manifest.json", "receipt.json", "SHA256SUMS")

    def __init__(self, reader: PortableHarnessPackageReader | None = None):
        self.reader = reader or PortableHarnessPackageReader()

    def verify(self, path: str | Path) -> dict[str, Any]:
        package_sha, member_tuple = self.reader.read(path)
        members = {item.path: item for item in member_tuple}
        missing = [name for name in self.REQUIRED_MEMBERS if name not in members]
        if missing:
            raise PipelineValidationError(f"harness package missing required members: {missing}")
        if set(members) != set(self.REQUIRED_MEMBERS):
            raise PipelineValidationError("harness package contains undeclared extra members")
        try:
            definition = json.loads(members["definition.json"].content.decode("utf-8"))
            manifest = json.loads(members["manifest.json"].content.decode("utf-8"))
            receipt = json.loads(members["receipt.json"].content.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PipelineValidationError("harness package JSON is invalid") from exc
        reject_noncanonical(definition)
        reject_noncanonical(manifest)
        reject_noncanonical(receipt)
        sums = self._parse_sums(members["SHA256SUMS"].content.decode("utf-8"))
        expected_sum_members = {"definition.json", "manifest.json", "receipt.json"}
        if set(sums) != expected_sum_members:
            raise PipelineValidationError("SHA256SUMS must cover exactly definition, manifest, and receipt")
        for name in expected_sum_members:
            if sums[name] != members[name].sha256:
                raise PipelineValidationError(f"SHA256SUMS mismatch for {name}")
        self._verify_manifest(manifest, members)
        self._verify_receipt(receipt, definition, manifest)
        core = {
            "package_sha256": package_sha,
            "definition_sha256": members["definition.json"].sha256,
            "manifest_sha256": members["manifest.json"].sha256,
            "receipt_sha256": members["receipt.json"].sha256,
            "member_digests": [
                {"path": name, "sha256": members[name].sha256, "byte_length": members[name].byte_length}
                for name in sorted(members)
            ],
        }
        return {
            "package_id": semantic_identity("harness-package", core),
            **core,
            "definition": definition,
            "manifest": manifest,
            "receipt": receipt,
        }

    @staticmethod
    def _parse_sums(text: str) -> dict[str, str]:
        result: dict[str, str] = {}
        for line in text.splitlines():
            if not line.strip():
                continue
            parts = line.split("  ", 1)
            if len(parts) != 2:
                raise PipelineValidationError("invalid SHA256SUMS line")
            digest = require_sha(parts[0], "SHA256SUMS.digest")
            name = require_string(parts[1], "SHA256SUMS.path")
            if name in result:
                raise PipelineValidationError(f"duplicate SHA256SUMS entry: {name}")
            result[name] = digest
        return result

    @staticmethod
    def _verify_manifest(manifest: Mapping[str, Any], members: Mapping[str, Any]) -> None:
        if set(manifest) != {"schema_version", "definition_sha256", "receipt_sha256", "package_profile"}:
            raise PipelineValidationError("manifest contains unknown or missing fields")
        require_string(manifest["schema_version"], "manifest.schema_version")
        if require_sha(manifest["definition_sha256"], "manifest.definition_sha256") != members["definition.json"].sha256:
            raise PipelineValidationError("manifest definition hash mismatch")
        if require_sha(manifest["receipt_sha256"], "manifest.receipt_sha256") != members["receipt.json"].sha256:
            raise PipelineValidationError("manifest receipt hash mismatch")
        require_string(manifest["package_profile"], "manifest.package_profile")

    @staticmethod
    def _verify_receipt(receipt: Mapping[str, Any], definition: Mapping[str, Any], manifest: Mapping[str, Any]) -> None:
        required = {"schema_version", "definition_id", "definition_sha256", "manifest_semantic_sha256", "production_ready", "certified"}
        if set(receipt) != required:
            raise PipelineValidationError("receipt contains unknown or missing fields")
        if receipt["definition_id"] != definition.get("definition_id"):
            raise PipelineValidationError("receipt definition_id mismatch")
        if require_sha(receipt["definition_sha256"], "receipt.definition_sha256") != canonical_sha256(definition):
            raise PipelineValidationError("receipt canonical definition hash mismatch")
        manifest_basis = {
            "schema_version": manifest["schema_version"],
            "definition_sha256": manifest["definition_sha256"],
            "package_profile": manifest["package_profile"],
        }
        if require_sha(receipt["manifest_semantic_sha256"], "receipt.manifest_semantic_sha256") != canonical_sha256(manifest_basis):
            raise PipelineValidationError("receipt manifest semantic hash mismatch")
        if receipt["production_ready"] is not False or receipt["certified"] is not False:
            raise PipelineValidationError("development harness package cannot claim production or certification")
