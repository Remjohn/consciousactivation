from __future__ import annotations

import json
import unittest

from cmf_builder.domain.generated_artifacts import (
    ARTIFACT_AUTHORITY_CLASS,
    ARTIFACT_PATHS,
    HUMAN_ARTIFACT_PATHS,
    MACHINE_ARTIFACT_PATHS,
    OPENSPEC_ARTIFACT_PATHS,
)
from cmf_builder.domain.run import LifecycleState
from tests.stories.st_03_04 import build_context, compile_command


class ArtifactSetAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service, _, self.repository, self.observations, self.run_id, _, self.ir_receipt = build_context()
        self.receipt = self.service.compile(compile_command(self.run_id))
        self.manifest = self.repository.get_artifact_manifest(self.receipt.manifest_id)
        assert self.manifest is not None

    def test_compiles_exact_bounded_inventory_atomically(self) -> None:
        self.assertEqual(tuple(item.path for item in self.manifest.artifacts), ARTIFACT_PATHS)
        self.assertEqual(len(HUMAN_ARTIFACT_PATHS), 8)
        self.assertEqual(len(OPENSPEC_ARTIFACT_PATHS), 3)
        self.assertEqual(len(MACHINE_ARTIFACT_PATHS), 10)
        self.assertEqual(self.repository.generated_artifact_count, 21)
        self.assertEqual(self.repository.artifact_manifest_count, 1)
        self.assertEqual(self.repository.artifact_receipt_count, 1)

    def test_generated_views_are_readable_canonical_and_non_executable(self) -> None:
        for artifact in self.manifest.artifacts:
            if artifact.path.endswith(".md"):
                text = artifact.content.decode("utf-8")
                self.assertTrue(text.startswith("# "))
                self.assertIn("NON_EXECUTABLE", text)
            else:
                payload = json.loads(artifact.content)
                self.assertFalse(payload["executable"])
                self.assertTrue(payload["projection_only"])
                self.assertEqual(payload["authority_class"], ARTIFACT_AUTHORITY_CLASS)

    def test_manifest_preserves_exact_ir_and_lineage(self) -> None:
        ir = self.repository.get_harness_ir(self.ir_receipt.ir_id)
        assert ir is not None
        self.assertEqual(self.manifest.ir_id, ir.ir_id)
        self.assertEqual(self.manifest.ir_hash, ir.ir_hash)
        self.assertEqual(self.manifest.upstream_refs, ir.upstream_refs)
        self.assertEqual(self.manifest.source_lock_ref, ir.source_lock_ref)
        self.assertTrue(all(item.source_node_paths for item in self.manifest.artifacts))

    def test_run_remains_genesis_and_replays_manifest_reference(self) -> None:
        run = self.repository.load_run(self.run_id)
        self.assertIs(run.lifecycle_state, LifecycleState.GENESIS)
        self.assertEqual(run.stream_version, 12)
        self.assertEqual(run.artifact_set_ref, self.manifest.artifact_set_id)
        self.assertEqual(run.artifact_manifest_ref, self.manifest.manifest_id)
        self.assertEqual(run.artifact_manifest_hash, self.manifest.manifest_hash)

    def test_required_observations_are_receipt_linked(self) -> None:
        names = {item.event_name for item in self.observations.observations}
        for name in (
            "ST-03.04:ArtifactSetCompiled",
            "ST-03.04:ArtifactManifestCommitted",
            "ST-03.04:CrossArtifactConsistencyValidated",
            "ST-03.04:OutcomeVerified",
        ):
            self.assertIn(name, names)
        observations = [item for item in self.observations.observations if item.story_id == "ST-03.04"]
        self.assertTrue(all(item.artifact_set_id == self.manifest.artifact_set_id for item in observations))
        self.assertTrue(all(item.decision_receipt_hash == self.receipt.receipt_hash for item in observations))


if __name__ == "__main__":
    unittest.main()

