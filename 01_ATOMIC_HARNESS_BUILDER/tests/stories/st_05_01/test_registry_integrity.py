from __future__ import annotations

from hashlib import sha256
import json
import unittest

from cmf_builder.domain.skill_registry import (
    REGISTRY_FIXTURE_PATH,
    REGISTRY_FIXTURE_SHA256,
    REGISTRY_POLICY_PATH,
    REGISTRY_POLICY_SHA256,
    REGISTRY_SCHEMA_PATH,
    REGISTRY_SCHEMA_SHA256,
    REGISTRY_VALIDATION_RECEIPT_PATH,
    REGISTRY_VALIDATION_RECEIPT_SHA256,
    SKILL_REGISTRY_INPUT_PATH,
    SKILL_REGISTRY_INPUT_SHA256,
)
from tests.stories.st_01_01_synthetic_proof import ROOT
from tests.stories.st_05_01 import build_context, compile_command


class SyntheticRegistryIntegrityTests(unittest.TestCase):
    def test_ac_04_all_five_governed_files_match_exact_pins(self) -> None:
        pins = {
            SKILL_REGISTRY_INPUT_PATH: SKILL_REGISTRY_INPUT_SHA256,
            REGISTRY_FIXTURE_PATH: REGISTRY_FIXTURE_SHA256,
            REGISTRY_POLICY_PATH: REGISTRY_POLICY_SHA256,
            REGISTRY_SCHEMA_PATH: REGISTRY_SCHEMA_SHA256,
            REGISTRY_VALIDATION_RECEIPT_PATH: REGISTRY_VALIDATION_RECEIPT_SHA256,
        }
        for path, expected in pins.items():
            self.assertEqual(sha256((ROOT / path).read_bytes()).hexdigest(), expected)

    def test_validation_receipt_binds_exact_policy_fixture_and_schema(self) -> None:
        value = json.loads((ROOT / REGISTRY_VALIDATION_RECEIPT_PATH).read_text(encoding="utf-8"))
        self.assertEqual(value["verdict"], "PASS")
        self.assertEqual(value["artifacts"]["fixture"]["sha256"], REGISTRY_FIXTURE_SHA256)
        self.assertEqual(value["artifacts"]["policy"]["sha256"], REGISTRY_POLICY_SHA256)
        self.assertEqual(value["artifacts"]["schema"]["sha256"], REGISTRY_SCHEMA_SHA256)

    def test_snapshot_preserves_exact_registry_policy_schema_and_receipt_hashes(self) -> None:
        service, _, _, _, run_id, _, _ = build_context()
        service.compile(compile_command(run_id))
        snapshot = service.get_active(run_id)
        self.assertEqual(snapshot.registry_hash, f"sha256:{REGISTRY_FIXTURE_SHA256}")
        self.assertEqual(snapshot.policy_hash, f"sha256:{REGISTRY_POLICY_SHA256}")
        self.assertEqual(snapshot.schema_hash, f"sha256:{REGISTRY_SCHEMA_SHA256}")
        self.assertEqual(
            snapshot.validation_receipt_hash,
            f"sha256:{REGISTRY_VALIDATION_RECEIPT_SHA256}",
        )
        self.assertEqual(snapshot.input_hash, f"sha256:{SKILL_REGISTRY_INPUT_SHA256}")

    def test_capability_evidence_is_explicit_and_bound_to_context(self) -> None:
        service, _, repository, _, run_id, _, _ = build_context()
        service.compile(compile_command(run_id))
        snapshot = service.get_active(run_id)
        context = repository.get_minimum_context_graph(snapshot.minimum_context_graph_id)
        assert context is not None
        expected_manifests = {item.manifest_id for item in context.manifests}
        for declaration in snapshot.capability_classifications:
            self.assertEqual(set(declaration.context_manifest_refs), expected_manifests)
            self.assertIn(context.capability_graph_id, declaration.evidence_refs)
            self.assertIn(context.module_graph_id, declaration.evidence_refs)
            self.assertIn(context.phase_graph_id, declaration.evidence_refs)


if __name__ == "__main__":
    unittest.main()
