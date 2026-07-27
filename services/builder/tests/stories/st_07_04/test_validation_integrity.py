from __future__ import annotations

from dataclasses import replace
import json
import unittest

from cmf_builder.domain.target_package_validation import (
    EXTERNAL_TARGET_COMPATIBILITY,
    TargetValidationLineageInvalid,
)
from tests.stories.st_07_04 import build_context, validation_command


class AtomicContentHarnessValidationIntegrityTests(unittest.TestCase):
    def _complete(self, *, seed: str = "ST-07.04-integrity"):
        service, _, _, repository, _, run_id, _, definition = build_context(seed=seed)
        receipt = service.validate(validation_command(run_id))
        return service, repository, run_id, receipt, service.get_active(run_id), definition

    def test_report_identity_and_canonical_order_are_reproducible(self) -> None:
        _, _, _, _, report, _ = self._complete()
        decoded = json.loads(report.canonical_bytes())
        self.assertEqual(
            report.report_hash.removeprefix("sha256:"),
            report.report_id.rsplit("_", 1)[1],
        )
        self.assertEqual(
            [item["dimension_id"] for item in decoded["dimensions"]],
            sorted(item["dimension_id"] for item in decoded["dimensions"]),
        )
        self.assertEqual(decoded["external_target_compatibility"], EXTERNAL_TARGET_COMPATIBILITY)

    def test_fresh_context_report_and_receipt_are_byte_identical(self) -> None:
        first = self._complete(seed="identical-validation")
        second = self._complete(seed="identical-validation")
        self.assertEqual(first[4].canonical_bytes(), second[4].canonical_bytes())
        self.assertEqual(first[3].canonical_bytes(), second[3].canonical_bytes())

    def test_changed_governed_input_produces_a_new_identity(self) -> None:
        first = self._complete(seed="validation-a")
        second = self._complete(seed="validation-b")
        self.assertNotEqual(first[4].report_id, second[4].report_id)

    def test_portable_report_contains_no_absolute_local_path(self) -> None:
        _, _, _, _, report, _ = self._complete()
        text = report.canonical_bytes().decode("utf-8")
        self.assertNotIn("D:\\\\", text)
        self.assertNotIn("C:\\\\", text)
        self.assertNotIn(str(__file__), text)

    def test_altered_definition_or_report_fails_historical_validation(self) -> None:
        service, repository, _, _, report, definition = self._complete()
        repository._atomic_harness_definitions[definition.definition_id] = replace(
            definition, external_runtime_count=1
        )
        with self.assertRaises(TargetValidationLineageInvalid):
            service.get_historical(report.report_id)
        repository._atomic_harness_definitions[definition.definition_id] = definition
        with self.assertRaises(TargetValidationLineageInvalid):
            replace(report, external_target_compatibility="PASS").validate(definition)


if __name__ == "__main__":
    unittest.main()
