from __future__ import annotations

import unittest

from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.domain.phase_graph import PhaseGraphInvalidatedError
from cmf_builder.domain.run import Run
from tests.stories.st_04_03 import build_context, compile_command


class PhaseGraphReplayInvalidationTests(unittest.TestCase):
    def test_repeat_command_returns_same_receipt_without_duplicate_state(self) -> None:
        service, _, repository, observations, run_id, _ = build_context()
        command = compile_command(run_id)
        first = service.compile(command)
        before = repository.event_count(run_id)
        second = service.compile(command)
        self.assertEqual(second, first)
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.phase_graph_count, 1)
        self.assertEqual(repository.phase_graph_receipt_count, 1)
        self.assertIn("ST-04.03:CompilationReplayReturned", {item.event_name for item in observations.observations})

    def test_fresh_contexts_produce_identical_graph_and_receipt_bytes(self) -> None:
        first, _, first_repo, _, first_run, _ = build_context(seed="same")
        second, _, second_repo, _, second_run, _ = build_context(seed="same")
        first_receipt = first.compile(compile_command(first_run))
        second_receipt = second.compile(compile_command(second_run))
        first_graph = first_repo.get_phase_graph(first_receipt.graph_id)
        second_graph = second_repo.get_phase_graph(second_receipt.graph_id)
        assert first_graph is not None and second_graph is not None
        self.assertEqual(first_graph.canonical_bytes(), second_graph.canonical_bytes())
        self.assertEqual(first_graph, second_graph)
        self.assertEqual(first_receipt, second_receipt)

    def test_run_replay_reproduces_phase_identity_and_state_hash(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        loaded = repository.load_run(run_id)
        replayed = Run.replay(repository.events(run_id))
        self.assertEqual(replayed, loaded)
        self.assertEqual(replayed.state_hash(), loaded.state_hash())
        self.assertEqual(replayed.phase_graph_ref, receipt.graph_id)

    def test_upstream_reopen_invalidates_phase_graph_and_preserves_history(self) -> None:
        service, atomicity, repository, observations, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        graph = service.get_active(run_id)
        reopen = atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-after-phase",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=16,
                correlation_id="reopen-correlation",
                causation_id=receipt.receipt_id,
                reason="Authorized correction requires a new immutable version.",
            )
        )
        run = repository.load_run(run_id)
        self.assertEqual(run.stream_version, 24)
        self.assertEqual(run.phase_graph_invalidation_ref, reopen.invalidation_ref)
        self.assertTrue(repository.is_phase_graph_invalidated(graph.graph_id))
        with self.assertRaises(PhaseGraphInvalidatedError):
            service.get_active(run_id)
        self.assertEqual(service.get_historical(graph.graph_id).canonical_bytes(), graph.canonical_bytes())
        self.assertIn("ST-04.03:PhaseGraphInvalidated", {item.event_name for item in observations.observations})

    def test_invalidation_chain_links_phase_to_module_parent(self) -> None:
        service, atomicity, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        graph = service.get_active(run_id)
        reopen = atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-phase-linkage",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=16,
                correlation_id="reopen-correlation",
                causation_id=receipt.receipt_id,
                reason="Linked invalidation test.",
            )
        )
        phase_invalidation = repository.get_phase_graph_invalidation(reopen.invalidation_ref)
        module_invalidation = repository.get_responsibility_module_invalidation(reopen.invalidation_ref)
        self.assertIsNotNone(phase_invalidation)
        self.assertIsNotNone(module_invalidation)
        self.assertEqual(phase_invalidation.phase_graph_ref, graph.graph_id)
        self.assertEqual(phase_invalidation.module_graph_ref, graph.module_graph_id)
        self.assertEqual(phase_invalidation.upstream_invalidation_ref, module_invalidation.invalidation_id)

    def test_reopen_emits_exact_eight_linked_descendant_events(self) -> None:
        service, atomicity, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        before = repository.event_count(run_id)
        atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-eight-events",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=16,
                correlation_id="reopen-correlation",
                causation_id=receipt.receipt_id,
                reason="Event chain test.",
            )
        )
        self.assertEqual(
            tuple(item.event_type for item in repository.events(run_id)[before:]),
            ("AtomicBoundaryReopened", "DraftHarnessModelInvalidated", "HarnessIRInvalidated", "ArtifactSetInvalidated", "ConstitutionalValidationInvalidated", "CapabilityOwnershipInvalidated", "ResponsibilityModulesInvalidated", "PhaseGraphInvalidated"),
        )


if __name__ == "__main__":
    unittest.main()
