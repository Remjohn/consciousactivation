from __future__ import annotations

import unittest

from cmf_builder.application.ports import AtomicCommitFailed, IdempotencyPayloadMismatch
from cmf_builder.domain.target_package_validation import (
    TargetValidationAuthorityInvalid,
    TargetValidationInputInvalid,
    TargetValidationLineageInvalid,
    TargetValidationScopeInvalid,
)
from tests.stories.st_07_04 import build_context, validation_command


class AtomicContentHarnessValidationFailureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service, _, _, self.repository, self.observations, self.run_id, _, _ = build_context(seed="ST-07.04-failure")

    def _assert_no_partial_state(self) -> None:
        self.assertEqual(self.repository.atomic_content_harness_validation_report_count, 0)
        self.assertEqual(self.repository.atomic_content_harness_validation_receipt_count, 0)
        self.assertIsNone(
            self.repository.load_run(self.run_id).atomic_content_harness_validation_ref
        )

    def test_wrong_policy_or_target_fails_closed(self) -> None:
        with self.assertRaises(TargetValidationInputInvalid):
            self.service.validate(validation_command(self.run_id, policy_sha256="0" * 64))
        with self.assertRaises(TargetValidationInputInvalid):
            self.service.validate(validation_command(self.run_id, command_id="wrong-target", requested_target_kind="visual_asset_demand"))
        self._assert_no_partial_state()

    def test_external_compatibility_promotion_and_field_flattening_fail_closed(self) -> None:
        with self.assertRaises(TargetValidationScopeInvalid):
            self.service.validate(validation_command(self.run_id, requested_external_target_compatibility="PASS"))
        with self.assertRaises(TargetValidationLineageInvalid):
            self.service.validate(validation_command(self.run_id, command_id="flatten", field_overrides=(("generic_notes", "external"),)))
        self._assert_no_partial_state()

    def test_production_certification_and_unauthorized_actor_fail_closed(self) -> None:
        with self.assertRaises(TargetValidationAuthorityInvalid):
            self.service.validate(validation_command(self.run_id, requested_production_eligible=True))
        with self.assertRaises(TargetValidationAuthorityInvalid):
            self.service.validate(validation_command(self.run_id, command_id="certified", requested_certified=True))
        with self.assertRaises(TargetValidationAuthorityInvalid):
            self.service.validate(validation_command(self.run_id, command_id="human", actor_id="architect-1"))
        self._assert_no_partial_state()

    def test_missing_definition_fails_closed(self) -> None:
        self.repository._atomic_harness_definitions.clear()
        with self.assertRaises(TargetValidationLineageInvalid):
            self.service.validate(validation_command(self.run_id))
        self._assert_no_partial_state()

    def test_atomic_failure_has_zero_partial_state_and_clean_retry(self) -> None:
        before_observations = len(self.observations.observations)
        self.repository.inject_next_atomic_commit_failure()
        command = validation_command(self.run_id)
        with self.assertRaises(AtomicCommitFailed):
            self.service.validate(command)
        self._assert_no_partial_state()
        self.assertEqual(len(self.observations.observations), before_observations)
        receipt = self.service.validate(command)
        self.assertEqual(receipt.stream_version, 24)

    def test_conflicting_repeat_command_fails_closed(self) -> None:
        self.service.validate(validation_command(self.run_id))
        before = self.repository.event_count(self.run_id)
        with self.assertRaises(IdempotencyPayloadMismatch):
            self.service.validate(validation_command(self.run_id, requested_operation="other"))
        self.assertEqual(self.repository.event_count(self.run_id), before)
        self.assertEqual(self.repository.atomic_content_harness_validation_report_count, 1)


if __name__ == "__main__":
    unittest.main()
