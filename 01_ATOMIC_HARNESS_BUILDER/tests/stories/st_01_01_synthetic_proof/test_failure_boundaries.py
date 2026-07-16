from __future__ import annotations

import ast
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from cmf_builder.domain.target_profile import (
    RegistryIntegrityError,
    TargetSelectionRejected,
    UnsupportedTargetForAuthorizedSlice,
)

from tests.stories.st_01_01_synthetic_proof import (
    CATEGORY_ID,
    PROFILE_ID,
    ROOT,
    build_service,
    copy_governed_inputs,
    create_command,
)


class SyntheticProofFailureBoundaryTests(unittest.TestCase):
    def test_ac_sp_06_mutated_profile_bytes_fail_before_run_creation(self) -> None:
        mutations = {
            "changed-bytes": lambda value: value + b"\n# drift",
            "wrong-profile-id": lambda value: value.replace(
                b"synthetic_text_normalization_v1",
                b"synthetic_text_normalization_v2",
                1,
            ),
            "wrong-target": lambda value: value.replace(
                b"compilation_target: atomic_content_harness",
                b"compilation_target: visual_asset_editor",
                1,
            ),
            "production-eligible": lambda value: value.replace(
                b"production_eligible: false", b"production_eligible: true", 1
            ),
            "canonical-category-membership": lambda value: value.replace(
                b"canonical_category_registry_membership: false",
                b"canonical_category_registry_membership: true",
                1,
            ),
            "wrong-registry-hash": lambda value: value.replace(
                b"a4a9e5afaf91f60b22529ec01f1bc8e22a0d895444ad9a9e9a96e7a3e7b28114",
                b"04a9e5afaf91f60b22529ec01f1bc8e22a0d895444ad9a9e9a96e7a3e7b28114",
                1,
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(mutation=name), TemporaryDirectory() as directory:
                root = Path(directory)
                copy_governed_inputs(root)
                fixture = root / (
                    "development-capsules/ST-01.01-SYNTHETIC-PROOF/"
                    "SYNTHETIC_TARGET_PROFILE_FIXTURE.yaml"
                )
                fixture.write_bytes(mutate(fixture.read_bytes()))
                service, repository, observations, _, _ = build_service(root=root)

                with self.assertRaises(RegistryIntegrityError):
                    service.create_run(create_command())

                self.assertEqual(repository.stream_count, 0)
                self.assertEqual(
                    observations.observations[-1].failure_context["code"],
                    "RegistryIntegrityError",
                )

    def test_ac_sp_06_wrong_identity_or_non_synthetic_binding_fails_closed(self) -> None:
        cases = (
            create_command(command_id="wrong-profile", profile_id="public_comment"),
            create_command(command_id="wrong-category", category_id="2d_character_animation"),
            create_command(command_id="format02", profile_id="format02_minimal_coach_theatre"),
        )
        for command in cases:
            with self.subTest(command=command.command_id):
                service, repository, _, _, _ = build_service()
                with self.assertRaises(UnsupportedTargetForAuthorizedSlice):
                    service.create_run(command)
                self.assertEqual(repository.stream_count, 0)

    def test_ac_sp_08_external_conversational_and_unknown_targets_remain_closed(self) -> None:
        cases = (
            create_command(command_id="vae", target_ids=("visual_asset_editor",)),
            create_command(
                command_id="delegation",
                target_ids=("content_asset_delegation_contract",),
            ),
            create_command(command_id="unknown", target_ids=("external_provider",)),
            create_command(
                command_id="conversational",
                category_id="conversational_activation_expression",
                profile_id="public_comment",
            ),
        )
        for command in cases:
            with self.subTest(command=command.command_id):
                service, repository, _, _, _ = build_service()
                expected = (
                    TargetSelectionRejected
                    if command.command_id == "unknown"
                    else UnsupportedTargetForAuthorizedSlice
                )
                with self.assertRaises(expected):
                    service.create_run(command)
                self.assertEqual(repository.stream_count, 0)

    def test_architecture_boundary_keeps_original_source_set_and_no_external_imports(self) -> None:
        expected = {
            "src/cmf_builder/__init__.py",
            "src/cmf_builder/domain/__init__.py",
            "src/cmf_builder/domain/run.py",
            "src/cmf_builder/domain/evidence_workspace.py",
            "src/cmf_builder/domain/evidence_index.py",
            "src/cmf_builder/domain/evidence_saturation.py",
            "src/cmf_builder/domain/genesis_questions.py",
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
            "src/cmf_builder/application/evidence_saturation_commands.py",
            "src/cmf_builder/application/genesis_question_commands.py",
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
        prohibited = {
            "requests",
            "sqlalchemy",
            "fastapi",
            "temporalio",
            "boto3",
            "delegation",
            "visual_asset_editor",
        }
        actual: set[str] = set()
        for path in (ROOT / "src/cmf_builder").rglob("*.py"):
            relative = path.relative_to(ROOT).as_posix()
            actual.add(relative)
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            roots: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    roots.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    roots.add(node.module.split(".", 1)[0])
            self.assertFalse(roots & prohibited, relative)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
