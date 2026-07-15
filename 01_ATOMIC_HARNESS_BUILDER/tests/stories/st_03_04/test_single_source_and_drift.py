from __future__ import annotations

import unittest

from cmf_builder.application.artifact_commands import ValidateArtifactBytesCommand
from tests.stories.st_03_04 import build_context, compile_command


class SingleSourceAndDriftTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service, _, self.repository, self.observations, self.run_id, _, self.ir_receipt = build_context()
        self.receipt = self.service.compile(compile_command(self.run_id))
        self.manifest = self.repository.get_artifact_manifest(self.receipt.manifest_id)
        assert self.manifest is not None

    def _validate(self, observed: dict[str, bytes]):
        return self.service.validate_artifacts(
            ValidateArtifactBytesCommand(
                command_id="artifact-drift-check-1",
                run_id=self.run_id,
                actor_id="code-1",
                correlation_id="drift-correlation",
                causation_id=self.receipt.receipt_id,
                manifest_id=self.manifest.manifest_id,
                observed_artifacts=observed,
            )
        )

    def test_every_projection_read_is_declared_against_ir(self) -> None:
        ir = self.repository.get_harness_ir(self.ir_receipt.ir_id)
        assert ir is not None
        available = {item.path for item in ir.material_values}
        for artifact in self.manifest.artifacts:
            self.assertTrue(set(artifact.source_node_paths) <= available)

    def test_exact_bytes_validate_without_quarantine(self) -> None:
        report = self._validate({item.path: item.content for item in self.manifest.artifacts})
        self.assertEqual(report.outcome, "PASS")
        self.assertFalse(report.quarantined)
        self.assertEqual(report.mismatches, ())

    def test_manual_mutation_is_quarantined_without_ir_mutation(self) -> None:
        ir = self.repository.get_harness_ir(self.ir_receipt.ir_id)
        assert ir is not None
        before = ir.canonical_bytes()
        observed = {item.path: item.content for item in self.manifest.artifacts}
        observed[self.manifest.artifacts[0].path] += b"manual drift"
        report = self._validate(observed)
        self.assertEqual(report.outcome, "DRIFT")
        self.assertTrue(report.quarantined)
        self.assertEqual(len(report.mismatches), 1)
        self.assertEqual(self.repository.get_harness_ir(ir.ir_id).canonical_bytes(), before)

    def test_missing_and_extra_artifacts_are_typed_drift(self) -> None:
        observed = {item.path: item.content for item in self.manifest.artifacts[1:]}
        observed["machine/undeclared.json"] = b"{}"
        report = self._validate(observed)
        self.assertEqual({item.reason for item in report.mismatches}, {"MISSING", "UNDECLARED_EXTRA"})

    def test_drift_observation_contains_quarantine_disposition(self) -> None:
        observed = {item.path: item.content for item in self.manifest.artifacts}
        observed[self.manifest.artifacts[-1].path] = b"altered"
        self._validate(observed)
        event = self.observations.observations[-1]
        self.assertEqual(event.event_name, "ST-03.04:ArtifactDriftDetected")
        self.assertEqual(event.quarantine_disposition, "QUARANTINED_NO_IR_MUTATION")


if __name__ == "__main__":
    unittest.main()

