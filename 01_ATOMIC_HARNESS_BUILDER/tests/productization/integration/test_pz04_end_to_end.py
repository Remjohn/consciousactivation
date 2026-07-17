from __future__ import annotations

from io import BytesIO, StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import zipfile

import pytest

from cmf_builder.adapters.sqlite_productization_repository import (
    SQLiteProductizationRepository,
)
from cmf_builder.application.export_service import (
    DeterministicPortableExportService,
    PortableAtomicHarnessCompiler,
)
from cmf_builder.application.manifest_parser import OperatorManifestParser
from cmf_builder.application.productization_contracts import (
    OperatorManifestRequest,
    PortableExportRequest,
    ProductizationCommandRequest,
    ProductizationError,
)
from cmf_builder.application.productization_service import BuilderProductizationService
from cmf_builder.cli.commands import run_cli
from cmf_builder.domain.portable_export import PortableAtomicHarnessDefinition


ROOT = Path(__file__).resolve().parents[3]
GENERIC = ROOT / "tests/fixtures/productization/manifests/generic_text_summary.json"
ACTIVATIVE = ROOT / "tests/fixtures/productization/manifests/activative_expression.json"


def _parse(path: Path):
    return OperatorManifestParser().parse(
        OperatorManifestRequest(manifest_bytes=path.read_bytes(), source_name=path.name)
    )


def _service(directory: Path):
    repository = SQLiteProductizationRepository(directory / "builder.sqlite3")
    exporter = DeterministicPortableExportService(repository)
    service = BuilderProductizationService(
        repository=repository,
        compiler=PortableAtomicHarnessCompiler(),
        exporter=exporter,
    )
    return service, repository, exporter


def test_generic_and_activative_compile_to_deterministic_atomic_harness_definitions() -> None:
    compiler = PortableAtomicHarnessCompiler()
    generic = compiler.compile(_parse(GENERIC))
    activative = compiler.compile(_parse(ACTIVATIVE))
    repeated = compiler.compile(_parse(GENERIC))

    assert generic == repeated
    assert generic.record_id != activative.record_id
    generic_definition = PortableAtomicHarnessDefinition.from_payload_bytes(generic.payload)
    activative_definition = PortableAtomicHarnessDefinition.from_payload_bytes(activative.payload)
    assert generic_definition.content["activative_intelligence"] is None
    assert activative_definition.content["mode"] == "activative"
    assert activative_definition.content["activative_intelligence"]["identity_dna_ref"]
    assert activative_definition.content["external_skills_required"] == 0


def test_activative_intelligence_remains_structured_and_human_identity_is_reference_only() -> None:
    record = PortableAtomicHarnessCompiler().compile(_parse(ACTIVATIVE))
    definition = PortableAtomicHarnessDefinition.from_payload_bytes(record.payload)
    activative = definition.content["activative_intelligence"]
    assert set(activative) >= {
        "activative_intelligence_pack_ref",
        "identity_dna_ref",
        "context_premise_ref",
        "resonance_map_ref",
        "matrix_of_edging_ref",
        "wrong_reading_locks",
        "reaction_receipt_refs",
        "expression_moment_refs",
    }
    assert "identity_dna" not in activative
    assert "notes" not in activative


def test_changed_governed_input_produces_new_definition_identity() -> None:
    original = GENERIC.read_bytes()
    changed = original.replace(b'"task_id": "generic_text_summary_v1"', b'"task_id": "generic_text_summary_v2"')
    parser = OperatorManifestParser()
    first = PortableAtomicHarnessCompiler().compile(
        parser.parse(OperatorManifestRequest(original, GENERIC.name))
    )
    second = PortableAtomicHarnessCompiler().compile(
        parser.parse(OperatorManifestRequest(changed, GENERIC.name))
    )
    assert first.record_id != second.record_id
    assert first.payload_hash != second.payload_hash


