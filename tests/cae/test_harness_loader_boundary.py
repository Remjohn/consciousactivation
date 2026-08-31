"""Tests for CAE Phase 2 Mandate M15 — Harness Package Loader + Runtime Binding Boundary.

Governed by:
- 00_CONTROL/14_PHASE1_BUILDER_RUNTIME_BINDING_CONTRACT.md
- 00_CONTROL/20_PHASE2_CAE_PI_STATE_MAPPING.md
- 02_PHASE_2_RUNTIME_FOUNDATION/M15_harness_package_loader_runtime_binding.md
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md

Proofs:
1. Real authored Harness package (from manifest and exported zip) loads and binds with workflow/actor/capability metadata intact.
2. Invalid packages fail closed before runtime (generic mode, corrupt zip, altered checksum, missing category binding, non-existent file).
3. Field-level source→binding provenance is recorded across all governed dimensions with cryptographic digests.
4. Full integration with PipelineRepository produces valid execution binding and runtime workflow definitions.
"""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict
import zipfile

import pytest

from ca_contracts import canonical_sha256
from ca_runtime.harness_loader import (
    HarnessBindingAdapter,
    HarnessBindingProvenance,
    HarnessBindingResult,
    HarnessCategoryBindingMissingError,
    HarnessLoaderError,
    HarnessModeNotSupportedError,
    HarnessPackage,
    HarnessPackageCorruptError,
    HarnessPackageLoader,
    HarnessPackageNotFoundError,
    HarnessPackageValidationError,
)
from ca_runtime.pi_adapter import AuthorityLane
from cmf_builder.adapters.sqlite_productization_repository import SQLiteProductizationRepository
from cmf_builder.application.export_service import (
    DeterministicPortableExportService,
    PortableAtomicHarnessCompiler,
)
from cmf_builder.application.manifest_parser import OperatorManifestParser
from cmf_builder.application.productization_contracts import (
    OperatorManifestRequest,
    PortableExportRequest,
    ProductizationCommandRequest,
)
from cmf_builder.application.productization_service import BuilderProductizationService
from cmf_builder.domain.portable_export import PortableAtomicHarnessDefinition
from cmf_pipeline.bindings.eligibility_registry import ImplementationEligibilityRegistry
from cmf_pipeline.workflow.infrastructure.repository import PipelineRepository


FIXTURE_DIR = Path(__file__).resolve().parents[2] / "tests/api/fixtures/harnesses"
ACTIVATIVE_FIXTURE = FIXTURE_DIR / "activative_expression.json"
GENERIC_FIXTURE = FIXTURE_DIR / "generic_text_summary.json"


def _create_real_harness_zip(destination_zip: Path) -> tuple[PortableAtomicHarnessDefinition, Path]:
    """Helper: builds and exports a real activative harness into a portable .zip archive."""
    with TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "builder.sqlite3"
        repo = SQLiteProductizationRepository(db_path)
        exporter = DeterministicPortableExportService(repo)
        service = BuilderProductizationService(
            repository=repo,
            compiler=PortableAtomicHarnessCompiler(),
            exporter=exporter,
        )

        ingested = service.execute(
            ProductizationCommandRequest(
                command="ingest",
                manifest_path=ACTIVATIVE_FIXTURE,
            )
        )
        built = service.execute(
            ProductizationCommandRequest(
                command="build",
                artifact_id=ingested.artifact_id,
            )
        )
        exporter.export(
            PortableExportRequest(
                definition_id=built.artifact_id,
                destination=destination_zip,
            )
        )

        record = repo.get_record("atomic_harness_definition", built.artifact_id)
        assert record is not None
        definition = PortableAtomicHarnessDefinition.from_payload_bytes(record.payload)
        return definition, destination_zip


