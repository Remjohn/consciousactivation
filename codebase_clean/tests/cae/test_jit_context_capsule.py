"""Unit and integration tests for CAE Phase 2 Mandate M18: JIT Context Capsule + Package Compilation.

Governed by:
- 00_CONTROL/22_PHASE2_AGENT_PACKAGE_COMPILATION_CONTRACT.md
- 00_CONTROL/27_PHASE2_CONTEXT_BUDGET_CONTRACT.md
- 00_CONTROL/21_PHASE2_CAPABILITY_SECURITY_MATRIX.md
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
"""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest

from ca_contracts import canonical_sha256
from ca_runtime.context_capsule import (
    AccessMode,
    AgentPackageCompiler,
    CapabilityProjection,
    CapabilityResolutionError,
    CapabilityScope,
    CompiledAgentPackage,
    ContextBudgetOverflowError,
    ContextBudgetReport,
    ContextCapsuleError,
    ContextExclusionReason,
    ContextExclusionRecord,
    ContextItem,
    ContextNestingViolationError,
    ContextPrecedenceConflictError,
    ContextPrecedenceLayer,
    ForbiddenContextError,
    JITContextCapsule,
    JITContextCompiler,
    MissingContextError,
    SkillMaturity,
    SkillMaturityViolationError,
    SkillPackageRef,
    estimate_tokens,
)
from ca_runtime.pi_adapter import AuthorityLane


@pytest.fixture
def sample_workspace_id():
    return uuid4()


def test_token_estimator():
    text = "Hello world! This is a test sentence with punctuation."
    tokens = estimate_tokens(text)
    assert tokens > 0
    assert estimate_tokens("") == 0


def test_context_precedence_hierarchy_assembly(sample_workspace_id):
    """Verifies strict 6-layer precedence order in assembled prompt."""
    capsule = JITContextCompiler.assemble(
        workspace_id=sample_workspace_id,
        lane=AuthorityLane.ANALYST,
        actor_id="analyst_agent_01",
        program_id="editorial_intelligence",
        harness_id="ca_topo_07",
        agent_id="curator_analyst",
        constitutions=[
            ("c_skill_const", "docs/CANONICAL_SKILL_AUTHORING_CONSTITUTION.md", "Skills must remain passive and flat."),
        ],
        operator_grants=[
            ("grant_op_01", "operator_session:grant_999", "Operator authorizes Analyst run for workspace."),
        ],
        program_harness_policies=[
            ("policy_harness_07", "harness:ca_topo_07", "Harness recovery law: descendant rerun only."),
        ],
        local_governance_cae_md=("agent/CAE.md", "Local rule: output must adhere to E3 schema."),
        local_guidance_agents_md=("agent/AGENTS.md", "Guidance: maintain concise summaries."),
        agent_instructions=("agent/instructions.md", "Analyze candidate collisions and score resonance."),
        skills=[
            (
                SkillPackageRef(
                    skill_id="collision_detection",
                    version="1.0.0",
                    maturity=SkillMaturity.STABLE,
                    procedure_ref="skills/collision_detection/SKILL.md",
                    package_sha256="abc123sha",
                ),
                "Procedure: Run similarity checks across semantic entities.",
            )
        ],
        artifacts=[
            ("art_01", "artifact:summary.md", "Previous run summary evidence."),
        ],
    )

    assert capsule.lane == AuthorityLane.ANALYST
    assert len(capsule.included_context) == 8
    assert len(capsule.exclusion_trace) == 0

    # Verify layer ordering in included_context
    layers = [item.layer for item in capsule.included_context]
    assert layers == sorted(layers)
    assert layers[0] == ContextPrecedenceLayer.CAE_CONSTITUTION
    assert layers[1] == ContextPrecedenceLayer.OPERATOR_AUTHORIZATION
    assert layers[2] == ContextPrecedenceLayer.PROGRAM_HARNESS_POLICY
    assert layers[3] == ContextPrecedenceLayer.LOCAL_GOVERNANCE
    assert layers[4] == ContextPrecedenceLayer.LOCAL_GOVERNANCE
    assert layers[5] == ContextPrecedenceLayer.AGENT_INSTRUCTIONS
    assert layers[6] == ContextPrecedenceLayer.SKILL_PROCEDURE
    assert layers[7] == ContextPrecedenceLayer.SKILL_PROCEDURE

    # Verify assembled prompt has precedence headings in order
    prompt = capsule.assembled_prompt
    pos_const = prompt.find("CAE_CONSTITUTION")
    pos_op = prompt.find("OPERATOR_AUTHORIZATION")
    pos_policy = prompt.find("PROGRAM_HARNESS_POLICY")
    pos_local = prompt.find("LOCAL_GOVERNANCE")
    pos_inst = prompt.find("AGENT_INSTRUCTIONS")
    pos_skill = prompt.find("SKILL_PROCEDURE")

    assert pos_const != -1
    assert pos_const < pos_op < pos_policy < pos_local < pos_inst < pos_skill

    # Verify canonical dict serialization
    c_dict = capsule.canonical_dict()
    assert c_dict["capsule_id"].startswith("jit_capsule_")
    assert c_dict["lane"] == "ANALYST"
    assert c_dict["workspace_id"] == str(sample_workspace_id)
    assert "collision_detection" in c_dict["skill_hashes"]


