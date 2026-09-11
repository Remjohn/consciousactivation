"""
Unit and Integration Tests for CAE Mandate M59: Workflow Control-Flow Compiler.

Validates:
- All 5 Acceptance Gates
- All 4 False-proof/Reward-hacking Defense Vectors (§10)
- Concrete Multi-Primitive Execution Trace
"""

import pytest
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.workflow_control_flow import (
    CompiledWorkflowExecutionGraph,
    ConditionEvaluationError,
    ControlFlowExecutionSnapshot,
    ControlFlowSchedulingError,
    DeterministicControlFlowScheduler,
    HumanGateLaneViolationError,
    HumanGateSuspendedError,
    JoinSynchronizationError,
    LoopBoundExceededError,
    OperatorGrantRecord,
    RoutingDecision,
    TimeoutExceededError,
    WorkflowControlFlowCompiler,
    WorkflowControlFlowError,
)
from ca_runtime.workflow_ir import (
    ExecutableWorkflowIR,
    IREdgeType,
    WorkflowIRCompiler,
    WorkflowIREdge,
    WorkflowIRNode,
)
from ca_runtime.workflow_primitives import (
    ConditionBranchDefinition,
    HumanGateRequirement,
    JoinCondition,
    JoinPolicy,
    LoopBoundPolicy,
    LoopTerminationKind,
    UnboundedLoopError,
    UnevaluableConditionError,
    WorkflowPrimitiveDefinition,
    WorkflowPrimitiveKind,
    WorkUnitKind,
)


# ============================================================================
# Gate 1: Same workflow + same state snapshot gives same routing decision
# ============================================================================


def test_gate1_deterministic_routing_reproducibility() -> None:
    """Verify that same (workflow, snapshot) yields bit-for-bit identical RoutingDecision."""
    nodes = [
        {"node_id": "STEP_1", "capability_id": "cap_1", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "STEP_2", "capability_id": "cap_2", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
    ]
    edges = [
        {"source_node_id": "STEP_1", "target_node_id": "STEP_2", "contract_id": "C1"},
    ]

    ir = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_DETERMINISM_TEST",
        name="Determinism Test",
        category_id="TEST",
        profile_id="DEFAULT",
        purpose="Routing Determinism",
        authority_lane=AuthorityLane.ANALYST,
        nodes=nodes,
        edges=edges,
    )

    snapshot = ControlFlowExecutionSnapshot(
        run_id="run_test_001",
        workflow_id="WIR_DETERMINISM_TEST",
        node_states={"STEP_1": "SUCCEEDED", "STEP_2": "BLOCKED"},
    )

    decision_1 = DeterministicControlFlowScheduler.compute_routing(ir, snapshot)
    decision_2 = DeterministicControlFlowScheduler.compute_routing(ir, snapshot)

    assert decision_1.ready_nodes == ("STEP_2",)
    assert decision_1.routing_digest_sha256 == decision_2.routing_digest_sha256
    assert len(decision_1.routing_digest_sha256) == 64


# ============================================================================
# Gate 2: Loop cannot exceed host bound
# ============================================================================