class TestHarnessPackageLoader:
    def test_load_from_manifest_success(self) -> None:
        """Proof: Real operator manifest compiles directly to verified in-memory HarnessPackage."""
        package = HarnessPackageLoader.load_from_manifest(ACTIVATIVE_FIXTURE)

        assert isinstance(package, HarnessPackage)
        assert package.package_id.startswith("atomic-harness-definition_")
        assert package.definition.content["mode"] == "activative"
        assert package.definition.content["category_binding"]["category_id"] == "conversational_activation_expression"
        assert package.package_sha256 is not None
        assert package.manifest_payload is not None

    def test_load_from_zip_success(self) -> None:
        """Proof: Real exported .zip archive loads, validates checksums, and returns verified HarnessPackage."""
        with TemporaryDirectory() as tmp:
            zip_path = Path(tmp) / "activative_harness.zip"
            original_def, exported_zip = _create_real_harness_zip(zip_path)

            package = HarnessPackageLoader.load_from_zip(exported_zip)

            assert isinstance(package, HarnessPackage)
            assert package.package_id == original_def.definition_id
            assert package.definition.definition_hash == original_def.definition_hash
            assert package.definition.content["mode"] == "activative"
            assert package.manifest_payload is not None
            assert package.receipt_payload is not None

    def test_load_from_definition_object(self) -> None:
        """Proof: Direct PortableAtomicHarnessDefinition encapsulation works cleanly."""
        package_from_manifest = HarnessPackageLoader.load_from_manifest(ACTIVATIVE_FIXTURE)
        package = HarnessPackageLoader.load_from_definition(package_from_manifest.definition)

        assert package.package_id == package_from_manifest.package_id
        assert package.definition == package_from_manifest.definition

    def test_missing_file_raises_not_found(self) -> None:
        """Proof: Non-existent archive or manifest raises HarnessPackageNotFoundError."""
        with pytest.raises(HarnessPackageNotFoundError):
            HarnessPackageLoader.load_from_zip(Path("/nonexistent/harness.zip"))

        with pytest.raises(HarnessPackageNotFoundError):
            HarnessPackageLoader.load_from_manifest(Path("/nonexistent/manifest.json"))

    def test_corrupt_zip_missing_definition_fails_closed(self) -> None:
        """Proof: Archive missing definition file fails closed."""
        with TemporaryDirectory() as tmp:
            corrupt_zip = Path(tmp) / "corrupt.zip"
            with zipfile.ZipFile(corrupt_zip, "w") as zf:
                zf.writestr("random.txt", b"hello world")

            with pytest.raises(HarnessPackageCorruptError) as exc_info:
                HarnessPackageLoader.load_from_zip(corrupt_zip)

            assert "missing definition JSON" in str(exc_info.value)

    def test_corrupt_checksum_fails_closed(self) -> None:
        """Proof: Archive with tampered member failing SHA256SUMS raises HarnessPackageCorruptError."""
        with TemporaryDirectory() as tmp:
            zip_path = Path(tmp) / "tampered.zip"
            original_def, exported_zip = _create_real_harness_zip(zip_path)

            # Modify contents to create a tampered archive
            with zipfile.ZipFile(exported_zip, "r") as zf:
                members = {name: zf.read(name) for name in zf.namelist()}

            # Tamper the manifest
            members["package_manifest.json"] = b'{"tampered": true}\n'
            tampered_zip = Path(tmp) / "tampered_modified.zip"
            with zipfile.ZipFile(tampered_zip, "w") as zf:
                for name, data in members.items():
                    zf.writestr(name, data)

            with pytest.raises(HarnessPackageCorruptError) as exc_info:
                HarnessPackageLoader.load_from_zip(tampered_zip)

            assert "checksum mismatch" in str(exc_info.value)


