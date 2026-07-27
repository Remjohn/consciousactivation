from __future__ import annotations

import unittest

from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.domain.capability_ownership import (
    CapabilityOwnershipInvalidatedError,
)
from cmf_builder.domain.run import Run
from tests.stories.st_04_01 import build_context, compile_command


class CapabilityReplayInvalidationAndReceiptTests(unittest.TestCase):
    def test_repeat_command_returns_same_receipt_without_duplicate_state(self) -> None:
        service, _, repository, observations, run_id, _ = build_context()
        command = compile_command(run_id)
        first = service.compile(command)
        count = repository.event_count(run_id)
        second = service.compile(command)
        self.assertEqual(second, first)
        self.assertEqual(repository.event_count(run_id), count)
        self.assertEqual(repository.capability_ownership_graph_count, 1)
        self.assertEqual(repository.capability_ownership_receipt_count, 1)
        self.assertIn(
            "ST-04.01:CompilationReplayReturned",
            {item.event_name for item in observations.observations},
        )

    def test_fresh_deterministic_contexts_produce_byte_identical_graphs(self) -> None:
        first_service, _, first_repo, _, first_run, _ = build_context(seed="same")
        second_service, _, second_repo, _, second_run, _ = build_context(seed="same")
        first_receipt = first_service.compile(compile_command(first_run))
        second_receipt = second_service.compile(compile_command(second_run))
        first_graph = first_repo.get_capability_ownership_graph(first_receipt.graph_id)
        second_graph = second_repo.get_capability_ownership_graph(second_receipt.graph_id)
        assert first_graph is not None and second_graph is not None
        self.assertEqual(first_graph, second_graph)
        self.assertEqual(first_receipt, second_receipt)
        self.assertEqual(first_graph.canonical_bytes(), second_graph.canonical_bytes())

    def test_run_replay_reproduces_capability_identity_and_state_hash(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        loaded = repository.load_run(run_id)
        replayed = Run.replay(repository.events(run_id))
        self.assertEqual(replayed, loaded)
        self.assertEqual(replayed.state_hash(), loaded.state_hash())
        self.assertEqual(replayed.capability_ownership_ref, receipt.graph_id)

    def test_upstream_reopen_invalidates_graph_and_preserves_history(self) -> None:
        service, atomicity, repository, observations, run_id, _ = build_context()
        capability_receipt = service.compile(compile_command(run_id))
        graph = service.get_active(run_id)
        reopen = atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-after-capability",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=14,
                correlation_id="reopen-correlation",
                causation_id=capability_receipt.receipt_id,
                reason="Authorized correction requires a new immutable version.",
            )
        )
        run = repository.load_run(run_id)
        self.assertEqual(run.stream_version, 20)
        self.assertEqual(run.capability_ownership_invalidation_ref, reopen.invalidation_ref)
        self.assertTrue(repository.is_capability_ownership_invalidated(graph.graph_id))
        with self.assertRaises(CapabilityOwnershipInvalidatedError):
            service.get_active(run_id)
        historical = service.get_historical(graph.graph_id)
        self.assertEqual(historical.canonical_bytes(), graph.canonical_bytes())
        self.assertIn(
            "ST-04.01:CapabilityOwnershipInvalidated",
            {item.event_name for item in observations.observations},
        )

    def test_invalidation_chain_links_graph_to_constitutional_parent(self) -> None:
        service, atomicity, repository, _, run_id, _ = build_context()
        capability_receipt = service.compile(compile_command(run_id))
        graph = service.get_active(run_id)
        reopen = atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-capability-linkage",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=14,
                correlation_id="reopen-correlation",
                causation_id=capability_receipt.receipt_id,
                reason="Linked invalidation test.",
            )
        )
        graph_invalidation = repository.get_capability_ownership_invalidation(
            reopen.invalidation_ref
        )
        constitutional_invalidation = (
            repository.get_constitutional_validation_invalidation(
                reopen.invalidation_ref
            )
        )
        self.assertIsNotNone(graph_invalidation)
        self.assertIsNotNone(constitutional_invalidation)
        self.assertEqual(graph_invalidation.graph_ref, graph.graph_id)
        self.assertEqual(
            graph_invalidation.constitutional_report_ref,
            graph.constitutional_report_id,
        )
        self.assertEqual(
            graph_invalidation.upstream_invalidation_ref,
            constitutional_invalidation.invalidation_id,
        )

    def test_reopen_emits_exact_six_linked_descendant_events(self) -> None:
        service, atomicity, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        before = repository.event_count(run_id)
        atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-six-events",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=14,
                correlation_id="reopen-correlation",
                causation_id=receipt.receipt_id,
                reason="Event chain test.",
            )
        )
        added = repository.events(run_id)[before:]
        self.assertEqual(len(added), 6)
        self.assertEqual(
            tuple(item.event_type for item in added),
            (
                "AtomicBoundaryReopened",
                "DraftHarnessModelInvalidated",
                "HarnessIRInvalidated",
                "ArtifactSetInvalidated",
                "ConstitutionalValidationInvalidated",
                "CapabilityOwnershipInvalidated",
            ),
        )


if __name__ == "__main__":
    unittest.main()
