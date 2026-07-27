from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from _support import ROOT  # type: ignore
from cmf_pipeline import PipelineApplication
from cmf_pipeline.demo import write_demo_harness
from cmf_pipeline.domain.errors import PipelineValidationError
from cmf_pipeline.intake import PortableHarnessPackageReader


class IntakeBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.app = PipelineApplication(self.root / "pipeline.sqlite3")
        self.app.initialize()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_safe_archive_rejects_traversal(self) -> None:
        path = self.root / "unsafe.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("../escape.json", "{}")
        with self.assertRaises(PipelineValidationError):
            PortableHarnessPackageReader().read(path)

    def test_import_reconcile_and_exact_binding(self) -> None:
        package = self.root / "harness.zip"
        write_demo_harness(package)
        imported = self.app.import_harness_package(package, idempotency_key="import")
        self.assertEqual(imported["compiler_profile"]["package_profile"], "portable_activative_v1")
        self.assertEqual(imported["graph_receipt"]["topological_order"], ["node:inspect", "node:compose", "node:review"])
        self.assertFalse(imported["projection"]["production_ready"])
        self.assertFalse(imported["projection"]["certified"])

        self.app.load_default_development_candidates()
        result = self.app.compile_binding(imported["projection"], imported["graph_receipt"], idempotency_key="binding")
        manifest = result["object"]["payload"]
        self.assertTrue(manifest["execution_eligible"])
        self.assertEqual(len(manifest["bindings"]), 3)
        self.assertEqual(manifest["blockers"], [])

    def test_binding_denies_missing_and_ambiguous_candidates(self) -> None:
        package = self.root / "harness.zip"
        write_demo_harness(package)
        imported = self.app.import_harness_package(package, idempotency_key="import")
        missing = self.app.compile_binding(imported["projection"], imported["graph_receipt"], idempotency_key="missing")
        self.assertFalse(missing["object"]["payload"]["execution_eligible"])
        self.assertEqual(len(missing["object"]["payload"]["blockers"]), 3)

        app = PipelineApplication(self.root / "ambiguous.sqlite3")
        app.initialize()
        app.load_default_development_candidates()
        app.eligibility.register({
            "implementation_id": "cmf-pipeline.synthetic.inspect-alt",
            "implementation_version": "1.0.0",
            "owner_product": "ATOMIC_HARNESS_PIPELINE",
            "implementation_kind": "DETERMINISTIC_MODULE",
            "capability_ids": ["inspect_source"],
            "features": ["canonical_hash", "read_only"],
            "side_effect_class": "READ_ONLY",
            "authority_boundary": "alternate development implementation only",
            "development_eligible": True,
            "production_authorized": False,
            "evidence_refs": ["phase3:test"],
        })
        imported2 = app.import_harness_package(package, idempotency_key="import")
        ambiguous = app.compile_binding(imported2["projection"], imported2["graph_receipt"], idempotency_key="binding")
        blockers = ambiguous["object"]["payload"]["blockers"]
        self.assertIn("AMBIGUOUS_IMPLEMENTATION_BINDING", {item["code"] for item in blockers})

    def test_format02_is_rejected(self) -> None:
        package = self.root / "harness.zip"
        definition = write_demo_harness(package)
        definition["profile_id"] = "format02_minimal_coach_theatre"
        with self.assertRaises(PipelineValidationError):
            self.app.definition_intake.validate(definition, self.app.profile_registry.resolve("portable_activative_v1"))


if __name__ == "__main__":
    unittest.main()
