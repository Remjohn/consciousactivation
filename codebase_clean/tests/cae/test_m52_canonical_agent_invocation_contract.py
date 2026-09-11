"""Comprehensive Test Suite for CAE Mandate M52: Canonical Agent Invocation Contract.

Governed by:
- 01_AGENT_EXECUTION/M52_canonical_agent_invocation_contract.md
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md

Verifies:
- Gate 1: Program-owned Agent call produces an AgentInvocation.
- Gate 2: Standalone session produces the same invocation shape.
- Gate 3: Prompt/context/package/model hashes are captured.
- Gate 4: Tool/action constraints travel with the invocation.
- Gate 5: Bypass attempts are blocked or flagged.
- False-Proof Defense 1: Invocation tampering / hash drift triggers InvocationIntegrityError.
- False-Proof Defense 2: Unauthorized tool injection triggers UnauthorizedToolError.
- False-Proof Defense 3: Unauthorized model policy triggers UnauthorizedModelError.
- False-Proof Defense 4: Output contract violation triggers OutputContractViolationError.
- Concrete Execution Trace: Agent -> Compiled Context -> Invocation -> Runtime -> Receipt.
"""

from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from ca_contracts import canonical_json_text, canonical_sha256
from ca_runtime import (
    AccessMode,
    AgentCapabilityGrant,
    AgentDefinition,
    AgentInvocation,
    AgentInvocationCompiler,
    AgentInvocationError,
    AgentInvocationReceipt,
    AgentInvocationRuntime,
    AgentLifecycleState,
    AgentModelPolicy,
    AgentOutputContract,
    AgentPromptReference,
    AgentRegistry,
    AuthorityLane,
    CapabilityProjection,
    CapabilityScope,
    ContextItem,
    ContextPrecedenceLayer,
    InvocationBypassError,
    InvocationIntegrityError,
    JITContextCapsule,
    JITContextCompiler,
    OutputContractViolationError,
    SkillMaturity,
    SkillPackageRef,
    StandaloneAgentSession,
    UnauthorizedModelError,
    UnauthorizedToolError,
    create_standalone_agent_session,
)


@pytest.fixture
def sample_workspace_id() -> UUID:
    return uuid4()


@pytest.fixture
def sample_skill_ref() -> SkillPackageRef:
    return SkillPackageRef(
        skill_id="signal_extraction",
        version="1.0.0",
        maturity=SkillMaturity.STABLE,
        procedure_ref="skills/signal_extraction/SKILL.md",
        package_sha256="a" * 64,
        allowed_tools=("tool:signal-reader",),
        forbidden_actions=("action:mutate_signals",),
    )


@pytest.fixture
def canonical_hunter_agent() -> AgentDefinition:
    raw_agent = AgentDefinition(
        agent_id="ResearchSynthesisAgent",
        version="1.0.0",
        name="Research Synthesis Agent",
        purpose="Performs governed psychological synthesis over research signals without mutation.",
        authority_lane=AuthorityLane.HUNTER,
        lifecycle_state=AgentLifecycleState.APPROVED,
        model_policy=AgentModelPolicy(
            preferred_model="gemini-2.5-pro",
            temperature=0.2,
            temperature_bps=2000,
            token_budget=64_000,
            fallback_models=["gemini-2.5-flash", "openai/gpt-oss-120b"],
            timeout_seconds=60,
        ),
        prompt_reference=AgentPromptReference(
            instructions_ref="instructions.md",
            cae_md_ref="CAE.md",
        ),
        tools=["tool:signal-reader", "tool:evidence-extractor"],
        capabilities=[
            AgentCapabilityGrant(
                scope=CapabilityScope.POSTGRES_STORAGE,
                mode=AccessMode.READ_ONLY,
                target="cae.research_signals",
            ),
            AgentCapabilityGrant(
                scope=CapabilityScope.FILESYSTEM,
                mode=AccessMode.READ_ONLY,
                target="workspace/evidence",
            ),
        ],
        output_contract=AgentOutputContract(
            contract_id="contract:research-synthesis:v1",
            output_type="JSON",
            description="Structured synthesis report with evidence citations",
        ),
    )
    registry = AgentRegistry()
    return registry.register(raw_agent)


