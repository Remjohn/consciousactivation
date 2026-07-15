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
from cmf_builder.domain.atomic_harness_definition import DefinitionInvalidatedError
from cmf_builder.domain.run import Run
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_07_02 import build_context, compile_command


class AtomicHarnessDefinitionReplayInvalidationTests(unittest.TestCase):
    def _complete(self, *, seed: str = "ST-07.02-replay"):
        service, atomicity, repository, observations, run_id, _, _, _ = build_context(seed=seed)
        receipt = service.compile(compile_command(run_id))
        return service, atomicity, repository, observations, run_id, receipt, service.get_active(run_id)

    def test_repeat_command_is_payload_safe_and_observable(self) -> None:
        service, _, repository, observations, run_id, receipt, definition = self._complete()
        before = repository.event_count(run_id)
        self.assertEqual(service.compile(compile_command(run_id)), receipt)
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.atomic_harness_definition_count, 1)
        self.assertEqual(service.get_active(run_id), definition)
        self.assertEqual(observations.observations[-1].event_name, "synthetic_atomic_harness_definition_replayed")

    def test_run_replay_preserves_definition_identity_and_state_hash(self) -> None:
        _, _, repository, _, run_id, _, definition = self._complete()
        loaded = repository.load_run(run_id)
        replayed = Run.replay(repository.events(run_id))
        self.assertEqual(replayed, loaded)
        self.assertEqual(replayed.state_hash(), loaded.state_hash())
        self.assertEqual(replayed.atomic_harness_definition_ref, definition.definition_id)
        self.assertEqual(replayed.atomic_harness_definition_hash, definition.definition_hash)

    def test_checkpoint_resume_preserves_active_definition(self) -> None:
        service, _, repository, observations, run_id, _, definition = self._complete()
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
            ids=DeterministicUuid7IdProvider(timestamp_ms=1_768_005_000_000, seed="ST-07.02-resume"),
            clock=FixedClock(NOW),
            observations=observations,
        )
        checkpoint = run_service.create_checkpoint(CreateCheckpointCommand(
            command_id="st-07-02-checkpoint",
            run_id=run_id,
            input_hash="synthetic-atomic-harness-definition-input",
            policy_hash="builder-core-constitutional-precedence",
            actor_id="architect-1",
            expected_version=23,
            correlation_id="st-07-02-resume",
            causation_id=definition.definition_id,
        ))
        run_service.resume_run(ResumeRunCommand(
            command_id="st-07-02-resume",
            run_id=run_id,
            input_hash="synthetic-atomic-harness-definition-input",
            policy_hash="builder-core-constitutional-precedence",
            actor_id="architect-1",
            expected_version=24,
            correlation_id="st-07-02-resume",
            causation_id=checkpoint.receipt_id,
        ))
        resumed = repository.load_run(run_id)
        self.assertEqual(resumed.atomic_harness_definition_ref, definition.definition_id)
        self.assertEqual(service.get_active(run_id), definition)

    def test_upstream_reopen_invalidates_active_definition_and_preserves_history(self) -> None:
        service, atomicity, repository, observations, run_id, _, definition = self._complete()
        before = repository.event_count(run_id)
        result = atomicity.reopen(ReopenAtomicBoundaryCommand(
            command_id="reopen-after-definition",
            run_id=run_id,
            actor_id="architect-1",
            expected_version=23,
            correlation_id="reopen-definition-correlation",
            causation_id=definition.definition_id,
            reason="Authorized upstream correction invalidates the definition.",
        ))
        run = repository.load_run(run_id)
        self.assertEqual(run.stream_version, 36)
        self.assertEqual(run.atomic_harness_definition_invalidation_ref, result.invalidation_ref)
        self.assertTrue(repository.is_atomic_harness_definition_invalidated(definition.definition_id))
        invalidation = repository.get_atomic_harness_definition_invalidation(result.invalidation_ref)
        assert invalidation is not None
        self.assertEqual(invalidation.definition_ref, definition.definition_id)
        self.assertEqual(service.get_historical(definition.definition_id).canonical_bytes(), definition.canonical_bytes())
        with self.assertRaises(DefinitionInvalidatedError):
            service.get_active(run_id)
        with self.assertRaises(DefinitionInvalidatedError):
            service.compile(compile_command(run_id, command_id="retry-invalidated-definition", expected_version=36))
        self.assertEqual(repository.events(run_id)[before:][-1].event_type, "AtomicHarnessDefinitionInvalidated")
        self.assertIn("synthetic_atomic_harness_definition_invalidated", {item.event_name for item in observations.observations})


if __name__ == "__main__":
    unittest.main()
