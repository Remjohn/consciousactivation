from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import unittest

from tests.stories.st_01_01 import ROOT, build_service
from tests.source_boundary_registry import registered_source_files


class ArchitectureAndContractBoundaryTests(unittest.TestCase):
    PROHIBITED_IMPORT_ROOTS = {
        "requests",
        "sqlalchemy",
        "fastapi",
        "temporalio",
        "boto3",
        "delegation",
        "visual_asset_editor",
    }

    def test_domain_does_not_import_application_or_adapters(self) -> None:
        for path in (ROOT / "src/cmf_builder/domain").glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            modules = self._imports(tree)
            self.assertFalse(
                any(
                    module.startswith("cmf_builder.application")
                    or module.startswith("cmf_builder.adapters")
                    for module in modules
                ),
                f"domain boundary violation in {path}",
            )

    def test_source_files_import_no_external_product_or_runtime_dependency(self) -> None:
        actual = set()
        for path in (ROOT / "src/cmf_builder").rglob("*.py"):
            relative = path.relative_to(ROOT).as_posix()
            actual.add(relative)
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            roots = {module.split(".", 1)[0] for module in self._imports(tree)}
            self.assertFalse(roots & self.PROHIBITED_IMPORT_ROOTS, relative)
        self.assertEqual(actual, registered_source_files(ROOT))

    def test_governed_contract_inputs_are_hash_valid_and_read_only(self) -> None:
        expected = {
            "governance/COMPILATION_TARGET_REGISTRY.yaml": "0e9c82b6f87a9b7f5dff317578c0da18241fbfd66e29cc2226e161399d4da2ca",
            "contracts/integration/CATEGORY_PROFILE_COMPATIBILITY.yaml": "781a438ef1298c1bc71da6ab54298774f09c0be97becf513510913f98fc97a71",
            "docs/contracts/CONTRACT_REGISTRY.yaml": "cb9240ef0818a6180de75fe79c02901e3f41a2ec2ed97688fb754a567ad79fce",
            "docs/contracts/schemas/constitutional-evaluation.schema.json": "886c119ab0e8be6b1f469886f7baf2cebcc08ac95148a56ff084933ffb4afc9f",
        }
        for relative, digest in expected.items():
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), digest)

        schema = json.loads(
            (ROOT / "docs/contracts/schemas/constitutional-evaluation.schema.json").read_text(
                encoding="utf-8-sig"
            )
        )
        self.assertIn("ConstitutionalReadinessReceipt", schema["$defs"])
        registry = (ROOT / "docs/contracts/CONTRACT_REGISTRY.yaml").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("contract_id: ConstitutionalReadinessReceipt", registry)
        _, _, _, _, profiles = build_service()
        self.assertEqual(profiles.load_authorized_profile().compatibility_state, "contract_compatible")

    @staticmethod
    def _imports(tree: ast.AST) -> set[str]:
        modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
        return modules


if __name__ == "__main__":
    unittest.main()