def test_reconcile_local_cae_and_agents_md(sample_workspace_id):
    """Verifies that CAE.md outranks AGENTS.md within Layer 4."""
    capsule = JITContextCompiler.assemble(
        workspace_id=sample_workspace_id,
        lane=AuthorityLane.HUNTER,
        actor_id="hunter_01",
        program_id="discovery",
        harness_id="harness_01",
        agent_id="hunter_scout",
        local_governance_cae_md=("package/CAE.md", "CAE mandatory rule."),
        local_guidance_agents_md=("package/AGENTS.md", "Operating guidance."),
    )

    local_items = [item for item in capsule.included_context if item.layer == ContextPrecedenceLayer.LOCAL_GOVERNANCE]
    assert len(local_items) == 2
    assert local_items[0].context_id == "local_cae_governance"
    assert local_items[1].context_id == "local_agents_guidance"


def test_skill_maturity_gating(sample_workspace_id):
    """Verifies that DRAFT skills fail closed in production mode."""
    draft_skill = SkillPackageRef(
        skill_id="draft_experiment",
        version="0.1.0",
        maturity=SkillMaturity.DRAFT,
        procedure_ref="skills/draft_experiment/SKILL.md",
        package_sha256="draftsha123",
    )
    stable_skill = SkillPackageRef(
        skill_id="stable_proc",
        version="1.0.0",
        maturity=SkillMaturity.STABLE,
        procedure_ref="skills/stable_proc/SKILL.md",
        package_sha256="stablesha123",
    )

    # 1. Non-production allows DRAFT
    dev_capsule = JITContextCompiler.assemble(
        workspace_id=sample_workspace_id,
        lane=AuthorityLane.COMPOSER,
        actor_id="composer_01",
        program_id="prog",
        harness_id="harness",
        agent_id="agent",
        skills=[(draft_skill, "Draft procedure content")],
        production_mode=False,
    )
    assert len(dev_capsule.included_context) == 1
    assert "draft_experiment" in dev_capsule.skill_hashes

    # 2. Production mode blocks DRAFT with SkillMaturityViolationError
    with pytest.raises(SkillMaturityViolationError) as exc_info:
        JITContextCompiler.assemble(
            workspace_id=sample_workspace_id,
            lane=AuthorityLane.COMPOSER,
            actor_id="composer_01",
            program_id="prog",
            harness_id="harness",
            agent_id="agent",
            skills=[(draft_skill, "Draft procedure content")],
            production_mode=True,
        )
    assert exc_info.value.reason_code == "SKILL_MATURITY_VIOLATION"
    assert exc_info.value.details["skill_id"] == "draft_experiment"

    # 3. Production mode accepts STABLE
    prod_capsule = JITContextCompiler.assemble(
        workspace_id=sample_workspace_id,
        lane=AuthorityLane.COMPOSER,
        actor_id="composer_01",
        program_id="prog",
        harness_id="harness",
        agent_id="agent",
        skills=[(stable_skill, "Stable procedure content")],
        production_mode=True,
    )
    assert len(prod_capsule.included_context) == 1
    assert "stable_proc" in prod_capsule.skill_hashes


