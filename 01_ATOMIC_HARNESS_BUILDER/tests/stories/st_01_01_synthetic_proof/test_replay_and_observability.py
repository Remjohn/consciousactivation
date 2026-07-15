from __future__ import annotations

from hashlib import sha256
import json
import unittest

from cmf_builder.application.run_commands import (
    CreateCheckpointCommand,
    ResumeRunCommand,
    TransitionRunCommand,
)
from cmf_builder.domain.run import LifecycleState, Run

from tests.stories.st_01_01_synthetic_proof import (
    EMPTY_REGISTRY_SHA256,
    PROFILE_FIXTURE_SHA256,
    build_service,
    create_command,
)


class SyntheticProofReplayAndObservabilityTests(unittest.TestCase):
    def test_ac_sp_04_checkpoint_resume_and_replay_preserve_decisions(self) -> None:
        service, repository, observations, _, _ = build_service()
        created = service.create_run(create_command())
        transitioned = service.transition_run(
            TransitionRunCommand(
                command_id="synthetic-transition-1",
                run_id=created.run_id,
                to_state=LifecycleState.SOURCE_DIAGNOSTIC,
                prerequisites=frozenset({"target_profile_selected"}),
                actor_id="architect-1",
                expected_version=2,
                correlation_id="synthetic-proof-correlation-1",
                causation_id=created.receipt_id,
            )
        )
        checkpoint = service.create_checkpoint(
            CreateCheckpointCommand(
                command_id="synthetic-checkpoint-1",
                run_id=created.run_id,
                input_hash=f"sha256:{PROFILE_FIXTURE_SHA256}",
                policy_hash=f"sha256:{EMPTY_REGISTRY_SHA256}",
                actor_id="architect-1",
                expected_version=3,
                correlation_id="synthetic-proof-correlation-1",
                causation_id=transitioned.receipt_id,
            )
        )
        resumed = service.resume_run(
            ResumeRunCommand(
                command_id="synthetic-resume-1",
                run_id=created.run_id,
                input_hash=f"sha256:{PROFILE_FIXTURE_SHA256}",
                policy_hash=f"sha256:{EMPTY_REGISTRY_SHA256}",
                actor_id="architect-1",
                expected_version=4,
                correlation_id="synthetic-proof-correlation-1",
                causation_id=checkpoint.receipt_id,
            )
        )

        current = repository.load_run(created.run_id)
        replayed = Run.replay(repository.events(created.run_id))
        self.assertEqual(current, replayed)
        self.assertEqual(current.run_id, created.run_id)
        self.assertEqual(resumed.detail("replayed_human_decision_count"), "0")
        self.assertEqual(resumed.detail("checkpoint_id"), checkpoint.detail("checkpoint_id"))
        self.assertEqual(current.lifecycle_state, LifecycleState.SOURCE_DIAGNOSTIC)
        self.assertTrue(any(o.event_name == "RunResumed" for o in observations.observations))

    def test_ac_sp_04_identical_command_is_idempotent(self) -> None:
        service, repository, observations, _, _ = build_service()
        command = create_command()

        first = service.create_run(command)
        before = repository.event_count(first.run_id)
        second = service.create_run(command)

        self.assertEqual(first, second)
        self.assertEqual(repository.event_count(first.run_id), before)
        self.assertTrue(
            any(o.event_name == "DuplicateCommandObserved" for o in observations.observations)
        )

    def test_ac_sp_09_correlates_audit_and_run_evidence_deterministically(self) -> None:
        first_service, first_repository, first_observations, _, _ = build_service()
        second_service, second_repository, second_observations, _, _ = build_service()
        first = first_service.create_run(create_command())
        second = second_service.create_run(create_command())

        first_events = [event.canonical_dict() for event in first_repository.events(first.run_id)]
        second_events = [event.canonical_dict() for event in second_repository.events(second.run_id)]
        encoded = json.dumps(
            first_events, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        evidence_hash = sha256(encoded).hexdigest()

        self.assertEqual(first, second)
        self.assertEqual(first_events, second_events)
        self.assertEqual(len(evidence_hash), 64)
        observation = first_observations.observations[-1]
        self.assertEqual(observation.run_id, first.run_id)
        self.assertEqual(observation.command_id, "synthetic-create-1")
        self.assertEqual(observation.target_id, "atomic_content_harness")
        self.assertEqual(observation.category_id, "none_test_only")
        self.assertEqual(observation.profile_id, "synthetic_text_normalization_v1")
        self.assertEqual(observation.authority_identity, "architect-1")
        self.assertEqual(observation.outcome, "PASS")
        self.assertEqual(
            first_repository.events(first.run_id)[0].value("skill_registry_hash"),
            EMPTY_REGISTRY_SHA256,
        )
        self.assertEqual(
            first_repository.events(first.run_id)[0].value("profile_source_hash"),
            PROFILE_FIXTURE_SHA256,
        )
        self.assertEqual(
            first_observations.observations[-1], second_observations.observations[-1]
        )


if __name__ == "__main__":
    unittest.main()
