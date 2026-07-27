from __future__ import annotations

import ast
from hashlib import sha256
from pathlib import Path
import unittest

from cmf_builder.domain.phase_graph import PHASE_GRAPH_INPUT_PATH, PHASE_GRAPH_INPUT_SHA256


ROOT = Path(__file__).resolve().parents[3]
NEW_SOURCE = {
    "src/cmf_builder/domain/phase_graph.py",
    "src/cmf_builder/application/phase_commands.py",
}
ST_04_04_SOURCE = {
    "src/cmf_builder/domain/handoff.py",
    "src/cmf_builder/application/handoff_commands.py",
}
ALLOWED_IMPORT_ROOTS = {
    "__future__", "dataclasses", "datetime", "enum", "hashlib", "json", "pathlib", "typing", "cmf_builder",
}


class PhaseGraphArchitectureTests(unittest.TestCase):
    def test_exact_two_story_source_modules_exist(self) -> None:
        expected = NEW_SOURCE | ST_04_04_SOURCE
        self.assertEqual({path for path in expected if (ROOT / path).is_file()}, expected)

    def test_story_modules_use_only_standard_library_and_builder(self) -> None:
        for relative in NEW_SOURCE:
            tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    roots = {alias.name.split(".", 1)[0] for alias in node.names}
                elif isinstance(node, ast.ImportFrom):
                    roots = {(node.module or "").split(".", 1)[0]}
                else:
                    continue
                self.assertTrue(roots <= ALLOWED_IMPORT_ROOTS, (relative, roots))

    def test_domain_remains_independent_of_application_and_adapters(self) -> None:
        tree = ast.parse((ROOT / "src/cmf_builder/domain/phase_graph.py").read_text(encoding="utf-8"))
        imports = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
        self.assertFalse(any(item.startswith(("cmf_builder.application", "cmf_builder.adapters")) for item in imports))

    def test_phase_input_is_exactly_hash_pinned(self) -> None:
        self.assertEqual(sha256((ROOT / PHASE_GRAPH_INPUT_PATH).read_bytes()).hexdigest(), PHASE_GRAPH_INPUT_SHA256)

    def test_no_external_dependency_schema_or_runtime_tree_is_added(self) -> None:
        for relative in NEW_SOURCE:
            tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
            imports = {
                alias.name.split(".", 1)[0]
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
                for alias in node.names
            }
            self.assertFalse(imports & {"requests", "httpx", "sqlalchemy", "fastapi", "subprocess", "delegation", "visual_asset_editor"})
        self.assertFalse(any((ROOT / name).exists() for name in ("requirements.txt", "poetry.lock", "package-lock.json")))


if __name__ == "__main__":
    unittest.main()
