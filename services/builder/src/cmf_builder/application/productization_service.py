from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Protocol

from cmf_builder.application.manifest_parser import OperatorManifestParser
from cmf_builder.application.productization_contracts import (
    DurableCommandReceipt,
    DurableProductizationRepository,
    DurableRecord,
    OperatorManifestRequest,
    OperatorManifestResult,
    PortableExportRequest,
    PortableExportService,
    ProductizationCommandRequest,
    ProductizationCommandResult,
    ProductizationError,
    ProductizationErrorCode,
)


class ProductizationDefinitionCompiler(Protocol):
    def compile(self, manifest: OperatorManifestResult) -> DurableRecord: ...


class BuilderProductizationService:
    """Compose the frozen manifest, durability, CLI, compiler and export seams."""

    def __init__(
        self,
        *,
        repository: DurableProductizationRepository,
        compiler: ProductizationDefinitionCompiler,
        exporter: PortableExportService,
        parser: OperatorManifestParser | None = None,
    ) -> None:
        self._repository = repository
        self._compiler = compiler
        self._exporter = exporter
        self._parser = parser or OperatorManifestParser()
        self._repository.initialize()

    def execute(self, request: ProductizationCommandRequest) -> ProductizationCommandResult:
        if request.command == "ingest":
            return self._ingest(request)
        if request.command == "build":
            return self._build(request)
        if request.command == "inspect":
            return self._inspect(request)
        if request.command == "export":
            return self._export(request)
        raise ProductizationError(
            ProductizationErrorCode.INVALID_MANIFEST,
            "The requested Builder command is not governed.",
            context={"command": request.command},
        )

    def _ingest(self, request: ProductizationCommandRequest) -> ProductizationCommandResult:
        path = self._required_path(request.manifest_path, "manifest_path")
        try:
            content = path.read_bytes()
        except OSError as error:
            raise ProductizationError(
                ProductizationErrorCode.NOT_FOUND,
                "Operator manifest is unavailable.",
                context={"source_name": path.name},
            ) from error
        manifest = self._parser.parse(
            OperatorManifestRequest(manifest_bytes=content, source_name=path.name)
        )
        record = DurableRecord(
            record_kind="operator_manifest",
            record_id=manifest.manifest_id,
            version=1,
            payload=manifest.canonical_bytes,
            payload_hash=manifest.manifest_hash,
        )
        command_id = f"ingest_{manifest.manifest_hash.removeprefix('sha256:')}"
        receipt = DurableCommandReceipt(
            command_id=command_id,
            payload_hash=manifest.manifest_hash,
            result_kind=record.record_kind,
            result_id=record.record_id,
            result_hash=record.payload_hash,
        )
        committed = self._repository.commit_record(
            record, command_receipt=receipt, expected_version=None
        )
        return ProductizationCommandResult(
            command="ingest",
            status="PASS",
            artifact_id=record.record_id,
            artifact_hash=record.payload_hash,
            receipt_id=committed.command_id,
            payload={
                "manifest_id": manifest.manifest_id,
                "manifest_version": manifest.manifest_version,
                "mode": manifest.mode,
                "task_id": manifest.task_id,
            },
        )

    def _build(self, request: ProductizationCommandRequest) -> ProductizationCommandResult:
        artifact_id = self._required_text(request.artifact_id, "artifact_id")
        source = self._repository.get_record("operator_manifest", artifact_id)
        if source is None:
            raise ProductizationError(
                ProductizationErrorCode.NOT_FOUND,
                "A governed operator manifest was not found.",
                context={"artifact_id": artifact_id},
            )
        manifest = self._parser.parse(
            OperatorManifestRequest(
                manifest_bytes=source.payload,
                source_name=f"{source.record_id}.canonical.json",
            )
        )
        definition = self._compiler.compile(manifest)
        if definition.record_kind != "atomic_harness_definition":
            raise ProductizationError(
                ProductizationErrorCode.INTERNAL_ERROR,
                "The compiler returned an unauthorized artifact kind.",
            )
        command_payload = _canonical_json(
            {"command": "build", "manifest_hash": manifest.manifest_hash}
        )
        receipt = DurableCommandReceipt(
            command_id=f"build_{sha256(command_payload).hexdigest()}",
            payload_hash=f"sha256:{sha256(command_payload).hexdigest()}",
            result_kind=definition.record_kind,
            result_id=definition.record_id,
            result_hash=definition.payload_hash,
        )
        committed = self._repository.commit_record(
            definition, command_receipt=receipt, expected_version=None
        )
        return ProductizationCommandResult(
            command="build",
            status="PASS",
            artifact_id=definition.record_id,
            artifact_hash=definition.payload_hash,
            receipt_id=committed.command_id,
            payload={"manifest_id": manifest.manifest_id, "mode": manifest.mode},
        )

    def _inspect(self, request: ProductizationCommandRequest) -> ProductizationCommandResult:
        artifact_id = self._required_text(request.artifact_id, "artifact_id")
        record = self._repository.get_record("atomic_harness_definition", artifact_id)
        if record is None:
            record = self._repository.get_record("operator_manifest", artifact_id)
        if record is None:
            raise ProductizationError(
                ProductizationErrorCode.NOT_FOUND,
                "The requested Builder artifact was not found.",
                context={"artifact_id": artifact_id},
            )
        try:
            payload = json.loads(record.payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ProductizationError(
                ProductizationErrorCode.STORAGE_INTEGRITY,
                "Stored artifact bytes are not canonical JSON.",
                context={"artifact_id": artifact_id},
            ) from error
        return ProductizationCommandResult(
            command="inspect",
            status="PASS",
            artifact_id=record.record_id,
            artifact_hash=record.payload_hash,
            receipt_id=None,
            payload={"record_kind": record.record_kind, "artifact": payload},
        )

    def _export(self, request: ProductizationCommandRequest) -> ProductizationCommandResult:
        artifact_id = self._required_text(request.artifact_id, "artifact_id")
        output = self._required_path(request.output_path, "output_path")
        result = self._exporter.export(
            PortableExportRequest(definition_id=artifact_id, destination=output)
        )
        return ProductizationCommandResult(
            command="export",
            status="PASS",
            artifact_id=result.package_id,
            artifact_hash=result.package_hash,
            receipt_id=result.receipt_id,
            payload={
                "definition_id": artifact_id,
                "file_hashes": [list(item) for item in result.file_hashes],
                "output_name": result.destination.name,
            },
        )

    @staticmethod
    def _required_text(value: str | None, field: str) -> str:
        if value is None or not value.strip():
            raise ProductizationError(
                ProductizationErrorCode.INVALID_MANIFEST,
                "A required command field is missing.",
                field_path=field,
            )
        return value.strip()

    @staticmethod
    def _required_path(value: Path | None, field: str) -> Path:
        if value is None:
            raise ProductizationError(
                ProductizationErrorCode.INVALID_MANIFEST,
                "A required command path is missing.",
                field_path=field,
            )
        return value


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