def test_agent_package_compiler_with_temp_dir(tmp_path: Path):
    """Verifies AgentPackageCompiler scanning, anti-nesting, and manifest generation."""
    pkg_dir = tmp_path / "test_agent_package"
    pkg_dir.mkdir()

    # 1. Missing CAE.md raises ContextCapsuleError
    (pkg_dir / "instructions.md").write_text("Agent instructions", encoding="utf-8")
    with pytest.raises(ContextCapsuleError) as exc_info:
        AgentPackageCompiler.compile(pkg_dir, agent_id="test_agent", lane=AuthorityLane.COMMANDER)
    assert "CAE.md" in str(exc_info.value)

    # 2. Create CAE.md and AGENTS.md
    (pkg_dir / "CAE.md").write_text("Governed CAE constraints", encoding="utf-8")
    (pkg_dir / "AGENTS.md").write_text("Operating guidance", encoding="utf-8")

    # 3. Add Flat Skill
    skills_dir = pkg_dir / "skills" / "summary_skill"
    skills_dir.mkdir(parents=True)
    (skills_dir / "SKILL.md").write_text("Skill procedure instructions", encoding="utf-8")
    (skills_dir / "manifest.json").write_text(
        json.dumps({"maturity": "STABLE", "version": "1.2.0", "allowed_tools": ["grep", "view"]}),
        encoding="utf-8",
    )

    # 4. Add Nested Skill (Violates Constitution)
    nested_skill_dir = skills_dir / "skills" / "illegal_nested"
    nested_skill_dir.mkdir(parents=True)
    (nested_skill_dir / "SKILL.md").write_text("Illegal nested skill", encoding="utf-8")

    with pytest.raises(ContextNestingViolationError):
        AgentPackageCompiler.compile(pkg_dir, agent_id="test_agent", lane=AuthorityLane.COMMANDER)

    # Remove illegal nested directory
    (nested_skill_dir / "SKILL.md").unlink()
    nested_skill_dir.rmdir()
    (skills_dir / "skills").rmdir()

    # 5. Compile cleanly
    cap_proj = CapabilityProjection(
        capability_id="cae.operation.execute",
        owner_product="CAE",
        scope=CapabilityScope.CAE_TYPED_OPERATION,
        mode=AccessMode.MUTATION_OPERATION,
        workspace_bound=True,
        approval_required=True,
        sandbox_required=False,
        audit_mode="receipt",
        bound_tools=("cae_exec_op",),
    )

    compiled_pkg = AgentPackageCompiler.compile(
        pkg_dir,
        agent_id="commander_agent",
        lane=AuthorityLane.COMMANDER,
        version="2.0.0",
        production_mode=True,
        declared_capabilities=[cap_proj],
    )

    assert compiled_pkg.agent_id == "commander_agent"
    assert compiled_pkg.lane == AuthorityLane.COMMANDER
    assert len(compiled_pkg.skills) == 1
    assert compiled_pkg.skills[0].skill_id == "summary_skill"
    assert compiled_pkg.skills[0].maturity == SkillMaturity.STABLE
    assert len(compiled_pkg.capabilities) == 1
    assert len(compiled_pkg.package_sha256) == 64

    # Verify canonical dict
    pkg_dict = compiled_pkg.canonical_dict()
    assert pkg_dict["lane"] == "COMMANDER"
    assert pkg_dict["version"] == "2.0.0"


