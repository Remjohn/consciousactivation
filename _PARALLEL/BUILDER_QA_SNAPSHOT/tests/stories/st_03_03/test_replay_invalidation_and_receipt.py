from __future__ import annotations

import unittest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.domain.harness_ir import HarnessIRInvalidatedError
from cmf_builder.domain.run import Run
from tests.stories.st_02_05 import reopen_command
from tests.stories.st_03_03 import build_context, compile_command


class HarnessIRReplayInvalidationReceiptTests(unittest.TestCase):
    def test_ac_09_identical_replay_returns_receipt_without_duplicate_events(self) -> None:
        service, _, repository, observations, run_id, _ = build_context()
        command = compile_command(run_id, command_id="replay-ir")
        first = service.compile(command)
        event_count = repository.event_count(run_id)
        second = service.compile(command)
        self.assertEqual(first, second)
        self.assertEqual(repository.event_count(run_id), event_count)
        self.assertIn("ST-03.03:CompilationReplayReturned", [item.event_name for item in observations.observations])

    def test_ac_10_event_replay_reconstructs_ir_reference_and_state_hash(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        current = repository.load_run(run_id)
        replayed = Run.replay(repository.events(run_id))
        self.assertEqual(replayed, current)
        self.assertEqual(replayed.state_hash(), current.state_hash())
        self.assertEqual(replayed.harness_ir_ref, receipt.ir_id)

    def test_ac_10_upstream_reopen_invalidates_ir_descendant_and_preserves_snapshot(self) -> None:
        service, atomicity, repository, observations, run_id, _ = build_context()
        compiled = service.compile(compile_command(run_id))
        reopened = atomicity.reopen(reopen_command(run_id, expected_version=11))
        self.assertTrue(repository.is_harness_ir_invalidated(compiled.ir_id))
        self.assertIsNotNone(repository.get_harness_ir(compiled.ir_id))
        self.assertEqual(repository.load_run(run_id).harness_ir_invalidation_ref, reopened.invalidation_ref)
        with self.assertRaises(HarnessIRInvalidatedError):
            service.get_active(run_id)
        self.assertIn("ST-03.03:HarnessIRInvalidated", [item.event_name for item in observations.observations])

    def test_ac_11_observations_and_receipt_have_complete_identity(self) -> None:
        service, _, _, observations, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        story = [item for item in observations.observations if item.story_id == "ST-03.03"]
        self.assertEqual(
            [item.event_name for item in story],
            [
                "ST-03.03:HarnessIRCompiled",
                "ST-03.03:HarnessIRSnapshotCommitted",
                "ST-03.03:CompatibilityValidated",
                "ST-03.03:OutcomeVerified",
            ],
        )
        for item in story:
            self.assertEqual(item.run_id, run_id)
            self.assertEqual(item.harness_ir_id, receipt.ir_id)
            self.assertEqual(item.harness_ir_hash, receipt.ir_hash)
            self.assertEqual(item.harness_ir_schema_version, "1.0.0")
            self.assertEqual(item.harness_ir_revision, 1)
            self.assertEqual(item.outcome, "PASS")

    def test_ac_10_unauthorized_reopen_preserves_active_ir(self) -> None:
        service, atomicity, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        with self.assertRaises(AuthorityDenied):
            atomicity.reopen(reopen_command(run_id, actor_id="agent-1", expected_version=11))
        self.assertFalse(repository.is_harness_ir_invalidated(receipt.ir_id))
        self.assertEqual(service.get_active(run_id).ir_id, receipt.ir_id)


if __name__ == "__main__":
    unittest.main()
