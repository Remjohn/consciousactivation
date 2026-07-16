from __future__ import annotations

import unittest

from cmf_builder.application.ports import AtomicCommitFailed, IdempotencyPayloadMismatch
from cmf_builder.domain.atomic_harness_definition import (
    DefinitionAuthorityInvalid,
    DefinitionInputInvalid,
    DefinitionLineageInvalid,
    DefinitionScopeInvalid,
)
from tests.stories.st_07_02 import build_context, compile_command


class AtomicHarnessDefinitionFailureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service, _, self.repository, self.observations, self.run_id, _, _, _ = build_context(seed="ST-07.02-failure")

    def _assert_no_partial_state(self) -> None:
        self.assertEqual(self.repository.atomic_harness_definition_count, 0)
        self.assertEqual(self.repository.atomic_harness_definition_receipt_count, 0)
        self.assertIsNone(self.repository.load_run(self.run_id).atomic_harness_definition_ref)

    def test_missing_or_wrong_input_pin_fails_closed(self) -> None:
        with self.assertRaises(DefinitionInputInvalid):
            self.service.compile(compile_command(self.run_id, definition_input_sha256="0" * 64))
        self._assert_no_partial_state()

    def test_external_runtime_and_skill_injection_fail_closed(self) -> None:
        with self.assertRaises(DefinitionScopeInvalid):
            self.service.compile(compile_command(self.run_id, requested_external_runtime_ids=("runtime",)))
        with self.assertRaises(DefinitionScopeInvalid):
            self.service.compile(compile_command(self.run_id, command_id="skill-injection", requested_external_skill_ids=("skill",)))
        self._assert_no_partial_state()

    def test_production_certification_or_marker_removal_fails_closed(self) -> None:
        with self.assertRaises(DefinitionAuthorityInvalid):
            self.service.compile(compile_command(self.run_id, requested_production_eligible=True))
        with self.assertRaises(DefinitionAuthorityInvalid):
            self.service.compile(compile_command(self.run_id, command_id="certified", requested_certified=True))
        with self.assertRaises(DefinitionAuthorityInvalid):
            self.service.compile(compile_command(self.run_id, command_id="marker", requested_synthetic_not_certifiable=False))
        self._assert_no_partial_state()

    def test_unauthorized_actor_and_lineage_override_fail_closed(self) -> None:
        with self.assertRaises(DefinitionAuthorityInvalid):
            self.service.compile(compile_command(self.run_id, actor_id="architect-1"))
        with self.assertRaises(DefinitionLineageInvalid):
            self.service.compile(compile_command(self.run_id, command_id="override", lineage_overrides=(("ir_id", "foreign"),)))
        self._assert_no_partial_state()

    def test_atomic_failure_commits_nothing_and_allows_clean_retry(self) -> None:
        self.repository.inject_next_atomic_commit_failure()
        command = compile_command(self.run_id)
        with self.assertRaises(AtomicCommitFailed):
            self.service.compile(command)
        self._assert_no_partial_state()
        receipt = self.service.compile(command)
        self.assertEqual(receipt.stream_version, 23)
        self.assertEqual(self.repository.atomic_harness_definition_count, 1)

    def test_conflicting_repeat_command_fails_closed(self) -> None:
        command = compile_command(self.run_id)
        self.service.compile(command)
        before = self.repository.event_count(self.run_id)
        with self.assertRaises(IdempotencyPayloadMismatch):
            self.service.compile(compile_command(self.run_id, requested_operation="other"))
        self.assertEqual(self.repository.event_count(self.run_id), before)
        self.assertEqual(self.repository.atomic_harness_definition_count, 1)


if __name__ == "__main__":
    unittest.main()
