from __future__ import annotations

from dataclasses import replace
import json
import unittest

from cmf_builder.application.ports import AtomicCommitFailed, IdempotencyPayloadMismatch
from cmf_builder.domain.implementation_plan import (
    PLAN_INPUT_PATH,
    ImplementationPlanAuthorityInvalid,
    ImplementationPlanInputInvalid,
    ImplementationPlanScopeInvalid,
    VerticalImplementationPlan,
)
from tests.stories.st_01_01_synthetic_proof import ROOT
from tests.stories.st_11_02 import build_context, plan_command


class ImplementationPlanFailureAuthorityTests(unittest.TestCase):
    def setUp(self) -> None:
        (
            self.service,
            _,
            _,
            self.repository,
            _,
            self.run_id,
            _,
            self.capsule,
        ) = build_context(seed="ST-11.02-failure")

    def _assert_empty(self) -> None:
        self.assertEqual(self.repository.implementation_plan_count, 0)
        self.assertEqual(self.repository.implementation_plan_receipt_count, 0)

    def test_wrong_pin_and_command_contract_fail_closed(self) -> None:
        with self.assertRaises(ImplementationPlanInputInvalid):
            self.service.compile(plan_command(self.run_id, plan_input_sha256="0" * 64))
        with self.assertRaises(ImplementationPlanInputInvalid):
            self.service.compile(plan_command(self.run_id, command_id="bad", requested_obligations=("FR-156",)))
        self._assert_empty()

    def test_implementation_production_and_certification_claims_fail_closed(self) -> None:
        with self.assertRaises(ImplementationPlanAuthorityInvalid):
            self.service.compile(plan_command(self.run_id, requested_implementation_authorized=True))
        with self.assertRaises(ImplementationPlanAuthorityInvalid):
            self.service.compile(plan_command(self.run_id, command_id="prod", requested_production_eligible=True))
        with self.assertRaises(ImplementationPlanAuthorityInvalid):
            self.service.compile(plan_command(self.run_id, command_id="cert", requested_certified=True))
        self._assert_empty()

    def test_external_runtime_skill_and_override_fail_closed(self) -> None:
        with self.assertRaises(ImplementationPlanScopeInvalid):
            self.service.compile(plan_command(self.run_id, requested_external_runtime_ids=("runtime",)))
        with self.assertRaises(ImplementationPlanScopeInvalid):
            self.service.compile(plan_command(self.run_id, command_id="skill", requested_external_skill_ids=("skill",)))
        with self.assertRaises(Exception):
            self.service.compile(plan_command(self.run_id, command_id="override", requested_increment_overrides=(("VI-001", "changed"),)))
        self._assert_empty()

    def test_non_code_actor_fails_closed(self) -> None:
        with self.assertRaises(ImplementationPlanAuthorityInvalid):
            self.service.compile(plan_command(self.run_id, actor_id="architect-1"))
        self._assert_empty()

    def test_forward_dependency_and_horizontal_layer_fail_domain_validation(self) -> None:
        value = json.loads((ROOT / PLAN_INPUT_PATH).read_text(encoding="utf-8"))
        value["increments"][0]["depends_on"] = ["VI-002"]
        with self.assertRaises(ImplementationPlanInputInvalid):
            VerticalImplementationPlan.create(capsule=self.capsule, plan_input=value, authority_identity="code-1")
        value = json.loads((ROOT / PLAN_INPUT_PATH).read_text(encoding="utf-8"))
        value["increments"][0]["outcome"] = "database"
        with self.assertRaises(ImplementationPlanScopeInvalid):
            VerticalImplementationPlan.create(capsule=self.capsule, plan_input=value, authority_identity="code-1")

    def test_atomic_failure_has_zero_partial_state_and_clean_retry(self) -> None:
        self.repository.inject_next_atomic_commit_failure()
        command = plan_command(self.run_id)
        with self.assertRaises(AtomicCommitFailed):
            self.service.compile(command)
        self._assert_empty()
        self.assertIsNone(self.repository.get_command_record(command.command_id))
        receipt = self.service.compile(command)
        self.assertEqual(receipt.increment_count, 3)

    def test_conflicting_repeat_command_fails_closed(self) -> None:
        self.service.compile(plan_command(self.run_id))
        with self.assertRaises(IdempotencyPayloadMismatch):
            self.service.compile(plan_command(self.run_id, requested_operation="other"))
        self.assertEqual(self.repository.implementation_plan_count, 1)


if __name__ == "__main__":
    unittest.main()

