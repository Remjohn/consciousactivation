from __future__ import annotations

import unittest

from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.capability_commands import CapabilityCommandRejected
from cmf_builder.application.ports import (
    AtomicCommitFailed,
    ConcurrencyConflict,
    IdempotencyPayloadMismatch,
)
from cmf_builder.domain.capability_ownership import CapabilityOwnershipInputInvalid
from tests.stories.st_04_01 import build_context, compile_command


class CapabilityOwnershipFailureTests(unittest.TestCase):
    def test_non_code_writer_is_rejected_without_partial_state(self) -> None:
        service, _, repository, observations, run_id, _ = build_context()
        with self.assertRaises(AuthorityDenied):
            service.compile(compile_command(run_id, actor_id="agent-1"))
        self.assertEqual(repository.event_count(run_id), 13)
        self.assertEqual(repository.capability_ownership_graph_count, 0)
        self.assertEqual(repository.capability_ownership_receipt_count, 0)
        self.assertEqual(
            observations.observations[-1].failure_context["code"],
            "AuthorityDenied",
        )

    def test_stale_stream_version_is_rejected_without_partial_state(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        with self.assertRaises(ConcurrencyConflict):
            service.compile(compile_command(run_id, expected_version=12))
        self.assertEqual(repository.event_count(run_id), 13)
        self.assertEqual(repository.capability_ownership_graph_count, 0)

    def test_arbitrary_or_hash_drifted_input_pin_is_rejected(self) -> None:
        cases = (
            {"ownership_input_path": "development-capsules/ST-04.01/OTHER.json"},
            {"ownership_input_sha256": "0" * 64},
        )
        for change in cases:
            with self.subTest(change=change):
                service, _, repository, _, run_id, _ = build_context()
                command = compile_command(run_id, **change)
                with self.assertRaises(CapabilityOwnershipInputInvalid):
                    service.compile(command)
                self.assertEqual(repository.capability_ownership_graph_count, 0)

    def test_injected_atomic_failure_leaves_zero_graph_event_receipt_or_command(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        repository.inject_next_atomic_commit_failure()
        command = compile_command(run_id)
        with self.assertRaises(AtomicCommitFailed):
            service.compile(command)
        self.assertEqual(repository.event_count(run_id), 13)
        self.assertEqual(repository.capability_ownership_graph_count, 0)
        self.assertEqual(repository.capability_ownership_receipt_count, 0)
        self.assertIsNone(repository.get_command_record(command.command_id))

    def test_reused_command_with_changed_payload_fails_closed(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        service.compile(compile_command(run_id))
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.compile(
                compile_command(
                    run_id,
                    actor_id="agent-1",
                )
            )
        self.assertEqual(repository.event_count(run_id), 14)
        self.assertEqual(repository.capability_ownership_graph_count, 1)

    def test_invalidated_constitutional_parent_cannot_compile_a_graph(self) -> None:
        service, atomicity, repository, _, run_id, constitutional_receipt = (
            build_context()
        )
        atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-before-capability",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=13,
                correlation_id="reopen-correlation",
                causation_id=constitutional_receipt.receipt_id,
                reason="Authorized parent invalidation test.",
            )
        )
        with self.assertRaises(CapabilityCommandRejected):
            service.compile(
                compile_command(
                    run_id,
                    command_id="compile-after-parent-invalidation",
                    expected_version=18,
                )
            )
        self.assertEqual(repository.capability_ownership_graph_count, 0)
        self.assertEqual(repository.capability_ownership_receipt_count, 0)


if __name__ == "__main__":
    unittest.main()
