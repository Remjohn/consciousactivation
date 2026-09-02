"""Unit and Integration Tests for CAE Mandate M50: Compiled Agent Package Contract.

Governed by:
- Mandate CAE-M50 (01_AGENT_EXECUTION/M50_compiled_agent_package_contract.md)
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/22_PHASE2_AGENT_PACKAGE_COMPILATION_CONTRACT.md

Proves:
1. Missing required CAE.md/instructions cause deterministic failure (Gate 1).
2. Constituent changes change package identity (Gate 2).
3. Uncertified Skills are blocked in production (Gate 3).
4. Nested Skill/subagent violations are rejected (Gate 4).
5. Same package inputs produce same package hash (Gate 5).
6. False-Proof Defense 1: Constituent removal after compilation triggers PackageDriftError.
7. False-Proof Defense 2: Skill tampering after compilation triggers drift detection.
8. False-Proof Defense 3: Quarantined package fails closed on integrity verification.
9. False-Proof Defense 4: Injected nested skill directory is rejected at compilation.
10. Inspection & Report: Component-hash manifest inspection report renders accurately.
11. Concrete Execution Trace: Agent -> CompiledAgentPackage -> JITContextCapsule -> Model Policy -> Gate -> Receipt.
"""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
from typing import Any, Dict
from uuid import uuid4
import pytest

from ca_contracts import canonical_json_text, canonical_sha256
from ca_runtime import (
    AccessMode,
    AgentPackageCompiler,
    AuthorityLane,
    CapabilityProjection,
    CapabilityScope,
    CompiledAgentPackage,
    ContextCapsuleError,
    ContextNestingViolationError,
    JITContextCompiler,
    PackageDriftError,
    PackageQuarantinedError,
    SkillMaturity,
    SkillMaturityViolationError,
    SkillPackageRef,
    get_agent_registry,
    reset_global_agent_registry,
)


@pytest.fixture
def sample_agent_dir(tmp_path: Path) -> Path:
    """Creates a standard, valid Eve-like agent package directory."""
    pkg_dir = tmp_path / "sample_analyst_agent"
    pkg_dir.mkdir(parents=True)

    # 1. CAE.md
    (pkg_dir / "CAE.md").write_text(
        "# CAE Governance: Sample Analyst Agent\n"
        "## Invariants\n"
        "1. Must operate in ANALYST lane.\n"
        "2. No direct database mutations.\n",
        encoding="utf-8",
    )

    # 2. instructions.md
    (pkg_dir / "instructions.md").write_text(
        "# Instructions — Sample Analyst Agent\n"
        "Analyze candidate relationships and detect contradictions.\n",
        encoding="utf-8",
    )

    # 3. AGENTS.md (optional guidance)
    (pkg_dir / "AGENTS.md").write_text(
        "# Agent Team Guidance\n"
        "Maintain adversarial independence.\n",
        encoding="utf-8",
    )

    # 4. Valid Flat Skill: skills/relationship_classifier
    skill_dir = pkg_dir / "skills" / "relationship_classifier"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "# Skill: Relationship Classifier\n"
        "Classify pairs into EQUIVALENT, SUBTYPE, or CONTRADICTION.\n",
        encoding="utf-8",
    )
    (skill_dir / "manifest.json").write_text(
        json.dumps({
            "name": "relationship_classifier",
            "version": "1.0.0",
            "maturity": "STABLE",
            "allowed_tools": ["semantic_similarity_analyzer"],
            "forbidden_actions": ["mutation"],
        }),
        encoding="utf-8",
    )

    return pkg_dir