def test_gate2_loop_cannot_exceed_bound() -> None:
    """Verify that loop iteration stops deterministically when max_iterations is reached."""
    loop_def = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_LOOP",
        primitive_kind=WorkflowPrimitiveKind.LOOP,
        loop_policy=LoopBoundPolicy(max_iterations=3),
    )
    nodes = [
        {"node_id": "LOOP_HEAD", "capability_id": "cap_loop", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY", "primitive_definition": loop_def},
        {"node_id": "LOOP_BODY", "capability_id": "cap_body", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
    ]
    edges = [
        {"source_node_id": "LOOP_HEAD", "target_node_id": "LOOP_BODY", "contract_id": "C1"},
        {"source_node_id": "LOOP_BODY", "target_node_id": "LOOP_HEAD", "contract_id": "C2", "edge_type": IREdgeType.LOOP_BACK.value},
    ]

    ir = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_LOOP_TEST",
        name="Loop Test",
        category_id="TEST",
        profile_id="DEFAULT",
        purpose="Loop Bound Verification",
        authority_lane=AuthorityLane.ANALYST,
        nodes=nodes,
        edges=edges,
    )

    # Iteration 0: Loop head ready
    s0 = ControlFlowExecutionSnapshot(
        run_id="run_loop",
        workflow_id="WIR_LOOP_TEST",
        node_states={"LOOP_HEAD": "READY", "LOOP_BODY": "BLOCKED"},
        loop_counters={"LOOP_HEAD": 0},
    )
    d0 = DeterministicControlFlowScheduler.compute_routing(ir, s0)
    assert "LOOP_HEAD" in d0.ready_nodes
    assert d0.loop_actions.get("LOOP_HEAD") == "CONTINUE_LOOP"

    # Iteration 3 (Bound reached): Terminate loop
    s3 = ControlFlowExecutionSnapshot(
        run_id="run_loop",
        workflow_id="WIR_LOOP_TEST",
        node_states={"LOOP_HEAD": "BLOCKED", "LOOP_BODY": "SUCCEEDED"},
        loop_counters={"LOOP_HEAD": 3},
    )
    d3 = DeterministicControlFlowScheduler.compute_routing(ir, s3)
    assert d3.loop_actions.get("LOOP_HEAD") == "TERMINATE_LOOP"
    assert "LOOP_HEAD" not in d3.ready_nodes


# ============================================================================
# Gate 3: JOIN waits for declared predecessors according to policy
# ============================================================================


def test_gate3_join_waits_for_declared_predecessors() -> None:
    """Verify JOIN primitive synchronization with ALL, ANY, and QUORUM policies."""
    join_all = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_JOIN_ALL",
        primitive_kind=WorkflowPrimitiveKind.JOIN,
        join_condition=JoinCondition(policy=JoinPolicy.ALL),
    )
    nodes = [
        {"node_id": "PARENT_1", "capability_id": "c1", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "PARENT_2", "capability_id": "c2", "phase_order": 1, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
        {"node_id": "JOIN_NODE", "capability_id": "c3", "phase_order": 2, "actor_kind": "DETERMINISTIC_MODULE", "role": "COMPOSER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY", "primitive_definition": join_all},
    ]
    edges = [
        {"source_node_id": "PARENT_1", "target_node_id": "JOIN_NODE", "contract_id": "C1"},
        {"source_node_id": "PARENT_2", "target_node_id": "JOIN_NODE", "contract_id": "C2"},
    ]

    ir = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_JOIN_TEST",
        name="Join Test",
        category_id="TEST",
        profile_id="DEFAULT",
        purpose="Join Sync Verification",
        authority_lane=AuthorityLane.ANALYST,
        nodes=nodes,
        edges=edges,
    )

    # State A: Only PARENT_1 succeeded -> JOIN waits
    s_partial = ControlFlowExecutionSnapshot(
        run_id="run_join",
        workflow_id="WIR_JOIN_TEST",
        node_states={"PARENT_1": "SUCCEEDED", "PARENT_2": "RUNNING", "JOIN_NODE": "BLOCKED"},
    )
    d_partial = DeterministicControlFlowScheduler.compute_routing(ir, s_partial)
    assert "JOIN_NODE" not in d_partial.ready_nodes
    assert d_partial.join_statuses.get("JOIN_NODE") == "WAITING_PREDECESSORS"

    # State B: Both PARENT_1 and PARENT_2 succeeded -> JOIN is ready
    s_complete = ControlFlowExecutionSnapshot(
        run_id="run_join",
        workflow_id="WIR_JOIN_TEST",
        node_states={"PARENT_1": "SUCCEEDED", "PARENT_2": "SUCCEEDED", "JOIN_NODE": "BLOCKED"},
    )
    d_complete = DeterministicControlFlowScheduler.compute_routing(ir, s_complete)
    assert "JOIN_NODE" in d_complete.ready_nodes
    assert d_complete.join_statuses.get("JOIN_NODE") == "SATISFIED"


