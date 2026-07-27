from __future__ import annotations

from dataclasses import replace
from datetime import timedelta
import unittest

from cmf_builder.application.run_commands import (
    CreateCheckpointCommand,
    GrantWaiverCommand,
    ResumeRunCommand,
    TransitionRunCommand,
)
from cmf_builder.domain.run import EventStreamInvalid, LifecycleState, Run

from tests.stories.st_01_01 import NOW, build_service, create_command


class ReplayAndReceiptTests(unittest.TestCase):
    def test_st_01_01_receipt_resume_preserves_identity_and_human_decision(self) -> None:
        service, repository, observations, _, _ = build_service()
        created = service.create_run(create_command())
        transitioned = service.transition_run(
            TransitionRunCommand(
                command_id="transition-1",
                run_id=created.run_id,
                to_state=LifecycleState.SOURCE_DIAGNOSTIC,
                prerequisites=frozenset({"target_profile_selected"}),
                actor_id="architect-1",
                expected_version=2,
                correlation_id="correlation-1",
                causation_id=created.receipt_id,
            )
        )
        waiver = service.grant_waiver(
            GrantWaiverCommand(
                command_id="waiver-1",
                run_id=created.run_id,
                skipped_obligation="optional_format02_review",
                rationale="Covered by deterministic test evidence.",
                risk="low",
                affected_gates=("HG-004",),
                scope="ST-01.01",
                expires_at=NOW + timedelta(hours=1),
                actor_id="architect-1",
                expected_version=3,
                correlation_id="correlation-1",
                causation_id=transitioned.receipt_id,
            )
        )
        checkpoint = service.create_checkpoint(
            CreateCheckpointCommand(
                command_id="checkpoint-1",
                run_id=created.run_id,
                input_hash="no-evidence:ST-01.01",
                policy_hash="policy:v1",
                actor_id="architect-1",
                expected_version=4,
                correlation_id="correlation-1",
                causation_id=waiver.receipt_id,
            )
        )
        resume = service.resume_run(
            ResumeRunCommand(
                command_id="resume-1",
                run_id=created.run_id,
                input_hash="no-evidence:ST-01.01",
                policy_hash="policy:v1",
                actor_id="architect-1",
                expected_version=5,
                correlation_id="correlation-1",
                causation_id=checkpoint.receipt_id,
            )
        )

        run = repository.load_run(created.run_id)
        replayed = Run.replay(repository.events(created.run_id))
        self.assertEqual(run, replayed)
        self.assertEqual(run.run_id, created.run_id)
        self.assertIn(waiver.detail("human_receipt_id"), run.human_decision_receipt_ids)
        self.assertEqual(resume.detail("replayed_human_decision_count"), "0")
        self.assertEqual(resume.detail("checkpoint_id"), checkpoint.detail("checkpoint_id"))
        self.assertTrue(any(o.event_name == "RunResumed" for o in observations.observations))

    def test_st_01_01_receipt_uses_older_valid_checkpoint_when_newer_is_corrupt(self) -> None:
        service, repository, observations, _, _ = build_service()
        created = service.create_run(create_command())
        older = service.create_checkpoint(
            CreateCheckpointCommand(
                command_id="checkpoint-old",
                run_id=created.run_id,
                input_hash="no-evidence:ST-01.01",
                policy_hash="policy:v1",
                actor_id="architect-1",
                expected_version=2,
                correlation_id="correlation-1",
                causation_id=created.receipt_id,
            )
        )
        service.transition_run(
            TransitionRunCommand(
                command_id="transition-after-checkpoint",
                run_id=created.run_id,
                to_state=LifecycleState.SOURCE_DIAGNOSTIC,
                prerequisites=frozenset({"target_profile_selected"}),
                actor_id="architect-1",
                expected_version=3,
                correlation_id="correlation-1",
                causation_id=older.receipt_id,
            )
        )
        newer = service.create_checkpoint(
            CreateCheckpointCommand(
                command_id="checkpoint-new",
                run_id=created.run_id,
                input_hash="no-evidence:ST-01.01",
                policy_hash="policy:v1",
                actor_id="architect-1",
                expected_version=4,
                correlation_id="correlation-1",
                causation_id=older.receipt_id,
            )
        )
        checkpoints = repository.list_checkpoints(created.run_id)
        newest = next(c for c in checkpoints if c.checkpoint_id == newer.detail("checkpoint_id"))
        repository.add_checkpoint(replace(newest, state_hash="corrupt"))

        resume = service.resume_run(
            ResumeRunCommand(
                command_id="resume-fallback",
                run_id=created.run_id,
                input_hash="no-evidence:ST-01.01",
                policy_hash="policy:v1",
                actor_id="architect-1",
                expected_version=5,
                correlation_id="correlation-1",
                causation_id=newer.receipt_id,
            )
        )

        self.assertEqual(resume.detail("checkpoint_id"), older.detail("checkpoint_id"))
        self.assertTrue(
            any(
                o.event_name == "CheckpointInvalid"
                and o.failure_context["checkpoint_id"] == newer.detail("checkpoint_id")
                for o in observations.observations
            )
        )

    def test_st_01_01_receipt_rejects_discontinuous_event_stream(self) -> None:
        service, repository, _, _, _ = build_service()
        created = service.create_run(create_command())
        events = list(repository.events(created.run_id))
        events[1] = replace(events[1], stream_version=3)
        with self.assertRaises(EventStreamInvalid):
            Run.replay(tuple(events))

    def test_st_01_01_receipt_is_deterministic_in_fresh_contexts(self) -> None:
        first_service, first_repository, _, _, _ = build_service()
        second_service, second_repository, _, _, _ = build_service()
        first = first_service.create_run(create_command())
        second = second_service.create_run(create_command())

        first_events = tuple(e.canonical_dict() for e in first_repository.events(first.run_id))
        second_events = tuple(e.canonical_dict() for e in second_repository.events(second.run_id))
        self.assertEqual(first, second)
        self.assertEqual(first_events, second_events)


if __name__ == "__main__":
    unittest.main()
