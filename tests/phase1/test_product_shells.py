from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest

from _support import ROOT  # type: ignore

PRODUCTS = (
    ("cmf_activative_intelligence", "activative-intelligence-runtime"),
    ("cmf_pipeline", "atomic-harness-pipeline"),
    ("conscious_activations_interview_expression", "interview-expression"),
)


class ProductShellTests(unittest.TestCase):
    def _env(self, data_root: str) -> dict[str, str]:
        paths = [
            ROOT / "packages" / "ca_contracts" / "src",
            ROOT / "packages" / "ca_runtime" / "src",
            ROOT / "04_ACTIVATIVE_INTELLIGENCE_RUNTIME" / "src",
            ROOT / "05_ATOMIC_HARNESS_PIPELINE" / "src",
            ROOT / "06_INTERVIEW_EXPRESSION" / "src",
        ]
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join(str(path) for path in paths)
        env["CA_DATA_ROOT"] = data_root
        return env

    def test_status_shells(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env = self._env(temp_dir)
            for module, product_id in PRODUCTS:
                with self.subTest(module=module):
                    completed = subprocess.run(
                        [sys.executable, "-m", module, "status", "--json"],
                        cwd=ROOT,
                        env=env,
                        text=True,
                        capture_output=True,
                        check=True,
                    )
                    status = json.loads(completed.stdout)
                    self.assertEqual(status["product_id"], product_id)
                    self.assertTrue(status["development_authorized"])
                    self.assertFalse(status["production_authorized"])
                    self.assertFalse(status["certified"])

    def test_bootstrap_shells(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env = self._env(temp_dir)
            for module, _ in PRODUCTS:
                subprocess.run(
                    [sys.executable, "-m", module, "bootstrap", "--json"],
                    cwd=ROOT,
                    env=env,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                health = subprocess.run(
                    [sys.executable, "-m", module, "health", "--json"],
                    cwd=ROOT,
                    env=env,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                body = json.loads(health.stdout)
                self.assertEqual(body["integrity"], "ok")
                self.assertEqual(body["receipt_count"], 1)


if __name__ == "__main__":
    unittest.main()
