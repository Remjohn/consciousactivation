from __future__ import annotations

import ast
from hashlib import sha256
import unittest

from cmf_builder.adapters.file_declared_boundary_repository import (
    FileDeclaredBoundaryRepository,
)
from cmf_builder.application.atomicity_commands import (
    DECLARED_INPUT_PATH,
    DECLARED_INPUT_SHA256,
)
from tests.stories.st_01_01_synthetic_proof import ROOT
from tests.source_boundary_registry import registered_source_files


class AtomicityArchitectureBoundaryTests(unittest.TestCase):
    PROHIBITED_IMPORT_ROOTS = {
        "boto3",
        "delegation",
        "fastapi",
        "requests",
        "sqlalchemy",
        "temporalio",
        "visual_asset_editor",
    }

    def test_ac_10_source_tree_is_layered_standard_library_only_and_exact(self) -> None:
        actual: set[str] = set()
        for path in (ROOT / "src/cmf_builder").rglob("*.py"):
            relative = path.relative_to(ROOT).as_posix()
            actual.add(relative)
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imports = self._imports(tree)
            roots = {item.split(".", 1)[0] for item in imports}
            self.assertFalse(roots & self.PROHIBITED_IMPORT_ROOTS, relative)
            if "/domain/" in relative:
                self.assertFalse(any(item.startswith(("cmf_builder.application", "cmf_builder.adapters")) for item in imports), relative)
        self.assertEqual(actual, registered_source_files(ROOT))

    def test_ac_01_10_declared_input_is_hash_pinned_and_nonproduction(self) -> None:
        self.assertEqual(sha256((ROOT / DECLARED_INPUT_PATH).read_bytes()).hexdigest(), DECLARED_INPUT_SHA256)
        value = FileDeclaredBoundaryRepository(ROOT).load(
            DECLARED_INPUT_PATH, DECLARED_INPUT_SHA256
        )
        self.assertTrue(value.synthetic)
        self.assertFalse(value.production_eligible)
        self.assertFalse(value.certified)
        self.assertEqual(value.category_binding, "none")

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