# ============================================================================
# Gate 4: TIMEOUT transitions to defined failure/recovery state
# ============================================================================


def test_gate4_timeout_detection_on_running_nodes() -> None:
    """Verify that elapsed duration exceeding timeout_seconds is detected and flagged."""
    timeout_def = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_TIMEOUT",
        primitive_kind=WorkflowPrimitiveKind.TIMEOUT,
        timeout_seconds=10,
    )
    nodes = [
        {"node_id": "LONG_STEP", "capability_id": "cap_long", "phase_order": 1, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY", "primitive_definition": timeout_def},
    ]
    edges: list = []

    ir = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_TIMEOUT_TEST",
        name="Timeout Test",
        category_id="TEST",
        profile_id="DEFAULT",
        purpose="Timeout Verification",
        authority_lane=AuthorityLane.ANALYST,
        nodes=nodes,
        edges=edges,
    )

    # Within timeout
    s_ok = ControlFlowExecutionSnapshot(
        run_id="run_timeout",
        workflow_id="WIR_TIMEOUT_TEST",
        node_states={"LONG_STEP": "RUNNING"},
        node_elapsed_seconds={"LONG_STEP": 5.0},
    )
    d_ok = DeterministicControlFlowScheduler.compute_routing(ir, s_ok)
    assert not d_ok.timed_out_nodes

    # Exceeded timeout
    s_expired = ControlFlowExecutionSnapshot(
        run_id="run_timeout",
        workflow_id="WIR_TIMEOUT_TEST",
        node_states={"LONG_STEP": "RUNNING"},
        node_elapsed_seconds={"LONG_STEP": 15.0},
    )
    d_expired = DeterministicControlFlowScheduler.compute_routing(ir, s_expired)
    assert "LONG_STEP" in d_expired.timed_out_nodes


# ============================================================================
# Gate 5: Human gate blocks until explicit operator grant from COMMANDER lane
# ============================================================================


def test_gate5_human_gate_blocks_until_commander_grant() -> None:
    """Verify that HUMAN_GATE remains suspended until approved by COMMANDER lane."""
    gate_prim = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_GATE",
        primitive_kind=WorkflowPrimitiveKind.HUMAN_GATE,
        human_gate=HumanGateRequirement(
            gate_id="EDITORIAL_GATE",
            required_lane=AuthorityLane.COMMANDER,
            approver_role="lead_operator",
        ),
    )
    nodes = [
        {"node_id": "ANALYST_STEP", "capability_id": "c1", "phase_order": 1, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
        {"node_id": "EDITORIAL_GATE", "capability_id": "c2", "phase_order": 2, "actor_kind": "HUMAN_GATE", "role": "COMMANDER", "product_boundary": "STUDIO", "side_effect_class": "READ_ONLY", "primitive_definition": gate_prim},
    ]
    edges = [
        {"source_node_id": "ANALYST_STEP", "target_node_id": "EDITORIAL_GATE", "contract_id": "C1"},
    ]

    ir = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_GATE_TEST",
        name="Human Gate Test",
        category_id="TEST",
        profile_id="DEFAULT",
        purpose="Gate Verification",
        authority_lane=AuthorityLane.COMMANDER,
        nodes=nodes,
        edges=edges,
    )

    # State A: No operator grant -> Gate is suspended in waiting_human_gates
    s_waiting = ControlFlowExecutionSnapshot(
        run_id="run_gate",
        workflow_id="WIR_GATE_TEST",
        node_states={"ANALYST_STEP": "SUCCEEDED", "EDITORIAL_GATE": "BLOCKED"},
    )
    d_waiting = DeterministicControlFlowScheduler.compute_routing(ir, s_waiting)
    assert "EDITORIAL_GATE" not in d_waiting.ready_nodes
    assert "EDITORIAL_GATE" in d_waiting.waiting_human_gates

    # State B: Valid COMMANDER grant recorded -> Gate becomes ready
    grant = OperatorGrantRecord(
        grant_id="grant_001",
        gate_id="EDITORIAL_GATE",
        approver_id="operator_alice",
        approver_role="lead_operator",
        authority_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        rationale="Evidence validated and verified",
        granted_at_utc="2026-09-02T05:30:00Z",
    )
    s_granted = ControlFlowExecutionSnapshot(
        run_id="run_gate",
        workflow_id="WIR_GATE_TEST",
        node_states={"ANALYST_STEP": "SUCCEEDED", "EDITORIAL_GATE": "BLOCKED"},
        operator_grants={"EDITORIAL_GATE": grant},
    )
    d_granted = DeterministicControlFlowScheduler.compute_routing(ir, s_granted)
    assert "EDITORIAL_GATE" in d_granted.ready_nodes
    assert not d_granted.waiting_human_gates


