from __future__ import annotations

import unittest

from cmf_builder.application.atomicity_commands import ReopenAtomicBoundaryCommand
from cmf_builder.domain.constitutional_validation import (
    ConstitutionalValidationInvalidatedError,
)
from cmf_builder.domain.run import Run
from tests.stories.st_03_05 import build_context, validate_command


class ReplayInvalidationAndReceiptTests(unittest.TestCase):
    def test_repeat_command_returns_same_receipt_without_new_event(self) -> None:
        service, _, repository, observations, run_id, _ = build_context()
        first = service.validate(validate_command(run_id))
        count = repository.event_count(run_id)
        second = service.validate(validate_command(run_id))
        self.assertEqual(second, first)
        self.assertEqual(repository.event_count(run_id), count)
        self.assertIn(
            "ST-03.05:ValidationReplayReturned",
            {item.event_name for item in observations.observations},
        )

    def test_fresh_deterministic_contexts_produce_identical_evidence(self) -> None:
        first_service, _, first_repo, _, first_run, _ = build_context(seed="same")
        second_service, _, second_repo, _, second_run, _ = build_context(seed="same")
        first_receipt = first_service.validate(validate_command(first_run))
        second_receipt = second_service.validate(validate_command(second_run))
        first_report = first_repo.get_constitutional_validation_report(
            first_receipt.report_id
        )
        second_report = second_repo.get_constitutional_validation_report(
            second_receipt.report_id
        )
        self.assertEqual(first_report, second_report)
        self.assertEqual(first_receipt, second_receipt)
        self.assertEqual(first_report.canonical_bytes(), second_report.canonical_bytes())

    def test_run_event_replay_preserves_validation_identity(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        receipt = service.validate(validate_command(run_id))
        loaded = repository.load_run(run_id)
        replayed = Run.replay(repository.events(run_id))
        self.assertEqual(replayed, loaded)
        self.assertEqual(replayed.state_hash(), loaded.state_hash())
        self.assertEqual(replayed.constitutional_validation_ref, receipt.report_id)

    def test_upstream_reopen_invalidates_active_validation_but_preserves_history(self) -> None:
        service, atomicity, repository, observations, run_id, _ = build_context()
        validation_receipt = service.validate(validate_command(run_id))
        reopen = atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-after-validation",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=13,
                correlation_id="reopen-correlation",
                causation_id=validation_receipt.receipt_id,
                reason="Authorized correction requires a new immutable version.",
            )
        )
        run = repository.load_run(run_id)
        self.assertEqual(run.stream_version, 18)
        self.assertEqual(
            run.constitutional_validation_invalidation_ref,
            reopen.invalidation_ref,
        )
        self.assertTrue(
            repository.is_constitutional_validation_invalidated(
                validation_receipt.report_id
            )
        )
        with self.assertRaises(ConstitutionalValidationInvalidatedError):
            service.get_active(run_id)
        historical = service.get_historical(validation_receipt.report_id)
        self.assertEqual(historical.report_id, validation_receipt.report_id)
        self.assertIn(
            "ST-03.05:ConstitutionalValidationInvalidated",
            {item.event_name for item in observations.observations},
        )

    def test_invalidation_receipt_links_to_artifact_invalidation(self) -> None:
        service, atomicity, repository, _, run_id, _ = build_context()
        receipt = service.validate(validate_command(run_id))
        reopened = atomicity.reopen(
            ReopenAtomicBoundaryCommand(
                command_id="reopen-linkage",
                run_id=run_id,
                actor_id="architect-1",
                expected_version=13,
                correlation_id="reopen-correlation",
                causation_id=receipt.receipt_id,
                reason="Linkage test.",
            )
        )
        invalidation = repository.get_constitutional_validation_invalidation(
            reopened.invalidation_ref
        )
        artifact_invalidation = repository.get_artifact_set_invalidation(
            reopened.invalidation_ref
        )
        self.assertIsNotNone(invalidation)
        self.assertIsNotNone(artifact_invalidation)
        self.assertEqual(invalidation.report_ref, receipt.report_id)
        self.assertEqual(
            invalidation.upstream_invalidation_ref,
            artifact_invalidation.invalidation_id,
        )


if __name__ == "__main__":
    unittest.main()
