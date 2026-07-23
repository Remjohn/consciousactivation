from __future__ import annotations

import json
import subprocess
import unittest

from _support import ROOT  # type: ignore


class StudioTests(unittest.TestCase):
    def test_generated_contracts_match_release(self) -> None:
        release = (
            ROOT
            / "CMF_PROGRAM_CONTROL"
            / "02_CROSS_REPO_CONTRACTS"
            / "activative-production-spine"
            / "0.1.0-dev.1"
            / "generated"
            / "typescript"
            / "contracts.ts"
        )
        studio = ROOT / "07_CONSCIOUS_ACTIVATIONS_STUDIO" / "src" / "generated" / "contracts.ts"
        self.assertEqual(release.read_bytes(), studio.read_bytes())

    def test_studio_health(self) -> None:
        studio = ROOT / "07_CONSCIOUS_ACTIVATIONS_STUDIO"
        completed = subprocess.run(
            ["node", "dist/index.js", "health", "--json"],
            cwd=studio,
            text=True,
            capture_output=True,
            check=True,
        )
        output = completed.stdout.strip() or completed.stderr.strip()
        status = json.loads(output)
        self.assertEqual(status["product_id"], "conscious-activations-studio")
        self.assertTrue(status["development_authorized"])
        self.assertFalse(status["production_authorized"])
        self.assertFalse(status["certified"])


if __name__ == "__main__":
    unittest.main()