def test_context_budget_overflow_and_exclusion(sample_workspace_id):
    """Verifies token budget enforcement and observable exclusion traces."""
    # Mandatory item exceeds budget -> raises ContextBudgetOverflowError
    with pytest.raises(ContextBudgetOverflowError) as exc_info:
        JITContextCompiler.assemble(
            workspace_id=sample_workspace_id,
            lane=AuthorityLane.HUNTER,
            actor_id="hunter_01",
            program_id="prog",
            harness_id="harness",
            agent_id="agent",
            total_token_budget=10,  # very small budget
            constitutions=[
                ("const_large", "doc/const.md", "This is a large constitution text that will exceed ten tokens by far."),
            ],
        )
    assert exc_info.value.reason_code == "CONTEXT_BUDGET_OVERFLOW"

    # Optional item exceeds remaining budget -> excluded with trace
    capsule = JITContextCompiler.assemble(
        workspace_id=sample_workspace_id,
        lane=AuthorityLane.HUNTER,
        actor_id="hunter_01",
        program_id="prog",
        harness_id="harness",
        agent_id="agent",
        total_token_budget=30,
        constitutions=[
            ("const_small", "doc/const.md", "Short constitution rule."),
        ],
        artifacts=[
            ("art_large", "doc/art.md", "This is a massive artifact summary text with lots of detailed information that will easily consume more than thirty tokens and therefore exceed the remaining token budget."),
        ],
    )

    assert len(capsule.included_context) == 1
    assert len(capsule.exclusion_trace) == 1
    assert capsule.exclusion_trace[0].context_id == "art_large"
    assert capsule.exclusion_trace[0].reason == ContextExclusionReason.BUDGET_EXCEEDED
    assert capsule.budget_report.consumed_tokens <= 30
    assert not capsule.budget_report.overflow


def test_forbidden_and_missing_context(sample_workspace_id):
    """Verifies forbidden context exclusion and missing mandatory context checks."""
    # 1. Forbidden context in optional section
    capsule = JITContextCompiler.assemble(
        workspace_id=sample_workspace_id,
        lane=AuthorityLane.ANALYST,
        actor_id="analyst_01",
        program_id="prog",
        harness_id="harness",
        agent_id="agent",
        skills=[
            (
                SkillPackageRef(
                    skill_id="forbidden_skill",
                    version="1.0.0",
                    maturity=SkillMaturity.STABLE,
                    procedure_ref="skills/forbidden_skill/SKILL.md",
                    package_sha256="sha123",
                ),
                "Forbidden skill procedure text",
            )
        ],
        forbidden_context_ids=["skill_forbidden_skill"],
    )
    assert len(capsule.included_context) == 0
    assert len(capsule.exclusion_trace) == 1
    assert capsule.exclusion_trace[0].context_id == "skill_forbidden_skill"
    assert capsule.exclusion_trace[0].reason == ContextExclusionReason.FORBIDDEN_BY_POLICY

    # 2. Mandatory context missing raises MissingContextError
    with pytest.raises(MissingContextError) as exc_info:
        JITContextCompiler.assemble(
            workspace_id=sample_workspace_id,
            lane=AuthorityLane.ANALYST,
            actor_id="analyst_01",
            program_id="prog",
            harness_id="harness",
            agent_id="agent",
            mandatory_context_ids=["required_identity_dna"],
        )
    assert exc_info.value.reason_code == "MISSING_MANDATORY_CONTEXT"
    assert "required_identity_dna" in exc_info.value.details["missing_contexts"]


