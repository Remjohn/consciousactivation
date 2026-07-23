from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from _support import ROOT  # type: ignore  # noqa: F401

from ca_contracts import (
    CanonicalizationError,
    ContractValidationError,
    SchemaRegistry,
    canonical_json_bytes,
    canonical_sha256,
)


class ContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = SchemaRegistry(
            ROOT / "packages" / "ca_contracts" / "src" / "ca_contracts" / "schemas"
        )

    def test_all_positive_fixtures(self) -> None:
        fixture_root = ROOT / "packages" / "ca_contracts" / "tests" / "fixtures" / "positive"
        for path in sorted(fixture_root.glob("*.json")):
            with self.subTest(path=path.name):
                self.registry.validate(path.stem, json.loads(path.read_text(encoding="utf-8")))

    def test_all_negative_fixtures(self) -> None:
        fixture_root = ROOT / "packages" / "ca_contracts" / "tests" / "fixtures" / "negative"
        for path in sorted(fixture_root.glob("*.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(path=path.name):
                with self.assertRaises(ContractValidationError):
                    self.registry.validate(record["schema"], record["payload"])

    def test_canonical_json_is_order_independent(self) -> None:
        left = {"b": [3, 2, 1], "a": {"z": True, "x": None}}
        right = {"a": {"x": None, "z": True}, "b": [3, 2, 1]}
        self.assertEqual(canonical_json_bytes(left), canonical_json_bytes(right))
        self.assertEqual(canonical_sha256(left), canonical_sha256(right))

    def test_canonical_json_rejects_float(self) -> None:
        with self.assertRaises(CanonicalizationError):
            canonical_json_bytes({"score": 0.5})

    def test_generated_bindings_are_reproducible(self) -> None:
        package = ROOT / "packages" / "ca_contracts"
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            subprocess.run(
                [
                    sys.executable,
                    str(package / "scripts" / "generate_types.py"),
                    "--schemas",
                    str(package / "src" / "ca_contracts" / "schemas"),
                    "--python-out",
                    str(temp / "generated.py"),
                    "--typescript-out",
                    str(temp / "contracts.ts"),
                ],
                check=True,
            )
            self.assertEqual(
                (temp / "generated.py").read_bytes(),
                (package / "src" / "ca_contracts" / "generated.py").read_bytes(),
            )
            release = (
                ROOT
                / "CMF_PROGRAM_CONTROL"
                / "02_CROSS_REPO_CONTRACTS"
                / "activative-production-spine"
                / "0.1.0-dev.1"
            )
            self.assertEqual(
                (temp / "contracts.ts").read_bytes(),
                (release / "generated" / "typescript" / "contracts.ts").read_bytes(),
            )


if __name__ == "__main__":
    unittest.main()
