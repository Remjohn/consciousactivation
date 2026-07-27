from __future__ import annotations

import unittest

from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.domain.responsibility_modules import (
    ResponsibilityModuleInvalidatedError,
)
from cmf_builder.domain.run import Run
from tests.stories.st_04_02 import build_context, compile_command


class ResponsibilityModuleReplayInvalidationTests(unittest.TestCase):
    def test_repeat_command_returns_same_receipt_without_duplicate_state(self) -> None:
        service, _, repository, observations, run_id, _ = build_context()
        command = compile_command(run_id)
        first = service.compile(command)
        before = repository.event_count(run_id)
        second = service.compile(command)
        self.assertEqual(second, first)
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.responsibility_module_graph_count, 1)
        self.assertEqual(repository.responsibility_module_receipt_count, 1)
        self.assertIn("ST-04.02:CompilationReplayReturned", {item.event_name for item in observations.observations})

    def test_fresh_contexts_produce_identical_graph_and_receipt_bytes(self) -> None:
        first, _, first_repo, _, first_run, _ = build_context(seed="same")
        second, _, second_repo, _, second_run, _ = build_context(seed="same")
        first_receipt = first.compile(compile_command(first_run))
        second_receipt = second.compile(compile_command(second_run))
        first_graph = first_repo.get_responsibility_module_graph(first_receipt.graph_id)
        second_graph = second_repo.get_responsibility_module_graph(second_receipt.graph_id)
        assert first_graph is not None and second_graph is not None
        self.assertEqual(first_graph.canonical_bytes(), second_graph.canonical_bytes())
        self.assertEqual(first_graph, second_graph)
        self.assertEqual(first_receipt, second_receipt)

    def test_run_replay_reproduces_module_identity_and_state_hash(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        loaded = repository.load_run(run_id)
        replayed = Run.replay(repository.events(run_id))
        self.assertEqual(replayed, loaded)
        self.assertEqual(replayed.state_hash(), loaded.state_hash())
        self.assertEqual(replayed.responsibility_module_ref, receipt.graph_id)

    def test_upstream_reopen_invalidates_modules_and_preserves_history(self) -> None:
        service, atomicity, repository, observations, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        graph = service.get_active(run_id)
        reopen = atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-after-modules",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=15,
                correlation_id="reopen-correlation",
                causation_id=receipt.receipt_id,
                reason="Authorized correction requires a new immutable version.",
            )
        )
        run = repository.load_run(run_id)
        self.assertEqual(run.stream_version, 22)
        self.assertEqual(run.responsibility_module_invalidation_ref, reopen.invalidation_ref)
        self.assertTrue(repository.is_responsibility_module_invalidated(graph.graph_id))
        with self.assertRaises(ResponsibilityModuleInvalidatedError):
            service.get_active(run_id)
        historical = service.get_historical(graph.graph_id)
        self.assertEqual(historical.canonical_bytes(), graph.canonical_bytes())
        self.assertIn("ST-04.02:ResponsibilityModulesInvalidated", {item.event_name for item in observations.observations})

    def test_invalidation_chain_links_modules_to_capability_parent(self) -> None:
        service, atomicity, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        graph = service.get_active(run_id)
        reopen = atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-module-linkage",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=15,
                correlation_id="reopen-correlation",
                causation_id=receipt.receipt_id,
                reason="Linked invalidation test.",
            )
        )
        module_invalidation = repository.get_responsibility_module_invalidation(reopen.invalidation_ref)
        capability_invalidation = repository.get_capability_ownership_invalidation(reopen.invalidation_ref)
        self.assertIsNotNone(module_invalidation)
        self.assertIsNotNone(capability_invalidation)
        self.assertEqual(module_invalidation.module_graph_ref, graph.graph_id)
        self.assertEqual(module_invalidation.capability_graph_ref, graph.capability_graph_id)
        self.assertEqual(module_invalidation.upstream_invalidation_ref, capability_invalidation.invalidation_id)

    def test_reopen_emits_exact_seven_linked_descendant_events(self) -> None:
        service, atomicity, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        before = repository.event_count(run_id)
        atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-seven-events",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=15,
                correlation_id="reopen-correlation",
                causation_id=receipt.receipt_id,
                reason="Event chain test.",
            )
        )
        added = repository.events(run_id)[before:]
        self.assertEqual(
            tuple(item.event_type for item in added),
            (
                "AtomicBoundaryReopened",
                "DraftHarnessModelInvalidated",
                "HarnessIRInvalidated",
                "ArtifactSetInvalidated",
                "ConstitutionalValidationInvalidated",
                "CapabilityOwnershipInvalidated",
                "ResponsibilityModulesInvalidated",
            ),
        )


if __name__ == "__main__":
    unittest.main()
