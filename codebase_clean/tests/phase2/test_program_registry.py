"""Unit and integration tests for CAE Program Registry and Package Discovery (Mandate M14)."""

from __future__ import annotations

import tempfile
from pathlib import Path
import pytest
import yaml

from ca_runtime.program_registry import (
    CANONICAL_AUTHORITY_LANES,
    InvalidAuthorityLaneError,
    MissingProgramDependencyError,
    ProgramConflictError,
    ProgramDependency,
    ProgramManifest,
    ProgramManifestValidationError,
    ProgramNotFoundError,
    ProgramPackage,
    ProgramPreflightResult,
    ProgramRegistry,
    ProgramStatus,
    SkillBinding,
    SkillNestingViolationError,
    compute_file_sha256,
    compute_package_composite_sha256,
    get_program_registry,
)


@pytest.fixture
def programs_root() -> Path:
    return Path("programs").resolve()


def test_canonical_program_manifest_parsing(programs_root: Path) -> None:
    registry = ProgramRegistry(discovery_roots=[programs_root])
    packages = registry.discover()
    assert len(packages) >= 3

    program_ids = {p.program_id for p in packages}
    assert "interview_semantic_program" in program_ids
    assert "collision_discovery_program" in program_ids
    assert "editorial_storyboard_program" in program_ids


def test_package_composite_sha256_stability(programs_root: Path) -> None:
    pkg_dir = programs_root / "interview_semantic_program"
    hash1, files1 = compute_package_composite_sha256(pkg_dir)
    hash2, files2 = compute_package_composite_sha256(pkg_dir)

    assert hash1 == hash2
    assert len(hash1) == 64
    assert "program_manifest.yaml" in files1
    assert "skills/interview_elicitation/SKILL.md" in files1


def test_authority_lanes_enforcement() -> None:
    # Valid lanes
    manifest = ProgramManifest(
        id="test_program",
        version="1.0.0",
        purpose="Test valid lanes",
        lanes=["HUNTER", "ANALYST"],
    )
    assert set(manifest.lanes).issubset(CANONICAL_AUTHORITY_LANES)

    # Invalid / Collapsed lane rejected
    with pytest.raises(ValueError, match="Invalid authority lanes"):
        ProgramManifest(
            id="test_program_invalid",
            version="1.0.0",
            purpose="Test invalid lanes",
            lanes=["HUNTER", "INVALID_LANE"],
        )


def test_semver_validation_enforcement() -> None:
    # Valid SemVer
    m1 = ProgramManifest(id="test_semver", version="0.1.0-alpha.1", purpose="Valid SemVer", lanes=["HUNTER"])
    assert m1.version == "0.1.0-alpha.1"

    # Invalid SemVers fail closed
    for bad_ver in ["1", "1.0", "v1.0.0", "1.0.0.0", "alpha"]:
        with pytest.raises(ValueError, match="not a valid SemVer"):
            ProgramManifest(id="test_semver_bad", version=bad_ver, purpose="Bad SemVer", lanes=["HUNTER"])


def test_skill_nesting_violation_rejection(tmp_path: Path) -> None:
    pkg_dir = tmp_path / "nested_skill_program"
    pkg_dir.mkdir()
    
    skill_dir = pkg_dir / "skills" / "illegal_nested_skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Illegal Skill", encoding="utf-8")
    
    # Create forbidden nested sub-skills directory
    (skill_dir / "skills").mkdir()
    (skill_dir / "skills" / "sub_skill.md").write_text("# Nested", encoding="utf-8")

    manifest_data = {
        "program": {
            "id": "nested_skill_program",
            "version": "1.0.0",
            "purpose": "Test nesting rejection",
            "lanes": ["HUNTER"],
            "skills": [
                {"name": "illegal_nested_skill", "path": "skills/illegal_nested_skill", "version": "1.0.0"}
            ],
        }
    }
    (pkg_dir / "program_manifest.yaml").write_text(yaml.dump(manifest_data), encoding="utf-8")

    registry = ProgramRegistry()
    with pytest.raises(SkillNestingViolationError, match="contains nested skills or subagents"):
        registry.inspect_and_validate_package(pkg_dir)


