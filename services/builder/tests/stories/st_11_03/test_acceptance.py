from __future__ import annotations

import unittest

from cmf_builder.domain.implementation_feedback import OWNED_OBLIGATIONS, REQUIRED_FEEDBACK_KINDS
from tests.stories.st_11_03 import build_context, feedback_command


class ImplementationFeedbackAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service, _, _, self.repository, _, self.run_id, _, self.plan = build_context()
        self.receipt = self.service.govern(feedback_command(self.run_id))
        self.proposal = self.service.get_active(self.run_id)

    def test_compiles_one_immutable_proposal_and_receipt(self) -> None:
        self.assertEqual(self.repository.amendment_proposal_count, 1)
        self.assertEqual(self.repository.amendment_proposal_receipt_count, 1)
        self.proposal.validate(self.plan)
        self.receipt.validate(self.proposal)

    def test_covers_exact_obligations_and_feedback_kinds(self) -> None:
        self.assertEqual(self.proposal.obligation_ids, OWNED_OBLIGATIONS)
        self.assertEqual(tuple(item.feedback_kind for item in self.proposal.feedback_items), REQUIRED_FEEDBACK_KINDS)
        self.assertEqual(self.receipt.feedback_item_count, 3)
        self.assertEqual(self.receipt.obligation_count, 2)

    def test_every_feedback_item_is_traceable_and_actionable(self) -> None:
        for item in self.proposal.feedback_items:
            self.assertTrue(item.subject_ref)
            self.assertTrue(item.subject_hash.startswith("sha256:"))
            self.assertTrue(item.source_identity)
            self.assertEqual(len(item.evidence_refs), len(item.evidence_hashes))
            self.assertTrue(item.provenance)
            self.assertTrue(item.finding)
            self.assertTrue(item.recommendation)
            self.assertTrue(item.required_human_disposition)

    def test_proposal_does_not_mutate_or_approve_authority(self) -> None:
        self.assertEqual(self.proposal.proposal_status, "PROPOSED_NOT_RATIFIED")
        self.assertFalse(self.proposal.authority_mutated)
        self.assertFalse(self.proposal.implementation_authorized)
        self.assertFalse(self.proposal.production_eligible)
        self.assertFalse(self.proposal.certified)
        self.assertFalse(self.receipt.authority_mutated)


if __name__ == "__main__":
    unittest.main()

