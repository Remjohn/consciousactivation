from __future__ import annotations

import unittest

from cmf_builder.application.run_commands import TransitionRunCommand
from cmf_builder.domain.run import LifecycleState
from cmf_builder.domain.target_profile import (
    TargetSelectionRejected,
    UnsupportedTargetForAuthorizedSlice,
)

from tests.stories.st_01_01 import (
    CATEGORY_ID,
    PROFILE_ID,
    TARGET_ID,
    build_service,
    create_command,
)


class StartAndResumeAcceptanceTests(unittest.TestCase):
    def test_st_01_01_acceptance_creates_one_format02_run(self) -> None:
        service, repository, observations, _, profiles = build_service()

        receipt = service.create_run(create_command())
        run = repository.load_run(receipt.run_id)

        self.assertEqual(run.run_id, receipt.run_id)
        self.assertEqual(run.target_profile.target_id, TARGET_ID)
        self.assertEqual(run.target_profile.category_id, CATEGORY_ID)
        self.assertEqual(run.target_profile.profile_id, PROFILE_ID)
        self.assertEqual(run.target_profile.compatibility_state, "contract_compatible")
        self.assertFalse(run.target_profile.production_certified)
        self.assertEqual(run.compiler_version, "builder-v1.2")
        self.assertEqual(run.created_by, "architect-1")
        self.assertEqual(run.lifecycle_state, LifecycleState.CREATED)
        self.assertIn("configure_evidence_workspace", run.required_work)
        self.assertEqual(run.stream_version, 2)
        self.assertEqual(len(receipt.event_ids), 2)
        self.assertEqual(
            profiles.recognized_target_ids(),
            frozenset(
                {
                    "atomic_content_harness",
                    "visual_asset_editor",
                    "content_asset_delegation_contract",
                }
            ),
        )
        self.assertEqual(observations.observations[-1].event_name, "ST-01.01:OutcomeVerified")

    def test_st_01_01_acceptance_legal_transition_emits_one_event(self) -> None:
        service, repository, _, _, _ = build_service()
        created = service.create_run(create_command())
        before = repository.event_count(created.run_id)

        receipt = service.transition_run(
            TransitionRunCommand(
                command_id="command-transition-1",
                run_id=created.run_id,
                to_state=LifecycleState.SOURCE_DIAGNOSTIC,
                prerequisites=frozenset({"target_profile_selected"}),
                actor_id="architect-1",
                expected_version=2,
                correlation_id="correlation-1",
                causation_id=created.receipt_id,
            )
        )

        self.assertEqual(repository.event_count(created.run_id), before + 1)
        self.assertEqual(len(receipt.event_ids), 1)
        self.assertEqual(
            repository.load_run(created.run_id).lifecycle_state,
            LifecycleState.SOURCE_DIAGNOSTIC,
        )

    def test_st_01_01_acceptance_identical_command_is_idempotent(self) -> None:
        service, repository, observations, _, _ = build_service()
        command = create_command()

        first = service.create_run(command)
        before = repository.event_count(first.run_id)
        second = service.create_run(command)

        self.assertEqual(first, second)
        self.assertEqual(repository.event_count(first.run_id), before)
        self.assertTrue(any(o.event_name == "DuplicateCommandObserved" for o in observations.observations))

    def test_st_01_01_acceptance_rejects_zero_multiple_and_unknown_targets(self) -> None:
        cases = (
            create_command(command_id="zero", target_ids=()),
            create_command(
                command_id="multiple",
                target_ids=("atomic_content_harness", "visual_asset_editor"),
            ),
            create_command(command_id="unknown", target_ids=("universal_agent_factory",)),
        )
        for command in cases:
            with self.subTest(command=command.command_id):
                service, repository, _, _, _ = build_service()
                with self.assertRaises(TargetSelectionRejected):
                    service.create_run(command)
                self.assertEqual(repository.stream_count, 0)

    def test_st_01_01_acceptance_rejects_external_and_conversational_execution(self) -> None:
        external = create_command(
            command_id="external",
            target_ids=("visual_asset_editor",),
        )
        conversational = create_command(
            command_id="conversational",
            category_id="conversational_activation_expression",
            profile_id="public_comment",
        )
        for command in (external, conversational):
            with self.subTest(command=command.command_id):
                service, repository, _, _, _ = build_service()
                with self.assertRaises(UnsupportedTargetForAuthorizedSlice):
                    service.create_run(command)
                self.assertEqual(repository.stream_count, 0)


if __name__ == "__main__":
    unittest.main()
