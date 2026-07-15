from __future__ import annotations

import ast
from hashlib import sha256
import json
import unittest

from cmf_builder.domain.atomic_harness_definition import (
    DEFINITION_INPUT_PATH,
    DEFINITION_INPUT_SHA256,
)
from tests.stories.st_01_01_synthetic_proof import ROOT


class AtomicHarnessDefinitionArchitectureBoundaryTests(unittest.TestCase):
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

    def test_governed_input_is_exact_hash_pinned_and_semantically_bounded(self) -> None:
        path = ROOT / DEFINITION_INPUT_PATH
        self.assertEqual(sha256(path.read_bytes()).hexdigest(), DEFINITION_INPUT_SHA256)
        value = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(value["target"]["profile_id"], "synthetic_text_normalization_v1")
        self.assertEqual(value["target"]["category_binding"], "none")
        self.assertFalse(value["target"]["production_eligible"])
        self.assertFalse(value["target"]["certified"])
        self.assertTrue(value["target"]["synthetic_not_certifiable"])
        self.assertFalse(value["execution_performed"])
        self.assertFalse(value["development_capsule_generated"])

    def test_no_external_product_runtime_or_later_story_module_exists(self) -> None:
        paths = {path.relative_to(ROOT).as_posix().lower() for path in (ROOT / "src/cmf_builder").rglob("*.py")}
        joined = "\n".join(sorted(paths))
        for prohibited in (
            "format02", "visual_asset_editor", "delegation_runtime", "control_tower",
            "development_capsule_compiler", "workflow_executor", "comfyui",
        ):
            self.assertNotIn(prohibited, joined)
        self.assertFalse(any((ROOT / name).exists() for name in ("requirements.txt", "poetry.lock", "package-lock.json")))

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
