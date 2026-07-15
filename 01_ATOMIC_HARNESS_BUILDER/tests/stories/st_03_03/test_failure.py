from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.application.ports import (
    AtomicCommitFailed,
    ConcurrencyConflict,
    IdempotencyPayloadMismatch,
)
from cmf_builder.application.harness_ir_commands import HarnessIRUpstreamInvalid
from cmf_builder.domain.harness_ir import HarnessIRAuthorityRejected
from tests.stories.st_02_05 import reopen_command
from tests.stories.st_03_03 import build_context, compile_command


class HarnessIRFailureTests(unittest.TestCase):
    def test_ac_09_stale_stream_version_fails_without_snapshot(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        with self.assertRaises(ConcurrencyConflict):
            service.compile(compile_command(run_id, expected_version=8))
        self.assertEqual(repository.harness_ir_count, 0)
        self.assertEqual(repository.event_count(run_id), 9)

    def test_ac_09_payload_changed_command_reuse_fails(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        command = compile_command(run_id, command_id="same-command")
        service.compile(command)
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.compile(replace(command, schema_version="2.0.0"))
        self.assertEqual(repository.harness_ir_count, 1)

    def test_ac_09_atomic_failure_has_zero_partial_writes_and_retry_commits_once(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        repository.inject_next_atomic_commit_failure()
        with self.assertRaises(AtomicCommitFailed):
            service.compile(compile_command(run_id))
        self.assertEqual(repository.event_count(run_id), 9)
        self.assertEqual(repository.harness_ir_count, 0)
        self.assertEqual(repository.harness_ir_receipt_count, 0)
        self.assertIsNone(repository.get_command_record("harness-ir-compile-1"))
        service.compile(compile_command(run_id))
        self.assertEqual(repository.harness_ir_count, 1)
        self.assertEqual(repository.harness_ir_receipt_count, 1)

    def test_ac_01_missing_ratification_fails_closed(self) -> None:
        service, _, repository, _, run_id, approval = build_context()
        repository._atomicity_ratifications.pop(approval.ratification_ref)
        with self.assertRaises(HarnessIRUpstreamInvalid):
            service.compile(compile_command(run_id))
        self.assertEqual(repository.harness_ir_count, 0)

    def test_ac_01_reopened_upstream_cannot_compile(self) -> None:
        service, atomicity, repository, _, run_id, _ = build_context()
        atomicity.reopen(reopen_command(run_id))
        with self.assertRaises(HarnessIRUpstreamInvalid):
            service.compile(compile_command(run_id, expected_version=11))
        self.assertEqual(repository.harness_ir_count, 0)

    def test_ac_01_altered_immutable_inputs_fail_closed(self) -> None:
        mutations = (
            ("source_lock", "_source_locks", "source_lock_ref", {"source_profile_hash": "sha256:altered"}),
            ("boundary", "_atomic_boundaries", "boundary_ref", {"boundary": "altered"}),
            ("ratification", "_atomicity_ratifications", "ratification_ref", {"rationale": "altered"}),
            ("model", "_draft_harness_models", "model_ref", {"unresolved_gaps": ("altered",)}),
        )
        for name, repository_field, approval_field, changes in mutations:
            with self.subTest(name=name):
                service, _, repository, _, run_id, approval = build_context(
                    seed=f"altered-{name}"
                )
                collection = getattr(repository, repository_field)
                identity = getattr(approval, approval_field)
                original = collection[identity]
                collection[identity] = replace(original, **changes)
                with self.assertRaises(HarnessIRAuthorityRejected):
                    service.compile(compile_command(run_id))
                self.assertEqual(repository.harness_ir_count, 0)
                self.assertEqual(repository.event_count(run_id), 9)


if __name__ == "__main__":
    unittest.main()
