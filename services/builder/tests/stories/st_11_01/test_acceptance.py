from __future__ import annotations

import unittest

from cmf_builder.domain.development_capsule import (
    DIRECT_DEPENDENCIES,
    OWNED_OBLIGATIONS,
    REQUIRED_CAPSULE_SECTIONS,
    REQUIRED_TEST_CLASSES,
)
from tests.stories.st_11_01 import build_context, capsule_command


class DevelopmentCapsuleAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        (
            self.service,
            _,
            _,
            self.repository,
            self.observations,
            self.run_id,
            _,
            self.validation,
            self.definition,
        ) = build_context()
        self.receipt = self.service.generate(capsule_command(self.run_id))
        self.capsule = self.service.get_active(self.run_id)

    def test_ac_01_commits_one_versioned_capsule_and_receipt(self) -> None:
        self.assertEqual(self.repository.development_capsule_count, 1)
        self.assertEqual(self.repository.development_capsule_receipt_count, 1)
        self.assertEqual(self.receipt.stream_version, 25)
        self.assertEqual(self.receipt.capsule_id, self.capsule.capsule_id)
        self.receipt.validate(self.capsule)
        self.capsule.validate(self.definition, self.validation)

    def test_ac_02_preserves_six_owned_obligations_and_dependency_order(self) -> None:
        self.assertEqual(self.capsule.obligation_ids, OWNED_OBLIGATIONS)
        self.assertEqual(self.capsule.dependency_order, DIRECT_DEPENDENCIES)
        self.assertEqual(self.receipt.obligation_count, 6)

    def test_ac_03_through_07_provides_complete_authority(self) -> None:
        self.assertEqual(
            tuple(item.section_id for item in self.capsule.sections),
            REQUIRED_CAPSULE_SECTIONS,
        )
        self.assertEqual(self.capsule.test_classes, REQUIRED_TEST_CLASSES)
        self.assertEqual(len(self.capsule.scaffolding), 3)
        self.assertGreaterEqual(len(self.capsule.references), 20)
        self.assertTrue(all(item.reference_ids for item in self.capsule.sections))

    def test_ac_12_is_explicitly_synthetic_and_noncertifiable(self) -> None:
        self.assertTrue(self.capsule.repository_owned)
        self.assertTrue(self.capsule.synthetic)
        self.assertTrue(self.capsule.category_neutral)
        self.assertFalse(self.capsule.production_eligible)
        self.assertFalse(self.capsule.certified)
        self.assertEqual(self.capsule.certification_state, "synthetic_not_certifiable")
        self.assertEqual(self.capsule.external_skills_required, 0)
        self.assertEqual(self.capsule.external_runtimes_required, 0)
        self.assertFalse(self.capsule.generated_product_implementation)

    def test_observations_cover_start_sections_and_commit(self) -> None:
        story = [item for item in self.observations.observations if item.story_id == "ST-11.01"]
        self.assertEqual(len(story), 17)
        self.assertEqual(story[0].event_name, "development_capsule_generation_started")
        self.assertEqual(story[-1].event_name, "development_capsule_generation_committed")
        for item in story:
            self.assertEqual(item.development_capsule_id, self.capsule.capsule_id)
            self.assertEqual(item.development_capsule_section_count, 15)
            self.assertEqual(item.development_capsule_obligation_count, 6)


if __name__ == "__main__":
    unittest.main()
