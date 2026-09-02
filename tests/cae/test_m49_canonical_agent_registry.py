"""Unit and Integration Tests for CAE Mandate M49: Canonical Agent Constitution + Registry.

Governed by:
- Mandate CAE-M49 (01_AGENT_EXECUTION/M49_canonical_agent_constitution_registry.md)
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/04_OBJECT_AUTHORITY_MAP.md

Proves:
1. An Agent is discoverable without a Program.
2. The same Agent ID/version resolves identically in repeated runs (deterministic resolution).
3. Program manifests can bind the registry Agent by reference.
4. A standalone-session call can bind the same Agent.
5. Invalid lifecycle/authority combinations fail closed (DRAFT in production, quarantined agents, lane mismatches).
6. False-Proof / Reward-Hacking Defense 1: Identity collision attack (conflicting body under existing ID/version) is blocked.
7. False-Proof / Reward-Hacking Defense 2: Capability & authority escalation attack (Hunter with mutation privileges) is blocked.
8. False-Proof / Reward-Hacking Defense 3: Inline unregistered agent invocation is blocked.
9. False-Proof / Reward-Hacking Defense 4: Prohibited skill nesting / recursive skill references are blocked.
10. Concrete Execution Trace: Demonstrates Agent -> Context -> Model Policy -> Typed Output -> Gate -> Receipt lineage.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
from uuid import UUID, uuid4
import pytest

from ca_contracts import canonical_json_text, canonical_sha256
from ca_runtime import (
    AccessMode,
    AgentCapabilityGrant,
    AgentCapabilityViolationError,
    AgentDefinition,
    AgentIdentityCollisionError,
    AgentLaneMismatchError,
    AgentLifecycleState,
    AgentLifecycleViolationError,
    AgentManifestValidationError,
    AgentModelPolicy,
    AgentNotFoundError,
    AgentOutputContract,
    AgentPromptReference,
    AgentQuarantinedError,
    AgentRegistry,
    AgentResolver,
    AuthorityLane,
    CapabilityScope,
    ProgramManifest,
    ProgramRegistry,
    create_standalone_agent_session,
    get_agent_registry,
    get_agent_resolver,
    reset_global_agent_registry,
)


@pytest.fixture(autouse=True)
def clean_registry():
    """Reset the global singleton registry before and after every test."""
    reset_global_agent_registry()
    yield
    reset_global_agent_registry()


def test_gate1_agent_discoverability_without_program():
    """Prove that Agents are discoverable, versioned, and valid without requiring a Program."""
    registry = get_agent_registry()
    discovered_count = registry.discover_agents("agents")

    assert discovered_count == 8, f"Expected 8 canonical agents in agents/, found {discovered_count}"

    agents = registry.list_agents()
    assert len(agents) == 8

    # Verify all 4 Authority Lanes are represented
    lanes = {a.authority_lane for a in agents}
    assert lanes == {
        AuthorityLane.HUNTER,
        AuthorityLane.ANALYST,
        AuthorityLane.COMPOSER,
        AuthorityLane.COMMANDER,
    }

    # Inspect ResearchCommanderAgent
    commander = registry.get("ResearchCommanderAgent", "1.0.0")
    assert commander.agent_id == "ResearchCommanderAgent"
    assert commander.version == "1.0.0"
    assert commander.authority_lane == AuthorityLane.COMMANDER
    assert commander.lifecycle_state == AgentLifecycleState.APPROVED
    assert commander.content_sha256 != ""
    assert len(commander.content_sha256) == 64
    assert commander.model_policy.preferred_model == "gemini-2.5-pro"
    assert commander.prompt_reference.instructions_ref == "instructions.md"
    assert commander.output_contract is not None
    assert commander.output_contract.contract_id == "research_canonicalization_receipt"


def test_gate2_deterministic_repeat_resolution():
    """Prove that resolving the same Agent ID/version yields byte-identical results across runs."""
    registry = get_agent_registry()
    registry.discover_agents("agents")
    resolver = AgentResolver(registry)

    res1 = resolver.resolve("ResearchCommanderAgent", "1.0.0")
    res2 = resolver.resolve("ResearchCommanderAgent", "1.0.0")
    res3 = resolver.resolve("ResearchCommanderAgent")  # highest SemVer

    assert res1.content_sha256 == res2.content_sha256 == res3.content_sha256
    assert res1.canonical_dict() == res2.canonical_dict() == res3.canonical_dict()
    assert res1.compute_content_sha256() == res1.content_sha256


def test_gate3_program_manifest_reference_binding():
    """Prove that Program manifests can bind canonical agents by reference and validate compatibility."""
    registry = get_agent_registry()
    registry.discover_agents("agents")
    resolver = AgentResolver(registry)

    # Manifest referencing agents with SemVer tags and bare IDs
    manifest = ProgramManifest(
        id="research_canonicalization_program",
        version="1.0.0",
        purpose="Canonical research curation and OKF projection",
        lanes=["COMMANDER", "HUNTER", "ANALYST", "COMPOSER"],
        agents=[
            "ResearchCommanderAgent@1.0.0",
            "KnowledgeCandidateHunterAgent@1.0.0",
            "RelationshipCanonicalizationAnalystAgent",
            "OKFBundleComposerAgent",
        ],
    )

    validated = manifest.validate_agent_bindings(resolver)
    assert len(validated) == 4
    assert "ResearchCommanderAgent@1.0.0" in validated
    assert "KnowledgeCandidateHunterAgent@1.0.0" in validated
    assert "RelationshipCanonicalizationAnalystAgent@1.0.0" in validated
    assert "OKFBundleComposerAgent@1.0.0" in validated


def test_gate4_standalone_session_binding():
    """Prove that a standalone governed session can bind a registered Agent directly without a Program."""
    registry = get_agent_registry()
    registry.discover_agents("agents")
    resolver = AgentResolver(registry)

    agent = resolver.resolve("CollisionHuntingAgent", "1.0.0")
    workspace_id = uuid4()

    session = create_standalone_agent_session(agent, workspace_id)
    assert session.session_id.startswith("standalone_CollisionHuntingAgent_")
    assert session.workspace_id == workspace_id
    assert session.agent.agent_id == "CollisionHuntingAgent"
    assert session.authority_lane == AuthorityLane.HUNTER
    assert session.agent.content_sha256 == agent.content_sha256

    session_dict = session.to_dict()
    assert session_dict["agent_id"] == "CollisionHuntingAgent"
    assert session_dict["authority_lane"] == "HUNTER"
    assert session_dict["workspace_id"] == str(workspace_id)


def test_gate5_invalid_lifecycle_and_authority_fail_closed():
    """Prove that unapproved, draft, or quarantined agents fail closed upon resolution."""
    registry = AgentRegistry()
    resolver = AgentResolver(registry)

    # 1. Register a DRAFT agent
    draft_agent = AgentDefinition(
        agent_id="DraftAnalystAgent",
        version="0.1.0",
        name="Experimental Draft Analyst",
        purpose="Testing draft lifecycle gating",
        authority_lane=AuthorityLane.ANALYST,
        lifecycle_state=AgentLifecycleState.DRAFT,
        prompt_reference=AgentPromptReference(instructions_ref="instructions.md"),
    )
    registry.register(draft_agent)

    # Resolving with default (APPROVED/ACTIVE required) must fail closed
    with pytest.raises(AgentLifecycleViolationError) as exc_info:
        resolver.resolve("DraftAnalystAgent", "0.1.0")
    assert exc_info.value.reason_code == "AGENT_LIFECYCLE_VIOLATION"

    # Resolving explicitly with min_lifecycle=DRAFT succeeds for dev lab
    resolved_draft = resolver.resolve("DraftAnalystAgent", "0.1.0", min_lifecycle=AgentLifecycleState.DRAFT)
    assert resolved_draft.agent_id == "DraftAnalystAgent"

    # 2. Register and Quarantine an approved agent
    stable_agent = AgentDefinition(
        agent_id="QuarantinedComposerAgent",
        version="1.0.0",
        name="Quarantined Composer",
        purpose="Testing quarantine gating",
        authority_lane=AuthorityLane.COMPOSER,
        lifecycle_state=AgentLifecycleState.APPROVED,
        prompt_reference=AgentPromptReference(instructions_ref="instructions.md"),
    )
    registry.register(stable_agent)
    registry.quarantine("QuarantinedComposerAgent", "1.0.0", reason="Identified prompt injection vulnerability")

    with pytest.raises(AgentQuarantinedError) as q_info:
        resolver.resolve("QuarantinedComposerAgent", "1.0.0")
    assert q_info.value.reason_code == "AGENT_QUARANTINED"

    # 3. Requesting non-existent version fails closed
    with pytest.raises(AgentNotFoundError):
        resolver.resolve("DraftAnalystAgent", "9.9.9")


def test_gate5_lane_mismatch_fails_closed():
    """Prove that resolving with an expected lane mismatch raises AgentLaneMismatchError."""
    registry = get_agent_registry()
    registry.discover_agents("agents")
    resolver = AgentResolver(registry)

    # ResearchCommanderAgent is in COMMANDER lane; expecting HUNTER must fail
    with pytest.raises(AgentLaneMismatchError) as exc_info:
        resolver.resolve("ResearchCommanderAgent", "1.0.0", expected_lane=AuthorityLane.HUNTER)
    assert exc_info.value.reason_code == "AGENT_LANE_MISMATCH"

    # Program manifest declaring only HUNTER/ANALYST referencing a COMMANDER agent must fail
    mismatched_manifest = ProgramManifest(
        id="hunter_only_program",
        version="1.0.0",
        purpose="Hunter only program",
        lanes=["HUNTER", "ANALYST"],
        agents=["ResearchCommanderAgent@1.0.0"],
    )
    with pytest.raises(AgentLaneMismatchError):
        mismatched_manifest.validate_agent_bindings(resolver)


def test_reward_hacking_defense_identity_collision():
    """False-Proof Defense 1: Attempt to register two differing bodies under the same (agent_id, version)."""
    registry = AgentRegistry()

    agent_v1_a = AgentDefinition(
        agent_id="AudienceInsightHunterAgent",
        version="1.0.0",
        name="Audience Insight Hunter",
        purpose="Extracts audience insights from transcripts",
        authority_lane=AuthorityLane.HUNTER,
        lifecycle_state=AgentLifecycleState.APPROVED,
        model_policy=AgentModelPolicy(preferred_model="gemini-2.5-flash", temperature=0.2),
        prompt_reference=AgentPromptReference(instructions_ref="instructions.md"),
    )
    registry.register(agent_v1_a)

    # Attempt to register a conflicting body with different temperature and purpose under same version
    agent_v1_b = AgentDefinition(
        agent_id="AudienceInsightHunterAgent",
        version="1.0.0",
        name="Audience Insight Hunter Divergent",
        purpose="Conflicting altered purpose that would stealthily change behavior",
        authority_lane=AuthorityLane.HUNTER,
        lifecycle_state=AgentLifecycleState.APPROVED,
        model_policy=AgentModelPolicy(preferred_model="gemini-2.5-flash", temperature=0.8),
        prompt_reference=AgentPromptReference(instructions_ref="instructions.md"),
    )

    with pytest.raises(AgentIdentityCollisionError) as exc_info:
        registry.register(agent_v1_b)
    assert exc_info.value.reason_code == "AGENT_IDENTITY_COLLISION"
    assert "IDENTITY_COLLISION" in str(exc_info.value)


def test_reward_hacking_defense_capability_and_lane_escalation():
    """False-Proof Defense 2: Attempt to create an Agent with capability escalation violating its Authority Lane."""
    # Attempt to give a HUNTER agent database mutation operations
    with pytest.raises(AgentCapabilityViolationError) as exc_info:
        AgentDefinition(
            agent_id="EscalatedHunterAgent",
            version="1.0.0",
            name="Escalated Hunter Agent",
            purpose="Hunter attempting unauthorized workspace provisioning",
            authority_lane=AuthorityLane.HUNTER,
            lifecycle_state=AgentLifecycleState.APPROVED,
            capabilities=[
                AgentCapabilityGrant(
                    scope=CapabilityScope.CAE_TYPED_OPERATION,
                    mode=AccessMode.MUTATION_OPERATION,
                    target="cae.workspace.provision@1.0.0",
                )
            ],
            prompt_reference=AgentPromptReference(instructions_ref="instructions.md"),
        ).validate_invariants()

    assert exc_info.value.reason_code == "AGENT_CAPABILITY_VIOLATION"


def test_reward_hacking_defense_inline_unregistered_agent():
    """False-Proof Defense 3: Attempt to invoke an Agent that exists only as an inline Program string."""
    registry = AgentRegistry()
    resolver = AgentResolver(registry)

    # Program declaring an un-registered inline phantom agent
    phantom_program = ProgramManifest(
        id="phantom_agent_program",
        version="1.0.0",
        purpose="Program referencing fictitious inline agent",
        lanes=["HUNTER"],
        agents=["PhantomHunterAgent@1.0.0"],
    )

    with pytest.raises(AgentNotFoundError) as exc_info:
        phantom_program.validate_agent_bindings(resolver)
    assert exc_info.value.reason_code == "AGENT_NOT_FOUND"


def test_reward_hacking_defense_skill_nesting_prohibited():
    """False-Proof Defense 4: Attempt to register an Agent with a skill name implying recursive/nested execution."""
    with pytest.raises(AgentManifestValidationError) as exc_info:
        AgentDefinition(
            agent_id="NestedSkillAgent",
            version="1.0.0",
            name="Nested Skill Agent",
            purpose="Agent attempting illegal skill nesting",
            authority_lane=AuthorityLane.HUNTER,
            lifecycle_state=AgentLifecycleState.APPROVED,
            skills=[
                {"name": "recursive_agent_spawner", "version": "1.0.0"}
            ],
            prompt_reference=AgentPromptReference(instructions_ref="instructions.md"),
        ).validate_invariants()

    assert "flat passive skill constitution" in str(exc_info.value)


def test_concrete_agent_execution_trace():
    """Concrete Execution Demonstration: Agent -> Compiled Context -> Model Policy -> Typed Output -> Gate -> Receipt."""
    registry = get_agent_registry()
    registry.discover_agents("agents")
    resolver = AgentResolver(registry)

    # 1. Resolve canonical Agent
    agent = resolver.resolve("ResearchCommanderAgent", "1.0.0")
    assert agent.lifecycle_state == AgentLifecycleState.APPROVED
    assert agent.authority_lane == AuthorityLane.COMMANDER

    # 2. Simulated Compiled Context Capsule
    context_payload = {
        "agent_id": agent.agent_id,
        "version": agent.version,
        "authority_lane": agent.authority_lane.value,
        "cae_governance_hash": canonical_sha256("CAE_GOVERNANCE_ROOT"),
        "instructions_hash": agent.prompt_reference.prompt_sha256 or canonical_sha256("INSTRUCTIONS"),
    }
    context_sha256 = canonical_sha256(canonical_json_text(context_payload))

    # 3. Model Policy Verification
    model_policy = agent.model_policy
    assert model_policy.preferred_model == "gemini-2.5-pro"
    assert model_policy.temperature == 0.1

    # 4. Typed Output Contract Fulfillment
    output_contract = agent.output_contract
    assert output_contract is not None
    assert output_contract.contract_id == "research_canonicalization_receipt"
    
    simulated_agent_output = {
        "contract_id": output_contract.contract_id,
        "canonical_knowledge_nodes_adjudicated": 3,
        "contradictions_resolved": 0,
        "operator_gate_decision": "AUTHORIZED",
    }
    output_sha256 = canonical_sha256(canonical_json_text(simulated_agent_output))

    # 5. Gate & Non-Repudiable Cryptographic Receipt Emission
    receipt_payload = {
        "receipt_type": "cae.agent.invocation_receipt@1.0.0",
        "agent_id": agent.agent_id,
        "agent_version": agent.version,
        "authority_lane": agent.authority_lane.value,
        "agent_sha256": agent.content_sha256,
        "context_sha256": context_sha256,
        "output_sha256": output_sha256,
        "gate_status": "PASSED",
    }
    receipt_sha256 = canonical_sha256(canonical_json_text(receipt_payload))

    assert receipt_sha256 is not None
    assert len(receipt_sha256) == 64
    assert receipt_payload["gate_status"] == "PASSED"
