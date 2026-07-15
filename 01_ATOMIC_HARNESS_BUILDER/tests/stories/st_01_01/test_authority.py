from __future__ import annotations

from datetime import timedelta
import unittest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.run_commands import GrantWaiverCommand
from cmf_builder.domain.run import WaiverRejected

from tests.stories.st_01_01 import NOW, build_service, create_command


class AuthorityBoundaryTests(unittest.TestCase):
    def test_st_01_01_authority_unauthorized_actor_cannot_create(self) -> None:
        service, repository, observations, _, _ = build_service()

        with self.assertRaises(AuthorityDenied):
            service.create_run(create_command(actor_id="unknown-actor"))

        self.assertEqual(repository.stream_count, 0)
        self.assertEqual(observations.observations[-1].failure_context["code"], "AuthorityDenied")

    def test_st_01_01_authority_agent_cannot_commit_even_with_grant(self) -> None:
        service, repository, _, _, _ = build_service(agent_granted=True)

        with self.assertRaises(AuthorityDenied):
            service.create_run(create_command(actor_id="agent-1"))
        self.assertEqual(repository.stream_count, 0)

    def test_st_01_01_authority_human_can_issue_bounded_waiver_receipt(self) -> None:
        service, repository, _, _, _ = build_service()
        created = service.create_run(create_command())

        receipt = service.grant_waiver(
            GrantWaiverCommand(
                command_id="waiver-1",
                run_id=created.run_id,
                skipped_obligation="optional_format02_review",
                rationale="The bounded review is covered by deterministic fixtures.",
                risk="low",
                affected_gates=("HG-004",),
                scope="ST-01.01 Format 02 only",
                expires_at=NOW + timedelta(hours=1),
                actor_id="architect-1",
                expected_version=2,
                correlation_id="correlation-1",
                causation_id=created.receipt_id,
            )
        )

        run = repository.load_run(created.run_id)
        self.assertIn(receipt.detail("human_receipt_id"), run.human_decision_receipt_ids)
        self.assertEqual(repository.events(created.run_id)[-1].event_type, "LifecycleWaiverGranted")

    def test_st_01_01_authority_expired_and_production_waivers_fail_closed(self) -> None:
        for command_id, expires_at, gates in (
            ("expired", NOW - timedelta(seconds=1), ("HG-004",)),
            ("production", NOW + timedelta(hours=1), ("production_certification",)),
        ):
            with self.subTest(command=command_id):
                service, repository, _, _, _ = build_service()
                created = service.create_run(create_command())
                with self.assertRaises(WaiverRejected):
                    service.grant_waiver(
                        GrantWaiverCommand(
                            command_id=command_id,
                            run_id=created.run_id,
                            skipped_obligation="gate",
                            rationale="Not sufficient for a protected gate.",
                            risk="high",
                            affected_gates=gates,
                            scope="ST-01.01",
                            expires_at=expires_at,
                            actor_id="architect-1",
                            expected_version=2,
                            correlation_id="correlation-1",
                            causation_id=created.receipt_id,
                        )
                    )
                self.assertEqual(repository.event_count(created.run_id), 2)


if __name__ == "__main__":
    unittest.main()
