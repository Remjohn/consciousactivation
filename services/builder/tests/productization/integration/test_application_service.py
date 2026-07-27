from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from cmf_builder.adapters.sqlite_productization_repository import (
    SQLiteProductizationRepository,
)
from cmf_builder.application.productization_contracts import (
    DurableRecord,
    PortableExportRequest,
    PortableExportResult,
    ProductizationCommandRequest,
)
from cmf_builder.application.productization_service import BuilderProductizationService
from cmf_builder.cli.commands import run_cli


ROOT = Path(__file__).resolve().parents[3]


class StubCompiler:
    def compile(self, manifest):
        payload = (
            json.dumps(
                {
                    "artifact_type": "AtomicHarnessDefinition",
                    "manifest_hash": manifest.manifest_hash,
                    "mode": manifest.mode,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        ).encode()
        digest = f"sha256:{sha256(payload).hexdigest()}"
        return DurableRecord(
            record_kind="atomic_harness_definition",
            record_id=f"definition_{digest.removeprefix('sha256:')}",
            version=1,
            payload=payload,
            payload_hash=digest,
        )


class StubExporter:
    def export(self, request: PortableExportRequest) -> PortableExportResult:
        return PortableExportResult(
            package_id=f"package_{request.definition_id}",
            package_hash="sha256:" + "a" * 64,
            destination=request.destination,
            file_hashes=(("definition.json", "sha256:" + "b" * 64),),
            receipt_id=f"export_{request.definition_id}",
        )


def _service(directory: str) -> BuilderProductizationService:
    return BuilderProductizationService(
        repository=SQLiteProductizationRepository(Path(directory) / "builder.sqlite3"),
        compiler=StubCompiler(),
        exporter=StubExporter(),
    )


def test_ingest_build_inspect_and_export_compose_against_frozen_contracts() -> None:
    with TemporaryDirectory() as directory:
        service = _service(directory)
        manifest = ROOT / "tests/fixtures/productization/manifests/generic_text_summary.json"
        ingested = service.execute(
            ProductizationCommandRequest(command="ingest", manifest_path=manifest)
        )
        built = service.execute(
            ProductizationCommandRequest(command="build", artifact_id=ingested.artifact_id)
        )
        inspected = service.execute(
            ProductizationCommandRequest(command="inspect", artifact_id=built.artifact_id)
        )
        exported = service.execute(
            ProductizationCommandRequest(
                command="export",
                artifact_id=built.artifact_id,
                output_path=Path(directory) / "package.zip",
            )
        )

        assert ingested.status == built.status == inspected.status == exported.status == "PASS"
        assert inspected.payload["artifact"]["artifact_type"] == "AtomicHarnessDefinition"
        assert exported.payload["output_name"] == "package.zip"


def test_cli_uses_real_composition_and_durable_idempotency() -> None:
    with TemporaryDirectory() as directory:
        service = _service(directory)
        manifest = ROOT / "tests/fixtures/productization/manifests/generic_text_summary.json"
        from io import StringIO

        first = StringIO()
        second = StringIO()
        assert run_cli(service, ["--format", "json", "ingest", str(manifest)], stdout=first) == 0
        assert run_cli(service, ["--format", "json", "ingest", str(manifest)], stdout=second) == 0
        assert first.getvalue() == second.getvalue()


def test_missing_artifact_fails_through_typed_service_boundary() -> None:
    with TemporaryDirectory() as directory:
        service = _service(directory)
        from cmf_builder.application.productization_contracts import ProductizationError

        try:
            service.execute(ProductizationCommandRequest(command="inspect", artifact_id="missing"))
        except ProductizationError as error:
            assert error.code.value == "NOT_FOUND"
        else:
            raise AssertionError("missing artifact was accepted")
