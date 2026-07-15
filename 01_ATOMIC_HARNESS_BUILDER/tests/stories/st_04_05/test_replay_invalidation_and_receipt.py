from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.application.ports import IdempotencyPayloadMismatch
from cmf_builder.domain.context_manifest import ContextInvalidatedError
from cmf_builder.domain.run import Run
from tests.stories.st_04_05 import build_context, compile_command


class MinimumContextReplayInvalidationTests(unittest.TestCase):
    def _complete(self, *, seed: str = "ST-04.05"):
        service, handoffs, atomicity, repository, observations, run_id, accepted = build_context(seed=seed)
        receipt = service.compile(compile_command(run_id))
        graph = service.get_active(run_id)
        return service, handoffs, atomicity, repository, observations, run_id, accepted, receipt, graph

    def test_repeat_command_is_payload_safe_and_does_not_duplicate_state(self) -> None:
        service, _, _, repository, observations, run_id, _, receipt, _ = self._complete()
        before = repository.event_count(run_id)
        self.assertEqual(service.compile(compile_command(run_id)), receipt)
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.minimum_context_graph_count, 1)
        self.assertEqual(repository.context_compilation_receipt_count, 1)
        self.assertEqual(observations.observations[-1].event_name, "ST-04.05:CommandReplayReturned")

    def test_fresh_context_is_byte_identical(self) -> None:
        first = self._complete(seed="identical-context")
        second = self._complete(seed="identical-context")
        self.assertEqual(first[8].canonical_bytes(), second[8].canonical_bytes())
        self.assertEqual(first[7].canonical_bytes(), second[7].canonical_bytes())

    def test_run_replay_preserves_context_state_and_hash(self) -> None:
        _, _, _, repository, _, run_id, _, _, graph = self._complete()
        loaded = repository.load_run(run_id)
        replayed = Run.replay(repository.events(run_id))
        self.assertEqual(replayed, loaded)
        self.assertEqual(replayed.state_hash(), loaded.state_hash())
        self.assertEqual(replayed.minimum_context_ref, graph.graph_id)
        self.assertEqual(replayed.minimum_context_hash, graph.graph_hash)

    def test_changed_repeat_payload_conflicts(self) -> None:
        service, _, _, repository, _, run_id, _, _, _ = self._complete()
        before = repository.event_count(run_id)
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.compile(replace(compile_command(run_id), causation_id="conflicting-cause"))
        self.assertEqual(repository.event_count(run_id), before)

    def test_upstream_reopen_invalidates_exact_context_descendants_and_preserves_history(self) -> None:
        service, _, atomicity, repository, observations, run_id, accepted, _, graph = self._complete()
        before = repository.event_count(run_id)
        result = atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-after-minimum-context",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=20,
                correlation_id="reopen-context-correlation",
                causation_id=accepted.receipt_id,
                reason="Authorized upstream correction invalidates affected context descendants.",
            )
        )
        run = repository.load_run(run_id)
        self.assertEqual(run.stream_version, 30)
        self.assertEqual(run.minimum_context_invalidation_ref, result.invalidation_ref)
        self.assertTrue(repository.is_minimum_context_invalidated(graph.graph_id))
        invalidation = repository.get_context_graph_invalidation(result.invalidation_ref)
        assert invalidation is not None
        self.assertEqual(
            invalidation.affected_manifest_ids,
            tuple(sorted(item.manifest_id for item in graph.manifests)),
        )
        self.assertEqual(service.get_historical(graph.graph_id).canonical_bytes(), graph.canonical_bytes())
        with self.assertRaises(ContextInvalidatedError):
            service.get_active(run_id)
        self.assertEqual(
            tuple(item.event_type for item in repository.events(run_id)[before:]),
            (
                "AtomicBoundaryReopened", "DraftHarnessModelInvalidated", "HarnessIRInvalidated",
                "ArtifactSetInvalidated", "ConstitutionalValidationInvalidated",
                "CapabilityOwnershipInvalidated", "ResponsibilityModulesInvalidated",
                "PhaseGraphInvalidated", "PhaseHandoffsInvalidated", "MinimumContextInvalidated",
            ),
        )
        self.assertIn(
            "ST-04.05:MinimumCompleteContextInvalidated",
            {item.event_name for item in observations.observations},
        )


if __name__ == "__main__":
    unittest.main()
