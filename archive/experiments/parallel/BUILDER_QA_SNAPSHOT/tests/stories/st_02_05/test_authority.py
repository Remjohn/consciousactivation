from __future__ import annotations

import unittest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.domain.atomicity import DecisionPackageIncomplete
from tests.stories.st_02_05 import (
    build_context,
    decide_command,
    decision,
    reopen_command,
)


class AtomicityAuthorityTests(unittest.TestCase):
    def test_ac_06_exact_human_authority_may_ratify(self) -> None:
        service, repository, _, run_id, _ = build_context()
        receipt = service.decide(decide_command(run_id))
        self.assertEqual(receipt.authority_identity, "architect-1")
        self.assertEqual(repository.atomic_boundary_count, 1)

    def test_ac_06_code_agent_external_and_evaluator_cannot_ratify(self) -> None:
        for actor_id in ("code-1", "agent-1", "external-1", "evaluator-1"):
            with self.subTest(actor=actor_id):
                service, repository, _, run_id, _ = build_context()
                with self.assertRaises(AuthorityDenied):
                    service.decide(
                        decide_command(
                            run_id,
                            actor_id=actor_id,
                            atomicity_decision=decision(human_id=actor_id),
                        )
                    )
                self.assertEqual(repository.event_count(run_id), 5)
                self.assertEqual(repository.atomic_boundary_count, 0)

    def test_ac_06_unknown_expired_and_wrong_resource_humans_are_denied(self) -> None:
        for actor_id in ("unknown-human", "expired-1", "other-human"):
            with self.subTest(actor=actor_id):
                service, repository, _, run_id, _ = build_context()
                with self.assertRaises(AuthorityDenied):
                    service.decide(
                        decide_command(
                            run_id,
                            actor_id=actor_id,
                            atomicity_decision=decision(human_id=actor_id),
                        )
                    )
                self.assertEqual(repository.event_count(run_id), 5)
                self.assertEqual(repository.atomicity_receipt_count, 0)

    def test_ac_06_actor_and_decision_identity_must_match(self) -> None:
        service, repository, _, run_id, _ = build_context()
        with self.assertRaises(DecisionPackageIncomplete):
            service.decide(
                decide_command(
                    run_id,
                    actor_id="architect-1",
                    atomicity_decision=decision(human_id="other-human"),
                )
            )
        self.assertEqual(repository.event_count(run_id), 5)
        self.assertEqual(repository.atomic_boundary_count, 0)

    def test_ac_07_only_human_authority_can_reopen(self) -> None:
        for actor_id in ("code-1", "agent-1", "external-1", "evaluator-1"):
            with self.subTest(actor=actor_id):
                service, repository, _, run_id, _ = build_context()
                service.decide(decide_command(run_id))
                with self.assertRaises(AuthorityDenied):
                    service.reopen(reopen_command(run_id, actor_id=actor_id))
                self.assertEqual(repository.event_count(run_id), 9)
                self.assertEqual(repository.boundary_invalidation_count, 0)


if __name__ == "__main__":
    unittest.main()
