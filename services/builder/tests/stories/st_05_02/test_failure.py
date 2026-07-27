from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.ports import (
    AtomicCommitFailed,
    ConcurrencyConflict,
    IdempotencyPayloadMismatch,
)
from cmf_builder.domain.harness_ir import HarnessIRAuthorityRejected
from cmf_builder.domain.skill_registry import (
    SkillNecessityAuthorityInvalid,
    SkillNecessityEvidenceInvalid,
    SkillNecessityInvalidatedError,
)
from tests.stories.st_05_02 import build_context, evaluate_command


class SyntheticSkillNecessityFailureTests(unittest.TestCase):
    def test_wrong_input_path_or_hash_fails_without_partial_state(self) -> None:
        service, _, repository, observations, run_id, _, _, snapshot = build_context()
        before = repository.event_count(run_id)
        commands = (
            evaluate_command(
                run_id,
                snapshot.snapshot_id,
                snapshot.snapshot_hash,
                necessity_input_path="development-capsules/ST-05.02/missing.json",
            ),
            evaluate_command(
                run_id,
                snapshot.snapshot_id,
                snapshot.snapshot_hash,
                necessity_input_sha256="0" * 64,
            ),
        )
        for command in commands:
            with self.subTest(command=command), self.assertRaises(SkillNecessityEvidenceInvalid):
                service.evaluate(command)
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.skill_necessity_decision_count, 0)
        self.assertEqual(observations.observations[-1].outcome, "FAIL")

    def test_wrong_snapshot_identity_or_hash_fails_closed(self) -> None:
        service, _, repository, _, run_id, _, _, snapshot = build_context()
        for command in (
            evaluate_command(run_id, "wrong-snapshot", snapshot.snapshot_hash),
            evaluate_command(run_id, snapshot.snapshot_id, "sha256:" + "0" * 64),
        ):
            with self.subTest(command=command), self.assertRaises(SkillNecessityInvalidatedError):
                service.evaluate(command)
        with self.assertRaises(ConcurrencyConflict):
            service.evaluate(evaluate_command(
                run_id,
                snapshot.snapshot_id,
                snapshot.snapshot_hash,
                expected_version=20,
            ))
        self.assertEqual(repository.skill_necessity_decision_count, 0)

    def test_unauthorized_actor_and_prohibited_operations_are_rejected(self) -> None:
        service, _, repository, _, run_id, _, _, snapshot = build_context()
        with self.assertRaises((HarnessIRAuthorityRejected, AuthorityDenied)):
            service.evaluate(evaluate_command(
                run_id, snapshot.snapshot_id, snapshot.snapshot_hash, actor_id="architect-1"
            ))
        for operation in ("design_skill", "discover_skill", "execute_skill", "package_skill"):
            with self.subTest(operation=operation), self.assertRaises(SkillNecessityAuthorityInvalid):
                service.evaluate(evaluate_command(
                    run_id,
                    snapshot.snapshot_id,
                    snapshot.snapshot_hash,
                    requested_operation=operation,
                ))
        self.assertEqual(repository.skill_necessity_decision_count, 0)

    def test_injected_atomic_failure_leaves_zero_partial_state_then_retry_succeeds(self) -> None:
        service, _, repository, _, run_id, _, _, snapshot = build_context()
        command = evaluate_command(run_id, snapshot.snapshot_id, snapshot.snapshot_hash)
        before = repository.event_count(run_id)
        repository.inject_next_atomic_commit_failure()
        with self.assertRaises(AtomicCommitFailed):
            service.evaluate(command)
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.skill_necessity_decision_count, 0)
        self.assertEqual(repository.skill_necessity_receipt_count, 0)
        self.assertIsNone(repository.get_command_record(command.command_id))
        receipt = service.evaluate(command)
        self.assertEqual(receipt.outcome, "NO_NEW_SKILL_REQUIRED")

    def test_conflicting_command_payload_fails_without_duplicate_state(self) -> None:
        service, _, repository, _, run_id, _, _, snapshot = build_context()
        command = evaluate_command(run_id, snapshot.snapshot_id, snapshot.snapshot_hash)
        service.evaluate(command)
        before = repository.event_count(run_id)
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.evaluate(replace(command, causation_id="conflicting-payload"))
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.skill_necessity_decision_count, 1)


if __name__ == "__main__":
    unittest.main()
