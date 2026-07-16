from __future__ import annotations

import unittest

from cmf_builder.application.ports import AtomicCommitFailed, IdempotencyPayloadMismatch
from cmf_builder.domain.development_capsule import (
    DevelopmentCapsuleAuthorityInvalid,
    DevelopmentCapsuleInputInvalid,
    DevelopmentCapsuleScopeInvalid,
    DevelopmentCapsuleTraceInvalid,
)
from tests.stories.st_11_01 import build_context, capsule_command


class DevelopmentCapsuleFailureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service, _, _, self.repository, self.observations, self.run_id, _, _, _ = build_context(seed="ST-11.01-failure")

    def _assert_no_partial_state(self) -> None:
        self.assertEqual(self.repository.development_capsule_count, 0)
        self.assertEqual(self.repository.development_capsule_receipt_count, 0)
        self.assertIsNone(self.repository.load_run(self.run_id).development_capsule_ref)

    def test_wrong_input_pin_or_incomplete_trace_fails_closed(self) -> None:
        with self.assertRaises(DevelopmentCapsuleInputInvalid):
            self.service.generate(capsule_command(self.run_id, capsule_input_sha256="0" * 64))
        with self.assertRaises(DevelopmentCapsuleInputInvalid):
            self.service.generate(capsule_command(self.run_id, command_id="missing-obligation", requested_obligations=("D029",)))
        self._assert_no_partial_state()

    def test_external_runtime_skill_or_product_implementation_fails_closed(self) -> None:
        with self.assertRaises(DevelopmentCapsuleScopeInvalid):
            self.service.generate(capsule_command(self.run_id, requested_external_runtime_ids=("runtime",)))
        with self.assertRaises(DevelopmentCapsuleScopeInvalid):
            self.service.generate(capsule_command(self.run_id, command_id="skill", requested_external_skill_ids=("skill",)))
        with self.assertRaises(DevelopmentCapsuleScopeInvalid):
            self.service.generate(capsule_command(self.run_id, command_id="implement", requested_generated_product_implementation=True))
        self._assert_no_partial_state()

    def test_production_certification_and_unauthorized_actor_fail_closed(self) -> None:
        with self.assertRaises(DevelopmentCapsuleAuthorityInvalid):
            self.service.generate(capsule_command(self.run_id, requested_production_eligible=True))
        with self.assertRaises(DevelopmentCapsuleAuthorityInvalid):
            self.service.generate(capsule_command(self.run_id, command_id="cert", requested_certified=True))
        with self.assertRaises(DevelopmentCapsuleAuthorityInvalid):
            self.service.generate(capsule_command(self.run_id, command_id="human", actor_id="architect-1"))
        self._assert_no_partial_state()

    def test_unjustified_override_fails_closed(self) -> None:
        with self.assertRaises(DevelopmentCapsuleTraceInvalid):
            self.service.generate(capsule_command(self.run_id, reference_overrides=(("notes", "value"),)))
        with self.assertRaises(DevelopmentCapsuleTraceInvalid):
            self.service.generate(capsule_command(self.run_id, command_id="scaffold", scaffolding_overrides=(("service", "because"),)))
        self._assert_no_partial_state()

    def test_missing_validated_parent_fails_closed(self) -> None:
        self.repository._atomic_content_harness_validation_reports.clear()
        with self.assertRaises(DevelopmentCapsuleTraceInvalid):
            self.service.generate(capsule_command(self.run_id))
        self._assert_no_partial_state()

    def test_atomic_failure_has_zero_partial_state_and_clean_retry(self) -> None:
        before_observations = len(self.observations.observations)
        self.repository.inject_next_atomic_commit_failure()
        command = capsule_command(self.run_id)
        with self.assertRaises(AtomicCommitFailed):
            self.service.generate(command)
        self._assert_no_partial_state()
        self.assertEqual(len(self.observations.observations), before_observations)
        receipt = self.service.generate(command)
        self.assertEqual(receipt.stream_version, 25)

    def test_conflicting_repeat_command_fails_closed(self) -> None:
        self.service.generate(capsule_command(self.run_id))
        before = self.repository.event_count(self.run_id)
        with self.assertRaises(IdempotencyPayloadMismatch):
            self.service.generate(capsule_command(self.run_id, requested_operation="other"))
        self.assertEqual(self.repository.event_count(self.run_id), before)
        self.assertEqual(self.repository.development_capsule_count, 1)


if __name__ == "__main__":
    unittest.main()
