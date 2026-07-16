from __future__ import annotations

import unittest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.domain.atomicity import AuthorityStatus, FieldAuthorityRejected
from cmf_builder.domain.run import Run
from tests.stories.st_02_05 import (
    build_context,
    decide_command,
    reopen_command,
)


class AtomicityReplayReceiptTests(unittest.TestCase):
    def test_ac_08_replay_returns_identical_receipt_without_duplicate_events(self) -> None:
        service, repository, observations, run_id, _ = build_context()
        command = decide_command(run_id, command_id="replay-command")
        first = service.decide(command)
        event_count = repository.event_count(run_id)
        second = service.decide(command)
        self.assertEqual(first, second)
        self.assertEqual(repository.event_count(run_id), event_count)
        self.assertTrue(any(item.event_name == "ST-02.05:DecisionReplayReturned" for item in observations.observations))

    def test_ac_09_success_observations_have_complete_governed_identity(self) -> None:
        service, _, observations, run_id, _ = build_context()
        receipt = service.decide(decide_command(run_id))
        story_events = [item for item in observations.observations if item.story_id == "ST-02.05"]
        self.assertEqual(
            [item.event_name for item in story_events],
            [
                "ST-02.05:BoundaryRatified",
                "ST-02.05:DraftModelCompiled",
                "ST-02.05:BoundaryFrozen",
                "ST-02.05:OutcomeVerified",
            ],
        )
        for item in story_events:
            self.assertEqual(item.run_id, run_id)
            self.assertEqual(item.story_id, "ST-02.05")
            self.assertEqual(item.authority_identity, "architect-1")
            self.assertEqual(item.declared_input_hash, receipt.declared_input_hash)
            self.assertEqual(item.boundary_id, receipt.boundary_ref)
            self.assertEqual(item.boundary_version, "1.0.0")
            self.assertEqual(item.model_id, receipt.model_ref)
            self.assertEqual(item.decision_receipt_id, receipt.receipt_id)
            self.assertEqual(item.hg_003, "PASS")
            self.assertEqual(item.outcome, "PASS")

    def test_ac_09_rejection_observations_prove_zero_authoritative_mutation(self) -> None:
        service, repository, observations, run_id, _ = build_context()
        with self.assertRaises(Exception):
            service.decide(decide_command(run_id, declared_input_sha256="0" * 64))
        story_events = [item for item in observations.observations if item.story_id == "ST-02.05"]
        self.assertEqual(
            [item.event_name for item in story_events],
            ["ST-02.05:BoundaryDecisionRejected", "ST-02.05:OutcomeRejected"],
        )
        self.assertTrue(all(item.outcome == "FAIL" for item in story_events))
        self.assertTrue(all("code" in item.failure_context for item in story_events))
        self.assertEqual(repository.event_count(run_id), 5)
        self.assertEqual(repository.atomicity_receipt_count, 0)

    def test_ac_07_reopen_emits_invalidation_and_blocks_the_old_model(self) -> None:
        service, repository, observations, run_id, _ = build_context()
        approved = service.decide(decide_command(run_id))
        reopened = service.reopen(reopen_command(run_id))
        invalidation = repository.get_boundary_invalidation(reopened.invalidation_ref)
        run = repository.load_run(run_id)

        self.assertEqual(reopened.decision_status, "REOPENED")
        self.assertEqual(reopened.hg_003_result, "FAIL")
        self.assertTrue(invalidation.new_version_required)
        self.assertEqual(invalidation.boundary_ref, approved.boundary_ref)
        self.assertEqual(invalidation.model_ref, approved.model_ref)
        self.assertEqual(run.boundary_invalidation_ref, reopened.invalidation_ref)
        self.assertTrue(repository.is_boundary_invalidated(approved.boundary_ref))
        self.assertTrue(repository.is_model_invalidated(approved.model_ref))
        self.assertIn("ST-02.05:BoundaryReopened", [item.event_name for item in observations.observations])
        with self.assertRaises(FieldAuthorityRejected):
            service.consume_field(
                run_id=run_id,
                field_name="atomic_boundary",
                required_authority=AuthorityStatus.HUMAN_RATIFIED,
            )

    def test_ac_07_unauthorized_reopen_preserves_frozen_state(self) -> None:
        service, repository, _, run_id, _ = build_context()
        approved = service.decide(decide_command(run_id))
        with self.assertRaises(AuthorityDenied):
            service.reopen(reopen_command(run_id, actor_id="agent-1"))
        self.assertEqual(repository.event_count(run_id), 9)
        self.assertFalse(repository.is_boundary_invalidated(approved.boundary_ref))
        self.assertEqual(repository.boundary_invalidation_count, 0)

    def test_ac_08_event_replay_reconstructs_boundary_refs_and_state_hash(self) -> None:
        service, repository, _, run_id, _ = build_context()
        receipt = service.decide(decide_command(run_id))
        current = repository.load_run(run_id)
        replayed = Run.replay(repository.events(run_id))
        self.assertEqual(replayed, current)
        self.assertEqual(replayed.state_hash(), current.state_hash())
        self.assertEqual(replayed.atomic_boundary_ref, receipt.boundary_ref)
        self.assertEqual(replayed.draft_harness_model_ref, receipt.model_ref)


if __name__ == "__main__":
    unittest.main()