def test_missing_skill_file_rejection(tmp_path: Path) -> None:
    pkg_dir = tmp_path / "missing_skill_program"
    pkg_dir.mkdir()

    manifest_data = {
        "program": {
            "id": "missing_skill_program",
            "version": "1.0.0",
            "purpose": "Test missing skill",
            "lanes": ["HUNTER"],
            "skills": [
                {"name": "non_existent_skill", "path": "skills/non_existent.md", "version": "1.0.0"}
            ],
        }
    }
    (pkg_dir / "program_manifest.yaml").write_text(yaml.dump(manifest_data), encoding="utf-8")

    registry = ProgramRegistry()
    with pytest.raises(SkillNestingViolationError, match="Skill file does not exist"):
        registry.inspect_and_validate_package(pkg_dir)


def test_program_preflight_success(programs_root: Path) -> None:
    registry = ProgramRegistry(discovery_roots=[programs_root])
    registry.discover()

    # Preflight for interview_semantic_program with required preconditions
    res = registry.preflight(
        program_id="interview_semantic_program",
        workspace_id="ws-1234",
        context_refs=["workspace_active", "interview_brief_approved"],
    )

    assert res.eligible is True
    assert res.issues == []
    assert res.authority_lane_checks == {"HUNTER": True, "ANALYST": True}
    assert len(res.preflight_digest) == 64


def test_program_preflight_fail_closed_missing_preconditions(programs_root: Path) -> None:
    registry = ProgramRegistry(discovery_roots=[programs_root])
    registry.discover()

    # Missing preconditions
    res = registry.preflight(
        program_id="interview_semantic_program",
        workspace_id="ws-1234",
        context_refs=[],
    )

    assert res.eligible is False
    assert "Unsatisfied precondition: workspace_active" in res.issues
    assert "Unsatisfied precondition: interview_brief_approved" in res.issues


def test_program_preflight_fail_closed_missing_dependency(programs_root: Path) -> None:
    registry = ProgramRegistry()
    # Register only editorial_storyboard_program (which depends on interview_semantic_program)
    pkg = registry.inspect_and_validate_package(programs_root / "editorial_storyboard_program")
    registry.register(pkg)

    res = registry.preflight(
        program_id="editorial_storyboard_program",
        workspace_id="ws-1234",
        context_refs=["workspace_active", "evidence_segments_verified"],
    )

    assert res.eligible is False
    assert "Missing dependency: interview_semantic_program" in res.issues
    assert "interview_semantic_program" in res.missing_dependencies


def test_inspect_program(programs_root: Path) -> None:
    registry = ProgramRegistry(discovery_roots=[programs_root])
    registry.discover()

    inspection = registry.inspect_program("collision_discovery_program")
    assert inspection["program_id"] == "collision_discovery_program"
    assert inspection["status"] == "ACTIVE"
    assert "HUNTER" in inspection["authority_lanes"]
    assert len(inspection["skills"]) == 1
    assert inspection["skills"][0]["name"] == "collision_hunting"
    assert len(inspection["manifest_sha256"]) == 64
    assert len(inspection["package_sha256"]) == 64


def test_program_conflict_detection(programs_root: Path) -> None:
    registry = ProgramRegistry()
    pkg = registry.inspect_and_validate_package(programs_root / "interview_semantic_program")
    registry.register(pkg)

    # Attempt duplicate registration without allow_overwrite raises ProgramConflictError
    with pytest.raises(ProgramConflictError):
        registry.register(pkg, allow_overwrite=False)


def test_program_not_found_handling() -> None:
    registry = ProgramRegistry()
    with pytest.raises(ProgramNotFoundError):
        registry.get_program("unknown_program_id")
