from __future__ import annotations

from pathlib import Path
import unittest

from cmf_builder.adapters.file_target_profile_repository import (
    FileTargetProfileRepository,
)
from cmf_builder.domain.run import LifecycleState

from tests.stories.st_01_01_synthetic_proof import (
    CATEGORY_ID,
    EMPTY_REGISTRY_SHA256,
    PROFILE_FIXTURE_SHA256,
    PROFILE_ID,
    ROOT,
    TARGET_ID,
    build_service,
    create_command,
)


class SyntheticProofAcceptanceTests(unittest.TestCase):
    def test_ac_sp_02_and_03_admit_pinned_category_neutral_profile(self) -> None:
        service, repository, observations, _, profiles = build_service()

        receipt = service.create_run(create_command())
        run = repository.load_run(receipt.run_id)
        proof = run.target_profile.supplemental_proof

        self.assertIsNotNone(proof)
        assert proof is not None
        self.assertEqual(run.target_profile.target_id, TARGET_ID)
        self.assertEqual(run.target_profile.category_id, CATEGORY_ID)
        self.assertEqual(run.target_profile.profile_id, PROFILE_ID)
        self.assertEqual(run.target_profile.version, "1.0.0")
        self.assertEqual(run.target_profile.compatibility_state, "builder_core_validation_only")
        self.assertFalse(run.target_profile.production_certified)
        self.assertEqual(proof.profile_source_hash, PROFILE_FIXTURE_SHA256)
        self.assertEqual(proof.skill_registry_hash, EMPTY_REGISTRY_SHA256)
        self.assertTrue(proof.synthetic)
        self.assertTrue(proof.repository_owned)
        self.assertTrue(proof.non_production)
        self.assertTrue(proof.non_certified)
        self.assertTrue(proof.builder_core_validation_only)
        self.assertEqual(proof.category_binding_mode, "none")
        self.assertFalse(proof.canonical_category_registry_membership)
        self.assertFalse(proof.external_skills_required)
        self.assertFalse(proof.dynamic_skill_discovery_allowed)
        self.assertEqual(proof.declared_skill_ids, ())
        self.assertEqual(
            run.required_work,
            (
                "lock_governed_synthetic_task_definition",
                "validate_declared_atomic_boundary",
                "compile_canonical_harness_ir",
                "compile_atomic_harness_definition",
                "validate_atomic_harness_definition",
                "compile_development_capsule",
            ),
        )
        self.assertEqual(run.lifecycle_state, LifecycleState.CREATED)
        self.assertEqual(run.stream_version, 2)
        self.assertEqual(len(receipt.event_ids), 2)
        self.assertEqual(observations.observations[-1].outcome, "PASS")
        self.assertEqual(profiles.load_authorized_profile(), run.target_profile)

    def test_ac_sp_02_profile_metadata_survives_event_replay(self) -> None:
        service, repository, _, _, _ = build_service()
        created = service.create_run(create_command())

        replayed = repository.load_run(created.run_id)
        first_event = repository.events(created.run_id)[0]

        self.assertEqual(
            replayed.target_profile.profile_hash,
            repository.events(created.run_id)[1].value("profile_hash"),
        )
        self.assertEqual(first_event.value("proof_kind"), "synthetic_builder_core_proof")
        self.assertEqual(first_event.value("profile_source_hash"), PROFILE_FIXTURE_SHA256)
        self.assertEqual(first_event.value("skill_registry_hash"), EMPTY_REGISTRY_SHA256)
        self.assertTrue(first_event.value("synthetic"))
        self.assertFalse(first_event.value("canonical_category_registry_membership"))

    def test_ac_sp_01_preserves_exact_format02_profile_behavior(self) -> None:
        profile = FileTargetProfileRepository(Path(ROOT)).load_authorized_profile()

        self.assertEqual(
            profile.profile_hash,
            "sha256:3ad28b4f622e975ff7943f89a533544469b3e81f7348fa67fa368e833e9fbfed",
        )
        self.assertEqual(profile.category_id, "2d_character_animation")
        self.assertEqual(profile.profile_id, "format02_minimal_coach_theatre")
        self.assertEqual(profile.compatibility_state, "contract_compatible")
        self.assertFalse(profile.production_certified)
        self.assertIsNone(profile.supplemental_proof)
        self.assertEqual(
            profile.required_work,
            ("configure_evidence_workspace", "lock_target_specific_evidence"),
        )

    def test_ac_sp_10_stops_before_any_later_story_output(self) -> None:
        service, repository, _, _, _ = build_service()
        created = service.create_run(create_command())

        event_types = tuple(event.event_type for event in repository.events(created.run_id))
        self.assertEqual(event_types, ("RunCreated", "TargetProfileSelected"))
        self.assertNotIn("AtomicHarnessDefinition", repr(repository.events(created.run_id)))
        self.assertNotIn("DevelopmentCapsuleGenerated", repr(repository.events(created.run_id)))
        self.assertNotIn("TaskExecuted", repr(repository.events(created.run_id)))


if __name__ == "__main__":
    unittest.main()
