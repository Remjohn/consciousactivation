from __future__ import annotations

from dataclasses import replace
import json
import unittest

from cmf_builder.domain.generated_artifacts import ARTIFACT_PATHS
from tests.stories.st_03_04 import BUILD_CONFIG, build_context, compile_command


class DeterminismAndCompatibilityTests(unittest.TestCase):
    def _compile(self, seed: str = "golden"):
        service, _, repository, _, run_id, _, _ = build_context(seed=seed)
        receipt = service.compile(compile_command(run_id))
        manifest = repository.get_artifact_manifest(receipt.manifest_id)
        assert manifest is not None
        return receipt, manifest

    def test_fresh_contexts_produce_byte_identical_outputs(self) -> None:
        first_receipt, first = self._compile()
        second_receipt, second = self._compile()
        self.assertEqual(first, second)
        self.assertEqual(first.canonical_bytes(), second.canonical_bytes())
        self.assertEqual(first_receipt, second_receipt)
        self.assertEqual(first_receipt.canonical_bytes(), second_receipt.canonical_bytes())

    def test_identical_artifacts_have_reproducible_identity(self) -> None:
        _, manifest = self._compile()
        self.assertEqual(manifest.artifact_set_id.removeprefix("artifact-set_"), manifest.manifest_hash.removeprefix("sha256:"))
        self.assertEqual(tuple(item.path for item in manifest.artifacts), ARTIFACT_PATHS)

    def test_changed_governed_input_changes_artifact_set_identity(self) -> None:
        _, first = self._compile("input-a")
        _, second = self._compile("input-b")
        self.assertNotEqual(first.ir_hash, second.ir_hash)
        self.assertNotEqual(first.artifact_set_id, second.artifact_set_id)

    def test_changed_build_config_changes_artifact_set_identity(self) -> None:
        service, _, repository, _, run_id, _, _ = build_context(seed="config-change")
        changed = replace(BUILD_CONFIG, generation_timestamp="2026-01-10T12:00:01Z")
        receipt = service.compile(compile_command(run_id, build_config=changed))
        manifest = repository.get_artifact_manifest(receipt.manifest_id)
        assert manifest is not None
        self.assertNotEqual(manifest.config_hash, BUILD_CONFIG.config_hash)

    def test_json_and_manifest_serialization_are_canonical(self) -> None:
        _, manifest = self._compile()
        for artifact in manifest.artifacts:
            if artifact.path.endswith(".json"):
                parsed = json.loads(artifact.content)
                expected = json.dumps(parsed, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
                self.assertEqual(artifact.content, expected)
        self.assertEqual(manifest.nondeterminism_exceptions, ())


if __name__ == "__main__":
    unittest.main()

