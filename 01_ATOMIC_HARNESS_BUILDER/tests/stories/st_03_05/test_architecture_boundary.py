from __future__ import annotations

import ast
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
NEW_SOURCE = {
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
ALLOWED_IMPORT_ROOTS = {
    "__future__",
    "dataclasses",
    "datetime",
    "enum",
    "hashlib",
    "json",
    "pathlib",
    "typing",
    "cmf_builder",
}


class ConstitutionalArchitectureBoundaryTests(unittest.TestCase):
    def test_exact_three_story_source_modules_exist(self) -> None:
        self.assertEqual(
            {path for path in NEW_SOURCE if (ROOT / path).is_file()}, NEW_SOURCE
        )

    def test_st_04_01_adds_only_its_two_authorized_source_modules(self) -> None:
        self.assertEqual(
            {
                path
                for path in ST_04_01_SOURCE | ST_04_02_SOURCE | ST_04_03_SOURCE | ST_04_04_SOURCE
                if (ROOT / path).is_file()
            },
            ST_04_01_SOURCE | ST_04_02_SOURCE | ST_04_03_SOURCE | ST_04_04_SOURCE,
        )

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
        path = ROOT / "src/cmf_builder/domain/constitutional_validation.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        }
        self.assertFalse(
            any(
                item.startswith("cmf_builder.application")
                or item.startswith("cmf_builder.adapters")
                for item in imports
            )
        )

    def test_no_external_runtime_schema_or_later_story_module_is_added(self) -> None:
        source_paths = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "src/cmf_builder").rglob("*.py")
        }
        joined = "\n".join(sorted(source_paths)).lower()
        for prohibited in (
            "workflow_ir",
            "atomic_harness_definition",
            "development_capsule_compiler",
            "control_tower",
            "format02",
        ):
            self.assertNotIn(prohibited, joined)
        self.assertFalse(
            any(
                (ROOT / name).exists()
                for name in ("requirements.txt", "poetry.lock", "package-lock.json")
            )
        )


if __name__ == "__main__":
    unittest.main()
