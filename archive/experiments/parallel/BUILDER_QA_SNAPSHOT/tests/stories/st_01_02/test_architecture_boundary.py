from __future__ import annotations

import ast
from pathlib import Path
import unittest

from tests.stories.st_01_02 import ROOT


class StoryArchitectureBoundaryTests(unittest.TestCase):
    def test_ac_10_source_tree_is_internal_standard_library_only_and_layered(self) -> None:
        expected = {
            "src/cmf_builder/__init__.py",
            "src/cmf_builder/domain/__init__.py",
            "src/cmf_builder/domain/run.py",
            "src/cmf_builder/domain/target_profile.py",
            "src/cmf_builder/domain/evidence_workspace.py",
            "src/cmf_builder/domain/atomicity.py",
            "src/cmf_builder/domain/harness_ir.py",
            "src/cmf_builder/domain/generated_artifacts.py",
            "src/cmf_builder/domain/constitutional_validation.py",
            "src/cmf_builder/domain/capability_ownership.py",
            "src/cmf_builder/domain/responsibility_modules.py",
            "src/cmf_builder/domain/phase_graph.py",
            "src/cmf_builder/domain/handoff.py",
            "src/cmf_builder/domain/context_manifest.py",
            "src/cmf_builder/domain/skill_registry.py",
            "src/cmf_builder/domain/atomic_harness_definition.py",
            "src/cmf_builder/application/__init__.py",
            "src/cmf_builder/application/ports.py",
            "src/cmf_builder/application/run_commands.py",
            "src/cmf_builder/application/authority.py",
            "src/cmf_builder/application/checkpoints.py",
            "src/cmf_builder/application/evidence_commands.py",
            "src/cmf_builder/application/atomicity_commands.py",
            "src/cmf_builder/application/harness_ir_commands.py",
            "src/cmf_builder/application/harness_ir_migrations.py",
            "src/cmf_builder/application/artifact_commands.py",
            "src/cmf_builder/application/artifact_renderers.py",
            "src/cmf_builder/application/constitutional_commands.py",
            "src/cmf_builder/application/capability_commands.py",
            "src/cmf_builder/application/module_commands.py",
            "src/cmf_builder/application/phase_commands.py",
            "src/cmf_builder/application/handoff_commands.py",
            "src/cmf_builder/application/context_commands.py",
            "src/cmf_builder/application/skill_commands.py",
            "src/cmf_builder/application/definition_commands.py",
            "src/cmf_builder/adapters/__init__.py",
            "src/cmf_builder/adapters/in_memory_run_repository.py",
            "src/cmf_builder/adapters/file_target_profile_repository.py",
            "src/cmf_builder/adapters/file_evidence_workspace.py",
            "src/cmf_builder/adapters/file_declared_boundary_repository.py",
            "src/cmf_builder/adapters/file_constitutional_policy_repository.py",
        }
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
        self.assertEqual(actual, expected)

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