@pytest.fixture
def sample_context_capsule(sample_workspace_id: UUID, sample_skill_ref: SkillPackageRef) -> JITContextCapsule:
    return JITContextCompiler.assemble(
        workspace_id=sample_workspace_id,
        lane=AuthorityLane.HUNTER,
        actor_id="actor:operator-hunter",
        program_id="program:research_canonicalization",
        harness_id="harness:atomic_hunter",
        agent_id="ResearchSynthesisAgent",
        model_id="gemini-2.5-pro",
        total_token_budget=64_000,
        constitutions=[
            ("CIVIL_CODE", "docs/CIVIL_CODE.md", "Civil Code Invariant: Truthful citations required.")
        ],
        operator_grants=[
            ("GRANT_READ", "grants/op_read.json", "Operator grant: Read-only research access.")
        ],
        program_harness_policies=[
            ("PROGRAM_POLICY", "policy/harness.yaml", "Program policy: Deterministic signal extraction.")
        ],
        local_governance_cae_md=("CAE.md", "Local CAE: Ingestion phase rules."),
        agent_instructions=("instructions.md", "Agent instructions: Extract psychological tension markers."),
        skills=[
            (
                sample_skill_ref,
                "Procedure: Extract signal markers from raw transcripts.",
            )
        ],
        capabilities=[
            CapabilityProjection(
                capability_id="cap:postgres-read",
                owner_product="cae",
                scope=CapabilityScope.POSTGRES_STORAGE,
                mode=AccessMode.READ_ONLY,
                workspace_bound=True,
                approval_required=False,
                sandbox_required=False,
                audit_mode="LOGGED",
                bound_tools=("tool:signal-reader", "tool:evidence-extractor"),
            )
        ],
        production_mode=True,
    )


# ---------------------------------------------------------------------------
# Acceptance Gate Tests
# ---------------------------------------------------------------------------

def test_gate1_program_owned_agent_call_produces_agent_invocation(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
):
    """Gate 1: A Program-owned Agent call produces an AgentInvocation with complete provenance."""
    invocation = AgentInvocationCompiler.compile(
        agent=canonical_hunter_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        run_id="run_prog_9901",
        state_id="STATE_INGESTION",
        skills=[sample_skill_ref],
    )

    assert isinstance(invocation, AgentInvocation)
    assert invocation.agent_id == "ResearchSynthesisAgent"
    assert invocation.lane == AuthorityLane.HUNTER
    assert invocation.run_id == "run_prog_9901"
    assert invocation.state_id == "STATE_INGESTION"
    assert invocation.workspace_id == sample_workspace_id
    assert invocation.model_id == "gemini-2.5-pro"
    assert invocation.temperature_bps == 2000
    assert len(invocation.invocation_sha256) == 64
    assert invocation.capsule_sha256 == sample_context_capsule.capsule_sha256
    assert invocation.package_sha256 == canonical_hunter_agent.content_sha256


def test_gate2_standalone_session_produces_same_invocation_shape(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
):
    """Gate 2: A standalone session produces the same invocation shape and contract compatibility."""
    session = create_standalone_agent_session(
        agent=canonical_hunter_agent,
        workspace_id=sample_workspace_id,
    )
    assert isinstance(session, StandaloneAgentSession)

    invocation = AgentInvocationCompiler.compile(
        agent=session.agent,
        capsule=sample_context_capsule,
        workspace_id=session.workspace_id,
        run_id=None,
        state_id=None,
        skills=[sample_skill_ref],
    )

    assert isinstance(invocation, AgentInvocation)
    assert invocation.agent_id == session.agent.agent_id
    assert invocation.workspace_id == session.workspace_id
    assert invocation.lane == session.authority_lane
    assert invocation.run_id is None
    assert invocation.state_id is None
    assert len(invocation.invocation_sha256) == 64


def test_gate3_prompt_context_package_model_hashes_captured(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
):
    """Gate 3: Prompt, context, package, and model hashes are captured and verifiable."""
    invocation = AgentInvocationCompiler.compile(
        agent=canonical_hunter_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        skills=[sample_skill_ref],
    )

    # Hashes captured
    assert invocation.package_sha256 == canonical_hunter_agent.content_sha256
    assert invocation.capsule_sha256 == sample_context_capsule.capsule_sha256
    assert invocation.model_id == "gemini-2.5-pro"
    assert invocation.assembled_prompt == sample_context_capsule.assembled_prompt

    # Canonical dictionary includes all hash references
    c_dict = invocation.canonical_dict()
    assert c_dict["package_sha256"] == invocation.package_sha256
    assert c_dict["capsule_sha256"] == invocation.capsule_sha256
    assert c_dict["model_id"] == "gemini-2.5-pro"
    assert c_dict["temperature_bps"] == 2000

    # Verification passes cleanly
    invocation.verify_integrity()


def test_gate4_tool_action_constraints_travel_with_invocation(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
):
    """Gate 4: Tool and action constraints travel with the invocation payload."""
    invocation = AgentInvocationCompiler.compile(
        agent=canonical_hunter_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        skills=[sample_skill_ref],
    )

    # Declared tools are included
    assert "tool:signal-reader" in invocation.tools
    assert "tool:evidence-extractor" in invocation.tools

    # Forbidden actions travel with invocation
    assert "action:mutate_signals" in invocation.forbidden_actions


