from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.application.ports import AtomicCommitFailed, IdempotencyPayloadMismatch
from cmf_builder.domain.context_manifest import (
    ContextInputInvalid,
    ContextInvalidatedError,
    ContextStateInvalid,
)
from cmf_builder.domain.harness_ir import HarnessIRAuthorityRejected
from tests.stories.st_04_05 import build_context, compile_command


class MinimumCompleteContextFailureTests(unittest.TestCase):
    def test_non_code_actor_cannot_compile(self) -> None:
        service, _, _, repository, _, run_id, _ = build_context()
        before = repository.event_count(run_id)
        with self.assertRaises((HarnessIRAuthorityRejected, AuthorityDenied)):
            service.compile(compile_command(run_id, actor_id="architect-1"))
        self.assertEqual(repository.event_count(run_id), before)

    def test_wrong_input_hash_or_path_fails_before_state_change(self) -> None:
        service, _, _, repository, observations, run_id, _ = build_context()
        before = repository.event_count(run_id)
        for command in (
            compile_command(run_id, context_input_sha256="0" * 64),
            compile_command(run_id, context_input_path="development-capsules/ST-04.04/PHASE_HANDOFF_INPUT.json"),
        ):
            with self.subTest(command=command), self.assertRaises(ContextInputInvalid):
                service.compile(command)
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.minimum_context_graph_count, 0)
        self.assertEqual(observations.observations[-1].outcome, "FAIL")

    def test_injected_atomic_failure_leaves_zero_partial_state(self) -> None:
        service, _, _, repository, _, run_id, _ = build_context()
        before = repository.event_count(run_id)
        repository.inject_next_atomic_commit_failure()
        with self.assertRaises(AtomicCommitFailed):
            service.compile(compile_command(run_id))
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.minimum_context_graph_count, 0)
        self.assertEqual(repository.context_compilation_receipt_count, 0)
        self.assertIsNone(repository.get_command_record("minimum-context-1"))

    def test_rejected_handoff_cannot_supply_minimum_context(self) -> None:
        service, _, _, repository, _, run_id, _ = build_context()
        handoff = repository.internal_handoffs(run_id)[0]
        decision = repository.get_internal_handoff_decision(handoff.handoff_id)
        assert decision is not None
        repository._internal_handoff_decisions[handoff.handoff_id] = replace(
            decision,
            action=type(decision.action).REJECTED,
        )
        with self.assertRaises(ContextStateInvalid):
            service.compile(compile_command(run_id))

    def test_command_payload_conflict_fails_without_duplicate_state(self) -> None:
        service, _, _, repository, _, run_id, _ = build_context()
        command = compile_command(run_id)
        service.compile(command)
        before = repository.event_count(run_id)
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.compile(replace(command, actor_id="architect-1"))
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.minimum_context_graph_count, 1)

    def test_active_parent_hash_drift_fails_closed(self) -> None:
        service, _, _, repository, _, run_id, _ = build_context()
        run = repository.load_run(run_id)
        repository._streams[run_id] = tuple(
            replace(event, payload=tuple(
                (key, "sha256:" + "0" * 64 if event.event_type == "PhaseHandoffsAttached" and key == "graph_hash" else value)
                for key, value in event.payload
            ))
            for event in repository.events(run_id)
        )
        with self.assertRaises(ContextStateInvalid):
            service.compile(compile_command(run_id))


if __name__ == "__main__":
    unittest.main()
