from __future__ import annotations

from dataclasses import replace
import unittest

from cmf_builder.domain.harness_ir import (
    ACTIVATIVE_LINEAGE_PATHS,
    GovernedValue,
    GovernedValueInvalid,
)
from tests.stories.st_03_03 import build_context, compile_command


class HarnessIRProvenanceLineageTests(unittest.TestCase):
    def _snapshot(self):
        service, _, repository, _, run_id, _ = build_context()
        receipt = service.compile(compile_command(run_id))
        return repository.get_harness_ir(receipt.ir_id)

    def test_ac_03_every_material_value_has_governed_metadata(self) -> None:
        snapshot = self._snapshot()
        for item in snapshot.material_values:
            self.assertTrue(item.path)
            self.assertTrue(item.knowledge_status)
            self.assertTrue(item.authority_status)
            self.assertTrue(item.evidence_refs)
            self.assertTrue(item.disposition)
            self.assertTrue(item.created_by)
            self.assertTrue(item.value_version)
            self.assertTrue(item.dependency_impact)

    def test_ac_04_rich_activative_lineage_keys_are_separate_not_applicable_values(self) -> None:
        snapshot = self._snapshot()
        self.assertTrue(
            set(ACTIVATIVE_LINEAGE_PATHS).issubset(
                {item.path for item in snapshot.section("activative_semantics")}
            )
        )
        for path in ACTIVATIVE_LINEAGE_PATHS:
            item = snapshot.value(path)
            self.assertIsNone(item.value)
            self.assertEqual(item.knowledge_status, "NOT_APPLICABLE")
            self.assertEqual(item.authority_status, "NOT_APPLICABLE")
            self.assertIn(snapshot.model_ref, item.evidence_refs)

    def test_ac_04_lineage_is_never_flattened_into_generic_notes(self) -> None:
        snapshot = self._snapshot()
        self.assertFalse(any(item.path == "notes" or item.path.endswith(".notes") for item in snapshot.material_values))
        self.assertNotIn("notes", snapshot.canonical_bytes().decode("utf-8"))

    def test_ac_03_upstream_model_authority_and_knowledge_status_are_preserved(self) -> None:
        snapshot = self._snapshot()
        self.assertEqual(snapshot.value("identity.atomic_boundary").authority_status, "HUMAN_RATIFIED")
        self.assertEqual(snapshot.value("identity.atomic_boundary").knowledge_status, "LOCKED_EVIDENCE")
        self.assertEqual(snapshot.value("phases.phase_hypotheses").authority_status, "UNRATIFIED")
        self.assertEqual(snapshot.value("phases.phase_hypotheses").knowledge_status, "HYPOTHESIS")

    def test_ac_03_missing_provenance_fails_closed(self) -> None:
        snapshot = self._snapshot()
        value = snapshot.value("identity.atomic_boundary")
        with self.assertRaises(GovernedValueInvalid):
            replace(value, evidence_refs=()).validate()
        with self.assertRaises(GovernedValueInvalid):
            GovernedValue(
                path="identity.bad",
                value="bad",
                knowledge_status="LOCKED_EVIDENCE",
                authority_status="SOURCE_LOCKED",
                evidence_refs=(),
                decision_ref=None,
                confidence=None,
                disposition="INVALID",
                created_by="code-1",
                value_version="1.0.0",
                dependency_impact=("identity.bad",),
            )


if __name__ == "__main__":
    unittest.main()
