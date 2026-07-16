from __future__ import annotations

import unittest

from cmf_builder.domain.atomicity import (
    AuthorityStatus,
    AtomicityDecisionAction,
    BoundaryStatus,
    KnowledgeStatus,
    ModelStatus,
)
from cmf_builder.domain.run import LifecycleState
from tests.stories.st_02_05 import (
    build_context,
    decide_command,
    decision,
)


class AtomicityAcceptanceTests(unittest.TestCase):
    def test_ac_01_02_approval_ratifies_freezes_and_compiles_atomically(self) -> None:
        service, repository, _, run_id, source_receipt = build_context()
        receipt = service.decide(decide_command(run_id))

        run = repository.load_run(run_id)
        boundary = repository.get_atomic_boundary(receipt.boundary_ref)
        model = repository.get_draft_harness_model(receipt.model_ref)
        ratification = repository.get_atomicity_ratification(receipt.ratification_ref)
        self.assertEqual(receipt.decision_status, "APPROVED")
        self.assertEqual(receipt.hg_003_result, "PASS")
        self.assertEqual(run.lifecycle_state, LifecycleState.ATOMICITY_RATIFICATION)
        self.assertEqual(run.stream_version, 9)
        self.assertEqual(run.source_lock_ref, source_receipt.source_lock_ref)
        self.assertEqual(run.atomic_boundary_ref, receipt.boundary_ref)
        self.assertEqual(run.draft_harness_model_ref, receipt.model_ref)
        self.assertEqual(boundary.status, BoundaryStatus.FROZEN)
        self.assertEqual(model.status, ModelStatus.UNRATIFIED_CONSTITUTIONAL_FIELDS)
        self.assertEqual(ratification.human_id, "architect-1")
        self.assertEqual(len(receipt.event_ids), 4)

    def test_ac_03_model_exposes_every_field_authority_and_knowledge_status(self) -> None:
        service, repository, _, run_id, _ = build_context()
        receipt = service.decide(decide_command(run_id))
        model = repository.get_draft_harness_model(receipt.model_ref)
        fields = {field.name: field for field in model.fields}

        self.assertEqual(len(fields), 19)
        self.assertEqual(fields["atomic_boundary"].authority_status, AuthorityStatus.HUMAN_RATIFIED)
        self.assertEqual(fields["atomic_boundary"].knowledge_status, KnowledgeStatus.LOCKED_EVIDENCE)
        for name in ("visual_syntax", "composition_variables", "sequence_grammar", "draft_activative_intelligence", "category_native_evaluation", "production_repair_policy"):
            self.assertEqual(fields[name].authority_status, AuthorityStatus.NOT_APPLICABLE)
            self.assertEqual(fields[name].knowledge_status, KnowledgeStatus.NOT_APPLICABLE)
        for name in ("phase_hypotheses", "runtime_hypotheses", "evaluation_hypotheses", "repair_hypotheses"):
            self.assertEqual(fields[name].authority_status, AuthorityStatus.UNRATIFIED)
            self.assertEqual(fields[name].knowledge_status, KnowledgeStatus.HYPOTHESIS)
        self.assertEqual(set(model.decisions_required), {"phase_hypotheses", "runtime_hypotheses", "evaluation_hypotheses", "repair_hypotheses"})

    def test_ac_02_09_fresh_context_compilation_and_receipt_are_deterministic(self) -> None:
        service_a, repository_a, _, run_a, _ = build_context(seed="deterministic")
        service_b, repository_b, _, run_b, _ = build_context(seed="deterministic")
        receipt_a = service_a.decide(decide_command(run_a))
        receipt_b = service_b.decide(decide_command(run_b))

        model_a = repository_a.get_draft_harness_model(receipt_a.model_ref)
        model_b = repository_b.get_draft_harness_model(receipt_b.model_ref)
        self.assertEqual(receipt_a.receipt_hash, receipt_b.receipt_hash)
        self.assertEqual(model_a.model_hash, model_b.model_hash)
        self.assertEqual(receipt_a, receipt_b)

    def test_ac_01_10_source_lock_and_nonproduction_scope_are_preserved(self) -> None:
        service, repository, _, run_id, source_receipt = build_context()
        before = repository.get_source_lock(source_receipt.source_lock_ref)
        receipt = service.decide(decide_command(run_id))
        after = repository.get_source_lock(source_receipt.source_lock_ref)
        boundary = repository.get_atomic_boundary(receipt.boundary_ref)

        self.assertEqual(before, after)
        self.assertEqual(repository.source_lock_count, 1)
        self.assertTrue(boundary.synthetic)
        self.assertTrue(boundary.repository_owned)
        self.assertFalse(boundary.production_eligible)
        self.assertFalse(boundary.certified)
        self.assertEqual(boundary.category_binding, "none")
        self.assertIn("do not execute", boundary.boundary)

    def test_ac_05_revise_and_reject_record_decisions_without_freezing(self) -> None:
        for action, status in (
            (AtomicityDecisionAction.REVISE, "REVISION_REQUIRED"),
            (AtomicityDecisionAction.REJECT, "REJECTED"),
        ):
            with self.subTest(action=action):
                service, repository, _, run_id, _ = build_context()
                receipt = service.decide(
                    decide_command(run_id, atomicity_decision=decision(action))
                )
                run = repository.load_run(run_id)
                self.assertEqual(receipt.decision_status, status)
                self.assertEqual(receipt.hg_003_result, "FAIL")
                self.assertIsNone(receipt.boundary_ref)
                self.assertIsNone(receipt.model_ref)
                self.assertEqual(run.lifecycle_state, LifecycleState.SOURCE_LOCKED)
                self.assertEqual(run.stream_version, 6)
                self.assertEqual(repository.atomic_boundary_count, 0)
                self.assertEqual(repository.draft_harness_model_count, 0)


if __name__ == "__main__":
    unittest.main()
