from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import unittest

from tests.stories.st_01_01 import ROOT, build_service


class ArchitectureAndContractBoundaryTests(unittest.TestCase):
    EXPECTED_SOURCE_FILES = {
        "src/cmf_builder/__init__.py",
        "src/cmf_builder/domain/__init__.py",
        "src/cmf_builder/domain/run.py",
        "src/cmf_builder/domain/evidence_workspace.py",
        "src/cmf_builder/domain/evidence_index.py",
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
        "src/cmf_builder/domain/target_package_validation.py",
        "src/cmf_builder/domain/development_capsule.py",
        "src/cmf_builder/domain/target_profile.py",
        "src/cmf_builder/application/__init__.py",
        "src/cmf_builder/application/ports.py",
        "src/cmf_builder/application/run_commands.py",
        "src/cmf_builder/application/authority.py",
        "src/cmf_builder/application/evidence_commands.py",
        "src/cmf_builder/application/evidence_index_commands.py",
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
        "src/cmf_builder/application/target_validation_commands.py",
        "src/cmf_builder/application/development_capsule_commands.py",
        "src/cmf_builder/application/checkpoints.py",
        "src/cmf_builder/adapters/__init__.py",
        "src/cmf_builder/adapters/in_memory_run_repository.py",
        "src/cmf_builder/adapters/file_evidence_workspace.py",
        "src/cmf_builder/adapters/file_declared_boundary_repository.py",
        "src/cmf_builder/adapters/file_constitutional_policy_repository.py",
        "src/cmf_builder/adapters/file_target_profile_repository.py",
    }
    PROHIBITED_IMPORT_ROOTS = {
        "requests",
        "sqlalchemy",
        "fastapi",
        "temporalio",
        "boto3",
        "delegation",
        "visual_asset_editor",
    }

    def test_domain_does_not_import_application_or_adapters(self) -> None:
        for path in (ROOT / "src/cmf_builder/domain").glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            modules = self._imports(tree)
            self.assertFalse(
                any(
                    module.startswith("cmf_builder.application")
                    or module.startswith("cmf_builder.adapters")
                    for module in modules
                ),
                f"domain boundary violation in {path}",
            )

    def test_source_files_import_no_external_product_or_runtime_dependency(self) -> None:
        actual = set()
        for path in (ROOT / "src/cmf_builder").rglob("*.py"):
            relative = path.relative_to(ROOT).as_posix()
            actual.add(relative)
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            roots = {module.split(".", 1)[0] for module in self._imports(tree)}
            self.assertFalse(roots & self.PROHIBITED_IMPORT_ROOTS, relative)
        self.assertEqual(actual, self.EXPECTED_SOURCE_FILES)

    def test_governed_contract_inputs_are_hash_valid_and_read_only(self) -> None:
        expected = {
            "governance/COMPILATION_TARGET_REGISTRY.yaml": "0e9c82b6f87a9b7f5dff317578c0da18241fbfd66e29cc2226e161399d4da2ca",
            "contracts/integration/CATEGORY_PROFILE_COMPATIBILITY.yaml": "781a438ef1298c1bc71da6ab54298774f09c0be97becf513510913f98fc97a71",
            "docs/contracts/CONTRACT_REGISTRY.yaml": "cb9240ef0818a6180de75fe79c02901e3f41a2ec2ed97688fb754a567ad79fce",
            "docs/contracts/schemas/constitutional-evaluation.schema.json": "886c119ab0e8be6b1f469886f7baf2cebcc08ac95148a56ff084933ffb4afc9f",
        }
        for relative, digest in expected.items():
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), digest)

        schema = json.loads(
            (ROOT / "docs/contracts/schemas/constitutional-evaluation.schema.json").read_text(
                encoding="utf-8-sig"
            )
        )
        self.assertIn("ConstitutionalReadinessReceipt", schema["$defs"])
        registry = (ROOT / "docs/contracts/CONTRACT_REGISTRY.yaml").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("contract_id: ConstitutionalReadinessReceipt", registry)
        _, _, _, _, profiles = build_service()
        self.assertEqual(profiles.load_authorized_profile().compatibility_state, "contract_compatible")

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
