from __future__ import annotations

import unittest

from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.application.ports import ConcurrencyConflict
from cmf_builder.domain.generated_artifacts import ArtifactSetInvalidatedError
from cmf_builder.domain.run import Run
from cmf_builder.domain.run import TransitionRejected
from tests.stories.st_03_04 import build_context, compile_command


class ReplayInvalidationAndReceiptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service, self.atomicity, self.repository, self.observations, self.run_id, _, _ = build_context()
        self.command = compile_command(self.run_id)
        self.receipt = self.service.compile(self.command)
        self.manifest = self.repository.get_artifact_manifest(self.receipt.manifest_id)
        assert self.manifest is not None

    def test_repeat_command_returns_same_receipt_without_duplicate_event(self) -> None:
        before = self.repository.event_count(self.run_id)
        replay = self.service.compile(self.command)
        self.assertEqual(replay, self.receipt)
        self.assertEqual(self.repository.event_count(self.run_id), before)
        self.assertEqual(self.observations.observations[-1].event_name, "ST-03.04:CompilationReplayReturned")

    def test_event_replay_reconstructs_exact_state_hash(self) -> None:
        active = self.repository.load_run(self.run_id)
        replayed = Run.replay(self.repository.events(self.run_id))
        self.assertEqual(replayed.artifact_set_ref, self.manifest.artifact_set_id)
        self.assertEqual(replayed.state_hash(), active.state_hash())

    def test_conflicting_second_compile_is_rejected(self) -> None:
        with self.assertRaises(TransitionRejected):
            self.service.compile(compile_command(self.run_id, command_id="artifact-set-compile-2", expected_version=12))
        self.assertEqual(self.repository.artifact_manifest_count, 1)

    def test_upstream_reopen_invalidates_ir_and_artifact_descendants(self) -> None:
        self.atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-after-artifacts",
                run_id=self.run_id,
                actor_id="architect-1",
                expected_version=12,
                correlation_id="reopen-correlation",
                causation_id=self.receipt.receipt_id,
                reason="Authoritative boundary amendment requires a new immutable lineage.",
            )
        )
        run = self.repository.load_run(self.run_id)
        self.assertIsNotNone(run.harness_ir_invalidation_ref)
        self.assertIsNotNone(run.artifact_set_invalidation_ref)
        self.assertTrue(self.repository.is_artifact_set_invalidated(self.manifest.artifact_set_id))
        self.assertEqual(self.repository.artifact_invalidation_count, 1)

    def test_invalidated_artifact_set_is_unusable_but_history_remains(self) -> None:
        self.test_upstream_reopen_invalidates_ir_and_artifact_descendants()
        with self.assertRaises(ArtifactSetInvalidatedError):
            self.service.get_active(self.run_id)
        self.assertEqual(self.repository.get_artifact_manifest(self.manifest.manifest_id), self.manifest)
        self.assertEqual(len(self.repository.artifacts_for_manifest(self.manifest.manifest_id)), 21)

    def test_receipt_is_hash_valid_and_complete(self) -> None:
        self.receipt.validate(self.manifest)
        self.assertEqual(self.receipt.artifact_count, 21)
        self.assertGreater(self.receipt.total_bytes, 0)
        self.assertEqual(self.receipt.stream_version, 12)


if __name__ == "__main__":
    unittest.main()
