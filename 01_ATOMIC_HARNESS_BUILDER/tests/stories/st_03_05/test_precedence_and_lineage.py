from __future__ import annotations

from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from cmf_builder.adapters.file_constitutional_policy_repository import (
    FileConstitutionalPolicyRepository,
)
from cmf_builder.domain.constitutional_validation import (
    AUTHORITY_ORDER,
    BUILDER_PRD_AMENDMENT_PATH,
    BUILDER_PRD_AMENDMENT_SHA256,
    CONSTITUTION_PATH,
    CONSTITUTION_SHA256,
    POLICY_PATH,
    POLICY_SHA256,
    ConstitutionalPolicyInvalid,
)
from tests.stories.st_01_01_synthetic_proof import ROOT
from tests.stories.st_03_05 import build_context, validate_command


class PrecedenceAndLineageTests(unittest.TestCase):
    def test_policy_projection_is_exact_and_ordered(self) -> None:
        policy = FileConstitutionalPolicyRepository(ROOT).load(
            POLICY_PATH, POLICY_SHA256
        )
        self.assertEqual(policy.authority_order, AUTHORITY_ORDER)
        self.assertEqual(policy.conflict_action, "BLOCK_AND_EMIT_DECISION_REQUEST")
        self.assertEqual(policy.hard_gates, ("HG-001", "HG-004", "HG-005", "HG-015"))
        self.assertEqual(policy.harness_development_law, "Visual Syntax First")
        self.assertEqual(policy.runtime_law, "Activation First")
        self.assertEqual(policy.constitution_hash, CONSTITUTION_SHA256)
        self.assertEqual(policy.builder_prd_amendment_hash, BUILDER_PRD_AMENDMENT_SHA256)

    def test_local_policy_references_canonical_authorities_without_copying_them(self) -> None:
        policy = FileConstitutionalPolicyRepository(ROOT).load(
            POLICY_PATH, POLICY_SHA256
        )
        self.assertEqual(policy.constitution_path, CONSTITUTION_PATH)
        self.assertEqual(policy.builder_prd_amendment_path, BUILDER_PRD_AMENDMENT_PATH)
        self.assertNotEqual(policy.source_path, policy.constitution_path)
        self.assertNotEqual(policy.source_hash, policy.constitution_hash)

    def test_historical_report_binds_authority_versions(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        receipt = service.validate(validate_command(run_id))
        historical = service.get_historical(receipt.report_id)
        self.assertEqual(historical.policy_hash, POLICY_SHA256)
        self.assertEqual(historical.constitution_hash, CONSTITUTION_SHA256)
        self.assertEqual(
            historical.builder_prd_amendment_hash, BUILDER_PRD_AMENDMENT_SHA256
        )
        self.assertIs(repository.get_constitutional_validation_report(receipt.report_id), historical)

    def test_arbitrary_policy_path_is_rejected_before_loading(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        with self.assertRaises(ConstitutionalPolicyInvalid):
            service.validate(validate_command(run_id, policy_path="other/policy.yaml"))
        self.assertEqual(repository.constitutional_validation_report_count, 0)

    def test_unpinned_policy_hash_is_rejected(self) -> None:
        service, _, repository, _, run_id, _ = build_context()
        with self.assertRaises(ConstitutionalPolicyInvalid):
            service.validate(validate_command(run_id, policy_sha256="0" * 64))
        self.assertEqual(repository.event_count(run_id), 12)

    def test_policy_byte_drift_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._copy_authorities(root)
            policy_path = root / POLICY_PATH
            policy_path.write_bytes(policy_path.read_bytes() + b"\n# drift")
            with self.assertRaises(ConstitutionalPolicyInvalid):
                FileConstitutionalPolicyRepository(root).load(POLICY_PATH, POLICY_SHA256)

    def test_constitution_byte_drift_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._copy_authorities(root)
            constitution = root / CONSTITUTION_PATH
            constitution.write_bytes(constitution.read_bytes() + b"\n")
            with self.assertRaises(ConstitutionalPolicyInvalid):
                FileConstitutionalPolicyRepository(root).load(POLICY_PATH, POLICY_SHA256)

    def test_builder_prd_amendment_byte_drift_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self._copy_authorities(root)
            amendment = root / BUILDER_PRD_AMENDMENT_PATH
            amendment.write_bytes(amendment.read_bytes() + b"\n")
            with self.assertRaises(ConstitutionalPolicyInvalid):
                FileConstitutionalPolicyRepository(root).load(POLICY_PATH, POLICY_SHA256)

    @staticmethod
    def _copy_authorities(root: Path) -> None:
        for relative in (POLICY_PATH, CONSTITUTION_PATH, BUILDER_PRD_AMENDMENT_PATH):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)


if __name__ == "__main__":
    unittest.main()
