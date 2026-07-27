from __future__ import annotations

import ast
from hashlib import sha256
import json
import unittest

from cmf_builder.domain.development_capsule import (
    CAPSULE_INPUT_PATH,
    CAPSULE_INPUT_SHA256,
)
from tests.stories.st_01_01_synthetic_proof import ROOT


class DevelopmentCapsuleArchitectureBoundaryTests(unittest.TestCase):
    PROHIBITED_IMPORT_ROOTS = {
        "boto3", "delegation", "fastapi", "requests", "sqlalchemy",
        "temporalio", "visual_asset_editor",
    }

    def test_source_tree_remains_layered_and_standard_library_only(self) -> None:
        for path in (ROOT / "src/cmf_builder").rglob("*.py"):
            relative = path.relative_to(ROOT).as_posix()
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imports = self._imports(tree)
            roots = {item.split(".", 1)[0] for item in imports}
            self.assertFalse(roots & self.PROHIBITED_IMPORT_ROOTS, relative)
            if "/domain/" in relative:
                self.assertFalse(any(item.startswith(("cmf_builder.application", "cmf_builder.adapters")) for item in imports), relative)
            if "/application/" in relative:
                self.assertFalse(any(item.startswith("cmf_builder.adapters") for item in imports), relative)

    def test_capsule_input_is_exact_hash_pinned_and_complete(self) -> None:
        path = ROOT / CAPSULE_INPUT_PATH
        self.assertEqual(sha256(path.read_bytes()).hexdigest(), CAPSULE_INPUT_SHA256)
        value = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(value["active_mode"], "SYNTHETIC_BUILDER_PROOF")
        self.assertEqual(len(value["required_sections"]), 15)
        self.assertEqual(len(value["owned_obligations"]), 6)
        self.assertEqual(len(value["dependency_receipts"]), 4)
        self.assertTrue(all(item.get("sha256") for key in ("authority_references", "requirement_references", "technical_spec_references", "accepted_adr_references", "dependency_receipts", "examples_and_fixtures") for item in value[key]))

    def test_no_external_product_runtime_or_downstream_implementation_exists(self) -> None:
        paths = {path.relative_to(ROOT).as_posix().lower() for path in (ROOT / "src/cmf_builder").rglob("*.py")}
        joined = "\n".join(sorted(paths))
        for prohibited in (
            "format02", "visual_asset_editor", "delegation_runtime", "control_tower",
            "workflow_executor", "comfyui", "synthetic_text_normalization/normalizer.py",
        ):
            self.assertNotIn(prohibited, joined)
        self.assertFalse(any((ROOT / name).exists() for name in ("requirements.txt", "poetry.lock", "package-lock.json")))

    def test_generated_capsule_modules_are_the_only_new_story_sources(self) -> None:
        expected = {
            "src/cmf_builder/domain/development_capsule.py",
            "src/cmf_builder/application/development_capsule_commands.py",
        }
        observed = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "src/cmf_builder").rglob("*development_capsule*.py")
        }
        self.assertEqual(observed, expected)

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