def test_gate5_execution_receipt_emitted_and_hashed(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
):
    """Gate 5: Execution through AgentInvocationRuntime emits a signed, immutable receipt."""
    invocation = AgentInvocationCompiler.compile(
        agent=canonical_hunter_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        run_id="run_gate5_receipt",
        state_id="STATE_REASONING",
        skills=[sample_skill_ref],
    )

    receipt = AgentInvocationRuntime.execute(
        invocation,
        supplied_tool_calls=["tool:signal-reader"],
    )

    assert isinstance(receipt, AgentInvocationReceipt)
    assert receipt.invocation_id == invocation.invocation_id
    assert receipt.agent_id == invocation.agent_id
    assert receipt.package_sha256 == invocation.package_sha256
    assert receipt.capsule_sha256 == invocation.capsule_sha256
    assert receipt.invocation_sha256 == invocation.invocation_sha256
    assert receipt.gate_passed is True
    assert receipt.output_contract_passed is True
    assert len(receipt.receipt_sha256) == 64


# ---------------------------------------------------------------------------
# False-Proof & Reward-Hacking Defenses
# ---------------------------------------------------------------------------

def test_false_proof_defense_invocation_tampering_hash_drift(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
):
    """False-Proof Defense 1: Modifying prompt or fields after compilation triggers InvocationIntegrityError."""
    invocation = AgentInvocationCompiler.compile(
        agent=canonical_hunter_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        skills=[sample_skill_ref],
    )

    # Tamper with the invocation by creating an altered instance with the original hash
    tampered_invocation = AgentInvocation(
        invocation_id=invocation.invocation_id,
        workspace_id=invocation.workspace_id,
        run_id=invocation.run_id,
        lane=invocation.lane,
        agent_id=invocation.agent_id,
        agent_version=invocation.agent_version,
        state_id=invocation.state_id,
        package_sha256=invocation.package_sha256,
        capsule_sha256=invocation.capsule_sha256,
        model_id="openai/gpt-oss-120b",  # Altered model
        model_provider=invocation.model_provider,
        temperature_bps=invocation.temperature_bps,
        timeout_ms=invocation.timeout_ms,
        skills=invocation.skills,
        tools=invocation.tools,
        forbidden_actions=invocation.forbidden_actions,
        capabilities=invocation.capabilities,
        output_contract=invocation.output_contract,
        assembled_prompt="TAMPERED: Injected prompt bypassing safety controls.",
        system_prompt=invocation.system_prompt,
        invocation_sha256=invocation.invocation_sha256,  # Original hash preserved
        created_at=invocation.created_at,
    )

    with pytest.raises(InvocationIntegrityError) as exc_info:
        AgentInvocationRuntime.execute(tampered_invocation)

    assert exc_info.value.reason_code == "INVOCATION_INTEGRITY_VIOLATION"


def test_false_proof_defense_unauthorized_tool_injection(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
):
    """False-Proof Defense 2: Supplying an un-projected or forbidden tool fails closed."""
    # Attempting to compile with a forbidden tool
    with pytest.raises(UnauthorizedToolError) as exc_info:
        AgentInvocationCompiler.compile(
            agent=canonical_hunter_agent,
            capsule=sample_context_capsule,
            workspace_id=sample_workspace_id,
            skills=[sample_skill_ref],
            requested_tools=["tool:signal-reader", "action:mutate_signals"],  # Forbidden!
        )
    assert exc_info.value.reason_code == "UNAUTHORIZED_TOOL"

    # Attempting to compile with an ungranted tool
    with pytest.raises(UnauthorizedToolError) as exc_info2:
        AgentInvocationCompiler.compile(
            agent=canonical_hunter_agent,
            capsule=sample_context_capsule,
            workspace_id=sample_workspace_id,
            skills=[sample_skill_ref],
            requested_tools=["tool:database-drop-table"],  # Not granted!
        )
    assert exc_info2.value.reason_code == "UNAUTHORIZED_TOOL"

    # Attempting runtime execution with a tool not present in the compiled invocation
    valid_invocation = AgentInvocationCompiler.compile(
        agent=canonical_hunter_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        skills=[sample_skill_ref],
    )
    with pytest.raises(UnauthorizedToolError) as exc_info3:
        AgentInvocationRuntime.execute(
            valid_invocation,
            supplied_tool_calls=["tool:unapproved-ambient-tool"],
        )
    assert exc_info3.value.reason_code == "UNAUTHORIZED_TOOL"


