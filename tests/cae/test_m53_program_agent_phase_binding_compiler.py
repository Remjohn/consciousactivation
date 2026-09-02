"""Comprehensive Test Suite for CAE Mandate M53: Program -> Agent -> Phase Binding Compiler.

Governed by:
- 01_AGENT_EXECUTION/M53_program_agent_phase_binding_compiler.md
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md

Verifies:
- Gate 1: Every Agent-owned workflow node resolves exactly one Agent.
- Gate 2: Lane, Skill, tool, and contract compatibility is validated.
- Gate 3: Missing Agent or ambiguous mapping fails closed.
- Gate 4: Runtime node stores binding identity and cryptographic SHA-256 hash.
- Gate 5: Evidence links directly to the Program manifest.
- False-Proof Defense 1: Renamed or removed agent raises UnresolvedAgentAssignmentError.
- False-Proof Defense 2: Lane mismatch raises LaneBindingMismatchError.
- False-Proof Defense 3: Incompatible skill requirement raises IncompatibleSkillBindingError.
- False-Proof Defense 4: Missing output contract raises UnresolvedOutputContractError.
- Proof Matrix: Concrete verification for Research Canonicalization Program & Script Program.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List
from uuid import UUID, uuid4

import pytest

from ca_contracts import canonical_json_text, canonical_sha256
from ca_runtime import (
    AccessMode,
    AgentCapabilityGrant,
    AgentDefinition,
    AgentLifecycleState,
    AgentModelPolicy,
    AgentOutputContract,
    AgentPromptReference,
    AgentRegistry,
    AmbiguousAgentAssignmentError,
    AuthorityLane,
    CapabilityScope,
    CompiledAgentNodeAssignment,
    IncompatibleSkillBindingError,
    IncompatibleToolBindingError,
    LaneBindingMismatchError,
    ProgramAgentBindingCompiler,
    ProgramAgentBindingError,
    ProgramAgentPhaseBindingManifest,
    ProgramManifest,
    UnresolvedAgentAssignmentError,
    UnresolvedOutputContractError,
)


@pytest.fixture
def populated_agent_registry() -> AgentRegistry:
    """Populates an AgentRegistry with canonical agents across all 4 Authority Lanes."""
    registry = AgentRegistry()

    # 1. Hunter Agent
    hunter = AgentDefinition(
        agent_id="KnowledgeCandidateHunterAgent",
        version="1.0.0",
        name="Knowledge Candidate Hunter Agent",
        purpose="Extracts candidate assertions and evidence segments from raw research sources.",
        authority_lane=AuthorityLane.HUNTER,
        lifecycle_state=AgentLifecycleState.APPROVED,
        tools=["source_provenance_verifier", "tool:signal-reader"],
        capabilities=[
            AgentCapabilityGrant(
                scope=CapabilityScope.POSTGRES_STORAGE,
                mode=AccessMode.READ_ONLY,
                target="cae.research_signals",
            )
        ],
        output_contract=AgentOutputContract(
            contract_id="contract:research-candidate:v1",
            output_type="JSON",
            description="Extracted knowledge candidates with verbatim evidence",
        ),
    )
    registry.register(hunter)

    # 2. Analyst Agent
    analyst = AgentDefinition(
        agent_id="RelationshipCanonicalizationAnalystAgent",
        version="1.0.0",
        name="Relationship Canonicalization Analyst Agent",
        purpose="Classifies relationships and resolves contradictions across knowledge candidates.",
        authority_lane=AuthorityLane.ANALYST,
        lifecycle_state=AgentLifecycleState.APPROVED,
        tools=["semantic_similarity_analyzer"],
        capabilities=[
            AgentCapabilityGrant(
                scope=CapabilityScope.POSTGRES_STORAGE,
                mode=AccessMode.READ_ONLY,
                target="cae.knowledge_graph",
            )
        ],
        output_contract=AgentOutputContract(
            contract_id="contract:canonical-relationship:v1",
            output_type="JSON",
            description="Classified relationship edges with confidence scoring",
        ),
    )
    registry.register(analyst)

    # 3. Composer Agent
    composer = AgentDefinition(
        agent_id="OKFBundleComposerAgent",
        version="1.0.0",
        name="OKF Bundle Composer Agent",
        purpose="Projects canonical knowledge graph nodes into structured Open Knowledge Foundation bundles.",
        authority_lane=AuthorityLane.COMPOSER,
        lifecycle_state=AgentLifecycleState.APPROVED,
        tools=["okf_markdown_renderer"],
        capabilities=[
            AgentCapabilityGrant(
                scope=CapabilityScope.FILESYSTEM,
                mode=AccessMode.READ_WRITE,
                target="workspace/okf_bundles",
            )
        ],
        output_contract=AgentOutputContract(
            contract_id="contract:okf-bundle:v1",
            output_type="JSON",
            description="Composed OKF bundle artifact with markdown projections",
        ),
    )
    registry.register(composer)

    # 4. Commander Agent
    commander = AgentDefinition(
        agent_id="ResearchCommanderAgent",
        version="1.0.0",
        name="Research Commander Agent",
        purpose="Supervises knowledge canonicalization and prepares operator adjudication gates.",
        authority_lane=AuthorityLane.COMMANDER,
        lifecycle_state=AgentLifecycleState.APPROVED,
        tools=["source_provenance_verifier", "semantic_similarity_analyzer"],
        capabilities=[
            AgentCapabilityGrant(
                scope=CapabilityScope.CAE_TYPED_OPERATION,
                mode=AccessMode.MUTATION_OPERATION,
                target="cae.research.commit_knowledge@1.0.0",
                approval_required=True,
            )
        ],
        output_contract=AgentOutputContract(
            contract_id="contract:research-adjudication-brief:v1",
            output_type="JSON",
            description="Adjudication brief presented to human operator",
        ),
    )
    registry.register(commander)

    # Script Program Agents
    script_hunter = AgentDefinition(
        agent_id="ScriptContextHunter",
        version="1.0.0",
        name="Script Context Hunter",
        purpose="Gathers storyboard and voice DNA context for script authoring.",
        authority_lane=AuthorityLane.HUNTER,
        lifecycle_state=AgentLifecycleState.APPROVED,
        tools=["quote_integrity_validator"],
        output_contract=AgentOutputContract(contract_id="contract:script-context:v1", output_type="JSON"),
    )
    registry.register(script_hunter)

    script_analyst = AgentDefinition(
        agent_id="SemanticQAScriptAnalyst",
        version="1.0.0",
        name="Semantic QA Script Analyst",
        purpose="Evaluates script candidates against semantic QA metrics.",
        authority_lane=AuthorityLane.ANALYST,
        lifecycle_state=AgentLifecycleState.APPROVED,
        tools=["voice_dna_checker"],
        output_contract=AgentOutputContract(contract_id="contract:script-qa:v1", output_type="JSON"),
    )
    registry.register(script_analyst)

    script_composer = AgentDefinition(
        agent_id="ScriptComposerAgent",
        version="1.0.0",
        name="Script Composer Agent",
        purpose="Authors full script proposals bound to authenticated evidence.",
        authority_lane=AuthorityLane.COMPOSER,
        lifecycle_state=AgentLifecycleState.APPROVED,
        tools=["quote_integrity_validator"],
        output_contract=AgentOutputContract(contract_id="contract:script-proposal:v1", output_type="JSON"),
    )
    registry.register(script_composer)

    script_commander = AgentDefinition(
        agent_id="ScriptCommanderSupervisor",
        version="1.0.0",
        name="Script Commander Supervisor",
        purpose="Oversees script authoring pipeline and operator approvals.",
        authority_lane=AuthorityLane.COMMANDER,
        lifecycle_state=AgentLifecycleState.APPROVED,
        tools=["quote_integrity_validator"],
        output_contract=AgentOutputContract(contract_id="contract:script-approval:v1", output_type="JSON"),
    )
    registry.register(script_commander)

    return registry


@pytest.fixture
def research_program_manifest() -> Dict[str, Any]:
    return {
        "id": "research_canonicalization_program",
        "version": "1.0.0",
        "status": "ACTIVE",
        "purpose": "Transforms raw research sources into curated OKF-compatible canonical knowledge nodes.",
        "state_machine": "RESEARCH_CANONICALIZATION_STATE_MACHINE_V1",
        "lanes": ["COMMANDER", "HUNTER", "ANALYST", "COMPOSER"],
        "agents": [
            "ResearchCommanderAgent",
            "KnowledgeCandidateHunterAgent",
            "RelationshipCanonicalizationAnalystAgent",
            "OKFBundleComposerAgent",
        ],
        "skills": [
            {"name": "knowledge_candidate_extractor", "path": "skills/knowledge_candidate_extractor/SKILL.md", "version": "1.0.0"},
            {"name": "canonical_relationship_classifier", "path": "skills/canonical_relationship_classifier/SKILL.md", "version": "1.0.0"},
            {"name": "okf_bundle_projector", "path": "skills/okf_bundle_projector/SKILL.md", "version": "1.0.0"},
        ],
        "tools": [
            "source_provenance_verifier",
            "semantic_similarity_analyzer",
            "okf_markdown_renderer",
        ],
    }


@pytest.fixture
def research_workflow_nodes() -> List[Dict[str, Any]]:
    return [
        {
            "node_id": "node_candidate_extraction",
            "phase_id": "PHASE_CANDIDATE_EXTRACTION",
            "phase_order": 1,
            "actor_kind": "GOVERNED_AGENT_NODE",
            "role": "HUNTER",
            "agent_id": "KnowledgeCandidateHunterAgent",
            "tool_ids": ["source_provenance_verifier"],
            "skills": ["knowledge_candidate_extractor"],
            "output_contracts": ["contract:research-candidate:v1"],
        },
        {
            "node_id": "node_relationship_canonicalization",
            "phase_id": "PHASE_RELATIONSHIP_CANONICALIZATION",
            "phase_order": 2,
            "actor_kind": "GOVERNED_AGENT_NODE",
            "role": "ANALYST",
            "agent_id": "RelationshipCanonicalizationAnalystAgent",
            "tool_ids": ["semantic_similarity_analyzer"],
            "skills": ["canonical_relationship_classifier"],
            "output_contracts": ["contract:canonical-relationship:v1"],
        },
        {
            "node_id": "node_okf_projection",
            "phase_id": "PHASE_OKF_PROJECTION",
            "phase_order": 3,
            "actor_kind": "GOVERNED_AGENT_NODE",
            "role": "COMPOSER",
            "agent_id": "OKFBundleComposerAgent",
            "tool_ids": ["okf_markdown_renderer"],
            "skills": ["okf_bundle_projector"],
            "output_contracts": ["contract:okf-bundle:v1"],
        },
        {
            "node_id": "node_adjudication_supervision",
            "phase_id": "PHASE_ADJUDICATION_SUPERVISION",
            "phase_order": 4,
            "actor_kind": "GOVERNED_AGENT_NODE",
            "role": "COMMANDER",
            "agent_id": "ResearchCommanderAgent",
            "tool_ids": ["source_provenance_verifier"],
            "skills": [],
            "output_contracts": ["contract:research-adjudication-brief:v1"],
        },
    ]


# ---------------------------------------------------------------------------
# Acceptance Gate Tests
# ---------------------------------------------------------------------------

def test_gate1_every_agent_owned_node_resolves_exactly_one_agent(
    research_program_manifest: Dict[str, Any],
    research_workflow_nodes: List[Dict[str, Any]],
    populated_agent_registry: AgentRegistry,
):
    """Gate 1: Every Agent-owned node resolves to exactly one valid AgentDefinition."""
    manifest = ProgramAgentBindingCompiler.compile(
        program_manifest=research_program_manifest,
        workflow_nodes=research_workflow_nodes,
        agent_registry=populated_agent_registry,
    )

    assert isinstance(manifest, ProgramAgentPhaseBindingManifest)
    assert len(manifest.node_assignments) == 4

    assigned_agent_ids = [a.agent_id for a in manifest.node_assignments]
    assert assigned_agent_ids == [
        "KnowledgeCandidateHunterAgent",
        "RelationshipCanonicalizationAnalystAgent",
        "OKFBundleComposerAgent",
        "ResearchCommanderAgent",
    ]


def test_gate2_lane_skill_tool_contract_compatibility_validated(
    research_program_manifest: Dict[str, Any],
    research_workflow_nodes: List[Dict[str, Any]],
    populated_agent_registry: AgentRegistry,
):
    """Gate 2: Lane parity, skill availability, tool permissions, and output contracts are verified."""
    manifest = ProgramAgentBindingCompiler.compile(
        program_manifest=research_program_manifest,
        workflow_nodes=research_workflow_nodes,
        agent_registry=populated_agent_registry,
    )

    hunter_assignment = manifest.get_assignment_for_node("node_candidate_extraction")
    assert hunter_assignment is not None
    assert hunter_assignment.lane == AuthorityLane.HUNTER
    assert hunter_assignment.role == "HUNTER"
    assert "source_provenance_verifier" in hunter_assignment.bound_tools
    assert "contract:research-candidate:v1" in hunter_assignment.output_contracts

    analyst_assignment = manifest.get_assignment_for_node("node_relationship_canonicalization")
    assert analyst_assignment is not None
    assert analyst_assignment.lane == AuthorityLane.ANALYST
    assert analyst_assignment.role == "ANALYST"
    assert "semantic_similarity_analyzer" in analyst_assignment.bound_tools


def test_gate3_missing_agent_or_ambiguous_mapping_fails_closed(
    research_program_manifest: Dict[str, Any],
    populated_agent_registry: AgentRegistry,
):
    """Gate 3: Missing Agent or ambiguous multi-match fails closed."""
    # 1. Missing Agent in Registry
    missing_nodes = [
        {
            "node_id": "node_ghost_hunter",
            "actor_kind": "GOVERNED_AGENT_NODE",
            "role": "HUNTER",
            "agent_id": "NonExistentGhostHunterAgent",
            "output_contracts": ["contract:test:v1"],
        }
    ]
    with pytest.raises(UnresolvedAgentAssignmentError) as exc_info:
        ProgramAgentBindingCompiler.compile(
            program_manifest=research_program_manifest,
            workflow_nodes=missing_nodes,
            agent_registry=populated_agent_registry,
        )
    assert exc_info.value.reason_code == "UNRESOLVED_AGENT_ASSIGNMENT"

    # 2. Ambiguous Mapping (multiple agents match role and no explicit agent_id specified)
    manifest_with_duplicates = dict(research_program_manifest)
    manifest_with_duplicates["agents"] = [
        "KnowledgeCandidateHunterAgent",
        "ScriptContextHunter",  # Second Hunter agent
    ]
    ambiguous_nodes = [
        {
            "node_id": "node_ambiguous_hunter",
            "actor_kind": "GOVERNED_AGENT_NODE",
            "role": "HUNTER",
            # agent_id omitted -> causes ambiguous resolution
            "output_contracts": ["contract:test:v1"],
        }
    ]
    with pytest.raises(AmbiguousAgentAssignmentError) as exc_info2:
        ProgramAgentBindingCompiler.compile(
            program_manifest=manifest_with_duplicates,
            workflow_nodes=ambiguous_nodes,
            agent_registry=populated_agent_registry,
        )
    assert exc_info2.value.reason_code == "AMBIGUOUS_AGENT_ASSIGNMENT"


def test_gate4_runtime_node_stores_binding_identity_and_hash(
    research_program_manifest: Dict[str, Any],
    research_workflow_nodes: List[Dict[str, Any]],
    populated_agent_registry: AgentRegistry,
):
    """Gate 4: Each node assignment captures agent content SHA-256 and deterministic binding hash."""
    manifest = ProgramAgentBindingCompiler.compile(
        program_manifest=research_program_manifest,
        workflow_nodes=research_workflow_nodes,
        agent_registry=populated_agent_registry,
    )

    for assignment in manifest.node_assignments:
        assert len(assignment.agent_content_sha256) == 64
        assert len(assignment.binding_sha256) == 64
        # Verify canonical dict serialization
        c_dict = assignment.canonical_dict()
        assert c_dict["binding_sha256"] == assignment.binding_sha256
        assert c_dict["agent_content_sha256"] == assignment.agent_content_sha256

    assert len(manifest.manifest_binding_sha256) == 64


def test_gate5_evidence_links_to_program_manifest(
    research_program_manifest: Dict[str, Any],
    research_workflow_nodes: List[Dict[str, Any]],
    populated_agent_registry: AgentRegistry,
):
    """Gate 5: Manifest binding records program ID, version, and program manifest digest."""
    manifest = ProgramAgentBindingCompiler.compile(
        program_manifest=research_program_manifest,
        workflow_nodes=research_workflow_nodes,
        agent_registry=populated_agent_registry,
    )

    assert manifest.program_id == "research_canonicalization_program"
    assert manifest.program_version == "1.0.0"
    assert manifest.state_machine_id == "RESEARCH_CANONICALIZATION_STATE_MACHINE_V1"
    assert len(manifest.program_manifest_sha256) == 64


# ---------------------------------------------------------------------------
# False-Proof & Reward-Hacking Defenses
# ---------------------------------------------------------------------------

def test_false_proof_defense_agent_removed_from_manifest(
    research_program_manifest: Dict[str, Any],
    research_workflow_nodes: List[Dict[str, Any]],
    populated_agent_registry: AgentRegistry,
):
    """False-Proof Defense 1: Removing an agent from the program manifest inventory fails closed."""
    tampered_manifest = dict(research_program_manifest)
    tampered_manifest["agents"] = [
        # Removed KnowledgeCandidateHunterAgent
        "RelationshipCanonicalizationAnalystAgent",
        "OKFBundleComposerAgent",
        "ResearchCommanderAgent",
    ]

    with pytest.raises(UnresolvedAgentAssignmentError) as exc_info:
        ProgramAgentBindingCompiler.compile(
            program_manifest=tampered_manifest,
            workflow_nodes=research_workflow_nodes,
            agent_registry=populated_agent_registry,
        )

    assert exc_info.value.reason_code == "UNRESOLVED_AGENT_ASSIGNMENT"


def test_false_proof_defense_authority_lane_mismatch(
    research_program_manifest: Dict[str, Any],
    populated_agent_registry: AgentRegistry,
):
    """False-Proof Defense 2: Assigning a COMPOSER Agent to a HUNTER node fails closed."""
    mismatched_nodes = [
        {
            "node_id": "node_illegal_lane_assignment",
            "actor_kind": "GOVERNED_AGENT_NODE",
            "role": "HUNTER",
            "agent_id": "OKFBundleComposerAgent",  # Composer agent in Hunter node!
            "output_contracts": ["contract:test:v1"],
        }
    ]

    with pytest.raises(LaneBindingMismatchError) as exc_info:
        ProgramAgentBindingCompiler.compile(
            program_manifest=research_program_manifest,
            workflow_nodes=mismatched_nodes,
            agent_registry=populated_agent_registry,
        )

    assert exc_info.value.reason_code == "LANE_BINDING_MISMATCH"


def test_false_proof_defense_incompatible_skill_binding(
    research_program_manifest: Dict[str, Any],
    populated_agent_registry: AgentRegistry,
):
    """False-Proof Defense 3: Node requiring an undeclared skill fails closed."""
    illegal_skill_nodes = [
        {
            "node_id": "node_unauthorized_skill",
            "actor_kind": "GOVERNED_AGENT_NODE",
            "role": "HUNTER",
            "agent_id": "KnowledgeCandidateHunterAgent",
            "skills": ["unauthorized_autonomous_mutation_skill"],  # Not in agent or manifest!
            "output_contracts": ["contract:test:v1"],
        }
    ]

    with pytest.raises(IncompatibleSkillBindingError) as exc_info:
        ProgramAgentBindingCompiler.compile(
            program_manifest=research_program_manifest,
            workflow_nodes=illegal_skill_nodes,
            agent_registry=populated_agent_registry,
        )

    assert exc_info.value.reason_code == "INCOMPATIBLE_SKILL_BINDING"


def test_false_proof_defense_unresolved_output_contract(
    research_program_manifest: Dict[str, Any],
    populated_agent_registry: AgentRegistry,
):
    """False-Proof Defense 4: Agent node without resolved output contract fails closed."""
    # Register an agent with no output contract
    raw_agent = AgentDefinition(
        agent_id="UncontractedHunterAgent",
        version="1.0.0",
        name="Uncontracted Hunter Agent",
        purpose="Hunter without declared output contract.",
        authority_lane=AuthorityLane.HUNTER,
        lifecycle_state=AgentLifecycleState.APPROVED,
        output_contract=None,
    )
    populated_agent_registry.register(raw_agent)

    manifest_dict = dict(research_program_manifest)
    manifest_dict["agents"] = list(manifest_dict["agents"]) + ["UncontractedHunterAgent"]

    uncontracted_nodes = [
        {
            "node_id": "node_uncontracted_output",
            "actor_kind": "GOVERNED_AGENT_NODE",
            "role": "HUNTER",
            "agent_id": "UncontractedHunterAgent",
            "output_contracts": [],  # Empty on node, None on agent!
        }
    ]

    with pytest.raises(UnresolvedOutputContractError) as exc_info:
        ProgramAgentBindingCompiler.compile(
            program_manifest=manifest_dict,
            workflow_nodes=uncontracted_nodes,
            agent_registry=populated_agent_registry,
        )

    assert exc_info.value.reason_code == "UNRESOLVED_OUTPUT_CONTRACT"


# ---------------------------------------------------------------------------
# Multi-Program Proof Matrix Demonstration
# ---------------------------------------------------------------------------

def test_proof_matrix_research_canonicalization_and_script_programs(
    research_program_manifest: Dict[str, Any],
    research_workflow_nodes: List[Dict[str, Any]],
    populated_agent_registry: AgentRegistry,
):
    """Proof Matrix: Validates complete Program -> Agent -> Phase binding for multiple canonical programs."""
    # 1. Compile Research Canonicalization Program Binding
    research_binding = ProgramAgentBindingCompiler.compile(
        program_manifest=research_program_manifest,
        workflow_nodes=research_workflow_nodes,
        agent_registry=populated_agent_registry,
    )

    assert research_binding.program_id == "research_canonicalization_program"
    assert len(research_binding.node_assignments) == 4
    assert len(research_binding.list_assignments_for_lane(AuthorityLane.HUNTER)) == 1
    assert len(research_binding.list_assignments_for_lane(AuthorityLane.ANALYST)) == 1
    assert len(research_binding.list_assignments_for_lane(AuthorityLane.COMPOSER)) == 1
    assert len(research_binding.list_assignments_for_lane(AuthorityLane.COMMANDER)) == 1

    # 2. Compile Script Program Binding
    script_manifest = {
        "id": "script_program",
        "version": "1.0.0",
        "status": "ACTIVE",
        "purpose": "Governed program runtime for script authoring.",
        "state_machine": "SCRIPT_STATE_MACHINE_V1",
        "lanes": ["HUNTER", "ANALYST", "COMPOSER", "COMMANDER"],
        "agents": [
            "ScriptContextHunter",
            "SemanticQAScriptAnalyst",
            "ScriptComposerAgent",
            "ScriptCommanderSupervisor",
        ],
        "skills": [
            {"name": "script_generation", "path": "skills/script_generation/SKILL.md", "version": "1.0.0"}
        ],
        "tools": ["quote_integrity_validator", "voice_dna_checker"],
    }

    script_nodes = [
        {
            "node_id": "node_script_context",
            "phase_id": "PHASE_CONTEXT_GATHERING",
            "phase_order": 1,
            "actor_kind": "GOVERNED_AGENT_NODE",
            "role": "HUNTER",
            "agent_id": "ScriptContextHunter",
            "tool_ids": ["quote_integrity_validator"],
            "output_contracts": ["contract:script-context:v1"],
        },
        {
            "node_id": "node_script_composition",
            "phase_id": "PHASE_SCRIPT_COMPOSITION",
            "phase_order": 2,
            "actor_kind": "GOVERNED_AGENT_NODE",
            "role": "COMPOSER",
            "agent_id": "ScriptComposerAgent",
            "tool_ids": ["quote_integrity_validator"],
            "skills": ["script_generation"],
            "output_contracts": ["contract:script-proposal:v1"],
        },
        {
            "node_id": "node_semantic_qa",
            "phase_id": "PHASE_SEMANTIC_QA",
            "phase_order": 3,
            "actor_kind": "GOVERNED_AGENT_NODE",
            "role": "ANALYST",
            "agent_id": "SemanticQAScriptAnalyst",
            "tool_ids": ["voice_dna_checker"],
            "output_contracts": ["contract:script-qa:v1"],
        },
        {
            "node_id": "node_script_approval",
            "phase_id": "PHASE_SCRIPT_APPROVAL",
            "phase_order": 4,
            "actor_kind": "GOVERNED_AGENT_NODE",
            "role": "COMMANDER",
            "agent_id": "ScriptCommanderSupervisor",
            "tool_ids": ["quote_integrity_validator"],
            "output_contracts": ["contract:script-approval:v1"],
        },
    ]

    script_binding = ProgramAgentBindingCompiler.compile(
        program_manifest=script_manifest,
        workflow_nodes=script_nodes,
        agent_registry=populated_agent_registry,
    )

    assert script_binding.program_id == "script_program"
    assert len(script_binding.node_assignments) == 4
    assert script_binding.get_assignment_for_phase("PHASE_SCRIPT_COMPOSITION").agent_id == "ScriptComposerAgent"
    assert script_binding.get_assignment_for_phase("PHASE_SEMANTIC_QA").agent_id == "SemanticQAScriptAnalyst"
    assert script_binding.manifest_binding_sha256 != ""
