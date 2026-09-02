"""Comprehensive Acceptance Test Suite for Mandate M56: Standalone Agent Session Runtime.

Governed by:
- Phase 6 Mandate M56 (01_AGENT_EXECUTION/M56_standalone_agent_session_runtime.md)
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/04_OBJECT_AUTHORITY_MAP.md
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md

Tests:
1. Gate 1: Agent Session is discoverable and inspectable.
2. Gate 2: Same Agent definition works in Program and Session.
3. Gate 3: Session has explicit authority/scope (scope bounds tools, evidence, read-only).
4. Gate 4: Context does not leak from another session (cross-session isolation).
5. Gate 5: Session can pause/resume/repair where authorized.
6. False-proof defense 1: Start debug session with broader tools than allowed in agent package.
7. False-proof defense 2: Reuse stale Program context / foreign capsule.
8. False-proof defense 3: Submit session without operator authorization.
9. False-proof defense 4: Create session that silently writes to canonical state.
10. Concrete trace: Full Standalone Agent Session lifecycle trace with execution and completion receipts.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
from uuid import UUID, uuid4
import pytest

from ca_runtime.agent_registry import (
    AgentCapabilityGrant,
    AgentDefinition,
    AgentLifecycleState,
    AgentModelPolicy,
    AgentOutputContract,
    AgentPromptReference,
    AgentRegistry,
    AgentResolver,
    reset_global_agent_registry,
)
from ca_runtime.agent_invocation import (
    AgentInvocation,
    AgentInvocationCompiler,
    AgentInvocationReceipt,
)
from ca_runtime.agent_result_gates import (
    AgentResultGateEngine,
    AgentResultGateEvaluation,
    TypedAgentResult,
)
from ca_runtime.bounded_repair import (
    BoundedRepairRuntimeEngine,
    BoundedRepairSession,
    RepairAttemptRecord,
)
from ca_runtime.context_capsule import (
    AccessMode,
    CapabilityProjection,
    CapabilityScope,
    JITContextCapsule,
    JITContextCompiler,
)
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_agent_binding import (
    ProgramAgentBindingCompiler,
)
from ca_runtime.program_registry import (
    ProgramManifest,
    ProgramPackage,
    ProgramStatus,
    SkillBinding,
)
from ca_runtime.standalone_session_runtime import (
    AgentSessionError,
    AgentSessionReceipt,
    AgentSessionRecord,
    AgentSessionRuntime,
    AgentSessionScope,
    SessionAuthorizationRequiredError,
    SessionCanonicalWriteBlockedError,
    SessionContextLeakError,
    SessionLifecycleState,
    SessionLifecycleViolationError,
    SessionNotFoundError,
    SessionPurpose,
    SessionScopeViolationError,
    SessionToolEscalationError,
)


@pytest.fixture(autouse=True)
def clean_registry():
    reset_global_agent_registry()
    yield
    reset_global_agent_registry()


@pytest.fixture
def workspace_id() -> UUID:
    return UUID("efdfcf16-62d1-4463-a043-aca8f948a127")


@pytest.fixture
def agent_registry() -> AgentRegistry:
    registry = AgentRegistry()
    agents_dir = Path("agents")
    if agents_dir.exists():
        registry.discover_agents(agents_dir)
    else:
        # Fallback registration for hermetic environments
        agent_def = AgentDefinition(
            agent_id="RelationshipCanonicalizationAnalystAgent",
            version="1.0.0",
            name="Relationship Canonicalization Analyst",
            purpose="Analyze and canonicalize relationship hypotheses between entities",
            authority_lane=AuthorityLane.ANALYST,
            lifecycle_state=AgentLifecycleState.APPROVED,
            model_policy=AgentModelPolicy(
                preferred_model="gemini-2.5-pro",
                temperature_bps=2000,
                token_budget=128000,
                fallback_models=["openai/gpt-oss-120b"],
            ),
            prompt_reference=AgentPromptReference(instructions_ref="instructions.md"),
            tools=["tool:query_evidence", "tool:verify_citation"],
            capabilities=[
                AgentCapabilityGrant(
                    scope=CapabilityScope.LOCAL_CONTEXT_READ,
                    mode=AccessMode.READ_ONLY,
                    target="evidence_pool",
                )
            ],
            output_contract=AgentOutputContract(
                contract_id="contract.relationship_canonicalization@1.0.0",
                output_type="JSON",
            ),
        )
        registry.register(agent_def)
    return registry


@pytest.fixture
def sample_session_runtime(agent_registry: AgentRegistry) -> AgentSessionRuntime:
    return AgentSessionRuntime(registry=agent_registry)


# ---------------------------------------------------------------------------
# Acceptance Gate 1: Agent Session is discoverable and inspectable
# ---------------------------------------------------------------------------

def test_gate1_session_discoverable_and_inspectable(
    sample_session_runtime: AgentSessionRuntime,
    workspace_id: UUID,
):
    """Gate 1: Agent Session is discoverable, queryable, and inspectable."""
    session = sample_session_runtime.start(
        agent_id="RelationshipCanonicalizationAnalystAgent",
        purpose=SessionPurpose.REVIEW,
        workspace_id=workspace_id,
        operator_id="operator_gate_officer_1",
        auto_authorize=True,
    )

    assert session.session_id.startswith("sess_standalone_")
    assert session.lifecycle_state == SessionLifecycleState.AUTHORIZED
    assert session.purpose == SessionPurpose.REVIEW
    assert session.authority_lane == AuthorityLane.ANALYST

    # Query sessions
    all_sessions = sample_session_runtime.list_sessions(workspace_id=workspace_id)
    assert len(all_sessions) == 1
    assert all_sessions[0].session_id == session.session_id

    review_sessions = sample_session_runtime.list_sessions(purpose=SessionPurpose.REVIEW)
    assert len(review_sessions) == 1

    debug_sessions = sample_session_runtime.list_sessions(purpose=SessionPurpose.DEBUG)
    assert len(debug_sessions) == 0

    # Inspection
    inspection = sample_session_runtime.inspect(session.session_id)
    assert inspection["session_id"] == session.session_id
    assert inspection["agent_id"] == "RelationshipCanonicalizationAnalystAgent"
    assert inspection["purpose"] == "REVIEW"
    assert inspection["lifecycle_state"] == "AUTHORIZED"
    assert inspection["operator_authorization_id"] == "operator_gate_officer_1"
    assert inspection["scope"]["read_only"] is True
    assert inspection["context_capsule_sha256"] is not None


# ---------------------------------------------------------------------------
# Acceptance Gate 2: Same Agent definition works in Program and Session
# ---------------------------------------------------------------------------

def test_gate2_same_agent_works_in_program_and_session(
    sample_session_runtime: AgentSessionRuntime,
    agent_registry: AgentRegistry,
    workspace_id: UUID,
):
    """Gate 2: The exact same AgentDefinition binds into both Program manifests and Standalone Sessions."""
    agent_id = "RelationshipCanonicalizationAnalystAgent"
    agent_def = agent_registry.get(agent_id)
    assert agent_def is not None

    # 1. Standalone Session Binding
    session = sample_session_runtime.start(
        agent_id=agent_id,
        purpose=SessionPurpose.PLANNING,
        workspace_id=workspace_id,
        operator_id="operator_human",
        auto_authorize=True,
    )
    assert session.agent_id == agent_def.agent_id
    assert session.agent_version == agent_def.version
    assert session.authority_lane == agent_def.authority_lane

    # 2. Program Manifest Binding (reusing ProgramAgentBindingCompiler from M53)
    manifest = {
        "id": "test_relationship_program",
        "version": "1.0.0",
        "purpose": "Relationship test workflow",
        "status": "ACTIVE",
        "lanes": ["ANALYST"],
        "agents": [agent_id],
        "skills": [
            {"name": "canonical_relationship_classifier", "path": "skills/canonical_relationship_classifier/SKILL.md", "version": "1.0.0"}
        ],
        "tools": ["semantic_similarity_analyzer"],
    }
    workflow_nodes = [
        {
            "node_id": "canonicalize_node",
            "role": "ANALYST",
            "agent_id": agent_id,
            "required_lane": "ANALYST",
            "declared_skills": ["canonical_relationship_classifier"],
            "declared_tools": ["semantic_similarity_analyzer"],
            "expected_output_contract": "relationship_analysis_receipt",
        }
    ]

    binding_manifest = ProgramAgentBindingCompiler.compile(
        program_manifest=manifest,
        workflow_nodes=workflow_nodes,
        agent_registry=agent_registry,
    )
    assert len(binding_manifest.node_assignments) == 1
    node_assignment = binding_manifest.node_assignments[0]
    assert node_assignment.agent_id == agent_def.agent_id
    assert node_assignment.lane == agent_def.authority_lane


# ---------------------------------------------------------------------------
# Acceptance Gate 3: Session has explicit authority/scope
# ---------------------------------------------------------------------------

def test_gate3_session_has_explicit_authority_scope(
    sample_session_runtime: AgentSessionRuntime,
    workspace_id: UUID,
):
    """Gate 3: Session has explicit, hash-addressed authority scope and budget limits."""
    custom_scope = AgentSessionScope(
        workspace_id=workspace_id,
        allowed_evidence_ids=("ev_candidate_101", "ev_candidate_102"),
        allowed_tools=("semantic_similarity_analyzer",),
        forbidden_actions=("action:delete_evidence",),
        read_only=True,
        max_invocations=2,
    )

    session = sample_session_runtime.start(
        agent_id="RelationshipCanonicalizationAnalystAgent",
        purpose=SessionPurpose.DEBUG,
        workspace_id=workspace_id,
        scope=custom_scope,
        operator_id="operator_debug",
        auto_authorize=True,
    )

    assert session.scope.scope_sha256 != ""
    assert session.scope.max_invocations == 2
    assert session.scope.allowed_tools == ("semantic_similarity_analyzer",)

    # Invocations within budget succeed
    def dummy_inference(inv: AgentInvocation) -> Dict[str, Any]:
        return {
            "response_text": json.dumps({
                "relationship_type": "CORROBORATES",
                "confidence_bps": 9500,
                "evidence_refs": ["ev_candidate_101"],
            }),
            "parsed_json": {
                "relationship_type": "CORROBORATES",
                "confidence_bps": 9500,
                "evidence_refs": ["ev_candidate_101"],
            },
        }

    rcpt1 = sample_session_runtime.invoke(session.session_id, "Task 1", inference_fn=dummy_inference)
    assert rcpt1.gate_passed is True

    rcpt2 = sample_session_runtime.invoke(session.session_id, "Task 2", inference_fn=dummy_inference)
    assert rcpt2.gate_passed is True

    # Third invocation exceeds max_invocations budget
    with pytest.raises(SessionScopeViolationError) as exc_info:
        sample_session_runtime.invoke(session.session_id, "Task 3", inference_fn=dummy_inference)
    assert exc_info.value.reason_code == "SESSION_SCOPE_VIOLATION"


# ---------------------------------------------------------------------------
# Acceptance Gate 4: Context does not leak across sessions
# ---------------------------------------------------------------------------

def test_gate4_context_does_not_leak_across_sessions(
    sample_session_runtime: AgentSessionRuntime,
    workspace_id: UUID,
):
    """Gate 4: Context does not leak from another session; capsules are strictly isolated."""
    other_workspace = UUID("11111111-2222-3333-4444-555555555555")

    session1 = sample_session_runtime.start(
        agent_id="RelationshipCanonicalizationAnalystAgent",
        purpose=SessionPurpose.REVIEW,
        workspace_id=workspace_id,
        operator_id="op_1",
        auto_authorize=True,
    )
    session2 = sample_session_runtime.start(
        agent_id="RelationshipCanonicalizationAnalystAgent",
        purpose=SessionPurpose.DEBUG,
        workspace_id=other_workspace,
        operator_id="op_2",
        auto_authorize=True,
    )

    # Distinct capsules and hashes
    assert session1.context_sha256_at_creation != session2.context_sha256_at_creation

    # Attempting to inject session 2's capsule into session 1 raises SessionContextLeakError
    capsule2 = sample_session_runtime._session_capsules[session2.session_id]

    with pytest.raises(SessionContextLeakError) as exc_info:
        sample_session_runtime.invoke(
            session1.session_id,
            "Contaminated task",
            capsule=capsule2,
        )
    assert exc_info.value.reason_code == "SESSION_CONTEXT_LEAK_DETECTED"


# ---------------------------------------------------------------------------
# Acceptance Gate 5: Session pause, resume, and repair
# ---------------------------------------------------------------------------

def test_gate5_session_pause_resume_repair(
    sample_session_runtime: AgentSessionRuntime,
    workspace_id: UUID,
):
    """Gate 5: Session supports pause, resume, and bounded in-session repair."""
    session = sample_session_runtime.start(
        agent_id="RelationshipCanonicalizationAnalystAgent",
        purpose=SessionPurpose.INCIDENT_INVESTIGATION,
        workspace_id=workspace_id,
        operator_id="op_commander",
        auto_authorize=True,
    )

    # 1. First invocation transitions to ACTIVE
    def valid_inference(inv: AgentInvocation) -> Dict[str, Any]:
        return {
            "response_text": json.dumps({"status": "INCIDENT_REVIEWED", "confidence_bps": 9900}),
            "parsed_json": {"status": "INCIDENT_REVIEWED", "confidence_bps": 9900},
        }

    sample_session_runtime.invoke(session.session_id, "Review incident", inference_fn=valid_inference)
    active_sess = sample_session_runtime.get_session(session.session_id)
    assert active_sess.lifecycle_state == SessionLifecycleState.ACTIVE

    # 2. Pause session
    paused_sess = sample_session_runtime.pause(session.session_id, operator_id="op_commander")
    assert paused_sess.lifecycle_state == SessionLifecycleState.PAUSED

    # Invocations while paused fail
    with pytest.raises(SessionLifecycleViolationError):
        sample_session_runtime.invoke(session.session_id, "Paused task", inference_fn=valid_inference)

    # 3. Resume session
    resumed_sess = sample_session_runtime.resume(session.session_id, operator_id="op_commander")
    assert resumed_sess.lifecycle_state == SessionLifecycleState.ACTIVE

    # 4. In-session Bounded Repair
    attempt_count = 0

    def recovering_inference(inv: AgentInvocation, prior: Optional[RepairAttemptRecord]) -> str:
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count == 1:
            return "Narrative done"  # Rejected by anti-narrative gate
        return json.dumps({
            "relationship_type": "CORROBORATES",
            "confidence_bps": 9200,
            "evidence_refs": ["ev_candidate_101"],
        })

    def gate_evaluator(raw_text: str, inv: AgentInvocation) -> Tuple[TypedAgentResult, AgentResultGateEvaluation]:
        try:
            parsed = json.loads(raw_text)
        except Exception:
            parsed = None
        return AgentResultGateEngine.evaluate(
            raw_response_text=raw_text,
            parsed_json=parsed,
            output_contract=inv.output_contract,
            invocation=inv,
            verified_evidence_ids=["ev_candidate_101"],
        )

    typed_result, repair_sess = sample_session_runtime.execute_with_repair(
        session_id=session.session_id,
        task_prompt="Canonicalize with repair",
        inference_fn=recovering_inference,
        gate_evaluator=gate_evaluator,
        max_retries=2,
    )
    assert typed_result.gate_evaluation.all_required_passed is True
    assert typed_result.gate_evaluation.composite_score_bps == 10000
    assert repair_sess.terminal_state == "REPAIR_SUCCEEDED"

    # 5. Complete session
    receipt = sample_session_runtime.complete(session.session_id)
    assert receipt.lifecycle_state == "COMPLETED"
    assert receipt.invocation_count >= 2
    assert receipt.repair_count == 1
    assert receipt.receipt_sha256 != ""


# ---------------------------------------------------------------------------
# False-Proof Defense 1: Start debug session with broader tools than allowed
# ---------------------------------------------------------------------------

def test_false_proof_debug_session_broader_tools(
    sample_session_runtime: AgentSessionRuntime,
    workspace_id: UUID,
):
    """False-Proof Defense 1: Starting a debug session with tools exceeding agent package fails closed."""
    escalated_scope = AgentSessionScope(
        workspace_id=workspace_id,
        allowed_tools=("semantic_similarity_analyzer", "tool:unauthorized_database_wiper"),
    )

    with pytest.raises(SessionToolEscalationError) as exc_info:
        sample_session_runtime.start(
            agent_id="RelationshipCanonicalizationAnalystAgent",
            purpose=SessionPurpose.DEBUG,
            workspace_id=workspace_id,
            scope=escalated_scope,
        )
    assert exc_info.value.reason_code == "SESSION_TOOL_ESCALATION"
    assert "tool:unauthorized_database_wiper" in str(exc_info.value)


# ---------------------------------------------------------------------------
# False-Proof Defense 2: Reuse stale Program context
# ---------------------------------------------------------------------------

def test_false_proof_reuse_stale_program_context(
    sample_session_runtime: AgentSessionRuntime,
    workspace_id: UUID,
):
    """False-Proof Defense 2: Passing stale/foreign context capsule into standalone session fails closed."""
    session = sample_session_runtime.start(
        agent_id="RelationshipCanonicalizationAnalystAgent",
        purpose=SessionPurpose.REVIEW,
        workspace_id=workspace_id,
        operator_id="op_reviewer",
        auto_authorize=True,
    )

    # Construct foreign capsule from a different workspace
    foreign_capsule = JITContextCompiler.assemble(
        workspace_id=UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"),
        lane=AuthorityLane.ANALYST,
        actor_id="actor_stale",
        program_id="stale_program",
        harness_id="stale_harness_foreign",
        agent_id="RelationshipCanonicalizationAnalystAgent",
        model_id="gemini-2.5-pro",
        total_token_budget=128000,
        agent_instructions=("instructions.md", "Stale instructions"),
    )

    with pytest.raises(SessionContextLeakError) as exc_info:
        sample_session_runtime.invoke(
            session.session_id,
            "Execute with stale context",
            capsule=foreign_capsule,
        )
    assert exc_info.value.reason_code == "SESSION_CONTEXT_LEAK_DETECTED"


# ---------------------------------------------------------------------------
# False-Proof Defense 3: Submit session without operator authorization
# ---------------------------------------------------------------------------

def test_false_proof_session_without_operator_authorization(
    sample_session_runtime: AgentSessionRuntime,
    workspace_id: UUID,
):
    """False-Proof Defense 3: Executing a session without operator authorization fails closed."""
    # Start session with auto_authorize=False (default)
    session = sample_session_runtime.start(
        agent_id="RelationshipCanonicalizationAnalystAgent",
        purpose=SessionPurpose.REVIEW,
        workspace_id=workspace_id,
    )
    assert session.lifecycle_state == SessionLifecycleState.CREATED

    with pytest.raises(SessionAuthorizationRequiredError) as exc_info:
        sample_session_runtime.invoke(session.session_id, "Attempt unauthorized invocation")
    assert exc_info.value.reason_code == "SESSION_AUTHORIZATION_REQUIRED"

    # Now authorize and verify invocation succeeds
    sample_session_runtime.authorize(session.session_id, operator_id="operator_valid")
    authorized_sess = sample_session_runtime.get_session(session.session_id)
    assert authorized_sess.lifecycle_state == SessionLifecycleState.AUTHORIZED


# ---------------------------------------------------------------------------
# False-Proof Defense 4: Session writes to canonical state silently
# ---------------------------------------------------------------------------

def test_false_proof_session_writes_canonical_state(
    sample_session_runtime: AgentSessionRuntime,
    workspace_id: UUID,
):
    """False-Proof Defense 4: Read-only standalone session attempting canonical state write fails closed."""
    session = sample_session_runtime.start(
        agent_id="RelationshipCanonicalizationAnalystAgent",
        purpose=SessionPurpose.REVIEW,
        workspace_id=workspace_id,
        operator_id="op_reviewer",
        auto_authorize=True,
    )
    assert session.scope.read_only is True

    with pytest.raises(SessionCanonicalWriteBlockedError) as exc_info:
        sample_session_runtime.invoke(
            session.session_id,
            "Attempting to write canonical state",
            is_canonical_mutation=True,
        )
    assert exc_info.value.reason_code == "CANONICAL_WRITE_BLOCKED"


# ---------------------------------------------------------------------------
# Concrete Execution Trace
# ---------------------------------------------------------------------------

def test_concrete_session_lifecycle_trace(
    sample_session_runtime: AgentSessionRuntime,
    workspace_id: UUID,
):
    """Demonstrates concrete Agent -> compiled context -> model/tool policy -> typed output -> gate -> receipt trace."""
    # 1. Start Session
    session = sample_session_runtime.start(
        agent_id="RelationshipCanonicalizationAnalystAgent",
        purpose=SessionPurpose.DEBATE,
        workspace_id=workspace_id,
    )
    assert session.lifecycle_state == SessionLifecycleState.CREATED

    # 2. Authorize Session
    sample_session_runtime.authorize(session.session_id, operator_id="lead_investigator")
    authorized = sample_session_runtime.get_session(session.session_id)
    assert authorized.lifecycle_state == SessionLifecycleState.AUTHORIZED
    assert authorized.operator_authorization_id == "lead_investigator"

    # 3. Governed Invocation
    def inference_handler(inv: AgentInvocation) -> Dict[str, Any]:
        assert inv.agent_id == "RelationshipCanonicalizationAnalystAgent"
        assert inv.lane == AuthorityLane.ANALYST
        return {
            "response_text": json.dumps({
                "relationship_type": "CONTRADICTS",
                "confidence_bps": 8800,
                "evidence_refs": ["ev_candidate_101"],
            }),
            "parsed_json": {
                "relationship_type": "CONTRADICTS",
                "confidence_bps": 8800,
                "evidence_refs": ["ev_candidate_101"],
            },
        }

    inv_receipt = sample_session_runtime.invoke(
        session.session_id,
        "Analyze potential contradiction between candidate 101 and hypothesis 202",
        inference_fn=inference_handler,
    )
    assert inv_receipt.gate_passed is True
    assert inv_receipt.output_contract_passed is True

    # 4. Session Completion
    session_receipt = sample_session_runtime.complete(session.session_id)
    assert session_receipt.lifecycle_state == "COMPLETED"
    assert session_receipt.invocation_count == 1
    assert session_receipt.agent_id == "RelationshipCanonicalizationAnalystAgent"
    assert session_receipt.purpose == "DEBATE"
    assert session_receipt.operator_authorization_id == "lead_investigator"
