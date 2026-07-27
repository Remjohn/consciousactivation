from __future__ import annotations

import ast
from hashlib import sha256
from pathlib import Path
import unittest

from cmf_builder.domain.capability_ownership import (
    CAPABILITY_OWNERSHIP_INPUT_PATH,
    CAPABILITY_OWNERSHIP_INPUT_SHA256,
    EMPTY_SKILL_REGISTRY_FIXTURE_PATH,
    EMPTY_SKILL_REGISTRY_FIXTURE_SHA256,
    EMPTY_SKILL_REGISTRY_POLICY_PATH,
    EMPTY_SKILL_REGISTRY_POLICY_SHA256,
    EMPTY_SKILL_REGISTRY_VALIDATION_PATH,
    EMPTY_SKILL_REGISTRY_VALIDATION_SHA256,
)


ROOT = Path(__file__).resolve().parents[3]
NEW_SOURCE = {
    "src/cmf_builder/domain/capability_ownership.py",
    "src/cmf_builder/application/capability_commands.py",
    "src/cmf_builder/domain/responsibility_modules.py",
    "src/cmf_builder/application/module_commands.py",
    "src/cmf_builder/domain/phase_graph.py",
    "src/cmf_builder/application/phase_commands.py",
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


class CapabilityArchitectureBoundaryTests(unittest.TestCase):
    def test_authorized_core_source_modules_exist(self) -> None:
        self.assertEqual(
            {path for path in NEW_SOURCE if (ROOT / path).is_file()}, NEW_SOURCE
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
        for relative in (
            "src/cmf_builder/domain/capability_ownership.py",
            "src/cmf_builder/domain/responsibility_modules.py",
            "src/cmf_builder/domain/phase_graph.py",
            "src/cmf_builder/domain/handoff.py",
        ):
            tree = ast.parse((ROOT / relative).read_text(encoding="utf-8"))
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

    def test_governed_inputs_are_exactly_hash_pinned(self) -> None:
        expected = {
            CAPABILITY_OWNERSHIP_INPUT_PATH: CAPABILITY_OWNERSHIP_INPUT_SHA256,
            EMPTY_SKILL_REGISTRY_POLICY_PATH: EMPTY_SKILL_REGISTRY_POLICY_SHA256,
            EMPTY_SKILL_REGISTRY_FIXTURE_PATH: EMPTY_SKILL_REGISTRY_FIXTURE_SHA256,
            EMPTY_SKILL_REGISTRY_VALIDATION_PATH: EMPTY_SKILL_REGISTRY_VALIDATION_SHA256,
        }
        for relative, digest in expected.items():
            self.assertEqual(sha256((ROOT / relative).read_bytes()).hexdigest(), digest)

    def test_no_later_story_or_external_runtime_module_is_added(self) -> None:
        source_paths = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "src/cmf_builder").rglob("*.py")
        }
        joined = "\n".join(sorted(source_paths)).lower()
        for prohibited in (
            "capability_module",
            "workflow_ir",
            "development_capsule_compiler",
            "control_tower",
            "format02",
            "skill_resolver",
            "skill_discovery",
            "delegation_runtime",
            "vae_runtime",
        ):
            self.assertNotIn(prohibited, joined)

    def test_no_dependency_lock_or_published_runtime_tree_is_created(self) -> None:
        self.assertFalse(
            any(
                (ROOT / name).exists()
                for name in (
                    "requirements.txt",
                    "poetry.lock",
                    "package-lock.json",
                    "human",
                    "openspec",
                    "machine",
                )
            )
        )


if __name__ == "__main__":
    unittest.main()
