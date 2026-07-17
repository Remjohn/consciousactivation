from __future__ import annotations

import unittest

from cmf_builder.domain.implementation_plan import OWNED_OBLIGATIONS, PLAN_OUTCOME
from tests.stories.st_11_02 import build_context, plan_command


class ImplementationPlanAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        (
            self.service,
            _,
            _,
            self.repository,
            self.observations,
            self.run_id,
            _,
            self.capsule,
        ) = build_context()
        self.receipt = self.service.compile(plan_command(self.run_id))
        self.plan = self.service.get_active(self.run_id)

    def test_compiles_one_immutable_plan_and_receipt(self) -> None:
        self.assertEqual(self.repository.implementation_plan_count, 1)
        self.assertEqual(self.repository.implementation_plan_receipt_count, 1)
        self.assertEqual(self.receipt.plan_id, self.plan.plan_id)
        self.assertEqual(self.receipt.outcome, PLAN_OUTCOME)
        self.plan.validate(self.capsule)
        self.receipt.validate(self.plan)

    def test_covers_exact_owned_obligations(self) -> None:
        self.assertEqual(self.plan.obligation_ids, OWNED_OBLIGATIONS)
        covered = {
            requirement
            for increment in self.plan.increments
            for requirement in increment.requirement_ids
        }
        self.assertEqual(covered, set(OWNED_OBLIGATIONS))
        self.assertEqual(self.receipt.obligation_count, 2)

    def test_has_three_vertical_user_observable_outcomes(self) -> None:
        self.assertEqual(len(self.plan.increments), 3)
        self.assertTrue(all(item.one_focused_context for item in self.plan.increments))
        self.assertTrue(all(item.user_observable for item in self.plan.increments))
        self.assertTrue(all(item.acceptance_evidence for item in self.plan.increments))
        self.assertTrue(all(item.test_ids for item in self.plan.increments))
        self.assertTrue(all(item.observability_evidence for item in self.plan.increments))
        self.assertTrue(all(item.rollback_requirements for item in self.plan.increments))

    def test_dependencies_are_backward_only_and_first_slice_is_runnable(self) -> None:
        ids: list[str] = []
        for increment in self.plan.increments:
            self.assertTrue(set(increment.depends_on).issubset(ids))
            ids.append(increment.increment_id)
        self.assertEqual(self.plan.first_working_increment_id, ids[0])
        self.assertEqual(self.plan.increments[0].depends_on, ())

    def test_plan_is_handoff_only_and_nonproduction(self) -> None:
        self.assertFalse(self.plan.implementation_authorized)
        self.assertFalse(self.plan.production_eligible)
        self.assertFalse(self.plan.certified)
        self.assertFalse(self.receipt.implementation_authorized)
        self.assertEqual(
            self.plan.external_target_compatibility,
            "NOT_EVALUATED_EXTERNAL_TARGET_BRANCH",
        )


if __name__ == "__main__":
    unittest.main()