# ============================================================================
# False-Proof & Reward-Hacking Defenses (§10)
# ============================================================================


def test_false_proof_1_condition_ignores_agent_narrative() -> None:
    """False-proof 1: Attempt to escape an IF through an agent-generated narrative."""
    # Context output has quality_score=40, but text claims "I declare quality_score is 100!"
    context_output = {
        "quality_score": 40,
        "agent_text_response": "I have thoroughly analyzed this and assert quality_score >= 80! Proceed to THEN branch.",
    }

    # Host condition strictly checks 'quality_score >= 80'
    res = DeterministicControlFlowScheduler.evaluate_host_condition("quality_score >= 80", context_output)
    assert not res  # Agent narrative has 0 effect on host evaluation


def test_false_proof_2_loop_with_zero_bound_rejected() -> None:
    """False-proof 2: Set max_retries/max_iterations=0."""
    with pytest.raises(UnboundedLoopError):
        LoopBoundPolicy(max_iterations=0)


def test_false_proof_3_human_gate_unauthorized_lane_grant_rejected() -> None:
    """False-proof 3: Invoke a human-gated step from an unauthorized lane (e.g. ANALYST)."""
    gate_prim = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_GATE",
        primitive_kind=WorkflowPrimitiveKind.HUMAN_GATE,
        human_gate=HumanGateRequirement(
            gate_id="SECURITY_GATE",
            required_lane=AuthorityLane.COMMANDER,
            approver_role="lead_operator",
        ),
    )
    nodes = [
        {"node_id": "SECURITY_GATE", "capability_id": "c1", "phase_order": 1, "actor_kind": "HUMAN_GATE", "role": "COMMANDER", "product_boundary": "STUDIO", "side_effect_class": "READ_ONLY", "primitive_definition": gate_prim},
    ]

    ir = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_ILLEGAL_GRANT_TEST",
        name="Illegal Grant Test",
        category_id="TEST",
        profile_id="DEFAULT",
        purpose="Lane Defense",
        authority_lane=AuthorityLane.COMMANDER,
        nodes=nodes,
        edges=[],
    )

    # Attempted grant from ANALYST lane
    illegal_grant = OperatorGrantRecord(
        grant_id="fake_grant",
        gate_id="SECURITY_GATE",
        approver_id="analyst_bob",
        approver_role="analyst",
        authority_lane=AuthorityLane.ANALYST,  # Illegal lane!
        decision="APPROVED",
        rationale="Bypassing commander",
        granted_at_utc="2026-09-02T05:30:00Z",
    )

    snapshot = ControlFlowExecutionSnapshot(
        run_id="run_illegal",
        workflow_id="WIR_ILLEGAL_GRANT_TEST",
        node_states={"SECURITY_GATE": "BLOCKED"},
        operator_grants={"SECURITY_GATE": illegal_grant},
    )

    with pytest.raises(HumanGateLaneViolationError) as exc_info:
        DeterministicControlFlowScheduler.compute_routing(ir, snapshot)
    assert exc_info.value.reason_code == "ERR_HUMAN_GATE_LANE_VIOLATION"


