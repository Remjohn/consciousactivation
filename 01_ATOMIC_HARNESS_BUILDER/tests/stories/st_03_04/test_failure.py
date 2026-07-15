from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.application.ports import AtomicCommitFailed, ConcurrencyConflict, IdempotencyPayloadMismatch
from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.artifact_renderers import _validate_safe_projection
from cmf_builder.domain.generated_artifacts import (
    ArtifactDependencyInvalid,
    ArtifactDependencySelector,
    ArtifactIntegrityInvalid,
    ArtifactInventoryInvalid,
    ArtifactManifest,
    ReproducibleBuildConfigInvalid,
)
from cmf_builder.domain.harness_ir import HarnessIRAuthorityRejected, HarnessIRImmutable
from tests.stories.st_03_04 import BUILD_CONFIG, build_context, compile_command


class ArtifactFailureTests(unittest.TestCase):
    def test_non_code_actor_is_rejected(self) -> None:
        service, _, repository, _, run_id, _, _ = build_context()
        with self.assertRaises(AuthorityDenied):
            service.compile(compile_command(run_id, actor_id="agent-1"))
        self.assertEqual(repository.artifact_manifest_count, 0)

    def test_invalid_reproducible_timestamp_is_rejected(self) -> None:
        service, _, repository, _, run_id, _, _ = build_context()
        bad = replace(BUILD_CONFIG, generation_timestamp="local-time")
        with self.assertRaises(ReproducibleBuildConfigInvalid):
            service.compile(compile_command(run_id, build_config=bad))
        self.assertEqual(repository.generated_artifact_count, 0)

    def test_stale_stream_version_is_rejected_without_mutation(self) -> None:
        service, _, repository, _, run_id, _, _ = build_context()
        with self.assertRaises(ConcurrencyConflict):
            service.compile(compile_command(run_id, expected_version=10))
        self.assertEqual(repository.event_count(run_id), 11)

    def test_changed_payload_reuse_fails_closed(self) -> None:
        service, _, repository, _, run_id, _, _ = build_context()
        service.compile(compile_command(run_id))
        changed = replace(BUILD_CONFIG, generation_timestamp="2026-01-10T12:00:01Z")
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.compile(compile_command(run_id, build_config=changed))
        self.assertEqual(repository.artifact_manifest_count, 1)

    def test_injected_atomic_failure_leaves_zero_partial_state(self) -> None:
        service, _, repository, _, run_id, _, _ = build_context()
        repository.inject_next_atomic_commit_failure()
        with self.assertRaises(AtomicCommitFailed):
            service.compile(compile_command(run_id))
        self.assertEqual(repository.event_count(run_id), 11)
        self.assertEqual(repository.generated_artifact_count, 0)
        self.assertEqual(repository.artifact_manifest_count, 0)
        self.assertEqual(repository.artifact_receipt_count, 0)
        self.assertIsNone(repository.get_command_record("artifact-set-compile-1"))

    def test_altered_harness_ir_fails_integrity_validation(self) -> None:
        service, _, repository, _, run_id, _, ir_receipt = build_context()
        ir = repository.get_harness_ir(ir_receipt.ir_id)
        assert ir is not None
        repository._harness_irs[ir.ir_id] = replace(ir, ir_hash="sha256:altered")
        with self.assertRaises(HarnessIRImmutable):
            service.compile(compile_command(run_id))
        self.assertEqual(repository.artifact_manifest_count, 0)

    def test_incomplete_inventory_is_rejected(self) -> None:
        service, _, repository, _, run_id, _, ir_receipt = build_context()
        receipt = service.compile(compile_command(run_id))
        manifest = repository.get_artifact_manifest(receipt.manifest_id)
        ir = repository.get_harness_ir(ir_receipt.ir_id)
        assert manifest is not None and ir is not None
        with self.assertRaises(ArtifactInventoryInvalid):
            ArtifactManifest.create(ir=ir, config=BUILD_CONFIG, artifacts=manifest.artifacts[:-1])

    def test_undeclared_ir_node_selector_is_rejected(self) -> None:
        _, _, repository, _, _, _, ir_receipt = build_context()
        ir = repository.get_harness_ir(ir_receipt.ir_id)
        assert ir is not None
        with self.assertRaises(ArtifactDependencyInvalid):
            ArtifactDependencySelector("human/product.md", ("missing.path",)).validate(ir)

    def test_cross_artifact_config_conflict_is_rejected(self) -> None:
        service, _, repository, _, run_id, _, ir_receipt = build_context()
        receipt = service.compile(compile_command(run_id))
        manifest = repository.get_artifact_manifest(receipt.manifest_id)
        ir = repository.get_harness_ir(ir_receipt.ir_id)
        assert manifest is not None and ir is not None
        conflicting = (replace(manifest.artifacts[0], config_hash="sha256:conflict"), *manifest.artifacts[1:])
        with self.assertRaises(ArtifactIntegrityInvalid):
            ArtifactManifest.create(ir=ir, config=BUILD_CONFIG, artifacts=conflicting)

    def test_secret_or_external_reference_is_rejected(self) -> None:
        service, _, repository, _, run_id, _, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        manifest = repository.get_artifact_manifest(receipt.manifest_id)
        assert manifest is not None
        for payload in (b'{"secret":"value"}', b'{"url":"https://example.invalid"}'):
            with self.assertRaises(ArtifactIntegrityInvalid):
                _validate_safe_projection(replace(manifest.artifacts[0], content=payload))


if __name__ == "__main__":
    unittest.main()
