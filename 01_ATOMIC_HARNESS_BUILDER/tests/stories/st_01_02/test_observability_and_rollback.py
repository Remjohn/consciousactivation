from __future__ import annotations

import unittest

from cmf_builder.application.ports import AtomicCommitFailed
from tests.stories.st_01_02 import build_context, lock_command


class ObservabilityAndRollbackTests(unittest.TestCase):
    def test_ac_09_success_observations_have_complete_governed_identity(self) -> None:
        service, _, observations, _, run_id = build_context()
        receipt = service.lock(lock_command(run_id))
        story_events = [
            item for item in observations.observations if item.story_id == "ST-01.02"
        ]

        self.assertEqual(
            [item.event_name for item in story_events],
            [
                "ST-01.02:SourceDiagnosticAccepted",
                "ST-01.02:SourceLockCreated",
                "ST-01.02:OutcomeVerified",
            ],
        )
        for item in story_events:
            self.assertEqual(item.run_id, run_id)
            self.assertEqual(item.command_id, receipt.command_id)
            self.assertEqual(item.authority_identity, "architect-1")
            self.assertEqual(item.profile_id, "synthetic_text_normalization_v1")
            self.assertEqual(item.category_id, "none_test_only")
            self.assertEqual(item.source_profile_id, "synthetic_task_definition_source_v1")
            self.assertEqual(item.source_profile_version, "1.0.0")
            self.assertEqual(len(item.source_profile_hash), 64)
            self.assertTrue(item.target_candidate.startswith("repo://"))
            self.assertEqual(item.source_lock_id, receipt.source_lock_ref)
            self.assertEqual(item.outcome, "PASS")

        second_service, _, _, _, second_run_id = build_context()
        second_receipt = second_service.lock(lock_command(second_run_id))
        self.assertEqual(receipt.receipt_hash, second_receipt.receipt_hash)

    def test_ac_03_rejection_observations_prove_zero_authoritative_mutation(self) -> None:
        service, repository, observations, _, run_id = build_context()
        command = lock_command(
            run_id,
            command_id="rejected-profile-hash",
            source_profile_sha256="0" * 64,
        )
        with self.assertRaises(Exception) as caught:
            service.lock(command)

        self.assertTrue(hasattr(caught.exception, "code"))
        self.assertEqual(repository.event_count(run_id), 2)
        self.assertEqual(repository.source_lock_count, 0)
        rejected = [
            item
            for item in observations.observations
            if item.story_id == "ST-01.02" and item.outcome == "FAIL"
        ]
        self.assertEqual(
            [item.event_name for item in rejected],
            [
                "ST-01.02:SourceDiagnosticRejected",
                "ST-01.02:OutcomeRejected",
            ],
        )
        self.assertTrue(all(item.stream_version == 2 for item in rejected))
        self.assertTrue(all("code" in item.failure_context for item in rejected))

    def test_ac_08_09_injected_atomic_failure_rolls_back_and_retry_commits_once(self) -> None:
        service, repository, observations, _, run_id = build_context()
        command = lock_command(run_id, command_id="atomic-failure-command")
        repository.inject_next_atomic_commit_failure()

        with self.assertRaises(AtomicCommitFailed):
            service.lock(command)
        self.assertEqual(repository.event_count(run_id), 2)
        self.assertEqual(repository.source_lock_count, 0)
        self.assertIsNone(repository.get_command_record(command.command_id))

        receipt = service.lock(command)
        self.assertEqual(repository.event_count(run_id), 5)
        self.assertEqual(repository.source_lock_count, 1)
        self.assertIsNotNone(repository.get_source_lock(receipt.source_lock_ref))
        rejected = [
            item
            for item in observations.observations
            if item.story_id == "ST-01.02" and item.outcome == "FAIL"
        ]
        self.assertEqual(len(rejected), 2)
        self.assertTrue(
            all(
                item.failure_context["code"] == "AtomicCommitFailed"
                for item in rejected
            )
        )


if __name__ == "__main__":
    unittest.main()
