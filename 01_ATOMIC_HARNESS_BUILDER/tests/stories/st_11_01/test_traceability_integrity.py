from __future__ import annotations

from hashlib import sha256
import unittest

from cmf_builder.domain.development_capsule import REQUIRED_CONTRACT_VERSIONS
from tests.stories.st_01_01_synthetic_proof import ROOT
from tests.stories.st_11_01 import build_context, capsule_command


class DevelopmentCapsuleTraceabilityTests(unittest.TestCase):
    def _compile(self, seed: str = "ST-11.01-trace"):
        service, _, _, _, _, run_id, _, validation, definition = build_context(seed=seed)
        receipt = service.generate(capsule_command(run_id))
        return service.get_active(run_id), receipt, validation, definition

    def test_every_file_reference_is_present_and_hash_valid(self) -> None:
        capsule, _, _, _ = self._compile()
        file_refs = [item for item in capsule.references if "/" in item.reference_id]
        self.assertGreaterEqual(len(file_refs), 19)
        for reference in file_refs:
            path = ROOT / reference.reference_id
            self.assertTrue(path.is_file(), reference.reference_id)
            self.assertEqual(
                f"sha256:{sha256(path.read_bytes()).hexdigest()}",
                reference.content_hash,
            )

    def test_definition_validation_and_complete_lineage_are_exact(self) -> None:
        capsule, _, validation, definition = self._compile()
        for value in (
            definition.definition_id,
            definition.definition_hash,
            validation.report_id,
            validation.report_hash,
            definition.constitutional_report_hash,
            definition.ratification_hash,
        ):
            self.assertIn(value, capsule.lineage)

    def test_contract_versions_and_compatibility_are_resolved(self) -> None:
        capsule, _, _, _ = self._compile()
        self.assertEqual(capsule.contract_versions, REQUIRED_CONTRACT_VERSIONS)
        self.assertEqual(capsule.internal_compatibility, "PASS")
        self.assertEqual(
            capsule.external_target_compatibility,
            "NOT_EVALUATED_EXTERNAL_TARGET_BRANCH",
        )

    def test_fresh_contexts_produce_byte_identical_capsules_and_receipts(self) -> None:
        first, first_receipt, _, _ = self._compile(seed="ST-11.01-fresh")
        second, second_receipt, _, _ = self._compile(seed="ST-11.01-fresh")
        self.assertEqual(first.canonical_bytes(), second.canonical_bytes())
        self.assertEqual(first.capsule_hash, second.capsule_hash)
        self.assertEqual(first_receipt.canonical_bytes(), second_receipt.canonical_bytes())

    def test_portable_artifact_contains_no_absolute_machine_path(self) -> None:
        capsule, _, _, _ = self._compile()
        text = capsule.canonical_bytes().decode("utf-8").lower()
        self.assertNotIn("d:/", text)
        self.assertNotIn("c:/", text)
        self.assertNotIn("d:\\", text)
        self.assertNotIn("c:\\", text)


if __name__ == "__main__":
    unittest.main()
