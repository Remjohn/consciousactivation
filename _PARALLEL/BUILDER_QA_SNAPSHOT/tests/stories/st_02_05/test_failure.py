from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from cmf_builder.adapters.file_declared_boundary_repository import (
    FileDeclaredBoundaryRepository,
)
from cmf_builder.application.atomicity_commands import (
    AtomicityCommandRejected,
    DECLARED_INPUT_PATH,
    DECLARED_INPUT_SHA256,
)
from cmf_builder.application.ports import AtomicCommitFailed, IdempotencyPayloadMismatch
from cmf_builder.domain.atomicity import (
    AuthorityStatus,
    BoundaryImmutable,
    BoundaryInputHashMismatch,
    BoundaryInputMismatch,
    CriticalBoundaryContradiction,
    DecisionPackageIncomplete,
    FieldAuthorityRejected,
)
from tests.stories.st_01_01_synthetic_proof import ROOT
from tests.stories.st_02_05 import (
    build_context,
    changed_decision,
    decide_command,
    decision,
)


class StubDeclaredInputRepository:
    def __init__(self, value) -> None:
        self.value = value

    def load(self, relative_path: str, expected_sha256: str):
        return self.value


class AtomicityFailureTests(unittest.TestCase):
    def test_ac_01_mutated_declared_input_bytes_fail_hash_verification(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / DECLARED_INPUT_PATH
            path.parent.mkdir(parents=True)
            path.write_bytes((ROOT / DECLARED_INPUT_PATH).read_bytes() + b"\n")
            repository = FileDeclaredBoundaryRepository(root)
            with self.assertRaises(BoundaryInputHashMismatch):
                repository.load(DECLARED_INPUT_PATH, DECLARED_INPUT_SHA256)

    def test_ac_01_command_cannot_substitute_input_path_or_hash(self) -> None:
        cases = (
            {"declared_input_path": "format02/boundary.json"},
            {"declared_input_sha256": "0" * 64},
        )
        for index, changes in enumerate(cases):
            with self.subTest(changes=changes):
                service, repository, _, run_id, _ = build_context()
                with self.assertRaises(AtomicityCommandRejected):
                    service.decide(
                        decide_command(run_id, command_id=f"substitute-{index}", **changes)
                    )
                self.assertEqual(repository.event_count(run_id), 5)
                self.assertEqual(repository.atomic_boundary_count, 0)

    def test_ac_01_source_lock_constraint_mismatch_fails_closed(self) -> None:
        governed = FileDeclaredBoundaryRepository(ROOT).load(
            DECLARED_INPUT_PATH, DECLARED_INPUT_SHA256
        )
        mismatched = replace(governed, source_profile_hash="0" * 64)
        service, repository, _, run_id, _ = build_context(
            input_repository=StubDeclaredInputRepository(mismatched)
        )
        with self.assertRaises(BoundaryInputMismatch):
            service.decide(decide_command(run_id))
        self.assertEqual(repository.event_count(run_id), 5)
        self.assertEqual(repository.atomicity_receipt_count, 0)

    def test_ac_02_incomplete_human_decision_packages_are_rejected(self) -> None:
        cases = (
            {"selected_candidate": None},
            {"rejected_alternatives": ()},
            {"evidence_refs": ()},
            {"rationale": ""},
            {"accepted_risks": ()},
        )
        for index, changes in enumerate(cases):
            with self.subTest(changes=changes):
                service, repository, _, run_id, _ = build_context()
                with self.assertRaises(DecisionPackageIncomplete):
                    service.decide(
                        decide_command(
                            run_id,
                            command_id=f"incomplete-{index}",
                            atomicity_decision=changed_decision(decision(), **changes),
                        )
                    )
                self.assertEqual(repository.event_count(run_id), 5)
                self.assertEqual(repository.atomic_boundary_count, 0)

    def test_ac_02_critical_contradiction_prevents_freeze(self) -> None:
        governed = FileDeclaredBoundaryRepository(ROOT).load(
            DECLARED_INPUT_PATH, DECLARED_INPUT_SHA256
        )
        contradicted = replace(
            governed,
            critical_contradictions=("input_and_output_cardinality_conflict",),
        )
        service, repository, _, run_id, _ = build_context(
            input_repository=StubDeclaredInputRepository(contradicted)
        )
        with self.assertRaises(CriticalBoundaryContradiction):
            service.decide(decide_command(run_id))
        self.assertEqual(repository.atomic_boundary_count, 0)
        self.assertEqual(repository.event_count(run_id), 5)

    def test_ac_08_stale_version_and_command_payload_reuse_fail(self) -> None:
        service, repository, _, run_id, _ = build_context()
        with self.assertRaises(AtomicityCommandRejected):
            service.decide(decide_command(run_id, expected_version=4))
        command = decide_command(run_id, command_id="idempotent")
        service.decide(command)
        with self.assertRaises(IdempotencyPayloadMismatch):
            service.decide(
                decide_command(
                    run_id,
                    command_id="idempotent",
                    expected_version=9,
                    atomicity_decision=changed_decision(
                        decision(), rationale="A different decision payload."
                    ),
                )
            )
        self.assertEqual(repository.atomic_boundary_count, 1)

    def test_ac_08_11_atomic_failure_leaves_no_partial_state_and_retry_commits(self) -> None:
        service, repository, _, run_id, _ = build_context()
        command = decide_command(run_id, command_id="atomic-failure")
        repository.inject_next_atomic_commit_failure()
        with self.assertRaises(AtomicCommitFailed):
            service.decide(command)
        self.assertEqual(repository.event_count(run_id), 5)
        self.assertEqual(repository.atomic_boundary_count, 0)
        self.assertEqual(repository.draft_harness_model_count, 0)
        self.assertEqual(repository.atomicity_receipt_count, 0)
        self.assertIsNone(repository.get_command_record(command.command_id))
        receipt = service.decide(command)
        self.assertEqual(receipt.hg_003_result, "PASS")
        self.assertEqual(repository.event_count(run_id), 9)

    def test_ac_07_same_version_boundary_rewrite_is_prohibited(self) -> None:
        service, repository, _, run_id, _ = build_context()
        receipt = service.decide(decide_command(run_id))
        boundary = repository.get_atomic_boundary(receipt.boundary_ref)
        with self.assertRaises(BoundaryImmutable):
            boundary.require_new_version(
                candidate_version=boundary.version,
                candidate_boundary=boundary.boundary + " Broadened.",
            )

    def test_ac_04_unratified_not_applicable_and_hypothesis_fields_fail_consumption(self) -> None:
        service, _, _, run_id, _ = build_context()
        service.decide(decide_command(run_id))
        for name in ("runtime_hypotheses", "visual_syntax", "production_promise"):
            with self.subTest(field=name), self.assertRaises(FieldAuthorityRejected):
                service.consume_field(
                    run_id=run_id,
                    field_name=name,
                    required_authority=AuthorityStatus.HUMAN_RATIFIED,
                )


if __name__ == "__main__":
    unittest.main()