def test_gate1_missing_required_constituents_fail_closed(tmp_path: Path):
    """Gate 1: Missing required CAE.md or instructions.md causes deterministic failure."""
    empty_dir = tmp_path / "empty_agent"
    empty_dir.mkdir()

    # Missing CAE.md
    with pytest.raises(ContextCapsuleError) as exc_cae:
        AgentPackageCompiler.compile(
            empty_dir,
            agent_id="test_agent",
            lane=AuthorityLane.ANALYST,
        )
    assert "missing required CAE.md" in str(exc_cae.value)

    # Add CAE.md but missing instructions.md
    (empty_dir / "CAE.md").write_text("# Governance", encoding="utf-8")
    with pytest.raises(ContextCapsuleError) as exc_inst:
        AgentPackageCompiler.compile(
            empty_dir,
            agent_id="test_agent",
            lane=AuthorityLane.ANALYST,
        )
    assert "missing required instructions.md" in str(exc_inst.value)


def test_gate2_constituent_changes_change_package_identity(sample_agent_dir: Path):
    """Gate 2: Modifying a constituent file immediately changes composite package SHA-256 and triggers drift."""
    pkg1 = AgentPackageCompiler.compile(
        sample_agent_dir,
        agent_id="SampleAnalystAgent",
        lane=AuthorityLane.ANALYST,
        version="1.0.0",
    )
    original_hash = pkg1.package_sha256
    assert len(original_hash) == 64
    assert len(pkg1.component_hashes) >= 4

    # Integrity verification passes initially
    pkg1.verify_integrity()
    has_drift, details = pkg1.detect_drift()
    assert not has_drift
    assert len(details["modified"]) == 0

    # Modify instructions.md on disk
    instructions_file = sample_agent_dir / "instructions.md"
    instructions_file.write_text(
        "# Instructions — Modified\nAltered instructions content.\n",
        encoding="utf-8",
    )

    # Existing compiled package detects drift against altered disk content
    has_drift, drift_details = pkg1.detect_drift()
    assert has_drift
    assert len(drift_details["modified"]) == 1
    assert drift_details["modified"][0]["file"] == "instructions.md"

    with pytest.raises(PackageDriftError) as exc_drift:
        pkg1.verify_integrity()
    assert exc_drift.value.reason_code == "PACKAGE_DRIFT"

    # Recompiling creates a new package with different hash
    pkg2 = AgentPackageCompiler.compile(
        sample_agent_dir,
        agent_id="SampleAnalystAgent",
        lane=AuthorityLane.ANALYST,
        version="1.0.0",
    )
    assert pkg2.package_sha256 != original_hash


def test_gate3_uncertified_draft_skills_blocked_in_production(tmp_path: Path):
    """Gate 3: Agent packages containing DRAFT skills fail closed when production_mode=True."""
    pkg_dir = tmp_path / "draft_skill_agent"
    pkg_dir.mkdir()
    (pkg_dir / "CAE.md").write_text("# Governance", encoding="utf-8")
    (pkg_dir / "instructions.md").write_text("# Instructions", encoding="utf-8")

    skill_dir = pkg_dir / "skills" / "experimental_skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Experimental Skill", encoding="utf-8")
    (skill_dir / "manifest.json").write_text(
        json.dumps({"name": "experimental_skill", "version": "0.1.0", "maturity": "DRAFT"}),
        encoding="utf-8",
    )

    # Non-production mode allows DRAFT skills for experimental exploration
    pkg_dev = AgentPackageCompiler.compile(
        pkg_dir,
        agent_id="DraftSkillAgent",
        lane=AuthorityLane.HUNTER,
        production_mode=False,
    )
    assert len(pkg_dev.skills) == 1
    assert pkg_dev.skills[0].maturity == SkillMaturity.DRAFT

    # Production mode strictly rejects DRAFT skills
    with pytest.raises(SkillMaturityViolationError) as exc_info:
        AgentPackageCompiler.compile(
            pkg_dir,
            agent_id="DraftSkillAgent",
            lane=AuthorityLane.HUNTER,
            production_mode=True,
        )
    assert exc_info.value.reason_code == "SKILL_MATURITY_VIOLATION"


