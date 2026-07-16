from __future__ import annotations

from datetime import timedelta
import unittest

from cmf_builder.adapters.file_target_profile_repository import FileTargetProfileRepository
from cmf_builder.adapters.in_memory_run_repository import DeterministicUuid7IdProvider, FixedClock
from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.application.authority import Action, Actor, ActorKind, AuthorityGrant, AuthorityService
from cmf_builder.application.run_commands import CreateCheckpointCommand, ResumeRunCommand, RunCommandService
from cmf_builder.domain.run import Run
from cmf_builder.domain.target_package_validation import TargetValidationInvalidatedError
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_07_04 import build_context, validation_command


class AtomicContentHarnessValidationReplayInvalidationTests(unittest.TestCase):
    def _complete(self, *, seed: str = "ST-07.04-replay"):
        service, _, atomicity, repository, observations, run_id, _, definition = build_context(seed=seed)
        receipt = service.validate(validation_command(run_id))
        return service, atomicity, repository, observations, run_id, receipt, service.get_active(run_id), definition

    def test_repeat_command_is_payload_safe_and_observable(self) -> None:
        service, _, repository, observations, run_id, receipt, report, _ = self._complete()
        before = repository.event_count(run_id)
        self.assertEqual(service.validate(validation_command(run_id)), receipt)
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(service.get_active(run_id), report)
        self.assertEqual(observations.observations[-1].event_name, "atomic_content_harness_validation_replayed")

    def test_run_replay_preserves_validation_identity_and_state_hash(self) -> None:
        _, _, repository, _, run_id, _, report, _ = self._complete()
        loaded = repository.load_run(run_id)
        replayed = Run.replay(repository.events(run_id))
        self.assertEqual(replayed, loaded)
        self.assertEqual(replayed.state_hash(), loaded.state_hash())
        self.assertEqual(replayed.atomic_content_harness_validation_ref, report.report_id)

    def test_checkpoint_resume_preserves_active_validation(self) -> None:
        service, _, repository, observations, run_id, _, report, _ = self._complete()
        authority = AuthorityService(
            actors=(Actor("architect-1", ActorKind.HUMAN),),
            grants=(AuthorityGrant(
                actor_id="architect-1",
                actions=frozenset(Action),
                resource_id="*",
                expires_at=NOW + timedelta(days=1),
            ),),
        )
        run_service = RunCommandService(
            repository=repository,
            profiles=FileTargetProfileRepository(ROOT),
            authority=authority,
            ids=DeterministicUuid7IdProvider(timestamp_ms=1_768_007_000_000, seed="ST-07.04-resume"),
            clock=FixedClock(NOW),
            observations=observations,
        )
        checkpoint = run_service.create_checkpoint(CreateCheckpointCommand(
            command_id="st-07-04-checkpoint",
            run_id=run_id,
            input_hash="synthetic-target-validation-input",
            policy_hash="builder-core-constitutional-precedence",
            actor_id="architect-1",
            expected_version=24,
            correlation_id="st-07-04-resume",
            causation_id=report.report_id,
        ))
        run_service.resume_run(ResumeRunCommand(
            command_id="st-07-04-resume",
            run_id=run_id,
            input_hash="synthetic-target-validation-input",
            policy_hash="builder-core-constitutional-precedence",
            actor_id="architect-1",
            expected_version=25,
            correlation_id="st-07-04-resume",
            causation_id=checkpoint.receipt_id,
        ))
        self.assertEqual(service.get_active(run_id), report)

    def test_upstream_reopen_invalidates_active_report_and_preserves_history(self) -> None:
        service, atomicity, repository, observations, run_id, _, report, _ = self._complete()
        result = atomicity.reopen(ReopenAtomicBoundaryCommand(
            command_id="reopen-after-target-validation",
            run_id=run_id,
            actor_id="architect-1",
            expected_version=24,
            correlation_id="reopen-target-validation-correlation",
            causation_id=report.report_id,
            reason="Authorized upstream correction invalidates target validation.",
        ))
        run = repository.load_run(run_id)
        self.assertEqual(run.atomic_content_harness_validation_invalidation_ref, result.invalidation_ref)
        self.assertTrue(repository.is_atomic_content_harness_validation_invalidated(report.report_id))
        invalidation = repository.get_atomic_content_harness_validation_invalidation(result.invalidation_ref)
        self.assertIsNotNone(invalidation)
        self.assertEqual(service.get_historical(report.report_id).canonical_bytes(), report.canonical_bytes())
        with self.assertRaises(TargetValidationInvalidatedError):
            service.get_active(run_id)
        self.assertIn("atomic_content_harness_validation_invalidated", {item.event_name for item in observations.observations})


if __name__ == "__main__":
    unittest.main()
