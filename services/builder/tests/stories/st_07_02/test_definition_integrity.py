from __future__ import annotations

from dataclasses import replace
import json
import unittest

from cmf_builder.domain.atomic_harness_definition import (
    DefinitionLineageInvalid,
    REQUIRED_SECTIONS,
)
from tests.stories.st_07_02 import build_context, compile_command


class AtomicHarnessDefinitionIntegrityTests(unittest.TestCase):
    def _complete(self, *, seed: str = "ST-07.02-integrity"):
        service, _, repository, _, run_id, _, _, _ = build_context(seed=seed)
        receipt = service.compile(compile_command(run_id))
        return service, repository, run_id, receipt, service.get_active(run_id)

    def test_definition_identity_matches_canonical_bytes(self) -> None:
        _, _, _, _, definition = self._complete()
        self.assertEqual(definition.definition_hash.removeprefix("sha256:"), definition.definition_id.rsplit("_", 1)[1])
        decoded = json.loads(definition.canonical_bytes())
        self.assertEqual(decoded["harness_id"], "synthetic_text_normalization_v1")
        self.assertEqual([item["section_id"] for item in decoded["sections"]], list(REQUIRED_SECTIONS))

    def test_fresh_context_definition_and_receipt_are_byte_identical(self) -> None:
        first = self._complete(seed="identical-definition")
        second = self._complete(seed="identical-definition")
        self.assertEqual(first[4].canonical_bytes(), second[4].canonical_bytes())
        self.assertEqual(first[3].canonical_bytes(), second[3].canonical_bytes())
        self.assertEqual(first[4].definition_hash, second[4].definition_hash)
        self.assertEqual(first[3].receipt_hash, second[3].receipt_hash)

    def test_definition_contains_no_absolute_machine_paths(self) -> None:
        _, _, _, _, definition = self._complete()
        text = definition.canonical_bytes().decode("utf-8")
        self.assertNotIn("D:\\\\", text)
        self.assertNotIn("C:\\\\", text)
        self.assertNotIn(str(__file__), text)

    def test_altered_definition_cannot_validate_as_historical(self) -> None:
        service, repository, _, _, definition = self._complete()
        altered = replace(definition, output_contract="altered")
        repository._atomic_harness_definitions[definition.definition_id] = altered
        with self.assertRaises(DefinitionLineageInvalid):
            service.get_historical(definition.definition_id)


if __name__ == "__main__":
    unittest.main()