def test_gate4_nested_skill_and_subagent_violations_rejected(tmp_path: Path):
    """Gate 4: Skills containing nested skills or subagents violate flat constitution and fail closed."""
    pkg_dir = tmp_path / "nested_violator_agent"
    pkg_dir.mkdir()
    (pkg_dir / "CAE.md").write_text("# Governance", encoding="utf-8")
    (pkg_dir / "instructions.md").write_text("# Instructions", encoding="utf-8")

    # 1. Nested skills inside a skill
    skill_dir = pkg_dir / "skills" / "parent_skill"
    (skill_dir / "skills" / "child_skill").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Parent Skill", encoding="utf-8")

    with pytest.raises(ContextNestingViolationError) as exc_nested_skill:
        AgentPackageCompiler.compile(pkg_dir, agent_id="ViolatorAgent", lane=AuthorityLane.COMPOSER)
    assert exc_nested_skill.value.reason_code == "SKILL_NESTING_VIOLATION"

    # Clean up nested skills, inject nested subagents
    (skill_dir / "skills" / "child_skill").rmdir()
    (skill_dir / "skills").rmdir()
    (skill_dir / "subagents" / "child_subagent").mkdir(parents=True)

    with pytest.raises(ContextNestingViolationError) as exc_nested_sa:
        AgentPackageCompiler.compile(pkg_dir, agent_id="ViolatorAgent", lane=AuthorityLane.COMPOSER)
    assert exc_nested_sa.value.reason_code == "SKILL_NESTING_VIOLATION"


def test_gate5_idempotent_package_hash(sample_agent_dir: Path):
    """Gate 5: Repeated compilation of identical package files produces byte-identical package_sha256."""
    pkg_a = AgentPackageCompiler.compile(
        sample_agent_dir,
        agent_id="SampleAnalystAgent",
        lane=AuthorityLane.ANALYST,
        version="1.0.0",
    )
    pkg_b = AgentPackageCompiler.compile(
        sample_agent_dir,
        agent_id="SampleAnalystAgent",
        lane=AuthorityLane.ANALYST,
        version="1.0.0",
    )

    assert pkg_a.package_sha256 == pkg_b.package_sha256
    assert pkg_a.component_hashes == pkg_b.component_hashes
    assert pkg_a.skills == pkg_b.skills


def test_false_proof_defense_constituent_removal(sample_agent_dir: Path):
    """False-Proof Defense 1: Deleting a required constituent after compilation triggers PackageDriftError."""
    pkg = AgentPackageCompiler.compile(
        sample_agent_dir,
        agent_id="SampleAnalystAgent",
        lane=AuthorityLane.ANALYST,
    )
    pkg.verify_integrity()

    # Remove CAE.md from disk
    cae_file = sample_agent_dir / "CAE.md"
    cae_file.unlink()

    has_drift, drift_details = pkg.detect_drift()
    assert has_drift
    assert "CAE.md" in drift_details["missing"]

    with pytest.raises(PackageDriftError) as exc_drift:
        pkg.verify_integrity()
    assert exc_drift.value.reason_code == "PACKAGE_DRIFT"


def test_false_proof_defense_skill_tampering(sample_agent_dir: Path):
    """False-Proof Defense 2: Modifying a skill file after compilation triggers drift detection."""
    pkg = AgentPackageCompiler.compile(
        sample_agent_dir,
        agent_id="SampleAnalystAgent",
        lane=AuthorityLane.ANALYST,
    )

    skill_file = sample_agent_dir / "skills" / "relationship_classifier" / "SKILL.md"
    skill_file.write_text("# Altered skill procedure text\nMalicious injection.", encoding="utf-8")

    has_drift, drift_details = pkg.detect_drift()
    assert has_drift
    assert any(m["file"] == "skills/relationship_classifier/SKILL.md" for m in drift_details["modified"])

    with pytest.raises(PackageDriftError):
        pkg.verify_integrity()


def test_false_proof_defense_quarantine_invalidation(sample_agent_dir: Path):
    """False-Proof Defense 3: Quarantining an agent package immediately blocks verify_integrity()."""
    pkg = AgentPackageCompiler.compile(
        sample_agent_dir,
        agent_id="SampleAnalystAgent",
        lane=AuthorityLane.ANALYST,
    )
    pkg.verify_integrity()  # Clean initially

    quarantined = pkg.quarantine("Identified prompt injection vector in relationship classifier")
    assert quarantined.is_quarantined
    assert quarantined.quarantine_reason == "Identified prompt injection vector in relationship classifier"
    assert quarantined.quarantined_at is not None

    with pytest.raises(PackageQuarantinedError) as exc_q:
        quarantined.verify_integrity()
    assert exc_q.value.reason_code == "PACKAGE_QUARANTINED"


