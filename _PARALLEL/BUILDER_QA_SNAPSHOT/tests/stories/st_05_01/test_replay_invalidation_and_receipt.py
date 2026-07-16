from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.application.ports import IdempotencyPayloadMismatch
from cmf_builder.domain.run import Run
from cmf_builder.domain.skill_registry import SkillRegistryInvalidatedError
from tests.stories.st_05_01 import build_context, compile_command


class SkillRegistryReplayInvalidationTests(unittest.TestCase):
    def _complete(self, *, seed: str = "ST-05.01"):
        service, atomicity, repository, observations, run_id, accepted, context_receipt = (
            build_context(seed=seed)
        )
        receipt = service.compile(compile_command(run_id))
        snapshot = service.get_active(run_id)
        return (
            service,
            atomicity,
            repository,
            observations,
            run_id,
            accepted,
            context_receipt,
            receipt,
            snapshot,
        )

    def test_ac_08_repeat_command_is_payload_safe_and_observable(self) -> None:
        service, _, repository, observations, run_id, _, _, receipt, _ = self._complete()
        before = repository.event_count(run_id)
        self.assertEqual(service.compile(compile_command(run_id)), receipt)
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.skill_registry_snapshot_count, 1)
        self.assertEqual(repository.skill_registry_consumption_receipt_count, 1)
        self.assertEqual(observations.observations[-1].event_name, "synthetic_skill_registry_replayed")

    def test_ac_08_fresh_context_bytes_and_hashes_are_identical(self) -> None:
        first = self._complete(seed="identical-skill-registry")
        second = self._complete(seed="identical-skill-registry")
        self.assertEqual(first[8].canonical_bytes(), second[8].canonical_bytes())
        self.assertEqual(first[7].canonical_bytes(), second[7].canonical_bytes())
        self.assertEqual(first[8].snapshot_hash, second[8].snapshot_hash)
        self.assertEqual(first[7].receipt_hash, second[7].receipt_hash)

    def test_run_replay_preserves_snapshot_identity_and_state_hash(self) -> None:
        _, _, repository, _, run_id, _, _, _, snapshot = self._complete()
        loaded = repository.load_run(run_id)
        replayed = Run.replay(repository.events(run_id))
        self.assertEqual(replayed, loaded)
        self.assertEqual(replayed.state_hash(), loaded.state_hash())
        self.assertEqual(replayed.skill_registry_snapshot_ref, snapshot.snapshot_id)
        self.assertEqual(replayed.skill_registry_snapshot_hash, snapshot.snapshot_hash)

    def test_changed_repeat_payload_conflicts(self) -> None:
        service, _, repository, _, run_id, _, _, _, _ = self._complete()
        before = repository.event_count(run_id)
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.compile(replace(compile_command(run_id), actor_id="architect-1"))
        self.assertEqual(repository.event_count(run_id), before)

    def test_ac_09_upstream_reopen_invalidates_snapshot_and_preserves_history(self) -> None:
        service, atomicity, repository, observations, run_id, accepted, _, _, snapshot = (
            self._complete()
        )
        before = repository.event_count(run_id)
        result = atomicity.reopen(ReopenAtomicBoundaryCommand(
            command_id="reopen-after-skill-snapshot",
            run_id=run_id,
            actor_id="architect-1",
            expected_version=21,
            correlation_id="reopen-skill-registry-correlation",
            causation_id=accepted.receipt_id,
            reason="Authorized upstream correction invalidates the synthetic skill snapshot.",
        ))
        run = repository.load_run(run_id)
        self.assertEqual(run.stream_version, 32)
        self.assertEqual(run.skill_registry_snapshot_invalidation_ref, result.invalidation_ref)
        self.assertTrue(repository.is_skill_registry_snapshot_invalidated(snapshot.snapshot_id))
        invalidation = repository.get_skill_registry_snapshot_invalidation(result.invalidation_ref)
        assert invalidation is not None
        self.assertEqual(invalidation.affected_capability_ids, snapshot.capability_ids)
        self.assertEqual(
            service.get_historical(snapshot.snapshot_id).canonical_bytes(),
            snapshot.canonical_bytes(),
        )
        with self.assertRaises(SkillRegistryInvalidatedError):
            service.get_active(run_id)
        self.assertEqual(
            tuple(item.event_type for item in repository.events(run_id)[before:]),
            (
                "AtomicBoundaryReopened",
                "DraftHarnessModelInvalidated",
                "HarnessIRInvalidated",
                "ArtifactSetInvalidated",
                "ConstitutionalValidationInvalidated",
                "CapabilityOwnershipInvalidated",
                "ResponsibilityModulesInvalidated",
                "PhaseGraphInvalidated",
                "PhaseHandoffsInvalidated",
                "MinimumContextInvalidated",
                "SkillRegistrySnapshotInvalidated",
            ),
        )
        self.assertIn(
            "synthetic_skill_registry_invalidated",
            {item.event_name for item in observations.observations},
        )


if __name__ == "__main__":
    unittest.main()
