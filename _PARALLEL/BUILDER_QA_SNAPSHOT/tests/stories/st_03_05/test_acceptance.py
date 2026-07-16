from __future__ import annotations

import unittest

from cmf_builder.domain.constitutional_validation import (
    AUTHORITY_ORDER,
    BUILDER_PRD_AMENDMENT_SHA256,
    CONSTITUTION_SHA256,
    POLICY_SHA256,
)
from cmf_builder.domain.generated_artifacts import ARTIFACT_PATHS
from cmf_builder.domain.harness_ir import ACTIVATIVE_LINEAGE_PATHS
from cmf_builder.domain.run import LifecycleState
from tests.stories.st_03_05 import build_context, validate_command


class ConstitutionalAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        (
            self.service,
            _,
            self.repository,
            self.observations,
            self.run_id,
            self.artifact_receipt,
        ) = build_context()
        self.receipt = self.service.validate(validate_command(self.run_id))
        self.report = self.repository.get_constitutional_validation_report(
            self.receipt.report_id
        )
        assert self.report is not None

    def test_validates_exact_active_artifact_set(self) -> None:
        self.assertEqual(self.report.artifact_set_id, self.artifact_receipt.artifact_set_id)
        self.assertEqual(self.report.manifest_id, self.artifact_receipt.manifest_id)
        self.assertEqual(self.report.coverage, ARTIFACT_PATHS)
        self.assertEqual(len(self.report.coverage), 21)
        self.assertEqual(self.report.outcome, "PASS")
        self.assertFalse(self.report.findings)

    def test_pins_authorities_and_precedence_order(self) -> None:
        self.assertEqual(self.report.policy_hash, POLICY_SHA256)
        self.assertEqual(self.report.constitution_hash, CONSTITUTION_SHA256)
        self.assertEqual(
            self.report.builder_prd_amendment_hash, BUILDER_PRD_AMENDMENT_SHA256
        )
        self.assertEqual(self.report.authority_order, AUTHORITY_ORDER)

    def test_preserves_all_rich_lineage_keys_as_separate_nodes(self) -> None:
        ir = self.repository.get_harness_ir(self.report.ir_id)
        assert ir is not None
        self.assertEqual(
            self.report.rich_lineage_paths, tuple(sorted(ACTIVATIVE_LINEAGE_PATHS))
        )
        for path in ACTIVATIVE_LINEAGE_PATHS:
            value = ir.value(path)
            self.assertIsNone(value.value)
            self.assertEqual(value.knowledge_status, "NOT_APPLICABLE")
            self.assertEqual(value.authority_status, "NOT_APPLICABLE")

    def test_run_remains_genesis_and_replays_validation_reference(self) -> None:
        run = self.repository.load_run(self.run_id)
        self.assertIs(run.lifecycle_state, LifecycleState.GENESIS)
        self.assertEqual(run.stream_version, 13)
        self.assertEqual(run.constitutional_validation_ref, self.report.report_id)
        self.assertEqual(run.constitutional_validation_hash, self.report.report_hash)
        self.assertIsNone(run.constitutional_validation_invalidation_ref)

    def test_report_and_receipt_are_content_addressed(self) -> None:
        self.report.validate()
        self.receipt.validate(self.report)
        self.assertTrue(self.report.report_id.removeprefix("constitutional-report_") in self.report.report_hash)
        self.assertTrue(self.receipt.receipt_id.removeprefix("constitutional-receipt_") in self.receipt.receipt_hash)

    def test_required_observations_are_complete_and_payload_free(self) -> None:
        observations = [
            item
            for item in self.observations.observations
            if item.story_id == "ST-03.05"
        ]
        names = {item.event_name for item in observations}
        self.assertTrue(
            {
                "ST-03.05:ConstitutionalValidationCompleted",
                "ST-03.05:CrossArtifactCompletenessValidated",
                "ST-03.05:ConstitutionalPrecedenceValidated",
                "ST-03.05:OutcomeVerified",
            }
            <= names
        )
        for item in observations:
            self.assertEqual(item.constitutional_report_id, self.report.report_id)
            self.assertEqual(item.constitutional_receipt_id, self.receipt.receipt_id)
            self.assertEqual(item.constitutional_coverage_count, 21)
            self.assertNotIn("source_nodes", repr(item.failure_context))


if __name__ == "__main__":
    unittest.main()
