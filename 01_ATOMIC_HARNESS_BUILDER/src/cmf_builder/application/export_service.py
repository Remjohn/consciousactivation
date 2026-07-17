from __future__ import annotations

from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
import zipfile

from cmf_builder.application.productization_contracts import (
    DurableProductizationRepository,
    DurableRecord,
    OperatorManifestResult,
    PortableExportRequest,
    PortableExportResult,
    ProductizationError,
    ProductizationErrorCode,
)
from cmf_builder.domain.portable_export import (
    PortableAtomicHarnessDefinition,
    PortableDefinitionInvalid,
)
from cmf_builder.domain.category_binding import CategoryBinding, CategoryBindingError


_CATEGORY_REGISTRY = (
    Path(__file__).resolve().parents[3] / "governance" / "CANONICAL_CATEGORY_REGISTRY.yaml"
)


class PortableAtomicHarnessCompiler:
    def compile(self, manifest: OperatorManifestResult) -> DurableRecord:
        try:
            binding = CategoryBinding.create(
                harness_id=manifest.task_id,
                harness_version=manifest.manifest_version,
                mode=manifest.mode,
                category_ids=(manifest.category_id,) if manifest.category_id else (),
                activative_input=(
                    manifest.normalized.get("activative_input")
                    if manifest.mode == "activative"
                    else None
                ),
                registry_bytes=_CATEGORY_REGISTRY.read_bytes(),
            )
            definition = PortableAtomicHarnessDefinition.create(
                manifest_id=manifest.manifest_id,
                manifest_version=manifest.manifest_version,
                manifest_hash=manifest.manifest_hash,
                task_id=manifest.task_id,
                mode=manifest.mode,
                normalized=manifest.normalized,
                category_binding=binding.portable_projection(),
            )
        except (PortableDefinitionInvalid, CategoryBindingError, OSError) as error:
            raise ProductizationError(
                ProductizationErrorCode.INVALID_MANIFEST,
                str(error),
            ) from error
        payload_hash = f"sha256:{sha256(definition.payload_bytes).hexdigest()}"
        return DurableRecord(
            record_kind="atomic_harness_definition",
            record_id=definition.definition_id,
            version=1,
            payload=definition.payload_bytes,
            payload_hash=payload_hash,
        )


class DeterministicPortableExportService:
    def __init__(self, repository: DurableProductizationRepository) -> None:
        self._repository = repository
        self._fail_before_replace = False

    def inject_failure_before_replace(self) -> None:
        self._fail_before_replace = True

    def export(self, request: PortableExportRequest) -> PortableExportResult:
        record = self._repository.get_record(
            "atomic_harness_definition", request.definition_id
        )
        if record is None:
            raise ProductizationError(
                ProductizationErrorCode.NOT_FOUND,
                "AtomicHarnessDefinition is unavailable for export.",
                context={"definition_id": request.definition_id},
            )
        try:
            definition = PortableAtomicHarnessDefinition.from_payload_bytes(record.payload)
        except PortableDefinitionInvalid as error:
            raise ProductizationError(
                ProductizationErrorCode.HASH_MISMATCH,
                str(error),
                context={"definition_id": request.definition_id},
            ) from error
        if definition.definition_id != record.record_id:
            raise ProductizationError(
                ProductizationErrorCode.HASH_MISMATCH,
                "Stored definition identity differs from its payload.",
            )

        definition_path = "atomic_harness_definition.json"
        definition_hash = _hash(record.payload)
        manifest_bytes = _canonical_json(
            {
                "schema_version": "cmf-builder-portable-package-manifest/v1",
                "definition_id": definition.definition_id,
                "definition_hash": definition.definition_hash,
                "definition_record_hash": definition_hash,
                "mode": definition.content["mode"],
                "files": [{"path": definition_path, "sha256": definition_hash}],
                "portable": True,
                "production_eligible": False,
                "certified": False,
            }
        )
        manifest_hash = _hash(manifest_bytes)
        content_package_hash = _hash(
            definition_path.encode() + record.payload + manifest_bytes
        )
        receipt_base = {
            "schema_version": "cmf-builder-portable-export-receipt/v1",
            "definition_id": definition.definition_id,
            "definition_hash": definition.definition_hash,
            "content_package_hash": content_package_hash,
            "file_hashes": [
                [definition_path, definition_hash],
                ["package_manifest.json", manifest_hash],
            ],
            "production_eligible": False,
            "certified": False,
            "outcome": "PORTABLE_NONPRODUCTION_PACKAGE_EXPORTED",
        }
        receipt_digest = sha256(_canonical_json(receipt_base)).hexdigest()
        receipt_id = f"portable-export-receipt_{receipt_digest}"
        receipt_bytes = _canonical_json(
            {**receipt_base, "receipt_id": receipt_id, "receipt_hash": f"sha256:{receipt_digest}"}
        )
        files = {
            definition_path: record.payload,
            "package_manifest.json": manifest_bytes,
            "export_receipt.json": receipt_bytes,
        }
        sums = "".join(
            f"{_hash(content).removeprefix('sha256:')}  {name}\n"
            for name, content in sorted(files.items())
        ).encode("utf-8")
        files["SHA256SUMS"] = sums
        archive_bytes = _deterministic_zip(files)
        archive_hash = _hash(archive_bytes)
        destination = request.destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".tmp")
        try:
            temporary.write_bytes(archive_bytes)
            if self._fail_before_replace:
                self._fail_before_replace = False
                raise ProductizationError(
                    ProductizationErrorCode.EXPORT_REJECTED,
                    "Injected portable export failure.",
                )
            os.replace(temporary, destination)
        except Exception:
            if temporary.exists():
                temporary.unlink()
            raise
        return PortableExportResult(
            package_id=f"atomic-harness-package_{content_package_hash.removeprefix('sha256:')}",
            package_hash=archive_hash,
            destination=destination,
            file_hashes=tuple(
                (name, _hash(content)) for name, content in sorted(files.items())
            ),
            receipt_id=receipt_id,
        )


def _deterministic_zip(files: dict[str, bytes]) -> bytes:
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    return buffer.getvalue()


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")


def _hash(content: bytes) -> str:
    return f"sha256:{sha256(content).hexdigest()}"
