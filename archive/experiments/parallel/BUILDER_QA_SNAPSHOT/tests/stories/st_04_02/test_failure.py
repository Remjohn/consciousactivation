from __future__ import annotations

import unittest

from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.module_commands import ModuleCommandRejected
from cmf_builder.application.ports import (
    AtomicCommitFailed,
    ConcurrencyConflict,
    IdempotencyPayloadMismatch,
)
from cmf_builder.domain.responsibility_modules import ModuleInputInvalid
from tests.stories.st_04_02 import build_context, compile_command


class ResponsibilityModuleFailureTests(unittest.TestCase):
    def test_non_code_writer_is_rejected_without_partial_state(self) -> None:
        service, _, repository, observations, run_id, _ = build_context()
        with self.assertRaises(AuthorityDenied):
            service.compile(compile_command(run_id, actor_id="agent-1"))
        self.assertEqual(repository.event_count(run_id), 14)
        self.assertEqual(repository.responsibility_module_graph_count, 0)
        self.assertEqual(repository.responsibility_module_receipt_count, 0)
        self.assertEqual(observations.observations[-1].event_name, "ST-04.02:OutcomeRejected")

    def test_missing_actor_authority_is_rejected(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        with self.assertRaises(AuthorityDenied):
            service.compile(compile_command(run_id, actor_id="unknown-actor"))
        self.assertEqual(repository.event_count(run_id), 14)
        self.assertEqual(repository.responsibility_module_graph_count, 0)

    def test_stale_stream_version_is_rejected_without_partial_state(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        with self.assertRaises(ConcurrencyConflict):
            service.compile(compile_command(run_id, expected_version=13))
        self.assertEqual(repository.event_count(run_id), 14)
        self.assertEqual(repository.responsibility_module_graph_count, 0)

    def test_arbitrary_path_or_hash_drift_is_rejected(self) -> None:
        cases = (
            {"module_input_path": "development-capsules/ST-04.02/OTHER.json"},
            {"module_input_sha256": "0" * 64},
        )
        for change in cases:
            with self.subTest(change=change):
                service, _, repository, _, run_id, _ = build_context()
                with self.assertRaises(ModuleInputInvalid):
                    service.compile(compile_command(run_id, **change))
                self.assertEqual(repository.responsibility_module_graph_count, 0)

    def test_injected_atomic_failure_leaves_zero_partial_state(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        repository.inject_next_atomic_commit_failure()
        command = compile_command(run_id)
        with self.assertRaises(AtomicCommitFailed):
            service.compile(command)
        self.assertEqual(repository.event_count(run_id), 14)
        self.assertEqual(repository.responsibility_module_graph_count, 0)
        self.assertEqual(repository.responsibility_module_receipt_count, 0)
        self.assertIsNone(repository.get_command_record(command.command_id))

    def test_reused_command_with_changed_payload_fails_closed(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        service.compile(compile_command(run_id))
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.compile(compile_command(run_id, actor_id="agent-1"))
        self.assertEqual(repository.event_count(run_id), 15)
        self.assertEqual(repository.responsibility_module_graph_count, 1)

    def test_invalidated_capability_parent_cannot_compile_modules(self) -> None:
        service, atomicity, repository, _, run_id, capability_receipt = build_context()
        atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-before-modules",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=14,
                correlation_id="reopen-correlation",
                causation_id=capability_receipt.receipt_id,
                reason="Authorized parent invalidation test.",
            )
        )
        with self.assertRaises(ModuleCommandRejected):
            service.compile(
                compile_command(
                    run_id,
                    command_id="compile-after-invalidation",
                    expected_version=20,
                )
            )
        self.assertEqual(repository.responsibility_module_graph_count, 0)


if __name__ == "__main__":
    unittest.main()
