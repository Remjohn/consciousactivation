from __future__ import annotations

import unittest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.evidence_commands import EvidenceWorkspaceCommandRejected
from cmf_builder.application.ports import IdempotencyPayloadMismatch
from tests.stories.st_01_02 import build_context, lock_command


class AuthorityAndIdempotencyTests(unittest.TestCase):
    def test_ac_09_human_and_deterministic_code_with_exact_grants_may_commit(self) -> None:
        for actor_id in ("architect-1", "code-1"):
            with self.subTest(actor=actor_id):
                service, repository, _, _, run_id = build_context()
                receipt = service.lock(
                    lock_command(
                        run_id,
                        command_id=f"allowed-{actor_id}",
                        actor_id=actor_id,
                    )
                )
                self.assertEqual(receipt.authority_identity, actor_id)
                self.assertEqual(repository.source_lock_count, 1)

    def test_ac_09_agent_external_and_expired_authority_are_denied_without_mutation(self) -> None:
        service, repository, _, _, run_id = build_context()
        for actor_id in ("agent-1", "external-1", "expired-1"):
            with self.subTest(actor=actor_id):
                with self.assertRaises(AuthorityDenied):
                    service.lock(
                        lock_command(
                            run_id,
                            command_id=f"denied-{actor_id}",
                            actor_id=actor_id,
                        )
                    )
                self.assertEqual(repository.event_count(run_id), 2)
                self.assertEqual(repository.source_lock_count, 0)

    def test_ac_08_09_replay_payload_reuse_and_stale_version_are_deterministic(self) -> None:
        service, repository, observations, _, run_id = build_context()
        command = lock_command(run_id, command_id="idempotent-command")
        first = service.lock(command)
        event_count = repository.event_count(run_id)
        second = service.lock(command)

        self.assertEqual(first, second)
        self.assertEqual(repository.event_count(run_id), event_count)
        self.assertEqual(repository.source_lock_count, 1)
        self.assertTrue(
            any(
                item.event_name == "ST-01.02:SourceLockReplayReturned"
                for item in observations.observations
            )
        )
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.lock(
                lock_command(
                    run_id,
                    command_id="idempotent-command",
                    actor_id="code-1",
                    expected_version=5,
                )
            )

        stale_service, stale_repository, _, _, stale_run_id = build_context()
        with self.assertRaises(EvidenceWorkspaceCommandRejected):
            stale_service.lock(
                lock_command(
                    stale_run_id,
                    command_id="stale-command",
                    expected_version=1,
                )
            )
        self.assertEqual(stale_repository.event_count(stale_run_id), 2)
        self.assertEqual(stale_repository.source_lock_count, 0)


if __name__ == "__main__":
    unittest.main()