def test_real_cli_ingest_build_inspect_and_export_generic_and_activative() -> None:
    with TemporaryDirectory() as directory_text:
        directory = Path(directory_text)
        service, _, _ = _service(directory)
        for source in (GENERIC, ACTIVATIVE):
            ingest_out = StringIO()
            assert run_cli(service, ["--format", "json", "ingest", str(source)], stdout=ingest_out) == 0
            manifest_id = json.loads(ingest_out.getvalue())["artifact_id"]
            build_out = StringIO()
            assert run_cli(service, ["--format", "json", "build", "--artifact-id", manifest_id], stdout=build_out) == 0
            definition_id = json.loads(build_out.getvalue())["artifact_id"]
            inspect_out = StringIO()
            assert run_cli(service, ["--format", "json", "inspect", "--artifact-id", definition_id], stdout=inspect_out) == 0
            assert json.loads(inspect_out.getvalue())["payload"]["artifact"]["artifact_type"] == "AtomicHarnessDefinition"
            output = directory / f"{source.stem}.zip"
            assert run_cli(
                service,
                ["--format", "json", "export", "--artifact-id", definition_id, "--output", str(output)],
                stdout=StringIO(),
            ) == 0
            assert output.is_file()


def test_portable_export_is_byte_identical_and_contains_only_relative_canonical_paths() -> None:
    with TemporaryDirectory() as directory_text:
        directory = Path(directory_text)
        service, _, exporter = _service(directory)
        ingested = service.execute(ProductizationCommandRequest(command="ingest", manifest_path=ACTIVATIVE))
        built = service.execute(ProductizationCommandRequest(command="build", artifact_id=ingested.artifact_id))
        first = exporter.export(PortableExportRequest(built.artifact_id, directory / "first.zip"))
        second = exporter.export(PortableExportRequest(built.artifact_id, directory / "second.zip"))
        assert first.package_hash == second.package_hash
        assert first.destination.read_bytes() == second.destination.read_bytes()
        with zipfile.ZipFile(BytesIO(first.destination.read_bytes())) as archive:
            assert archive.namelist() == sorted(archive.namelist())
            assert all(not Path(name).is_absolute() and ".." not in Path(name).parts for name in archive.namelist())
            joined = b"\n".join(archive.read(name) for name in archive.namelist()).lower()
            assert b'"production_eligible":true' not in joined
            assert b'"certified":true' not in joined
            assert b":/" not in joined and b"\\\\" not in joined


def test_export_failure_rolls_back_without_replacing_existing_package() -> None:
    with TemporaryDirectory() as directory_text:
        directory = Path(directory_text)
        service, _, exporter = _service(directory)
        ingested = service.execute(ProductizationCommandRequest(command="ingest", manifest_path=GENERIC))
        built = service.execute(ProductizationCommandRequest(command="build", artifact_id=ingested.artifact_id))
        destination = directory / "package.zip"
        destination.write_bytes(b"historical-package")
        exporter.inject_failure_before_replace()
        with pytest.raises(ProductizationError):
            exporter.export(PortableExportRequest(built.artifact_id, destination))
        assert destination.read_bytes() == b"historical-package"
        assert not destination.with_name("package.zip.tmp").exists()


def test_durable_state_resumes_in_fresh_service_context() -> None:
    with TemporaryDirectory() as directory_text:
        directory = Path(directory_text)
        first, _, _ = _service(directory)
        ingested = first.execute(ProductizationCommandRequest(command="ingest", manifest_path=GENERIC))
        built = first.execute(ProductizationCommandRequest(command="build", artifact_id=ingested.artifact_id))
        second, _, _ = _service(directory)
        inspected = second.execute(ProductizationCommandRequest(command="inspect", artifact_id=built.artifact_id))
        assert inspected.artifact_hash == built.artifact_hash


def test_altered_definition_bytes_fail_closed_before_export() -> None:
    record = PortableAtomicHarnessCompiler().compile(_parse(GENERIC))
    altered = record.payload.replace(b"uncertified_nonproduction", b"production_certified_status")
    with pytest.raises(Exception):
        PortableAtomicHarnessDefinition.from_payload_bytes(altered)
