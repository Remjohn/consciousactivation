from __future__ import annotations

import ast
from hashlib import sha256
import json
import unittest

from cmf_builder.domain.target_package_validation import (
    EXTERNAL_TARGET_COMPATIBILITY,
    VALIDATION_POLICY_PATH,
    VALIDATION_POLICY_SHA256,
)
from tests.stories.st_01_01_synthetic_proof import ROOT


class AtomicContentHarnessValidationArchitectureBoundaryTests(unittest.TestCase):
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

    def test_validation_policy_is_exact_hash_pinned_and_bounded(self) -> None:
        path = ROOT / VALIDATION_POLICY_PATH
        self.assertEqual(sha256(path.read_bytes()).hexdigest(), VALIDATION_POLICY_SHA256)
        value = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(value["target"]["profile_id"], "synthetic_text_normalization_v1")
        self.assertFalse(value["target"]["production_eligible"])
        self.assertFalse(value["target"]["certified"])
        self.assertEqual(value["compatibility_scope"]["visual_asset_editor"], EXTERNAL_TARGET_COMPATIBILITY)
        self.assertEqual(value["compatibility_scope"]["delegation_contract"], EXTERNAL_TARGET_COMPATIBILITY)

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
