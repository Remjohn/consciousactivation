from __future__ import annotations

import ast
from pathlib import Path
import unittest

from tests.stories.st_01_02 import ROOT
from tests.source_boundary_registry import registered_source_files


class StoryArchitectureBoundaryTests(unittest.TestCase):
    def test_ac_10_source_tree_is_internal_standard_library_only_and_layered(self) -> None:
        prohibited_roots = {
            "boto3",
            "delegation",
            "fastapi",
            "requests",
            "sqlalchemy",
            "temporalio",
            "visual_asset_editor",
        }
        actual: set[str] = set()
        for path in (ROOT / "src/cmf_builder").rglob("*.py"):
            relative = path.relative_to(ROOT).as_posix()
            actual.add(relative)
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imports = self._imports(tree)
            roots = {item.split(".", 1)[0] for item in imports}
            self.assertFalse(roots & prohibited_roots, relative)
            if "/domain/" in relative:
                self.assertFalse(
                    any(
                        item.startswith("cmf_builder.application")
                        or item.startswith("cmf_builder.adapters")
                        for item in imports
                    ),
                    relative,
                )
            if "/application/" in relative:
                self.assertFalse(
                    any(item.startswith("cmf_builder.adapters") for item in imports),
                    relative,
                )
        self.assertEqual(actual, registered_source_files(ROOT))

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
