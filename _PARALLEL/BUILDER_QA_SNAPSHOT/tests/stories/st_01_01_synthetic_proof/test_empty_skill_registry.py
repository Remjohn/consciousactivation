from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from jsonschema import Draft202012Validator
import yaml

from cmf_builder.adapters import SyntheticProofTargetProfileRepository
from cmf_builder.domain.target_profile import (
    ImmutableProfileVersionRequired,
    RegistryIntegrityError,
    UndeclaredSkillUseRejected,
)

from tests.stories.st_01_01_synthetic_proof import (
    EMPTY_REGISTRY_SHA256,
    ROOT,
    copy_governed_inputs,
)


class EmptySkillRegistryTests(unittest.TestCase):
    def test_ac_sp_05_governed_registry_is_schema_valid_and_explicitly_empty(self) -> None:
        schema = json.loads(
            (ROOT / "governance/schemas/empty-skill-registry.schema.json").read_text(
                encoding="utf-8"
            )
        )
        fixture = yaml.safe_load(
            (ROOT / "governance/fixtures/synthetic-core/empty-skill-registry.yaml").read_text(
                encoding="utf-8"
            )
        )
        Draft202012Validator(schema).validate(fixture)

        registry = SyntheticProofTargetProfileRepository(ROOT).load_empty_skill_registry()
        self.assertEqual(registry.registry_id, "builder-core-synthetic-empty-skill-registry")
        self.assertEqual(registry.version, "1.0.0")
        self.assertEqual(registry.source_hash, EMPTY_REGISTRY_SHA256)
        self.assertEqual(registry.skills, ())
        self.assertFalse(registry.external_skills_required)
        self.assertFalse(registry.dynamic_skill_discovery_allowed)
        self.assertEqual(registry.undeclared_skill_use, "FAIL_CLOSED")

    def test_ac_sp_05_undeclared_and_dynamic_skill_use_fail_closed(self) -> None:
        registry = SyntheticProofTargetProfileRepository(ROOT).load_empty_skill_registry()

        with self.assertRaises(UndeclaredSkillUseRejected):
            registry.require_skill("future_external_skill")
        with self.assertRaises(UndeclaredSkillUseRejected):
            registry.require_skill("future_external_skill", dynamically_discovered=True)

    def test_same_version_cannot_add_a_skill(self) -> None:
        repository = SyntheticProofTargetProfileRepository(ROOT)
        registry = repository.load_empty_skill_registry()
        profile = repository.load_authorized_profile()

        with self.assertRaises(ImmutableProfileVersionRequired):
            registry.validate_skill_change(
                candidate_version="1.0.0",
                candidate_skills=("future_external_skill",),
            )
        registry.validate_skill_change(
            candidate_version="1.0.1",
            candidate_skills=("future_external_skill",),
        )
        with self.assertRaises(UndeclaredSkillUseRejected):
            profile.require_skill("future_external_skill")
        with self.assertRaises(ImmutableProfileVersionRequired):
            profile.validate_skill_change(
                candidate_profile_version="1.0.0",
                candidate_skill_ids=("future_external_skill",),
            )
        profile.validate_skill_change(
            candidate_profile_version="1.0.1",
            candidate_skill_ids=("future_external_skill",),
        )

    def test_mutated_registry_bytes_are_rejected_before_use(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            copy_governed_inputs(root)
            registry_path = root / (
                "governance/fixtures/synthetic-core/empty-skill-registry.yaml"
            )
            registry_path.write_bytes(
                registry_path.read_bytes().replace(b"skills: []", b"skills: [injected]")
            )

            with self.assertRaises(RegistryIntegrityError):
                SyntheticProofTargetProfileRepository(root).load_empty_skill_registry()


if __name__ == "__main__":
    unittest.main()
