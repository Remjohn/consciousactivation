from __future__ import annotations

import ast
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
STORY_SOURCE = {
    "src/cmf_builder/domain/skill_registry.py",
    "src/cmf_builder/application/skill_commands.py",
}
ALLOWED_IMPORT_ROOTS = {
    "__future__",
    "dataclasses",
    "enum",
    "hashlib",
    "json",
    "pathlib",
    "cmf_builder",
}


class SyntheticSkillNecessityArchitectureTests(unittest.TestCase):
    def test_story_adds_no_source_module_or_external_import(self) -> None:
        self.assertFalse((ROOT / "src/cmf_builder/domain/skill_necessity.py").exists())
        self.assertFalse((ROOT / "src/cmf_builder/application/skill_necessity_commands.py").exists())
        for relative in STORY_SOURCE:
            tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
            roots: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    roots.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    roots.add((node.module or "").split(".", 1)[0])
            self.assertTrue(roots <= ALLOWED_IMPORT_ROOTS, (relative, roots))

    def test_no_external_runtime_skill_execution_or_later_story_behavior_is_added(self) -> None:
        joined = "\n".join(
            (ROOT / path).read_text(encoding="utf-8").lower()
            for path in sorted(STORY_SOURCE)
        )
        for prohibited in (
            "import requests",
            "import httpx",
            "import sqlalchemy",
            "import fastapi",
            "import subprocess",
            "dynamic_skill_loader",
            "skill_package_installer",
            "workflow_runtime",
            "atomic_harness_definition_compiler",
            "development_capsule_compiler",
            "vae_runtime",
            "delegation_runtime",
            "control_tower",
        ):
            self.assertNotIn(prohibited, joined)

    def test_no_dependency_database_transport_or_schema_surface_is_added(self) -> None:
        self.assertFalse(any((ROOT / name).exists() for name in (
            "requirements.txt",
            "poetry.lock",
            "package-lock.json",
        )))
        self.assertFalse((ROOT / "contracts/schemas/skill-necessity.schema.json").exists())
        self.assertFalse((ROOT / "governance/schemas/skill-necessity.schema.json").exists())


if __name__ == "__main__":
    unittest.main()