class TestHarnessRuntimeBindingAdapter:
    def test_real_harness_binds_to_pipeline_intake(self) -> None:
        """Proof: Real authored harness package compiles to 14-key intake projection preserving metadata."""
        package = HarnessPackageLoader.load_from_manifest(ACTIVATIVE_FIXTURE)
        adapter = HarnessBindingAdapter()

        result = adapter.bind_to_pipeline_intake(package)

        assert isinstance(result, HarnessBindingResult)
        assert result.definition_id == package.definition.definition_id
        assert result.intake_projection["definition_id"] == package.definition.definition_id
        assert result.intake_projection["category_id"] == "conversational_activation_expression"
        assert result.intake_projection["profile_id"] == "portable-activative-v1"
        assert result.intake_projection["production_ready"] is False
        assert result.intake_projection["certified"] is False
        assert result.intake_projection["invalidation_state"] == "NOT_INVALIDATED"
        assert len(result.intake_projection["wrong_reading_locks"]) >= 1

        # Check Authority Lanes in workflow
        roles = [node["role"] for node in result.intake_projection["workflow"]["nodes"]]
        assert all(role in [lane.value for lane in AuthorityLane] for role in roles)

    def test_generic_mode_harness_rejected_fail_closed(self) -> None:
        """Proof: Generic non-activative harness fails closed before runtime (Blocker 3)."""
        package = HarnessPackageLoader.load_from_manifest(GENERIC_FIXTURE)
        adapter = HarnessBindingAdapter()

        with pytest.raises(HarnessModeNotSupportedError) as exc_info:
            adapter.bind_to_pipeline_intake(package)

        assert "mode is 'generic'" in str(exc_info.value)

    def test_missing_category_binding_rejected(self) -> None:
        """Proof: Definition missing valid category binding fails closed."""
        from tests.pipeline.test_harness_compiler import _make_definition
        dummy_def = _make_definition(mode="activative")
        mutated_content = dict(dummy_def.content)
        mutated_content["category_binding"] = {}
        mutated_double = type(dummy_def)(
            definition_id=dummy_def.definition_id,
            definition_hash=dummy_def.definition_hash,
            content=mutated_content,
        )

        adapter = HarnessBindingAdapter()
        with pytest.raises(HarnessCategoryBindingMissingError):
            adapter.bind_to_pipeline_intake(mutated_double)

    def test_provenance_recording_is_comprehensive(self) -> None:
        """Proof: Field provenance tracks source-to-binding mappings with digests."""
        package = HarnessPackageLoader.load_from_manifest(ACTIVATIVE_FIXTURE)
        adapter = HarnessBindingAdapter()

        result = adapter.bind_to_pipeline_intake(package)
        provenance = result.provenance

        assert isinstance(provenance, HarnessBindingProvenance)
        assert provenance.definition_id == package.definition.definition_id
        assert provenance.projection_id == result.projection_id
        assert len(provenance.fields) >= 10
        assert provenance.composite_digest is not None

        prov_dict = provenance.to_dict()
        assert prov_dict["field_count"] == len(provenance.fields)
        source_fields = {f["source_field"] for f in prov_dict["fields"]}
        assert "definition_id" in source_fields
        assert "manifest_version" in source_fields
        assert "category_binding.category_id" in source_fields
        assert "goal" in source_fields
        assert "category_binding.wrong_reading_locks" in source_fields
        assert "capability_requirements" in source_fields
        assert "execution_plan" in source_fields
        assert "production_eligible" in source_fields

    def test_full_pipeline_repository_binding_and_workflow_compilation(self) -> None:
        """Proof: End-to-end integration compiles harness into PipelineRepository storage with execution manifest."""
        with TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "pipeline.sqlite3"
            repository = PipelineRepository(db_path)
            repository.initialize()

            eligibility = ImplementationEligibilityRegistry()

            package = HarnessPackageLoader.load_from_manifest(ACTIVATIVE_FIXTURE)
            adapter = HarnessBindingAdapter()

            eligibility.register(
                {
                    "implementation_id": "impl:synthetic-validation",
                    "implementation_version": "1.0.0",
                    "owner_product": "ATOMIC_HARNESS_PIPELINE",
                    "implementation_kind": "DETERMINISTIC_MODULE",
                    "capability_ids": ["activative_contract_validation"],
                    "features": ["canonical_hash", "typed_output"],
                    "side_effect_class": "READ_ONLY",
                    "authority_boundary": "pipeline_owned_execution",
                    "development_eligible": True,
                    "production_authorized": False,
                    "evidence_refs": ["phase3:synthetic-validation"],
                }
            )
            eligibility.register(
                {
                    "implementation_id": "impl:synthetic-lineage",
                    "implementation_version": "1.0.0",
                    "owner_product": "ATOMIC_HARNESS_PIPELINE",
                    "implementation_kind": "DETERMINISTIC_MODULE",
                    "capability_ids": ["lineage_preservation"],
                    "features": ["canonical_hash", "typed_output"],
                    "side_effect_class": "LOCAL_STATE_WRITE",
                    "authority_boundary": "pipeline_owned_execution",
                    "development_eligible": True,
                    "production_authorized": False,
                    "evidence_refs": ["phase3:synthetic-lineage"],
                }
            )

            result = adapter.bind_to_pipeline_intake(
                package,
                pipeline_repository=repository,
                eligibility_registry=eligibility,
                idempotency_key="m15-test-binding",
            )

            assert result.binding_manifest is not None
            assert result.binding_manifest["execution_eligible"] is True
            assert result.binding_manifest["manifest_id"].startswith("harness-binding:")
            assert len(result.binding_manifest["bindings"]) == 2

            assert result.runtime_workflow is not None
            assert result.runtime_workflow["workflow_id"].startswith("runtime-workflow:")
            assert len(result.runtime_workflow["nodes"]) == 2
            assert result.runtime_workflow["nodes"][0]["role"] == AuthorityLane.HUNTER.value
            assert result.runtime_workflow["nodes"][1]["role"] == AuthorityLane.COMPOSER.value
