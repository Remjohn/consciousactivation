from __future__ import annotations

from datetime import timedelta
import unittest

from cmf_builder.adapters.file_target_profile_repository import FileTargetProfileRepository
from cmf_builder.adapters.in_memory_run_repository import DeterministicUuid7IdProvider, FixedClock
from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.application.authority import Action, Actor, ActorKind, AuthorityGrant, AuthorityService
from cmf_builder.application.run_commands import CreateCheckpointCommand, ResumeRunCommand, RunCommandService
from cmf_builder.domain.development_capsule import DevelopmentCapsuleInvalidatedError
from cmf_builder.domain.run import Run
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_11_01 import build_context, capsule_command


class DevelopmentCapsuleReplayInvalidationTests(unittest.TestCase):
    def _complete(self, seed: str = "ST-11.01-replay"):
        service, _, atomicity, repository, observations, run_id, _, _, _ = build_context(seed=seed)
        receipt = service.generate(capsule_command(run_id))
        return service, atomicity, repository, observations, run_id, receipt, service.get_active(run_id)

    def test_repeat_command_is_payload_safe_and_observable(self) -> None:
        service, _, repository, observations, run_id, receipt, capsule = self._complete()
        before = repository.event_count(run_id)
        self.assertEqual(service.generate(capsule_command(run_id)), receipt)
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(service.get_active(run_id), capsule)
        self.assertEqual(observations.observations[-1].event_name, "development_capsule_generation_replayed")

    def test_run_replay_preserves_capsule_identity_and_state_hash(self) -> None:
        _, _, repository, _, run_id, _, capsule = self._complete()
        loaded = repository.load_run(run_id)
        replayed = Run.replay(repository.events(run_id))
        self.assertEqual(replayed, loaded)
        self.assertEqual(replayed.state_hash(), loaded.state_hash())
        self.assertEqual(replayed.development_capsule_ref, capsule.capsule_id)

    def test_checkpoint_resume_preserves_active_capsule(self) -> None:
        service, _, repository, observations, run_id, _, capsule = self._complete()
        authority = AuthorityService(
            actors=(Actor("architect-1", ActorKind.HUMAN),),
            grants=(AuthorityGrant(actor_id="architect-1", actions=frozenset(Action), resource_id="*", expires_at=NOW + timedelta(days=1)),),
        )
        run_service = RunCommandService(
            repository=repository,
            profiles=FileTargetProfileRepository(ROOT),
            authority=authority,
            ids=DeterministicUuid7IdProvider(timestamp_ms=1_768_009_000_000, seed="ST-11.01-resume"),
            clock=FixedClock(NOW),
            observations=observations,
        )
        checkpoint = run_service.create_checkpoint(CreateCheckpointCommand(
            command_id="st-11-01-checkpoint", run_id=run_id,
            input_hash="synthetic-capsule-input", policy_hash="builder-core-constitutional-precedence",
            actor_id="architect-1", expected_version=25,
            correlation_id="st-11-01-resume", causation_id=capsule.capsule_id,
        ))
        run_service.resume_run(ResumeRunCommand(
            command_id="st-11-01-resume", run_id=run_id,
            input_hash="synthetic-capsule-input", policy_hash="builder-core-constitutional-precedence",
            actor_id="architect-1", expected_version=26,
            correlation_id="st-11-01-resume", causation_id=checkpoint.receipt_id,
        ))
        self.assertEqual(service.get_active(run_id), capsule)

    def test_upstream_reopen_invalidates_active_capsule_and_preserves_history(self) -> None:
        service, atomicity, repository, observations, run_id, _, capsule = self._complete()
        result = atomicity.reopen(ReopenAtomicBoundaryCommand(
            command_id="reopen-after-development-capsule", run_id=run_id,
            actor_id="architect-1", expected_version=25,
            correlation_id="reopen-development-capsule", causation_id=capsule.capsule_id,
            reason="Authorized upstream correction invalidates the generated capsule.",
        ))
        run = repository.load_run(run_id)
        self.assertEqual(run.development_capsule_invalidation_ref, result.invalidation_ref)
        self.assertTrue(repository.is_development_capsule_invalidated(capsule.capsule_id))
        self.assertIsNotNone(repository.get_development_capsule_invalidation(result.invalidation_ref))
        self.assertEqual(service.get_historical(capsule.capsule_id).canonical_bytes(), capsule.canonical_bytes())
        with self.assertRaises(DevelopmentCapsuleInvalidatedError):
            service.get_active(run_id)
        self.assertIn("development_capsule_invalidated", {item.event_name for item in observations.observations})


if __name__ == "__main__":
    unittest.main()
