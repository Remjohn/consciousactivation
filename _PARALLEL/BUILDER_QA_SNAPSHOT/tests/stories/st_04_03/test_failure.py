from __future__ import annotations

import unittest

from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.phase_commands import PhaseCommandRejected
from cmf_builder.application.ports import AtomicCommitFailed, ConcurrencyConflict, IdempotencyPayloadMismatch
from cmf_builder.domain.phase_graph import PhaseGraphInputInvalid
from tests.stories.st_04_03 import build_context, compile_command


class PhaseGraphFailureTests(unittest.TestCase):
    def test_non_code_writer_is_rejected_without_partial_state(self) -> None:
        service, _, repository, observations, run_id, _ = build_context()
        with self.assertRaises(AuthorityDenied):
            service.compile(compile_command(run_id, actor_id="agent-1"))
        self.assertEqual(repository.event_count(run_id), 15)
        self.assertEqual(repository.phase_graph_count, 0)
        self.assertEqual(repository.phase_graph_receipt_count, 0)
        self.assertEqual(observations.observations[-1].event_name, "ST-04.03:OutcomeRejected")

    def test_missing_actor_authority_is_rejected(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        with self.assertRaises(AuthorityDenied):
            service.compile(compile_command(run_id, actor_id="unknown-actor"))
        self.assertEqual(repository.phase_graph_count, 0)

    def test_stale_stream_version_is_rejected_without_partial_state(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        with self.assertRaises(ConcurrencyConflict):
            service.compile(compile_command(run_id, expected_version=14))
        self.assertEqual(repository.event_count(run_id), 15)
        self.assertEqual(repository.phase_graph_count, 0)

    def test_arbitrary_path_or_hash_drift_is_rejected(self) -> None:
        cases = (
            {"phase_input_path": "development-capsules/ST-04.03/OTHER.json"},
            {"phase_input_sha256": "0" * 64},
        )
        for change in cases:
            with self.subTest(change=change):
                service, _, repository, _, run_id, _ = build_context()
                with self.assertRaises(PhaseGraphInputInvalid):
                    service.compile(compile_command(run_id, **change))
                self.assertEqual(repository.phase_graph_count, 0)

    def test_injected_atomic_failure_leaves_zero_partial_state(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        repository.inject_next_atomic_commit_failure()
        command = compile_command(run_id)
        with self.assertRaises(AtomicCommitFailed):
            service.compile(command)
        self.assertEqual(repository.event_count(run_id), 15)
        self.assertEqual(repository.phase_graph_count, 0)
        self.assertEqual(repository.phase_graph_receipt_count, 0)
        self.assertIsNone(repository.get_command_record(command.command_id))

    def test_reused_command_with_changed_payload_fails_closed(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        service.compile(compile_command(run_id))
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.compile(compile_command(run_id, actor_id="agent-1"))
        self.assertEqual(repository.event_count(run_id), 16)
        self.assertEqual(repository.phase_graph_count, 1)

    def test_invalidated_module_parent_cannot_compile_phase_graph(self) -> None:
        service, atomicity, repository, _, run_id, module_receipt = build_context()
        atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-before-phase",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=15,
                correlation_id="reopen-correlation",
                causation_id=module_receipt.receipt_id,
                reason="Authorized parent invalidation test.",
            )
        )
        with self.assertRaises(PhaseCommandRejected):
            service.compile(compile_command(run_id, command_id="compile-after-invalidation", expected_version=22))
        self.assertEqual(repository.phase_graph_count, 0)


if __name__ == "__main__":
    unittest.main()
