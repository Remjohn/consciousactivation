from __future__ import annotations

import json
import unittest
from pathlib import Path

from _support import ROOT  # type: ignore


class BoundaryTests(unittest.TestCase):
    def test_no_format02_or_vae_stage5_implementation(self) -> None:
        new_roots = [
            ROOT / "packages" / "ca_contracts",
            ROOT / "packages" / "ca_runtime",
            ROOT / "04_ACTIVATIVE_INTELLIGENCE_RUNTIME" / "src",
            ROOT / "05_ATOMIC_HARNESS_PIPELINE" / "src",
            ROOT / "06_INTERVIEW_EXPRESSION" / "src",
            ROOT / "07_CONSCIOUS_ACTIVATIONS_STUDIO" / "src",
        ]
        text = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for root in new_roots
            for path in root.rglob("*")
            if path.is_file() and path.suffix in {".py", ".ts", ".json", ".sql"}
        ).lower()
        self.assertNotIn("format02_minimal_coach_theatre", text)
        self.assertNotIn("vae_stage5_started: true", text)

    def test_contract_package_schema_bytes_match_release(self) -> None:
        release = (
            ROOT
            / "CMF_PROGRAM_CONTROL"
            / "02_CROSS_REPO_CONTRACTS"
            / "activative-production-spine"
            / "0.1.0-dev.1"
            / "schemas"
        )
        package = ROOT / "packages" / "ca_contracts" / "src" / "ca_contracts" / "schemas"
        for path in sorted(release.glob("*.schema.json")):
            with self.subTest(schema=path.name):
                self.assertEqual(path.read_bytes(), (package / path.name).read_bytes())

    def test_all_products_pin_same_contract_release(self) -> None:
        digest = "sha256:df3b12d3f49cae6cfca8614c4f4d71f0f1711cf91131f7438332ed43191f7a74"
        for root in (
            "04_ACTIVATIVE_INTELLIGENCE_RUNTIME",
            "05_ATOMIC_HARNESS_PIPELINE",
            "06_INTERVIEW_EXPRESSION",
            "07_CONSCIOUS_ACTIVATIONS_STUDIO",
        ):
            with self.subTest(root=root):
                text = (ROOT / root / "contracts" / "SHARED_CONTRACT_PIN.yaml").read_text(encoding="utf-8")
                self.assertIn("version: 0.1.0-dev.1", text)
                self.assertIn(f"release_digest: {digest}", text)


if __name__ == "__main__":
    unittest.main()
