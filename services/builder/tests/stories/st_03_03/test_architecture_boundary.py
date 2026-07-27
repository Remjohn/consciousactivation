from __future__ import annotations

import ast
import unittest

from tests.stories.st_01_01_synthetic_proof import ROOT
from tests.source_boundary_registry import registered_source_files


class HarnessIRArchitectureBoundaryTests(unittest.TestCase):
    PROHIBITED_IMPORT_ROOTS = {
        "boto3", "delegation", "fastapi", "requests", "sqlalchemy",
        "temporalio", "visual_asset_editor",
    }

    def test_ac_12_source_tree_is_exact_layered_and_standard_library_only(self) -> None:
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

    def test_ac_07_12_no_external_runtime_schema_or_later_story_module_exists(self) -> None:
        paths = {path.relative_to(ROOT).as_posix() for path in (ROOT / "src/cmf_builder").rglob("*.py")}
        joined = "\n".join(sorted(paths)).lower()
        for prohibited in (
            "workflow_ir", "artifact_compiler",
            "development_capsule_compiler", "control_tower", "format02", "vae", "delegation",
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
