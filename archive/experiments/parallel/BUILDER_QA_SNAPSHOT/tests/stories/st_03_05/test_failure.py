from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.ports import (
    AtomicCommitFailed,
    ConcurrencyConflict,
    IdempotencyPayloadMismatch,
)
from cmf_builder.domain.constitutional_validation import (
    ConstitutionalPolicyInvalid,
)
from cmf_builder.domain.generated_artifacts import ArtifactIntegrityInvalid
from cmf_builder.domain.harness_ir import HarnessIRAuthorityRejected, HarnessIRImmutable
from tests.stories.st_03_05 import build_context, validate_command


class ConstitutionalFailureTests(unittest.TestCase):
    def test_non_code_actors_are_rejected(self) -> None:
        cases = (
            ("architect-1", HarnessIRAuthorityRejected),
            ("agent-1", AuthorityDenied),
            ("external-1", AuthorityDenied),
            ("evaluator-1", AuthorityDenied),
        )
        for actor_id, expected in cases:
            with self.subTest(actor_id=actor_id):
                service, _, repository, _, run_id, _ = build_context(seed=actor_id)
                with self.assertRaises(expected):
                    service.validate(validate_command(run_id, actor_id=actor_id))
                self.assertEqual(repository.constitutional_validation_report_count, 0)

    def test_stale_stream_version_is_rejected_without_mutation(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        with self.assertRaises(ConcurrencyConflict):
            service.validate(validate_command(run_id, expected_version=11))
        self.assertEqual(repository.event_count(run_id), 12)

    def test_changed_command_payload_reuse_is_rejected(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        service.validate(validate_command(run_id))
        changed = replace(
            validate_command(run_id), correlation_id="different-correlation"
        )
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.validate(changed)
        self.assertEqual(repository.constitutional_validation_report_count, 1)

    def test_injected_atomic_failure_leaves_zero_partial_state(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        repository.inject_next_atomic_commit_failure()
        with self.assertRaises(AtomicCommitFailed):
            service.validate(validate_command(run_id))
        self.assertEqual(repository.event_count(run_id), 12)
        self.assertEqual(repository.constitutional_validation_report_count, 0)
        self.assertEqual(repository.constitutional_validation_receipt_count, 0)
        self.assertIsNone(repository.get_command_record("constitutional-validation-1"))
        run = repository.load_run(run_id)
        self.assertIsNone(run.constitutional_validation_ref)

    def test_altered_harness_ir_is_rejected(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        run = repository.load_run(run_id)
        ir = repository.get_harness_ir(run.harness_ir_ref)
        assert ir is not None
        repository._harness_irs[ir.ir_id] = replace(ir, ir_hash="sha256:altered")
        with self.assertRaises(HarnessIRImmutable):
            service.validate(validate_command(run_id))
        self.assertEqual(repository.constitutional_validation_report_count, 0)

    def test_altered_manifest_identity_is_rejected(self) -> None:
        service, _, repository, _, run_id, artifact_receipt = build_context()
        manifest = repository.get_artifact_manifest(artifact_receipt.manifest_id)
        assert manifest is not None
        repository._artifact_manifests[manifest.manifest_id] = replace(
            manifest, manifest_hash="sha256:altered"
        )
        with self.assertRaises(ArtifactIntegrityInvalid):
            service.validate(validate_command(run_id))
        self.assertEqual(repository.constitutional_validation_report_count, 0)

    def test_missing_manifest_is_rejected(self) -> None:
        service, _, repository, _, run_id, artifact_receipt = build_context()
        repository._artifact_manifests.pop(artifact_receipt.manifest_id)
        with self.assertRaises(Exception) as caught:
            service.validate(validate_command(run_id))
        self.assertEqual(
            getattr(caught.exception, "code", ""), "ConstitutionalCommandRejected"
        )
        self.assertEqual(repository.constitutional_validation_report_count, 0)

    def test_mismatched_authority_hashes_are_rejected(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        command = replace(
            validate_command(run_id), constitution_sha256="1" * 64
        )
        with self.assertRaises(ConstitutionalPolicyInvalid):
            service.validate(command)
        self.assertEqual(repository.constitutional_validation_report_count, 0)


if __name__ == "__main__":
    unittest.main()
