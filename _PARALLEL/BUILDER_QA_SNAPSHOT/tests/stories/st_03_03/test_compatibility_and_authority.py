from __future__ import annotations

import unittest

from cmf_builder.application.harness_ir_migrations import (
    HarnessIRVersionRegistry,
    MissingHarnessIRMigration,
)
from cmf_builder.domain.harness_ir import (
    AggregateBoundaryViolation,
    HARNESS_IR_SCHEMA_VERSION,
    HarnessIR,
    HarnessIRAuthorityRejected,
    HarnessIRSchemaUnsupported,
)
from tests.stories.st_03_03 import build_context, compile_command


class HarnessIRCompatibilityAuthorityTests(unittest.TestCase):
    def test_ac_06_initial_compatibility_and_empty_deprecation_are_explicit(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        policy = repository.get_harness_ir(receipt.ir_id).compatibility
        self.assertEqual(policy.write_version, HARNESS_IR_SCHEMA_VERSION)
        self.assertEqual(policy.readable_versions, (HARNESS_IR_SCHEMA_VERSION,))
        self.assertEqual(policy.migrations, ())
        self.assertEqual(policy.deprecations, ())

    def test_ac_06_unknown_schema_version_is_blocked(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        with self.assertRaises(HarnessIRSchemaUnsupported):
            service.compile(compile_command(run_id, schema_version="2.0.0"))
        self.assertEqual(repository.harness_ir_count, 0)

    def test_ac_06_missing_migration_is_explicit_and_non_mutating(self) -> None:
        registry = HarnessIRVersionRegistry.initial()
        with self.assertRaises(MissingHarnessIRMigration):
            registry.require_migration("0.9.0", "1.0.0")
        self.assertEqual(registry.migrations, ())

    def test_ac_07_workflow_ir_ownership_fields_are_rejected(self) -> None:
        for field in ("worker", "queue", "retry", "sandbox", "deployment"):
            with self.subTest(field=field), self.assertRaises(AggregateBoundaryViolation):
                HarnessIR.validate_candidate_paths((f"identity.{field}",))

    def test_ac_08_only_deterministic_code_actor_may_compile(self) -> None:
        for actor in ("architect-1", "agent-1", "external-1", "evaluator-1", "unknown"):
            service, _, repository, _, run_id, _ = build_context(seed=f"authority-{actor}")
            with self.subTest(actor=actor), self.assertRaises(Exception):
                service.compile(compile_command(run_id, actor_id=actor))
            self.assertEqual(repository.harness_ir_count, 0)
        service, _, repository, _, run_id, _ = build_context(seed="authority-code")
        self.assertIsNotNone(service.compile(compile_command(run_id, actor_id="code-1")))
        self.assertEqual(repository.harness_ir_count, 1)


if __name__ == "__main__":
    unittest.main()
