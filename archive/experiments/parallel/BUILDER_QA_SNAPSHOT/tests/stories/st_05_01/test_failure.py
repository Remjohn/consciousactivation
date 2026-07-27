from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.ports import AtomicCommitFailed, IdempotencyPayloadMismatch
from cmf_builder.domain.harness_ir import HarnessIRAuthorityRejected
from cmf_builder.domain.skill_registry import (
    SkillRegistryAuthorityInvalid,
    SkillRegistryContractInvalid,
    SkillRegistryInputInvalid,
    UndeclaredSkillRequirement,
)
from tests.stories.st_05_01 import build_context, compile_command


class SyntheticSkillRegistryFailureTests(unittest.TestCase):
    def test_ac_04_wrong_input_or_governance_pin_fails_without_state(self) -> None:
        service, _, repository, observations, run_id, _, _ = build_context()
        before = repository.event_count(run_id)
        commands = (
            compile_command(run_id, registry_input_sha256="0" * 64),
            compile_command(run_id, registry_fixture_sha256="0" * 64),
            compile_command(run_id, policy_sha256="0" * 64),
            compile_command(run_id, schema_sha256="0" * 64),
            compile_command(run_id, validation_receipt_sha256="0" * 64),
        )
        for command in commands:
            with self.subTest(command=command), self.assertRaises(SkillRegistryInputInvalid):
                service.compile(command)
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.skill_registry_snapshot_count, 0)
        self.assertEqual(observations.observations[-1].outcome, "FAIL")

    def test_ac_05_undeclared_skill_and_same_version_mutation_fail_closed(self) -> None:
        service, _, repository, _, run_id, _, _ = build_context()
        before = repository.event_count(run_id)
        with self.assertRaises(UndeclaredSkillRequirement):
            service.compile(
                compile_command(run_id, declared_external_skill_ids=("invented-skill",))
            )
        with self.assertRaises(SkillRegistryContractInvalid):
            service.compile(
                compile_command(
                    run_id,
                    capability_overrides=(("governed_run_lifecycle", "external_skill"),),
                )
            )
        self.assertEqual(repository.event_count(run_id), before)

    def test_ac_06_relation_maturity_and_evaluator_sediment_are_rejected(self) -> None:
        service, _, repository, _, run_id, _, _ = build_context()
        for command in (
            compile_command(run_id, relation_edges=(("a", "b"),)),
            compile_command(run_id, evaluator_receipt_ids=("stale-evaluator",)),
            compile_command(run_id, active_maturity_claims=(("capability", "STABLE"),)),
        ):
            with self.subTest(command=command), self.assertRaises(SkillRegistryContractInvalid):
                service.compile(command)
        self.assertEqual(repository.skill_registry_snapshot_count, 0)

    def test_ac_07_unauthorized_actor_and_prohibited_operations_are_rejected(self) -> None:
        service, _, repository, _, run_id, _, _ = build_context()
        with self.assertRaises((HarnessIRAuthorityRejected, AuthorityDenied)):
            service.compile(compile_command(run_id, actor_id="architect-1"))
        for operation in ("register_skill", "discover_skill", "execute_skill", "compile_recipe"):
            with self.subTest(operation=operation), self.assertRaises(SkillRegistryAuthorityInvalid):
                service.compile(compile_command(run_id, requested_operation=operation))
        self.assertEqual(repository.skill_registry_snapshot_count, 0)

    def test_ac_10_injected_atomic_failure_leaves_zero_partial_state_then_retry_succeeds(self) -> None:
        service, _, repository, _, run_id, _, _ = build_context()
        before = repository.event_count(run_id)
        repository.inject_next_atomic_commit_failure()
        with self.assertRaises(AtomicCommitFailed):
            service.compile(compile_command(run_id))
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.skill_registry_snapshot_count, 0)
        self.assertEqual(repository.skill_registry_consumption_receipt_count, 0)
        self.assertIsNone(repository.get_command_record("synthetic-skill-registry-1"))
        receipt = service.compile(compile_command(run_id))
        self.assertEqual(receipt.outcome, "PASS")

    def test_conflicting_command_payload_fails_without_duplicate_state(self) -> None:
        service, _, repository, _, run_id, _, _ = build_context()
        command = compile_command(run_id)
        service.compile(command)
        before = repository.event_count(run_id)
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.compile(replace(command, causation_id="conflicting-payload"))
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.skill_registry_snapshot_count, 1)


if __name__ == "__main__":
    unittest.main()
