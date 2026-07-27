from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.application.ports import IdempotencyPayloadMismatch
from cmf_builder.domain.handoff import HandoffInvalidatedError, HandoffStateInvalid
from cmf_builder.domain.run import Run
from tests.stories.st_04_04 import (
    build_context,
    compile_command,
    decision_command,
    governed_artifacts,
    issue_command,
)


class InternalHandoffReplayInvalidationTests(unittest.TestCase):
    def _complete(self, *, seed: str = "ST-04.04"):
        service, atomicity, repository, observations, run_id, _ = build_context(seed=seed)
        compiled = service.compile(compile_command(run_id))
        graph = service.get_active(run_id)
        artifacts = governed_artifacts(service, repository, run_id)
        issued = service.issue(issue_command(run_id, artifacts))
        accepted = service.decide(decision_command(run_id, issued.handoff_id))
        return service, atomicity, repository, observations, run_id, compiled, graph, issued, accepted

    def test_compile_issue_and_decision_replays_are_payload_safe(self) -> None:
        service, _, repository, observations, run_id, compiled, _, issued, accepted = self._complete()
        before = repository.event_count(run_id)
        self.assertEqual(service.compile(compile_command(run_id)), compiled)
        self.assertEqual(service.issue(issue_command(run_id, governed_artifacts(service, repository, run_id))), issued)
        self.assertEqual(service.decide(decision_command(run_id, issued.handoff_id)), accepted)
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.phase_handoff_graph_count, 1)
        self.assertEqual(repository.internal_handoff_count, 1)
        self.assertEqual(repository.internal_handoff_decision_count, 1)
        self.assertEqual(
            len([item for item in observations.observations if item.event_name == "ST-04.04:CommandReplayReturned"]),
            3,
        )

    def test_fresh_context_reproduction_is_byte_identical(self) -> None:
        first = self._complete(seed="identical")
        second = self._complete(seed="identical")
        self.assertEqual(first[6].canonical_bytes(), second[6].canonical_bytes())
        self.assertEqual(first[5].canonical_bytes(), second[5].canonical_bytes())
        first_handoff = first[2].get_internal_handoff(first[7].handoff_id)
        second_handoff = second[2].get_internal_handoff(second[7].handoff_id)
        self.assertEqual(first_handoff, second_handoff)
        self.assertEqual(first[8], second[8])

    def test_run_replay_preserves_handoff_state_and_hash(self) -> None:
        _, _, repository, _, run_id, _, graph, issued, _ = self._complete()
        loaded = repository.load_run(run_id)
        replayed = Run.replay(repository.events(run_id))
        self.assertEqual(replayed, loaded)
        self.assertEqual(replayed.state_hash(), loaded.state_hash())
        self.assertEqual(replayed.phase_handoff_ref, graph.graph_id)
        self.assertEqual(repository.get_internal_handoff(issued.handoff_id).handoff_id, issued.handoff_id)

    def test_repeat_command_with_changed_payload_conflicts(self) -> None:
        service, _, repository, _, run_id, _, _, issued, _ = self._complete()
        command = decision_command(run_id, issued.handoff_id)
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.decide(replace(command, reason="Conflicting repeat payload."))
        self.assertEqual(repository.internal_handoff_decision_count, 1)

    def test_second_decision_under_new_command_identity_is_rejected(self) -> None:
        service, _, repository, _, run_id, _, _, issued, _ = self._complete()
        with self.assertRaises(HandoffStateInvalid):
            service.decide(decision_command(
                run_id,
                issued.handoff_id,
                command_id="second-decision",
                expected_version=19,
            ))
        self.assertEqual(repository.internal_handoff_decision_count, 1)

    def test_upstream_reopen_invalidates_handoff_descendants_and_preserves_history(self) -> None:
        service, atomicity, repository, observations, run_id, _, graph, issued, _ = self._complete()
        before = repository.event_count(run_id)
        result = atomicity.reopen(ReopenAtomicBoundaryCommand(
            command_id="reopen-after-handoff",
            run_id=run_id,
            actor_id="architect-1",
            expected_version=19,
            correlation_id="reopen-handoff-correlation",
            causation_id=issued.receipt_id,
            reason="Authorized upstream correction invalidates affected handoffs.",
        ))
        run = repository.load_run(run_id)
        self.assertEqual(run.stream_version, 28)
        self.assertEqual(run.phase_handoff_invalidation_ref, result.invalidation_ref)
        self.assertTrue(repository.is_phase_handoff_invalidated(graph.graph_id))
        self.assertTrue(repository.is_internal_handoff_invalidated(issued.handoff_id))
        invalidation = repository.get_phase_handoff_invalidation(result.invalidation_ref)
        assert invalidation is not None
        self.assertEqual(invalidation.affected_handoff_ids, (issued.handoff_id,))
        self.assertEqual(service.get_historical(graph.graph_id).canonical_bytes(), graph.canonical_bytes())
        with self.assertRaises(HandoffInvalidatedError):
            service.get_active(run_id)
        self.assertEqual(
            tuple(item.event_type for item in repository.events(run_id)[before:]),
            (
                "AtomicBoundaryReopened", "DraftHarnessModelInvalidated", "HarnessIRInvalidated",
                "ArtifactSetInvalidated", "ConstitutionalValidationInvalidated",
                "CapabilityOwnershipInvalidated", "ResponsibilityModulesInvalidated",
                "PhaseGraphInvalidated", "PhaseHandoffsInvalidated",
            ),
        )
        self.assertIn("ST-04.04:PhaseHandoffsInvalidated", {item.event_name for item in observations.observations})


if __name__ == "__main__":
    unittest.main()
