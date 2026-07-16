from __future__ import annotations

import unittest

from cmf_builder.application.authority import AuthorityDenied

from tests.stories.st_01_01_synthetic_proof import build_service, create_command


class SyntheticProofAuthorityTests(unittest.TestCase):
    def test_ac_sp_07_unknown_actor_cannot_admit_profile(self) -> None:
        service, repository, observations, _, _ = build_service()

        with self.assertRaises(AuthorityDenied):
            service.create_run(create_command(actor_id="unknown-actor"))

        self.assertEqual(repository.stream_count, 0)
        self.assertEqual(observations.observations[-1].outcome, "FAIL")
        self.assertEqual(
            observations.observations[-1].failure_context["code"], "AuthorityDenied"
        )

    def test_ac_sp_07_agent_cannot_commit_even_when_granted(self) -> None:
        service, repository, _, _, _ = build_service(agent_granted=True)

        with self.assertRaises(AuthorityDenied):
            service.create_run(create_command(actor_id="agent-1"))

        self.assertEqual(repository.stream_count, 0)

    def test_ac_sp_07_authorized_human_admits_exactly_one_run(self) -> None:
        service, repository, observations, _, _ = build_service()

        receipt = service.create_run(create_command())

        self.assertEqual(repository.stream_count, 1)
        self.assertEqual(repository.event_count(receipt.run_id), 2)
        self.assertEqual(observations.observations[-1].authority_identity, "architect-1")


if __name__ == "__main__":
    unittest.main()
