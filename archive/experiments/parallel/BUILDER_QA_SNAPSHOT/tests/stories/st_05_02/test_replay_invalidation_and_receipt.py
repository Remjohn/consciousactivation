from __future__ import annotations

from datetime import timedelta
import unittest

from cmf_builder.adapters.file_target_profile_repository import FileTargetProfileRepository
from cmf_builder.adapters.in_memory_run_repository import (
    DeterministicUuid7IdProvider,
    FixedClock,
)
from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.application.run_commands import (
    CreateCheckpointCommand,
    ResumeRunCommand,
    RunCommandService,
)
from cmf_builder.domain.run import Run
from cmf_builder.domain.skill_registry import SkillNecessityInvalidatedError
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_05_02 import build_context, evaluate_command


class SkillNecessityReplayInvalidationTests(unittest.TestCase):
    def _complete(self, *, seed: str = "ST-05.02"):
        service, atomicity, repository, observations, run_id, _, _, snapshot = (
            build_context(seed=seed)
        )
        receipt = service.evaluate(evaluate_command(
            run_id, snapshot.snapshot_id, snapshot.snapshot_hash
        ))
        decision = service.get_active(run_id)
        return service, atomicity, repository, observations, run_id, receipt, decision, snapshot

    def test_repeat_command_is_payload_safe_and_observable(self) -> None:
        service, _, repository, observations, run_id, receipt, decision, snapshot = self._complete()
        before = repository.event_count(run_id)
        self.assertEqual(
            service.evaluate(evaluate_command(run_id, snapshot.snapshot_id, snapshot.snapshot_hash)),
            receipt,
        )
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.skill_necessity_decision_count, 1)
        self.assertEqual(service.get_active(run_id), decision)
        self.assertEqual(observations.observations[-1].event_name, "synthetic_skill_necessity_replayed")

    def test_fresh_context_decision_and_receipt_bytes_are_identical(self) -> None:
        first = self._complete(seed="identical-skill-necessity")
        second = self._complete(seed="identical-skill-necessity")
        self.assertEqual(first[6].canonical_bytes(), second[6].canonical_bytes())
        self.assertEqual(first[5].canonical_bytes(), second[5].canonical_bytes())
        self.assertEqual(first[6].decision_hash, second[6].decision_hash)
        self.assertEqual(first[5].receipt_hash, second[5].receipt_hash)

    def test_run_replay_preserves_decision_identity_and_state_hash(self) -> None:
        _, _, repository, _, run_id, _, decision, _ = self._complete()
        loaded = repository.load_run(run_id)
        replayed = Run.replay(repository.events(run_id))
        self.assertEqual(replayed, loaded)
        self.assertEqual(replayed.state_hash(), loaded.state_hash())
        self.assertEqual(replayed.skill_necessity_ref, decision.decision_id)
        self.assertEqual(replayed.skill_necessity_hash, decision.decision_hash)

    def test_checkpoint_resume_preserves_active_necessity_decision(self) -> None:
        service, _, repository, observations, run_id, _, decision, _ = self._complete()
        actors = (Actor("architect-1", ActorKind.HUMAN),)
        authority = AuthorityService(
            actors=actors,
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
            ids=DeterministicUuid7IdProvider(
                timestamp_ms=1_768_003_000_000,
                seed="ST-05.02-resume",
            ),
            clock=FixedClock(NOW),
            observations=observations,
        )
        checkpoint = run_service.create_checkpoint(CreateCheckpointCommand(
            command_id="st-05-02-checkpoint",
            run_id=run_id,
            input_hash="synthetic-skill-necessity-input",
            policy_hash="empty-skill-registry-policy",
            actor_id="architect-1",
            expected_version=22,
            correlation_id="st-05-02-resume",
            causation_id=decision.decision_id,
        ))
        run_service.resume_run(ResumeRunCommand(
            command_id="st-05-02-resume",
            run_id=run_id,
            input_hash="synthetic-skill-necessity-input",
            policy_hash="empty-skill-registry-policy",
            actor_id="architect-1",
            expected_version=23,
            correlation_id="st-05-02-resume",
            causation_id=checkpoint.receipt_id,
        ))
        resumed = repository.load_run(run_id)
        self.assertEqual(resumed.skill_necessity_ref, decision.decision_id)
        self.assertEqual(resumed.skill_necessity_hash, decision.decision_hash)
        self.assertEqual(service.get_active(run_id), decision)

    def test_upstream_reopen_invalidates_active_decision_and_preserves_history(self) -> None:
        service, atomicity, repository, observations, run_id, _, decision, snapshot = self._complete()
        before = repository.event_count(run_id)
        result = atomicity.reopen(ReopenAtomicBoundaryCommand(
            command_id="reopen-after-skill-necessity",
            run_id=run_id,
            actor_id="architect-1",
            expected_version=22,
            correlation_id="reopen-skill-necessity-correlation",
            causation_id=decision.decision_id,
            reason="Authorized upstream correction invalidates the necessity decision.",
        ))
        run = repository.load_run(run_id)
        self.assertEqual(run.stream_version, 34)
        self.assertEqual(run.skill_necessity_invalidation_ref, result.invalidation_ref)
        self.assertTrue(repository.is_skill_necessity_invalidated(decision.decision_id))
        invalidation = repository.get_skill_necessity_invalidation(result.invalidation_ref)
        assert invalidation is not None
        self.assertEqual(invalidation.snapshot_ref, snapshot.snapshot_id)
        self.assertEqual(service.get_historical(decision.decision_id).canonical_bytes(), decision.canonical_bytes())
        with self.assertRaises(SkillNecessityInvalidatedError):
            service.get_active(run_id)
        with self.assertRaises(SkillNecessityInvalidatedError):
            service.evaluate(evaluate_command(
                run_id,
                snapshot.snapshot_id,
                snapshot.snapshot_hash,
                command_id="retry-invalidated-skill-necessity",
                expected_version=34,
            ))
        self.assertEqual(repository.events(run_id)[before:][-1].event_type, "SkillNecessityInvalidated")
        self.assertIn(
            "synthetic_skill_necessity_invalidated",
            {item.event_name for item in observations.observations},
        )


if __name__ == "__main__":
    unittest.main()
