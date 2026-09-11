"""Tests for CAE JIT Skill Loader, Maturity Gating, and Package-Local Context Resolution (Mandate M22)."""

from __future__ import annotations

import hashlib
from pathlib import Path
import tempfile
import pytest
import yaml

from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_registry import (
    ProgramManifest,
    ProgramPackage,
    ProgramRegistry,
    compute_file_sha256,
)
from ca_runtime.skill_loader import (
    LoadedSkill,
    MaturityGateViolationError,
    PassiveSkillExecutionEnvironment,
    SkillAuthorityMismatchError,
    SkillExecutionContextCapsule,
    SkillFrontmatterParseError,
    SkillLoader,
    SkillLoaderError,
    SkillMaturityState,
    SkillMetadata,
    SkillNestingError,
    SkillNotFoundError,
    SkillToSkillInvocationProhibitedError,
    UnapprovedSkillExecutionError,
    compile_skill_context_capsule,
    execute_passive_skill,
    parse_skill_markdown,
    resolve_package_context,
)


@pytest.fixture
def programs_root() -> Path:
    return Path("programs").resolve()


def test_parse_skill_markdown_with_valid_frontmatter() -> None:
    raw = """---
name: sample_skill
description: A test skill for validation.
version: 1.2.0
maturity: STABLE
lanes:
  - HUNTER
  - ANALYST
triggers:
  - test_trigger
inputs:
  - test_input
outputs:
  - test_output
---

# Sample Skill

This is the body of the skill.
"""
    fm, body = parse_skill_markdown(raw)
    assert fm["name"] == "sample_skill"
    assert fm["version"] == "1.2.0"
    assert fm["maturity"] == "STABLE"
    assert fm["lanes"] == ["HUNTER", "ANALYST"]
    assert fm["triggers"] == ["test_trigger"]
    assert body == "# Sample Skill\n\nThis is the body of the skill."


def test_parse_skill_markdown_fallback_without_frontmatter() -> None:
    raw = """# Fallback Header

This is a skill without YAML frontmatter.
"""
    fm, body = parse_skill_markdown(raw)
    assert fm["name"] == "fallback_header"
    assert fm["description"] == "This is a skill without YAML frontmatter."
    assert fm["version"] == "1.0.0"
    assert fm["maturity"] == "STABLE"
    assert body == raw.strip()


def test_load_canonical_programs_skills(programs_root: Path) -> None:
    loader = SkillLoader()
    
    # 1. Collision Hunting Skill
    skill_path_1 = programs_root / "collision_discovery_program" / "skills" / "collision_hunting"
    loaded_1 = loader.load_skill_from_path(
        skill_path_1,
        package_root=programs_root / "collision_discovery_program",
    )
    assert loaded_1.metadata.name == "collision_hunting"
    assert loaded_1.metadata.version == "1.0.0"
    assert loaded_1.metadata.maturity == SkillMaturityState.STABLE
    assert len(loaded_1.metadata.sha256) == 64
    assert loaded_1.package_context is not None
    assert loaded_1.package_context.cae_constitution is not None
    assert "Collision" in loaded_1.body_markdown

    # 2. Storyboard Compiler Skill
    skill_path_2 = programs_root / "editorial_storyboard_program" / "skills" / "storyboard_compiler"
    loaded_2 = loader.load_skill_from_path(
        skill_path_2,
        package_root=programs_root / "editorial_storyboard_program",
    )
    assert loaded_2.metadata.name == "storyboard_compiler"
    assert loaded_2.metadata.maturity == SkillMaturityState.STABLE

    # 3. Interview Elicitation Skill
    skill_path_3 = programs_root / "interview_semantic_program" / "skills" / "interview_elicitation"
    loaded_3 = loader.load_skill_from_path(
        skill_path_3,
        package_root=programs_root / "interview_semantic_program",
    )
    assert loaded_3.metadata.name == "interview_elicitation"
    assert loaded_3.metadata.maturity == SkillMaturityState.STABLE


def test_resolve_skill_via_program_registry(programs_root: Path) -> None:
    registry = ProgramRegistry(discovery_roots=[programs_root])
    registry.discover()
    loader = SkillLoader(program_registry=registry)

    resolved = loader.resolve_skill("collision_discovery_program", "collision_hunting")
    assert resolved.metadata.name == "collision_hunting"
    assert resolved.metadata.version == "1.0.0"
    assert resolved.metadata.maturity == SkillMaturityState.STABLE

    # Non-existent skill raises SkillNotFoundError
    with pytest.raises(SkillNotFoundError):
        loader.resolve_skill("collision_discovery_program", "non_existent_skill")


