from __future__ import annotations

import unittest

from cmf_builder.domain.atomic_harness_definition import REQUIRED_SECTIONS
from cmf_builder.domain.target_package_validation import (
    EXTERNAL_TARGET_COMPATIBILITY,
    REQUIRED_VALIDATION_DIMENSIONS,
)
from tests.stories.st_07_04 import build_context, validation_command


class AtomicContentHarnessValidationAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        (
            self.service,
            _,
            _,
            self.repository,
            self.observations,
            self.run_id,
            _,
            self.definition,
        ) = build_context()
        self.receipt = self.service.validate(validation_command(self.run_id))
        self.report = self.service.get_active(self.run_id)

    def test_ac_01_commits_one_independent_report_and_receipt(self) -> None:
        self.assertEqual(self.repository.atomic_content_harness_validation_report_count, 1)
        self.assertEqual(self.repository.atomic_content_harness_validation_receipt_count, 1)
        self.assertEqual(self.receipt.stream_version, 24)
        self.assertEqual(self.receipt.report_id, self.report.report_id)
        self.receipt.validate(self.report)
        self.report.validate(self.definition)

    def test_ac_02_03_proves_complete_artifacts_and_all_gates(self) -> None:
        self.assertEqual(self.report.section_ids, REQUIRED_SECTIONS)
        self.assertEqual(
            tuple(item.dimension_id for item in self.report.dimensions),
            REQUIRED_VALIDATION_DIMENSIONS,
        )
        self.assertTrue(all(item.verdict == "PASS" for item in self.report.dimensions))
        self.assertEqual(len(self.report.capability_ids), 5)
        self.assertEqual(len(self.report.module_ids), 2)
        self.assertEqual(len(self.report.phase_ids), 2)
        self.assertEqual(len(self.report.context_manifest_ids), 2)

    def test_ac_04_05_preserves_target_separation_and_compatibility_scope(self) -> None:
        self.assertEqual(self.report.target_kind, "atomic_content_harness")
        self.assertEqual(self.report.category_binding, "none")
        self.assertEqual(self.report.internal_compatibility, "PASS")
        self.assertEqual(
            self.report.external_target_compatibility,
            EXTERNAL_TARGET_COMPATIBILITY,
        )
        self.assertNotIn("delegation", self.report.canonical_bytes().decode("utf-8").lower())
        self.assertNotIn("visual_asset", self.report.canonical_bytes().decode("utf-8").lower())

    def test_ac_06_07_preserves_noncertification_authority_and_lineage(self) -> None:
        self.assertFalse(self.report.production_eligible)
        self.assertFalse(self.report.certified)
        self.assertTrue(self.report.synthetic_not_certifiable)
        self.assertEqual(self.report.authority_identity, "code-1")
        for value in (
            self.definition.definition_id,
            self.definition.definition_hash,
            self.definition.constitutional_report_hash,
            self.definition.ratification_hash,
        ):
            self.assertIn(value, self.report.lineage)

    def test_ac_12_observations_are_complete_and_deterministic(self) -> None:
        story = [item for item in self.observations.observations if item.story_id == "ST-07.04"]
        self.assertEqual(len(story), 10)
        self.assertEqual(story[0].event_name, "atomic_content_harness_validation_started")
        self.assertEqual(story[-1].event_name, "atomic_content_harness_validation_committed")
        for item in story:
            self.assertEqual(item.atomic_content_harness_validation_id, self.report.report_id)
            self.assertEqual(item.atomic_content_harness_validation_dimension_count, 8)
            self.assertEqual(item.atomic_content_harness_external_compatibility, EXTERNAL_TARGET_COMPATIBILITY)


if __name__ == "__main__":
    unittest.main()
