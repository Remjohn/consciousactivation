from __future__ import annotations

import json
import unittest

from cmf_builder.application.ports import AtomicCommitFailed, IdempotencyPayloadMismatch
from cmf_builder.domain.implementation_feedback import (
    FEEDBACK_INPUT_PATH,
    AuthorityAmendmentProposal,
    ImplementationFeedbackAuthorityInvalid,
    ImplementationFeedbackInputInvalid,
)
from tests.stories.st_01_01_synthetic_proof import ROOT
from tests.stories.st_11_03 import build_context, feedback_command


class ImplementationFeedbackFailureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service, _, _, self.repository, _, self.run_id, _, self.plan = build_context(seed="ST-11.03-failure")

    def _assert_empty(self) -> None:
        self.assertEqual(self.repository.amendment_proposal_count, 0)
        self.assertEqual(self.repository.amendment_proposal_receipt_count, 0)

    def test_wrong_pin_and_contract_fail_closed(self) -> None:
        with self.assertRaises(ImplementationFeedbackInputInvalid):
            self.service.govern(feedback_command(self.run_id, feedback_input_sha256="0" * 64))
        with self.assertRaises(ImplementationFeedbackInputInvalid):
            self.service.govern(feedback_command(self.run_id, command_id="bad", requested_obligations=("FR-158",)))
        self._assert_empty()

    def test_apply_ratify_mutate_production_and_certification_fail_closed(self) -> None:
        for index, kwargs in enumerate((
            {"requested_apply_proposal": True}, {"requested_ratified": True},
            {"requested_authority_mutation": True}, {"requested_production_eligible": True},
            {"requested_certified": True},
        )):
            with self.assertRaises(ImplementationFeedbackAuthorityInvalid):
                self.service.govern(feedback_command(self.run_id, command_id=f"authority-{index}", **kwargs))
        self._assert_empty()

    def test_non_code_actor_and_override_fail_closed(self) -> None:
        with self.assertRaises(ImplementationFeedbackAuthorityInvalid):
            self.service.govern(feedback_command(self.run_id, actor_id="architect-1"))
        with self.assertRaises(Exception):
            self.service.govern(feedback_command(self.run_id, command_id="override", feedback_overrides=(("finding", "changed"),)))
        self._assert_empty()

    def test_missing_provenance_or_unsupported_kind_fails_domain_validation(self) -> None:
        value = json.loads((ROOT / FEEDBACK_INPUT_PATH).read_text(encoding="utf-8"))
        value["feedback_items"][0]["provenance"] = ""
        with self.assertRaises(ImplementationFeedbackInputInvalid):
            AuthorityAmendmentProposal.create(plan=self.plan, feedback_input=value, authority_identity="code-1")
        value = json.loads((ROOT / FEEDBACK_INPUT_PATH).read_text(encoding="utf-8"))
        value["feedback_items"][0]["feedback_kind"] = "UNKNOWN"
        with self.assertRaises(ImplementationFeedbackInputInvalid):
            AuthorityAmendmentProposal.create(plan=self.plan, feedback_input=value, authority_identity="code-1")

    def test_atomic_failure_has_zero_partial_state_and_clean_retry(self) -> None:
        self.repository.inject_next_atomic_commit_failure()
        command = feedback_command(self.run_id)
        with self.assertRaises(AtomicCommitFailed):
            self.service.govern(command)
        self._assert_empty()
        self.assertIsNone(self.repository.get_command_record(command.command_id))
        self.assertEqual(self.service.govern(command).feedback_item_count, 3)

    def test_repeat_is_idempotent_and_conflicting_payload_fails(self) -> None:
        receipt = self.service.govern(feedback_command(self.run_id))
        self.assertEqual(self.service.govern(feedback_command(self.run_id)), receipt)
        with self.assertRaises(IdempotencyPayloadMismatch):
            self.service.govern(feedback_command(self.run_id, requested_operation="other"))

    def test_fresh_context_proposal_and_receipt_are_byte_identical(self) -> None:
        first = build_context(seed="ST-11.03-fresh")
        second = build_context(seed="ST-11.03-fresh")
        first_receipt = first[0].govern(feedback_command(first[5]))
        second_receipt = second[0].govern(feedback_command(second[5]))
        self.assertEqual(first[0].get_active(first[5]).canonical_bytes(), second[0].get_active(second[5]).canonical_bytes())
        self.assertEqual(first_receipt.canonical_bytes(), second_receipt.canonical_bytes())


if __name__ == "__main__":
    unittest.main()