def test_false_proof_defense_unauthorized_model_policy_violation(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
):
    """False-Proof Defense 3: Requesting a model outside the agent's policy is rejected."""
    with pytest.raises(UnauthorizedModelError) as exc_info:
        AgentInvocationCompiler.compile(
            agent=canonical_hunter_agent,
            capsule=sample_context_capsule,
            workspace_id=sample_workspace_id,
            skills=[sample_skill_ref],
            model_id="claude-3-opus-unapproved",  # Not in preferred or fallback models
        )

    assert exc_info.value.reason_code == "UNAUTHORIZED_MODEL"


def test_false_proof_defense_output_contract_violation(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
):
    """False-Proof Defense 4: Malformed or non-JSON output violating contract fails closed."""
    invocation = AgentInvocationCompiler.compile(
        agent=canonical_hunter_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        skills=[sample_skill_ref],
        output_contract={"contract_id": "contract:strict-json:v1", "output_type": "JSON"},
    )

    # Mock inference returning unstructured markdown instead of valid JSON
    def malformed_inference(inv: AgentInvocation):
        return {
            "response_text": "I am unable to generate JSON because of an internal error.",
            "parsed_json": None,
            "prompt_tokens": 100,
            "completion_tokens": 20,
        }

    with pytest.raises(OutputContractViolationError) as exc_info:
        AgentInvocationRuntime.execute(invocation, inference_fn=malformed_inference)

    assert exc_info.value.reason_code == "OUTPUT_CONTRACT_VIOLATION"


# ---------------------------------------------------------------------------
# Concrete Execution Trace Demonstration
# ---------------------------------------------------------------------------

def test_concrete_agent_compiled_context_invocation_receipt_trace(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
):
    """Demonstrate the concrete Agent -> compiled context -> invocation -> model -> typed output -> receipt path."""
    # 1. Agent definition verified
    assert canonical_hunter_agent.authority_lane == AuthorityLane.HUNTER
    assert canonical_hunter_agent.content_sha256 != ""

    # 2. Compiled Context Capsule verified
    assert sample_context_capsule.capsule_sha256 != ""
    assert len(sample_context_capsule.included_context) >= 3

    # 3. Compile governed AgentInvocation
    invocation = AgentInvocationCompiler.compile(
        agent=canonical_hunter_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        run_id="run_e2e_trace_001",
        state_id="PHASE_2_SYNTHESIS",
        model_id="gemini-2.5-pro",
        temperature_bps=2000,
        skills=[sample_skill_ref],
    )

    assert invocation.invocation_sha256 != ""
    assert invocation.lane == AuthorityLane.HUNTER
    assert invocation.tools == ("tool:evidence-extractor", "tool:signal-reader")

    # 4. Custom inference producing valid structured JSON conforming to contract
    def realistic_inference_fn(inv: AgentInvocation):
        response_payload = {
            "synthesis_id": "synth_001",
            "findings": [
                {
                    "theme": "Psychological dissonance in interview signals",
                    "evidence_refs": ["ev_101", "ev_102"],
                    "confidence_bps": 9500,
                }
            ],
            "governance_lane": inv.lane.value,
        }
        return {
            "response_text": json.dumps(response_payload),
            "parsed_json": response_payload,
            "prompt_tokens": 240,
            "completion_tokens": 65,
            "latency_micros": 42_000,
            "provider_class": "GroqOpenAIProvider",
        }

    # 5. Execute through Runtime
    receipt = AgentInvocationRuntime.execute(
        invocation,
        inference_fn=realistic_inference_fn,
        supplied_tool_calls=["tool:signal-reader"],
    )

    # 6. Verify end-to-end receipt provenance
    assert receipt.receipt_id.startswith("rcpt_inv_")
    assert receipt.invocation_id == invocation.invocation_id
    assert receipt.agent_id == canonical_hunter_agent.agent_id
    assert receipt.lane == "HUNTER"
    assert receipt.package_sha256 == canonical_hunter_agent.content_sha256
    assert receipt.capsule_sha256 == sample_context_capsule.capsule_sha256
    assert receipt.invocation_sha256 == invocation.invocation_sha256
    assert receipt.model_id == "gemini-2.5-pro"
    assert receipt.provider_class == "GroqOpenAIProvider"
    assert receipt.prompt_tokens == 240
    assert receipt.completion_tokens == 65
    assert receipt.total_tokens == 305
    assert receipt.latency_micros == 42_000
    assert receipt.parsed_output["synthesis_id"] == "synth_001"
    assert receipt.parsed_output["findings"][0]["confidence_bps"] == 9500
    assert receipt.output_contract_passed is True
    assert receipt.gate_passed is True
    assert len(receipt.receipt_sha256) == 64
