from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.application.ports import AtomicCommitFailed, IdempotencyPayloadMismatch
from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.domain.handoff import (
    HandoffAuthorityInvalid,
    HandoffContractInvalid,
    HandoffInputInvalid,
    HandoffLineageInvalid,
    HandoffStateInvalid,
)
from cmf_builder.domain.harness_ir import HarnessIRAuthorityRejected
from tests.stories.st_04_04 import (
    build_context,
    compile_command,
    decision_command,
    governed_artifacts,
    issue_command,
)


class InternalHandoffFailureTests(unittest.TestCase):
    def test_non_code_actor_cannot_compile_issue_or_decide(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        with self.assertRaises(HarnessIRAuthorityRejected):
            service.compile(compile_command(run_id, actor_id="architect-1"))
        service.compile(compile_command(run_id))
        artifacts = governed_artifacts(service, repository, run_id)
        with self.assertRaises(AuthorityDenied):
            service.issue(issue_command(run_id, artifacts, actor_id="agent-1"))

    def test_wrong_input_pin_fails_before_state_change(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        before = repository.event_count(run_id)
        with self.assertRaises(HandoffInputInvalid):
            service.compile(compile_command(run_id, handoff_input_sha256="0" * 64))
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.phase_handoff_graph_count, 0)

    def test_injected_compile_failure_leaves_zero_partial_state(self) -> None:
        service, _, repository, observations, run_id, _ = build_context()
        before_events = repository.event_count(run_id)
        repository.inject_next_atomic_commit_failure()
        with self.assertRaises(AtomicCommitFailed):
            service.compile(compile_command(run_id))
        self.assertEqual(repository.event_count(run_id), before_events)
        self.assertEqual(repository.phase_handoff_graph_count, 0)
        self.assertEqual(repository.phase_handoff_receipt_count, 0)
        self.assertIsNone(repository.get_command_record("phase-handoffs-1"))
        self.assertEqual(observations.observations[-1].outcome, "FAIL")

    def test_issue_rejects_missing_altered_or_stale_artifacts(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        service.compile(compile_command(run_id))
        artifacts = governed_artifacts(service, repository, run_id)
        candidates = (
            artifacts[:-1],
            (replace(artifacts[0], artifact_hash="sha256:" + "0" * 64), artifacts[1]),
            (replace(artifacts[0], version="2.0.0"), artifacts[1]),
            (replace(artifacts[0], lineage_refs=artifacts[0].lineage_refs[:-1]), artifacts[1]),
        )
        for candidate in candidates:
            with self.subTest(candidate=candidate), self.assertRaises((HandoffContractInvalid, HandoffLineageInvalid)):
                service.issue(issue_command(run_id, candidate))
        self.assertEqual(repository.internal_handoff_count, 0)

    def test_wrong_sender_or_receiver_is_rejected(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        service.compile(compile_command(run_id))
        artifacts = governed_artifacts(service, repository, run_id)
        for command in (
            issue_command(run_id, artifacts, sender_phase="governed_contract_ready"),
            issue_command(run_id, artifacts, receiver_phase="ratified_boundary_ready"),
        ):
            with self.assertRaises(HandoffContractInvalid):
                service.issue(command)

    def test_receiver_authority_and_decision_rules_fail_closed(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        service.compile(compile_command(run_id))
        issued = service.issue(issue_command(run_id, governed_artifacts(service, repository, run_id)))
        candidates = (
            decision_command(run_id, issued.handoff_id, receiver_authority="cmf_builder.atomicity"),
            decision_command(run_id, issued.handoff_id, receiver_phase="ratified_boundary_ready"),
            decision_command(run_id, issued.handoff_id, reason_code="INVALID_ACCEPTANCE"),
        )
        for command in candidates:
            with self.subTest(command=command), self.assertRaises((HandoffAuthorityInvalid, HandoffStateInvalid)):
                service.decide(command)
        self.assertEqual(repository.internal_handoff_decision_count, 0)

    def test_command_payload_conflict_fails_closed(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        command = compile_command(run_id)
        service.compile(command)
        before = repository.event_count(run_id)
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.compile(replace(command, actor_id="architect-1"))
        self.assertEqual(repository.event_count(run_id), before)

    def test_injected_issue_and_decision_failures_are_atomic(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        service.compile(compile_command(run_id))
        artifacts = governed_artifacts(service, repository, run_id)
        repository.inject_next_atomic_commit_failure()
        with self.assertRaises(AtomicCommitFailed):
            service.issue(issue_command(run_id, artifacts))
        self.assertEqual(repository.internal_handoff_count, 0)
        issued = service.issue(issue_command(run_id, artifacts, command_id="issue-after-failure"))
        before = repository.event_count(run_id)
        repository.inject_next_atomic_commit_failure()
        with self.assertRaises(AtomicCommitFailed):
            service.decide(decision_command(run_id, issued.handoff_id, expected_version=18))
        self.assertEqual(repository.event_count(run_id), before)
        self.assertEqual(repository.internal_handoff_decision_count, 0)


if __name__ == "__main__":
    unittest.main()
