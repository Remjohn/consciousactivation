from __future__ import annotations

import unittest

from cmf_builder.domain.atomic_harness_definition import (
    ACCEPTANCE_TEST_DECLARATIONS,
    CATEGORY_ADAPTER_REF,
    CLASSIFICATION,
    REQUIRED_SECTIONS,
)
from tests.stories.st_07_02 import build_context, compile_command


class GenericAtomicContentHarnessAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        (
            self.service,
            _,
            self.repository,
            self.observations,
            self.run_id,
            _,
            self.necessity,
            _,
        ) = build_context()
        self.receipt = self.service.compile(compile_command(self.run_id))
        self.definition = self.service.get_active(self.run_id)

    def test_ac_01_commits_exactly_one_definition_and_receipt(self) -> None:
        self.assertEqual(self.repository.atomic_harness_definition_count, 1)
        self.assertEqual(self.repository.atomic_harness_definition_receipt_count, 1)
        self.assertEqual(self.receipt.stream_version, 23)
        self.assertEqual(self.receipt.definition_id, self.definition.definition_id)
        self.assertEqual(
            self.receipt.initial_atomic_harness_definition_milestone, "PASS"
        )
        self.receipt.validate(self.definition)

    def test_ac_01_07_has_complete_required_contract_sections(self) -> None:
        self.assertEqual(
            tuple(item.section_id for item in self.definition.sections),
            REQUIRED_SECTIONS,
        )
        self.assertTrue(all(item.applicability == "REQUIRED" for item in self.definition.sections))
        self.assertEqual(
            self.definition.acceptance_test_declarations,
            ACCEPTANCE_TEST_DECLARATIONS,
        )
        self.assertEqual(self.definition.task_id, "synthetic_utf8_line_ending_normalization")
        self.assertIn("UTF-8", self.definition.input_contract)
        self.assertIn("exactly one terminal newline", self.definition.output_contract)

    def test_ac_02_05_preserves_exact_upstream_lineage(self) -> None:
        run = self.repository.load_run(self.run_id)
        self.assertEqual(self.definition.source_lock_ref, run.source_lock_ref)
        self.assertEqual(self.definition.ir_id, run.harness_ir_ref)
        self.assertEqual(self.definition.constitutional_report_id, run.constitutional_validation_ref)
        self.assertEqual(self.definition.minimum_context_graph_id, run.minimum_context_ref)
        self.assertEqual(self.definition.skill_necessity_decision_id, self.necessity.decision_id)
        self.assertIn(self.necessity.decision_hash, self.definition.lineage)

    def test_ac_04_plan_is_governed_but_not_executed(self) -> None:
        self.assertTrue(self.definition.capability_ids)
        self.assertTrue(self.definition.module_ids)
        self.assertTrue(self.definition.phase_ids)
        self.assertTrue(self.definition.context_manifest_ids)
        self.assertEqual(
            self.definition.workflow_declaration,
            "PHASE_GRAPH_PLAN_ONLY_NOT_EXECUTED",
        )
        self.assertFalse(self.definition.execution_performed)
        self.assertFalse(self.definition.development_capsule_generated)

    def test_ac_05_06_is_synthetic_category_neutral_and_zero_dependency(self) -> None:
        self.assertEqual(self.definition.harness_id, "synthetic_text_normalization_v1")
        self.assertEqual(self.definition.category_binding, "none")
        self.assertEqual(self.definition.category_adapter_ref, CATEGORY_ADAPTER_REF)
        self.assertEqual(self.definition.classification, CLASSIFICATION)
        self.assertEqual(self.definition.external_skill_count, 0)
        self.assertEqual(self.definition.external_runtime_count, 0)
        self.assertFalse(self.definition.dynamic_skill_discovery_allowed)
        self.assertFalse(self.definition.production_eligible)
        self.assertFalse(self.definition.certified)
        self.assertTrue(self.definition.synthetic_not_certifiable)

    def test_ac_12_observations_prove_identity_scope_and_milestone(self) -> None:
        story = [item for item in self.observations.observations if item.story_id == "ST-07.02"]
        self.assertEqual(
            {item.event_name for item in story},
            {
                "synthetic_atomic_harness_definition_started",
                "synthetic_atomic_harness_definition_validated",
                "synthetic_atomic_harness_definition_committed",
            },
        )
        for item in story:
            self.assertEqual(item.atomic_harness_definition_id, self.definition.definition_id)
            self.assertEqual(item.atomic_harness_definition_receipt_id, self.receipt.receipt_id)
            self.assertEqual(item.atomic_harness_definition_section_count, len(REQUIRED_SECTIONS))
            self.assertEqual(item.atomic_harness_definition_external_skill_count, 0)
            self.assertEqual(item.atomic_harness_definition_external_runtime_count, 0)
            self.assertEqual(item.atomic_harness_definition_milestone, "PASS")


if __name__ == "__main__":
    unittest.main()
