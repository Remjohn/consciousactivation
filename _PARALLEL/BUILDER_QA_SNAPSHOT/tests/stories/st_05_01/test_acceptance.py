from __future__ import annotations

import unittest

from cmf_builder.domain.skill_registry import (
    AUTHORITY_LANES,
    CAPABILITY_IDS,
    MATURITY_STATES,
    PLASTICITY_STATES,
    CapabilityClassification,
)
from tests.stories.st_05_01 import build_context, compile_command


class SyntheticEmptySkillRegistryAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        (
            self.service,
            _,
            self.repository,
            self.observations,
            self.run_id,
            _,
            _,
        ) = build_context()
        self.receipt = self.service.compile(compile_command(self.run_id))
        self.snapshot = self.service.get_active(self.run_id)

    def test_ac_01_compiles_one_snapshot_and_receipt_against_active_context(self) -> None:
        self.assertEqual(self.repository.skill_registry_snapshot_count, 1)
        self.assertEqual(self.repository.skill_registry_consumption_receipt_count, 1)
        self.assertEqual(self.receipt.stream_version, 21)
        self.assertEqual(self.snapshot.run_id, self.run_id)
        self.receipt.validate(self.snapshot)

    def test_ac_02_classifies_exactly_five_capabilities_without_skills(self) -> None:
        self.assertEqual(self.snapshot.capability_ids, CAPABILITY_IDS)
        self.assertEqual(len(self.snapshot.capability_classifications), 5)
        for declaration in self.snapshot.capability_classifications:
            self.assertIs(
                declaration.classification,
                CapabilityClassification.BUILDER_OWNED_CODE,
            )
            self.assertEqual(declaration.owner_kind, "builder_code")
            self.assertEqual(declaration.determinism, "deterministic")
            self.assertFalse(declaration.skill_required)
            self.assertFalse(declaration.external_skill_required)

    def test_ac_03_preserves_distinct_authority_maturity_and_plasticity_taxonomies(self) -> None:
        taxonomy = self.snapshot.taxonomy
        self.assertEqual(taxonomy.authority_lanes, AUTHORITY_LANES)
        self.assertEqual(taxonomy.maturity_states, MATURITY_STATES)
        self.assertEqual(taxonomy.plasticity_states, PLASTICITY_STATES)
        self.assertEqual(taxonomy.canonical_skills, ())
        self.assertEqual(taxonomy.harness_local_adaptations, ())
        self.assertEqual(taxonomy.experimental_capabilities, ())
        self.assertEqual(taxonomy.recipes, ())
        self.assertEqual(taxonomy.jit_capsules, ())

    def test_ac_11_production_and_external_boundaries_remain_closed(self) -> None:
        self.assertFalse(self.snapshot.production_eligible)
        self.assertFalse(self.snapshot.certified)
        self.assertFalse(self.snapshot.external_skills_required)
        self.assertFalse(self.snapshot.dynamic_skill_discovery_allowed)
        self.assertEqual(self.snapshot.undeclared_skill_use, "FAIL_CLOSED")
        self.assertEqual(
            self.snapshot.real_profile_registry_subscope,
            "DEFERRED_BLOCKED_BY_EXISTING_GATES",
        )

    def test_ac_12_success_observations_are_complete_and_zero_skill(self) -> None:
        story = [item for item in self.observations.observations if item.story_id == "ST-05.01"]
        self.assertEqual(
            {item.event_name for item in story},
            {
                "synthetic_skill_registry_compilation_started",
                "synthetic_skill_registry_validated",
                "synthetic_skill_registry_snapshot_committed",
            },
        )
        for item in story:
            self.assertEqual(item.skill_snapshot_id, self.snapshot.snapshot_id)
            self.assertEqual(item.skill_capability_count, 5)
            self.assertEqual(item.registered_skill_count, 0)
            self.assertEqual(item.required_external_skill_count, 0)


if __name__ == "__main__":
    unittest.main()
