from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
import json
import unittest

from cmf_builder.domain.constitutional_validation import ConstitutionalConflict
from tests.stories.st_03_05 import build_context, validate_command


class CompletenessAndConflictTests(unittest.TestCase):
    def _context(self):
        service, _, repository, observations, run_id, receipt = build_context()
        manifest = repository.get_artifact_manifest(receipt.manifest_id)
        assert manifest is not None
        return service, repository, observations, run_id, manifest

    def test_missing_artifact_fails_closed_with_typed_finding(self) -> None:
        service, repository, observations, run_id, manifest = self._context()
        repository._artifact_manifest_artifacts[manifest.manifest_id] = manifest.artifacts[1:]
        with self.assertRaises(ConstitutionalConflict) as caught:
            service.validate(validate_command(run_id))
        self.assertIn("ARTIFACT_MISSING", {item.code for item in caught.exception.findings})
        self._assert_no_commit(repository, observations, run_id)

    def test_extra_artifact_fails_closed(self) -> None:
        service, repository, observations, run_id, manifest = self._context()
        repository._artifact_manifest_artifacts[manifest.manifest_id] = (
            *manifest.artifacts,
            replace(manifest.artifacts[0], path="machine/extra.json"),
        )
        with self.assertRaises(ConstitutionalConflict) as caught:
            service.validate(validate_command(run_id))
        self.assertIn(
            "ARTIFACT_INVENTORY_MISMATCH",
            {item.code for item in caught.exception.findings},
        )
        self._assert_no_commit(repository, observations, run_id)

    def test_drifted_markdown_fails_closed(self) -> None:
        service, repository, observations, run_id, manifest = self._context()
        artifacts = list(manifest.artifacts)
        altered = artifacts[0].content + b"\nlocal override\n"
        artifacts[0] = replace(
            artifacts[0],
            content=altered,
            content_hash=f"sha256:{sha256(altered).hexdigest()}",
        )
        repository._artifact_manifest_artifacts[manifest.manifest_id] = tuple(artifacts)
        with self.assertRaises(ConstitutionalConflict) as caught:
            service.validate(validate_command(run_id))
        self.assertIn(
            "PROJECTED_SEMANTIC_DRIFT",
            {item.code for item in caught.exception.findings},
        )
        self._assert_no_commit(repository, observations, run_id)

    def test_syntax_valid_authority_escalation_fails_closed(self) -> None:
        service, repository, observations, run_id, manifest = self._context()
        artifacts = list(manifest.artifacts)
        index = next(i for i, item in enumerate(artifacts) if item.path.endswith(".json"))
        payload = json.loads(artifacts[index].content)
        payload["authority_class"] = "LOCAL_OVERRIDES_CONSTITUTION"
        altered = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()
        artifacts[index] = replace(
            artifacts[index],
            authority_class="LOCAL_OVERRIDES_CONSTITUTION",
            content=altered,
            content_hash=f"sha256:{sha256(altered).hexdigest()}",
        )
        repository._artifact_manifest_artifacts[manifest.manifest_id] = tuple(artifacts)
        with self.assertRaises(ConstitutionalConflict) as caught:
            service.validate(validate_command(run_id))
        self.assertIn("LOWER_AUTHORITY_OVERRIDE", {item.code for item in caught.exception.findings})
        self._assert_no_commit(repository, observations, run_id)

    def test_syntax_valid_semantic_compression_fails_closed(self) -> None:
        service, repository, observations, run_id, manifest = self._context()
        artifacts = list(manifest.artifacts)
        index = next(
            i for i, item in enumerate(artifacts) if item.path == "machine/traceability-map.json"
        )
        payload = json.loads(artifacts[index].content)
        payload["source_nodes"] = [
            node
            for node in payload["source_nodes"]
            if not node["path"].startswith("activative_semantics.")
        ]
        altered = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()
        artifacts[index] = replace(
            artifacts[index],
            content=altered,
            content_hash=f"sha256:{sha256(altered).hexdigest()}",
        )
        repository._artifact_manifest_artifacts[manifest.manifest_id] = tuple(artifacts)
        with self.assertRaises(ConstitutionalConflict):
            service.validate(validate_command(run_id))
        self._assert_no_commit(repository, observations, run_id)

    def test_invented_downstream_execution_flag_fails_closed(self) -> None:
        service, repository, observations, run_id, manifest = self._context()
        artifacts = list(manifest.artifacts)
        index = next(i for i, item in enumerate(artifacts) if item.path.endswith(".json"))
        payload = json.loads(artifacts[index].content)
        payload["executable"] = True
        payload["delegated_runtime"] = "invented"
        altered = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()
        artifacts[index] = replace(
            artifacts[index],
            content=altered,
            content_hash=f"sha256:{sha256(altered).hexdigest()}",
        )
        repository._artifact_manifest_artifacts[manifest.manifest_id] = tuple(artifacts)
        with self.assertRaises(ConstitutionalConflict):
            service.validate(validate_command(run_id))
        self._assert_no_commit(repository, observations, run_id)

    def test_unresolved_source_node_fails_closed(self) -> None:
        service, repository, observations, run_id, manifest = self._context()
        artifacts = list(manifest.artifacts)
        artifacts[0] = replace(
            artifacts[0],
            source_node_paths=(*artifacts[0].source_node_paths, "references.missing"),
        )
        repository._artifact_manifest_artifacts[manifest.manifest_id] = tuple(artifacts)
        with self.assertRaises(ConstitutionalConflict) as caught:
            service.validate(validate_command(run_id))
        self.assertIn(
            "UNRESOLVED_HARNESS_IR_REFERENCE",
            {item.code for item in caught.exception.findings},
        )
        self._assert_no_commit(repository, observations, run_id)

    def _assert_no_commit(self, repository, observations, run_id: str) -> None:
        self.assertEqual(repository.constitutional_validation_report_count, 0)
        self.assertEqual(repository.constitutional_validation_receipt_count, 0)
        self.assertEqual(repository.event_count(run_id), 12)
        self.assertIsNone(repository.get_command_record("constitutional-validation-1"))
        names = {item.event_name for item in observations.observations}
        self.assertIn("ST-03.05:OutcomeRejected", names)


if __name__ == "__main__":
    unittest.main()
