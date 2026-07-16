from __future__ import annotations

import unittest

from cmf_builder.domain.harness_ir import (
    HARNESS_IR_SCHEMA_ID,
    HARNESS_IR_SCHEMA_VERSION,
    REQUIRED_SECTIONS,
)
from cmf_builder.domain.run import LifecycleState
from tests.stories.st_03_03 import build_context, compile_command


class HarnessIRAcceptanceTests(unittest.TestCase):
    def test_ac_01_02_compiles_one_immutable_revision_from_exact_upstream(self) -> None:
        service, _, repository, _, run_id, approval = build_context()
        receipt = service.compile(compile_command(run_id))
        snapshot = repository.get_harness_ir(receipt.ir_id)
        run = repository.load_run(run_id)
        self.assertEqual(snapshot.schema_id, HARNESS_IR_SCHEMA_ID)
        self.assertEqual(snapshot.schema_version, HARNESS_IR_SCHEMA_VERSION)
        self.assertEqual(snapshot.revision, 1)
        self.assertEqual(snapshot.source_lock_ref, approval.source_lock_ref)
        self.assertEqual(snapshot.boundary_ref, approval.boundary_ref)
        self.assertEqual(snapshot.model_ref, approval.model_ref)
        self.assertEqual(snapshot.ratification_ref, approval.ratification_ref)
        self.assertEqual(run.harness_ir_ref, snapshot.ir_id)
        self.assertEqual(run.lifecycle_state, LifecycleState.GENESIS)

    def test_ac_02_contains_every_required_typed_section(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        snapshot = repository.get_harness_ir(receipt.ir_id)
        self.assertEqual(tuple(section.name for section in snapshot.sections), REQUIRED_SECTIONS)
        self.assertTrue(all(section.values for section in snapshot.sections))

    def test_ac_01_preserves_exact_run_source_boundary_model_and_ratification(self) -> None:
        service, _, repository, _, run_id, approval = build_context()
        receipt = service.compile(compile_command(run_id))
        snapshot = repository.get_harness_ir(receipt.ir_id)
        self.assertEqual(snapshot.run_id, run_id)
        self.assertEqual(snapshot.source_lock_ref, approval.source_lock_ref)
        self.assertEqual(snapshot.boundary_ref, approval.boundary_ref)
        self.assertEqual(snapshot.model_ref, approval.model_ref)
        self.assertEqual(snapshot.ratification_ref, approval.ratification_ref)
        self.assertEqual(receipt.upstream_refs, snapshot.upstream_refs)

    def test_ac_05_fresh_context_identity_and_bytes_are_deterministic(self) -> None:
        first = build_context(seed="deterministic-ir")
        second = build_context(seed="deterministic-ir")
        first_receipt = first[0].compile(compile_command(first[4]))
        second_receipt = second[0].compile(compile_command(second[4]))
        first_ir = first[2].get_harness_ir(first_receipt.ir_id)
        second_ir = second[2].get_harness_ir(second_receipt.ir_id)
        self.assertEqual(first_ir.ir_id, second_ir.ir_id)
        self.assertEqual(first_ir.ir_hash, second_ir.ir_hash)
        self.assertEqual(first_ir.canonical_bytes(), second_ir.canonical_bytes())
        self.assertEqual(first_receipt.receipt_hash, second_receipt.receipt_hash)

    def test_ac_02_one_run_has_one_authoritative_initial_snapshot(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        self.assertEqual(repository.harness_ir_count, 1)
        self.assertEqual(repository.harness_irs(run_id), (repository.get_harness_ir(receipt.ir_id),))


if __name__ == "__main__":
    unittest.main()
