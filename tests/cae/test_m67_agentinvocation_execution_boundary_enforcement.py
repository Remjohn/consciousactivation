"""Comprehensive Test Suite for CAE Mandate M67: AgentInvocation Execution Boundary Enforcement.

Governed by:
- 03_AGENT_RUNTIME_ENFORCEMENT/M67_agentinvocation_execution_boundary_enforcement.md
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md
- 00_CONTROL/05_CLAIM_CEILING.md

Verifies:
- Gate 1: Missing production executor/provider blocks fail closed (ProductionExecutionModeViolationError).
- Gate 2: Deterministic fallback in TEST_FIXTURE mode produces synthetic receipt.
- Gate 3: Provider-backed production invocation emits valid receipt with is_synthetic=False.
- Gate 4: Invocation tampering fails closed (InvocationIntegrityError).
- Gate 5: Unauthorized tool injection fails closed (UnauthorizedToolError).
- Gate 6: Output contract violation fails closed (OutputContractViolationError).
- Gate 7: Static caller graph and runtime trace for genuine invocation.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from uuid import UUID, uuid4

import pytest

from ca_contracts import canonical_sha256
from ca_runtime import (
    AccessMode,
    AgentCapabilityGrant,
    AgentDefinition,
    AgentInvocation,
    AgentInvocationCompiler,
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
    ExecutionMode,
    InvocationIntegrityError,
    JITContextCapsule,
    JITContextCompiler,
    OutputContractViolationError,
    ProductionExecutionModeViolationError,
    SkillMaturity,
    SkillPackageRef,
    UnauthorizedToolError,
)


# ---------------------------------------------------------------------------
# Shared Fixtures
# ---------------------------------------------------------------------------

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
        agent_id="BoundaryEnforcementTestAgent",
        version="1.0.0",
        name="Boundary Enforcement Test Agent",
        purpose="Tests execution boundary enforcement for M67.",
        authority_lane=AuthorityLane.HUNTER,
        lifecycle_state=AgentLifecycleState.APPROVED,
        model_policy=AgentModelPolicy(
            preferred_model="gemini-2.5-pro",
            temperature=0.2,
            temperature_bps=2000,
            token_budget=64_000,
            fallback_models=["gemini-2.5-flash"],
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
        ],
        output_contract=AgentOutputContract(
            contract_id="contract:m67-boundary:v1",
            output_type="JSON",
            description="Structured JSON output with boundary verification",
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
        agent_id="BoundaryEnforcementTestAgent",
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


@pytest.fixture
def compiled_invocation(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
) -> AgentInvocation:
    return AgentInvocationCompiler.compile(
        agent=canonical_hunter_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        run_id="run_m67_boundary_test",
        state_id="STATE_REASONING",
        skills=[sample_skill_ref],
    )


# ---------------------------------------------------------------------------
# Mock ModelReasoningEngine for Production-Mode Tests
# ---------------------------------------------------------------------------

@dataclass
class MockInferenceResult:
    response_text: str
    parsed_json: dict | None
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_micros: int
    provider_class: str


class MockModelReasoningEngine:
    """Simulates a real ModelReasoningEngine for production boundary enforcement testing."""

    def infer(self, *, prompt: str, system_prompt: str, temperature: float, max_tokens: int) -> MockInferenceResult:
        response_payload = {
            "status": "SUCCESS",
            "agent_id": "BoundaryEnforcementTestAgent",
            "lane": "HUNTER",
            "summary": "Production inference executed via MockModelReasoningEngine.",
            "evidence": ["ev_prod_001"],
        }
        return MockInferenceResult(
            response_text=json.dumps(response_payload),
            parsed_json=response_payload,
            prompt_tokens=200,
            completion_tokens=60,
            total_tokens=260,
            latency_micros=38_000,
            provider_class="GoogleGeminiProvider",
        )


# ===========================================================================
# Gate 1: Missing production executor/provider blocks fail closed
# ===========================================================================

def test_m67_missing_production_executor_blocks_fail_closed(
    compiled_invocation: AgentInvocation,
) -> None:
    """Gate 1: Production mode without engine or inference_fn raises ProductionExecutionModeViolationError."""
    with pytest.raises(ProductionExecutionModeViolationError) as exc_info:
        AgentInvocationRuntime.execute(
            compiled_invocation,
            mode=ExecutionMode.PRODUCTION,
            # No inference_fn, no model_reasoning_engine
        )
    assert exc_info.value.reason_code == "ERR_PRODUCTION_EXECUTION_MODE_VIOLATION"
    assert "Deterministic mock fallback is strictly forbidden" in str(exc_info.value)
    assert exc_info.value.details["agent_id"] == "BoundaryEnforcementTestAgent"


# ===========================================================================
# Gate 2: Deterministic fallback marked synthetic in TEST_FIXTURE mode
# ===========================================================================

def test_m67_deterministic_fallback_marked_synthetic(
    compiled_invocation: AgentInvocation,
) -> None:
    """Gate 2: TEST_FIXTURE mode deterministic fallback emits receipt with is_synthetic=True."""
    receipt = AgentInvocationRuntime.execute(
        compiled_invocation,
        mode=ExecutionMode.TEST_FIXTURE,
        # No inference_fn, no engine — uses deterministic mock
    )

    assert isinstance(receipt, AgentInvocationReceipt)
    assert receipt.execution_mode == "TEST_FIXTURE"
    assert receipt.is_synthetic is True
    assert receipt.gate_passed is True
    assert receipt.parsed_output["summary"] == "Governed invocation execution completed successfully."

    # Verify canonical dict includes execution_mode and is_synthetic
    c_dict = receipt.canonical_dict()
    assert c_dict["execution_mode"] == "TEST_FIXTURE"
    assert c_dict["is_synthetic"] is True


# ===========================================================================
# Gate 3: Provider-backed production invocation emits valid receipt
# ===========================================================================

def test_m67_provider_backed_production_invocation_emits_valid_receipt(
    compiled_invocation: AgentInvocation,
) -> None:
    """Gate 3: PRODUCTION mode with ModelReasoningEngine emits receipt with is_synthetic=False."""
    engine = MockModelReasoningEngine()

    receipt = AgentInvocationRuntime.execute(
        compiled_invocation,
        mode=ExecutionMode.PRODUCTION,
        model_reasoning_engine=engine,
    )

    assert isinstance(receipt, AgentInvocationReceipt)
    assert receipt.execution_mode == "PRODUCTION"
    assert receipt.is_synthetic is False
    assert receipt.gate_passed is True
    assert receipt.provider_class == "GoogleGeminiProvider"
    assert receipt.prompt_tokens == 200
    assert receipt.completion_tokens == 60
    assert receipt.total_tokens == 260
    assert receipt.latency_micros == 38_000
    assert receipt.parsed_output["summary"] == "Production inference executed via MockModelReasoningEngine."
    assert len(receipt.receipt_sha256) == 64


def test_m67_production_mode_with_inference_fn_succeeds(
    compiled_invocation: AgentInvocation,
) -> None:
    """Gate 3b: PRODUCTION mode with inference_fn (authorized provider bridge) succeeds."""
    def provider_inference_fn(inv: AgentInvocation) -> dict:
        payload = {"status": "SUCCESS", "agent_id": inv.agent_id, "lane": inv.lane.value}
        return {
            "response_text": json.dumps(payload),
            "parsed_json": payload,
            "prompt_tokens": 120,
            "completion_tokens": 30,
            "latency_micros": 22_000,
            "provider_class": "OpenAIAPIProvider",
        }

    receipt = AgentInvocationRuntime.execute(
        compiled_invocation,
        mode=ExecutionMode.PRODUCTION,
        inference_fn=provider_inference_fn,
    )

    assert receipt.execution_mode == "PRODUCTION"
    assert receipt.is_synthetic is False
    assert receipt.provider_class == "OpenAIAPIProvider"


# ===========================================================================
# Gate 4 (Countertest): Invocation tampering fails closed
# ===========================================================================

def test_m67_invocation_tampering_fails_closed(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
) -> None:
    """Countertest: Tampered invocation triggers InvocationIntegrityError regardless of execution mode."""
    invocation = AgentInvocationCompiler.compile(
        agent=canonical_hunter_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        skills=[sample_skill_ref],
    )

    # Tamper with assembled_prompt but preserve original hash
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
        model_id=invocation.model_id,
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
        invocation_sha256=invocation.invocation_sha256,  # Original hash
        created_at=invocation.created_at,
    )

    # Fails in TEST_FIXTURE mode
    with pytest.raises(InvocationIntegrityError):
        AgentInvocationRuntime.execute(tampered_invocation, mode=ExecutionMode.TEST_FIXTURE)

    # Also fails in PRODUCTION mode
    with pytest.raises(InvocationIntegrityError):
        AgentInvocationRuntime.execute(
            tampered_invocation,
            mode=ExecutionMode.PRODUCTION,
            model_reasoning_engine=MockModelReasoningEngine(),
        )


# ===========================================================================
# Gate 5 (Countertest): Unauthorized tool call fails closed
# ===========================================================================

def test_m67_unauthorized_tool_call_fails_closed(
    compiled_invocation: AgentInvocation,
) -> None:
    """Countertest: Unauthorized tool call fails in both TEST_FIXTURE and PRODUCTION modes."""
    # TEST_FIXTURE mode
    with pytest.raises(UnauthorizedToolError):
        AgentInvocationRuntime.execute(
            compiled_invocation,
            mode=ExecutionMode.TEST_FIXTURE,
            supplied_tool_calls=["tool:unapproved-ambient-tool"],
        )

    # PRODUCTION mode
    with pytest.raises(UnauthorizedToolError):
        AgentInvocationRuntime.execute(
            compiled_invocation,
            mode=ExecutionMode.PRODUCTION,
            model_reasoning_engine=MockModelReasoningEngine(),
            supplied_tool_calls=["tool:unapproved-ambient-tool"],
        )


# ===========================================================================
# Gate 6 (Countertest): Output contract violation fails closed
# ===========================================================================

def test_m67_output_contract_violation_fails_closed(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
) -> None:
    """Countertest: Malformed output failing contract fails closed in both modes."""
    invocation = AgentInvocationCompiler.compile(
        agent=canonical_hunter_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        skills=[sample_skill_ref],
        output_contract={"contract_id": "contract:strict-json:v1", "output_type": "JSON"},
    )

    def malformed_inference(inv: AgentInvocation):
        return {
            "response_text": "This is not JSON at all. Just plain text.",
            "parsed_json": None,
            "prompt_tokens": 100,
            "completion_tokens": 20,
        }

    # Fails in TEST_FIXTURE mode
    with pytest.raises(OutputContractViolationError):
        AgentInvocationRuntime.execute(
            invocation,
            mode=ExecutionMode.TEST_FIXTURE,
            inference_fn=malformed_inference,
        )

    # Fails in PRODUCTION mode
    with pytest.raises(OutputContractViolationError):
        AgentInvocationRuntime.execute(
            invocation,
            mode=ExecutionMode.PRODUCTION,
            inference_fn=malformed_inference,
        )


# ===========================================================================
# Gate 7: Static caller graph and runtime trace
# ===========================================================================

def test_m67_static_caller_graph_and_runtime_trace(
    canonical_hunter_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    sample_skill_ref: SkillPackageRef,
) -> None:
    """Gate 7: Traces genuine invocation flow across the full chain and verifies execution_mode stamps."""
    # 1. Agent definition verified
    assert canonical_hunter_agent.authority_lane == AuthorityLane.HUNTER
    assert canonical_hunter_agent.content_sha256 != ""

    # 2. Context capsule verified
    assert sample_context_capsule.capsule_sha256 != ""

    # 3. Compile governed AgentInvocation
    invocation = AgentInvocationCompiler.compile(
        agent=canonical_hunter_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        run_id="run_m67_trace_001",
        state_id="PHASE_BOUNDARY_ENFORCEMENT",
        skills=[sample_skill_ref],
    )

    assert invocation.invocation_sha256 != ""
    assert invocation.lane == AuthorityLane.HUNTER

    # 4. Execute in TEST_FIXTURE mode — synthetic receipt
    fixture_receipt = AgentInvocationRuntime.execute(
        invocation,
        mode=ExecutionMode.TEST_FIXTURE,
    )

    assert fixture_receipt.execution_mode == "TEST_FIXTURE"
    assert fixture_receipt.is_synthetic is True
    assert fixture_receipt.invocation_sha256 == invocation.invocation_sha256

    # 5. Execute in PRODUCTION mode — real receipt
    engine = MockModelReasoningEngine()
    production_receipt = AgentInvocationRuntime.execute(
        invocation,
        mode=ExecutionMode.PRODUCTION,
        model_reasoning_engine=engine,
    )

    assert production_receipt.execution_mode == "PRODUCTION"
    assert production_receipt.is_synthetic is False
    assert production_receipt.invocation_sha256 == invocation.invocation_sha256
    assert production_receipt.provider_class == "GoogleGeminiProvider"

    # 6. Both receipts share invocation lineage but differ on evidence classification
    assert fixture_receipt.invocation_id == production_receipt.invocation_id
    assert fixture_receipt.execution_mode != production_receipt.execution_mode
    assert fixture_receipt.is_synthetic != production_receipt.is_synthetic

    # 7. Verify receipt SHA integrity for both
    assert len(fixture_receipt.receipt_sha256) == 64
    assert len(production_receipt.receipt_sha256) == 64
    assert fixture_receipt.receipt_sha256 != production_receipt.receipt_sha256
"""Comprehensive Test Suite for CAE Mandate M67: AgentInvocation Execution Boundary Enforcement."""
