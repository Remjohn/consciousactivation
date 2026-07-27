from __future__ import annotations

import ast
import unittest

from tests.stories.st_01_01_synthetic_proof import ROOT


class HarnessIRArchitectureBoundaryTests(unittest.TestCase):
    EXPECTED_SOURCE_FILES = {
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
        self.assertEqual(actual, self.EXPECTED_SOURCE_FILES)

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
