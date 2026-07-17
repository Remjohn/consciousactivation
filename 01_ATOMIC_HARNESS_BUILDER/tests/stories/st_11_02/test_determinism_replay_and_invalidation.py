from __future__ import annotations

import unittest

from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.domain.implementation_plan import ImplementationPlanInvalidatedError
from tests.stories.st_11_02 import build_context, plan_command


class ImplementationPlanDeterminismReplayTests(unittest.TestCase):
    def _complete(self, seed: str = "ST-11.02-determinism"):
        service, _, atomicity, repository, observations, run_id, _, _ = build_context(seed=seed)
        receipt = service.compile(plan_command(run_id))
        return service, atomicity, repository, observations, run_id, receipt, service.get_active(run_id)

    def test_identical_fresh_contexts_are_byte_identical(self) -> None:
        first = self._complete(seed="ST-11.02-fresh")
        second = self._complete(seed="ST-11.02-fresh")
        self.assertEqual(first[-1].canonical_bytes(), second[-1].canonical_bytes())
        self.assertEqual(first[-2].canonical_bytes(), second[-2].canonical_bytes())

    def test_repeat_command_returns_original_receipt_without_duplicate_state(self) -> None:
        service, _, repository, observations, run_id, receipt, plan = self._complete()
        self.assertEqual(service.compile(plan_command(run_id)), receipt)
        self.assertEqual(repository.implementation_plan_count, 1)
        self.assertEqual(service.get_active(run_id), plan)
        self.assertEqual(observations.observations[-1].event_name, "implementation_plan_compilation_replayed")

    def test_upstream_invalidation_disables_active_plan_and_preserves_history(self) -> None:
        service, atomicity, repository, _, run_id, _, plan = self._complete(seed="ST-11.02-invalidation")
        atomicity.reopen(ReopenAtomicBoundaryCommand(
            command_id="reopen-after-plan", run_id=run_id, actor_id="architect-1",
            expected_version=25, correlation_id="st-11-02-reopen",
            causation_id=plan.plan_id, reason="Authorized upstream correction.",
        ))
        self.assertTrue(repository.is_implementation_plan_invalidated(plan.plan_id))
        with self.assertRaises(ImplementationPlanInvalidatedError):
            service.get_active(run_id)
        self.assertEqual(service.get_historical(plan.plan_id).canonical_bytes(), plan.canonical_bytes())


if __name__ == "__main__":
    unittest.main()