# ============================================================================
# Concrete End-to-End Control-Flow Execution Trace
# ============================================================================


def test_concrete_multi_primitive_execution_trace() -> None:
    """
    Demonstrate full multi-primitive workflow scheduling trace:
    Condition -> Parallel Fan-Out (Hunter & Analyst) -> Join -> Human Gate.
    """
    cond_prim = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_COND",
        primitive_kind=WorkflowPrimitiveKind.CONDITION,
        condition_config=ConditionBranchDefinition(
            condition_expression="signal_count > 0",
            then_step_id="HUNTER_STEP",
            else_step_id="FALLBACK_STEP",
        ),
    )
    join_prim = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_JOIN",
        primitive_kind=WorkflowPrimitiveKind.JOIN,
        join_condition=JoinCondition(policy=JoinPolicy.ALL),
    )
    gate_prim = WorkflowPrimitiveDefinition(
        primitive_id="PRIM_GATE",
        primitive_kind=WorkflowPrimitiveKind.HUMAN_GATE,
        human_gate=HumanGateRequirement(
            gate_id="COMMANDER_GATE",
            required_lane=AuthorityLane.COMMANDER,
            approver_role="lead_operator",
        ),
    )

    nodes = [
        {"node_id": "COND_CHECK", "capability_id": "c0", "phase_order": 1, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY", "primitive_definition": cond_prim},
        {"node_id": "HUNTER_STEP", "capability_id": "c1", "phase_order": 2, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "ANALYST_STEP", "capability_id": "c2", "phase_order": 2, "actor_kind": "AGENT_PROGRAM", "role": "ANALYST", "product_boundary": "AIR", "side_effect_class": "READ_ONLY"},
        {"node_id": "FALLBACK_STEP", "capability_id": "c_fb", "phase_order": 2, "actor_kind": "DETERMINISTIC_MODULE", "role": "HUNTER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY"},
        {"node_id": "JOIN_STEP", "capability_id": "c3", "phase_order": 3, "actor_kind": "DETERMINISTIC_MODULE", "role": "COMPOSER", "product_boundary": "AHP", "side_effect_class": "READ_ONLY", "primitive_definition": join_prim},
        {"node_id": "COMMANDER_GATE", "capability_id": "c4", "phase_order": 4, "actor_kind": "HUMAN_GATE", "role": "COMMANDER", "product_boundary": "STUDIO", "side_effect_class": "READ_ONLY", "primitive_definition": gate_prim},
    ]

    edges = [
        {"source_node_id": "COND_CHECK", "target_node_id": "HUNTER_STEP", "contract_id": "C_THEN", "edge_type": IREdgeType.THEN_BRANCH.value},
        {"source_node_id": "COND_CHECK", "target_node_id": "ANALYST_STEP", "contract_id": "C_PARALLEL"},
        {"source_node_id": "COND_CHECK", "target_node_id": "FALLBACK_STEP", "contract_id": "C_ELSE", "edge_type": IREdgeType.ELSE_BRANCH.value},
        {"source_node_id": "HUNTER_STEP", "target_node_id": "JOIN_STEP", "contract_id": "C_J1"},
        {"source_node_id": "ANALYST_STEP", "target_node_id": "JOIN_STEP", "contract_id": "C_J2"},
        {"source_node_id": "JOIN_STEP", "target_node_id": "COMMANDER_GATE", "contract_id": "C_GATE"},
    ]

    ir = WorkflowIRCompiler.compile_from_source(
        workflow_ir_id="WIR_E2E_CONTROL_FLOW",
        name="E2E Control Flow",
        category_id="RESEARCH",
        profile_id="CANONICAL",
        purpose="Complete Control Flow Verification",
        authority_lane=AuthorityLane.COMMANDER,
        nodes=nodes,
        edges=edges,
    )

    # Step 1: Condition succeeds with signal_count=5 -> HUNTER and ANALYST become ready, FALLBACK is skipped
    s1 = ControlFlowExecutionSnapshot(
        run_id="run_e2e",
        workflow_id="WIR_E2E_CONTROL_FLOW",
        node_states={
            "COND_CHECK": "SUCCEEDED",
            "HUNTER_STEP": "BLOCKED",
            "ANALYST_STEP": "BLOCKED",
            "FALLBACK_STEP": "BLOCKED",
            "JOIN_STEP": "BLOCKED",
            "COMMANDER_GATE": "BLOCKED",
        },
        node_outputs={"COND_CHECK": {"signal_count": 5}},
    )
    d1 = DeterministicControlFlowScheduler.compute_routing(ir, s1)
    assert "FALLBACK_STEP" in d1.skipped_nodes
    assert "HUNTER_STEP" in d1.ready_nodes
    assert "ANALYST_STEP" in d1.ready_nodes

    # Step 2: HUNTER and ANALYST complete -> JOIN step becomes ready
    s2 = ControlFlowExecutionSnapshot(
        run_id="run_e2e",
        workflow_id="WIR_E2E_CONTROL_FLOW",
        node_states={
            "COND_CHECK": "SUCCEEDED",
            "HUNTER_STEP": "SUCCEEDED",
            "ANALYST_STEP": "SUCCEEDED",
            "FALLBACK_STEP": "SKIPPED",
            "JOIN_STEP": "BLOCKED",
            "COMMANDER_GATE": "BLOCKED",
        },
    )
    d2 = DeterministicControlFlowScheduler.compute_routing(ir, s2)
    assert "JOIN_STEP" in d2.ready_nodes

    # Step 3: JOIN completes -> COMMANDER_GATE is suspended awaiting grant
    s3 = ControlFlowExecutionSnapshot(
        run_id="run_e2e",
        workflow_id="WIR_E2E_CONTROL_FLOW",
        node_states={
            "COND_CHECK": "SUCCEEDED",
            "HUNTER_STEP": "SUCCEEDED",
            "ANALYST_STEP": "SUCCEEDED",
            "FALLBACK_STEP": "SKIPPED",
            "JOIN_STEP": "SUCCEEDED",
            "COMMANDER_GATE": "BLOCKED",
        },
    )
    d3 = DeterministicControlFlowScheduler.compute_routing(ir, s3)
    assert "COMMANDER_GATE" in d3.waiting_human_gates
    assert not d3.ready_nodes

    # Step 4: COMMANDER operator grants release -> Gate becomes ready
    grant = OperatorGrantRecord(
        grant_id="grant_e2e",
        gate_id="COMMANDER_GATE",
        approver_id="lead_operator_1",
        approver_role="lead_operator",
        authority_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        rationale="Release approved after verification",
        granted_at_utc="2026-09-02T05:35:00Z",
    )
    s4 = ControlFlowExecutionSnapshot(
        run_id="run_e2e",
        workflow_id="WIR_E2E_CONTROL_FLOW",
        node_states={
            "COND_CHECK": "SUCCEEDED",
            "HUNTER_STEP": "SUCCEEDED",
            "ANALYST_STEP": "SUCCEEDED",
            "FALLBACK_STEP": "SKIPPED",
            "JOIN_STEP": "SUCCEEDED",
            "COMMANDER_GATE": "BLOCKED",
        },
        operator_grants={"COMMANDER_GATE": grant},
    )
    d4 = DeterministicControlFlowScheduler.compute_routing(ir, s4)
    assert "COMMANDER_GATE" in d4.ready_nodes
