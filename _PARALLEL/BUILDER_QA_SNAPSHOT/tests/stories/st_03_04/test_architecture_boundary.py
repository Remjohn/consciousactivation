from __future__ import annotations

import ast
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
NEW_SOURCE = {
    "src/cmf_builder/domain/generated_artifacts.py",
    "src/cmf_builder/application/artifact_commands.py",
    "src/cmf_builder/application/artifact_renderers.py",
}
ST_03_05_SOURCE = {
    "src/cmf_builder/domain/constitutional_validation.py",
    "src/cmf_builder/application/constitutional_commands.py",
    "src/cmf_builder/adapters/file_constitutional_policy_repository.py",
}
ST_04_01_SOURCE = {
    "src/cmf_builder/domain/capability_ownership.py",
    "src/cmf_builder/application/capability_commands.py",
}
ST_04_02_SOURCE = {
    "src/cmf_builder/domain/responsibility_modules.py",
    "src/cmf_builder/application/module_commands.py",
}
ST_04_03_SOURCE = {
    "src/cmf_builder/domain/phase_graph.py",
    "src/cmf_builder/application/phase_commands.py",
}
ST_04_04_SOURCE = {
    "src/cmf_builder/domain/handoff.py",
    "src/cmf_builder/application/handoff_commands.py",
}


class ArtifactArchitectureBoundaryTests(unittest.TestCase):
    def test_exact_three_authorized_source_modules_exist(self) -> None:
        for relative in NEW_SOURCE:
            self.assertTrue((ROOT / relative).is_file())

    def test_new_modules_use_only_standard_library_and_cmf_builder(self) -> None:
        for relative in NEW_SOURCE:
            tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    roots = {alias.name.split(".", 1)[0] for alias in node.names}
                elif isinstance(node, ast.ImportFrom):
                    roots = {(node.module or "").split(".", 1)[0]}
                else:
                    continue
                self.assertTrue(roots <= {"__future__", "dataclasses", "datetime", "enum", "hashlib", "json", "typing", "cmf_builder"})

    def test_no_forbidden_runtime_or_external_product_imports(self) -> None:
        forbidden = ("requests", "httpx", "subprocess", "comfy", "delegation", "vae", "control_tower")
        for relative in NEW_SOURCE:
            text = (ROOT / relative).read_text(encoding="utf-8").lower()
            for token in forbidden:
                self.assertNotIn(f"import {token}", text)

    def test_story_does_not_create_published_artifact_directories(self) -> None:
        for name in ("human", "openspec", "machine"):
            self.assertFalse((ROOT / name).exists())

    def test_st_03_05_adds_only_its_three_authorized_source_modules(self) -> None:
        for relative in ST_03_05_SOURCE:
            self.assertTrue((ROOT / relative).is_file())

    def test_st_04_01_adds_only_its_two_authorized_source_modules(self) -> None:
        for relative in ST_04_01_SOURCE | ST_04_02_SOURCE | ST_04_03_SOURCE | ST_04_04_SOURCE:
            self.assertTrue((ROOT / relative).is_file())


if __name__ == "__main__":
    unittest.main()