def test_deterministic_capsule_sha256(sample_workspace_id):
    """Verifies that identical context inputs produce exact matching SHA-256 digests."""
    cap1 = JITContextCompiler.assemble(
        workspace_id=sample_workspace_id,
        lane=AuthorityLane.COMPOSER,
        actor_id="composer_01",
        program_id="creative_engine",
        harness_id="harness_alpha",
        agent_id="beat_composer",
        constitutions=[("c1", "const.md", "Invariant 1")],
        agent_instructions=("inst.md", "Compose sonic beat cluster"),
    )

    cap2 = JITContextCompiler.assemble(
        workspace_id=sample_workspace_id,
        lane=AuthorityLane.COMPOSER,
        actor_id="composer_01",
        program_id="creative_engine",
        harness_id="harness_alpha",
        agent_id="beat_composer",
        constitutions=[("c1", "const.md", "Invariant 1")],
        agent_instructions=("inst.md", "Compose sonic beat cluster"),
    )

    assert cap1.included_context[0].sha256 == cap2.included_context[0].sha256
    assert cap1.budget_report.consumed_tokens == cap2.budget_report.consumed_tokens
    assert len(cap1.capsule_sha256) == 64
    assert len(cap2.capsule_sha256) == 64


def test_explicit_capability_projections(sample_workspace_id):
    """Verifies that capabilities are bound to workspace and lane with security sandbox settings."""
    cap1 = CapabilityProjection(
        capability_id="cae.interview.read",
        owner_product="INTERVIEW",
        scope=CapabilityScope.CAE_TYPED_OPERATION,
        mode=AccessMode.READ_ONLY,
        workspace_bound=True,
        approval_required=False,
        sandbox_required=False,
        audit_mode="receipt",
        bound_tools=("read_interview_transcript",),
    )
    cap2 = CapabilityProjection(
        capability_id="cae.mcp.web_search",
        owner_product="CAE",
        scope=CapabilityScope.MCP_TOOL,
        mode=AccessMode.READ_ONLY,
        workspace_bound=True,
        approval_required=False,
        sandbox_required=True,
        audit_mode="connection_trace",
        mcp_servers=("google_search_mcp",),
    )

    capsule = JITContextCompiler.assemble(
        workspace_id=sample_workspace_id,
        lane=AuthorityLane.HUNTER,
        actor_id="hunter_01",
        program_id="discovery_prog",
        harness_id="harness_alpha",
        agent_id="scout_agent",
        capabilities=[cap1, cap2],
    )

    assert len(capsule.capability_projections) == 2
    c_dict = capsule.canonical_dict()
    assert len(c_dict["capability_projections"]) == 2
    assert c_dict["capability_projections"][0]["capability_id"] == "cae.interview.read"
    assert c_dict["capability_projections"][0]["mode"] == "READ_ONLY"
    assert c_dict["capability_projections"][1]["capability_id"] == "cae.mcp.web_search"
    assert c_dict["capability_projections"][1]["sandbox_required"] is True


def test_agent_package_with_subagents(tmp_path: Path):
    """Verifies scanning and resolving subagent directories in agent package."""
    pkg_dir = tmp_path / "agent_with_subagents"
    pkg_dir.mkdir()
    (pkg_dir / "CAE.md").write_text("CAE constraints", encoding="utf-8")
    (pkg_dir / "instructions.md").write_text("Commander instructions", encoding="utf-8")

    subagents_dir = pkg_dir / "subagents" / "specialist_analyst"
    subagents_dir.mkdir(parents=True)
    (subagents_dir / "instructions.md").write_text("Subagent instructions", encoding="utf-8")

    compiled_pkg = AgentPackageCompiler.compile(
        pkg_dir,
        agent_id="main_commander",
        lane=AuthorityLane.COMMANDER,
    )

    assert len(compiled_pkg.subagents) == 1
    assert compiled_pkg.subagents[0] == "specialist_analyst"
    pkg_dict = compiled_pkg.canonical_dict()
    assert "specialist_analyst" in pkg_dict["subagents"]

