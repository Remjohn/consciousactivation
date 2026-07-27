from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from _support import ROOT  # type: ignore


class SchemaCliBoundaryTests(unittest.TestCase):
    def _env(self, data_root: str) -> dict[str, str]:
        paths = [
            ROOT / "tests" / "phase3",
            ROOT / "tests" / "phase2",
            ROOT / "tests" / "phase1",
            ROOT / "packages" / "ca_contracts" / "src",
            ROOT / "packages" / "ca_runtime" / "src",
            ROOT / "04_ACTIVATIVE_INTELLIGENCE_RUNTIME" / "src",
            ROOT / "05_ATOMIC_HARNESS_PIPELINE" / "src",
            ROOT / "06_INTERVIEW_EXPRESSION" / "src",
        ]
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join(str(item) for item in paths)
        env["CA_DATA_ROOT"] = data_root
        return env

    def test_product_schemas_are_closed_and_registered(self) -> None:
        root = ROOT / "05_ATOMIC_HARNESS_PIPELINE" / "contracts" / "schemas"
        registry = json.loads((root / "CONTRACT_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertEqual(len(registry["schemas"]), 16)
        for item in registry["schemas"]:
            schema = json.loads((root / item["path"]).read_text(encoding="utf-8"))
            with self.subTest(schema=item["name"]):
                self.assertEqual(schema.get("additionalProperties"), False)
                self.assertIn("$id", schema)

    def test_cli_status_demo_and_export(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env = self._env(temp_dir)
            status = subprocess.run([sys.executable, "-m", "cmf_pipeline", "status", "--json"], cwd=ROOT, env=env, text=True, capture_output=True, check=True)
            body = json.loads(status.stdout)
            self.assertEqual(body["claim_ceiling"], "AHP_PHASE_03_CORE_IMPLEMENTED_DEVELOPMENT_PASS")
            self.assertFalse(body["production_authorized"])
            demo = subprocess.run([sys.executable, "-m", "cmf_pipeline", "demo", "--json"], cwd=ROOT, env=env, text=True, capture_output=True, check=True)
            result = json.loads(demo.stdout)
            self.assertEqual(result["run_state"], "COMPLETED")
            self.assertEqual(result["real_external_calls"], 0)
            destination = Path(temp_dir) / "schemas"
            exported = subprocess.run([sys.executable, "-m", "cmf_pipeline", "export-schemas", str(destination), "--json"], cwd=ROOT, env=env, text=True, capture_output=True, check=True)
            export_result = json.loads(exported.stdout)
            self.assertEqual(export_result["file_count"], 17)

    def test_no_format02_or_vae_stage5_activation(self) -> None:
        source_root = ROOT / "05_ATOMIC_HARNESS_PIPELINE" / "src"
        text = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in source_root.rglob("*")
            if path.is_file() and path.suffix in {".py", ".json", ".sql"}
        ).lower()
        self.assertNotIn("format02_minimal_coach_theatre", text)
        self.assertNotIn("vae_stage5_started: true", text)


if __name__ == "__main__":
    unittest.main()