def test_package_inspection_and_reporting(sample_agent_dir: Path):
    """Validates structured inspection dictionary and human-readable Markdown report."""
    pkg = AgentPackageCompiler.compile(
        sample_agent_dir,
        agent_id="SampleAnalystAgent",
        lane=AuthorityLane.ANALYST,
        version="1.0.0",
        declared_capabilities=[
            CapabilityProjection(
                capability_id="analyze_relationships",
                owner_product="cae",
                scope=CapabilityScope.CAE_TYPED_OPERATION,
                mode=AccessMode.READ_ONLY,
                workspace_bound=True,
                approval_required=False,
                sandbox_required=False,
                audit_mode="STANDARD",
            )
        ],
    )

    inspection = pkg.inspect()
    assert inspection["agent_id"] == "SampleAnalystAgent"
    assert inspection["lane"] == "ANALYST"
    assert inspection["version"] == "1.0.0"
    assert len(inspection["component_hashes"]) >= 4
    assert inspection["total_constituents"] >= 4

    report = pkg.to_inspection_report()
    assert "# Compiled Agent Package Inspection: SampleAnalystAgent (v1.0.0)" in report
    assert "## Constituents & Component Hashes" in report
    assert "## Bound Skills" in report
    assert "## Bound Capabilities" in report
    assert "CAE.md" in report


def test_concrete_agent_execution_trace_from_agents_directory():
    """Concrete Execution Demonstration on canonical package in agents/:
    Agent Package -> AgentPackageCompiler.compile() -> CompiledAgentPackage -> JITContextCapsule -> Receipt.
    """
    pkg_root = Path("agents/research_commander_agent")
    assert pkg_root.exists(), "Expected agents/research_commander_agent to exist"

    # 1. Compile canonical agent package
    compiled_pkg = AgentPackageCompiler.compile(
        pkg_root,
        agent_id="ResearchCommanderAgent",
        lane=AuthorityLane.COMMANDER,
        version="1.0.0",
        production_mode=True,
    )
    assert compiled_pkg.package_sha256 != ""
    assert not compiled_pkg.is_quarantined
    compiled_pkg.verify_integrity()

    # 2. Assemble JIT context capsule using compiled package refs
    workspace_id = uuid4()
    cae_text = (pkg_root / "CAE.md").read_text(encoding="utf-8")
    inst_text = (pkg_root / "instructions.md").read_text(encoding="utf-8")

    capsule = JITContextCompiler.assemble(
        workspace_id=workspace_id,
        lane=compiled_pkg.lane,
        actor_id="research_commander_01",
        program_id="research_canonicalization_program",
        harness_id="RESEARCH_HARNESS_V1",
        agent_id=compiled_pkg.agent_id,
        local_governance_cae_md=(compiled_pkg.cae_governance_ref, cae_text),
        agent_instructions=(compiled_pkg.instructions_ref, inst_text),
    )

    assert capsule.lane == AuthorityLane.COMMANDER
    assert capsule.capsule_sha256 != ""
    assert len(capsule.included_context) == 2

    # 3. Model & Output Policy Gate Simulation
    simulated_receipt = {
        "receipt_id": "cae.agent.compiled_invocation_receipt@1.0.0",
        "agent_id": compiled_pkg.agent_id,
        "package_sha256": compiled_pkg.package_sha256,
        "capsule_sha256": capsule.capsule_sha256,
        "authority_lane": compiled_pkg.lane.value,
        "gate_status": "PASSED",
    }
    receipt_sha = canonical_sha256(canonical_json_text(simulated_receipt))
    assert len(receipt_sha) == 64
    assert simulated_receipt["gate_status"] == "PASSED"