def test_hash_pinning_stability_and_mismatch_detection(tmp_path: Path) -> None:
    pkg_dir = tmp_path / "test_pkg"
    pkg_dir.mkdir()
    skill_dir = pkg_dir / "skills" / "pinned_skill"
    skill_dir.mkdir(parents=True)
    
    skill_content = """---
name: pinned_skill
description: Deterministic pinned skill
version: 1.0.0
maturity: STABLE
---
# Content
"""
    (skill_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")
    actual_sha = compute_file_sha256(skill_dir / "SKILL.md")

    manifest_data = {
        "program": {
            "id": "test_pkg",
            "version": "1.0.0",
            "purpose": "Test hash pinning",
            "lanes": ["HUNTER"],
            "skills": [
                {
                    "name": "pinned_skill",
                    "path": "skills/pinned_skill",
                    "version": "1.0.0",
                    "sha256": actual_sha,
                }
            ],
        }
    }
    (pkg_dir / "program_manifest.yaml").write_text(yaml.dump(manifest_data), encoding="utf-8")

    registry = ProgramRegistry()
    pkg = registry.inspect_and_validate_package(pkg_dir)
    registry.register(pkg)

    loader = SkillLoader(program_registry=registry)
    loaded = loader.resolve_skill("test_pkg", "pinned_skill")
    assert loaded.metadata.sha256 == actual_sha

    # Tamper with file content to trigger hash mismatch detection
    (skill_dir / "SKILL.md").write_text(skill_content + "\n# Tampered line", encoding="utf-8")
    with pytest.raises(SkillLoaderError, match="hash mismatch"):
        loader.resolve_skill("test_pkg", "pinned_skill")


def test_fail_closed_maturity_gating(tmp_path: Path) -> None:
    # Test DRAFT state
    draft_skill_dir = tmp_path / "draft_skill"
    draft_skill_dir.mkdir()
    (draft_skill_dir / "SKILL.md").write_text("""---
name: draft_skill
description: Draft skill authoring in progress
version: 0.1.0
maturity: DRAFT
lanes:
  - HUNTER
---
# Draft
""", encoding="utf-8")

    loader = SkillLoader()
    draft_skill = loader.load_skill_from_path(draft_skill_dir)
    assert draft_skill.metadata.maturity == SkillMaturityState.DRAFT

    capsule = compile_skill_context_capsule(
        skill=draft_skill,
        workspace_id="ws-test",
        lane=AuthorityLane.HUNTER,
    )

    def dummy_runner(env: PassiveSkillExecutionEnvironment, inputs: dict) -> dict:
        return {"result": "ok"}

    # DRAFT execution must fail closed
    with pytest.raises(UnapprovedSkillExecutionError, match="Cannot execute skill 'draft_skill' with maturity state 'DRAFT'"):
        execute_passive_skill(draft_skill, capsule, dummy_runner)

    # Test REVOKED state
    revoked_skill_dir = tmp_path / "revoked_skill"
    revoked_skill_dir.mkdir()
    (revoked_skill_dir / "SKILL.md").write_text("""---
name: revoked_skill
description: Revoked skill
version: 1.0.0
maturity: REVOKED
lanes:
  - HUNTER
---
# Revoked
""", encoding="utf-8")

    revoked_skill = loader.load_skill_from_path(revoked_skill_dir)
    revoked_capsule = compile_skill_context_capsule(revoked_skill, "ws-test", AuthorityLane.HUNTER)

    with pytest.raises(UnapprovedSkillExecutionError, match="with maturity state 'REVOKED'"):
        execute_passive_skill(revoked_skill, revoked_capsule, dummy_runner)

    # Test DEPRECATED state
    dep_skill_dir = tmp_path / "deprecated_skill"
    dep_skill_dir.mkdir()
    (dep_skill_dir / "SKILL.md").write_text("""---
name: deprecated_skill
description: Deprecated skill
version: 1.0.0
maturity: DEPRECATED
lanes:
  - HUNTER
---
# Deprecated
""", encoding="utf-8")

    dep_skill = loader.load_skill_from_path(dep_skill_dir)
    dep_capsule = compile_skill_context_capsule(dep_skill, "ws-test", AuthorityLane.HUNTER)

    with pytest.raises(UnapprovedSkillExecutionError, match="with maturity state 'DEPRECATED'"):
        execute_passive_skill(dep_skill, dep_capsule, dummy_runner)


def test_prototype_maturity_gating_sandbox(tmp_path: Path) -> None:
    proto_skill_dir = tmp_path / "proto_skill"
    proto_skill_dir.mkdir()
    (proto_skill_dir / "SKILL.md").write_text("""---
name: proto_skill
description: Prototype skill
version: 0.9.0
maturity: PROTOTYPE
lanes:
  - ANALYST
---
# Prototype
""", encoding="utf-8")

    loader = SkillLoader()
    proto_skill = loader.load_skill_from_path(proto_skill_dir)
    capsule = compile_skill_context_capsule(proto_skill, "ws-test", AuthorityLane.ANALYST)

    def dummy_runner(env: PassiveSkillExecutionEnvironment, inputs: dict) -> dict:
        return {"analyst_output": "data"}

    # Default production execution fails closed
    with pytest.raises(MaturityGateViolationError, match="requires explicit sandbox authorization"):
        execute_passive_skill(proto_skill, capsule, dummy_runner, allow_prototype_sandbox=False)

    # Allowed when sandbox is explicitly authorized
    res = execute_passive_skill(proto_skill, capsule, dummy_runner, allow_prototype_sandbox=True)
    assert res["status"] == "COMPLETED"
    assert res["output"] == {"analyst_output": "data"}


def test_approved_stable_skill_execution(tmp_path: Path) -> None:
    stable_skill_dir = tmp_path / "stable_skill"
    stable_skill_dir.mkdir()
    (stable_skill_dir / "SKILL.md").write_text("""---
name: stable_skill
description: Stable approved skill
version: 1.0.0
maturity: STABLE
lanes:
  - COMPOSER
---
# Stable
""", encoding="utf-8")

    loader = SkillLoader()
    stable_skill = loader.load_skill_from_path(stable_skill_dir)
    capsule = compile_skill_context_capsule(stable_skill, "ws-prod", AuthorityLane.COMPOSER)

    def composer_runner(env: PassiveSkillExecutionEnvironment, inputs: dict) -> dict:
        return {"storyboard_rendered": True, "beat_count": 4}

    res = execute_passive_skill(stable_skill, capsule, composer_runner, inputs={"theme": "tension"})
    assert res["status"] == "COMPLETED"
    assert res["skill_name"] == "stable_skill"
    assert res["lane"] == "COMPOSER"
    assert res["output"]["beat_count"] == 4
    assert len(res["execution_sha256"]) == 64


def test_authority_lane_enforcement_fail_closed(tmp_path: Path) -> None:
    hunter_skill_dir = tmp_path / "hunter_only_skill"
    hunter_skill_dir.mkdir()
    (hunter_skill_dir / "SKILL.md").write_text("""---
name: hunter_only_skill
description: Only permitted in HUNTER lane
version: 1.0.0
maturity: STABLE
lanes:
  - HUNTER
---
# Hunter Only
""", encoding="utf-8")

    loader = SkillLoader()
    skill = loader.load_skill_from_path(hunter_skill_dir)

    # Attempt to execute in COMPOSER lane must fail closed
    composer_capsule = compile_skill_context_capsule(skill, "ws-1", AuthorityLane.COMPOSER)

    def dummy_runner(env: PassiveSkillExecutionEnvironment, inputs: dict) -> dict:
        return {}

    with pytest.raises(SkillAuthorityMismatchError, match="does not permit execution in Authority Lane 'COMPOSER'"):
        execute_passive_skill(skill, composer_capsule, dummy_runner)


def test_anti_nesting_and_prohibition_of_skill_to_skill_invocation(tmp_path: Path) -> None:
    # 1. Filesystem nesting rejection
    bad_dir = tmp_path / "nesting_attempt"
    bad_dir.mkdir()
    (bad_dir / "SKILL.md").write_text("# Root Skill", encoding="utf-8")
    (bad_dir / "skills").mkdir()
    (bad_dir / "skills" / "nested.md").write_text("# Nested", encoding="utf-8")

    loader = SkillLoader()
    with pytest.raises(SkillNestingError, match="violates flat constitution"):
        loader.load_skill_from_path(bad_dir)

    # 2. Runtime Skill-to-Skill invocation rejection
    clean_dir = tmp_path / "clean_skill"
    clean_dir.mkdir()
    (clean_dir / "SKILL.md").write_text("""---
name: clean_skill
description: Clean skill
version: 1.0.0
maturity: STABLE
lanes:
  - HUNTER
---
# Clean
""", encoding="utf-8")

    clean_skill = loader.load_skill_from_path(clean_dir)
    capsule = compile_skill_context_capsule(clean_skill, "ws-1", AuthorityLane.HUNTER)

    def illegal_invoking_runner(env: PassiveSkillExecutionEnvironment, inputs: dict) -> dict:
        # Attempt to invoke another skill from inside skill execution frame
        env.invoke_skill("another_skill")
        return {}

    with pytest.raises(SkillToSkillInvocationProhibitedError, match="Skill-to-Skill invocation is strictly prohibited"):
        execute_passive_skill(clean_skill, capsule, illegal_invoking_runner)


def test_context_precedence_capsule_structure(programs_root: Path) -> None:
    loader = SkillLoader()
    pkg_root = programs_root / "interview_semantic_program"
    skill_path = pkg_root / "skills" / "interview_elicitation"
    skill = loader.load_skill_from_path(skill_path, package_root=pkg_root)

    capsule = compile_skill_context_capsule(
        skill=skill,
        workspace_id="ws-9999",
        lane=AuthorityLane.HUNTER,
        operator_grant_id="grant-001",
        program_id="interview_semantic_program",
    )

    # Verify 6-layer precedence representation
    assert capsule.cae_constitution_ref == "CAE_ACTIVATE_CONSTITUTION_v1.1"
    assert capsule.tenancy_layer["workspace_id"] == "ws-9999"
    assert capsule.tenancy_layer["operator_grant_id"] == "grant-001"
    assert capsule.program_policy_layer["program_id"] == "interview_semantic_program"
    assert capsule.local_governance_layer["has_local_cae"] is True
    assert capsule.instructions_layer["has_instructions"] is True
    assert capsule.skill_layer["name"] == "interview_elicitation"
    assert len(capsule.composite_digest) == 64
    assert capsule.capsule_id.startswith("capsule-interview_elicitation-")
