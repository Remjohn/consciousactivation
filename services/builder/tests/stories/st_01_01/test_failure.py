from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.adapters.in_memory_run_repository import (
    ConcurrencyConflict,
    IdempotencyPayloadMismatch,
)
from cmf_builder.application.checkpoints import CheckpointInvalid
from cmf_builder.application.run_commands import (
    CreateCheckpointCommand,
    ResumeRunCommand,
    TransitionRunCommand,
)
from cmf_builder.domain.run import LifecycleState, TransitionRejected

from tests.stories.st_01_01 import build_service, create_command


class FailClosedContractTests(unittest.TestCase):
    def test_st_01_01_failure_invalid_transition_does_not_mutate(self) -> None:
        service, repository, observations, _, _ = build_service()
        created = service.create_run(create_command())
        before = repository.event_count(created.run_id)

        with self.assertRaises(TransitionRejected):
            service.transition_run(
                TransitionRunCommand(
                    command_id="invalid-transition",
                    run_id=created.run_id,
                    to_state=LifecycleState.GENESIS,
                    prerequisites=frozenset(),
                    actor_id="architect-1",
                    expected_version=2,
                    correlation_id="correlation-1",
                    causation_id=created.receipt_id,
                )
            )

        self.assertEqual(repository.event_count(created.run_id), before)
        self.assertEqual(repository.load_run(created.run_id).lifecycle_state, LifecycleState.CREATED)
        self.assertEqual(observations.observations[-1].failure_context["code"], "TransitionRejected")

    def test_st_01_01_failure_stale_version_does_not_mutate(self) -> None:
        service, repository, _, _, _ = build_service()
        created = service.create_run(create_command())

        with self.assertRaises(ConcurrencyConflict):
            service.transition_run(
                TransitionRunCommand(
                    command_id="stale-transition",
                    run_id=created.run_id,
                    to_state=LifecycleState.SOURCE_DIAGNOSTIC,
                    prerequisites=frozenset({"target_profile_selected"}),
                    actor_id="architect-1",
                    expected_version=1,
                    correlation_id="correlation-1",
                    causation_id=created.receipt_id,
                )
            )
        self.assertEqual(repository.event_count(created.run_id), 2)

    def test_st_01_01_failure_reused_command_with_new_payload_rejects(self) -> None:
        service, repository, _, _, _ = build_service()
        created = service.create_run(create_command())
        command = TransitionRunCommand(
            command_id="same-command",
            run_id=created.run_id,
            to_state=LifecycleState.SOURCE_DIAGNOSTIC,
            prerequisites=frozenset({"target_profile_selected"}),
            actor_id="architect-1",
            expected_version=2,
            correlation_id="correlation-1",
            causation_id=created.receipt_id,
        )
        service.transition_run(command)
        before = repository.event_count(created.run_id)

        with self.assertRaises(IdempotencyPayloadMismatch):
            service.transition_run(replace(command, to_state=LifecycleState.SOURCE_LOCKED))
        self.assertEqual(repository.event_count(created.run_id), before)

    def test_st_01_01_failure_corrupt_only_checkpoint_blocks_resume(self) -> None:
        service, repository, _, _, _ = build_service()
        created = service.create_run(create_command())
        checkpoint_receipt = service.create_checkpoint(
            CreateCheckpointCommand(
                command_id="checkpoint-1",
                run_id=created.run_id,
                input_hash="no-evidence:ST-01.01",
                policy_hash="policy:v1",
                actor_id="architect-1",
                expected_version=2,
                correlation_id="correlation-1",
                causation_id=created.receipt_id,
            )
        )
        checkpoint_id = checkpoint_receipt.detail("checkpoint_id")
        checkpoint = repository.list_checkpoints(created.run_id)[0]
        repository.add_checkpoint(replace(checkpoint, state_hash="corrupt"))
        before = repository.event_count(created.run_id)

        with self.assertRaises(CheckpointInvalid) as caught:
            service.resume_run(
                ResumeRunCommand(
                    command_id="resume-corrupt",
                    run_id=created.run_id,
                    input_hash="no-evidence:ST-01.01",
                    policy_hash="policy:v1",
                    actor_id="architect-1",
                    expected_version=3,
                    correlation_id="correlation-1",
                    causation_id=checkpoint_receipt.receipt_id,
                )
            )
        self.assertIn(checkpoint_id, caught.exception.context["invalid_checkpoint_ids"])
        self.assertEqual(repository.event_count(created.run_id), before)


if __name__ == "__main__":
    unittest.main()
